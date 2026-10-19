import os
from enum import StrEnum
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[3]


def _default_data_dir() -> Path:
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
    data_dir: Path = _default_data_dir()
    web_dist: Path = REPO_ROOT / "web" / "dist"

    @property
    def data_subdirs(self) -> dict[str, Path]:
        names = ("db", "images", "models", "logs", "backups", "dataset")
        return {name: self.data_dir / name for name in names}

    def ensure_data_dirs(self) -> None:
        for path in self.data_subdirs.values():
            path.mkdir(parents=True, exist_ok=True)
