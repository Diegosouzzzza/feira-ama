"""End-to-end cycles through the HTTP API against the simulated bench (accelerated 50x)."""

import time
import uuid
from collections.abc import Callable, Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from amazonvision.config import Settings
from amazonvision.domain.quality import Grade
from amazonvision.main import create_app
from amazonvision.services.container import Simulation
from amazonvision.simulation.scenario import confident, invalid_image, uncertain


@pytest.fixture
def bench(settings: Settings) -> Iterator[TestClient]:
    fast = settings.model_copy(update={"sim_speed": 50.0, "device_silence_ms": 800})
    with TestClient(create_app(fast)) as client:
        yield client


@pytest.fixture
def operator(bench: TestClient) -> dict[str, str]:
    token = bench.post("/api/control/claim", json={"operator": "Ana"}).json()["token"]
    return {"X-Control-Token": token}


def sim(client: TestClient) -> Simulation:
    simulation = client.app.state.services.simulation
    assert simulation is not None
    return simulation


def status(client: TestClient) -> dict[str, Any]:
    return client.get("/api/status").json()


def wait_for(
    client: TestClient, predicate: Callable[[dict[str, Any]], bool], timeout: float = 6.0
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    current = status(client)
    while not predicate(current):
        if time.monotonic() > deadline:
            raise AssertionError(f"condição não atingida; último status: {current}")
        time.sleep(0.02)
        current = status(client)
    return current


def idle(s: dict[str, Any]) -> bool:
    return not s["machine"]["running"] and s["current_cycle"] is None


def machine(client: TestClient, headers: dict[str, str], action: str, **extra: Any):
    body = {"request_id": str(uuid.uuid4()), **extra}
    return client.post(f"/api/machine/{action}", json=body, headers=headers)


def open_lot(client: TestClient, headers: dict[str, str], product: str = "tucuma") -> dict:
    body = {"request_id": str(uuid.uuid4()), "product_id": product, "operator": "Ana"}
    response = client.post("/api/lots", json=body, headers=headers)
    assert response.status_code == 201, response.text
    return response.json()


def run_one(client: TestClient, headers: dict[str, str]) -> dict[str, Any]:
    """Start, let exactly one cycle begin, pause, and wait until the bench is idle."""
    assert machine(client, headers, "start").status_code == 200
    wait_for(client, lambda s: s["current_cycle"] is not None)
    assert machine(client, headers, "pause").status_code == 200
    return wait_for(client, idle)


def inspections_of(client: TestClient, lot_id: int) -> list[dict[str, Any]]:
    services = client.app.state.services
    rows = client.portal.call(
        services.db.run,
        lambda conn: conn.execute(
            "SELECT i.id FROM inspections i JOIN cycles c ON c.id = i.cycle_id "
            "WHERE c.lot_id = ? ORDER BY i.id",
            (lot_id,),
        ).fetchall(),
    )
    return [client.get(f"/api/inspections/{r[0]}").json() for r in rows]


# ---------------------------------------------------------------- happy paths


def test_approved_cycle_end_to_end(bench: TestClient, operator):
    lot = open_lot(bench, operator)
    assert status(bench)["model"]["status"] == "ready"
    sim(bench).scenario.push(confident(Grade.A))

    final = run_one(bench, operator)

    summary = final["active_lot_summary"]
    assert summary["cycles_completed"] == 1
    assert summary["approved"] == 1
    assert summary["by_grade"]["A"] == 1
    assert final["machine"]["state"] == "READY"

    [inspection] = inspections_of(bench, lot["id"])
    assert inspection["predicted_grade"] == "A"
    assert inspection["auto_decision"] == "APPROVED"
    assert inspection["final_decision"] == "APPROVED"
    assert inspection["decided_by"] == "auto"
    assert inspection["cycle_status"] == "completed"
    assert inspection["confidence"] == pytest.approx(0.92)

    image = bench.get(inspection["image_url"])
    assert image.status_code == 200
    assert image.headers["content-type"] == "image/png"
    assert image.content.startswith(b"\x89PNG")

    events = [e["type"] for e in bench.get("/api/diagnostics/events?limit=200").json()]
    for expected in ("CAPTURE_READY", "CYCLE_COMPLETED", "MACHINE_START", "MACHINE_PAUSE"):
        assert expected in events


@pytest.mark.parametrize("grade", [Grade.B, Grade.C])
def test_defective_and_reject_grades_go_to_rejected(bench: TestClient, operator, grade):
    lot = open_lot(bench, operator)
    sim(bench).scenario.push(confident(grade))
    final = run_one(bench, operator)
    assert final["active_lot_summary"]["rejected"] == 1
    assert final["active_lot_summary"]["by_grade"][grade.value] == 1
    [inspection] = inspections_of(bench, lot["id"])
    assert inspection["final_decision"] == "REJECTED"


# ---------------------------------------------------------------- inconclusive review


def test_inconclusive_waits_for_operator_then_moves(bench: TestClient, operator):
    lot = open_lot(bench, operator)
    sim(bench).scenario.push(uncertain(Grade.A))
    assert machine(bench, operator, "start").status_code == 200
    waiting = wait_for(bench, lambda s: s["machine"]["pending_review_inspection_id"] is not None)
    machine(bench, operator, "pause")
    waiting = wait_for(bench, lambda s: s["machine"]["state"] == "REVIEW_HOLD")
    inspection_id = waiting["machine"]["pending_review_inspection_id"]

    blocked = machine(bench, operator, "start")
    assert blocked.status_code == 409
    assert blocked.json()["code"] == "REVIEW_REQUIRED"

    review = {
        "request_id": str(uuid.uuid4()),
        "decision": "REJECTED",
        "reviewer": "Ana",
        "reason": "mancha escura visível",
    }
    created = bench.post(f"/api/inspections/{inspection_id}/review", json=review, headers=operator)
    assert created.status_code == 201, created.text
    assert created.json()["previous_decision"] is None
    again = bench.post(f"/api/inspections/{inspection_id}/review", json=review, headers=operator)
    assert again.status_code == 200
    assert again.json()["id"] == created.json()["id"]

    final = wait_for(bench, idle)
    assert final["active_lot_summary"]["rejected"] == 1
    assert final["active_lot_summary"]["review_pending"] == 0
    assert final["active_lot_summary"]["reviewed"] == 1
    [inspection] = inspections_of(bench, lot["id"])
    assert inspection["auto_decision"] == "REVIEW"
    assert inspection["review_reason"] == "LOW_CONFIDENCE"
    assert inspection["predicted_grade"] == "A"
    assert inspection["final_decision"] == "REJECTED"
    assert inspection["decided_by"] == "operator"
    assert inspection["cycle_status"] == "completed"


def test_invalid_image_is_inconclusive_without_prediction(bench: TestClient, operator):
    open_lot(bench, operator)
    sim(bench).scenario.push(invalid_image())
    machine(bench, operator, "start")
    s = wait_for(bench, lambda s: s["machine"]["pending_review_inspection_id"] is not None)
    inspection = bench.get(
        f"/api/inspections/{s['machine']['pending_review_inspection_id']}"
    ).json()
    assert inspection["review_reason"] == "INVALID_IMAGE"
    assert inspection["predicted_grade"] is None
    assert inspection["scores"] is None


def test_correction_after_the_fact_keeps_prediction(bench: TestClient, operator):
    lot = open_lot(bench, operator)
    sim(bench).scenario.push(confident(Grade.A))
    run_one(bench, operator)
    [inspection] = inspections_of(bench, lot["id"])
    review = {
        "request_id": str(uuid.uuid4()),
        "decision": "REJECTED",
        "reviewer": "Bruno",
        "reason": "rachadura na lateral",
    }
    response = bench.post(
        f"/api/inspections/{inspection['id']}/review", json=review, headers=operator
    )
    assert response.status_code == 201
    assert response.json()["previous_decision"] == "APPROVED"
    summary = status(bench)["active_lot_summary"]
    assert (summary["approved"], summary["rejected"]) == (0, 1)
    [after] = inspections_of(bench, lot["id"])
    assert after["auto_decision"] == "APPROVED"
    assert after["predicted_grade"] == "A"
    assert after["final_decision"] == "REJECTED"


# ---------------------------------------------------------------- operator commands


def test_start_requires_open_lot(bench: TestClient, operator):
    response = machine(bench, operator, "start")
    assert response.status_code == 409
    assert response.json()["code"] == "INVALID_STATE"


def test_commands_require_control(bench: TestClient):
    assert machine(bench, {}, "start").status_code == 423


def test_command_request_id_is_idempotent(bench: TestClient, operator):
    open_lot(bench, operator)
    sim(bench).scenario.push(*[confident(Grade.A)] * 5)
    body = {"request_id": str(uuid.uuid4())}
    first = bench.post("/api/machine/start", json=body, headers=operator).json()
    second = bench.post("/api/machine/start", json=body, headers=operator).json()
    assert first["duplicate"] is False
    assert second["duplicate"] is True
    machine(bench, operator, "pause")
    wait_for(bench, idle)


def test_expected_state_mismatch_is_refused(bench: TestClient, operator):
    open_lot(bench, operator)
    response = machine(bench, operator, "start", expected_state="READY")
    assert response.status_code == 409
    assert response.json()["code"] == "INVALID_STATE"


def test_pause_finishes_current_cycle_only(bench: TestClient, operator):
    open_lot(bench, operator)
    sim(bench).scenario.push(*[confident(Grade.A)] * 10)
    final = run_one(bench, operator)
    time.sleep(0.3)
    later = status(bench)
    assert (
        later["active_lot_summary"]["cycles_completed"]
        == final["active_lot_summary"]["cycles_completed"]
    )
    assert later["current_cycle"] is None


def test_stop_aborts_cycle(bench: TestClient, operator):
    open_lot(bench, operator)
    sim(bench).scenario.push(uncertain())
    machine(bench, operator, "start")
    wait_for(bench, lambda s: s["machine"]["state"] == "REVIEW_HOLD")
    assert machine(bench, operator, "stop").json()["state"] == "DISARMED"
    final = wait_for(bench, idle)
    assert final["active_lot_summary"]["cycles_aborted"] == 1
    assert final["machine"]["state"] == "DISARMED"


def test_lot_cannot_close_while_running(bench: TestClient, operator):
    lot = open_lot(bench, operator)
    sim(bench).scenario.push(*[confident(Grade.A)] * 5)
    machine(bench, operator, "start")
    response = bench.post(f"/api/lots/{lot['id']}/close", headers=operator)
    assert response.status_code == 409
    machine(bench, operator, "pause")
    wait_for(bench, idle)
    assert bench.post(f"/api/lots/{lot['id']}/close", headers=operator).status_code == 200
    assert status(bench)["model"]["status"] == "not_loaded"


# ---------------------------------------------------------------- faults


def test_missing_s1_faults_then_rearm_without_motion(bench: TestClient, operator):
    open_lot(bench, operator)
    sim(bench).device.faults.s1_missing = True
    machine(bench, operator, "start")
    faulted = wait_for(bench, lambda s: s["machine"]["state"] == "FAULT")
    assert faulted["machine"]["fault"] == "S1_TIMEOUT"
    final = wait_for(bench, idle)
    assert final["active_lot_summary"]["cycles_aborted"] == 1

    assert machine(bench, operator, "start").status_code == 409
    sim(bench).device.faults.s1_missing = False
    rearmed = machine(bench, operator, "rearm")
    assert rearmed.status_code == 200
    assert rearmed.json()["state"] == "READY"
    time.sleep(0.2)
    assert status(bench)["machine"]["running"] is False
    assert status(bench)["current_cycle"] is None


def test_camera_failure_stops_the_bench(bench: TestClient, operator):
    lot = open_lot(bench, operator)
    sim(bench).camera.fail_next_capture = True
    machine(bench, operator, "start")
    final = wait_for(bench, lambda s: idle(s) and s["active_lot_summary"]["cycles_aborted"] == 1)
    assert final["machine"]["state"] == "DISARMED"
    assert inspections_of(bench, lot["id"]) == []
    events = bench.get("/api/diagnostics/events?severity=error").json()
    assert events[0]["type"] == "CAMERA_UNAVAILABLE"


def test_estop_aborts_and_blocks_until_released(bench: TestClient, operator):
    open_lot(bench, operator)
    sim(bench).scenario.push(uncertain())
    machine(bench, operator, "start")
    wait_for(bench, lambda s: s["machine"]["state"] == "REVIEW_HOLD")
    bench.portal.call(_call, sim(bench).device.press_estop)
    estop = wait_for(bench, lambda s: s["machine"]["state"] == "ESTOP" and idle(s))
    assert estop["machine"]["sensors"]["estop"] is True
    assert machine(bench, operator, "rearm").status_code == 409
    bench.portal.call(_call, sim(bench).device.remove_items)
    bench.portal.call(_call, sim(bench).device.release_estop)
    wait_for(bench, lambda s: s["machine"]["state"] == "DISARMED")
    assert machine(bench, operator, "rearm").json()["state"] == "READY"


def test_device_reboot_mid_cycle_never_replays_decision(bench: TestClient, operator):
    lot = open_lot(bench, operator)
    sim(bench).scenario.push(uncertain())
    machine(bench, operator, "start")
    waiting = wait_for(bench, lambda s: s["machine"]["state"] == "REVIEW_HOLD")
    old_boot = waiting["machine"]["link"]["boot_id"]
    inspection_id = waiting["machine"]["pending_review_inspection_id"]

    bench.portal.call(_call, sim(bench).device.reboot)
    after = wait_for(
        bench,
        lambda s: (
            s["machine"]["link"]["boot_id"] not in (None, old_boot)
            and s["machine"]["state"] == "DISARMED"
            and idle(s)
        ),
    )
    assert after["active_lot_summary"]["cycles_aborted"] == 1

    review = {
        "request_id": str(uuid.uuid4()),
        "decision": "APPROVED",
        "reviewer": "Ana",
        "reason": "conferido manualmente",
    }
    assert (
        bench.post(
            f"/api/inspections/{inspection_id}/review", json=review, headers=operator
        ).status_code
        == 201
    )
    events = bench.get("/api/diagnostics/events?limit=200").json()
    recorded = next(e for e in events if e["type"] == "REVIEW_RECORDED")
    assert recorded["data"]["delivered_to_machine"] is False
    assert sim(bench).device.state.value == "DISARMED"

    # The piece is still physically on S1: arming must be refused until it is removed.
    refused = machine(bench, operator, "rearm")
    assert refused.status_code == 409
    assert "sensor" in refused.json()["message"]
    bench.portal.call(_call, sim(bench).device.remove_items)
    assert machine(bench, operator, "rearm").json()["state"] == "READY"
    [inspection] = inspections_of(bench, lot["id"])
    assert inspection["cycle_status"] == "aborted"


def test_silent_device_is_reported_and_blocks_commands(bench: TestClient, operator):
    open_lot(bench, operator)
    sim(bench).device.faults.silent = True
    lost = wait_for(bench, lambda s: s["machine"]["link"]["connected"] is False)
    assert lost["machine"]["running"] is False
    response = machine(bench, operator, "start")
    assert response.status_code == 503
    assert response.json()["code"] == "SERIAL_DISCONNECTED"
    sim(bench).device.faults.silent = False
    wait_for(bench, lambda s: s["machine"]["link"]["connected"] is True)


def test_duplicated_device_events_do_not_double_count(bench: TestClient, operator):
    lot = open_lot(bench, operator)
    sim(bench).device.faults.duplicate_events = True
    sim(bench).scenario.push(confident(Grade.A), confident(Grade.B))
    machine(bench, operator, "start")
    wait_for(bench, lambda s: s["active_lot_summary"]["cycles_completed"] >= 2)
    machine(bench, operator, "pause")
    final = wait_for(bench, idle)
    completed = final["active_lot_summary"]["cycles_completed"]
    services = bench.app.state.services
    stored = bench.portal.call(
        services.db.run,
        lambda conn: conn.execute(
            "SELECT COUNT(*) FROM events WHERE type = 'CYCLE_COMPLETED' AND lot_id = ?",
            (lot["id"],),
        ).fetchone()[0],
    )
    assert stored == completed
    assert final["active_lot_summary"]["inspected"] == completed


# ---------------------------------------------------------------- endurance


def test_hundred_cycles_stay_consistent(settings: Settings):
    fast = settings.model_copy(update={"sim_speed": 400.0})
    with TestClient(create_app(fast)) as client:
        headers = {
            "X-Control-Token": client.post("/api/control/claim", json={"operator": "Ana"}).json()[
                "token"
            ]
        }
        lot = open_lot(client, headers, "castanha")
        plan = [confident([Grade.A, Grade.A, Grade.B, Grade.A, Grade.C][i % 5]) for i in range(110)]
        sim(client).scenario.push(*plan)
        machine(client, headers, "start")
        wait_for(client, lambda s: s["active_lot_summary"]["cycles_completed"] >= 100, timeout=90)
        machine(client, headers, "pause")
        final = wait_for(client, idle, timeout=10)

        summary = final["active_lot_summary"]
        n = summary["cycles_completed"]
        # Cycles keep finishing while the pause request travels; all stay within the plan.
        assert 100 <= n <= len(plan)
        assert summary["cycles_aborted"] == 0
        assert summary["inspected"] == n
        assert summary["approved"] + summary["rejected"] == n
        expected = {g.value: sum(1 for p in plan[:n] if p.label == g.value) for g in Grade}
        assert summary["by_grade"] == expected

        services = client.app.state.services
        mismatches = client.portal.call(
            services.db.run,
            lambda conn: conn.execute(
                "SELECT COUNT(*) FROM cycles c JOIN inspections i ON i.cycle_id = c.id "
                "WHERE c.lot_id = ? AND c.commanded_destination <> i.final_decision",
                (lot["id"],),
            ).fetchone()[0],
        )
        assert mismatches == 0


async def _call(fn: Callable[[], None]) -> None:
    fn()
