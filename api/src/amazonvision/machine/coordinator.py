"""Cycle coordinator. Single owner of the device link; turns device events into recorded cycles.

The ESP32 is the authority on physical state: this class only requests transitions and reacts to
what the device reports. It never replays a decision after a reconnection or a reboot."""

import asyncio
import contextlib
import logging
import secrets
import sqlite3
import time
from collections import OrderedDict
from collections.abc import Awaitable, Callable, Coroutine
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from amazonvision.camera.base import Camera, CameraError
from amazonvision.config import Settings
from amazonvision.core.bus import EventBus
from amazonvision.core.clock import to_db, utc_now
from amazonvision.domain.machine import CYCLE_STATES, FaultCode, MachineState
from amazonvision.domain.quality import AutoDecision, Destination, QualityPolicy, decide
from amazonvision.machine.bench_config import FAULT_TEXT, bench_config_for
from amazonvision.machine.link import Link, LinkClosed
from amazonvision.machine.protocol import (
    PROTOCOL_VERSION,
    ArmCmd,
    ClearFaultCmd,
    ConfigureCmd,
    DecisionCmd,
    DecisionPayload,
    DeviceAck,
    DeviceNak,
    EnterMaintenanceCmd,
    EventName,
    ExitMaintenanceCmd,
    HelloCmd,
    HoldForReviewCmd,
    HostHeartbeat,
    MotorTestCmd,
    MotorTestPayload,
    NakCode,
    ProtocolError,
    ServoTestCmd,
    ServoTestPayload,
    StartCycleCmd,
    StopCmd,
    encode,
    parse_device_line,
)
from amazonvision.schemas.api import (
    CycleOut,
    DecidedBy,
    DeviceLink,
    EventSource,
    LotOut,
    MachineCommandResult,
    MachineInfo,
    SensorSnapshot,
    Severity,
)
from amazonvision.schemas.errors import ApiError, ErrorCode
from amazonvision.schemas.events import (
    Component,
    ConnectionData,
    ConnectionLostEvent,
    ConnectionRestoredEvent,
    CycleAbortedData,
    CycleAbortedEvent,
    CycleCompletedData,
    CycleCompletedEvent,
    DecisionAcceptedData,
    DecisionAcceptedEvent,
    FaultData,
    FaultEvent,
    InspectionReadyEvent,
    SensorChangedData,
    SensorChangedEvent,
    StateChangedData,
    StateChangedEvent,
)
from amazonvision.storage import cycles as cycle_repo
from amazonvision.storage import inspections as insp_repo
from amazonvision.storage.db import Database
from amazonvision.storage.events import add_event
from amazonvision.storage.images import save_image
from amazonvision.storage.lots import get_open_lot, get_summary
from amazonvision.storage.products import get_product_row
from amazonvision.vision.classifier import ModelManager

log = logging.getLogger("amazonvision.coordinator")

S = MachineState
Recorder = Callable[..., Awaitable[None]]


class DeviceRejected(Exception):
    def __init__(self, code: NakCode, detail: str | None) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


@dataclass
class ActiveCycle:
    cycle_id: int
    lot_id: int
    product_id: str
    policy: QualityPolicy
    inspection_id: int | None = None
    capture_started: bool = False
    awaiting_review: bool = False
    abort_override: str | None = None


def _serial_down(message: str = "A placa não está respondendo.") -> ApiError:
    return ApiError(
        ErrorCode.SERIAL_DISCONNECTED, message, "Verifique o cabo USB e a alimentação da placa."
    )


def _rejected_to_api(exc: DeviceRejected) -> ApiError:
    detail = (exc.detail or "").lower()
    if exc.code is NakCode.PRECONDITION_FAILED and "sensor" in detail:
        return ApiError(
            ErrorCode.INVALID_STATE,
            "Há uma peça sobre um sensor.",
            "Retire a peça da esteira e tente de novo.",
        )
    if exc.code is NakCode.PRECONDITION_FAILED and "emerg" in detail:
        return ApiError(
            ErrorCode.INVALID_STATE, "A emergência está acionada.", "Solte o botão de emergência."
        )
    return ApiError(
        ErrorCode.INVALID_STATE,
        f"A placa recusou o comando ({exc.code}).",
        "Confira o estado da máquina no diagnóstico.",
    )


