import json
import sqlite3
from dataclasses import dataclass

from amazonvision.core.clock import from_db
from amazonvision.domain.quality import AutoDecision, Destination, Grade, ReviewReason
from amazonvision.schemas.api import (
    CycleStatus,
    DecidedBy,
    InspectionOut,
    InspectionOutcome,
    ReviewOut,
)

_SELECT = """
SELECT i.*, c.lot_id AS lot_id, c.status AS cycle_status, l.product_id AS product_id
FROM inspections i
JOIN cycles c ON c.id = i.cycle_id
JOIN lots l ON l.id = c.lot_id
"""


@dataclass(frozen=True)
class NewInspection:
    cycle_id: int
    image_path: str
    image_sha256: str
    captured_at: str
    frame_age_ms: float | None
    model_id: str | None
    scores: dict[Grade, float] | None
    predicted_grade: Grade | None
    confidence: float | None
    latency_ms: float | None
    policy_threshold: float
    policy_version: str
    auto_decision: AutoDecision
    review_reason: ReviewReason | None
    created_at: str


def _to_inspection(row: sqlite3.Row) -> InspectionOut:
    scores = json.loads(row["scores_json"]) if row["scores_json"] else None
    return InspectionOut(
        id=row["id"],
        cycle_id=row["cycle_id"],
        lot_id=row["lot_id"],
        product_id=row["product_id"],
        captured_at=from_db(row["captured_at"]),
        image_url=f"/api/inspections/{row['id']}/image",
        model_id=row["model_id"],
        predicted_grade=Grade(row["predicted_grade"]) if row["predicted_grade"] else None,
        scores={Grade(k): v for k, v in scores.items()} if scores else None,
        confidence=row["confidence"],
        latency_ms=row["latency_ms"],
        auto_decision=AutoDecision(row["auto_decision"]),
        review_reason=ReviewReason(row["review_reason"]) if row["review_reason"] else None,
        final_decision=Destination(row["final_decision"]) if row["final_decision"] else None,
        decided_by=DecidedBy(row["decided_by"]) if row["decided_by"] else None,
        cycle_status=CycleStatus(row["cycle_status"]),
    )


