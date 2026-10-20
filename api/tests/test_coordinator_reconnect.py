"""The coordinator reopens the device link on its own after it breaks (cable unplugged)."""

import asyncio
import secrets
from pathlib import Path

import pytest

from amazonvision.camera.base import NoCamera
from amazonvision.config import Settings
from amazonvision.core.bus import EventBus
from amazonvision.domain.machine import MachineState
from amazonvision.machine.coordinator import Coordinator
from amazonvision.machine.link import LinkClosed
from amazonvision.machine.protocol import AckPayload, CommandName, DeviceAck, parse_host_line
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
