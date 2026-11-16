"""Photo collection for training: one row per photo, pointing to a file under dataset/."""

import json
import sqlite3
from typing import Any

from amazonvision.core.clock import from_db
from amazonvision.domain.quality import Grade
from amazonvision.schemas.api import DatasetClassCount, DatasetSampleOut, SampleStatus


def to_sample(row: sqlite3.Row) -> DatasetSampleOut:
    return DatasetSampleOut(
        id=row["id"],
        product_id=row["product_id"],
        physical_sample_id=row["physical_sample_id"],
        collection_session=row["collection_session"],
        image_url=f"/api/dataset/samples/{row['id']}/image",
        label=Grade(row["label"]) if row["label"] else None,
        label_author=row["label_author"],
        status=SampleStatus(row["status"]),
        reviewed_by=row["reviewed_by"],
        created_at=from_db(row["created_at"]),
        updated_at=from_db(row["updated_at"]),
    )


def insert_sample(
    conn: sqlite3.Connection,
    *,
    product_id: str,
    physical_sample_id: str,
    collection_session: str,
    image_path: str,
    image_sha256: str,
    label: Grade | None,
    author: str,
    capture_config: dict[str, Any],
    at: str,
) -> int:
    cursor = conn.execute(
        """INSERT INTO dataset_samples (product_id, physical_sample_id, collection_session,
               image_path, image_sha256, label, label_author, status, capture_config_json,
               created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            product_id,
            physical_sample_id,
            collection_session,
            image_path,
            image_sha256,
            label.value if label else None,
            author if label else None,
            (SampleStatus.LABELED if label else SampleStatus.PENDING).value,
            json.dumps(capture_config, default=str),
            at,
            at,
        ),
    )
    assert cursor.lastrowid is not None
    return cursor.lastrowid


def get_sample(conn: sqlite3.Connection, sample_id: int) -> DatasetSampleOut | None:
    row = conn.execute("SELECT * FROM dataset_samples WHERE id = ?", (sample_id,)).fetchone()
    return to_sample(row) if row else None


def get_image_path(conn: sqlite3.Connection, sample_id: int) -> str | None:
    row = conn.execute(
        "SELECT image_path FROM dataset_samples WHERE id = ?", (sample_id,)
    ).fetchone()
    return row[0] if row else None


def piece_labels(
    conn: sqlite3.Connection, product_id: str, physical_sample_id: str, *, exclude: int | None
) -> set[Grade]:
    """Labels already given to other photos of the same physical piece."""
    rows = conn.execute(
        """SELECT DISTINCT label FROM dataset_samples
           WHERE product_id = ? AND physical_sample_id = ? AND status = 'labeled'
             AND id IS NOT ?""",
        (product_id, physical_sample_id, exclude),
    ).fetchall()
    return {Grade(r[0]) for r in rows}


def update_sample(
    conn: sqlite3.Connection,
    sample_id: int,
    *,
    status: SampleStatus,
    label: Grade | None,
    reviewer: str,
    at: str,
) -> None:
    labeled = status is SampleStatus.LABELED
    conn.execute(
        """UPDATE dataset_samples
           SET status = ?, label = ?, label_author = ?, reviewed_by = ?, split = NULL,
               updated_at = ?
           WHERE id = ?""",
        (
            status.value,
            label.value if labeled and label else None,
            reviewer if labeled else None,
            reviewer,
            at,
            sample_id,
        ),
    )


def list_samples(
    conn: sqlite3.Connection,
    *,
    product_id: str | None,
    status: SampleStatus | None,
    label: Grade | None,
    physical_sample_id: str | None,
    limit: int,
    offset: int,
) -> tuple[list[DatasetSampleOut], int]:
    where, params = [], []
    for column, value in (
        ("product_id", product_id),
        ("status", status.value if status else None),
        ("label", label.value if label else None),
        ("physical_sample_id", physical_sample_id),
    ):
        if value is not None:
            where.append(f"{column} = ?")
            params.append(value)
    clause = f" WHERE {' AND '.join(where)}" if where else ""
    total = conn.execute(f"SELECT COUNT(*) FROM dataset_samples{clause}", params).fetchone()[0]  # noqa: S608
    rows = conn.execute(
        f"SELECT * FROM dataset_samples{clause} ORDER BY id DESC LIMIT ? OFFSET ?",  # noqa: S608
        [*params, limit, offset],
    ).fetchall()
    return [to_sample(r) for r in rows], total


def summary_counts(
    conn: sqlite3.Connection, product_id: str
) -> tuple[list[DatasetClassCount], dict[str, int]]:
    by_class = {
        Grade(r["label"]): r
        for r in conn.execute(
            """SELECT label, COUNT(*) AS photos, COUNT(DISTINCT physical_sample_id) AS pieces
               FROM dataset_samples WHERE product_id = ? AND status = 'labeled'
               GROUP BY label""",
            (product_id,),
        ).fetchall()
    }
    classes = [
        DatasetClassCount(
            label=grade,
            photos=by_class[grade]["photos"] if grade in by_class else 0,
            pieces=by_class[grade]["pieces"] if grade in by_class else 0,
        )
        for grade in Grade
    ]
    statuses = dict(
        conn.execute(
            "SELECT status, COUNT(*) FROM dataset_samples WHERE product_id = ? GROUP BY status",
            (product_id,),
        ).fetchall()
    )
    return classes, statuses


def labeled_for_export(conn: sqlite3.Connection, product_id: str) -> list[sqlite3.Row]:
    return conn.execute(
        """SELECT image_path, product_id, physical_sample_id, label FROM dataset_samples
           WHERE product_id = ? AND status = 'labeled' ORDER BY id""",
        (product_id,),
    ).fetchall()
