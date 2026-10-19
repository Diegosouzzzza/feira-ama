import os
from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import model_validator
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
