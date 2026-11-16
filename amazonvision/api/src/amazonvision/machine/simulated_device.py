"""Simulated ESP32 firmware. Same protocol (machine/protocol.py) and same state table
(domain/machine.py) the real firmware must follow, with simulated physics and fault injection."""

import asyncio
import contextlib
import json
import logging
import secrets
import time
import zlib
from collections import OrderedDict
from collections.abc import Coroutine
from dataclasses import dataclass
from typing import Any

from amazonvision.domain.machine import CYCLE_STATES, FaultCode, MachineState, Trigger, next_state
from amazonvision.domain.quality import Destination
from amazonvision.machine.protocol import (
    AbortReason,
    AckPayload,
    CaptureReadyEvt,
    CommandName,
    ConfigurePayload,
    CycleAbortedEvt,
    CycleAbortedPayload,
    CycleCompletedEvt,
    CycleCompletedPayload,
    DeviceAck,
    DeviceHeartbeat,
    DeviceNak,
    DeviceStatus,
    FaultEvt,
    FaultPayload,
    NakCode,
    ProtocolError,
    SensorChangedEvt,
    SensorChangedPayload,
    SensorName,
    StateChangedEvt,
    StateChangedPayload,
    encode,
    parse_host_line,
)

log = logging.getLogger("amazonvision.sim.device")

S = MachineState
T = Trigger
FW_VERSION = "sim-1.0"
_SAFE_STATES = {S.DISARMED, S.FAULT, S.ESTOP, S.MAINTENANCE}


@dataclass
class SimPhysics:
    """Travel times of the simulated item, in real milliseconds (divided by speed)."""

    travel_to_s1_ms: int = 1500
    leave_s1_ms: int = 300
    travel_to_s2_ms: int = 1500
    leave_s2_ms: int = 400


@dataclass
class SimFaults:
    s1_missing: bool = False
    s2_missing: bool = False
    exit_blocked: bool = False
    duplicate_events: bool = False
    silent: bool = False


