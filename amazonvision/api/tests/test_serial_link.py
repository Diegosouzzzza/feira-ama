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
        port.push(b'{"a":1}\n')
        line = await asyncio.wait_for(link.read_line(), timeout=1)
        assert line == b'{"a":1}\n'
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
        ports[1].push(b'{"again":true}\n')
        line = await asyncio.wait_for(link.read_line(), timeout=1)
        assert line == b'{"again":true}\n'
    finally:
        await link.close()


async def test_bootloader_noise_is_dropped_and_the_next_message_survives():
    """Opening the port resets the ESP32: the ROM prints text at another baud rate first."""
    port = FakeSerial()
    link = SerialLink("COM9", opener=lambda: port)
    await link.start()
    try:
        port.push(b"ets Jun  8 2016 00:22:57\r\n")
        port.push(b"rst:0x1 (POWERON_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)\r\n")
        port.push(b"\xff\xfe\x00\x8f\xc0\r\n")
        port.push(b'"seq":4,"state":"DISARMED"}\n')  # tail of a line cut by the reset
        port.push(b'{"protocol_version":1,"type":"hb"')  # head of a line cut by the reset
        port.push(b'\x00\xf8\xe0{"protocol_version":1,"seq":1}\r\n')  # noise glued in front
        line = await asyncio.wait_for(link.read_line(), timeout=1)
        assert line == b'{"protocol_version":1,"seq":1}\n'
        assert link.discarded == 5
    finally:
        await link.close()


def test_port_is_opened_without_raising_dtr_and_rts(monkeypatch):
    """DTR/RTS drive EN/GPIO0 on the DevKit: raising them at open reboots the board."""
    seen: dict[str, object] = {}

    class RecordingSerial:
        def __init__(self) -> None:
            self.port = None
            self.baudrate = None
            self.timeout = None
            self.write_timeout = None
            self.dtr = True
            self.rts = True

        def open(self) -> None:
            seen.update(port=self.port, baud=self.baudrate, dtr=self.dtr, rts=self.rts)
            seen["write_timeout"] = self.write_timeout

        def reset_input_buffer(self) -> None:
            seen["flushed"] = True

    monkeypatch.setattr(serial_link.serial, "Serial", RecordingSerial)
    serial_link.open_port("COM7", 115200)
    assert seen == {
        "port": "COM7",
        "baud": 115200,
        "dtr": False,
        "rts": False,
        "write_timeout": serial_link.WRITE_TIMEOUT_S,
        "flushed": True,
    }


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
