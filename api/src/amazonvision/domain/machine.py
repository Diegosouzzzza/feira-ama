"""Official bench state machine. The ESP32 firmware and the simulator must implement this table.

Keep in sync with docs/maquina-de-estados.md (a test compares both).
"""

from enum import StrEnum


class MachineState(StrEnum):
    DISARMED = "DISARMED"
    READY = "READY"
    TO_S1 = "TO_S1"
    SETTLING = "SETTLING"
    INSPECTING = "INSPECTING"
    REVIEW_HOLD = "REVIEW_HOLD"
    TO_S2 = "TO_S2"
    SORTING = "SORTING"
    RELEASING = "RELEASING"
    FAULT = "FAULT"
    ESTOP = "ESTOP"
    MAINTENANCE = "MAINTENANCE"


class Trigger(StrEnum):
    # host commands
    HELLO = "HELLO"
    ARM = "ARM"
    STOP = "STOP"
    START_CYCLE = "START_CYCLE"
    DECISION = "DECISION"
    HOLD_FOR_REVIEW = "HOLD_FOR_REVIEW"
    CLEAR_FAULT = "CLEAR_FAULT"
    ENTER_MAINTENANCE = "ENTER_MAINTENANCE"
    EXIT_MAINTENANCE = "EXIT_MAINTENANCE"
    # device-internal
    S1_PRESENT = "S1_PRESENT"
    SETTLED = "SETTLED"
    S2_PRESENT = "S2_PRESENT"
    SORT_DONE = "SORT_DONE"
    RELEASED = "RELEASED"
    TIMEOUT = "TIMEOUT"
    LINK_LOST = "LINK_LOST"
    ESTOP_PRESSED = "ESTOP_PRESSED"
    ESTOP_RELEASED = "ESTOP_RELEASED"


class FaultCode(StrEnum):
    S1_TIMEOUT = "S1_TIMEOUT"
    DECISION_TIMEOUT = "DECISION_TIMEOUT"
    S2_TIMEOUT = "S2_TIMEOUT"
    EXIT_BLOCKED = "EXIT_BLOCKED"
    LINK_LOST = "LINK_LOST"
    SESSION_REPLACED = "SESSION_REPLACED"
    SENSOR_CONFLICT = "SENSOR_CONFLICT"
    INTERNAL = "INTERNAL"


S = MachineState
T = Trigger

CYCLE_STATES: frozenset[MachineState] = frozenset(
    {S.TO_S1, S.SETTLING, S.INSPECTING, S.REVIEW_HOLD, S.TO_S2, S.SORTING, S.RELEASING}
)
MOTION_STATES: frozenset[MachineState] = frozenset({S.TO_S1, S.TO_S2, S.SORTING, S.RELEASING})

TIMEOUT_FAULTS: dict[MachineState, FaultCode] = {
    S.TO_S1: FaultCode.S1_TIMEOUT,
    S.INSPECTING: FaultCode.DECISION_TIMEOUT,
    S.TO_S2: FaultCode.S2_TIMEOUT,
    S.RELEASING: FaultCode.EXIT_BLOCKED,
}


def _build_transitions() -> dict[tuple[MachineState, Trigger], MachineState]:
    table: dict[tuple[MachineState, Trigger], MachineState] = {
        (S.DISARMED, T.HELLO): S.DISARMED,
        (S.DISARMED, T.ARM): S.READY,
        (S.DISARMED, T.ENTER_MAINTENANCE): S.MAINTENANCE,
        (S.READY, T.HELLO): S.DISARMED,
        (S.READY, T.STOP): S.DISARMED,
        (S.READY, T.LINK_LOST): S.DISARMED,
        (S.READY, T.START_CYCLE): S.TO_S1,
        (S.TO_S1, T.S1_PRESENT): S.SETTLING,
        (S.SETTLING, T.SETTLED): S.INSPECTING,
        (S.INSPECTING, T.DECISION): S.TO_S2,
        (S.INSPECTING, T.HOLD_FOR_REVIEW): S.REVIEW_HOLD,
        (S.REVIEW_HOLD, T.DECISION): S.TO_S2,
        (S.TO_S2, T.S2_PRESENT): S.SORTING,
        (S.SORTING, T.SORT_DONE): S.RELEASING,
        (S.RELEASING, T.RELEASED): S.READY,
        (S.FAULT, T.HELLO): S.FAULT,
        (S.FAULT, T.CLEAR_FAULT): S.DISARMED,
        (S.ESTOP, T.HELLO): S.ESTOP,
        (S.ESTOP, T.ESTOP_RELEASED): S.DISARMED,
        (S.MAINTENANCE, T.HELLO): S.DISARMED,
        (S.MAINTENANCE, T.STOP): S.DISARMED,
        (S.MAINTENANCE, T.LINK_LOST): S.DISARMED,
        (S.MAINTENANCE, T.EXIT_MAINTENANCE): S.DISARMED,
    }
    for state in CYCLE_STATES:
        table[(state, T.HELLO)] = S.FAULT
        table[(state, T.STOP)] = S.DISARMED
        table[(state, T.LINK_LOST)] = S.FAULT
    for state in TIMEOUT_FAULTS:
        table[(state, T.TIMEOUT)] = S.FAULT
    for state in MachineState:
        if state is not S.ESTOP:
            table[(state, T.ESTOP_PRESSED)] = S.ESTOP
    return table


TRANSITIONS: dict[tuple[MachineState, Trigger], MachineState] = _build_transitions()


def next_state(state: MachineState, trigger: Trigger) -> MachineState | None:
    """Return the next state, or None when the trigger is not allowed in this state."""
    return TRANSITIONS.get((state, trigger))
