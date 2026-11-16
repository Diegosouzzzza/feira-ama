"""The coordinator reopens the device link on its own after it breaks (cable unplugged)."""

import asyncio
import secrets
from pathlib import Path
from uuid import uuid4

import pytest

from amazonvision.camera.base import NoCamera
from amazonvision.config import Settings
from amazonvision.core.bus import EventBus
from amazonvision.domain.machine import MachineState
from amazonvision.machine.coordinator import Coordinator
from amazonvision.machine.link import LinkClosed
from amazonvision.machine.protocol import (
    AckPayload,
    CommandName,
    DeviceAck,
    DeviceHeartbeat,
    DeviceNak,
    DeviceStatus,
    NakCode,
    parse_host_line,
)
from amazonvision.services.container import Recorder
from amazonvision.storage.db import Database
from amazonvision.vision.classifier import ModelManager

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


class TinyDevice:
    """A fake link good enough to answer HELLO, and that can be told to drop the connection."""

    def __init__(self) -> None:
        self.starts = 0
        self.closed_calls = 0
        self._queue: asyncio.Queue[bytes | None] = asyncio.Queue()
        self._seq = 0
        self._broken = False
        self.boot_id = secrets.token_hex(4)

    async def start(self) -> None:
        self.starts += 1
        self._broken = False

    def break_link(self) -> None:
        """Simulate the cable coming out: the next (or a pending) read fails."""
        self._broken = True
        self._queue.put_nowait(None)

    async def read_line(self) -> bytes:
        while True:
            line = await self._queue.get()
            if self._broken:
                raise LinkClosed("cabo solto")
            assert line is not None
            return line

    async def write(self, data: bytes) -> None:
        for raw in data.split(b"\n"):
            if not raw.strip():
                continue
            command = parse_host_line(raw)
            if command.name is CommandName.HELLO:
                self._seq += 1
                ack = DeviceAck(
                    boot_id=self.boot_id,
                    session_id=command.session_id,
                    seq=self._seq,
                    state=MachineState.DISARMED,
                    cmd_id=command.cmd_id,
                    name=command.name,
                    payload=AckPayload(fw_version="test-1.0"),
                )
                self._queue.put_nowait(ack.model_dump_json(exclude_none=True).encode() + b"\n")

    async def close(self) -> None:
        self.closed_calls += 1


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(_env_file=None, data_dir=tmp_path / "data", log_to_file=False)


async def wait_until(condition, timeout: float = 2.0) -> None:
    deadline = asyncio.get_running_loop().time() + timeout
    while not condition():
        assert asyncio.get_running_loop().time() < deadline, "condição não atingida"
        await asyncio.sleep(0.01)


async def test_coordinator_reopens_the_link_after_it_breaks(settings: Settings):
    settings.ensure_data_dirs()
    db = Database(settings.db_path)
    await db.open()
    try:
        bus = EventBus()
        device = TinyDevice()
        models = ModelManager(settings)
        record = Recorder(db)
        coordinator = Coordinator(
            settings, db, bus, device, NoCamera(), models, record, "COM-teste"
        )
        coordinator.RECONNECT_DELAY_S = 0.02  # type: ignore[misc]

        await coordinator.start()
        try:
            await wait_until(lambda: coordinator.connected)
            assert device.starts == 1
            first_boot = coordinator.boot_id

            device.break_link()
            await wait_until(lambda: not coordinator.connected)

            await wait_until(lambda: device.starts == 2, timeout=3)
            await wait_until(lambda: coordinator.connected, timeout=3)
            assert coordinator.boot_id == first_boot  # same simulated board, same identity
        finally:
            await coordinator.stop()
    finally:
        await db.close()


async def test_reconnect_loop_stops_when_the_coordinator_stops(settings: Settings):
    settings.ensure_data_dirs()
    db = Database(settings.db_path)
    await db.open()
    try:
        bus = EventBus()
        device = TinyDevice()
        models = ModelManager(settings)
        record = Recorder(db)
        coordinator = Coordinator(
            settings, db, bus, device, NoCamera(), models, record, "COM-teste"
        )
        coordinator.RECONNECT_DELAY_S = 10.0  # type: ignore[misc] - never fires in this test

        await coordinator.start()
        await wait_until(lambda: coordinator.connected)
        device.break_link()
        await wait_until(lambda: not coordinator.connected)

        await asyncio.wait_for(coordinator.stop(), timeout=2)
        assert device.starts == 1  # stop() happened before the (slow) reconnect attempt
    finally:
        await db.close()


