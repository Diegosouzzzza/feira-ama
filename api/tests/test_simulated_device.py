import asyncio
from collections.abc import AsyncIterator, Callable
from typing import Any

import pytest

from amazonvision.domain.machine import TRANSITIONS, MachineState, Trigger
from amazonvision.machine.protocol import (
    ArmCmd,
    ClearFaultCmd,
    ConfigureCmd,
    ConfigurePayload,
    DecisionCmd,
    DecisionPayload,
    GetStatusCmd,
    HelloCmd,
    HoldForReviewCmd,
    HostHeartbeat,
    StartCycleCmd,
    encode,
    parse_device_line,
)
from amazonvision.machine.simulated_device import SimulatedDevice

pytestmark = pytest.mark.anyio

SESSION = "5e1a9c03"
CONFIG = ConfigurePayload(
    sensor_debounce_ms=20,
    s1_timeout_ms=3000,
    settle_ms=200,
    decision_timeout_ms=600,
    s2_timeout_ms=3000,
    servo_rest_deg=10,
    servo_reject_deg=75,
    reject_hold_ms=200,
    reject_motor_ms=0,
    release_ms=500,
    release_max_ms=2000,
    link_timeout_ms=2000,
)


class Driver:
    def __init__(self, device: SimulatedDevice) -> None:
        self.device = device
        self.messages: list[Any] = []
        self._claimed: set[int] = set()
        self._n = 0

    async def send(self, cls: type, *, cmd_id: str | None = None, **fields: Any) -> Any:
        self._n += 1
        cmd_id = cmd_id or f"t{self._n}"
        await self.device.write(encode(cls(session_id=SESSION, cmd_id=cmd_id, **fields)))
        return await self.wait(lambda m: m.type in ("ack", "nak") and m.cmd_id == cmd_id)

    async def heartbeat(self) -> None:
        await self.device.write(encode(HostHeartbeat(session_id=SESSION)))

    async def wait(self, predicate: Callable[[Any], bool], timeout: float = 3.0) -> Any:
        """First match among unclaimed messages already read, else keep reading."""
        for index, message in enumerate(self.messages):
            if index not in self._claimed and predicate(message):
                self._claimed.add(index)
                return message
        async with asyncio.timeout(timeout):
            while True:
                message = parse_device_line(await self.device.read_line())
                self.messages.append(message)
                if predicate(message):
                    self._claimed.add(len(self.messages) - 1)
                    return message

    async def wait_event(self, name: str, timeout: float = 3.0) -> Any:
        return await self.wait(lambda m: m.type == "evt" and m.name == name, timeout)

    async def ready(self) -> None:
        assert (await self.send(HelloCmd)).type == "ack"
        assert (await self.send(ConfigureCmd, payload=CONFIG)).type == "ack"
        assert (await self.send(ArmCmd)).type == "ack"
        assert self.device.state is MachineState.READY

    def events(self, name: str) -> list[Any]:
        return [m for m in self.messages if m.type == "evt" and m.name == name]


@pytest.fixture
async def device() -> AsyncIterator[SimulatedDevice]:
    dev = SimulatedDevice(speed=50)
    await dev.start()
    yield dev
    await dev.close()


@pytest.fixture
def host(device: SimulatedDevice) -> Driver:
    return Driver(device)


async def test_boots_disarmed_and_beats_without_session(host: Driver):
    beat = await host.wait(lambda m: m.type == "hb")
    assert beat.state is MachineState.DISARMED
    assert beat.session_id is None
    assert beat.payload.configured is False


async def test_requires_session_except_status(host: Driver):
    assert (await host.send(ArmCmd)).code == "NO_SESSION"
    assert (await host.send(GetStatusCmd)).type == "ack"


async def test_arm_requires_configuration(host: Driver):
    await host.send(HelloCmd)
    assert (await host.send(ArmCmd)).code == "NOT_CONFIGURED"


async def test_full_rejected_cycle(host: Driver):
    await host.ready()
    await host.send(StartCycleCmd, lot_id=1, cycle_id=7)
    capture = await host.wait_event("CAPTURE_READY")
    assert capture.cycle_id == 7
    assert host.device.state is MachineState.INSPECTING
    ack = await host.send(DecisionCmd, cycle_id=7, payload=DecisionPayload(destination="REJECTED"))
    assert ack.type == "ack"
    done = await host.wait_event("CYCLE_COMPLETED")
    assert done.cycle_id == 7
    assert done.payload.destination == "REJECTED"
    assert done.state is MachineState.READY
    assert host.device.s1 is False and host.device.s2 is False
    sensors = [(e.payload.sensor, e.payload.active) for e in host.events("SENSOR_CHANGED")]
    assert sensors == [("S1", True), ("S1", False), ("S2", True), ("S2", False)]


async def test_repeated_cmd_id_does_not_execute_twice(host: Driver):
    await host.ready()
    first = await host.send(StartCycleCmd, cmd_id="same", lot_id=1, cycle_id=8)
    again = await host.send(StartCycleCmd, cmd_id="same", lot_id=1, cycle_id=8)
    assert first.duplicate is False
    assert again.duplicate is True
    starts = [e for e in host.events("STATE_CHANGED") if e.payload.trigger is Trigger.START_CYCLE]
    assert len(starts) == 1


async def test_decision_must_match_state_and_cycle(host: Driver):
    await host.ready()
    early = await host.send(
        DecisionCmd, cycle_id=9, payload=DecisionPayload(destination="APPROVED")
    )
    assert early.code == "INVALID_STATE"
    await host.send(StartCycleCmd, lot_id=1, cycle_id=9)
    await host.wait_event("CAPTURE_READY")
    wrong = await host.send(
        DecisionCmd, cycle_id=99, payload=DecisionPayload(destination="APPROVED")
    )
    assert wrong.code == "CYCLE_MISMATCH"


