"""A phone as the bench camera: stream URL or virtual webcam, rotation, capture timeout and the
diagnostics that tell the cameras apart."""

import asyncio
import time
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from amazonvision.camera import opencv_camera, probe
from amazonvision.camera.base import CameraError, Frame
from amazonvision.camera.opencv_camera import OpenCvCamera, is_device_index, open_device
from amazonvision.config import Settings
from amazonvision.core.bus import EventBus
from amazonvision.core.clock import utc_now
from amazonvision.domain.quality import QualityPolicy
from amazonvision.machine.coordinator import ActiveCycle, Coordinator
from amazonvision.main import create_app
from amazonvision.schemas.api import CameraInfo
from amazonvision.schemas.errors import ErrorCode
from amazonvision.storage.db import Database
from amazonvision.vision.classifier import ModelManager
from tests.conftest import TEST_HOSTS

# ---------------------------------------------------------------- opening the source


class RecordingCapture:
    """Stands in for cv2.VideoCapture and records how it was opened and configured."""

    instances: list["RecordingCapture"] = []

    def __init__(self, *args) -> None:
        self.args = args
        self.props: dict[int, float] = {}
        RecordingCapture.instances.append(self)

    def set(self, prop: int, value: float) -> bool:
        self.props[prop] = value
        return True


@pytest.fixture
def captures(monkeypatch) -> list[RecordingCapture]:
    RecordingCapture.instances = []
    monkeypatch.setattr(opencv_camera.cv2, "VideoCapture", RecordingCapture)
    return RecordingCapture.instances


@pytest.mark.parametrize(
    "source",
    ["http://127.0.0.1:8080/video", "http://192.168.0.20:4747/video", "rtsp://192.168.0.20/h264"],
)
def test_stream_url_gets_timeouts_and_no_device_properties(captures, source):
    open_device(source, 1280, 720, exposure=-6)
    (capture,) = captures
    opened_source, backend, params = capture.args
    assert opened_source == source
    assert backend == cv2.CAP_FFMPEG
    assert dict(zip(params[::2], params[1::2], strict=True)) == {
        cv2.CAP_PROP_OPEN_TIMEOUT_MSEC: opencv_camera.STREAM_OPEN_TIMEOUT_MS,
        cv2.CAP_PROP_READ_TIMEOUT_MSEC: opencv_camera.STREAM_READ_TIMEOUT_MS,
    }
    # Focus, white balance, exposure and resolution belong to the phone app.
    assert capture.props == {}


def test_device_index_keeps_the_stabilising_properties(captures):
    open_device("1", 1280, 720, exposure=-6)
    (capture,) = captures
    assert capture.args[0] == 1
    assert capture.props[cv2.CAP_PROP_FRAME_WIDTH] == 1280
    assert capture.props[cv2.CAP_PROP_FRAME_HEIGHT] == 720
    assert capture.props[cv2.CAP_PROP_AUTOFOCUS] == 0
    assert capture.props[cv2.CAP_PROP_AUTO_WB] == 0
    assert capture.props[cv2.CAP_PROP_EXPOSURE] == -6


def test_index_and_url_are_told_apart():
    assert is_device_index("0") and is_device_index(" 2 ")
    assert not is_device_index("http://127.0.0.1:8080/video")
    assert not is_device_index("rtsp://10.0.0.5/live")


# ---------------------------------------------------------------- rotation


class LandscapeDevice:
    """64x48 frames whose top-left corner is white: shows where rotation moves it."""

    def isOpened(self) -> bool:  # noqa: N802 - OpenCV naming
        return True

    def read(self):
        time.sleep(0.005)
        image = np.zeros((48, 64, 3), dtype=np.uint8)
        image[:8, :8] = 255
        return True, image

    def set(self, prop: int, value: float) -> bool:
        return True

    def release(self) -> None:
        pass


def _decoded(data: bytes) -> np.ndarray:
    return cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_GRAYSCALE)


def _wait_ok(camera: OpenCvCamera) -> None:
    deadline = time.monotonic() + 2
    while camera.info().status != "ok":
        assert time.monotonic() < deadline, "câmera não entregou imagem"
        time.sleep(0.01)


@pytest.mark.parametrize(
    ("rotate", "shape", "white_corner"),
    [
        (0, (48, 64), (0, 0)),
        (90, (64, 48), (0, -1)),  # clockwise: top-left goes to top-right
        (180, (48, 64), (-1, -1)),
        (270, (64, 48), (-1, 0)),
    ],
)
def test_rotation_applies_to_capture_and_preview(rotate, shape, white_corner):
    camera = OpenCvCamera("http://celular/video", rotate=rotate, opener=LandscapeDevice)
    camera.start()
    try:
        _wait_ok(camera)
        frame = asyncio.run(camera.capture(utc_now(), timeout_s=1))
        preview = asyncio.run(camera.preview())
        assert preview is not None
        for data in (frame.data, preview[0]):
            image = _decoded(data)
            assert image.shape == shape
            row, column = white_corner
            assert image[row, column] > 200
        assert frame.meta["camera"]["rotate"] == rotate
    finally:
        camera.stop()


