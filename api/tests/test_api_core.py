import sqlite3
import uuid
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from amazonvision.config import RunMode, Settings
from amazonvision.core.clock import to_db, utc_now
from amazonvision.core.control import ControlManager
from amazonvision.main import create_app
from amazonvision.schemas.errors import ApiError


def new_lot(product_id: str = "tucuma", operator: str = "Ana", request_id: str | None = None):
    return {
        "request_id": request_id or str(uuid.uuid4()),
        "product_id": product_id,
        "operator": operator,
    }


# ---------------------------------------------------------------- status and products


def test_simulated_mode_reports_the_simulated_bench(client: TestClient):
    status = client.get("/api/status").json()
    assert status["mode"] == "simulado"
    assert status["machine"]["state"] == "DISARMED"
    assert status["machine"]["link"]["connected"] is True
    assert status["machine"]["link"]["port"] == "simulador"
    assert status["machine"]["running"] is False
    assert status["camera"]["status"] == "ok"
    assert status["camera"]["source"] == "simulada"
    assert status["model"]["status"] == "not_loaded"
    assert status["storage"]["status"] in {"ok", "low_space"}
    assert status["active_lot"] is None
    assert status["current_cycle"] is None
    assert status["control_locked"] is False
    assert status["control_holder"] is None


def test_real_mode_never_claims_absent_equipment(settings: Settings):
    with TestClient(create_app(settings.model_copy(update={"mode": RunMode.REAL}))) as client:
        status = client.get("/api/status").json()
    assert status["machine"]["state"] is None
    assert status["machine"]["link"]["connected"] is False
    assert status["camera"]["status"] == "unavailable"
    assert status["model"]["status"] == "not_loaded"


def test_products_lists_initial_profiles(client: TestClient):
    products = client.get("/api/products").json()
    assert {p["id"] for p in products} == {"tucuma", "castanha"}
    assert all(p["active_model_id"] is None for p in products)


# ---------------------------------------------------------------- control lock


def test_second_operator_is_locked_out_until_takeover(client: TestClient, control):
    locked = client.post("/api/control/claim", json={"operator": "Bruno"})
    assert locked.status_code == 423
    assert locked.json()["code"] == "CONTROL_LOCKED"
    assert "Ana" in locked.json()["message"]

    taken = client.post("/api/control/claim", json={"operator": "Bruno", "takeover": True})
    assert taken.status_code == 200
    assert client.get("/api/status").json()["control_holder"] == "Bruno"

    old = client.post("/api/lots", json=new_lot(), headers=control)
    assert old.status_code == 423


def test_same_token_renews_without_new_token(client: TestClient, control):
    renewed = client.post("/api/control/claim", json={"operator": "Ana"}, headers=control)
    assert renewed.status_code == 200
    assert renewed.json()["token"] == control["X-Control-Token"]


def test_release_frees_control(client: TestClient, control):
    assert client.post("/api/control/release", headers=control).status_code == 204
    assert client.get("/api/status").json()["control_locked"] is False
    assert client.post("/api/control/release", headers=control).status_code == 423


def test_control_expires_and_slides():
    now = [datetime(2026, 10, 18, 12, 0, tzinfo=UTC)]
    manager = ControlManager(ttl=timedelta(minutes=30), clock=lambda: now[0])
    grant, _, _ = manager.claim("Ana")
    now[0] += timedelta(minutes=20)
    manager.verify(grant.token)
    now[0] += timedelta(minutes=20)
    assert manager.holder == "Ana"
    now[0] += timedelta(minutes=11)
    assert manager.holder is None
    with pytest.raises(ApiError):
        manager.verify(grant.token)


# ---------------------------------------------------------------- lots


def test_lot_requires_control(client: TestClient):
    response = client.post("/api/lots", json=new_lot())
    assert response.status_code == 423


