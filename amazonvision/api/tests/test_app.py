from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from amazonvision.config import Settings
from amazonvision.main import create_app


@pytest.fixture
def make_client(settings: Settings):
    def _make(web_dist: Path | None = None) -> TestClient:
        update = {"web_dist": web_dist} if web_dist else {}
        return TestClient(create_app(settings.model_copy(update=update)))

    return _make


def test_health_reports_version_and_mode(make_client):
    with make_client() as client:
        response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0", "mode": "simulado"}


def test_startup_creates_data_dirs(make_client, tmp_path: Path):
    with make_client():
        pass
    for name in ("db", "images", "models", "logs", "backups", "dataset"):
        assert (tmp_path / "data" / name).is_dir()


def test_unknown_api_route_is_404_not_spa(make_client, tmp_path: Path):
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("<html>spa</html>", encoding="utf-8")
    with make_client(dist) as client:
        assert client.get("/api/nao-existe").status_code == 404


def test_spa_fallback_serves_index_for_client_routes(make_client, tmp_path: Path):
    dist = tmp_path / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "index.html").write_text("<html>spa</html>", encoding="utf-8")
    (dist / "assets" / "app.js").write_text("console.log(1)", encoding="utf-8")
    with make_client(dist) as client:
        assert client.get("/historico").text == "<html>spa</html>"
        assert client.get("/assets/app.js").text == "console.log(1)"


def test_spa_does_not_serve_files_outside_dist(make_client, tmp_path: Path):
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("<html>spa</html>", encoding="utf-8")
    (tmp_path / "secret.txt").write_text("segredo", encoding="utf-8")
    with make_client(dist) as client:
        response = client.get("/..%2Fsecret.txt")
    assert "segredo" not in response.text


def test_missing_build_returns_503_page(make_client):
    with make_client() as client:
        response = client.get("/")
    assert response.status_code == 503
    assert "Interface não compilada" in response.text