class BootingDevice(TinyDevice):
    """An ESP32 that was reset by the port being opened (DTR/RTS on Windows).

    While it boots it hears nothing: the first HELLOs are lost. Once up it has no session and
    says so in its heartbeat; it answers NAK NO_SESSION to anything but HELLO."""

    def __init__(self) -> None:
        super().__init__()
        self.booted = False
        self.session: str | None = None
        self.hellos_lost = 0
        self.hellos_answered = 0
        self.no_session_naks = 0

    def _emit(self, message) -> None:
        self._queue.put_nowait(message.model_dump_json(exclude_none=True).encode() + b"\n")

    def finish_boot(self) -> None:
        self.booted = True
        self.heartbeat()

    def heartbeat(self) -> None:
        self._seq += 1
        status = DeviceStatus(
            s1=False,
            s2=False,
            estop=False,
            motor_on=False,
            servo_deg_cmd=0,
            configured=False,
            uptime_ms=1000 * self._seq,
        )
        self._emit(
            DeviceHeartbeat(
                boot_id=self.boot_id,
                session_id=self.session,
                seq=self._seq,
                state=MachineState.DISARMED,
                payload=status,
            )
        )

    async def write(self, data: bytes) -> None:
        for raw in data.split(b"\n"):
            if not raw.strip():
                continue
            message = parse_host_line(raw)
            if message.type != "cmd":
                continue
            if not self.booted:
                if message.name is CommandName.HELLO:
                    self.hellos_lost += 1
                continue
            self._seq += 1
            common = {"boot_id": self.boot_id, "seq": self._seq, "cmd_id": message.cmd_id}
            if message.name is CommandName.HELLO:
                self.hellos_answered += 1
                self.session = message.session_id
                self._emit(
                    DeviceAck(
                        **common,
                        session_id=self.session,
                        state=MachineState.DISARMED,
                        name=message.name,
                        payload=AckPayload(fw_version="test-1.0"),
                    )
                )
            elif message.session_id != self.session:
                self.no_session_naks += 1
                self._emit(
                    DeviceNak(
                        **common,
                        session_id=self.session,
                        state=MachineState.DISARMED,
                        code=NakCode.NO_SESSION,
                    )
                )
            else:
                self._emit(
                    DeviceAck(
                        **common,
                        session_id=self.session,
                        state=MachineState.MAINTENANCE,
                        name=message.name,
                    )
                )


def make_coordinator(settings: Settings, db: Database, device: TinyDevice) -> Coordinator:
    return Coordinator(
        settings,
        db,
        EventBus(),
        device,
        NoCamera(),
        ModelManager(settings),
        Recorder(db),
        "COM-teste",
    )


async def test_heartbeat_without_session_triggers_a_new_hello(settings: Settings):
    """The initial HELLO expires while the board boots; its first heartbeat must fix it."""
    settings.ensure_data_dirs()
    db = Database(settings.db_path)
    await db.open()
    try:
        device = BootingDevice()
        coordinator = make_coordinator(settings, db, device)
        coordinator.ACK_TIMEOUT_S = 0.02  # type: ignore[misc]

        await coordinator.start()
        try:
            # The handshake timed out: nothing known about the board, and no usable session.
            assert device.hellos_lost == Coordinator.SEND_ATTEMPTS
            assert coordinator.boot_id is None
            assert coordinator.session_id is None
            assert not coordinator.connected

            device.finish_boot()  # hb with session_id = None

            await wait_until(lambda: coordinator.firmware == "test-1.0")  # HELLO acknowledged
            assert coordinator.session_id is not None
            assert coordinator.session_id == device.session
            assert coordinator.connected
            assert coordinator.boot_id == device.boot_id
            assert device.hellos_answered == 1

            # Commands now carry the session the board accepted: no NAK NO_SESSION.
            result = await coordinator.execute("maintenance_enter", uuid4(), None)
            assert result.state is MachineState.MAINTENANCE
            assert device.no_session_naks == 0

            # Later heartbeats with the right session do not start another handshake.
            device.heartbeat()
            device.heartbeat()
            await asyncio.sleep(0.1)
            assert device.hellos_answered == 1
        finally:
            await coordinator.stop()
    finally:
        await db.close()


async def test_board_that_lost_its_session_gets_a_new_one(settings: Settings):
    """Same boot_id, but the heartbeat stops carrying our session: handshake again."""
    settings.ensure_data_dirs()
    db = Database(settings.db_path)
    await db.open()
    try:
        device = BootingDevice()
        device.booted = True
        coordinator = make_coordinator(settings, db, device)
        await coordinator.start()
        try:
            await wait_until(lambda: coordinator.connected)
            first = coordinator.session_id
            assert first is not None and first == device.session

            device.session = None
            device.heartbeat()

            await wait_until(lambda: device.hellos_answered == 2)
            await wait_until(lambda: coordinator.session_id == device.session)
            assert coordinator.session_id != first
        finally:
            await coordinator.stop()
    finally:
        await db.close()


async def test_unanswered_hello_is_retried_one_at_a_time(settings: Settings):
    """A board that keeps ignoring HELLO gets one attempt at a time, not one per message."""
    settings.ensure_data_dirs()
    db = Database(settings.db_path)
    await db.open()
    try:
        device = BootingDevice()
        coordinator = make_coordinator(settings, db, device)
        coordinator.ACK_TIMEOUT_S = 0.05  # type: ignore[misc]
        await coordinator.start()
        try:
            lost = device.hellos_lost
            for _ in range(5):  # a burst of heartbeats: only one handshake may be running
                device.heartbeat()
            await wait_until(lambda: device.hellos_lost == lost + Coordinator.SEND_ATTEMPTS)
            await asyncio.sleep(0.2)
            assert device.hellos_lost == lost + Coordinator.SEND_ATTEMPTS
            assert coordinator.session_id is None

            device.finish_boot()
            await wait_until(lambda: device.session is not None)
            await wait_until(lambda: coordinator.session_id == device.session)
        finally:
            await coordinator.stop()
    finally:
        await db.close()
