import json
import sqlite3
from typing import Any

from amazonvision.core.clock import from_db
from amazonvision.domain.quality import Grade
from amazonvision.schemas.api import LotOut, LotStatus, LotSummary


def _to_lot(row: sqlite3.Row) -> LotOut:
    return LotOut(
        id=row["id"],
        product_id=row["product_id"],
        model_id=row["model_id"],
        operator=row["operator"],
        status=LotStatus(row["status"]),
        is_simulated=bool(row["is_simulated"]),
        started_at=from_db(row["started_at"]),
        ended_at=from_db(row["ended_at"]) if row["ended_at"] else None,
        notes=row["notes"],
    )


def get_lot(conn: sqlite3.Connection, lot_id: int) -> LotOut | None:
    row = conn.execute("SELECT * FROM lots WHERE id = ?", (lot_id,)).fetchone()
    return _to_lot(row) if row else None


def get_lot_row_by_request(conn: sqlite3.Connection, request_id: str) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM lots WHERE request_id = ?", (request_id,)).fetchone()


def get_open_lot(conn: sqlite3.Connection) -> LotOut | None:
    row = conn.execute("SELECT * FROM lots WHERE status = 'open'").fetchone()
    return _to_lot(row) if row else None


def list_lots(
    conn: sqlite3.Connection, *, limit: int, offset: int, product_id: str | None = None
) -> list[LotOut]:
    sql = "SELECT * FROM lots"
    params: list[Any] = []
    if product_id is not None:
        sql += " WHERE product_id = ?"
        params.append(product_id)
    sql += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params += [limit, offset]
    return [_to_lot(r) for r in conn.execute(sql, params).fetchall()]


def insert_lot(
    conn: sqlite3.Connection,
    *,
    request_id: str,
    product_id: str,
    model_id: str | None,
    operator: str,
    is_simulated: bool,
    policy_threshold: float,
    policy_version: str,
    config_snapshot: dict[str, Any],
    notes: str | None,
    started_at: str,
) -> int:
    cur = conn.execute(
        """INSERT INTO lots (request_id, product_id, model_id, operator, status, is_simulated,
               policy_threshold, policy_version, config_snapshot_json, notes, started_at)
           VALUES (?, ?, ?, ?, 'open', ?, ?, ?, ?, ?, ?)""",
        (
            request_id,
            product_id,
            model_id,
            operator,
            int(is_simulated),
            policy_threshold,
            policy_version,
            json.dumps(config_snapshot, ensure_ascii=False, sort_keys=True),
            notes,
            started_at,
        ),
    )
    assert cur.lastrowid is not None
    return cur.lastrowid


def close_lot(conn: sqlite3.Connection, lot_id: int, ended_at: str) -> None:
    conn.execute(
        "UPDATE lots SET status = 'closed', ended_at = ? WHERE id = ? AND status = 'open'",
        (ended_at, lot_id),
    )


def has_running_cycle(conn: sqlite3.Connection, lot_id: int) -> bool:
    row = conn.execute(
        "SELECT 1 FROM cycles WHERE lot_id = ? AND status = 'running' LIMIT 1", (lot_id,)
    ).fetchone()
    return row is not None


def get_summary(conn: sqlite3.Connection, lot_id: int) -> LotSummary | None:
    row = conn.execute("SELECT * FROM v_lot_summary WHERE lot_id = ?", (lot_id,)).fetchone()
    if row is None:
        return None
    decided = row["approved"] + row["rejected"]
    return LotSummary(
        lot_id=lot_id,
        inspected=row["inspected"],
        approved=row["approved"],
        rejected=row["rejected"],
        review_pending=row["review_pending"],
        reviewed=row["reviewed"],
        by_grade={Grade.A: row["grade_a"], Grade.B: row["grade_b"], Grade.C: row["grade_c"]},
        cycles_completed=row["cycles_completed"],
        cycles_aborted=row["cycles_aborted"],
        approval_rate=(row["approved"] / decided) if decided else None,
        approval_rate_denominator=decided,
    )
