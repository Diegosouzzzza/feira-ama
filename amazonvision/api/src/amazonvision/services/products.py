import json
import sqlite3
from collections.abc import Callable
from typing import Any

from amazonvision.config import Settings
from amazonvision.core.clock import to_db, utc_now
from amazonvision.machine.bench_config import SIMULATED_BENCH
from amazonvision.machine.protocol import ConfigurePayload
from amazonvision.schemas.api import ProductConfigOut, ProductConfigUpdate, RoiOut
from amazonvision.schemas.errors import ApiError, ErrorCode
from amazonvision.storage import products as repo
from amazonvision.storage.db import Database, transaction
from amazonvision.storage.lots import get_open_lot


class ProductConfigService:
    """Per-product profile: presentation, decision threshold and the bench calibration.

    Changes apply to the next lot: an open lot keeps the values frozen when it was opened."""

    def __init__(self, settings: Settings, db: Database, machine_busy: Callable[[], bool]) -> None:
        self._settings = settings
        self._db = db
        self._machine_busy = machine_busy

    def _locked_reason(self, conn: sqlite3.Connection, product_id: str) -> str | None:
        if self._machine_busy():
            return "A esteira está em operação. Pare a máquina para alterar a configuração."
        lot = get_open_lot(conn)
        if lot is not None and lot.product_id == product_id:
            return "Há um lote aberto deste produto. Encerre o lote para alterar a configuração."
        return None

    def _build(self, conn: sqlite3.Connection, product_id: str) -> ProductConfigOut:
        row = repo.get_product_row(conn, product_id)
        if row is None:
            raise ApiError(ErrorCode.NOT_FOUND, "Produto não encontrado.")
        # Not calibrated yet: offer the simulated bench values as a starting point. The real
        # bench still refuses to arm until someone saves a calibration (bench_config_for).
        default = not row["bench_config_json"]
        bench = (
            SIMULATED_BENCH
            if default
            else ConfigurePayload.model_validate_json(row["bench_config_json"])
        )
        roi = RoiOut.model_validate_json(row["roi_json"]) if row["roi_json"] else None
        reason = self._locked_reason(conn, product_id)
        return ProductConfigOut(
            product=repo.to_product(row),
            bench=bench,
            bench_is_default=default,
            roi=roi,
            editable=reason is None,
            locked_reason=reason,
        )

    async def get(self, product_id: str) -> ProductConfigOut:
        return await self._db.run(lambda conn: self._build(conn, product_id))

    async def update(
        self, product_id: str, body: ProductConfigUpdate
    ) -> tuple[ProductConfigOut, dict[str, Any]]:
        """Save and return the new configuration plus what changed (for the event log)."""
        now = to_db(utc_now())

        def tx(conn: sqlite3.Connection) -> tuple[ProductConfigOut, dict[str, Any]]:
            with transaction(conn):
                before = self._build(conn, product_id)
                if before.locked_reason:
                    raise ApiError(ErrorCode.INVALID_STATE, before.locked_reason)
                saved = repo.update_config(
                    conn,
                    product_id,
                    expected_version=body.expected_version,
                    presentation=body.presentation or None,
                    decision_threshold=body.decision_threshold,
                    bench_config_json=body.bench.model_dump_json(),
                    roi_json=body.roi.model_dump_json() if body.roi else None,
                    at=now,
                )
                if not saved:
                    raise ApiError(
                        ErrorCode.CONFLICT,
                        "A configuração foi alterada em outra tela.",
                        "Recarregue a configuração e refaça a alteração.",
                    )
                after = self._build(conn, product_id)
            return after, _changes(before, after)

        return await self._db.run(tx)


def _changes(before: ProductConfigOut, after: ProductConfigOut) -> dict[str, Any]:
    old: dict[str, Any] = {
        "presentation": before.product.presentation,
        "decision_threshold": before.product.decision_threshold,
        "roi": before.roi.model_dump() if before.roi else None,
        **json.loads(before.bench.model_dump_json()),
    }
    new: dict[str, Any] = {
        "presentation": after.product.presentation,
        "decision_threshold": after.product.decision_threshold,
        "roi": after.roi.model_dump() if after.roi else None,
        **json.loads(after.bench.model_dump_json()),
    }
    return {
        key: {"de": old.get(key), "para": value}
        for key, value in new.items()
        if old.get(key) != value
    }
