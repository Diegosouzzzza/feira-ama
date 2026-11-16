"""Link to the real ESP32 over a USB serial port.

pyserial is blocking, so reads happen on a background thread: it pushes each line onto an
asyncio queue the coordinator awaits. Writes go through the same thread so they never
interleave with a read. Closing the port from another thread is pyserial's documented way to
interrupt a blocked read, so `close()` can run from the event loop while the thread is reading."""

import asyncio
import contextlib
import logging
import threading
from collections.abc import Callable

import serial
from serial.tools import list_ports as _list_ports

from amazonvision.machine.link import LinkClosed

log = logging.getLogger("amazonvision.machine.serial")

BAUD_RATE = 115200
READ_TIMEOUT_S = 1.0  # bounds how long close() may wait for the reader thread to notice.
WRITE_TIMEOUT_S = 1.0  # a stuck driver must not hang a command forever.


def open_port(port: str, baud_rate: int) -> serial.Serial:
    """Open the port without raising DTR/RTS.

    On the ESP32 DevKit those two lines drive EN and GPIO0 (auto-reset circuit). pyserial raises
    both when it opens a port, and on Windows that usually reboots the board. Setting them low
    *before* opening keeps the board running with most CH340/CP210x drivers; when a driver
    resets it anyway, the coordinator handshakes again on the first heartbeat."""
    handle = serial.Serial()
    handle.port = port
    handle.baudrate = baud_rate
    handle.timeout = READ_TIMEOUT_S
    handle.write_timeout = WRITE_TIMEOUT_S
    handle.dtr = False
    handle.rts = False
    handle.open()
    with contextlib.suppress(OSError, serial.SerialException):
        handle.reset_input_buffer()  # whatever the board printed before we were listening
    return handle


def clean_line(raw: bytes) -> bytes | None:
    """Keep only what can be a protocol message (one JSON object per line).

    At reset the ESP32 ROM bootloader prints text at 74880 baud ("ets Jun  8 2016...",
    "rst:0x1 (POWERON_RESET)"), which arrives here as garbage, sometimes glued to the start of
    the first real line. Returns None for lines to drop."""
    start = raw.find(b"{")
    if start < 0:
        return None
    line = raw[start:].strip()
    if not line.endswith(b"}"):
        return None  # cut in the middle (port opened or board reset mid-line)
    return line + b"\n"


def list_ports() -> list[dict[str, str | None]]:
    """USB serial ports currently visible to the OS, for the configuration screen."""
    return [
        {"device": p.device, "description": p.description, "hwid": p.hwid}
        for p in _list_ports.comports()
    ]


class SerialLink:
    def __init__(
        self,
        port: str,
        baud_rate: int = BAUD_RATE,
        *,
        opener: Callable[[], serial.Serial] | None = None,
    ) -> None:
        self.port = port
        self.baud_rate = baud_rate
        self._opener = opener or (lambda: open_port(port, baud_rate))
        self._serial: serial.Serial | None = None
        self._queue: asyncio.Queue[bytes | None] = asyncio.Queue()
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()
        self._loop: asyncio.AbstractEventLoop | None = None
        self.discarded = 0  # lines dropped as noise (bootloader text, cut lines)

    async def start(self) -> None:
        self._loop = asyncio.get_running_loop()
        self._stop.clear()
        try:
            self._serial = await asyncio.to_thread(self._opener)
        except (OSError, serial.SerialException) as exc:
            raise LinkClosed(f"não foi possível abrir {self.port}: {exc}") from exc
        self._thread = threading.Thread(target=self._run, name="av-serial", daemon=True)
        self._thread.start()

    def _run(self) -> None:
        assert self._serial is not None
        assert self._loop is not None
        loop = self._loop
        while not self._stop.is_set():
            try:
                line = self._serial.readline()
            except (OSError, serial.SerialException):
                break
            if not line:
                continue  # read timed out; loop again to re-check _stop
            line = clean_line(line)
            if line is None:
                self.discarded += 1
                continue
            with contextlib.suppress(RuntimeError):  # loop closing during shutdown
                loop.call_soon_threadsafe(self._queue.put_nowait, line)
        with contextlib.suppress(RuntimeError):
            loop.call_soon_threadsafe(self._queue.put_nowait, None)

    async def read_line(self) -> bytes:
        line = await self._queue.get()
        if line is None:
            raise LinkClosed(f"porta serial {self.port} fechada")
        return line

    async def write(self, data: bytes) -> None:
        if self._serial is None:
            raise LinkClosed(f"porta serial {self.port} não aberta")
        try:
            await asyncio.to_thread(self._serial.write, data)
        except (OSError, serial.SerialException) as exc:
            raise LinkClosed(str(exc)) from exc

    async def close(self) -> None:
        self._stop.set()
        serial_obj, self._serial = self._serial, None
        if serial_obj is not None:
            with contextlib.suppress(Exception):
                serial_obj.close()
        if self._thread is not None:
            await asyncio.to_thread(self._thread.join, READ_TIMEOUT_S + 1)
            self._thread = None
        # Drain so a stale read_line() call from before close() doesn't hang on an old queue.
        while not self._queue.empty():
            self._queue.get_nowait()
