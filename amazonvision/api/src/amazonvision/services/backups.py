"""Backup and restore of the local data folder (database, inspection photos, models, dataset).

A backup is a single .zip an operator can copy to a pendrive. The database inside it is a
consistent point-in-time snapshot (SQLite `VACUUM INTO`, run on the database's single writer
thread), so it is correct even while the bench is recording cycles. Restoring is deliberately
left to `scripts/restaurar.ps1`: it needs the service stopped, which an HTTP route cannot do to
itself."""

import asyncio
import sqlite3
import zipfile
from pathlib import Path

from amazonvision.config import Settings
from amazonvision.core.clock import utc_now
from amazonvision.schemas.api import BackupOut
from amazonvision.schemas.errors import ApiError, ErrorCode
from amazonvision.storage.db import Database

_INCLUDED_FOLDERS = ("images", "models", "dataset")


def _not_found() -> ApiError:
    return ApiError(ErrorCode.NOT_FOUND, "Cópia de segurança não encontrada.")


class BackupService:
    def __init__(self, settings: Settings, db: Database) -> None:
        self._settings = settings
        self._db = db

    @property
    def _folder(self) -> Path:
        return self._settings.data_root / "backups"

    def _sidecar(self, name: str) -> Path:
        return self._folder / (name.removesuffix(".zip") + ".json")

    async def create(self) -> BackupOut:
        self._folder.mkdir(parents=True, exist_ok=True)
        timestamp = utc_now()
        stamp = f"{timestamp:%Y%m%d-%H%M%S}"
        name = f"backup-{stamp}.zip"
        target = self._folder / name
        snapshot = self._folder / f".snapshot-{stamp}.sqlite"

        def read_counts_and_snapshot(conn: sqlite3.Connection) -> tuple[int, int]:
            inspections = conn.execute("SELECT COUNT(*) FROM inspections").fetchone()[0]
            dataset_photos = conn.execute("SELECT COUNT(*) FROM dataset_samples").fetchone()[0]
            snapshot.unlink(missing_ok=True)
            # A consistent copy taken on the one thread that ever writes to this database.
            conn.execute("VACUUM INTO ?", (str(snapshot),))
            return inspections, dataset_photos

        try:
            inspections, dataset_photos = await self._db.run(read_counts_and_snapshot)
            await asyncio.to_thread(self._build_zip, target, snapshot)
        finally:
            snapshot.unlink(missing_ok=True)

        info = BackupOut(
            name=name,
            size_bytes=target.stat().st_size,
            created_at=timestamp,
            inspections=inspections,
            dataset_photos=dataset_photos,
        )
        self._sidecar(name).write_text(info.model_dump_json(), encoding="utf-8")
        return info

    def _build_zip(self, target: Path, snapshot: Path) -> None:
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.write(snapshot, "db/amazonvision.sqlite")
            for folder in _INCLUDED_FOLDERS:
                source = self._settings.data_root / folder
                if not source.is_dir():
                    continue
                for path in source.rglob("*"):
                    if path.is_file():
                        archive.write(path, str(Path(folder) / path.relative_to(source)))

    async def list(self) -> list[BackupOut]:
        if not self._folder.is_dir():
            return []

        def scan() -> list[BackupOut]:
            backups = []
            for zip_path in sorted(self._folder.glob("backup-*.zip"), reverse=True):
                sidecar = self._sidecar(zip_path.name)
                if sidecar.is_file():
                    info = BackupOut.model_validate_json(sidecar.read_text(encoding="utf-8"))
                    info = info.model_copy(update={"size_bytes": zip_path.stat().st_size})
                else:
                    # Sidecar missing (copied by hand, or from before this field existed).
                    stat = zip_path.stat()
                    info = BackupOut(
                        name=zip_path.name,
                        size_bytes=stat.st_size,
                        created_at=utc_now(),
                        inspections=0,
                        dataset_photos=0,
                    )
                backups.append(info)
            return backups

        return await asyncio.to_thread(scan)

    def file_path(self, name: str) -> Path:
        candidate = (self._folder / name).resolve()
        folder = self._folder.resolve()
        if (
            not name.startswith("backup-")
            or not name.endswith(".zip")
            or not candidate.is_relative_to(folder)
            or not candidate.is_file()
        ):
            raise _not_found()
        return candidate

    async def delete(self, name: str) -> None:
        target = self.file_path(name)

        def remove() -> None:
            target.unlink(missing_ok=True)
            self._sidecar(name).unlink(missing_ok=True)

        await asyncio.to_thread(remove)