def test_create_lot_and_status_reflect_it(client: TestClient, control):
    response = client.post("/api/lots", json=new_lot(), headers=control)
    assert response.status_code == 201, response.text
    lot = response.json()
    assert lot["status"] == "open"
    assert lot["is_simulated"] is True
    assert lot["model_id"] is None

    status = client.get("/api/status").json()
    assert status["active_lot"]["id"] == lot["id"]
    summary = status["active_lot_summary"]
    assert summary["inspected"] == 0
    assert summary["approval_rate"] is None
    assert summary["approval_rate_denominator"] == 0
    assert summary["by_grade"] == {"A": 0, "B": 0, "C": 0}


def test_repeated_request_returns_same_lot(client: TestClient, control):
    body = new_lot()
    first = client.post("/api/lots", json=body, headers=control)
    again = client.post("/api/lots", json=body, headers=control)
    assert first.status_code == 201
    assert again.status_code == 200
    assert again.json()["id"] == first.json()["id"]


def test_reused_request_id_with_other_data_conflicts(client: TestClient, control):
    body = new_lot()
    client.post("/api/lots", json=body, headers=control)
    response = client.post("/api/lots", json={**body, "operator": "Outra"}, headers=control)
    assert response.status_code == 409
    assert response.json()["code"] == "CONFLICT"


def test_only_one_open_lot(client: TestClient, control):
    client.post("/api/lots", json=new_lot(), headers=control)
    response = client.post("/api/lots", json=new_lot("castanha"), headers=control)
    assert response.status_code == 409
    assert response.json()["recovery"]


@pytest.mark.parametrize(
    ("product", "status", "code"),
    [("acai", 404, "NOT_FOUND"), ("Tucumã!", 422, "VALIDATION_ERROR")],
)
def test_invalid_products(client: TestClient, control, product, status, code):
    response = client.post("/api/lots", json=new_lot(product), headers=control)
    assert response.status_code == status
    assert response.json()["code"] == code


def test_real_mode_requires_a_model(settings: Settings):
    with TestClient(create_app(settings.model_copy(update={"mode": RunMode.REAL}))) as client:
        token = client.post("/api/control/claim", json={"operator": "Ana"}).json()["token"]
        response = client.post("/api/lots", json=new_lot(), headers={"X-Control-Token": token})
    assert response.status_code == 503
    assert response.json()["code"] == "MODEL_NOT_READY"


def test_close_lot_is_idempotent_and_allows_next_lot(client: TestClient, control):
    lot = client.post("/api/lots", json=new_lot(), headers=control).json()
    closed = client.post(f"/api/lots/{lot['id']}/close", headers=control)
    assert closed.status_code == 200
    assert closed.json()["status"] == "closed"
    assert closed.json()["ended_at"] is not None
    again = client.post(f"/api/lots/{lot['id']}/close", headers=control)
    assert again.json() == closed.json()
    assert client.get("/api/status").json()["active_lot"] is None
    assert client.post("/api/lots", json=new_lot("castanha"), headers=control).status_code == 201


def test_cannot_close_lot_with_running_cycle(client: TestClient, control):
    lot = client.post("/api/lots", json=new_lot(), headers=control).json()
    services = client.app.state.services

    def start_cycle(conn: sqlite3.Connection) -> None:
        conn.execute(
            "INSERT INTO cycles (lot_id, seq_in_lot, started_at) VALUES (?, 1, ?)",
            (lot["id"], to_db(utc_now())),
        )

    client.portal.call(services.db.run, start_cycle)
    response = client.post(f"/api/lots/{lot['id']}/close", headers=control)
    assert response.status_code == 409
    assert response.json()["code"] == "INVALID_STATE"


def test_list_get_and_summary(client: TestClient, control):
    lot = client.post("/api/lots", json=new_lot(), headers=control).json()
    assert [x["id"] for x in client.get("/api/lots").json()] == [lot["id"]]
    assert client.get("/api/lots?product_id=castanha").json() == []
    assert client.get(f"/api/lots/{lot['id']}").json() == lot
    assert client.get(f"/api/lots/{lot['id']}/summary").json()["lot_id"] == lot["id"]
    assert client.get("/api/lots/999").json()["code"] == "NOT_FOUND"
    assert client.get("/api/lots/999/summary").status_code == 404