class SimulatedDevice:
    HEARTBEAT_S = 1.0
    WATCHDOG_S = 0.05
    CMD_CACHE = 16

    def __init__(self, *, speed: float = 1.0, physics: SimPhysics | None = None) -> None:
        if speed < 1:
            raise ValueError("speed >= 1")
        self.speed = speed
        self.physics = physics or SimPhysics()
        self.faults = SimFaults()
        self._out: asyncio.Queue[bytes] = asyncio.Queue()
        self._loops: list[asyncio.Task[Any]] = []
        self._work: set[asyncio.Task[Any]] = set()
        # physical inputs survive a reboot
        self.s1 = False
        self.s2 = False
        self.estop = False
        self._boot()

    # ------------------------------------------------------------ lifecycle

    def _boot(self) -> None:
        self.boot_id = secrets.token_hex(4)
        self._seq = 0
        self.session_id: str | None = None
        self.state = S.ESTOP if self.estop else S.DISARMED
        self.config: ConfigurePayload | None = None
        self.config_hash: str | None = None
        self.fault: FaultCode | None = None
        self.lot_id: int | None = None
        self.cycle_id: int | None = None
        self.destination: Destination | None = None
        self.motor_on = False
        self.servo_deg = 0
        self._cmd_cache: OrderedDict[str, tuple[str, dict[str, Any]]] = OrderedDict()
        self._booted_at = time.monotonic()
        self._last_host = time.monotonic()

    async def start(self) -> None:
        self._loops = [
            asyncio.create_task(self._heartbeat_loop()),
            asyncio.create_task(self._watchdog_loop()),
        ]

    async def close(self) -> None:
        for task in [*self._loops, *self._work]:
            task.cancel()
        for task in [*self._loops, *self._work]:
            with contextlib.suppress(asyncio.CancelledError):
                await task
        self._loops, self._work = [], set()

    async def read_line(self) -> bytes:
        return await self._out.get()

    async def write(self, data: bytes) -> None:
        for line in data.split(b"\n"):
            if line.strip():
                self._handle(line)

    # ------------------------------------------------------------ fault injection

    def reboot(self) -> None:
        self._cancel_work()
        self._boot()

    def press_estop(self) -> None:
        self.estop = True
        self._emit_sensor(SensorName.ESTOP, True)
        self._transition(T.ESTOP_PRESSED, abort_reason=AbortReason.ESTOP)

    def release_estop(self) -> None:
        self.estop = False
        self._emit_sensor(SensorName.ESTOP, False)
        self._transition(T.ESTOP_RELEASED)

    def remove_items(self) -> None:
        if self.s1:
            self.s1 = False
            self._emit_sensor(SensorName.S1, False)
        if self.s2:
            self.s2 = False
            self._emit_sensor(SensorName.S2, False)

    # ------------------------------------------------------------ output

    def _status(self) -> DeviceStatus:
        return DeviceStatus(
            s1=self.s1,
            s2=self.s2,
            estop=self.estop,
            motor_on=self.motor_on,
            servo_deg_cmd=self.servo_deg,
            configured=self.config is not None,
            lot_id=self.lot_id,
            cycle_id=self.cycle_id,
            destination=self.destination,
            fault=self.fault,
            uptime_ms=int((time.monotonic() - self._booted_at) * 1000) % 4_294_967_296,
        )

    def _emit(self, cls: type, **fields: Any) -> None:
        if self.faults.silent:
            return
        self._seq += 1
        message = cls(
            boot_id=self.boot_id,
            session_id=self.session_id,
            seq=self._seq,
            state=self.state,
            **fields,
        )
        line = encode(message)
        self._out.put_nowait(line)
        if self.faults.duplicate_events and message.type == "evt":
            self._out.put_nowait(line)

    def _emit_sensor(self, sensor: SensorName, active: bool) -> None:
        self._emit(
            SensorChangedEvt,
            cycle_id=self.cycle_id,
            payload=SensorChangedPayload(sensor=sensor, active=active),
        )

    def _set_sensor(self, sensor: SensorName, active: bool) -> None:
        attr = sensor.value.lower()
        if getattr(self, attr) != active:
            setattr(self, attr, active)
            self._emit_sensor(sensor, active)

    def _reply(
        self,
        cmd_id: str | None,
        name: CommandName | None,
        *,
        code: NakCode | None = None,
        detail: str | None = None,
        payload: AckPayload | None = None,
    ) -> None:
        if code is None:
            fields: dict[str, Any] = {
                "cmd_id": cmd_id,
                "name": name,
                "payload": payload or AckPayload(),
            }
            self._emit(DeviceAck, **fields)
            kind = "ack"
        else:
            fields = {"cmd_id": cmd_id, "code": code, "detail": detail}
            self._emit(DeviceNak, **fields)
            kind = "nak"
        if cmd_id is not None:
            self._cmd_cache[cmd_id] = (kind, fields)
            while len(self._cmd_cache) > self.CMD_CACHE:
                self._cmd_cache.popitem(last=False)

    # ------------------------------------------------------------ state machine

    def _cancel_work(self) -> None:
        current = asyncio.current_task()
        for task in list(self._work):
            if task is not current:
                task.cancel()
        self._work.clear()

    def _spawn(self, coro: Coroutine[Any, Any, None]) -> None:
        task = asyncio.create_task(coro)
        self._work.add(task)
        task.add_done_callback(self._work.discard)

    def _actuators_safe(self) -> None:
        self.motor_on = False
        if self.config is not None:
            self.servo_deg = self.config.servo_rest_deg

    def _transition(
        self,
        trigger: Trigger,
        *,
        fault: FaultCode | None = None,
        abort_reason: AbortReason | None = None,
    ) -> bool:
        target = next_state(self.state, trigger)
        if target is None:
            return False
        previous = self.state
        self.state = target
        aborting = previous in CYCLE_STATES and target in _SAFE_STATES
        entering_fault = target is S.FAULT and previous is not S.FAULT
        if target in _SAFE_STATES:
            self._cancel_work()
            self._actuators_safe()
        if previous is target:
            return True
        if entering_fault:
            self.fault = fault or FaultCode.INTERNAL
        self._emit(
            StateChangedEvt,
            cycle_id=self.cycle_id,
            payload=StateChangedPayload(
                from_state=previous,
                to_state=target,
                trigger=trigger,
                fault=self.fault if target is S.FAULT else None,
            ),
        )
        if entering_fault:
            self._emit(FaultEvt, cycle_id=self.cycle_id, payload=FaultPayload(code=self.fault))
        if aborting and self.cycle_id is not None:
            reason = abort_reason or (
                AbortReason(self.fault.value)
                if target is S.FAULT and self.fault
                else AbortReason.STOP
            )
            self._emit(
                CycleAbortedEvt, cycle_id=self.cycle_id, payload=CycleAbortedPayload(reason=reason)
            )
            self._clear_cycle()
        return True

    def _clear_cycle(self) -> None:
        self.lot_id = None
        self.cycle_id = None
        self.destination = None

    async def _sleep(self, ms: float, *, physical: bool = True) -> None:
        await asyncio.sleep(ms / 1000 / (self.speed if physical else 1))

    # ------------------------------------------------------------ host input

    def _handle(self, raw: bytes) -> None:
        if self.faults.silent:
            return
        self._last_host = time.monotonic()
        try:
            msg = parse_host_line(raw)
        except ProtocolError as exc:
            self._reply(None, None, code=exc.code, detail=exc.detail[:80])
            return
        if msg.type == "hb":
            return
        cached = self._cmd_cache.get(msg.cmd_id)
        if cached is not None:
            kind, fields = cached
            self._emit(DeviceAck if kind == "ack" else DeviceNak, **fields, duplicate=True)
            return
        if msg.name is CommandName.HELLO:
            self._on_hello(msg)
            return
        if self.session_id is None and msg.name is not CommandName.GET_STATUS:
            self._reply(msg.cmd_id, msg.name, code=NakCode.NO_SESSION)
            return
        if self.session_id is not None and msg.session_id != self.session_id:
            self._emit(DeviceNak, cmd_id=msg.cmd_id, code=NakCode.SESSION_MISMATCH)
            return
        handler = getattr(self, f"_on_{msg.name.value.lower()}")
        handler(msg)

    def _invalid_state(self, msg: Any) -> None:
        self._reply(msg.cmd_id, msg.name, code=NakCode.INVALID_STATE, detail=f"estado {self.state}")

    def _on_hello(self, msg: Any) -> None:
        self.session_id = msg.session_id
        self._transition(T.HELLO, fault=FaultCode.SESSION_REPLACED)
        self._reply(msg.cmd_id, msg.name, payload=AckPayload(fw_version=FW_VERSION))

    def _on_configure(self, msg: Any) -> None:
        if self.state not in (S.DISARMED, S.READY):
            return self._invalid_state(msg)
        self.config = msg.payload
        raw = json.dumps(msg.payload.model_dump(mode="json"), sort_keys=True).encode()
        self.config_hash = f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"
        self.servo_deg = msg.payload.servo_rest_deg
        self._reply(msg.cmd_id, msg.name, payload=AckPayload(config_hash=self.config_hash))

    def _on_arm(self, msg: Any) -> None:
        if self.state is not S.DISARMED:
            return self._invalid_state(msg)
        if self.config is None:
            return self._reply(msg.cmd_id, msg.name, code=NakCode.NOT_CONFIGURED)
        if self.estop or self.s1 or self.s2:
            detail = "emergencia acionada" if self.estop else "sensor ocupado"
            return self._reply(
                msg.cmd_id, msg.name, code=NakCode.PRECONDITION_FAILED, detail=detail
            )
        self._transition(T.ARM)
        self._reply(msg.cmd_id, msg.name)

    def _on_stop(self, msg: Any) -> None:
        if not self._transition(T.STOP, abort_reason=AbortReason.STOP):
            return self._invalid_state(msg)
        self._reply(msg.cmd_id, msg.name)

    def _on_start_cycle(self, msg: Any) -> None:
        if self.state is not S.READY:
            return self._invalid_state(msg)
        if self.s2:
            return self._reply(
                msg.cmd_id, msg.name, code=NakCode.PRECONDITION_FAILED, detail="S2 ocupado"
            )
        self.lot_id, self.cycle_id = msg.lot_id, msg.cycle_id
        self._reply(msg.cmd_id, msg.name)
        self._transition(T.START_CYCLE)
        self._spawn(self._run_to_inspection(msg.cycle_id))

    def _on_decision(self, msg: Any) -> None:
        if self.state not in (S.INSPECTING, S.REVIEW_HOLD):
            return self._invalid_state(msg)
        if msg.cycle_id != self.cycle_id:
            return self._reply(msg.cmd_id, msg.name, code=NakCode.CYCLE_MISMATCH)
        self.destination = msg.payload.destination
        self._cancel_work()
        self._reply(msg.cmd_id, msg.name)
        self._transition(T.DECISION)
        self._spawn(self._run_to_exit(msg.cycle_id))

    def _on_hold_for_review(self, msg: Any) -> None:
        if self.state is not S.INSPECTING:
            return self._invalid_state(msg)
        if msg.cycle_id != self.cycle_id:
            return self._reply(msg.cmd_id, msg.name, code=NakCode.CYCLE_MISMATCH)
        self._cancel_work()
        self._reply(msg.cmd_id, msg.name)
        self._transition(T.HOLD_FOR_REVIEW)

    def _on_clear_fault(self, msg: Any) -> None:
        if self.state is not S.FAULT:
            return self._invalid_state(msg)
        if self.s1 or self.s2:
            return self._reply(
                msg.cmd_id, msg.name, code=NakCode.PRECONDITION_FAILED, detail="sensor ocupado"
            )
        self.fault = None
        self._transition(T.CLEAR_FAULT)
        self._reply(msg.cmd_id, msg.name)

    def _on_enter_maintenance(self, msg: Any) -> None:
        if not self._transition(T.ENTER_MAINTENANCE):
            return self._invalid_state(msg)
        self._reply(msg.cmd_id, msg.name)

    def _on_exit_maintenance(self, msg: Any) -> None:
        if not self._transition(T.EXIT_MAINTENANCE):
            return self._invalid_state(msg)
        self._reply(msg.cmd_id, msg.name)

    def _on_get_status(self, msg: Any) -> None:
        self._reply(msg.cmd_id, msg.name, payload=AckPayload(status=self._status()))

    def _on_test_motor(self, msg: Any) -> None:
        if self.state is not S.MAINTENANCE:
            return self._invalid_state(msg)
        self._reply(msg.cmd_id, msg.name)

        async def run() -> None:
            self.motor_on = True
            await self._sleep(msg.payload.run_ms, physical=False)
            self.motor_on = False

        self._spawn(run())

    def _on_test_servo(self, msg: Any) -> None:
        if self.state is not S.MAINTENANCE:
            return self._invalid_state(msg)
        self._reply(msg.cmd_id, msg.name)

        async def run() -> None:
            self.servo_deg = msg.payload.angle_deg
            await self._sleep(msg.payload.hold_ms, physical=False)
            self._actuators_safe()

        self._spawn(run())

    # ------------------------------------------------------------ simulated physics

    def _timeout(self, fault: FaultCode) -> None:
        self._transition(T.TIMEOUT, fault=fault)

    async def _run_to_inspection(self, cycle_id: int) -> None:
        cfg = self.config
        assert cfg is not None
        if not self.s1:
            self.motor_on = True
            travel = self.physics.travel_to_s1_ms
            if self.faults.s1_missing or travel >= cfg.s1_timeout_ms:
                await self._sleep(cfg.s1_timeout_ms)
                return self._timeout(FaultCode.S1_TIMEOUT)
            await self._sleep(travel)
            self._set_sensor(SensorName.S1, True)
            self.motor_on = False
        self._transition(T.S1_PRESENT)
        await self._sleep(cfg.settle_ms)
        self._transition(T.SETTLED)
        self._emit(CaptureReadyEvt, cycle_id=cycle_id)
        # Decision deadline is a communication deadline: not accelerated.
        await self._sleep(cfg.decision_timeout_ms, physical=False)
        if self.state is S.INSPECTING and self.cycle_id == cycle_id:
            self._timeout(FaultCode.DECISION_TIMEOUT)

    async def _run_to_exit(self, cycle_id: int) -> None:
        cfg = self.config
        assert cfg is not None
        p = self.physics
        self.motor_on = True
        await self._sleep(p.leave_s1_ms)
        self._set_sensor(SensorName.S1, False)
        if self.faults.s2_missing or p.leave_s1_ms + p.travel_to_s2_ms >= cfg.s2_timeout_ms:
            await self._sleep(cfg.s2_timeout_ms - p.leave_s1_ms)
            return self._timeout(FaultCode.S2_TIMEOUT)
        await self._sleep(p.travel_to_s2_ms)
        self._set_sensor(SensorName.S2, True)
        self.motor_on = False
        self._transition(T.S2_PRESENT)

        if self.destination is Destination.REJECTED:
            self.servo_deg = cfg.servo_reject_deg
            self.motor_on = cfg.reject_motor_ms > 0
            await self._sleep(max(cfg.reject_hold_ms, cfg.reject_motor_ms))
            self.motor_on = False
            self.servo_deg = cfg.servo_rest_deg
        self._transition(T.SORT_DONE)

        self.motor_on = True
        started = time.monotonic()
        await self._sleep(p.leave_s2_ms)
        if not self.faults.exit_blocked:
            self._set_sensor(SensorName.S2, False)
        await self._sleep(max(cfg.release_ms - p.leave_s2_ms, 0))
        limit_s = cfg.release_max_ms / 1000 / self.speed
        while self.s1 or self.s2:
            if time.monotonic() - started >= limit_s:
                return self._timeout(FaultCode.EXIT_BLOCKED)
            await self._sleep(20, physical=False)
        self.motor_on = False
        destination = self.destination
        assert destination is not None
        self._transition(T.RELEASED)
        self._emit(
            CycleCompletedEvt,
            cycle_id=cycle_id,
            payload=CycleCompletedPayload(destination=destination),
        )
        self._clear_cycle()

    # ------------------------------------------------------------ background loops

    async def _heartbeat_loop(self) -> None:
        while True:
            self._emit(DeviceHeartbeat, payload=self._status())
            await asyncio.sleep(self.HEARTBEAT_S)

    async def _watchdog_loop(self) -> None:
        while True:
            await asyncio.sleep(self.WATCHDOG_S)
            if self.faults.silent or self.session_id is None:
                continue
            limit_ms = self.config.link_timeout_ms if self.config else 2000
            if (time.monotonic() - self._last_host) * 1000 < limit_ms:
                continue
            if self.state in CYCLE_STATES:
                self._transition(T.LINK_LOST, fault=FaultCode.LINK_LOST)
            elif self.state in (S.READY, S.MAINTENANCE):
                self._transition(T.LINK_LOST)
