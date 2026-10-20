"""Automatic and on-demand cleanup of old inspection photos (not the Coleta/dataset photos)."""

import asyncio
import contextlib
import logging
from collections.abc import Awaitable, Callable
from datetime import timedelta
from pathlib import Path
from typing import Any

from amazonvision.config import Settings
from amazonvision.core.clock import to_db, utc_now
from amazonvision.schemas.api import PurgeOut, Severity
from amazonvision.storage import retention as repo
from amazonvision.storage.db import Database
from amazonvision.storage.images import resolve_image
from amazonvision.storage.lots import get_open_lot

log = logging.getLogger("amazonvision.retention")

BATCH_LIMIT = 500


def _delete_files(data_root: Path, items: list[tuple[int, str]]) -> tuple[list[int], int]:
    """Runs off the event loop: each unlink is a blocking filesystem call."""
    freed = 0
    purged_ids: list[int] = []
    for inspection_id, relative in items:
        path = resolve_image(data_root, relative)
        if path is not None:
            freed += path.stat().st_size
            path.unlink(missing_ok=True)
        purged_ids.append(inspection_id)
    return purged_ids, freed


class RetentionService:
    """Deletes the photo file once an inspection is old enough and its lot is closed; the
    database row (prediction, decision, the events it produced) is kept for the CSV export."""

    def __init__(
        self,
        settings: Settings,
        db: Database,
        record: Callable[..., Awaitable[None]],
    ) -> None:
        self._settings = settings
        self._db = db
        self._record = record
        self._task: asyncio.Task[Any] | None = None

    def start(self) -> None:
        if self._settings.retention_check_minutes > 0:
            self._task = asyncio.create_task(self._loop())

    async def stop(self) -> None:
        if self._task is not None:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
            self._task = None

    async def _loop(self) -> None:
        interval_s = self._settings.retention_check_minutes * 60
        while True:
            await asyncio.sleep(interval_s)
            try:
                result = await self.purge_old_images()
                if result.purged:
                    log.info(
                        "limpeza automática: %d fotos, %d bytes liberados",
                        result.purged,
                        result.freed_bytes,
                    )
            except Exception:
                log.exception("falha na limpeza automática de fotos")

    async def purge_old_images(
        self, *, max_age_days: int | None = None, operator: str | None = None
    ) -> PurgeOut:
        """Purge inspection photos older than max_age_days (default: AV_IMAGE_RETENTION_DAYS).

        Never touches the lot that is still open, so the operator can always review it."""
        days = max_age_days if max_age_days is not None else self._settings.image_retention_days
        cutoff = to_db(utc_now() - timedelta(days=days))
        open_lot = await self._db.run(get_open_lot)
        exclude_lot_id = open_lot.id if open_lot is not None else None

        candidates = await self._db.run(
            lambda conn: repo.purge_candidates(
                conn, before=cutoff, exclude_lot_id=exclude_lot_id, limit=BATCH_LIMIT
            )
        )
        if not candidates:
            return PurgeOut(purged=0, freed_bytes=0)

        purged_ids, freed = await asyncio.to_thread(
            _delete_files, self._settings.data_root, candidates
        )
        now = to_db(utc_now())
        await self._db.run(lambda conn: repo.mark_purged(conn, purged_ids, now))
        data = {"count": len(purged_ids), "freed_bytes": freed, "max_age_days": days}
        if operator is not None:
            data["operator"] = operator
        await self._record("IMAGES_PURGED", severity=Severity.INFO, data=data)
        return PurgeOut(purged=len(purged_ids), freed_bytes=freed)
