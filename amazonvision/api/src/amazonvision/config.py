import os
from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[3]


def data_base_dir() -> Path:
    base = os.environ.get("LOCALAPPDATA") or Path.home() / ".local" / "share"
    return Path(base) / "AmazonVision"


class RunMode(StrEnum):
    SIMULADO = "simulado"
    REAL = "real"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AV_", env_file=".env", extra="ignore")

    host: str = "127.0.0.1"
    port: int = 8000
    mode: RunMode = RunMode.SIMULADO
    # Default depends on mode, so simulated runs never share a database with real operation.
    data_dir: Path | None = None
    web_dist: Path = REPO_ROOT / "web" / "dist"
    allowed_hosts: list[str] = ["127.0.0.1", "localhost", "[::1]"]
    control_ttl_minutes: int = 30
    low_disk_bytes: int = 1_000_000_000
    log_to_file: bool = True
    # Must stay above the board's 1 s heartbeat, or an idle board looks silent.
    device_silence_ms: int = Field(default=3_000, ge=1_500)
    sim_speed: float = Field(default=1.0, ge=1.0)
    sim_seed: int | None = None
    # Simulated mode only: folder of real photos (JPEG/PNG) the simulated camera shows instead of
    # its drawings, one per piece, so a trained model can be rehearsed before the bench exists.
    sim_photos: Path | None = None
    # Simulated mode only: run this command as the device instead of the Python simulator
    # (e.g. the native build of the firmware logic). JSON list in AV_FIRMWARE_HARNESS.
    firmware_harness: list[str] | None = None
    # Camera: index ("0") or stream URL. Unset: simulated camera in simulated mode, none in real.
    # A phone works both ways: as a virtual webcam (DroidCam/Iriun: index "1" or "2") or as a
    # stream (IP Webcam: "http://127.0.0.1:8080/video" through `adb forward`, or over Wi-Fi).
    camera_source: str | None = None
    # Width, height and exposure apply to index sources only; a stream is set in the phone app.
    camera_width: int = 1280
    camera_height: int = 720
    camera_exposure: float | None = None  # driver units; None keeps the camera's own setting
    # Clockwise rotation of every frame (0, 90, 180, 270), for a phone mounted sideways.
    camera_rotate: int = 0
    # How long an inspection waits for a frame newer than the piece's arrival. Streams deliver
    # frames in bursts: too short gives false STALE_FRAME. Keep it well under the product's
    # decision_timeout_ms, which the board enforces.
    camera_capture_timeout_s: float = Field(default=2.0, gt=0, le=10)
    # Real mode only: USB serial port to the ESP32 (e.g. "COM5"). Unset: no board, API stays up.
    serial_port: str | None = None
    serial_baud_rate: int = 115_200
    # Inspection photos older than this, from closed lots, are purged automatically to protect
    # disk space; the database row (prediction, decision, events) is kept. Dataset photos
    # (training collection) are never touched by this.
    image_retention_days: int = Field(default=30, ge=1)
    retention_check_minutes: int = Field(default=60, ge=1)

    @field_validator("camera_source")
    @classmethod
    def _blank_camera_is_none(cls, value: str | None) -> str | None:
        value = value.strip() if value else value
        return value or None

    @field_validator("camera_rotate")
    @classmethod
    def _valid_rotation(cls, value: int) -> int:
        if value not in (0, 90, 180, 270):
            raise ValueError("AV_CAMERA_ROTATE aceita 0, 90, 180 ou 270")
        return value

    @model_validator(mode="after")
    def _default_data_dir(self) -> Self:
        if self.data_dir is None:
            self.data_dir = data_base_dir() / self.mode.value
        return self

    @property
    def data_root(self) -> Path:
        assert self.data_dir is not None
        return self.data_dir

    @property
    def db_path(self) -> Path:
        return self.data_root / "db" / "amazonvision.sqlite"

    @property
    def data_subdirs(self) -> dict[str, Path]:
        names = ("db", "images", "models", "logs", "backups", "dataset")
        return {name: self.data_root / name for name in names}

    def ensure_data_dirs(self) -> None:
        for path in self.data_subdirs.values():
            path.mkdir(parents=True, exist_ok=True)
