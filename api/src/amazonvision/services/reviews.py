import sqlite3

from amazonvision.core.bus import EventBus
from amazonvision.core.clock import to_db, utc_now
from amazonvision.machine.coordinator import Coordinator
from amazonvision.schemas.api import DecidedBy, InspectionReviewCreate, ReviewOut
from amazonvision.schemas.errors import ApiError, ErrorCode
from amazonvision.schemas.events import LotUpdatedData, LotUpdatedEvent
from amazonvision.storage import inspections as repo
from amazonvision.storage.db import Database, transaction
from amazonvision.storage.lots import get_lot, get_summary


class ReviewService:
    """Human review: decides inconclusive pieces and corrects past decisions.

    The original prediction is never changed; each review is an appended record."""

    def __init__(self, db: Database, bus: EventBus, coordinator: Coordinator) -> None:
        self._db = db
        self._bus = bus
        self._coordinator = coordinator

    async def review(
        self, inspection_id: int, body: InspectionReviewCreate
    ) -> tuple[ReviewOut, bool, bool]:
        """Returns (review, created, delivered_to_machine)."""
        request_id = str(body.request_id)
        existing = await self._db.run(lambda conn: repo.get_review_by_request(conn, request_id))
        if existing is not None:
            if existing.inspection_id != inspection_id or existing.new_decision != body.decision:
                raise ApiError(
                    ErrorCode.CONFLICT,
                    "Esta solicitação já foi usada com outros dados.",
                    "Recarregue a página e tente de novo.",
                )
            return existing, False, False

        inspection = await self._db.run(lambda conn: repo.get_inspection(conn, inspection_id))
        if inspection is None:
            raise ApiError(ErrorCode.NOT_FOUND, "Inspeção não encontrada.")

        # Move the piece first: a recorded decision must never leave a piece stuck on the bench.
        delivered = await self._coordinator.decide_review(inspection_id, body.decision)

        def tx(conn: sqlite3.Connection) -> ReviewOut:
            with transaction(conn):
                review = repo.insert_review(
                    conn,
                    inspection_id=inspection_id,
                    request_id=request_id,
                    reviewer=body.reviewer,
                    previous=inspection.final_decision,
                    new=body.decision,
                    reason=body.reason,
                    created_at=to_db(utc_now()),
                )
                repo.set_final_decision(conn, inspection_id, body.decision, DecidedBy.OPERATOR)
                return review

        review = await self._db.run(tx)
        lot_id = inspection.lot_id
        lot, summary = await self._db.run(
            lambda conn: (get_lot(conn, lot_id), get_summary(conn, lot_id))
        )
        if lot is not None and summary is not None:
            self._bus.publish(
                LotUpdatedEvent, LotUpdatedData(lot=lot, summary=summary), lot_id=lot_id
            )
        return review, True, delivered
