"""Labeling agreement: two reviewers label the same Coleta photos blind, compared afterwards."""

from typing import Any

from fastapi.testclient import TestClient

from tests.test_dataset import capture

SESSION = "2026-10-20-criterios"


def submit(
    client: TestClient, sample_id: int, reviewer: str, label: str, product: str = "tucuma"
) -> Any:
    body = {
        "product_id": product,
        "session": SESSION,
        "sample_id": sample_id,
        "reviewer": reviewer,
        "label": label,
    }
    return client.post("/api/dataset/agreement/labels", json=body)


def test_submitting_a_label_needs_no_control(client: TestClient, control):
    sample = capture(client, control).json()
    response = submit(client, sample["id"], "Ana", "A")
    assert response.status_code == 201, response.text
    assert response.json() == {
        "sample_id": sample["id"],
        "reviewer": "Ana",
        "label": "A",
        "created_at": response.json()["created_at"],
    }


def test_relabeling_the_same_photo_updates_the_answer(client: TestClient, control):
    sample = capture(client, control).json()
    submit(client, sample["id"], "Ana", "A")
    second = submit(client, sample["id"], "Ana", "B")
    assert second.json()["label"] == "B"


def test_queue_hands_out_photos_not_yet_labeled_by_this_reviewer(client: TestClient, control):
    first = capture(client, control, piece="T-1").json()
    second = capture(client, control, piece="T-2").json()

    params = {"product_id": "tucuma", "session": SESSION, "reviewer": "Ana"}
    next1 = client.get("/api/dataset/agreement/next", params=params)
    assert next1.status_code == 200
    assert next1.json()["remaining"] == 2
    first_id = next1.json()["sample"]["id"]
    assert first_id in (first["id"], second["id"])

    submit(client, first_id, "Ana", "A")
    next2 = client.get("/api/dataset/agreement/next", params=params).json()
    assert next2["remaining"] == 1
    assert next2["sample"]["id"] != first_id

    submit(client, next2["sample"]["id"], "Ana", "A")
    done = client.get("/api/dataset/agreement/next", params=params)
    assert done.status_code == 200
    assert done.json() is None


def test_each_reviewer_has_their_own_queue(client: TestClient, control):
    sample = capture(client, control).json()
    submit(client, sample["id"], "Ana", "A")

    params = {"product_id": "tucuma", "session": SESSION, "reviewer": "Bruno"}
    pending = client.get("/api/dataset/agreement/next", params=params).json()
    assert pending["sample"]["id"] == sample["id"]  # Bruno still has not labeled it


def test_summary_needs_two_reviewers(client: TestClient, control):
    sample = capture(client, control).json()
    submit(client, sample["id"], "Ana", "A")

    only_one = client.get(
        "/api/dataset/agreement/summary", params={"product_id": "tucuma", "session": SESSION}
    )
    assert only_one.status_code == 409
    assert only_one.json()["code"] == "INVALID_STATE"


def test_summary_reports_agreement_and_disagreement(client: TestClient, control):
    agree = capture(client, control, piece="T-1").json()
    disagree = capture(client, control, piece="T-2").json()
    only_ana = capture(client, control, piece="T-3").json()

    submit(client, agree["id"], "Ana", "A")
    submit(client, agree["id"], "Bruno", "A")
    submit(client, disagree["id"], "Ana", "B")
    submit(client, disagree["id"], "Bruno", "C")
    submit(client, only_ana["id"], "Ana", "A")  # Bruno never gets to this one

    summary = client.get(
        "/api/dataset/agreement/summary", params={"product_id": "tucuma", "session": SESSION}
    )
    assert summary.status_code == 200, summary.text
    data = summary.json()
    assert data["reviewers"] == ["Ana", "Bruno"]
    assert data["compared"] == 2  # only_ana is not compared: just one reviewer so far
    assert data["agreed"] == 1
    assert data["agreement_rate"] == 0.5
    [item] = data["disagreements"]
    assert item["sample"]["id"] == disagree["id"]
    assert item["labels"] == {"Ana": "B", "Bruno": "C"}
    assert item["agree"] is False


def test_sessions_do_not_mix(client: TestClient, control):
    sample = capture(client, control).json()
    submit(client, sample["id"], "Ana", "A")
    client.post(
        "/api/dataset/agreement/labels",
        json={
            "product_id": "tucuma",
            "session": "outra-rodada",
            "sample_id": sample["id"],
            "reviewer": "Bruno",
            "label": "B",
        },
    )
    summary = client.get(
        "/api/dataset/agreement/summary", params={"product_id": "tucuma", "session": SESSION}
    )
    assert summary.status_code == 409  # Bruno labeled it in a different session


def test_label_rejected_for_unknown_product_or_sample(client: TestClient, control):
    sample = capture(client, control).json()
    assert submit(client, sample["id"], "Ana", "A", product="acai").status_code == 422
    missing = submit(client, 999999, "Ana", "A")
    assert missing.status_code == 404
