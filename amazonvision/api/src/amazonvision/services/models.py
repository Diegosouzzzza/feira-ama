import shutil
import sqlite3
from pathlib import Path

from amazonvision.config import RunMode, Settings
from amazonvision.core.clock import to_db, utc_now
from amazonvision.schemas.api import ModelOut, ModelValidationStatus
from amazonvision.schemas.errors import ApiError, ErrorCode
from amazonvision.storage import models as repo
from amazonvision.storage.db import Database, transaction
from amazonvision.storage.lots import get_open_lot
from amazonvision.storage.products import get_product_row
from amazonvision.vision.package import PackageError, load_package


def _not_found() -> ApiError:
    return ApiError(ErrorCode.NOT_FOUND, "Modelo não encontrado.")


class ModelService:
    """Model versions: install a trained package, record the team's validation, activate it."""

    def __init__(self, settings: Settings, db: Database) -> None:
        self._settings = settings
        self._db = db

    @property
    def _store(self) -> Path:
        return self._settings.data_root / "models"

    async def list_models(self, product_id: str | None) -> list[ModelOut]:
        return await self._db.run(lambda conn: repo.list_models(conn, product_id))

    async def install(self, source: Path) -> tuple[ModelOut, bool]:
        """Copy a package into the data folder and register it. Same package again: no-op."""
        try:
            package = load_package(source)
        except PackageError as exc:
            raise ApiError(ErrorCode.VALIDATION_ERROR, f"Pacote inválido: {exc}") from exc

        existing = await self._db.run(lambda conn: repo.get_model(conn, package.model_id))
        if existing is not None:
            stored = await self._db.run(
                lambda conn: conn.execute(
                    "SELECT weights_sha256 FROM model_versions WHERE id = ?", (package.model_id,)
                ).fetchone()[0]
            )
            if stored != package.weights_sha256:
                raise ApiError(
                    ErrorCode.CONFLICT,
                    "Já existe um modelo com este nome e pesos diferentes.",
                    "Gere o pacote de novo para receber um nome novo.",
                )
            return existing, False

        product = await self._db.run(lambda conn: get_product_row(conn, package.product_id))
        if product is None:
            raise ApiError(ErrorCode.VALIDATION_ERROR, f"Produto {package.product_id} não existe.")

        target = self._store / package.model_id
        if not target.exists():
            shutil.copytree(source, target)
        installed = load_package(target)  # verify the copy, not just the source

        def tx(conn: sqlite3.Connection) -> ModelOut:
            with transaction(conn):
                repo.insert_model(
                    conn, installed, f"models/{installed.model_id}/model.onnx", to_db(utc_now())
                )
                model = repo.get_model(conn, installed.model_id)
                assert model is not None
                return model

        return await self._db.run(tx), True

    async def set_validation(
        self, model_id: str, status: ModelValidationStatus, reviewer: str
    ) -> ModelOut:
        def tx(conn: sqlite3.Connection) -> ModelOut:
            with transaction(conn):
                if repo.get_model(conn, model_id) is None:
                    raise _not_found()
                repo.set_validation(conn, model_id, status, reviewer, to_db(utc_now()))
                model = repo.get_model(conn, model_id)
                assert model is not None
                return model

        return await self._db.run(tx)

    async def activate(self, model_id: str) -> ModelOut:
        def tx(conn: sqlite3.Connection) -> ModelOut:
            with transaction(conn):
                model = repo.get_model(conn, model_id)
                if model is None:
                    raise _not_found()
                if model.validation_status is ModelValidationStatus.REJECTED:
                    raise ApiError(ErrorCode.CONFLICT, "Este modelo foi reprovado pela equipe.")
                if (
                    self._settings.mode is RunMode.REAL
                    and model.validation_status is not ModelValidationStatus.VALIDATED
                ):
                    raise ApiError(
                        ErrorCode.CONFLICT,
                        "No modo real só um modelo validado pode ser ativado.",
                        "Revise o relatório e marque o modelo como validado.",
                    )
                lot = get_open_lot(conn)
                if lot is not None and lot.product_id == model.product_id:
                    raise ApiError(
                        ErrorCode.INVALID_STATE,
                        "Há um lote aberto deste produto.",
                        "Encerre o lote antes de trocar o modelo; o próximo lote usará o novo.",
                    )
                repo.activate(
                    conn, model.product_id, model.id, model.recommended_threshold, to_db(utc_now())
                )
                active = repo.get_model(conn, model_id)
                assert active is not None
                return active

        return await self._db.run(tx)

    def report_path(self, model_id: str) -> Path | None:
        path = (self._store / model_id / "relatorio.md").resolve()
        if not path.is_relative_to(self._store.resolve()) or not path.is_file():
            return None
        return path
