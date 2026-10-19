import shutil
import sqlite3

from amazonvision.config import Settings
from amazonvision.core.clock import utc_now
from amazonvision.core.control import ControlManager
from amazonvision.schemas.api import (
    CameraInfo,
    DeviceLink,
    LotOut,
    LotSummary,
    MachineInfo,
    ModelInfo,
    StorageInfo,
    SystemStatus,
)
from amazonvision.storage.db import Database
from amazonvision.storage.lots import get_open_lot, get_summary


def _read_active_lot(conn: sqlite3.Connection) -> tuple[LotOut | None, LotSummary | None]:
    lot = get_open_lot(conn)
    return lot, (get_summary(conn, lot.id) if lot else None)


class StatusService:
    def __init__(self, settings: Settings, db: Database, control: ControlManager) -> None:
        self._settings = settings
        self._db = db
        self._control = control

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
        # Machine, camera and model are reported as absent until their components exist
        # (Blocks 4, 7 and 8): never claim a connection that was not observed.
        return SystemStatus(
            mode=self._settings.mode,
            generated_at=utc_now(),
            state_version=state_version,
            machine=MachineInfo(
                state=None,
                fault=None,
                sensors=None,
                link=DeviceLink(
                    connected=False,
                    port=None,
                    boot_id=None,
                    firmware_version=None,
                    last_seen_at=None,
                ),
            ),
            camera=CameraInfo(status="unavailable", source=None, last_frame_at=None),
            model=ModelInfo(status="not_loaded", model_id=None, product_id=None),
            storage=self.storage_info(),
            control_locked=holder is not None,
            control_holder=holder,
            active_lot=lot,
            active_lot_summary=summary,
            current_cycle=None,
        )
