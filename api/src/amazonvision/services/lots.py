import sqlite3
from collections.abc import Awaitable, Callable
from typing import Any

from amazonvision.config import RunMode, Settings
from amazonvision.core.bus import EventBus
from amazonvision.core.clock import to_db, utc_now
from amazonvision.domain.quality import DEFAULT_DESTINATIONS, QualityPolicy
from amazonvision.schemas.api import (
    EventSource,
    LotCreate,
    LotOut,
    LotStatus,
    LotSummary,
    Severity,
)
from amazonvision.schemas.errors import ApiError, ErrorCode
from amazonvision.schemas.events import LotUpdatedData, LotUpdatedEvent
from amazonvision.storage import lots as repo
from amazonvision.storage.db import Database, transaction
from amazonvision.storage.events import add_event
from amazonvision.storage.products import get_product_row

POLICY_VERSION = QualityPolicy(threshold=1.0).version


def _not_found() -> ApiError:
    return ApiError(ErrorCode.NOT_FOUND, "Lote não encontrado.")


class LotService:
    def __init__(
        self,
        settings: Settings,
        db: Database,
        bus: EventBus,
        machine_busy: Callable[[], Awaitable[bool]] | None = None,
    ) -> None:
        self._settings = settings
        self._db = db
        self._bus = bus
        self._machine_busy = machine_busy

    async def _ensure_machine_idle(self) -> None:
        if self._machine_busy is not None and await self._machine_busy():
            raise ApiError(
                ErrorCode.INVALID_STATE,
                "A máquina está com um ciclo em andamento.",
                "Aguarde o fim do ciclo ou pare a máquina.",
            )

    def _config_snapshot(self, product: sqlite3.Row) -> dict[str, Any]:
        return {
            "mode": self._settings.mode.value,
            "product": {
                "id": product["id"],
                "name": product["name"],
                "presentation": product["presentation"],
                "version": product["version"],
                "bench_config": product["bench_config_json"],
            },
            "policy": {
                "version": POLICY_VERSION,
                "threshold": product["decision_threshold"],
                "destinations": {g.value: d.value for g, d in DEFAULT_DESTINATIONS.items()},
            },
        }

    async def create(self, body: LotCreate) -> tuple[LotOut, bool]:
        """Open a lot. Repeating the same request_id returns the original lot (created=False)."""
        await self._ensure_machine_idle()
        request_id = str(body.request_id)

        def tx(conn: sqlite3.Connection) -> tuple[LotOut, bool]:
            with transaction(conn):
                existing = repo.get_lot_row_by_request(conn, request_id)
                if existing is not None:
                    same = (
                        existing["product_id"] == body.product_id
                        and existing["operator"] == body.operator
                        and existing["notes"] == body.notes
                    )
                    if not same:
                        raise ApiError(
                            ErrorCode.CONFLICT,
                            "Esta solicitação já foi usada com outros dados.",
                            "Recarregue a página e tente de novo.",
                        )
                    lot = repo.get_lot(conn, existing["id"])
                    assert lot is not None
                    return lot, False

                product = get_product_row(conn, body.product_id)
                if product is None:
                    raise ApiError(ErrorCode.NOT_FOUND, "Produto não cadastrado.")
                if repo.get_open_lot(conn) is not None:
                    raise ApiError(
                        ErrorCode.CONFLICT,
                        "Já existe um lote aberto.",
                        "Encerre o lote atual antes de abrir outro.",
                    )
                model_id = product["active_model_id"]
                if self._settings.mode is RunMode.REAL and model_id is None:
                    raise ApiError(
                        ErrorCode.MODEL_NOT_READY,
                        "Este produto ainda não tem um modelo validado.",
                        "Importe e valide o modelo do produto antes de operar.",
                    )
                now = to_db(utc_now())
                lot_id = repo.insert_lot(
                    conn,
                    request_id=request_id,
                    product_id=body.product_id,
                    model_id=model_id,
                    operator=body.operator,
                    is_simulated=self._settings.mode is RunMode.SIMULADO,
                    policy_threshold=product["decision_threshold"],
                    policy_version=POLICY_VERSION,
                    config_snapshot=self._config_snapshot(product),
                    notes=body.notes,
                    started_at=now,
                )
                add_event(
                    conn,
                    source=EventSource.OPERATOR,
                    type="LOT_OPENED",
                    severity=Severity.INFO,
                    occurred_at=now,
                    lot_id=lot_id,
                    data={"product_id": body.product_id, "operator": body.operator},
                )
                lot = repo.get_lot(conn, lot_id)
                assert lot is not None
                return lot, True

        lot, created = await self._db.run(tx)
        if created:
            await self.publish_update(lot)
        return lot, created

    async def close(self, lot_id: int, operator: str) -> LotOut:
        """Close a lot. Closing an already closed lot returns it unchanged."""
        await self._ensure_machine_idle()

        def tx(conn: sqlite3.Connection) -> tuple[LotOut, bool]:
            with transaction(conn):
                lot = repo.get_lot(conn, lot_id)
                if lot is None:
                    raise _not_found()
                if lot.status is LotStatus.CLOSED:
                    return lot, False
                if repo.has_running_cycle(conn, lot_id):
                    raise ApiError(
                        ErrorCode.INVALID_STATE,
                        "O lote tem um ciclo em andamento.",
                        "Aguarde o fim do ciclo ou pare a máquina.",
                    )
                now = to_db(utc_now())
                repo.close_lot(conn, lot_id, now)
                add_event(
                    conn,
                    source=EventSource.OPERATOR,
                    type="LOT_CLOSED",
                    severity=Severity.INFO,
                    occurred_at=now,
                    lot_id=lot_id,
                    data={"operator": operator},
                )
                closed = repo.get_lot(conn, lot_id)
                assert closed is not None
                return closed, True

        lot, changed = await self._db.run(tx)
        if changed:
            await self.publish_update(lot)
        return lot

    async def publish_update(self, lot: LotOut) -> None:
        summary = await self._db.run(lambda conn: repo.get_summary(conn, lot.id))
        assert summary is not None
        self._bus.publish(LotUpdatedEvent, LotUpdatedData(lot=lot, summary=summary), lot_id=lot.id)

    async def get(self, lot_id: int) -> LotOut:
        lot = await self._db.run(lambda conn: repo.get_lot(conn, lot_id))
        if lot is None:
            raise _not_found()
        return lot

    async def summary(self, lot_id: int) -> LotSummary:
        summary = await self._db.run(lambda conn: repo.get_summary(conn, lot_id))
        if summary is None:
            raise _not_found()
        return summary

    async def list_lots(self, *, limit: int, offset: int, product_id: str | None) -> list[LotOut]:
        return await self._db.run(
            lambda conn: repo.list_lots(conn, limit=limit, offset=offset, product_id=product_id)
        )
