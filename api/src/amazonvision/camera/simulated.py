import asyncio
from collections.abc import Callable
from datetime import datetime
from itertools import count

from amazonvision.camera.base import CameraError, Frame
from amazonvision.core.clock import utc_now
from amazonvision.schemas.api import CameraInfo
from amazonvision.schemas.errors import ErrorCode
from amazonvision.simulation.images import render
from amazonvision.simulation.scenario import Scenario

SOURCE = "simulada"


class SimulatedCamera:
    def __init__(self, scenario: Scenario, clock: Callable[[], datetime] = utc_now) -> None:
        self._scenario = scenario
        self._clock = clock
        self._variants = count()
        self._last_frame_at: datetime | None = None
        self.available = True
        self.fail_next_capture = False

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
        png = await asyncio.to_thread(render, item.drawn_as, next(self._variants) % 3)
        captured_at = max(self._clock(), not_before)
        self._last_frame_at = captured_at
        return Frame(
            data=png,
            media_type="image/png",
            extension="png",
            captured_at=captured_at,
            source=SOURCE,
            meta={"sim_item": item},
        )