async def test_missing_s1_faults_and_aborts(host: Driver):
    await host.ready()
    host.device.faults.s1_missing = True
    await host.send(StartCycleCmd, lot_id=1, cycle_id=10)
    fault = await host.wait_event("FAULT")
    assert fault.payload.code == "S1_TIMEOUT"
    aborted = await host.wait_event("CYCLE_ABORTED")
    assert aborted.cycle_id == 10
    assert aborted.payload.reason == "S1_TIMEOUT"
    assert host.device.motor_on is False
    assert (await host.send(ClearFaultCmd)).type == "ack"
    assert host.device.state is MachineState.DISARMED


async def test_decision_timeout_faults(host: Driver):
    await host.ready()
    await host.send(StartCycleCmd, lot_id=1, cycle_id=11)
    await host.wait_event("CAPTURE_READY")
    fault = await host.wait_event("FAULT", timeout=2)
    assert fault.payload.code == "DECISION_TIMEOUT"


async def test_review_hold_waits_beyond_decision_timeout(host: Driver):
    await host.ready()
    await host.send(StartCycleCmd, lot_id=1, cycle_id=12)
    await host.wait_event("CAPTURE_READY")
    await host.send(HoldForReviewCmd, cycle_id=12)
    for _ in range(4):
        await asyncio.sleep(0.25)
        await host.heartbeat()
    assert host.device.state is MachineState.REVIEW_HOLD
    await host.send(DecisionCmd, cycle_id=12, payload=DecisionPayload(destination="APPROVED"))
    done = await host.wait_event("CYCLE_COMPLETED")
    assert done.payload.destination == "APPROVED"


async def test_link_loss_during_cycle_faults(host: Driver):
    await host.send(HelloCmd)
    await host.send(ConfigureCmd, payload=CONFIG.model_copy(update={"link_timeout_ms": 500}))
    await host.send(ArmCmd)
    await host.send(StartCycleCmd, lot_id=1, cycle_id=13)
    await host.wait_event("CAPTURE_READY")
    await host.send(HoldForReviewCmd, cycle_id=13)
    fault = await host.wait_event("FAULT", timeout=2)
    assert fault.payload.code == "LINK_LOST"
    assert (await host.wait_event("CYCLE_ABORTED")).payload.reason == "LINK_LOST"


async def test_new_hello_mid_cycle_aborts(host: Driver):
    await host.ready()
    await host.send(StartCycleCmd, lot_id=1, cycle_id=14)
    await host.wait_event("CAPTURE_READY")
    await host.send(HelloCmd)
    aborted = await host.wait_event("CYCLE_ABORTED")
    assert aborted.payload.reason == "SESSION_REPLACED"
    assert host.device.state is MachineState.FAULT


async def test_hello_in_fault_keeps_original_fault(host: Driver):
    await host.ready()
    host.device.faults.s1_missing = True
    await host.send(StartCycleCmd, lot_id=1, cycle_id=15)
    await host.wait_event("FAULT")
    await host.send(HelloCmd)
    assert host.device.fault == "S1_TIMEOUT"


async def test_estop_aborts_and_release_disarms(host: Driver):
    await host.ready()
    await host.send(StartCycleCmd, lot_id=1, cycle_id=16)
    await host.wait_event("CAPTURE_READY")
    host.device.press_estop()
    assert (await host.wait_event("CYCLE_ABORTED")).payload.reason == "ESTOP"
    assert host.device.state is MachineState.ESTOP
    assert (await host.send(ArmCmd)).code == "INVALID_STATE"
    host.device.release_estop()
    assert host.device.state is MachineState.DISARMED


async def test_exit_blocked_requires_clearing_items(host: Driver):
    await host.ready()
    host.device.faults.exit_blocked = True
    await host.send(StartCycleCmd, lot_id=1, cycle_id=17)
    await host.wait_event("CAPTURE_READY")
    await host.send(DecisionCmd, cycle_id=17, payload=DecisionPayload(destination="APPROVED"))
    fault = await host.wait_event("FAULT")
    assert fault.payload.code == "EXIT_BLOCKED"
    assert (await host.send(ClearFaultCmd)).code == "PRECONDITION_FAILED"
    host.device.remove_items()
    assert (await host.send(ClearFaultCmd)).type == "ack"


async def test_reboot_changes_boot_id_and_drops_session(host: Driver):
    await host.ready()
    old = host.device.boot_id
    host.device.reboot()
    beat = await host.wait(lambda m: m.type == "hb" and m.boot_id != old)
    assert beat.session_id is None
    assert beat.state is MachineState.DISARMED
    assert beat.seq == 1


async def test_every_message_is_contract_valid_and_ordered(host: Driver):
    await host.ready()
    await host.send(StartCycleCmd, lot_id=1, cycle_id=18)
    await host.wait_event("CAPTURE_READY")
    await host.send(DecisionCmd, cycle_id=18, payload=DecisionPayload(destination="APPROVED"))
    await host.wait_event("CYCLE_COMPLETED")
    seqs = [m.seq for m in host.messages]
    assert seqs == sorted(seqs)
    assert len(set(seqs)) == len(seqs)
    for evt in host.events("STATE_CHANGED"):
        p = evt.payload
        assert TRANSITIONS[(p.from_state, p.trigger)] is p.to_state