def test_invalid_rotation_is_rejected():
    with pytest.raises(ValueError):
        OpenCvCamera("0", rotate=45, opener=LandscapeDevice)


# ---------------------------------------------------------------- settings


def test_camera_settings_defaults(tmp_path: Path):
    settings = Settings(_env_file=None, data_dir=tmp_path)
    assert settings.camera_rotate == 0
    assert settings.camera_capture_timeout_s == 2.0


def test_camera_settings_come_from_the_environment(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("AV_CAMERA_SOURCE", " http://127.0.0.1:8080/video ")
    monkeypatch.setenv("AV_CAMERA_ROTATE", "90")
    monkeypatch.setenv("AV_CAMERA_CAPTURE_TIMEOUT_S", "3.5")
    settings = Settings(_env_file=None, data_dir=tmp_path)
    assert settings.camera_source == "http://127.0.0.1:8080/video"
    assert settings.camera_rotate == 90
    assert settings.camera_capture_timeout_s == 3.5


def test_blank_camera_source_means_no_camera(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("AV_CAMERA_SOURCE", "")
    assert Settings(_env_file=None, data_dir=tmp_path).camera_source is None


@pytest.mark.parametrize("value", ["45", "-90", "360"])
def test_rotation_other_than_quarter_turns_is_refused(tmp_path: Path, monkeypatch, value):
    monkeypatch.setenv("AV_CAMERA_ROTATE", value)
    with pytest.raises(ValidationError):
        Settings(_env_file=None, data_dir=tmp_path)


# ---------------------------------------------------------------- capture timeout


class SlowCamera:
    """Remembers the timeout it was given, then fails like a stream without a new frame."""

    def __init__(self) -> None:
        self.timeouts: list[float] = []

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def info(self) -> CameraInfo:
        return CameraInfo(status="ok", source="http://celular/video", last_frame_at=None)

    async def capture(self, not_before: datetime, timeout_s: float) -> Frame:
        self.timeouts.append(timeout_s)
        raise CameraError(ErrorCode.STALE_FRAME, "A câmera não entregou uma imagem nova.")

    async def preview(self) -> tuple[bytes, str] | None:
        return None


@pytest.mark.anyio
@pytest.mark.parametrize("configured", [None, 3.5])
async def test_inspection_waits_the_configured_capture_timeout(tmp_path: Path, configured):
    extra = {} if configured is None else {"camera_capture_timeout_s": configured}
    settings = Settings(_env_file=None, data_dir=tmp_path / "data", log_to_file=False, **extra)
    settings.ensure_data_dirs()
    db = Database(settings.db_path)
    await db.open()
    try:
        recorded: list[str] = []

        async def record(event_type: str, **_: object) -> None:
            recorded.append(event_type)

        camera = SlowCamera()
        coordinator = Coordinator(
            settings, db, EventBus(), None, camera, ModelManager(settings), record
        )
        cycle = ActiveCycle(
            cycle_id=1, lot_id=1, product_id="tucuma", policy=QualityPolicy(threshold=0.8)
        )
        await coordinator._inspect(cycle)
        assert camera.timeouts == [configured or 2.0]
        assert recorded == ["CAMERA_UNAVAILABLE"]
        assert cycle.abort_override == "CAMERA_UNAVAILABLE"
    finally:
        await db.close()


# ---------------------------------------------------------------- probing


class ProbeDevice:
    def __init__(self, opened: bool = True, frames: bool = True) -> None:
        self.opened = opened
        self.frames = frames
        self.released = False

    def isOpened(self) -> bool:  # noqa: N802 - OpenCV naming
        return self.opened

    def read(self):
        if not self.frames:
            return False, None
        return True, np.full((30, 40, 3), 90, dtype=np.uint8)

    def set(self, prop: int, value: float) -> bool:
        return True

    def release(self) -> None:
        self.released = True


def test_probe_reports_size_and_a_picture():
    device = ProbeDevice()
    result = probe.probe("1", opener=lambda source: device)
    assert result.available and (result.width, result.height) == (40, 30)
    assert result.jpeg is not None and result.jpeg.startswith(b"\xff\xd8")
    assert device.released


def test_probe_rotates_like_the_bench_camera():
    result = probe.probe("1", rotate=90, opener=lambda source: ProbeDevice())
    assert (result.width, result.height) == (30, 40)


@pytest.mark.parametrize("device", [ProbeDevice(opened=False), ProbeDevice(frames=False)])
def test_probe_of_a_missing_or_silent_camera(device):
    result = probe.probe("3", opener=lambda source: device)
    assert not result.available and result.jpeg is None
    assert device.released


def test_probe_survives_an_opener_that_raises():
    def opener(source: str):
        raise RuntimeError("driver")

    assert not probe.probe("0", opener=opener).available


def test_probe_indexes_skips_the_camera_in_use():
    opened: list[str] = []

    def opener(source: str) -> ProbeDevice:
        opened.append(source)
        return ProbeDevice(opened=source != "2")

    results = probe.probe_indexes(4, skip=frozenset({1}), opener=opener)
    assert opened == ["0", "2", "3"]
    assert [(r.source, r.available) for r in results] == [("0", True), ("2", False), ("3", True)]


def test_probe_command_line_saves_one_photo_per_camera(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.setattr(
        probe, "_default_opener", lambda source: ProbeDevice(opened=source in ("0", "1"))
    )
    assert probe.main(["--max", "3", "--out", str(tmp_path)]) == 0
    assert sorted(p.name for p in tmp_path.iterdir()) == ["camera-0.jpg", "camera-1.jpg"]
    output = capsys.readouterr().out
    assert "índice 2: sem câmera" in output
    assert "adb forward tcp:8080 tcp:8080" in output


def test_probe_command_line_fails_when_the_stream_is_down(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.setattr(probe, "_default_opener", lambda source: ProbeDevice(opened=False))
    code = probe.main(["--url", "http://127.0.0.1:8080/video", "--out", str(tmp_path)])
    assert code == 1
    assert "O stream não abriu" in capsys.readouterr().out


# ---------------------------------------------------------------- diagnostics endpoints


@pytest.fixture
def fake_cameras(monkeypatch) -> list[str]:
    """Index 0 = notebook webcam, 1 = phone's virtual webcam, the rest absent."""
    opened: list[str] = []

    def opener(source: str) -> ProbeDevice:
        opened.append(source)
        return ProbeDevice(opened=source in ("0", "1"))

    monkeypatch.setattr(probe, "_default_opener", opener)
    return opened


def test_cameras_endpoint_lists_what_each_index_delivers(client: TestClient, fake_cameras):
    body = client.get("/api/diagnostics/cameras?max_index=3").json()
    assert body["configured_source"] is None
    assert body["source_kind"] == "none"
    assert body["rotate"] == 0
    assert body["capture_timeout_s"] == 2.0
    assert [(d["index"], d["available"], d["in_use"]) for d in body["devices"]] == [
        (0, True, False),
        (1, True, False),
        (2, False, False),
    ]
    assert body["devices"][1]["snapshot_url"] == "/api/diagnostics/cameras/1/snapshot"
    assert body["devices"][2]["snapshot_url"] is None
    assert (body["devices"][0]["width"], body["devices"][0]["height"]) == (40, 30)
    assert any("adb forward" in line for line in body["guide"])
    assert fake_cameras == ["0", "1", "2"]


def test_camera_snapshot_endpoint_returns_a_jpeg(client: TestClient, fake_cameras):
    response = client.get("/api/diagnostics/cameras/1/snapshot")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    assert response.content.startswith(b"\xff\xd8")


def test_camera_snapshot_of_an_absent_index_is_unavailable(client: TestClient, fake_cameras):
    response = client.get("/api/diagnostics/cameras/4/snapshot")
    assert response.status_code == 503
    assert response.json()["code"] == "CAMERA_UNAVAILABLE"


def test_camera_in_use_is_reported_without_being_reopened(
    tmp_path: Path, monkeypatch, fake_cameras
):
    """Reopening the device the bench is reading would steal it from the inspection."""
    monkeypatch.setattr(opencv_camera, "open_device", lambda *args: LandscapeDevice())
    settings = Settings(
        _env_file=None,
        data_dir=tmp_path / "data",
        web_dist=tmp_path / "no-dist",
        allowed_hosts=TEST_HOSTS,
        log_to_file=False,
        camera_source="1",
        camera_rotate=90,
    )
    with TestClient(create_app(settings)) as client:
        deadline = time.monotonic() + 3
        while client.get("/api/camera/snapshot").status_code != 200:
            assert time.monotonic() < deadline, "câmera não entregou imagem"
            time.sleep(0.02)
        body = client.get("/api/diagnostics/cameras?max_index=3").json()
        assert body["configured_source"] == "1"
        assert body["source_kind"] == "index"
        assert body["rotate"] == 90
        assert body["camera"]["status"] == "ok"
        in_use = body["devices"][1]
        assert in_use == {
            "index": 1,
            "available": True,
            "width": None,
            "height": None,
            "in_use": True,
            "snapshot_url": "/api/camera/snapshot",
        }
        assert fake_cameras == ["0", "2"]

        snapshot = client.get("/api/diagnostics/cameras/1/snapshot")
        assert snapshot.status_code == 200
        assert _decoded(snapshot.content).shape == (64, 48)  # the live, rotated frame
        assert fake_cameras == ["0", "2"]


def test_stream_source_is_reported_as_stream(tmp_path: Path, monkeypatch, fake_cameras):
    monkeypatch.setattr(opencv_camera, "open_device", lambda *args: LandscapeDevice())
    settings = Settings(
        _env_file=None,
        data_dir=tmp_path / "data",
        web_dist=tmp_path / "no-dist",
        allowed_hosts=TEST_HOSTS,
        log_to_file=False,
        camera_source="http://127.0.0.1:8080/video",
    )
    with TestClient(create_app(settings)) as client:
        body = client.get("/api/diagnostics/cameras?max_index=2").json()
    assert body["source_kind"] == "stream"
    assert all(not device["in_use"] for device in body["devices"])
    assert fake_cameras == ["0", "1"]
