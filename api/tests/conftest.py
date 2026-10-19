from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from amazonvision.config import Settings
from amazonvision.main import create_app

TEST_HOSTS = ["testserver", "127.0.0.1", "localhost"]


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(
        _env_file=None,
        data_dir=tmp_path / "data",
        web_dist=tmp_path / "no-dist",
        allowed_hosts=TEST_HOSTS,
        log_to_file=False,
    )


@pytest.fixture
def client(settings: Settings) -> Iterator[TestClient]:
    with TestClient(create_app(settings)) as test_client:
        yield test_client


@pytest.fixture
def control(client: TestClient) -> dict[str, str]:
    """Headers of an operator holding the control lock."""
    response = client.post("/api/control/claim", json={"operator": "Ana"})
    assert response.status_code == 200, response.text
    return {"X-Control-Token": response.json()["token"]}
