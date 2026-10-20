import asyncio
import queue
import time

import pytest
import serial

from amazonvision.machine import serial_link
from amazonvision.machine.link import LinkClosed
from amazonvision.machine.serial_link import SerialLink, list_ports

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


class FakeSerial:
    """Stands in for serial.Serial: readline() blocks until a line is pushed or close()."""

    def __init__(self) -> None:
        self._lines: queue.Queue[bytes] = queue.Queue()
        self.written: list[bytes] = []
        self.closed = False

    def push(self, line: bytes) -> None:
        self._lines.put(line)

    def readline(self) -> bytes:
        while not self.closed:
            try:
                return self._lines.get(timeout=0.02)
            except queue.Empty:
                continue
        return b""

    def write(self, data: bytes) -> int:
        self.written.append(data)
        return len(data)

    def close(self) -> None:
        self.closed = True


def wait_until(condition, timeout: float = 2.0) -> None:
    deadline = time.monotonic() + timeout
    while not condition():
        assert time.monotonic() < deadline, "condição não atingida"
        time.sleep(0.01)


async def test_read_line_returns_what_the_port_sends():
    port = FakeSerial()
    link = SerialLink("COM9", opener=lambda: port)
    await link.start()
    try:
        port.push(b"hello\n")
        line = await asyncio.wait_for(link.read_line(), timeout=1)
        assert line == b"hello\n"
    finally:
        await link.close()


async def test_write_goes_to_the_port():
    port = FakeSerial()
    link = SerialLink("COM9", opener=lambda: port)
    await link.start()
    try:
        await link.write(b"ping\n")
        wait_until(lambda: port.written == [b"ping\n"])
    finally:
        await link.close()


async def test_open_failure_raises_link_closed():
    def opener():
        raise serial.SerialException("porta ocupada")

    link = SerialLink("COM9", opener=opener)
    with pytest.raises(LinkClosed):
        await link.start()


async def test_write_before_start_raises_link_closed():
    link = SerialLink("COM9", opener=lambda: FakeSerial())
    with pytest.raises(LinkClosed):
        await link.write(b"x")


async def test_close_interrupts_a_blocked_read():
    port = FakeSerial()
    link = SerialLink("COM9", opener=lambda: port)
    await link.start()

    read = asyncio.ensure_future(link.read_line())
    await asyncio.sleep(0.05)
    assert not read.done()
    await link.close()
    with pytest.raises(LinkClosed):
        await asyncio.wait_for(read, timeout=1)


async def test_reopening_the_same_link_object_works():
    ports = [FakeSerial(), FakeSerial()]
    calls = iter(ports)
    link = SerialLink("COM9", opener=lambda: next(calls))
    await link.start()
    await link.close()

    await link.start()
    try:
        ports[1].push(b"again\n")
        line = await asyncio.wait_for(link.read_line(), timeout=1)
        assert line == b"again\n"
    finally:
        await link.close()


def test_list_ports_reports_device_description_and_hwid(monkeypatch):
    class FakePortInfo:
        device = "COM5"
        description = "USB-SERIAL CH340"
        hwid = "USB VID:PID=1A86:7523"

    monkeypatch.setattr(serial_link._list_ports, "comports", lambda: [FakePortInfo()])
    ports = list_ports()
    assert ports == [
        {"device": "COM5", "description": "USB-SERIAL CH340", "hwid": "USB VID:PID=1A86:7523"}
    ]
