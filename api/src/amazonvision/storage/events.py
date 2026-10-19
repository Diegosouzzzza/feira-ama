import json
import sqlite3
from typing import Any

from amazonvision.core.clock import from_db
from amazonvision.schemas.api import EventOut, EventSource, Severity


def add_event(
    conn: sqlite3.Connection,
    *,
    source: EventSource,
    type: str,
    severity: Severity,
    occurred_at: str,
    data: dict[str, Any] | None = None,
    lot_id: int | None = None,
    cycle_id: int | None = None,
    boot_id: str | None = None,
    device_seq: int | None = None,
) -> int | None:
    """Insert an event. Returns None if the device event (boot_id, device_seq) already exists."""
    row = conn.execute(
        """INSERT INTO events (source, type, severity, boot_id, device_seq, lot_id, cycle_id,
               data_json, occurred_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT (boot_id, device_seq) DO NOTHING
           RETURNING id""",
        (
            source.value,
            type,
            severity.value,
            boot_id,
            device_seq,
            lot_id,
            cycle_id,
            json.dumps(data or {}, ensure_ascii=False),
            occurred_at,
        ),
    ).fetchone()
    return row[0] if row else None


def list_events(
    conn: sqlite3.Connection,
    *,
    limit: int,
    offset: int,
    severity: Severity | None = None,
    source: EventSource | None = None,
    type: str | None = None,
    lot_id: int | None = None,
) -> list[EventOut]:
    sql = "SELECT * FROM events"
    where: list[str] = []
    params: list[Any] = []
    for clause, value in (
        ("severity = ?", severity.value if severity else None),
        ("source = ?", source.value if source else None),
        ("type = ?", type),
        ("lot_id = ?", lot_id),
    ):
        if value is not None:
            where.append(clause)
            params.append(value)
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params += [limit, offset]
    return [
        EventOut(
            id=r["id"],
            source=EventSource(r["source"]),
            type=r["type"],
            severity=Severity(r["severity"]),
            lot_id=r["lot_id"],
            cycle_id=r["cycle_id"],
            data=json.loads(r["data_json"]),
            occurred_at=from_db(r["occurred_at"]),
        )
        for r in conn.execute(sql, params).fetchall()
    ]
