import json
from pathlib import Path

import pytest

from amazonvision.machine.protocol import (
    MAX_LINE_BYTES,
    CaptureReadyEvt,
    ConfigureCmd,
    ConfigurePayload,
    DecisionCmd,
    DecisionPayload,
    Destination,
    DeviceAck,
    HelloCmd,
    NakCode,
    ProtocolError,
    encode,
    parse_device_line,
    parse_host_line,
)

EXAMPLES = Path(__file__).resolve().parents[2] / "docs" / "protocolo" / "exemplos"
VALID = sorted((EXAMPLES / "validos").glob("*.json"))
INVALID = sorted((EXAMPLES / "invalidos").glob("*.json"))


def _compact(path: Path) -> bytes:
    data = json.loads(path.read_text(encoding="utf-8"))
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def test_examples_exist():
    assert len(VALID) >= 20
    assert len(INVALID) >= 10


@pytest.mark.parametrize("path", VALID, ids=lambda p: p.stem)
def test_valid_examples_parse_and_roundtrip(path: Path):
    line = _compact(path)
    parse = parse_host_line if path.stem.startswith("host-") else parse_device_line
    message = parse(line)
    reencoded = encode(message)
    assert len(reencoded) <= MAX_LINE_BYTES
    assert parse(reencoded) == message


@pytest.mark.parametrize("path", INVALID, ids=lambda p: p.stem)
def test_invalid_examples_are_rejected_with_expected_code(path: Path):
    case = json.loads(path.read_text(encoding="utf-8"))
    parse = parse_host_line if case["direction"] == "host" else parse_device_line
    with pytest.raises(ProtocolError) as info:
        parse(case["line"].encode("utf-8"))
    assert info.value.code == NakCode(case["expect"])


def test_line_too_long_is_rejected_before_parsing():
    with pytest.raises(ProtocolError) as info:
        parse_host_line(b"{" + b" " * MAX_LINE_BYTES + b"}")
    assert info.value.code is NakCode.LINE_TOO_LONG


def test_encode_is_single_compact_line_without_nulls():
    line = encode(HelloCmd(session_id="5e1a9c03", cmd_id="c1"))
    assert line.endswith(b"\n")
    assert line.count(b"\n") == 1
    assert b": " not in line
    assert b"null" not in line


def test_largest_messages_fit_the_line_limit():
    config = ConfigurePayload(
        sensor_debounce_ms=200,
        s1_timeout_ms=30_000,
        settle_ms=5_000,
        decision_timeout_ms=30_000,
        s2_timeout_ms=30_000,
        servo_rest_deg=180,
        servo_reject_deg=179,
        reject_hold_ms=5_000,
        reject_motor_ms=10_000,
        release_ms=10_000,
        release_max_ms=30_000,
        link_timeout_ms=10_000,
        motor_power_pct=100,
    )
    cmd = ConfigureCmd(session_id="ffffffff", cmd_id="x" * 24, payload=config)
    assert len(encode(cmd)) <= MAX_LINE_BYTES // 2


def test_decision_requires_matching_cycle_and_destination():
    cmd = DecisionCmd(
        session_id="5e1a9c03",
        cmd_id="c9",
        cycle_id=41,
        payload=DecisionPayload(destination=Destination.APPROVED),
    )
    assert parse_host_line(encode(cmd)) == cmd


def test_ack_defaults_are_not_duplicate():
    ack = DeviceAck(
        boot_id="b0071d2e", seq=1, state="READY", cmd_id="c1", name="ARM", session_id="5e1a9c03"
    )
    assert ack.duplicate is False
    assert parse_device_line(encode(ack)) == ack


def test_capture_ready_requires_cycle_id():
    evt = CaptureReadyEvt(boot_id="b0071d2e", seq=3, state="INSPECTING", cycle_id=7)
    assert parse_device_line(encode(evt)) == evt
