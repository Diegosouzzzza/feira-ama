"""Labeling agreement: two (or more) people label the same Coleta photos blind, compared after.

A reviewer's own labels are never used to decide what to show them next, and the comparison
route is the only place answers from different reviewers meet."""

import sqlite3

from amazonvision.core.clock import from_db
from amazonvision.domain.quality import Grade
from amazonvision.schemas.api import AgreementLabelOut, DatasetSampleOut
from amazonvision.storage.dataset import to_sample


def upsert_label(
    conn: sqlite3.Connection,
    *,
    sample_id: int,
    session: str,
    reviewer: str,
    label: Grade,
    at: str,
) -> AgreementLabelOut:
    conn.execute(
        """INSERT INTO label_agreement (sample_id, session, reviewer, label, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?)
           ON CONFLICT (sample_id, session, reviewer)
               DO UPDATE SET label = excluded.label, updated_at = excluded.updated_at""",
        (sample_id, session, reviewer, label.value, at, at),
    )
    row = conn.execute(
        """SELECT sample_id, reviewer, label, created_at FROM label_agreement
           WHERE sample_id = ? AND session = ? AND reviewer = ?""",
        (sample_id, session, reviewer),
    ).fetchone()
    assert row is not None
    return AgreementLabelOut(
        sample_id=row["sample_id"],
        reviewer=row["reviewer"],
        label=Grade(row["label"]),
        created_at=from_db(row["created_at"]),
    )


def next_for_reviewer(
    conn: sqlite3.Connection, *, product_id: str, session: str, reviewer: str
) -> tuple[DatasetSampleOut | None, int]:
    """The reviewer's next photo (oldest first) and how many, including it, are left."""
    rows = conn.execute(
        """SELECT s.* FROM dataset_samples s
           WHERE s.product_id = ?
             AND NOT EXISTS (
                 SELECT 1 FROM label_agreement a
                 WHERE a.sample_id = s.id AND a.session = ? AND a.reviewer = ?
             )
           ORDER BY s.id""",
        (product_id, session, reviewer),
    ).fetchall()
    if not rows:
        return None, 0
    return to_sample(rows[0]), len(rows)


def samples_with_labels(
    conn: sqlite3.Connection, *, product_id: str, session: str
) -> list[tuple[DatasetSampleOut, dict[str, Grade]]]:
    """Every photo of the product with at least one agreement label in this session."""
    rows = conn.execute(
        """SELECT DISTINCT s.* FROM dataset_samples s JOIN label_agreement a ON a.sample_id = s.id
           WHERE s.product_id = ? AND a.session = ? ORDER BY s.id""",
        (product_id, session),
    ).fetchall()
    result = []
    for row in rows:
        labels = conn.execute(
            "SELECT reviewer, label FROM label_agreement WHERE sample_id = ? AND session = ?",
            (row["id"], session),
        ).fetchall()
        result.append((to_sample(row), {r["reviewer"]: Grade(r["label"]) for r in labels}))
    return result
