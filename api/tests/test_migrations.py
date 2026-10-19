import json
import sqlite3
from pathlib import Path

import pytest

from amazonvision.core.clock import to_db, utc_now
from amazonvision.storage.migrator import (
    MIGRATIONS_DIR,
    MigrationError,
    connect,
    current_version,
    discover,
    migrate,
)

NOW = to_db(utc_now())
SHA = "a" * 64


@pytest.fixture
def db(tmp_path: Path):
    conn = connect(tmp_path / "av.sqlite")
    migrate(conn)
    yield conn
    conn.close()


def add_lot(conn, *, status="open", request_id="r-lot-1", product="tucuma", model=None):
    ended = None if status == "open" else NOW
    cur = conn.execute(
        """INSERT INTO lots (request_id, product_id, model_id, operator, status, is_simulated,
               policy_threshold, policy_version, config_snapshot_json, started_at, ended_at)
           VALUES (?, ?, ?, 'Equipe', ?, 1, 0.8, 'v1', '{}', ?, ?)""",
        (request_id, product, model, status, NOW, ended),
    )
    return cur.lastrowid


def add_cycle(conn, lot_id, seq, *, status="completed", destination="APPROVED", reason=None):
    ended = None if status == "running" else NOW
    cur = conn.execute(
        """INSERT INTO cycles (lot_id, seq_in_lot, status, commanded_destination, abort_reason,
               started_at, ended_at) VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (lot_id, seq, status, destination, reason, NOW, ended),
    )
    return cur.lastrowid


def add_inspection(conn, cycle_id, *, grade, auto, reason=None, final=None, by=None):
    scores = None if grade is None else json.dumps({"A": 0.6, "B": 0.3, "C": 0.1})
    confidence = None if grade is None else 0.6
    cur = conn.execute(
        """INSERT INTO inspections (cycle_id, image_path, image_sha256, captured_at,
               predicted_grade, scores_json, confidence, policy_threshold, policy_version,
               auto_decision, review_reason, final_decision, decided_by, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, 0.8, 'v1', ?, ?, ?, ?, ?)""",
        (
            cycle_id,
            f"img/{cycle_id}.jpg",
            SHA,
            NOW,
            grade,
            scores,
            confidence,
            auto,
            reason,
            final,
            by,
            NOW,
        ),
    )
    return cur.lastrowid


# ---------------------------------------------------------------- runner


def test_fresh_database_reaches_latest_version(db):
    assert current_version(db) == discover()[-1][0]
    assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    assert db.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    assert db.execute("PRAGMA journal_mode").fetchone()[0] == "wal"


def test_migrate_is_idempotent(db):
    assert migrate(db) == []


def test_refuses_database_newer_than_code(db):
    db.execute("PRAGMA user_version = 999")
    with pytest.raises(MigrationError):
        migrate(db)


def test_failed_migration_rolls_back(tmp_path: Path):
    folder = tmp_path / "migs"
    folder.mkdir()
    (folder / "001_ok.sql").write_text("CREATE TABLE a (x INTEGER);", "utf-8")
    (folder / "002_bad.sql").write_text("CREATE TABLE b (y INTEGER);\nSELEC broken;", "utf-8")
    conn = connect(":memory:")
    with pytest.raises(MigrationError):
        migrate(conn, folder)
    assert current_version(conn) == 1
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert "a" in tables
    assert "b" not in tables


def test_migration_files_do_not_manage_transactions(tmp_path: Path):
    folder = tmp_path / "migs"
    folder.mkdir()
    (folder / "001_tx.sql").write_text("BEGIN;\nCREATE TABLE a (x INTEGER);\nCOMMIT;", "utf-8")
    with pytest.raises(MigrationError):
        migrate(connect(":memory:"), folder)


def test_migrations_are_numbered_contiguously(tmp_path: Path):
    folder = tmp_path / "migs"
    folder.mkdir()
    (folder / "001_a.sql").write_text("SELECT 1;", "utf-8")
    (folder / "003_c.sql").write_text("SELECT 1;", "utf-8")
    with pytest.raises(MigrationError):
        discover(folder)


def test_shipped_migrations_are_valid():
    assert discover(MIGRATIONS_DIR)


def test_initial_profiles_are_seeded(db):
    rows = db.execute("SELECT id, name FROM product_profiles ORDER BY id").fetchall()
    assert [(r["id"], r["name"]) for r in rows] == [
        ("castanha", "Castanha-do-pará"),
        ("tucuma", "Tucumã"),
    ]


# ---------------------------------------------------------------- integrity rules


def test_only_one_open_lot(db):
    add_lot(db)
    with pytest.raises(sqlite3.IntegrityError):
        add_lot(db, request_id="r-lot-2")
    add_lot(db, status="closed", request_id="r-lot-3")


def test_lot_request_id_is_idempotency_key(db):
    add_lot(db, status="closed")
    with pytest.raises(sqlite3.IntegrityError):
        add_lot(db, status="closed")


def test_lot_model_must_belong_to_same_product(db):
    db.execute(
        """INSERT INTO model_versions (id, product_id, architecture, weights_path, weights_sha256,
               class_order_json, preprocess_json, dataset_version, created_at)
           VALUES ('cast-v1', 'castanha', 'mobilenet_v3_small', 'm.onnx', ?, '["A","B","C"]',
                   '{}', 'ds1', ?)""",
        (SHA, NOW),
    )
    with pytest.raises(sqlite3.IntegrityError):
        add_lot(db, product="tucuma", model="cast-v1")
    add_lot(db, product="castanha", model="cast-v1")


def test_only_one_running_cycle(db):
    lot = add_lot(db)
    add_cycle(db, lot, 1, status="running", destination=None)
    with pytest.raises(sqlite3.IntegrityError):
        add_cycle(db, lot, 2, status="running", destination=None)


def test_aborted_cycle_requires_reason(db):
    lot = add_lot(db)
    with pytest.raises(sqlite3.IntegrityError):
        add_cycle(db, lot, 1, status="aborted", destination=None)


def test_auto_decision_needs_final_decision_and_review_needs_reason(db):
    lot = add_lot(db)
    c1 = add_cycle(db, lot, 1)
    with pytest.raises(sqlite3.IntegrityError):
        add_inspection(db, c1, grade="A", auto="APPROVED")
    with pytest.raises(sqlite3.IntegrityError):
        add_inspection(db, c1, grade="A", auto="REVIEW")


def test_original_prediction_is_immutable_and_not_deletable(db):
    lot = add_lot(db)
    cycle = add_cycle(db, lot, 1)
    insp = add_inspection(db, cycle, grade="A", auto="REVIEW", reason="LOW_CONFIDENCE")
    with pytest.raises(sqlite3.IntegrityError, match="imutavel"):
        db.execute("UPDATE inspections SET predicted_grade = 'C' WHERE id = ?", (insp,))
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("DELETE FROM inspections WHERE id = ?", (insp,))
    db.execute(
        "UPDATE inspections SET final_decision = 'REJECTED', decided_by = 'operator' WHERE id = ?",
        (insp,),
    )


def test_reviews_are_append_only(db):
    lot = add_lot(db)
    cycle = add_cycle(db, lot, 1)
    insp = add_inspection(db, cycle, grade="A", auto="REVIEW", reason="LOW_CONFIDENCE")
    db.execute(
        """INSERT INTO reviews (inspection_id, request_id, reviewer, new_decision, reason,
               created_at) VALUES (?, 'r1', 'Ana', 'REJECTED', 'mancha visível', ?)""",
        (insp, NOW),
    )
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("UPDATE reviews SET new_decision = 'APPROVED'")
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("DELETE FROM reviews")


def test_duplicate_device_event_is_rejected(db):
    sql = """INSERT INTO events (source, type, severity, boot_id, device_seq, occurred_at)
             VALUES ('device', 'STATE_CHANGED', 'info', 'b0071d2e', 42, ?)"""
    db.execute(sql, (NOW,))
    with pytest.raises(sqlite3.IntegrityError):
        db.execute(sql, (NOW,))


def test_host_events_do_not_need_device_ids(db):
    for _ in range(2):
        db.execute(
            "INSERT INTO events (source, type, severity, occurred_at) "
            "VALUES ('host', 'CONNECTION_LOST', 'warning', ?)",
            (NOW,),
        )


def test_timestamps_must_be_utc_iso(db):
    with pytest.raises(sqlite3.IntegrityError):
        db.execute(
            "INSERT INTO events (source, type, severity, occurred_at) "
            "VALUES ('host', 'X', 'info', '18/10/2026 15:00')"
        )


def test_labeled_sample_requires_label_and_author(db):
    with pytest.raises(sqlite3.IntegrityError):
        db.execute(
            """INSERT INTO dataset_samples (product_id, physical_sample_id, collection_session,
                   image_path, image_sha256, status, created_at, updated_at)
               VALUES ('tucuma', 'T-001', 'S1', 'ds/1.jpg', ?, 'labeled', ?, ?)""",
            (SHA, NOW, NOW),
        )


# ---------------------------------------------------------------- derived summary


def test_lot_summary_is_derived_from_records(db):
    lot = add_lot(db)
    c1 = add_cycle(db, lot, 1, destination="APPROVED")
    add_inspection(db, c1, grade="A", auto="APPROVED", final="APPROVED", by="auto")
    c2 = add_cycle(db, lot, 2, destination="REJECTED")
    add_inspection(db, c2, grade="B", auto="REJECTED", final="REJECTED", by="auto")
    c3 = add_cycle(db, lot, 3, destination="REJECTED")
    add_inspection(
        db, c3, grade="A", auto="REVIEW", reason="LOW_CONFIDENCE", final="REJECTED", by="operator"
    )
    c4 = add_cycle(db, lot, 4, status="aborted", destination=None, reason="S2_TIMEOUT")
    add_inspection(db, c4, grade=None, auto="REVIEW", reason="INVALID_IMAGE")

    row = dict(db.execute("SELECT * FROM v_lot_summary WHERE lot_id = ?", (lot,)).fetchone())
    assert row == {
        "lot_id": lot,
        "inspected": 4,
        "approved": 1,
        "rejected": 2,
        "review_pending": 1,
        "reviewed": 1,
        "grade_a": 2,
        "grade_b": 1,
        "grade_c": 0,
        "cycles_completed": 3,
        "cycles_aborted": 1,
    }


def test_empty_lot_summary_has_zeros(db):
    lot = add_lot(db)
    row = dict(db.execute("SELECT * FROM v_lot_summary WHERE lot_id = ?", (lot,)).fetchone())
    assert row["inspected"] == 0
    assert row["cycles_completed"] == 0
