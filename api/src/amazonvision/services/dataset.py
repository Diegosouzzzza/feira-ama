import asyncio
import hashlib
import json
import sqlite3
from collections.abc import Callable
from pathlib import Path, PurePosixPath

from amazonvision.camera.base import Camera, CameraError
from amazonvision.config import Settings
from amazonvision.core.clock import to_db, utc_now
from amazonvision.domain.quality import Grade
from amazonvision.schemas.api import (
    DatasetCapture,
    DatasetExportOut,
    DatasetSampleOut,
    DatasetSamplePage,
    DatasetSampleUpdate,
    DatasetSummary,
    SampleStatus,
)
from amazonvision.schemas.errors import ApiError, ErrorCode
from amazonvision.storage import dataset as repo
from amazonvision.storage.db import Database, transaction
from amazonvision.storage.images import resolve_image, write_atomic
from amazonvision.storage.products import get_product_row
from amazonvision.training.dataset import Sample, write_manifest

# Training plan: 300-500 labeled photos per class, from many distinct physical pieces.
TARGET_PHOTOS_PER_CLASS = 300
CAPTURE_TIMEOUT_S = 3.0


def _not_found() -> ApiError:
    return ApiError(ErrorCode.NOT_FOUND, "Foto não encontrada.")


def _label_conflict(piece: str, labels: set[Grade]) -> ApiError:
    given = ", ".join(sorted(g.value for g in labels))
    return ApiError(
        ErrorCode.CONFLICT,
        f"A peça {piece} já tem fotos com a classe {given}.",
        "Todas as fotos de uma peça física levam a mesma classe. Confira a etiqueta da peça.",
    )


