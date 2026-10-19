"""Serial protocol v1 between the host (this service) and the ESP32.

One compact JSON object per line (UTF-8, LF). Spec: docs/protocolo-serial.md.
"""

import json
from enum import StrEnum
from typing import Annotated, Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    TypeAdapter,
    ValidationError,
    model_validator,
)

from amazonvision.domain.machine import FaultCode, MachineState, Trigger
from amazonvision.domain.quality import Destination

__all__ = ["Destination"]  # re-exported: part of the wire contract

PROTOCOL_VERSION = 1
MAX_LINE_BYTES = 1024

CmdId = Annotated[str, StringConstraints(pattern=r"^[A-Za-z0-9_-]{1,24}$")]
HexId = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{8}$")]
DbId = Annotated[int, Field(ge=1, le=2_147_483_647)]
Uint32 = Annotated[int, Field(ge=0, le=4_294_967_295)]
Degrees = Annotated[int, Field(ge=0, le=180)]
ShortText = Annotated[str, StringConstraints(max_length=80)]


class CommandName(StrEnum):
    HELLO = "HELLO"
    CONFIGURE = "CONFIGURE"
    ARM = "ARM"
    STOP = "STOP"
    START_CYCLE = "START_CYCLE"
    DECISION = "DECISION"
    HOLD_FOR_REVIEW = "HOLD_FOR_REVIEW"
    CLEAR_FAULT = "CLEAR_FAULT"
    ENTER_MAINTENANCE = "ENTER_MAINTENANCE"
    EXIT_MAINTENANCE = "EXIT_MAINTENANCE"
    GET_STATUS = "GET_STATUS"
    TEST_MOTOR = "TEST_MOTOR"
    TEST_SERVO = "TEST_SERVO"


class EventName(StrEnum):
    STATE_CHANGED = "STATE_CHANGED"
    SENSOR_CHANGED = "SENSOR_CHANGED"
    CAPTURE_READY = "CAPTURE_READY"
    CYCLE_COMPLETED = "CYCLE_COMPLETED"
    CYCLE_ABORTED = "CYCLE_ABORTED"
    FAULT = "FAULT"


class NakCode(StrEnum):
    BAD_JSON = "BAD_JSON"
    LINE_TOO_LONG = "LINE_TOO_LONG"
    UNSUPPORTED_VERSION = "UNSUPPORTED_VERSION"
    UNKNOWN_COMMAND = "UNKNOWN_COMMAND"
    INVALID_PAYLOAD = "INVALID_PAYLOAD"
    NO_SESSION = "NO_SESSION"
    SESSION_MISMATCH = "SESSION_MISMATCH"
    INVALID_STATE = "INVALID_STATE"
    CYCLE_MISMATCH = "CYCLE_MISMATCH"
    NOT_CONFIGURED = "NOT_CONFIGURED"
    PRECONDITION_FAILED = "PRECONDITION_FAILED"


class SensorName(StrEnum):
    S1 = "S1"
    S2 = "S2"
    ESTOP = "ESTOP"


class AbortReason(StrEnum):
    STOP = "STOP"
    ESTOP = "ESTOP"
    S1_TIMEOUT = FaultCode.S1_TIMEOUT.value
    DECISION_TIMEOUT = FaultCode.DECISION_TIMEOUT.value
    S2_TIMEOUT = FaultCode.S2_TIMEOUT.value
    EXIT_BLOCKED = FaultCode.EXIT_BLOCKED.value
    LINK_LOST = FaultCode.LINK_LOST.value
    SESSION_REPLACED = FaultCode.SESSION_REPLACED.value
    SENSOR_CONFLICT = FaultCode.SENSOR_CONFLICT.value
    INTERNAL = FaultCode.INTERNAL.value


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class EmptyPayload(_Strict):
    pass


# ---------------------------------------------------------------- payloads


class ConfigurePayload(_Strict):
    """Bench timing and actuator parameters. All values are calibrated per profile."""

    sensor_debounce_ms: Annotated[int, Field(ge=1, le=200)]
    s1_timeout_ms: Annotated[int, Field(ge=500, le=30_000)]
    settle_ms: Annotated[int, Field(ge=0, le=5_000)]
    decision_timeout_ms: Annotated[int, Field(ge=500, le=30_000)]
    s2_timeout_ms: Annotated[int, Field(ge=500, le=30_000)]
    servo_rest_deg: Degrees
    servo_reject_deg: Degrees
    reject_hold_ms: Annotated[int, Field(ge=100, le=5_000)]
    reject_motor_ms: Annotated[int, Field(ge=0, le=10_000)]
    release_ms: Annotated[int, Field(ge=0, le=10_000)]
    release_max_ms: Annotated[int, Field(ge=500, le=30_000)]
    link_timeout_ms: Annotated[int, Field(ge=500, le=10_000)]
    motor_power_pct: Annotated[int, Field(ge=1, le=100)] | None = None

    @model_validator(mode="after")
    def _coherent(self) -> Self:
        if self.servo_rest_deg == self.servo_reject_deg:
            raise ValueError("servo_reject_deg deve ser diferente de servo_rest_deg")
        if self.release_max_ms < self.release_ms:
            raise ValueError("release_max_ms deve ser >= release_ms")
        return self


