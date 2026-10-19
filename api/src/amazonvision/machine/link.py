from typing import Protocol


class LinkClosed(Exception):
    pass


class Link(Protocol):
    """Byte-line transport to the ESP32 (serial port, or the in-process simulator)."""

    async def start(self) -> None: ...

    async def write(self, data: bytes) -> None: ...

    async def read_line(self) -> bytes:
        """Next line from the device. Raises LinkClosed when the link is gone."""
        ...

    async def close(self) -> None: ...
