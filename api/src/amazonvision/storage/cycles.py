import sqlite3

from amazonvision.core.clock import from_db
from amazonvision.domain.quality import Destination
from amazonvision.schemas.api import CycleOut, CycleStatus


def _to_cycle(row: sqlite3.Row) -> CycleOut:
    return CycleOut(
        id=row["id"],
        lot_id=row["lot_id"],
        seq_in_lot=row["seq_in_lot"],
        status=CycleStatus(row["status"]),
        machine_state=None,
        commanded_destination=(
            Destination(row["commanded_destination"]) if row["commanded_destination"] else None
        ),
        abort_reason=row["abort_reason"],
        started_at=from_db(row["started_at"]),
        ended_at=from_db(row["ended_at"]) if row["ended_at"] else None,
    )


def get_cycle(conn: sqlite3.Connection, cycle_id: int) -> CycleOut | None:
    row = conn.execute("SELECT * FROM cycles WHERE id = ?", (cycle_id,)).fetchone()
    return _to_cycle(row) if row else None


def insert_cycle(
    conn: sqlite3.Connection, *, lot_id: int, device_session_id: int | None, started_at: str
) -> CycleOut:
    seq = conn.execute(
        "SELECT COALESCE(MAX(seq_in_lot), 0) + 1 FROM cycles WHERE lot_id = ?", (lot_id,)
    ).fetchone()[0]
    cur = conn.execute(
        """INSERT INTO cycles (lot_id, seq_in_lot, device_session_id, status, started_at)
           VALUES (?, ?, ?, 'running', ?)""",
        (lot_id, seq, device_session_id, started_at),
    )
    cycle = get_cycle(conn, cur.lastrowid or 0)
    assert cycle is not None
    return cycle


def complete_cycle(
    conn: sqlite3.Connection, cycle_id: int, destination: Destination, ended_at: str
) -> bool:
    cur = conn.execute(
        """UPDATE cycles SET status = 'completed', commanded_destination = ?, ended_at = ?
           WHERE id = ? AND status = 'running'""",
        (destination.value, ended_at, cycle_id),
    )
    return cur.rowcount == 1


def abort_cycle(conn: sqlite3.Connection, cycle_id: int, reason: str, ended_at: str) -> bool:
    cur = conn.execute(
        """UPDATE cycles SET status = 'aborted', abort_reason = ?, ended_at = ?
           WHERE id = ? AND status = 'running'""",
        (reason, ended_at, cycle_id),
    )
    return cur.rowcount == 1


def abort_running_cycles(conn: sqlite3.Connection, reason: str, ended_at: str) -> list[int]:
    ids = [r[0] for r in conn.execute("SELECT id FROM cycles WHERE status = 'running'")]
    for cycle_id in ids:
        abort_cycle(conn, cycle_id, reason, ended_at)
    return ids


def open_device_session(
    conn: sqlite3.Connection,
    *,
    boot_id: str,
    session_id: str,
    firmware_version: str | None,
    protocol_version: int,
    port: str | None,
    opened_at: str,
) -> int:
    cur = conn.execute(
        """INSERT INTO device_sessions (boot_id, session_id, firmware_version, protocol_version,
               port, opened_at) VALUES (?, ?, ?, ?, ?, ?)""",
        (boot_id, session_id, firmware_version, protocol_version, port, opened_at),
    )
    return cur.lastrowid or 0


def close_device_session(conn: sqlite3.Connection, session_db_id: int, closed_at: str) -> None:
    conn.execute(
        "UPDATE device_sessions SET closed_at = ? WHERE id = ? AND closed_at IS NULL",
        (closed_at, session_db_id),
    )
