import uuid

from fastapi.testclient import TestClient


def test_opening_and_closing_a_lot_resyncs_model_status(client: TestClient, control):
    with client.websocket_connect("/api/events") as ws:
        assert ws.receive_json()["data"]["model"]["status"] == "not_loaded"
        body = {"request_id": str(uuid.uuid4()), "product_id": "tucuma", "operator": "Ana"}
        lot = client.post("/api/lots", json=body, headers=control).json()
        received = [ws.receive_json() for _ in range(2)]
        snapshot = next(m for m in received if m["type"] == "SNAPSHOT")
        assert snapshot["data"]["model"]["status"] == "ready"
        assert snapshot["data"]["model"]["product_id"] == "tucuma"

        client.post(f"/api/lots/{lot['id']}/close", headers=control)
        received = [ws.receive_json() for _ in range(2)]
        snapshot = next(m for m in received if m["type"] == "SNAPSHOT")
        assert snapshot["data"]["model"]["status"] == "not_loaded"
        assert snapshot["data"]["active_lot"] is None
