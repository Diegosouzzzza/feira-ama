import shutil
import sqlite3

from amazonvision.camera.base import Camera
from amazonvision.config import Settings
from amazonvision.core.clock import utc_now
from amazonvision.core.control import ControlManager
from amazonvision.machine.coordinator import Coordinator
from amazonvision.schemas.api import LotOut, LotSummary, StorageInfo, SystemStatus
from amazonvision.storage.db import Database
from amazonvision.storage.lots import get_open_lot, get_summary
from amazonvision.vision.classifier import ModelManager


def _read_active_lot(conn: sqlite3.Connection) -> tuple[LotOut | None, LotSummary | None]:
    lot = get_open_lot(conn)
    return lot, (get_summary(conn, lot.id) if lot else None)


class StatusService:
    def __init__(
        self,
        settings: Settings,
        db: Database,
        control: ControlManager,
        coordinator: Coordinator,
        camera: Camera,
        models: ModelManager,
    ) -> None:
        self._settings = settings
        self._db = db
        self._control = control
        self._coordinator = coordinator
        self._camera = camera
        self._models = models

    def storage_info(self) -> StorageInfo:
        if not self._db.healthy:
            return StorageInfo(status="error", free_bytes=None)
        try:
            free = shutil.disk_usage(self._settings.data_root).free
        except OSError:
            return StorageInfo(status="error", free_bytes=None)
        status = "low_space" if free < self._settings.low_disk_bytes else "ok"
        return StorageInfo(status=status, free_bytes=free)

    async def build(self, state_version: int) -> SystemStatus:
        lot, summary = await self._db.run(_read_active_lot)
        holder = self._control.holder
        return SystemStatus(
            mode=self._settings.mode,
            generated_at=utc_now(),
            state_version=state_version,
            machine=self._coordinator.machine_info(),
            camera=self._camera.info(),
            model=self._models.info(),
            storage=self.storage_info(),
            control_locked=holder is not None,
            control_holder=holder,
            active_lot=lot,
            active_lot_summary=summary,
            current_cycle=await self._coordinator.current_cycle(),
        )
