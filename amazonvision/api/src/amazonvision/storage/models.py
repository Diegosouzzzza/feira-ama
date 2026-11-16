import json
import sqlite3

from amazonvision.core.clock import from_db
from amazonvision.domain.quality import Grade
from amazonvision.schemas.api import ModelOut, ModelValidationStatus
from amazonvision.vision.package import ModelPackage

_SELECT = """
SELECT m.*, (p.active_model_id = m.id) AS active
FROM model_versions m JOIN product_profiles p ON p.id = m.product_id
"""


def _to_model(row: sqlite3.Row) -> ModelOut:
    return ModelOut(
        id=row["id"],
        product_id=row["product_id"],
        architecture=row["architecture"],
        class_order=[Grade(g) for g in json.loads(row["class_order_json"])],
        dataset_version=row["dataset_version"],
        validation_status=ModelValidationStatus(row["validation_status"]),
        validated_by=row["validated_by"],
        metrics=json.loads(row["metrics_json"]) if row["metrics_json"] else None,
        recommended_threshold=row["recommended_threshold"],
        active=bool(row["active"]),
        created_at=from_db(row["created_at"]),
    )


def list_models(conn: sqlite3.Connection, product_id: str | None = None) -> list[ModelOut]:
    sql, params = _SELECT, []
    if product_id is not None:
        sql += " WHERE m.product_id = ?"
        params.append(product_id)
    sql += " ORDER BY m.created_at DESC"
    return [_to_model(r) for r in conn.execute(sql, params).fetchall()]


def get_model(conn: sqlite3.Connection, model_id: str) -> ModelOut | None:
    row = conn.execute(_SELECT + " WHERE m.id = ?", (model_id,)).fetchone()
    return _to_model(row) if row else None


def insert_model(
    conn: sqlite3.Connection, package: ModelPackage, weights_path: str, created_at: str
) -> None:
    conn.execute(
        """INSERT INTO model_versions (id, product_id, architecture, weights_path, weights_sha256,
               class_order_json, preprocess_json, dataset_version, metrics_json,
               validation_status, recommended_threshold, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?, ?)""",
        (
            package.model_id,
            package.product_id,
            package.architecture,
            weights_path,
            package.weights_sha256,
            json.dumps([g.value for g in package.class_order]),
            json.dumps(package.preprocess.to_dict()),
            package.dataset_version,
            json.dumps(package.metrics),
            package.recommended_threshold,
            created_at,
        ),
    )


def set_validation(
    conn: sqlite3.Connection,
    model_id: str,
    status: ModelValidationStatus,
    reviewer: str,
    at: str,
) -> None:
    conn.execute(
        """UPDATE model_versions SET validation_status = ?, validated_by = ?, validated_at = ?
           WHERE id = ?""",
        (status.value, reviewer, at, model_id),
    )


def activate(
    conn: sqlite3.Connection, product_id: str, model_id: str, threshold: float | None, at: str
) -> None:
    conn.execute(
        """UPDATE product_profiles
           SET active_model_id = ?, decision_threshold = COALESCE(?, decision_threshold),
               version = version + 1, updated_at = ?
           WHERE id = ?""",
        (model_id, threshold, at, product_id),
    )