class DecisionPayload(_Strict):
    destination: Destination


class MotorTestPayload(_Strict):
    run_ms: Annotated[int, Field(ge=1, le=5_000)]


class ServoTestPayload(_Strict):
    angle_deg: Degrees
    hold_ms: Annotated[int, Field(ge=0, le=5_000)]


# ---------------------------------------------------------------- host -> device


class _HostBase(_Strict):
    protocol_version: Literal[1] = PROTOCOL_VERSION
    session_id: HexId


class _CommandBase(_HostBase):
    type: Literal["cmd"] = "cmd"
    cmd_id: CmdId


class HelloCmd(_CommandBase):
    """session_id is the new session proposed by the host."""

    name: Literal[CommandName.HELLO] = CommandName.HELLO
    payload: EmptyPayload = EmptyPayload()


class ConfigureCmd(_CommandBase):
    name: Literal[CommandName.CONFIGURE] = CommandName.CONFIGURE
    payload: ConfigurePayload


class ArmCmd(_CommandBase):
    name: Literal[CommandName.ARM] = CommandName.ARM
    payload: EmptyPayload = EmptyPayload()


class StopCmd(_CommandBase):
    name: Literal[CommandName.STOP] = CommandName.STOP
    payload: EmptyPayload = EmptyPayload()


class StartCycleCmd(_CommandBase):
    name: Literal[CommandName.START_CYCLE] = CommandName.START_CYCLE
    lot_id: DbId
    cycle_id: DbId
    payload: EmptyPayload = EmptyPayload()


class DecisionCmd(_CommandBase):
    name: Literal[CommandName.DECISION] = CommandName.DECISION
    cycle_id: DbId
    payload: DecisionPayload


class HoldForReviewCmd(_CommandBase):
    name: Literal[CommandName.HOLD_FOR_REVIEW] = CommandName.HOLD_FOR_REVIEW
    cycle_id: DbId
    payload: EmptyPayload = EmptyPayload()


class ClearFaultCmd(_CommandBase):
    name: Literal[CommandName.CLEAR_FAULT] = CommandName.CLEAR_FAULT
    payload: EmptyPayload = EmptyPayload()


class EnterMaintenanceCmd(_CommandBase):
    name: Literal[CommandName.ENTER_MAINTENANCE] = CommandName.ENTER_MAINTENANCE
    payload: EmptyPayload = EmptyPayload()


class ExitMaintenanceCmd(_CommandBase):
    name: Literal[CommandName.EXIT_MAINTENANCE] = CommandName.EXIT_MAINTENANCE
    payload: EmptyPayload = EmptyPayload()


class GetStatusCmd(_CommandBase):
    name: Literal[CommandName.GET_STATUS] = CommandName.GET_STATUS
    payload: EmptyPayload = EmptyPayload()


class MotorTestCmd(_CommandBase):
    name: Literal[CommandName.TEST_MOTOR] = CommandName.TEST_MOTOR
    payload: MotorTestPayload


class ServoTestCmd(_CommandBase):
    name: Literal[CommandName.TEST_SERVO] = CommandName.TEST_SERVO
    payload: ServoTestPayload


HostCommand = Annotated[
    HelloCmd
    | ConfigureCmd
    | ArmCmd
    | StopCmd
    | StartCycleCmd
    | DecisionCmd
    | HoldForReviewCmd
    | ClearFaultCmd
    | EnterMaintenanceCmd
    | ExitMaintenanceCmd
    | GetStatusCmd
    | MotorTestCmd
    | ServoTestCmd,
    Field(discriminator="name"),
]


class HostHeartbeat(_HostBase):
    type: Literal["hb"] = "hb"


HostMessage = Annotated[HostCommand | HostHeartbeat, Field(discriminator="type")]


# ---------------------------------------------------------------- device -> host


class DeviceStatus(_Strict):
    s1: bool
    s2: bool
    estop: bool
    motor_on: bool
    servo_deg_cmd: Degrees
    configured: bool
    lot_id: DbId | None = None
    cycle_id: DbId | None = None
    destination: Destination | None = None
    fault: FaultCode | None = None
    uptime_ms: Uint32


class AckPayload(_Strict):
    fw_version: Annotated[str, StringConstraints(max_length=16)] | None = None
    config_hash: Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{8}$")] | None = None
    status: DeviceStatus | None = None


class _DeviceBase(_Strict):
    protocol_version: Literal[1] = PROTOCOL_VERSION
    boot_id: HexId
    session_id: HexId | None = None
    seq: Uint32
    state: MachineState


