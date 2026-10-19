"""History filters and CSV, product configuration and maintenance, over the simulated bench."""

import csv
import io
import time
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi.testclient import TestClient

from amazonvision.domain.quality import Grade
from amazonvision.services.inspection_csv import safe_cell
from amazonvision.simulation.scenario import confident, uncertain
from tests.test_cycle_simulated import (
    machine,
    open_lot,
    run_one,
    sim,
    status,
    wait_for,
)


def close_lot(client: TestClient, headers: dict[str, str], lot_id: int) -> None:
    assert client.post(f"/api/lots/{lot_id}/close", headers=headers).status_code == 200


def run_lot(client: TestClient, headers: dict[str, str], *items: Any) -> dict[str, Any]:
    lot = open_lot(client, headers)
    sim(client).scenario.push(*items)
    for _ in items:
        run_one(client, headers)
    return lot


# ---------------------------------------------------------------- history


def test_history_filters(bench: TestClient, operator):
    lot = run_lot(bench, operator, confident(Grade.A), confident(Grade.C))
    sim(bench).scenario.push(uncertain())
    assert machine(bench, operator, "start").status_code == 200
    wait_for(bench, lambda s: s["machine"]["state"] == "REVIEW_HOLD")

    def total(**params: Any) -> int:
        response = bench.get("/api/inspections", params=params)
        assert response.status_code == 200, response.text
        return response.json()["total"]

    assert total(lot_id=lot["id"]) == 3
    assert total(product_id="tucuma") == 3
    assert total(product_id="castanha") == 0
    assert total(grade="C") == 1
    assert total(outcome="approved") == 1
    assert total(outcome="rejected") == 1
    assert total(outcome="pending_review") == 1
    assert total(outcome="inconclusive") == 1
    assert total(outcome="reviewed") == 0

    now = datetime.now(UTC)
    assert total(**{"from": (now - timedelta(hours=1)).isoformat()}) == 3
    assert total(**{"from": (now + timedelta(hours=1)).isoformat()}) == 0
    wrong = bench.get(
        "/api/inspections",
        params={"from": now.isoformat(), "to": (now - timedelta(minutes=1)).isoformat()},
    )
    assert wrong.status_code == 422


