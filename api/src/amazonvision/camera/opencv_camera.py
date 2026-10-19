"""USB/UVC camera through OpenCV. A background thread keeps only the latest frame with its
timestamp; captures wait for a frame newer than the request, never an old buffered one."""

import asyncio
import contextlib
import logging
import sys
import threading
import time
from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Any, Protocol

import cv2
import numpy as np

from amazonvision.camera.base import CameraError, Frame
from amazonvision.core.clock import utc_now
from amazonvision.schemas.api import CameraInfo
from amazonvision.schemas.errors import ErrorCode

log = logging.getLogger("amazonvision.camera")

STALE_AFTER = timedelta(seconds=2)
REOPEN_DELAY_S = 1.0


class VideoSource(Protocol):
    def isOpened(self) -> bool: ...  # noqa: N802 - OpenCV naming

    def read(self) -> tuple[bool, Any]: ...

    def set(self, prop: int, value: float) -> bool: ...

    def release(self) -> None: ...


def open_device(source: str, width: int, height: int, exposure: float | None) -> VideoSource:
    """Open a camera index ("0") or a stream URL, with the settings that keep images stable."""
    if source.isdigit():
        backend = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_ANY
        capture = cv2.VideoCapture(int(source), backend)
    else:
        capture = cv2.VideoCapture(source)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    # Lock what the camera would otherwise change between photos (best effort: not every camera
    # or driver honours these). Unstable exposure/focus would teach the model the wrong thing.
    capture.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    capture.set(cv2.CAP_PROP_AUTO_WB, 0)
    if exposure is not None:
        capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # manual on DirectShow/V4L2
        capture.set(cv2.CAP_PROP_EXPOSURE, exposure)
    return capture


class OpenCvCamera:
    def __init__(
        self,
        source: str,
        *,
        width: int = 1280,
        height: int = 720,
        exposure: float | None = None,
        opener: Callable[[], VideoSource] | None = None,
        clock: Callable[[], datetime] = utc_now,
    ) -> None:
        self.source = source
        self._opener = opener or (lambda: open_device(source, width, height, exposure))
        self._clock = clock
        self._lock = threading.Lock()
        self._frame: np.ndarray | None = None
        self._frame_at: datetime | None = None
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self.settings = {"source": source, "width": width, "height": height, "exposure": exposure}

    # ------------------------------------------------------------ lifecycle

    def start(self) -> None:
        if self._thread is None:
            self._stop.clear()
            self._thread = threading.Thread(target=self._run, name="av-camera", daemon=True)
            self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=3)
            self._thread = None

    def _run(self) -> None:
        capture: VideoSource | None = None
        while not self._stop.is_set():
            if capture is None:
                try:
                    capture = self._opener()
                except Exception:
                    log.exception("falha ao abrir a câmera %s", self.source)
                    capture = None
                if capture is None or not capture.isOpened():
                    capture = None
                    self._stop.wait(REOPEN_DELAY_S)
                    continue
                log.info("câmera %s aberta", self.source)
            ok, image = capture.read()
            if not ok or image is None:
                log.warning("câmera %s sem quadro; reabrindo", self.source)
                with contextlib.suppress(Exception):
                    capture.release()
                capture = None
                self._stop.wait(REOPEN_DELAY_S)
                continue
            with self._lock:
                self._frame = image
                self._frame_at = self._clock()
        if capture is not None:
            with contextlib.suppress(Exception):
                capture.release()

    # ------------------------------------------------------------ reading

    def _latest(self) -> tuple[np.ndarray | None, datetime | None]:
        with self._lock:
            return self._frame, self._frame_at

    def info(self) -> CameraInfo:
        _, at = self._latest()
        if at is None:
            return CameraInfo(status="unavailable", source=self.source, last_frame_at=None)
        status = "stale" if self._clock() - at > STALE_AFTER else "ok"
        return CameraInfo(status=status, source=self.source, last_frame_at=at)

    @staticmethod
    def _jpeg(image: np.ndarray, quality: int) -> bytes:
        ok, buffer = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, quality])
        if not ok:
            raise CameraError(ErrorCode.CAMERA_UNAVAILABLE, "Falha ao codificar a imagem.")
        return buffer.tobytes()

    async def capture(self, not_before: datetime, timeout_s: float) -> Frame:
        deadline = time.monotonic() + timeout_s
        while True:
            image, at = self._latest()
            if image is not None and at is not None and at >= not_before:
                data = await asyncio.to_thread(self._jpeg, image, 92)
                return Frame(
                    data=data,
                    media_type="image/jpeg",
                    extension="jpg",
                    captured_at=at,
                    source=self.source,
                    meta={"camera": self.settings},
                )
            if time.monotonic() >= deadline:
                if image is None:
                    raise CameraError(ErrorCode.CAMERA_UNAVAILABLE, "Câmera sem imagem.")
                raise CameraError(ErrorCode.STALE_FRAME, "A câmera não entregou uma imagem nova.")
            await asyncio.sleep(0.01)

    async def preview(self) -> tuple[bytes, str] | None:
        image, _ = self._latest()
        if image is None:
            return None
        return await asyncio.to_thread(self._jpeg, image, 70), "image/jpeg"
