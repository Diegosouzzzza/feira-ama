"""Backups (consistent zip of the data folder) and automatic/manual photo retention."""

import io
import sqlite3
import zipfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

from fastapi.testclient import TestClient

from amazonvision.domain.quality import Grade
from amazonvision.services import retention as retention_module
from amazonvision.simulation.scenario import confident
from tests.test_cycle_simulated import inspections_of
from tests.test_history_config import close_lot, run_lot


def travel_forward(monkeypatch, days: int) -> None:
    """`captured_at` is immutable by design (inspections_prediction_immutable trigger), so
    retention tests move the service's clock forward instead of backdating rows."""
    future = datetime.now(UTC) + timedelta(days=days)
    monkeypatch.setattr(retention_module, "utc_now", lambda: future)


# ---------------------------------------------------------------- retention


def test_purge_removes_old_photos_but_keeps_the_open_lot(client: TestClient, control, monkeypatch):
    closed_lot = run_lot(client, control, confident(Grade.A))
    [old_inspection] = inspections_of(client, closed_lot["id"])
    close_lot(client, control, closed_lot["id"])

    open_lot = run_lot(client, control, confident(Grade.A))
    [recent_inspection] = inspections_of(client, open_lot["id"])

    travel_forward(monkeypatch, days=40)  # both inspections are now "old"; the open lot stays
    response = client.post("/api/images/purge", params={"max_age_days": 30}, headers=control)
    assert response.status_code == 200, response.text
    result = response.json()
    assert result["purged"] == 1
    assert result["freed_bytes"] > 0

    purged_image = client.get(old_inspection["image_url"])
    assert purged_image.status_code == 404
    assert purged_image.json()["code"] == "NOT_FOUND"

    kept_image = client.get(recent_inspection["image_url"])
    assert kept_image.status_code == 200

    events = client.get("/api/diagnostics/events", params={"type": "IMAGES_PURGED"}).json()
    [event] = events
    assert event["data"]["count"] == 1
    assert event["data"]["operator"] == "Ana"


def test_purge_uses_the_configured_default_age(client: TestClient, control, monkeypatch):
    lot = run_lot(client, control, confident(Grade.A))
    inspections_of(client, lot["id"])
    close_lot(client, control, lot["id"])
    default_days = client.app.state.services.settings.image_retention_days

    travel_forward(monkeypatch, days=default_days + 5)
    response = client.post("/api/images/purge", headers=control)
    assert response.json()["purged"] == 1


def test_purge_nothing_to_do_is_not_an_error(client: TestClient, control):
    response = client.post("/api/images/purge", headers=control)
    assert response.status_code == 200
    assert response.json() == {"purged": 0, "freed_bytes": 0}


def test_purge_needs_control(client: TestClient):
    assert client.post("/api/images/purge").status_code == 423


# ---------------------------------------------------------------- backups


def read_zip_inspection_count(content: bytes, tmp_path: Path) -> int:
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        db_bytes = archive.read("db/amazonvision.sqlite")
    path = tmp_path / "snapshot.sqlite"
    path.write_bytes(db_bytes)
    with sqlite3.connect(path) as conn:
        return conn.execute("SELECT COUNT(*) FROM inspections").fetchone()[0]


def test_create_backup_contains_a_consistent_db_snapshot(
    client: TestClient, control, tmp_path: Path
):
    lot = run_lot(client, control, confident(Grade.A), confident(Grade.A))
    close_lot(client, control, lot["id"])

    response = client.post("/api/backups", headers=control)
    assert response.status_code == 201, response.text
    backup = response.json()
    assert backup["name"].startswith("backup-") and backup["name"].endswith(".zip")
    assert backup["inspections"] == 2
    assert backup["size_bytes"] > 0

    download = client.get(f"/api/backups/{backup['name']}/file")
    assert download.status_code == 200
    assert download.headers["content-type"] == "application/zip"
    assert read_zip_inspection_count(download.content, tmp_path) == 2


def test_list_backups_shows_created_ones(client: TestClient, control):
    assert client.get("/api/backups").json() == []
    created = client.post("/api/backups", headers=control).json()
    [listed] = client.get("/api/backups").json()
    assert listed["name"] == created["name"]
    assert listed["size_bytes"] == created["size_bytes"]


def test_delete_backup_removes_the_file(client: TestClient, control):
    backup = client.post("/api/backups", headers=control).json()
    assert client.delete(f"/api/backups/{backup['name']}", headers=control).status_code == 204
    assert client.get("/api/backups").json() == []
    assert client.get(f"/api/backups/{backup['name']}/file").status_code == 404


def test_backup_download_refuses_paths_outside_the_folder(client: TestClient, control):
    client.post("/api/backups", headers=control)
    traversal = client.get("/api/backups/..%2F..%2Fpyproject.toml/file")
    assert traversal.status_code in (404, 422)
    assert client.get("/api/backups/not-a-real-backup.zip/file").status_code == 404


def test_backups_need_control_to_create_or_delete(client: TestClient, control):
    assert client.post("/api/backups").status_code == 423
    backup = client.post("/api/backups", headers=control).json()
    assert client.delete(f"/api/backups/{backup['name']}").status_code == 423