def test_csv_export(bench: TestClient, operator):
    run_lot(bench, operator, confident(Grade.A), confident(Grade.B))

    response = bench.get("/api/exports/inspections.csv", params={"grade": "B"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "attachment" in response.headers["content-disposition"]
    assert response.content.startswith("﻿".encode())

    rows = list(csv.reader(io.StringIO(response.content.decode("utf-8-sig")), delimiter=";"))
    header, *data = rows
    assert header[0] == "inspecao"
    assert len(data) == 1
    row = dict(zip(header, data[0], strict=True))
    assert row["classe_prevista"] == "B"
    assert row["decisao_final"] == "Rejeitado"
    assert row["confianca"] == "0,920"
    assert len(row["imagem_sha256"]) == 64


def test_csv_cells_never_become_formulas():
    assert safe_cell("=HYPERLINK(1)") == "'=HYPERLINK(1)"
    assert safe_cell("+1") == "'+1"
    assert safe_cell("@SUM") == "'@SUM"
    assert safe_cell("tucuma-20261019") == "tucuma-20261019"


# ---------------------------------------------------------------- product configuration


def config(client: TestClient, product: str = "tucuma") -> dict[str, Any]:
    response = client.get(f"/api/products/{product}/config")
    assert response.status_code == 200, response.text
    return response.json()


def update(
    client: TestClient, headers: dict[str, str], current: dict[str, Any], **changes: Any
) -> Any:
    bench_config = {**current["bench"], **changes.pop("bench", {})}
    body = {
        "expected_version": current["product"]["version"],
        "presentation": current["product"]["presentation"],
        "decision_threshold": current["product"]["decision_threshold"],
        "bench": bench_config,
        **changes,
    }
    return client.put(
        f"/api/products/{current['product']['id']}/config", json=body, headers=headers
    )


def test_config_defaults_to_simulated_bench(bench: TestClient):
    current = config(bench)
    assert current["bench_is_default"] is True
    assert current["bench"]["settle_ms"] > 0
    assert current["editable"] is True
    assert bench.get("/api/products/acai/config").status_code == 404


def test_config_update_applies_to_next_lot_and_is_logged(bench: TestClient, operator):
    current = config(bench)
    response = update(bench, operator, current, decision_threshold=0.9, bench={"settle_ms": 650})
    assert response.status_code == 200, response.text
    saved = response.json()
    assert saved["product"]["version"] == current["product"]["version"] + 1
    assert saved["product"]["decision_threshold"] == 0.9
    assert saved["bench"]["settle_ms"] == 650
    assert saved["bench_is_default"] is False

    [event] = [
        e for e in bench.get("/api/diagnostics/events", params={"type": "CONFIG_CHANGED"}).json()
    ]
    assert event["data"]["changes"]["settle_ms"] == {"de": 400, "para": 650}
    assert event["data"]["operator"] == "Ana"

    lot = open_lot(bench, operator)
    assert status(bench)["active_lot"]["id"] == lot["id"]
    sim(bench).scenario.push(confident(Grade.A, confidence=0.85))  # below the new 0.90
    assert machine(bench, operator, "start").status_code == 200
    final = wait_for(bench, lambda s: s["machine"]["state"] == "REVIEW_HOLD")
    assert final["active_lot_summary"]["review_pending"] == 1


def test_config_refused_with_stale_version_or_bad_values(bench: TestClient, operator):
    current = config(bench)
    assert update(bench, operator, current, bench={"settle_ms": 500}).status_code == 200

    stale = update(bench, operator, current, bench={"settle_ms": 700})
    assert stale.status_code == 409
    assert stale.json()["code"] == "CONFLICT"

    fresh = config(bench)
    same_angles = update(bench, operator, fresh, bench={"servo_reject_deg": 10})
    assert same_angles.status_code == 422
    assert update(bench, operator, fresh, decision_threshold=0.2).status_code == 422
    assert update(bench, {}, fresh).status_code == 423


def test_config_locked_while_a_lot_of_the_product_is_open(bench: TestClient, operator):
    lot = open_lot(bench, operator)
    current = config(bench)
    assert current["editable"] is False
    assert "lote aberto" in current["locked_reason"]
    refused = update(bench, operator, current, bench={"settle_ms": 500})
    assert refused.status_code == 409
    assert refused.json()["code"] == "INVALID_STATE"

    assert config(bench, "castanha")["editable"] is True
    close_lot(bench, operator, lot["id"])
    assert config(bench)["editable"] is True


# ---------------------------------------------------------------- maintenance


def wait_device(client: TestClient, predicate, timeout: float = 3.0) -> None:
    device = sim(client).device
    assert device is not None
    deadline = time.monotonic() + timeout
    while not predicate(device):
        assert time.monotonic() < deadline, "a placa simulada não reagiu"
        time.sleep(0.01)


def test_maintenance_runs_manual_tests(bench: TestClient, operator):
    assert machine(bench, operator, "maintenance/test-motor", run_ms=500).status_code == 409

    entered = machine(bench, operator, "maintenance/enter")
    assert entered.status_code == 200, entered.text
    assert entered.json()["state"] == "MAINTENANCE"
    assert status(bench)["machine"]["state"] == "MAINTENANCE"

    assert machine(bench, operator, "maintenance/test-motor", run_ms=2000).status_code == 200
    wait_device(bench, lambda d: d.motor_on)
    servo = machine(bench, operator, "maintenance/test-servo", angle_deg=80, hold_ms=2000)
    assert servo.status_code == 200
    wait_device(bench, lambda d: d.servo_deg == 80)

    assert (
        machine(bench, operator, "maintenance/test-servo", angle_deg=200, hold_ms=0).status_code
        == 422
    )

    exited = machine(bench, operator, "maintenance/exit")
    assert exited.json()["state"] == "DISARMED"
    types = {e["type"] for e in bench.get("/api/diagnostics/events?limit=200").json()}
    assert {"MAINTENANCE_ENTER", "TEST_MOTOR", "TEST_SERVO", "MAINTENANCE_EXIT"} <= types


def test_maintenance_refused_while_running(bench: TestClient, operator):
    open_lot(bench, operator)
    sim(bench).scenario.push(*(confident(Grade.A) for _ in range(20)))
    assert machine(bench, operator, "start").status_code == 200
    wait_for(bench, lambda s: s["machine"]["running"])
    refused = machine(bench, operator, "maintenance/enter")
    assert refused.status_code == 409
    assert refused.json()["code"] == "INVALID_STATE"
    assert machine(bench, operator, "stop").status_code == 200


def test_maintenance_from_ready_disarms_first(bench: TestClient, operator):
    open_lot(bench, operator)
    sim(bench).scenario.push(confident(Grade.A))
    assert run_one(bench, operator)["machine"]["state"] == "READY"
    assert machine(bench, operator, "maintenance/enter").json()["state"] == "MAINTENANCE"
    request_id = str(uuid.uuid4())
    body = {"request_id": request_id}
    first = bench.post("/api/machine/maintenance/exit", json=body, headers=operator).json()
    again = bench.post("/api/machine/maintenance/exit", json=body, headers=operator).json()
    assert again["duplicate"] is True
    assert again["state"] == first["state"] == "DISARMED"
