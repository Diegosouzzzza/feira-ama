import io
import time
import uuid
from pathlib import Path

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from amazonvision.config import RunMode, Settings
from amazonvision.domain.quality import Grade
from amazonvision.main import create_app
from amazonvision.simulation.images import render
from amazonvision.simulation.scenario import confident
from amazonvision.vision.onnx_classifier import OnnxClassifier
from amazonvision.vision.package import PackageError, load_package
from amazonvision.vision.preprocess import PreprocessSpec, letterbox, prepare_bytes
from tests.model_factory import build_package

# ---------------------------------------------------------------- preprocessing and package


def test_letterbox_keeps_the_whole_frame():
    wide = Image.new("RGB", (400, 100), (255, 0, 0))
    boxed = letterbox(wide, PreprocessSpec(input_size=224))
    assert boxed.size == (224, 224)
    top, middle = boxed.getpixel((112, 2)), boxed.getpixel((112, 112))
    assert top == PreprocessSpec().pad_rgb  # padded, not cropped
    assert middle[0] > 200  # the red image is fully inside


def test_prepare_bytes_shape_and_normalisation():
    buffer = io.BytesIO()
    Image.new("RGB", (64, 48), (124, 116, 104)).save(buffer, format="PNG")
    array = prepare_bytes(buffer.getvalue(), PreprocessSpec())
    assert array.shape == (3, 224, 224)
    assert array.dtype == np.float32
    assert abs(float(array.mean())) < 0.05  # mean colour ~ 0 after normalisation


def test_package_detects_tampered_weights(tmp_path: Path):
    folder = build_package(tmp_path)
    load_package(folder)
    with open(folder / "model.onnx", "ab") as handle:
        handle.write(b"x")
    with pytest.raises(PackageError, match="não conferem"):
        load_package(folder)


def test_onnx_classifier_returns_probabilities_in_class_order(tmp_path: Path):
    classifier = OnnxClassifier(load_package(build_package(tmp_path)))
    bright = classifier.classify_array(prepare_bytes(render("A", 0), PreprocessSpec()))
    dark = classifier.classify_array(prepare_bytes(render("C", 0), PreprocessSpec()))
    assert set(bright) == set(Grade)
    assert sum(bright.values()) == pytest.approx(1.0)
    assert sum(dark.values()) == pytest.approx(1.0)
    assert bright != pytest.approx(dark)


# ---------------------------------------------------------------- API


@pytest.fixture
def operator(client: TestClient) -> dict[str, str]:
    token = client.post("/api/control/claim", json={"operator": "Ana"}).json()["token"]
    return {"X-Control-Token": token}


def install(client: TestClient, headers, folder: Path):
    return client.post("/api/models/install", json={"path": str(folder)}, headers=headers)


def test_install_is_idempotent_and_starts_pending(client: TestClient, operator, tmp_path: Path):
    folder = build_package(tmp_path / "pkgs")
    first = install(client, operator, folder)
    assert first.status_code == 201, first.text
    model = first.json()
    assert model["validation_status"] == "pending"
    assert model["active"] is False
    assert model["recommended_threshold"] == 0.6
    assert install(client, operator, folder).status_code == 200
    assert [m["id"] for m in client.get("/api/models?product_id=tucuma").json()] == [model["id"]]
    assert client.get(f"/api/models/{model['id']}/report").text.startswith("# Relatório")


def test_install_rejects_invalid_package(client: TestClient, operator, tmp_path: Path):
    response = install(client, operator, tmp_path / "nao-existe")
    assert response.status_code == 422
    assert "Pacote inválido" in response.json()["message"]


