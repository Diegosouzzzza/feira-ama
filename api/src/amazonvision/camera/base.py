from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Protocol

from amazonvision.schemas.api import CameraInfo
from amazonvision.schemas.errors import ErrorCode


@dataclass(frozen=True)
class Frame:
    data: bytes
    media_type: str
    extension: str
    captured_at: datetime
    source: str
    meta: Mapping[str, Any] = field(default_factory=dict)


class CameraError(Exception):
    def __init__(self, code: ErrorCode, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class Camera(Protocol):
    def start(self) -> None: ...

    def stop(self) -> None: ...

    def info(self) -> CameraInfo: ...

    async def capture(self, not_before: datetime, timeout_s: float) -> Frame:
        """Return a frame captured at or after not_before, or raise CameraError."""
        ...

    async def preview(self) -> tuple[bytes, str] | None:
        """Latest image for the live view (bytes, media type); None when there is none."""
        ...


class NoCamera:
    """No camera configured: always unavailable."""

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def info(self) -> CameraInfo:
        return CameraInfo(status="unavailable", source=None, last_frame_at=None)

    async def capture(self, not_before: datetime, timeout_s: float) -> Frame:
        raise CameraError(ErrorCode.CAMERA_UNAVAILABLE, "Nenhuma câmera configurada.")

    async def preview(self) -> tuple[bytes, str] | None:
        return None
