import sqlite3

from amazonvision.schemas.api import ProductOut


def _to_product(row: sqlite3.Row) -> ProductOut:
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
    return [_to_product(r) for r in rows]


def get_product_row(conn: sqlite3.Connection, product_id: str) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM product_profiles WHERE id = ?", (product_id,)).fetchone()
