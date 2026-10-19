"""The real firmware logic (firmware/lib/av_core), compiled for the PC, checked against the
contract owned by this service: state table, protocol examples and full cycles via the API."""

import asyncio
import importlib.util
import json
import subprocess
import time
import uuid
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from amazonvision.config import Settings
from amazonvision.domain.machine import TRANSITIONS, MachineState, Trigger
from amazonvision.domain.quality import Grade
from amazonvision.machine.protocol import NakCode, parse_device_line
from amazonvision.main import create_app
from amazonvision.simulation.scenario import confident, uncertain

REPO = Path(__file__).resolve().parents[2]
EXAMPLES = REPO / "docs" / "protocolo" / "exemplos"
PARSE_ERRORS = {
    NakCode.BAD_JSON,
    NakCode.LINE_TOO_LONG,
    NakCode.UNSUPPORTED_VERSION,
    NakCode.UNKNOWN_COMMAND,
    NakCode.INVALID_PAYLOAD,
}


def _load_builder():
    spec = importlib.util.spec_from_file_location(
        "build_native", REPO / "firmware" / "tools" / "build_native.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def native() -> dict[str, Path]:
    builder = _load_builder()
    return {target: builder.build(target) for target in ("unit_tests", "harness")}


def test_firmware_unit_tests_pass(native):
    result = subprocess.run([native["unit_tests"]], capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr


def test_firmware_transition_table_matches_python(native):
    output = subprocess.run(
        [native["harness"], "--dump-transitions"], capture_output=True, text=True, timeout=30
    ).stdout
    table = {}
    for line in output.splitlines():
        state, trigger, nxt = line.split()
        table[(MachineState(state), Trigger(trigger))] = MachineState(nxt)
    assert table == TRANSITIONS


# ---------------------------------------------------------------- protocol contract


class Harness:
    """Talks to the native firmware; every line it prints must satisfy the Pydantic contract."""

    def __init__(self, process: asyncio.subprocess.Process) -> None:
        self.process = process
        self.received: list[Any] = []

    async def send(self, line: str) -> None:
        assert self.process.stdin is not None
        self.process.stdin.write(line.encode() + b"\n")
        await self.process.stdin.drain()

    async def wait(self, predicate: Callable[[Any], bool], timeout: float = 3.0) -> Any:
        assert self.process.stdout is not None
        async with asyncio.timeout(timeout):
            while True:
                raw = await self.process.stdout.readline()
                message = parse_device_line(raw)  # raises if the firmware breaks the contract
                self.received.append(message)
                if predicate(message):
                    return message


def _compact(path: Path) -> str:
    return json.dumps(json.loads(path.read_text(encoding="utf-8")), separators=(",", ":"))


@pytest.mark.anyio
async def test_firmware_accepts_every_valid_example_and_rejects_every_invalid_one(native):
    process = await asyncio.create_subprocess_exec(
        str(native["harness"]),
        "--belt-mm-s",
        "2000",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
    )
    harness = Harness(process)
    try:
        for path in sorted((EXAMPLES / "validos").glob("host-*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            await harness.send(_compact(path))
            if data["type"] == "hb":
                continue
            reply = await harness.wait(
                lambda m, cid=data["cmd_id"]: m.type in ("ack", "nak") and m.cmd_id == cid
            )
            assert reply.type == "ack" or reply.code not in PARSE_ERRORS, (path.name, reply)

        for path in sorted((EXAMPLES / "invalidos").glob("*.json")):
            case = json.loads(path.read_text(encoding="utf-8"))
            if case["direction"] != "host":
                continue
            await harness.send(case["line"])
            reply = await harness.wait(lambda m: m.type == "nak" and m.cmd_id is None)
            assert reply.code == NakCode(case["expect"]), path.name

        await harness.send("{" + " " * 1100 + "}")
        reply = await harness.wait(lambda m: m.type == "nak" and m.cmd_id is None)
        assert reply.code is NakCode.LINE_TOO_LONG

        await harness.wait(lambda m: m.type == "hb")
        seqs = [m.seq for m in harness.received]
        assert seqs == sorted(seqs) and len(set(seqs)) == len(seqs)
        for event in harness.received:
            if event.type == "evt" and event.name == "STATE_CHANGED":
                p = event.payload
                assert TRANSITIONS[(p.from_state, p.trigger)] is p.to_state
    finally:
        process.stdin.close()
        await asyncio.wait_for(process.wait(), timeout=5)


# ---------------------------------------------------------------- full system


@pytest.fixture
def firmware_bench(settings: Settings, native) -> Iterator[TestClient]:
    # 600 mm/s keeps a piece in each 40 mm sensor window longer than the 20 ms debounce.
    command = [str(native["harness"]), "--belt-mm-s", "600"]
    with TestClient(create_app(settings.model_copy(update={"firmware_harness": command}))) as c:
        yield c


def _status(client: TestClient) -> dict[str, Any]:
    return client.get("/api/status").json()


def _wait(client: TestClient, predicate: Callable[[dict], bool], timeout: float = 15) -> dict:
    deadline = time.monotonic() + timeout
    current = _status(client)
    while not predicate(current):
        if time.monotonic() > deadline:
            raise AssertionError(f"condição não atingida: {current['machine']}")
        time.sleep(0.05)
        current = _status(client)
    return current


def _machine(client: TestClient, headers: dict[str, str], action: str):
    return client.post(
        f"/api/machine/{action}", json={"request_id": str(uuid.uuid4())}, headers=headers
    )


def _control(client: TestClient, instruction: str) -> None:
    native_link = client.app.state.services.simulation.native

    async def send() -> None:
        await native_link.control(instruction)

    client.portal.call(send)


def test_api_runs_cycles_on_the_real_firmware_logic(firmware_bench: TestClient):
    client = firmware_bench
    status = _status(client)
    assert status["machine"]["link"]["port"] == "firmware nativo"
    assert status["machine"]["link"]["firmware_version"] == "nativo-0.2"

    headers = {
        "X-Control-Token": client.post("/api/control/claim", json={"operator": "Ana"}).json()[
            "token"
        ]
    }
    body = {"request_id": str(uuid.uuid4()), "product_id": "tucuma", "operator": "Ana"}
    assert client.post("/api/lots", json=body, headers=headers).status_code == 201
    client.app.state.services.simulation.scenario.push(
        confident(Grade.A), confident(Grade.B), uncertain()
    )

    assert _machine(client, headers, "start").status_code == 200
    waiting = _wait(client, lambda s: s["machine"]["state"] == "REVIEW_HOLD", timeout=25)
    assert waiting["active_lot_summary"]["cycles_completed"] == 2
    _machine(client, headers, "pause")

    inspection_id = waiting["machine"]["pending_review_inspection_id"]
    review = {
        "request_id": str(uuid.uuid4()),
        "decision": "REJECTED",
        "reviewer": "Ana",
        "reason": "conferido na bancada",
    }
    response = client.post(f"/api/inspections/{inspection_id}/review", json=review, headers=headers)
    assert response.status_code == 201
    final = _wait(client, lambda s: s["current_cycle"] is None and s["machine"]["state"] == "READY")
    summary = final["active_lot_summary"]
    assert summary["cycles_completed"] == 3
    assert summary["cycles_aborted"] == 0
    assert (summary["approved"], summary["rejected"], summary["reviewed"]) == (1, 2, 1)


def test_estop_and_reboot_on_the_real_firmware_logic(firmware_bench: TestClient):
    client = firmware_bench
    headers = {
        "X-Control-Token": client.post("/api/control/claim", json={"operator": "Ana"}).json()[
            "token"
        ]
    }
    body = {"request_id": str(uuid.uuid4()), "product_id": "castanha", "operator": "Ana"}
    client.post("/api/lots", json=body, headers=headers)
    client.app.state.services.simulation.scenario.push(uncertain())
    _machine(client, headers, "start")
    waiting = _wait(client, lambda s: s["machine"]["state"] == "REVIEW_HOLD", timeout=20)

    _control(client, "estop 1")
    estop = _wait(client, lambda s: s["machine"]["state"] == "ESTOP" and s["current_cycle"] is None)
    assert estop["active_lot_summary"]["cycles_aborted"] == 1
    assert _machine(client, headers, "rearm").status_code == 409

    _control(client, "estop 0")
    _wait(client, lambda s: s["machine"]["state"] == "DISARMED")
    # The piece is still under the camera: arming is refused until it is removed.
    refused = _machine(client, headers, "rearm")
    assert refused.status_code == 409
    assert "sensor" in refused.json()["message"]
    _control(client, "remove")
    _wait(client, lambda s: not s["machine"]["sensors"]["s1"])
    assert _machine(client, headers, "rearm").json()["state"] == "READY"

    old_boot = waiting["machine"]["link"]["boot_id"]
    _control(client, "reboot")
    after = _wait(
        client,
        lambda s: (
            s["machine"]["link"]["boot_id"] not in (None, old_boot)
            and s["machine"]["state"] == "DISARMED"
        ),
    )
    assert after["machine"]["running"] is False
