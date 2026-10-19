import asyncio
import threading
import time
from datetime import timedelta

import cv2
import numpy as np
import pytest

from amazonvision.camera import opencv_camera
from amazonvision.camera.base import CameraError
from amazonvision.camera.opencv_camera import OpenCvCamera
from amazonvision.core.clock import utc_now
from amazonvision.schemas.errors import ErrorCode


class FakeDevice:
    """Stands in for cv2.VideoCapture: a numbered gray frame every few milliseconds."""

    def __init__(self, frames_before_failure: int | None = None, opened: bool = True) -> None:
        self.frames_before_failure = frames_before_failure
        self.opened = opened
        self.reads = 0
        self.released = False

    def isOpened(self) -> bool:  # noqa: N802 - OpenCV naming
        return self.opened

    def read(self):
        time.sleep(0.005)  # a real camera blocks until the next frame
        self.reads += 1
        if self.frames_before_failure is not None and self.reads > self.frames_before_failure:
            return False, None
        return True, np.full((48, 64, 3), self.reads % 256, dtype=np.uint8)

    def set(self, prop: int, value: float) -> bool:
        return True

    def release(self) -> None:
        self.released = True


@pytest.fixture(autouse=True)
def fast_reopen(monkeypatch):
    monkeypatch.setattr(opencv_camera, "REOPEN_DELAY_S", 0.01)


def wait_until(condition, timeout: float = 2.0) -> None:
    deadline = time.monotonic() + timeout
    while not condition():
        assert time.monotonic() < deadline, "condição não atingida"
        time.sleep(0.01)


def test_capture_returns_a_frame_newer_than_the_request():
    camera = OpenCvCamera("0", opener=FakeDevice)
    camera.start()
    try:
        wait_until(lambda: camera.info().status == "ok")
        asked_at = utc_now()
        frame = asyncio.run(camera.capture(asked_at, timeout_s=1))
        assert frame.captured_at >= asked_at
        assert frame.media_type == "image/jpeg"
        image = cv2.imdecode(np.frombuffer(frame.data, np.uint8), cv2.IMREAD_COLOR)
        assert image.shape == (48, 64, 3)
        assert frame.meta["camera"]["source"] == "0"
    finally:
        camera.stop()


def test_old_frame_is_never_returned():
    camera = OpenCvCamera("0", opener=FakeDevice)
    camera.start()
    try:
        wait_until(lambda: camera.info().status == "ok")
        future = utc_now() + timedelta(seconds=30)
        with pytest.raises(CameraError) as error:
            asyncio.run(camera.capture(future, timeout_s=0.1))
        assert error.value.code is ErrorCode.STALE_FRAME
    finally:
        camera.stop()


def test_camera_that_never_opens_is_unavailable():
    camera = OpenCvCamera("0", opener=lambda: FakeDevice(opened=False))
    camera.start()
    try:
        assert camera.info().status == "unavailable"
        assert asyncio.run(camera.preview()) is None
        with pytest.raises(CameraError) as error:
            asyncio.run(camera.capture(utc_now(), timeout_s=0.1))
        assert error.value.code is ErrorCode.CAMERA_UNAVAILABLE
    finally:
        camera.stop()


def test_reopens_after_the_device_stops_delivering():
    devices: list[FakeDevice] = []
    lock = threading.Lock()

    def opener() -> FakeDevice:
        with lock:
            device = FakeDevice(frames_before_failure=3)
            devices.append(device)
            return device

    camera = OpenCvCamera("0", opener=opener)
    camera.start()
    try:
        wait_until(lambda: len(devices) >= 3)
        assert devices[0].released
        frame = asyncio.run(camera.capture(utc_now(), timeout_s=1))
        assert frame.data
    finally:
        camera.stop()


def test_info_turns_stale_when_frames_stop():
    now = [utc_now()]
    camera = OpenCvCamera(
        "0", opener=lambda: FakeDevice(frames_before_failure=1), clock=lambda: now[0]
    )
    camera.start()
    try:
        wait_until(lambda: camera.info().last_frame_at is not None)
        camera.stop()
        now[0] += timedelta(seconds=5)
        assert camera.info().status == "stale"
    finally:
        camera.stop()


def test_preview_is_a_compressed_jpeg():
    camera = OpenCvCamera("0", opener=FakeDevice)
    camera.start()
    try:
        wait_until(lambda: camera.info().status == "ok")
        latest = asyncio.run(camera.preview())
        assert latest is not None
        data, media_type = latest
        assert media_type == "image/jpeg"
        assert data.startswith(b"\xff\xd8")
    finally:
        camera.stop()
