from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

from amazonvision.training.dataset import read_manifest


def capture(
    client: TestClient,
    headers: dict[str, str],
    piece: str = "T-0001",
    label: str | None = "A",
    product: str = "tucuma",
) -> Any:
    body = {
        "product_id": product,
        "physical_sample_id": piece,
        "collection_session": "2026-10-19-manha",
        "label": label,
    }
    return client.post("/api/dataset/capture", json=body, headers=headers)


def test_capture_stores_labeled_photo(client: TestClient, control, settings):
    response = capture(client, control)
    assert response.status_code == 201, response.text
    sample = response.json()
    assert sample["status"] == "labeled"
    assert sample["label"] == "A"
    assert sample["label_author"] == "Ana"

    image = client.get(sample["image_url"])
    assert image.status_code == 200
    assert image.content.startswith(b"\x89PNG")
    folder = settings.data_root / "dataset" / "tucuma" / "2026-10-19-manha"
    assert [f.name.startswith("T-0001_") for f in folder.iterdir()] == [True]


def test_every_capture_is_a_distinct_photo(client: TestClient, control):
    first = capture(client, control).json()
    second = capture(client, control).json()
    assert first["id"] != second["id"]
    assert client.get(first["image_url"]).content != client.get(second["image_url"]).content


def test_label_later_then_review(client: TestClient, control):
    sample = capture(client, control, label=None).json()
    assert sample["status"] == "pending"
    assert sample["label"] is None

    url = f"/api/dataset/samples/{sample['id']}"
    missing = client.patch(url, json={"status": "labeled"}, headers=control)
    assert missing.status_code == 422

    labeled = client.patch(url, json={"status": "labeled", "label": "C"}, headers=control)
    assert labeled.status_code == 200, labeled.text
    assert labeled.json()["label"] == "C"
    assert labeled.json()["reviewed_by"] == "Ana"

    unusable = client.patch(url, json={"status": "unusable", "label": "C"}, headers=control)
    assert unusable.json()["status"] == "unusable"
    assert unusable.json()["label"] is None


def test_one_physical_piece_keeps_one_label(client: TestClient, control):
    capture(client, control, piece="T-0007", label="B")
    conflict = capture(client, control, piece="T-0007", label="A")
    assert conflict.status_code == 409
    assert conflict.json()["code"] == "CONFLICT"

    pending = capture(client, control, piece="T-0007", label=None).json()
    relabel = client.patch(
        f"/api/dataset/samples/{pending['id']}",
        json={"status": "labeled", "label": "A"},
        headers=control,
    )
    assert relabel.status_code == 409


def test_capture_needs_control_and_valid_tags(client: TestClient, control):
    assert capture(client, {}).status_code == 423
    assert capture(client, control, piece="../fora").status_code == 422
    assert capture(client, control, product="acai").status_code == 422


def test_capture_refused_while_the_belt_runs(client: TestClient, control):
    client.app.state.services.dataset._machine_busy = lambda: True
    response = capture(client, control)
    assert response.status_code == 409
    assert response.json()["code"] == "INVALID_STATE"


def test_capture_without_camera_image(client: TestClient, control):
    client.app.state.services.simulation.camera.available = False
    response = capture(client, control)
    assert response.status_code == 503
    assert response.json()["code"] == "CAMERA_UNAVAILABLE"


def test_summary_counts_photos_and_pieces(client: TestClient, control):
    capture(client, control, piece="T-1", label="A")
    capture(client, control, piece="T-1", label="A")
    capture(client, control, piece="T-2", label="A")
    capture(client, control, piece="T-3", label="C")
    capture(client, control, piece="T-4", label=None)
    capture(client, control, piece="C-1", label="B", product="castanha")

    summary = client.get("/api/dataset/summary", params={"product_id": "tucuma"}).json()
    classes = {c["label"]: c for c in summary["classes"]}
    assert classes["A"] == {"label": "A", "photos": 3, "pieces": 2}
    assert classes["B"]["photos"] == 0
    assert classes["C"]["pieces"] == 1
    assert summary["pending"] == 1
    assert summary["total"] == 5
    assert summary["target_photos_per_class"] >= 300


def test_list_filters_and_pages(client: TestClient, control):
    for i in range(3):
        capture(client, control, piece=f"T-{i}", label="A")
    capture(client, control, piece="T-9", label=None)

    page = client.get("/api/dataset/samples", params={"status": "labeled", "limit": 2}).json()
    assert page["total"] == 3
    assert len(page["items"]) == 2
    ids = [s["id"] for s in page["items"]]
    assert ids == sorted(ids, reverse=True)

    pending = client.get("/api/dataset/samples", params={"status": "pending"}).json()
    assert [s["physical_sample_id"] for s in pending["items"]] == ["T-9"]


def test_export_writes_a_training_manifest(client: TestClient, control):
    refused = client.post("/api/dataset/export", json={"product_id": "tucuma"}, headers=control)
    assert refused.status_code == 409

    capture(client, control, piece="T-1", label="A")
    capture(client, control, piece="T-2", label="B")
    capture(client, control, piece="T-3", label=None)  # not labeled: stays out
    capture(client, control, piece="C-1", label="C", product="castanha")  # other product

    response = client.post("/api/dataset/export", json={"product_id": "tucuma"}, headers=control)
    assert response.status_code == 200, response.text
    result = response.json()
    assert result["photos"] == 2
    assert result["pieces"] == 2
    assert "treinar" in result["command"]

    manifest = Path(result["manifest_path"])
    samples = read_manifest(manifest)
    assert {(s.physical_sample_id, s.label.value) for s in samples} == {("T-1", "A"), ("T-2", "B")}
    for s in samples:
        assert (manifest.parent / s.path).is_file()


def test_camera_snapshot_is_a_jpeg(client: TestClient):
    response = client.get("/api/camera/snapshot")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    assert response.content.startswith(b"\xff\xd8")


def test_camera_snapshot_without_camera(client: TestClient):
    client.app.state.services.simulation.camera.available = False
    assert client.get("/api/camera/snapshot").status_code == 503
