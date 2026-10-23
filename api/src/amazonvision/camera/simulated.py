import asyncio
import io
import random
import struct
import zlib
from collections.abc import Callable, Sequence
from datetime import datetime
from itertools import count
from pathlib import Path

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


PHOTO_SUFFIXES = (".jpg", ".jpeg", ".png")


def list_photos(folder: Path) -> list[Path]:
    photos = sorted(p for p in folder.iterdir() if p.suffix.lower() in PHOTO_SUFFIXES)
    if not photos:
        raise ValueError(f"nenhuma foto JPEG ou PNG em {folder}")
    return photos


def _photo_jpeg(path: Path, serial: int) -> bytes:
    """A real photo re-encoded with a serial in its comment: each piece is a distinct file."""
    buffer = io.BytesIO()
    load_rgb(path.read_bytes()).save(
        buffer, format="JPEG", quality=90, comment=f"amazonvision-sim-{serial}".encode()
    )
    return buffer.getvalue()


class SimulatedCamera:
    """Drawn pieces by default; with `photos`, real photos in a shuffled loop (one per piece)."""

    def __init__(
        self,
        scenario: Scenario,
        clock: Callable[[], datetime] = utc_now,
        photos: Sequence[Path] = (),
        seed: int | None = None,
    ) -> None:
        self._scenario = scenario
        self._clock = clock
        self._variants = count()
        self._last_frame_at: datetime | None = None
        self.available = True
        self.fail_next_capture = False
        self._last_drawn = "empty"
        self._photos = list(photos)
        self._queue: list[Path] = []
        self._random = random.Random(seed)  # noqa: S311 - shuffles demo photos, not security
        self._last_photo: Path | None = None

    def _next_photo(self) -> Path:
        if not self._queue:
            self._queue = self._random.sample(self._photos, len(self._photos))
        return self._queue.pop()

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    async def preview(self) -> tuple[bytes, str] | None:
        if not self.available:
            return None
        # Shows the last photographed piece; never consumes the scenario's planned items.
        if self._last_photo is not None:
            return await asyncio.to_thread(_photo_jpeg, self._last_photo, 0), "image/jpeg"
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
        captured_at = max(self._clock(), not_before)
        if self._photos:
            photo = self._next_photo()
            data = await asyncio.to_thread(_photo_jpeg, photo, serial)
            self._last_frame_at = captured_at
            self._last_photo = photo
            return Frame(
                data=data,
                media_type="image/jpeg",
                extension="jpg",
                captured_at=captured_at,
                source=SOURCE,
                meta={"sim_item": item, "sim_photo": photo.name},
            )
        png = await asyncio.to_thread(render, item.drawn_as, serial % 3)
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