def insert_inspection(conn: sqlite3.Connection, new: NewInspection) -> InspectionOut:
    automatic = new.auto_decision is not AutoDecision.REVIEW
    cur = conn.execute(
        """INSERT INTO inspections (cycle_id, image_path, image_sha256, captured_at, frame_age_ms,
               model_id, predicted_grade, scores_json, confidence, latency_ms, policy_threshold,
               policy_version, auto_decision, review_reason, final_decision, decided_by,
               created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            new.cycle_id,
            new.image_path,
            new.image_sha256,
            new.captured_at,
            new.frame_age_ms,
            new.model_id,
            new.predicted_grade.value if new.predicted_grade else None,
            json.dumps({g.value: s for g, s in new.scores.items()}) if new.scores else None,
            new.confidence,
            new.latency_ms,
            new.policy_threshold,
            new.policy_version,
            new.auto_decision.value,
            new.review_reason.value if new.review_reason else None,
            new.auto_decision.value if automatic else None,
            "auto" if automatic else None,
            new.created_at,
        ),
    )
    inspection = get_inspection(conn, cur.lastrowid or 0)
    assert inspection is not None
    return inspection


def get_inspection(conn: sqlite3.Connection, inspection_id: int) -> InspectionOut | None:
    row = conn.execute(_SELECT + " WHERE i.id = ?", (inspection_id,)).fetchone()
    return _to_inspection(row) if row else None


@dataclass(frozen=True)
class InspectionFilters:
    lot_id: int | None = None
    product_id: str | None = None
    grade: Grade | None = None
    outcome: InspectionOutcome | None = None
    captured_from: str | None = None  # database timestamps (UTC)
    captured_to: str | None = None


_OUTCOME_SQL: dict[InspectionOutcome, str] = {
    InspectionOutcome.APPROVED: "i.final_decision = 'APPROVED'",
    InspectionOutcome.REJECTED: "i.final_decision = 'REJECTED'",
    InspectionOutcome.PENDING_REVIEW: "i.auto_decision = 'REVIEW' AND i.final_decision IS NULL",
    InspectionOutcome.INCONCLUSIVE: "i.auto_decision = 'REVIEW'",
    InspectionOutcome.REVIEWED: "i.decided_by = 'operator'",
}


def _where(filters: InspectionFilters) -> tuple[str, list[object]]:
    clauses: list[str] = []
    params: list[object] = []
    for clause, value in (
        ("c.lot_id = ?", filters.lot_id),
        ("l.product_id = ?", filters.product_id),
        ("i.predicted_grade = ?", filters.grade.value if filters.grade else None),
        ("i.captured_at >= ?", filters.captured_from),
        ("i.captured_at < ?", filters.captured_to),
    ):
        if value is not None:
            clauses.append(clause)
            params.append(value)
    if filters.outcome is not None:
        clauses.append(_OUTCOME_SQL[filters.outcome])
    return (f"WHERE {' AND '.join(clauses)}" if clauses else ""), params


def list_inspections(
    conn: sqlite3.Connection, filters: InspectionFilters, *, limit: int, offset: int
) -> tuple[list[InspectionOut], int]:
    where, params = _where(filters)
    total = conn.execute(
        "SELECT COUNT(*) FROM inspections i JOIN cycles c ON c.id = i.cycle_id "  # noqa: S608
        f"JOIN lots l ON l.id = c.lot_id {where}",
        params,
    ).fetchone()[0]
    rows = conn.execute(
        f"{_SELECT} {where} ORDER BY i.id DESC LIMIT ? OFFSET ?",  # noqa: S608
        [*params, limit, offset],
    ).fetchall()
    return [_to_inspection(r) for r in rows], total


def export_rows(conn: sqlite3.Connection, filters: InspectionFilters) -> list[sqlite3.Row]:
    """Every matching inspection, oldest first, with what the CSV export shows."""
    where, params = _where(filters)
    return conn.execute(
        f"{_SELECT} {where} ORDER BY i.id",  # noqa: S608
        params,
    ).fetchall()


def get_inspection_by_cycle(conn: sqlite3.Connection, cycle_id: int) -> InspectionOut | None:
    row = conn.execute(_SELECT + " WHERE i.cycle_id = ?", (cycle_id,)).fetchone()
    return _to_inspection(row) if row else None


def get_image_path(conn: sqlite3.Connection, inspection_id: int) -> tuple[str, bool] | None:
    row = conn.execute(
        "SELECT image_path, image_purged_at FROM inspections WHERE id = ?", (inspection_id,)
    ).fetchone()
    return (row["image_path"], row["image_purged_at"] is not None) if row else None


def set_final_decision(
    conn: sqlite3.Connection, inspection_id: int, decision: Destination, decided_by: DecidedBy
) -> None:
    conn.execute(
        "UPDATE inspections SET final_decision = ?, decided_by = ? WHERE id = ?",
        (decision.value, decided_by.value, inspection_id),
    )


def _to_review(row: sqlite3.Row) -> ReviewOut:
    return ReviewOut(
        id=row["id"],
        inspection_id=row["inspection_id"],
        reviewer=row["reviewer"],
        previous_decision=(
            Destination(row["previous_decision"]) if row["previous_decision"] else None
        ),
        new_decision=Destination(row["new_decision"]),
        reason=row["reason"],
        created_at=from_db(row["created_at"]),
    )


def get_review_by_request(conn: sqlite3.Connection, request_id: str) -> ReviewOut | None:
    row = conn.execute("SELECT * FROM reviews WHERE request_id = ?", (request_id,)).fetchone()
    return _to_review(row) if row else None


def insert_review(
    conn: sqlite3.Connection,
    *,
    inspection_id: int,
    request_id: str,
    reviewer: str,
    previous: Destination | None,
    new: Destination,
    reason: str,
    created_at: str,
) -> ReviewOut:
    cur = conn.execute(
        """INSERT INTO reviews (inspection_id, request_id, reviewer, previous_decision,
               new_decision, reason, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            inspection_id,
            request_id,
            reviewer,
            previous.value if previous else None,
            new.value,
            reason,
            created_at,
        ),
    )
    row = conn.execute("SELECT * FROM reviews WHERE id = ?", (cur.lastrowid,)).fetchone()
    return _to_review(row)
