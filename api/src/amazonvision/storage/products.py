import sqlite3

from amazonvision.schemas.api import ProductOut


def to_product(row: sqlite3.Row) -> ProductOut:
    return ProductOut(
        id=row["id"],
        name=row["name"],
        presentation=row["presentation"],
        active_model_id=row["active_model_id"],
        decision_threshold=row["decision_threshold"],
        version=row["version"],
    )


def list_products(conn: sqlite3.Connection) -> list[ProductOut]:
    rows = conn.execute("SELECT * FROM product_profiles ORDER BY name").fetchall()
    return [to_product(r) for r in rows]


def get_product_row(conn: sqlite3.Connection, product_id: str) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM product_profiles WHERE id = ?", (product_id,)).fetchone()


def update_config(
    conn: sqlite3.Connection,
    product_id: str,
    *,
    expected_version: int,
    presentation: str | None,
    decision_threshold: float,
    bench_config_json: str,
    at: str,
) -> bool:
    """Optimistic update: False when someone saved another version in the meantime."""
    cursor = conn.execute(
        """UPDATE product_profiles
           SET presentation = ?, decision_threshold = ?, bench_config_json = ?,
               version = version + 1, updated_at = ?
           WHERE id = ? AND version = ?""",
        (presentation, decision_threshold, bench_config_json, at, product_id, expected_version),
    )
    return cursor.rowcount == 1
