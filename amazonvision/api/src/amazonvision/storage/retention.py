"""Automatic cleanup of old inspection photos. The database row (prediction, decision, the
events it produced) is kept forever; only the image file and `image_purged_at` change."""

import sqlite3


def purge_candidates(
    conn: sqlite3.Connection, *, before: str, exclude_lot_id: int | None, limit: int
) -> list[tuple[int, str]]:
    """Inspections not yet purged, older than `before`, outside the lot still open (if any)."""
    sql = """SELECT i.id, i.image_path FROM inspections i JOIN cycles c ON c.id = i.cycle_id
             WHERE i.image_purged_at IS NULL AND i.captured_at < ?"""
    params: list[object] = [before]
    if exclude_lot_id is not None:
        sql += " AND c.lot_id != ?"
        params.append(exclude_lot_id)
    sql += " ORDER BY i.captured_at LIMIT ?"
    params.append(limit)
    return [(r["id"], r["image_path"]) for r in conn.execute(sql, params).fetchall()]


def mark_purged(conn: sqlite3.Connection, inspection_ids: list[int], at: str) -> None:
    conn.executemany(
        "UPDATE inspections SET image_purged_at = ? WHERE id = ?",
        [(at, i) for i in inspection_ids],
    )