class Coordinator:
    ACK_TIMEOUT_S = 0.3
    SEND_ATTEMPTS = 3
    HOST_HEARTBEAT_S = 0.5
    WATCHDOG_S = 0.1
    LEDGER_SIZE = 256

    def __init__(
        self,
        settings: Settings,
        db: Database,
        bus: EventBus,
        link: Link | None,
        camera: Camera,
        models: ModelManager,
        record: Recorder,
        port_label: str | None = None,
        clock: Callable[[], datetime] = utc_now,
    ) -> None:
        self._settings = settings
        self._db = db
        self._bus = bus
        self._link = link
        self._camera = camera
        self._models = models
        self._record = record
        self._port_label = port_label
        self._clock = clock
        self.on_change: Callable[[], Awaitable[None]] | None = None

        self.state: MachineState | None = None
        self.fault: FaultCode | None = None
        self.sensors: SensorSnapshot | None = None
        self.boot_id: str | None = None
        self.firmware: str | None = None
        self.session_id: str | None = None
        self.connected = False
        self.last_seen: datetime | None = None
        self.running = False
        self.cycle: ActiveCycle | None = None

        self._session_db_id: int | None = None
        self._config_hash: str | None = None
        self._last_seq = -1
        self._last_seen_mono = 0.0
        self._lost_announced = False
        self._pending: dict[str, asyncio.Future[Any]] = {}
        self._tasks: set[asyncio.Task[Any]] = set()
        self._loops: list[asyncio.Task[Any]] = []
        self._op_lock = asyncio.Lock()
        self._cycle_lock = asyncio.Lock()
        self._ledger: OrderedDict[UUID, MachineCommandResult] = OrderedDict()
        self._infer = ThreadPoolExecutor(max_workers=1, thread_name_prefix="av-infer")

    # ------------------------------------------------------------ lifecycle

    async def start(self) -> None:
        now = to_db(self._clock())
        stale = await self._db.run(
            lambda conn: cycle_repo.abort_running_cycles(conn, "SERVICE_RESTARTED", now)
        )
        for cycle_id in stale:
            await self._record(
                "CYCLE_ABORTED",
                severity=Severity.WARNING,
                source=EventSource.HOST,
                data={"cycle_id": cycle_id, "reason": "SERVICE_RESTARTED"},
            )
        lot = await self._db.run(get_open_lot)
        if lot is not None:
            self._models.load(lot.product_id, lot.model_id)
        if self._link is None:
            return
        await self._link.start()
        self._loops = [
            asyncio.create_task(self._reader()),
            asyncio.create_task(self._host_heartbeat()),
            asyncio.create_task(self._watchdog()),
        ]
        try:
            await self._handshake()
        except ApiError:
            log.warning("placa não respondeu ao HELLO na inicialização")

    async def stop(self) -> None:
        if self._link is not None and self.connected and self.state in CYCLE_STATES:
            with contextlib.suppress(Exception):
                await self._send(
                    StopCmd,
                )
        for task in [*self._loops, *self._tasks]:
            task.cancel()
        for task in [*self._loops, *self._tasks]:
            with contextlib.suppress(asyncio.CancelledError, Exception):
                await task
        if self._link is not None:
            await self._link.close()
        if self._session_db_id is not None:
            closed = to_db(self._clock())
            session_id = self._session_db_id
            with contextlib.suppress(Exception):
                await self._db.run(
                    lambda conn: cycle_repo.close_device_session(conn, session_id, closed)
                )
        self._infer.shutdown(wait=False, cancel_futures=True)

    def busy(self) -> bool:
        return self.running or self.cycle is not None

    async def _changed(self) -> None:
        if self.on_change is not None:
            await self.on_change()

    def _spawn(self, coro: Coroutine[Any, Any, Any]) -> None:
        task = asyncio.create_task(coro)
        self._tasks.add(task)
        task.add_done_callback(self._task_done)

    def _task_done(self, task: asyncio.Task[Any]) -> None:
        self._tasks.discard(task)
        if not task.cancelled() and task.exception() is not None:
            log.error("tarefa do coordenador falhou", exc_info=task.exception())

    # ------------------------------------------------------------ views for the status service

    def machine_info(self) -> MachineInfo:
        pending = None
        if self.cycle is not None and self.cycle.awaiting_review:
            pending = self.cycle.inspection_id
        fault_text = FAULT_TEXT.get(self.fault) if self.fault else None
        return MachineInfo(
            state=self.state,
            fault=self.fault,
            fault_message=fault_text[0] if fault_text else None,
            fault_recovery=fault_text[1] if fault_text else None,
            sensors=self.sensors,
            link=DeviceLink(
                connected=self.connected,
                port=self._port_label,
                boot_id=self.boot_id,
                firmware_version=self.firmware,
                last_seen_at=self.last_seen,
            ),
            running=self.running,
            pending_review_inspection_id=pending,
        )

    async def current_cycle(self) -> CycleOut | None:
        if self.cycle is None:
            return None
        cycle_id = self.cycle.cycle_id
        cycle = await self._db.run(lambda conn: cycle_repo.get_cycle(conn, cycle_id))
        return cycle.model_copy(update={"machine_state": self.state}) if cycle else None

    # ------------------------------------------------------------ link plumbing

    async def _send(self, cls: type, **fields: Any) -> DeviceAck:
        if self._link is None:
            raise _serial_down("Nenhuma placa configurada neste modo.")
        if self.session_id is None:
            raise _serial_down()
        cmd = cls(session_id=self.session_id, cmd_id=secrets.token_hex(6), **fields)
        return await self._exchange(cmd)

    async def _exchange(self, cmd: Any) -> DeviceAck:
        assert self._link is not None
        future: asyncio.Future[Any] = asyncio.get_running_loop().create_future()
        self._pending[cmd.cmd_id] = future
        line = encode(cmd)
        try:
            for _ in range(self.SEND_ATTEMPTS):
                try:
                    await self._link.write(line)
                except LinkClosed as exc:
                    raise _serial_down() from exc
                try:
                    reply = await asyncio.wait_for(asyncio.shield(future), self.ACK_TIMEOUT_S)
                    break
                except TimeoutError:
                    continue
            else:
                raise _serial_down()
        finally:
            self._pending.pop(cmd.cmd_id, None)
        if isinstance(reply, DeviceNak):
            raise DeviceRejected(reply.code, reply.detail)
        return reply

    async def _handshake(self) -> None:
        self.session_id = secrets.token_hex(4)
        ack = await self._exchange(
            HelloCmd(session_id=self.session_id, cmd_id=secrets.token_hex(6))
        )
        self.boot_id = ack.boot_id
        self.firmware = ack.payload.fw_version
        self.state = ack.state
        self._config_hash = None
        opened = to_db(self._clock())
        boot_id, session_id, firmware = ack.boot_id, self.session_id, self.firmware
        port = self._port_label
        self._session_db_id = await self._db.run(
            lambda conn: cycle_repo.open_device_session(
                conn,
                boot_id=boot_id,
                session_id=session_id,
                firmware_version=firmware,
                protocol_version=PROTOCOL_VERSION,
                port=port,
                opened_at=opened,
            )
        )
        await self._record(
            "DEVICE_SESSION_OPENED",
            source=EventSource.HOST,
            data={"boot_id": boot_id, "session_id": session_id, "firmware": firmware},
        )
        await self._changed()

    async def _reader(self) -> None:
        assert self._link is not None
        while True:
            try:
                line = await self._link.read_line()
            except LinkClosed:
                await self._mark_lost("Conexão com a placa encerrada.")
                return
            try:
                message = parse_device_line(line)
            except ProtocolError as exc:
                log.warning("mensagem inválida da placa: %s", exc)
                continue
            try:
                await self._on_message(message)
            except ApiError:
                log.exception("falha ao registrar mensagem da placa")

    async def _host_heartbeat(self) -> None:
        assert self._link is not None
        while True:
            await asyncio.sleep(self.HOST_HEARTBEAT_S)
            if self.session_id is not None:
                with contextlib.suppress(LinkClosed):
                    await self._link.write(encode(HostHeartbeat(session_id=self.session_id)))

    async def _watchdog(self) -> None:
        silence_s = self._settings.device_silence_ms / 1000
        while True:
            await asyncio.sleep(self.WATCHDOG_S)
            if self.connected and time.monotonic() - self._last_seen_mono > silence_s:
                await self._mark_lost("A placa parou de responder.")

    async def _mark_lost(self, message: str) -> None:
        if not self.connected:
            return
        self.connected = False
        self.running = False
        self._lost_announced = True
        self._bus.publish(
            ConnectionLostEvent, ConnectionData(component=Component.DEVICE, message=message)
        )
        await self._record(
            "CONNECTION_LOST",
            severity=Severity.WARNING,
            source=EventSource.HOST,
            data={"component": "device"},
        )
        if self.cycle is not None:
            await self._finish_aborted(self.cycle.cycle_id, "DEVICE_SILENT")
        await self._changed()

    # ------------------------------------------------------------ device messages

    async def _on_message(self, message: Any) -> None:
        self._last_seen_mono = time.monotonic()
        self.last_seen = self._clock()
        if not self.connected:
            self.connected = True
            if self._lost_announced:
                self._lost_announced = False
                self._bus.publish(
                    ConnectionRestoredEvent,
                    ConnectionData(component=Component.DEVICE, message="Placa respondendo."),
                )
        if self.boot_id is not None and message.boot_id != self.boot_id:
            await self._on_reboot(message.boot_id)
        elif self.boot_id is None:
            self.boot_id = message.boot_id
        if message.seq <= self._last_seq:
            return
        self._last_seq = message.seq

        if message.type in ("ack", "nak"):
            future = self._pending.get(message.cmd_id) if message.cmd_id else None
            if future is not None and not future.done():
                future.set_result(message)
            return
        if message.type == "hb":
            await self._apply_heartbeat(message)
            return
        if message.session_id != self.session_id:
            return
        await self._store_device_event(message)
        handler = {
            EventName.STATE_CHANGED: self._on_state_changed,
            EventName.SENSOR_CHANGED: self._on_sensor_changed,
            EventName.CAPTURE_READY: self._on_capture_ready,
            EventName.CYCLE_COMPLETED: self._on_cycle_completed,
            EventName.CYCLE_ABORTED: self._on_cycle_aborted,
            EventName.FAULT: self._on_fault,
        }[message.name]
        await handler(message)

    async def _store_device_event(self, message: Any) -> None:
        severity = {
            EventName.FAULT: Severity.ERROR,
            EventName.CYCLE_ABORTED: Severity.WARNING,
        }.get(message.name, Severity.INFO)
        occurred = to_db(self._clock())
        payload = message.payload.model_dump(mode="json")
        lot_id = self.cycle.lot_id if self.cycle else None
        await self._db.run(
            lambda conn: add_event(
                conn,
                source=EventSource.DEVICE,
                type=message.name.value,
                severity=severity,
                occurred_at=occurred,
                data=payload,
                lot_id=lot_id if message.cycle_id else None,
                cycle_id=message.cycle_id,
                boot_id=message.boot_id,
                device_seq=message.seq,
            )
        )

    async def _apply_heartbeat(self, message: Any) -> None:
        status = message.payload
        sensors = SensorSnapshot(s1=status.s1, s2=status.s2, estop=status.estop)
        changed = (self.state, self.fault, self.sensors) != (message.state, status.fault, sensors)
        self.state = message.state
        self.fault = status.fault
        self.sensors = sensors
        if changed:
            await self._changed()

    async def _on_reboot(self, new_boot_id: str) -> None:
        log.warning("placa reiniciou (boot %s -> %s)", self.boot_id, new_boot_id)
        old_session = self._session_db_id
        self.boot_id = new_boot_id
        self._last_seq = -1
        self.session_id = None
        self._session_db_id = None
        self.state = None
        self.running = False
        closed = to_db(self._clock())
        if old_session is not None:
            await self._db.run(
                lambda conn: cycle_repo.close_device_session(conn, old_session, closed)
            )
        await self._record(
            "DEVICE_REBOOTED",
            severity=Severity.WARNING,
            source=EventSource.HOST,
            data={"boot_id": new_boot_id},
        )
        if self.cycle is not None:
            await self._finish_aborted(self.cycle.cycle_id, "DEVICE_REBOOTED")
        self._spawn(self._rehandshake())

    async def _rehandshake(self) -> None:
        try:
            await self._handshake()
        except ApiError:
            log.warning("placa reiniciada não respondeu ao HELLO")

    async def _on_state_changed(self, message: Any) -> None:
        payload = message.payload
        self.state = payload.to_state
        if payload.to_state is S.FAULT:
            self.fault = payload.fault
            self.running = False
        elif payload.from_state is S.FAULT:
            self.fault = None
        self._bus.publish(
            StateChangedEvent,
            StateChangedData(
                from_state=payload.from_state,
                to_state=payload.to_state,
                trigger=payload.trigger,
                fault=payload.fault,
            ),
            lot_id=self.cycle.lot_id if self.cycle else None,
            cycle_id=message.cycle_id,
        )

    async def _on_sensor_changed(self, message: Any) -> None:
        sensor, active = message.payload.sensor, message.payload.active
        current = self.sensors or SensorSnapshot(s1=False, s2=False, estop=False)
        self.sensors = current.model_copy(update={sensor.value.lower(): active})
        self._bus.publish(
            SensorChangedEvent,
            SensorChangedData(sensor=sensor.value, active=active),
            cycle_id=message.cycle_id,
        )

    async def _on_fault(self, message: Any) -> None:
        code = message.payload.code
        self.fault = code
        self.running = False
        text, recovery = FAULT_TEXT[code]
        self._bus.publish(
            FaultEvent,
            FaultData(code=code, message=text, recovery=recovery),
            cycle_id=message.cycle_id,
        )

    async def _on_capture_ready(self, message: Any) -> None:
        cycle = self.cycle
        if cycle is None or cycle.cycle_id != message.cycle_id or cycle.capture_started:
            return
        cycle.capture_started = True
        self._spawn(self._inspect(cycle))

    async def _on_cycle_completed(self, message: Any) -> None:
        destination = message.payload.destination
        cycle_id = message.cycle_id
        ended = to_db(self._clock())
        await self._db.run(
            lambda conn: cycle_repo.complete_cycle(conn, cycle_id, destination, ended)
        )
        lot_id = self.cycle.lot_id if self.cycle and self.cycle.cycle_id == cycle_id else None
        if lot_id is not None:
            self.cycle = None
            summary = await self._db.run(lambda conn: get_summary(conn, lot_id))
            assert summary is not None
            self._bus.publish(
                CycleCompletedEvent,
                CycleCompletedData(destination=destination, summary=summary),
                lot_id=lot_id,
                cycle_id=cycle_id,
            )
        await self._changed()
        self._spawn(self._start_next_cycle())

    async def _on_cycle_aborted(self, message: Any) -> None:
        reason = message.payload.reason.value
        if self.cycle is not None and self.cycle.cycle_id == message.cycle_id:
            reason = self.cycle.abort_override or reason
        await self._finish_aborted(message.cycle_id, reason)

    async def _finish_aborted(self, cycle_id: int, reason: str) -> None:
        self.running = False
        ended = to_db(self._clock())
        changed = await self._db.run(
            lambda conn: cycle_repo.abort_cycle(conn, cycle_id, reason, ended)
        )
        lot_id = self.cycle.lot_id if self.cycle and self.cycle.cycle_id == cycle_id else None
        if self.cycle is not None and self.cycle.cycle_id == cycle_id:
            self.cycle = None
        if changed and lot_id is not None:
            summary = await self._db.run(lambda conn: get_summary(conn, lot_id))
            assert summary is not None
            self._bus.publish(
                CycleAbortedEvent,
                CycleAbortedData(reason=reason, summary=summary),
                lot_id=lot_id,
                cycle_id=cycle_id,
            )
        await self._changed()

    # ------------------------------------------------------------ the inspection step

    async def _halt(
        self, cycle: ActiveCycle, reason: str, component: Component, message: str
    ) -> None:
        """Stop the bench because the host cannot complete the inspection."""
        cycle.abort_override = reason
        self.running = False
        self._bus.publish(ConnectionLostEvent, ConnectionData(component=component, message=message))
        await self._record(
            reason,
            severity=Severity.ERROR,
            source=EventSource.HOST,
            data={"cycle_id": cycle.cycle_id, "message": message},
            lot_id=cycle.lot_id,
        )
        try:
            await self._send(StopCmd)
        except (ApiError, DeviceRejected):
            log.exception("não foi possível parar a placa após %s", reason)

    async def _inspect(self, cycle: ActiveCycle) -> None:
        requested_at = self._clock()
        try:
            frame = await self._camera.capture(not_before=requested_at, timeout_s=1.0)
        except CameraError as exc:
            await self._halt(cycle, "CAMERA_UNAVAILABLE", Component.CAMERA, exc.message)
            return

        classifier = self._models.classifier
        if classifier is None or not self._models.ready_for(cycle.product_id):
            await self._halt(cycle, "MODEL_NOT_READY", Component.MODEL, "Modelo não carregado.")
            return
        try:
            prediction = await asyncio.get_running_loop().run_in_executor(
                self._infer, classifier.classify, frame
            )
        except Exception:
            log.exception("falha na inferência")
            await self._halt(cycle, "MODEL_ERROR", Component.MODEL, "Falha ao analisar a imagem.")
            return

        result = decide(prediction.scores, cycle.policy)
        data_root = self._settings.data_root
        try:
            relative, sha = await asyncio.to_thread(
                save_image, data_root, cycle.lot_id, cycle.cycle_id, frame.data, frame.extension
            )
        except OSError:
            log.exception("falha ao gravar imagem")
            self._db.healthy = False
            await self._halt(cycle, "STORAGE_ERROR", Component.STORAGE, "Falha ao gravar a imagem.")
            return

        new = insp_repo.NewInspection(
            cycle_id=cycle.cycle_id,
            image_path=relative,
            image_sha256=sha,
            captured_at=to_db(frame.captured_at),
            frame_age_ms=max((self._clock() - frame.captured_at).total_seconds() * 1000, 0.0),
            model_id=classifier.model_id,
            scores=prediction.scores,
            predicted_grade=result.predicted_grade,
            confidence=result.confidence,
            latency_ms=prediction.latency_ms,
            policy_threshold=cycle.policy.threshold,
            policy_version=cycle.policy.version,
            auto_decision=result.decision,
            review_reason=result.review_reason,
            created_at=to_db(self._clock()),
        )
        try:
            inspection = await self._db.run(lambda conn: insp_repo.insert_inspection(conn, new))
        except ApiError:
            await self._halt(
                cycle, "STORAGE_ERROR", Component.STORAGE, "Falha ao gravar a inspeção."
            )
            return
        cycle.inspection_id = inspection.id
        self._bus.publish(
            InspectionReadyEvent, inspection, lot_id=cycle.lot_id, cycle_id=cycle.cycle_id
        )

        try:
            if result.decision is AutoDecision.REVIEW:
                cycle.awaiting_review = True
                await self._send(HoldForReviewCmd, cycle_id=cycle.cycle_id)
                await self._changed()
            else:
                destination = Destination(result.decision.value)
                await self._send(
                    DecisionCmd,
                    cycle_id=cycle.cycle_id,
                    payload=DecisionPayload(destination=destination),
                )
                self._bus.publish(
                    DecisionAcceptedEvent,
                    DecisionAcceptedData(
                        inspection_id=inspection.id,
                        destination=destination,
                        decided_by=DecidedBy.AUTO,
                    ),
                    lot_id=cycle.lot_id,
                    cycle_id=cycle.cycle_id,
                )
        except (ApiError, DeviceRejected):
            # The device enforces its own decision deadline and will fault the cycle.
            log.exception("decisão não entregue à placa (ciclo %s)", cycle.cycle_id)

    # ------------------------------------------------------------ cycles

    async def _start_next_cycle(self) -> None:
        async with self._cycle_lock:
            if not (self.running and self.connected and self.state is S.READY):
                return
            if self.cycle is not None:
                return
            if not self._db.healthy:
                self.running = False
                await self._changed()
                return
            lot = await self._db.run(get_open_lot)
            if lot is None:
                self.running = False
                await self._changed()
                return
            started = to_db(self._clock())
            session_db_id = self._session_db_id
            cycle_out = await self._db.run(
                lambda conn: cycle_repo.insert_cycle(
                    conn, lot_id=lot.id, device_session_id=session_db_id, started_at=started
                )
            )
            threshold = await self._db.run(lambda conn: _lot_threshold(conn, lot.id))
            self.cycle = ActiveCycle(
                cycle_id=cycle_out.id,
                lot_id=lot.id,
                product_id=lot.product_id,
                policy=QualityPolicy(threshold=threshold),
            )
            try:
                await self._send(StartCycleCmd, lot_id=lot.id, cycle_id=cycle_out.id)
            except (ApiError, DeviceRejected) as exc:
                code = exc.code if isinstance(exc, DeviceRejected) else "NO_RESPONSE"
                await self._finish_aborted(cycle_out.id, f"START_REFUSED:{code}")
                return
            await self._changed()

    # ------------------------------------------------------------ operator commands

    async def execute(
        self,
        action: str,
        request_id: UUID,
        expected_state: MachineState | None,
        params: dict[str, int] | None = None,
    ) -> MachineCommandResult:
        async with self._op_lock:
            if request_id in self._ledger:
                return self._ledger[request_id].model_copy(update={"duplicate": True})
            if expected_state is not None and self.state is not expected_state:
                raise ApiError(
                    ErrorCode.INVALID_STATE,
                    f"A máquina está em {self.state}, não em {expected_state}.",
                    "Atualize a tela e tente de novo.",
                )
            handler = {
                "start": self._op_start,
                "pause": self._op_pause,
                "stop": self._op_stop,
                "rearm": self._op_rearm,
                "maintenance_enter": self._op_maintenance_enter,
                "maintenance_exit": self._op_maintenance_exit,
                "test_motor": self._op_test_motor,
                "test_servo": self._op_test_servo,
            }[action]
            await handler(**(params or {}))
            if self.state is None:
                raise _serial_down()
            result = MachineCommandResult(
                request_id=request_id, accepted=True, duplicate=False, state=self.state
            )
            self._ledger[request_id] = result
            while len(self._ledger) > self.LEDGER_SIZE:
                self._ledger.popitem(last=False)
            await self._changed()
            return result

    def _require_device(self) -> None:
        if self._link is None or not self.connected or self.session_id is None:
            raise _serial_down()

    async def _configure_and_arm(self, lot: LotOut) -> None:
        product = await self._db.run(lambda conn: get_product_row(conn, lot.product_id))
        assert product is not None
        config = bench_config_for(self._settings.mode, product["bench_config_json"])
        try:
            ack = await self._send(ConfigureCmd, payload=config)
            self._config_hash = ack.payload.config_hash
            await self._send(ArmCmd)
        except DeviceRejected as exc:
            raise _rejected_to_api(exc) from exc
        self.state = S.READY

    async def _op_start(self) -> None:
        self._require_device()
        lot = await self._db.run(get_open_lot)
        if lot is None:
            raise ApiError(ErrorCode.INVALID_STATE, "Nenhum lote aberto.", "Abra um lote antes.")
        if not self._db.healthy:
            raise ApiError(
                ErrorCode.STORAGE_ERROR,
                "Falha de gravação: novos ciclos estão bloqueados.",
                "Verifique o espaço em disco e reinicie o sistema.",
            )
        if not self._models.ready_for(lot.product_id):
            raise ApiError(ErrorCode.MODEL_NOT_READY, "Modelo do produto não carregado.")
        if self._camera.info().status != "ok":
            raise ApiError(ErrorCode.CAMERA_UNAVAILABLE, "Câmera indisponível.")
        if self.cycle is not None and self.cycle.awaiting_review:
            raise ApiError(
                ErrorCode.REVIEW_REQUIRED,
                "Há uma peça aguardando a decisão do operador.",
                "Decida o destino da peça inconclusiva.",
            )
        if self.state in (S.FAULT, S.ESTOP, S.MAINTENANCE):
            raise ApiError(
                ErrorCode.INVALID_STATE,
                "A máquina precisa ser rearmada antes de iniciar.",
                "Resolva a causa e use Rearmar.",
            )
        if self.state is S.DISARMED:
            await self._configure_and_arm(lot)
        self.running = True
        self._spawn(self._start_next_cycle())

    async def _op_pause(self) -> None:
        self.running = False

    async def _op_stop(self) -> None:
        self._require_device()
        self.running = False
        if self.state in CYCLE_STATES or self.state in (S.READY, S.MAINTENANCE):
            try:
                await self._send(StopCmd)
            except DeviceRejected as exc:
                raise _rejected_to_api(exc) from exc
            if self.state is S.READY or self.state is S.MAINTENANCE:
                self.state = S.DISARMED

    async def _op_rearm(self) -> None:
        self._require_device()
        self.running = False
        if self.state is S.ESTOP:
            raise ApiError(
                ErrorCode.INVALID_STATE,
                "A emergência está acionada.",
                "Solte o botão de emergência e tente de novo.",
            )
        if self.state is S.FAULT:
            try:
                await self._send(ClearFaultCmd)
            except DeviceRejected as exc:
                raise ApiError(
                    ErrorCode.INVALID_STATE,
                    "A causa da falha ainda está presente.",
                    "Retire peças sobre os sensores e tente de novo.",
                ) from exc
            self.state = S.DISARMED
            self.fault = None
        lot = await self._db.run(get_open_lot)
        if self.state is S.DISARMED and lot is not None:
            await self._configure_and_arm(lot)

    # ------------------------------------------------------------ maintenance

    async def _command(self, cls: type, **fields: Any) -> None:
        try:
            ack = await self._send(cls, **fields)
        except DeviceRejected as exc:
            raise _rejected_to_api(exc) from exc
        self.state = ack.state

    async def _op_maintenance_enter(self) -> None:
        """Manual tests of motor and servo. Only with the belt stopped and no cycle."""
        self._require_device()
        if self.running or self.cycle is not None:
            raise ApiError(
                ErrorCode.INVALID_STATE,
                "A esteira está em operação.",
                "Pare a máquina antes de entrar em manutenção.",
            )
        if self.state is S.MAINTENANCE:
            return
        if self.state is S.READY:
            await self._command(StopCmd)
        if self.state is not S.DISARMED:
            raise ApiError(
                ErrorCode.INVALID_STATE,
                "A máquina precisa estar desarmada para entrar em manutenção.",
                "Resolva a falha ou a emergência e tente de novo.",
            )
        await self._command(EnterMaintenanceCmd)

    async def _op_maintenance_exit(self) -> None:
        self._require_device()
        if self.state is S.MAINTENANCE:
            await self._command(ExitMaintenanceCmd)

    def _require_maintenance(self) -> None:
        self._require_device()
        if self.state is not S.MAINTENANCE:
            raise ApiError(
                ErrorCode.INVALID_STATE,
                "Os testes manuais só funcionam em manutenção.",
                "Entre no modo manutenção antes.",
            )

    async def _op_test_motor(self, run_ms: int) -> None:
        self._require_maintenance()
        await self._command(MotorTestCmd, payload=MotorTestPayload(run_ms=run_ms))

    async def _op_test_servo(self, angle_deg: int, hold_ms: int) -> None:
        self._require_maintenance()
        await self._command(
            ServoTestCmd, payload=ServoTestPayload(angle_deg=angle_deg, hold_ms=hold_ms)
        )

    async def decide_review(self, inspection_id: int, destination: Destination) -> bool:
        """Deliver an operator decision for the piece waiting in REVIEW_HOLD.

        Returns False when no piece is waiting for this inspection (decision is record-only)."""
        async with self._op_lock:
            cycle = self.cycle
            if (
                cycle is None
                or cycle.inspection_id != inspection_id
                or not cycle.awaiting_review
                or self.state not in (S.INSPECTING, S.REVIEW_HOLD)
            ):
                return False
            try:
                await self._send(
                    DecisionCmd,
                    cycle_id=cycle.cycle_id,
                    payload=DecisionPayload(destination=destination),
                )
            except DeviceRejected as exc:
                raise _rejected_to_api(exc) from exc
            cycle.awaiting_review = False
            self._bus.publish(
                DecisionAcceptedEvent,
                DecisionAcceptedData(
                    inspection_id=inspection_id,
                    destination=destination,
                    decided_by=DecidedBy.OPERATOR,
                ),
                lot_id=cycle.lot_id,
                cycle_id=cycle.cycle_id,
            )
            return True


def _lot_threshold(conn: sqlite3.Connection, lot_id: int) -> float:
    return conn.execute("SELECT policy_threshold FROM lots WHERE id = ?", (lot_id,)).fetchone()[0]
