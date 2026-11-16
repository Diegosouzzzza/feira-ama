import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi import APIRouter
from fastapi.testclient import TestClient
from pydantic import TypeAdapter

from amazonvision.config import Settings
from amazonvision.main import create_app
from amazonvision.openapi import CONTRACT_INPUTS, CONTRACT_OUTPUTS
from amazonvision.schemas.api import LotCreate
from amazonvision.schemas.errors import HTTP_STATUS, ApiError, ErrorCode
from amazonvision.schemas.events import EventType, WsEvent


@pytest.fixture
def app(settings: Settings):
    app = create_app(settings)
    router = APIRouter()

    @router.get("/_test/api-error")
    def api_error():
        raise ApiError(ErrorCode.MODEL_NOT_READY, "Modelo não carregado.", "Selecione o produto.")

    @router.post("/_test/lots")
    def create_lot(body: LotCreate):
        return {"ok": True}

    @router.get("/_test/boom")
    def boom():
        raise RuntimeError("detalhe interno que não pode vazar")

    app.include_router(router, prefix="/api")
    return app


def test_every_error_code_has_http_status():
    assert set(HTTP_STATUS) == set(ErrorCode)


def test_api_error_uses_standard_body(app):
    with TestClient(app) as client:
        response = client.get("/api/_test/api-error")
    assert response.status_code == 503
    body = response.json()
    assert body["code"] == "MODEL_NOT_READY"
    assert body["message"] == "Modelo não carregado."
    assert body["recovery"] == "Selecione o produto."
    assert len(body["trace_id"]) == 12


def test_validation_error_uses_standard_body(app):
    with TestClient(app) as client:
        response = client.post("/api/_test/lots", json={"product_id": "TUCUMA!"})
    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"


def test_unknown_api_route_uses_standard_body(app):
    with TestClient(app) as client:
        response = client.get("/api/nao-existe")
    assert response.status_code == 404
    assert response.json()["code"] == "NOT_FOUND"


def test_unexpected_error_does_not_leak_details(app):
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/api/_test/boom")
    assert response.status_code == 500
    assert response.json()["code"] == "INTERNAL_ERROR"
    assert "detalhe interno" not in response.text


def test_openapi_publishes_every_contract_type(app):
    with TestClient(app) as client:
        schemas = client.get("/api/openapi.json").json()["components"]["schemas"]
    for name in [*CONTRACT_INPUTS, *CONTRACT_OUTPUTS]:
        assert name in schemas, name
    for event in EventType:
        assert any(
            event.value in str(s.get("properties", {}).get("type", {})) for s in schemas.values()
        )


def test_committed_openapi_file_is_current():
    committed = Path(__file__).resolve().parents[1] / "openapi.json"
    generated = create_app().openapi()
    assert json.loads(committed.read_text(encoding="utf-8")) == generated, (
        "openapi.json desatualizado: rode 'uv run amazonvision --dump-openapi openapi.json' "
        "e 'pnpm gen:api' no web/"
    )


def test_ws_events_are_discriminated_by_type():
    adapter = TypeAdapter(WsEvent)
    event = adapter.validate_python(
        {
            "type": "CONNECTION_LOST",
            "seq": 7,
            "at": datetime(2026, 10, 18, 15, 0, tzinfo=UTC),
            "state_version": 3,
            "data": {"component": "device", "message": "ESP32 sem resposta"},
        }
    )
    assert event.type is EventType.CONNECTION_LOST
    with pytest.raises(ValueError):
        adapter.validate_python({"type": "UNKNOWN", "seq": 1, "at": "2026-10-18T15:00:00Z"})


def test_ws_event_requires_timezone():
    with pytest.raises(ValueError):
        TypeAdapter(WsEvent).validate_python(
            {
                "type": "FAULT",
                "seq": 1,
                "at": "2026-10-18T15:00:00",
                "state_version": 0,
                "data": {"code": "S1_TIMEOUT", "message": "x"},
            }
        )