def test_activate_sets_threshold_and_lot_uses_onnx_model(client: TestClient, operator, tmp_path):
    model = install(client, operator, build_package(tmp_path / "pkgs")).json()
    activated = client.post(f"/api/models/{model['id']}/activate", headers=operator)
    assert activated.status_code == 200
    assert activated.json()["active"] is True
    product = next(p for p in client.get("/api/products").json() if p["id"] == "tucuma")
    assert product["active_model_id"] == model["id"]
    assert product["decision_threshold"] == 0.6

    body = {"request_id": str(uuid.uuid4()), "product_id": "tucuma", "operator": "Ana"}
    lot = client.post("/api/lots", json=body, headers=operator).json()
    assert lot["model_id"] == model["id"]
    status = client.get("/api/status").json()
    assert status["model"] == {"status": "ready", "model_id": model["id"], "product_id": "tucuma"}

    blocked = client.post(f"/api/models/{model['id']}/activate", headers=operator)
    assert blocked.status_code == 409
    assert blocked.json()["code"] == "INVALID_STATE"


def test_cycle_runs_through_the_onnx_model(settings: Settings, tmp_path: Path):
    fast = settings.model_copy(update={"sim_speed": 50.0})
    with TestClient(create_app(fast)) as client:
        headers = {
            "X-Control-Token": client.post("/api/control/claim", json={"operator": "Ana"}).json()[
                "token"
            ]
        }
        model = install(client, headers, build_package(tmp_path / "pkgs", threshold=0.4)).json()
        client.post(f"/api/models/{model['id']}/activate", headers=headers)
        body = {"request_id": str(uuid.uuid4()), "product_id": "tucuma", "operator": "Ana"}
        lot = client.post("/api/lots", json=body, headers=headers).json()
        client.app.state.services.simulation.scenario.push(*[confident(Grade.A)] * 4)
        client.post("/api/machine/start", json={"request_id": str(uuid.uuid4())}, headers=headers)
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            page = client.get(f"/api/inspections?lot_id={lot['id']}").json()
            if page["total"] >= 1:
                break
            time.sleep(0.05)
        client.post("/api/machine/pause", json={"request_id": str(uuid.uuid4())}, headers=headers)
        inspection = page["items"][-1]
        assert inspection["model_id"] == model["id"]
        assert set(inspection["scores"]) == {"A", "B", "C"}
        # Scores come from the ONNX graph, not from the simulator's plan (0.92 for "A").
        assert inspection["scores"]["A"] != pytest.approx(0.92)


def test_real_mode_requires_validation_before_activation(settings: Settings, tmp_path: Path):
    with TestClient(create_app(settings.model_copy(update={"mode": RunMode.REAL}))) as client:
        headers = {
            "X-Control-Token": client.post("/api/control/claim", json={"operator": "Ana"}).json()[
                "token"
            ]
        }
        model = install(client, headers, build_package(tmp_path / "pkgs")).json()
        refused = client.post(f"/api/models/{model['id']}/activate", headers=headers)
        assert refused.status_code == 409
        validated = client.post(
            f"/api/models/{model['id']}/validation",
            json={"status": "validated", "reviewer": "Professora"},
            headers=headers,
        )
        assert validated.json()["validation_status"] == "validated"
        assert validated.json()["validated_by"] == "Professora"
        assert (
            client.post(f"/api/models/{model['id']}/activate", headers=headers).status_code == 200
        )


def test_corrupted_model_is_reported_not_used(client: TestClient, operator, tmp_path: Path):
    model = install(client, operator, build_package(tmp_path / "pkgs")).json()
    client.post(f"/api/models/{model['id']}/activate", headers=operator)
    installed = client.app.state.services.settings.data_root / "models" / model["id"] / "model.onnx"
    with open(installed, "ab") as handle:
        handle.write(b"corrompido")
    body = {"request_id": str(uuid.uuid4()), "product_id": "tucuma", "operator": "Ana"}
    client.post("/api/lots", json=body, headers=operator)
    status = client.get("/api/status").json()
    assert status["model"]["status"] == "error"
    start = client.post(
        "/api/machine/start", json={"request_id": str(uuid.uuid4())}, headers=operator
    )
    assert start.json()["code"] == "MODEL_NOT_READY"
