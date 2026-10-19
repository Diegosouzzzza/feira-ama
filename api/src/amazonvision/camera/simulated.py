import asyncio
import io
import struct
import zlib
from collections.abc import Callable
from datetime import datetime
from itertools import count

from amazonvision.camera.base import CameraError, Frame
from amazonvision.core.clock import utc_now
from amazonvision.schemas.api import CameraInfo
from amazonvision.schemas.errors import ErrorCode
from amazonvision.simulation.images import render
from amazonvision.simulation.scenario import Scenario
from amazonvision.vision.preprocess import load_rgb

SOURCE = "simulada"
_IHDR_END = 8 + 25  # PNG signature + IHDR chunk


def _tagged(png: bytes, serial: int) -> bytes:
    """Same picture, unique bytes: each simulated photo is a distinct file (and hash)."""
    data = b"Comment\x00" + f"amazonvision-sim-{serial}".encode()
    chunk = struct.pack(">I", len(data)) + b"tEXt" + data
    chunk += struct.pack(">I", zlib.crc32(b"tEXt" + data) & 0xFFFFFFFF)
    return png[:_IHDR_END] + chunk + png[_IHDR_END:]


def _as_jpeg(png: bytes) -> bytes:
    buffer = io.BytesIO()
    load_rgb(png).save(buffer, format="JPEG", quality=80)
    return buffer.getvalue()


class SimulatedCamera:
    def __init__(self, scenario: Scenario, clock: Callable[[], datetime] = utc_now) -> None:
        self._scenario = scenario
        self._clock = clock
        self._variants = count()
        self._last_frame_at: datetime | None = None
        self.available = True
        self.fail_next_capture = False
        self._last_drawn = "empty"

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    async def preview(self) -> tuple[bytes, str] | None:
        if not self.available:
            return None
        # Shows the last photographed drawing; never consumes the scenario's planned items.
        return await asyncio.to_thread(_as_jpeg, render(self._last_drawn, 0)), "image/jpeg"

    def info(self) -> CameraInfo:
        if not self.available:
            return CameraInfo(
                status="unavailable", source=SOURCE, last_frame_at=self._last_frame_at
            )
        return CameraInfo(status="ok", source=SOURCE, last_frame_at=self._last_frame_at)

    async def capture(self, not_before: datetime, timeout_s: float) -> Frame:
        if not self.available:
            raise CameraError(ErrorCode.CAMERA_UNAVAILABLE, "Câmera simulada desligada.")
        if self.fail_next_capture:
            self.fail_next_capture = False
            raise CameraError(ErrorCode.CAMERA_UNAVAILABLE, "Câmera simulada falhou na captura.")
        item = self._scenario.next()
        serial = next(self._variants)
        png = await asyncio.to_thread(render, item.drawn_as, serial % 3)
        captured_at = max(self._clock(), not_before)
        self._last_frame_at = captured_at
        self._last_drawn = item.drawn_as
        return Frame(
            data=_tagged(png, serial),
            media_type="image/png",
            extension="png",
            captured_at=captured_at,
            source=SOURCE,
            meta={"sim_item": item},
        )
