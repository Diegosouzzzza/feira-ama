import re
from pathlib import Path

import pytest

from amazonvision.domain.machine import (
    CYCLE_STATES,
    MOTION_STATES,
    TIMEOUT_FAULTS,
    TRANSITIONS,
    MachineState,
    Trigger,
    next_state,
)

DOC = Path(__file__).resolve().parents[2] / "docs" / "maquina-de-estados.md"
ROW = re.compile(r"^\| `([A-Z0-9_]+)` \| `([A-Z0-9_]+)` \| `([A-Z0-9_]+)` \|$")


def _doc_transitions() -> dict[tuple[MachineState, Trigger], MachineState]:
    section = DOC.read_text(encoding="utf-8").split("## Tabela de transições", 1)[1]
    rows = {}
    for line in section.splitlines():
        match = ROW.match(line.strip())
        if match:
            state, trigger, nxt = match.groups()
            key = (MachineState(state), Trigger(trigger))
            assert key not in rows, f"linha duplicada no documento: {key}"
            rows[key] = MachineState(nxt)
    return rows


def test_documented_table_matches_code():
    assert _doc_transitions() == TRANSITIONS


def test_every_state_is_reachable_from_disarmed():
    seen = {MachineState.DISARMED}
    frontier = [MachineState.DISARMED]
    while frontier:
        state = frontier.pop()
        for (src, _), dst in TRANSITIONS.items():
            if src is state and dst not in seen:
                seen.add(dst)
                frontier.append(dst)
    assert seen == set(MachineState)


@pytest.mark.parametrize("state", sorted(CYCLE_STATES))
def test_cycle_states_can_always_be_stopped_safely(state):
    assert next_state(state, Trigger.STOP) is MachineState.DISARMED
    assert next_state(state, Trigger.LINK_LOST) is MachineState.FAULT
    assert next_state(state, Trigger.HELLO) is MachineState.FAULT
    assert next_state(state, Trigger.ESTOP_PRESSED) is MachineState.ESTOP


@pytest.mark.parametrize("state", list(MachineState))
def test_estop_wins_everywhere(state):
    expected = None if state is MachineState.ESTOP else MachineState.ESTOP
    assert next_state(state, Trigger.ESTOP_PRESSED) is expected


@pytest.mark.parametrize("state", [MachineState.DISARMED, MachineState.FAULT, MachineState.ESTOP])
def test_no_direct_motion_from_safe_states(state):
    for (src, _), dst in TRANSITIONS.items():
        if src is state:
            assert dst not in MOTION_STATES


def test_only_ready_starts_a_cycle():
    starters = {src for (src, trig) in TRANSITIONS if trig is Trigger.START_CYCLE}
    assert starters == {MachineState.READY}


def test_decision_only_while_waiting_for_it():
    states = {src for (src, trig) in TRANSITIONS if trig is Trigger.DECISION}
    assert states == {MachineState.INSPECTING, MachineState.REVIEW_HOLD}


def test_review_hold_has_no_decision_timeout():
    assert next_state(MachineState.REVIEW_HOLD, Trigger.TIMEOUT) is None


def test_timeouts_have_fault_codes():
    timeout_states = {src for (src, trig) in TRANSITIONS if trig is Trigger.TIMEOUT}
    assert timeout_states == set(TIMEOUT_FAULTS)


def test_unknown_transition_is_rejected():
    assert next_state(MachineState.READY, Trigger.DECISION) is None