class DatasetService:
    """Photos taken on the bench for training, their labels and the export to a manifest."""

    def __init__(
        self, settings: Settings, db: Database, camera: Camera, machine_busy: Callable[[], bool]
    ) -> None:
        self._settings = settings
        self._db = db
        self._camera = camera
        self._machine_busy = machine_busy
        self._capture_lock = asyncio.Lock()

    @property
    def root(self) -> Path:
        return self._settings.data_root / "dataset"

    async def _require_product(self, product_id: str) -> sqlite3.Row:
        product = await self._db.run(lambda conn: get_product_row(conn, product_id))
        if product is None:
            raise ApiError(ErrorCode.VALIDATION_ERROR, f"Produto {product_id} não existe.")
        return product

    async def capture(self, body: DatasetCapture, operator: str) -> DatasetSampleOut:
        if self._machine_busy():
            raise ApiError(
                ErrorCode.INVALID_STATE,
                "A esteira está em operação.",
                "Pare a máquina antes de coletar fotos.",
            )
        await self._require_product(body.product_id)
        if body.label is not None:
            labels = await self._db.run(
                lambda conn: repo.piece_labels(
                    conn, body.product_id, body.physical_sample_id, exclude=None
                )
            )
            if labels - {body.label}:
                raise _label_conflict(body.physical_sample_id, labels)

        async with self._capture_lock:
            try:
                frame = await self._camera.capture(utc_now(), CAPTURE_TIMEOUT_S)
            except CameraError as exc:
                raise ApiError(exc.code, exc.message, "Confira o cabo e a luz da câmera.") from exc

            sha = hashlib.sha256(frame.data).hexdigest()
            relative = PurePosixPath(
                "dataset",
                body.product_id,
                body.collection_session,
                f"{body.physical_sample_id}_{sha[:12]}.{frame.extension}",
            )
            config: dict[str, object] = {
                "source": frame.source,
                "media_type": frame.media_type,
                "captured_at": to_db(frame.captured_at),
            }
            if isinstance(frame.meta.get("camera"), dict):
                config["camera"] = frame.meta["camera"]
            if "sim_item" in frame.meta:
                config["simulated_as"] = frame.meta["sim_item"].drawn_as

            target = self._settings.data_root / relative
            if target.exists():
                raise ApiError(ErrorCode.CONFLICT, "Esta foto já está na coleta.")
            await asyncio.to_thread(write_atomic, target, frame.data)
            now = to_db(utc_now())

            def insert(conn: sqlite3.Connection) -> DatasetSampleOut:
                with transaction(conn):
                    sample_id = repo.insert_sample(
                        conn,
                        product_id=body.product_id,
                        physical_sample_id=body.physical_sample_id,
                        collection_session=body.collection_session,
                        image_path=relative.as_posix(),
                        image_sha256=sha,
                        label=body.label,
                        author=operator,
                        capture_config=config,
                        at=now,
                    )
                sample = repo.get_sample(conn, sample_id)
                assert sample is not None
                return sample

            try:
                return await self._db.run(insert)
            except sqlite3.IntegrityError as exc:
                target.unlink(missing_ok=True)
                raise ApiError(ErrorCode.CONFLICT, "Esta foto já está na coleta.") from exc

    async def update(
        self, sample_id: int, body: DatasetSampleUpdate, reviewer: str
    ) -> DatasetSampleOut:
        labeled = body.status is SampleStatus.LABELED
        if labeled and body.label is None:
            raise ApiError(ErrorCode.VALIDATION_ERROR, "Escolha a classe A, B ou C.")
        now = to_db(utc_now())

        def apply(conn: sqlite3.Connection) -> DatasetSampleOut:
            with transaction(conn):
                current = repo.get_sample(conn, sample_id)
                if current is None:
                    raise _not_found()
                if labeled:
                    labels = repo.piece_labels(
                        conn, current.product_id, current.physical_sample_id, exclude=sample_id
                    )
                    if labels - {body.label}:
                        raise _label_conflict(current.physical_sample_id, labels)
                repo.update_sample(
                    conn,
                    sample_id,
                    status=body.status,
                    label=body.label,
                    reviewer=reviewer,
                    at=now,
                )
            sample = repo.get_sample(conn, sample_id)
            assert sample is not None
            return sample

        return await self._db.run(apply)

    async def list_samples(
        self,
        *,
        product_id: str | None,
        status: SampleStatus | None,
        label: Grade | None,
        physical_sample_id: str | None,
        limit: int,
        offset: int,
    ) -> DatasetSamplePage:
        items, total = await self._db.run(
            lambda conn: repo.list_samples(
                conn,
                product_id=product_id,
                status=status,
                label=label,
                physical_sample_id=physical_sample_id,
                limit=limit,
                offset=offset,
            )
        )
        return DatasetSamplePage(items=items, total=total, limit=limit, offset=offset)

    async def summary(self, product_id: str) -> DatasetSummary:
        await self._require_product(product_id)
        classes, statuses = await self._db.run(lambda conn: repo.summary_counts(conn, product_id))
        return DatasetSummary(
            product_id=product_id,
            target_photos_per_class=TARGET_PHOTOS_PER_CLASS,
            classes=classes,
            pending=statuses.get("pending", 0),
            ambiguous=statuses.get("ambiguous", 0),
            unusable=statuses.get("unusable", 0),
            total=sum(statuses.values()),
        )

    async def image_path(self, sample_id: int) -> Path:
        relative = await self._db.run(lambda conn: repo.get_image_path(conn, sample_id))
        path = resolve_image(self._settings.data_root, relative) if relative else None
        if path is None:
            raise _not_found()
        return path

    async def export(self, product_id: str) -> DatasetExportOut:
        """Write dataset/manifest-<product>.csv (training format, paths relative to dataset/).

        Only labeled photos go in; the split by physical piece is left to the training step."""
        product = await self._require_product(product_id)
        rows = await self._db.run(lambda conn: repo.labeled_for_export(conn, product_id))
        if not rows:
            raise ApiError(
                ErrorCode.INVALID_STATE,
                "Ainda não há fotos rotuladas deste produto.",
                "Colete e rotule fotos antes de exportar.",
            )
        samples = [
            Sample(
                path=PurePosixPath(r["image_path"]).relative_to("dataset").as_posix(),
                product_id=r["product_id"],
                physical_sample_id=r["physical_sample_id"],
                label=Grade(r["label"]),
            )
            for r in rows
        ]
        manifest = self.root / f"manifest-{product_id}.csv"
        temporary = manifest.with_suffix(".csv.tmp")
        await asyncio.to_thread(write_manifest, temporary, samples)
        temporary.replace(manifest)
        command = (
            "uv run --group training python -m amazonvision.training treinar "
            f'--manifesto "{manifest}" --produto {product_id}'
        )
        if product["roi_json"]:
            roi = json.loads(product["roi_json"])
            command += f" --roi {roi['x']},{roi['y']},{roi['width']},{roi['height']}"
        return DatasetExportOut(
            product_id=product_id,
            manifest_path=str(manifest),
            photos=len(samples),
            pieces=len({s.physical_sample_id for s in samples}),
            command=command,
        )