# ---------------------------------------------------------------- diagnostics


def test_operator_actions_are_recorded(client: TestClient, control):
    lot = client.post("/api/lots", json=new_lot(), headers=control).json()
    client.post(f"/api/lots/{lot['id']}/close", headers=control)
    client.post("/api/control/claim", json={"operator": "Bruno", "takeover": True})
    events = client.get("/api/diagnostics/events").json()
    assert [e["type"] for e in events if e["source"] == "operator"] == [
        "CONTROL_TAKEOVER",
        "LOT_CLOSED",
        "LOT_OPENED",
        "CONTROL_CLAIMED",
    ]
    assert events[-1]["type"] == "DEVICE_SESSION_OPENED"
    warnings = client.get("/api/diagnostics/events?severity=warning").json()
    assert [e["type"] for e in warnings] == ["CONTROL_TAKEOVER"]
    assert warnings[0]["data"] == {"operator": "Bruno", "previous": "Ana"}


# ---------------------------------------------------------------- storage failure


def test_storage_failure_is_sticky_and_reported(client: TestClient):
    services = client.app.state.services

    def broken(conn: sqlite3.Connection) -> None:
        raise sqlite3.OperationalError("disk I/O error")

    with pytest.raises(ApiError) as info:
        client.portal.call(services.db.run, broken)
    assert info.value.code == "STORAGE_ERROR"
    status = client.get("/api/status").json()
    assert status["storage"]["status"] == "error"


# ---------------------------------------------------------------- WebSocket


def test_ws_starts_with_snapshot_then_streams_lot_updates(client: TestClient, control):
    with client.websocket_connect("/api/events") as ws:
        snapshot = ws.receive_json()
        assert snapshot["type"] == "SNAPSHOT"
        assert snapshot["data"]["active_lot"] is None
        assert snapshot["data"]["control_holder"] == "Ana"

        lot = client.post("/api/lots", json=new_lot(), headers=control).json()
        event = ws.receive_json()
        assert event["type"] == "LOT_UPDATED"
        assert event["seq"] == snapshot["seq"] + 1
        assert event["state_version"] > snapshot["state_version"]
        assert event["lot_id"] == lot["id"]
        assert event["data"]["summary"]["inspected"] == 0


def test_ws_reconnect_gets_current_state(client: TestClient, control):
    lot = client.post("/api/lots", json=new_lot(), headers=control).json()
    with client.websocket_connect("/api/events") as ws:
        snapshot = ws.receive_json()
    assert snapshot["type"] == "SNAPSHOT"
    assert snapshot["data"]["active_lot"]["id"] == lot["id"]
    assert snapshot["seq"] == client.app.state.services.bus.seq


def test_ws_control_change_resyncs_everyone(client: TestClient):
    with client.websocket_connect("/api/events") as ws:
        first = ws.receive_json()
        client.post("/api/control/claim", json={"operator": "Carla"})
        resync = ws.receive_json()
    assert resync["type"] == "SNAPSHOT"
    assert resync["data"]["control_holder"] == "Carla"
    assert resync["state_version"] > first["state_version"]


def test_ws_rejects_foreign_origin(client: TestClient):
    with (
        pytest.raises(WebSocketDisconnect) as info,
        client.websocket_connect("/api/events", headers={"origin": "http://evil.example"}) as ws,
    ):
        ws.receive_json()
    assert info.value.code == 1008


def test_ws_accepts_local_origin(client: TestClient):
    with client.websocket_connect("/api/events", headers={"origin": "http://127.0.0.1:5173"}) as ws:
        assert ws.receive_json()["type"] == "SNAPSHOT"


def test_foreign_host_header_is_rejected(client: TestClient):
    response = client.get("/api/status", headers={"host": "evil.example"})
    assert response.status_code == 400
