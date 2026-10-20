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
        self._opener = opener or (lambda: serial.Serial(port, baud_rate, timeout=READ_TIMEOUT_S))
        self._serial: serial.Serial | None = None
        self._queue: asyncio.Queue[bytes | None] = asyncio.Queue()
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()
        self._loop: asyncio.AbstractEventLoop | None = None

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