class DeviceAck(_DeviceBase):
    """Command accepted. Physical completion is reported later by events."""

    type: Literal["ack"] = "ack"
    cmd_id: CmdId
    name: CommandName
    duplicate: bool = False
    payload: AckPayload = AckPayload()


class DeviceNak(_DeviceBase):
    type: Literal["nak"] = "nak"
    cmd_id: CmdId | None = None
    code: NakCode
    detail: ShortText | None = None
    duplicate: bool = False


class StateChangedPayload(_Strict):
    from_state: MachineState
    to_state: MachineState
    trigger: Trigger
    fault: FaultCode | None = None


class SensorChangedPayload(_Strict):
    sensor: SensorName
    active: bool


class CycleCompletedPayload(_Strict):
    destination: Destination


class CycleAbortedPayload(_Strict):
    reason: AbortReason


class FaultPayload(_Strict):
    code: FaultCode
    detail: ShortText | None = None


class _EventBase(_DeviceBase):
    type: Literal["evt"] = "evt"


class StateChangedEvt(_EventBase):
    name: Literal[EventName.STATE_CHANGED] = EventName.STATE_CHANGED
    cycle_id: DbId | None = None
    payload: StateChangedPayload


class SensorChangedEvt(_EventBase):
    name: Literal[EventName.SENSOR_CHANGED] = EventName.SENSOR_CHANGED
    cycle_id: DbId | None = None
    payload: SensorChangedPayload


class CaptureReadyEvt(_EventBase):
    name: Literal[EventName.CAPTURE_READY] = EventName.CAPTURE_READY
    cycle_id: DbId
    payload: EmptyPayload = EmptyPayload()


class CycleCompletedEvt(_EventBase):
    name: Literal[EventName.CYCLE_COMPLETED] = EventName.CYCLE_COMPLETED
    cycle_id: DbId
    payload: CycleCompletedPayload


class CycleAbortedEvt(_EventBase):
    name: Literal[EventName.CYCLE_ABORTED] = EventName.CYCLE_ABORTED
    cycle_id: DbId
    payload: CycleAbortedPayload


class FaultEvt(_EventBase):
    name: Literal[EventName.FAULT] = EventName.FAULT
    cycle_id: DbId | None = None
    payload: FaultPayload


DeviceEvent = Annotated[
    StateChangedEvt
    | SensorChangedEvt
    | CaptureReadyEvt
    | CycleCompletedEvt
    | CycleAbortedEvt
    | FaultEvt,
    Field(discriminator="name"),
]


class DeviceHeartbeat(_DeviceBase):
    type: Literal["hb"] = "hb"
    payload: DeviceStatus


DeviceMessage = Annotated[
    DeviceAck | DeviceNak | DeviceEvent | DeviceHeartbeat, Field(discriminator="type")
]


# ---------------------------------------------------------------- framing


class ProtocolError(Exception):
    def __init__(self, code: NakCode, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def encode(message: BaseModel) -> bytes:
    """Serialize one message as a compact JSON line."""
    line = message.model_dump_json(exclude_none=True).encode("utf-8") + b"\n"
    if len(line) > MAX_LINE_BYTES:
        raise ProtocolError(NakCode.LINE_TOO_LONG, f"{len(line)} bytes")
    return line


def _decode(line: bytes) -> dict:
    if len(line) > MAX_LINE_BYTES:
        raise ProtocolError(NakCode.LINE_TOO_LONG, f"{len(line)} bytes")
    try:
        data = json.loads(line.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProtocolError(NakCode.BAD_JSON, str(exc)[:80]) from exc
    if not isinstance(data, dict):
        raise ProtocolError(NakCode.BAD_JSON, "esperado objeto JSON")
    if data.get("protocol_version") != PROTOCOL_VERSION:
        raise ProtocolError(NakCode.UNSUPPORTED_VERSION, repr(data.get("protocol_version")))
    return data


HOST_ADAPTER: TypeAdapter[HostMessage] = TypeAdapter(HostMessage)
DEVICE_ADAPTER: TypeAdapter[DeviceMessage] = TypeAdapter(DeviceMessage)


def _validate[M](adapter: TypeAdapter[M], data: dict) -> M:
    try:
        return adapter.validate_python(data)
    except ValidationError as exc:
        first = exc.errors()[0]
        where = ".".join(str(p) for p in first["loc"])
        raise ProtocolError(NakCode.INVALID_PAYLOAD, f"{where}: {first['msg']}"[:80]) from exc


def parse_device_line(line: bytes) -> DeviceMessage:
    return _validate(DEVICE_ADAPTER, _decode(line.strip()))


def parse_host_line(line: bytes) -> HostMessage:
    data = _decode(line.strip())
    if data.get("type") == "cmd" and data.get("name") not in set(CommandName):
        raise ProtocolError(NakCode.UNKNOWN_COMMAND, repr(data.get("name"))[:80])
    return _validate(HOST_ADAPTER, data)
