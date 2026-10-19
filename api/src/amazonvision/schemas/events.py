"""WebSocket /api/events contract: server -> client only. Commands always go through HTTP."""

from enum import StrEnum
from typing import Annotated, Literal

from pydantic import AwareDatetime, BaseModel, Field

from amazonvision.domain.machine import FaultCode, MachineState, Trigger
from amazonvision.domain.quality import Destination
from amazonvision.schemas.api import (
    DecidedBy,
    InspectionOut,
    LotOut,
    LotSummary,
    SystemStatus,
)


class EventType(StrEnum):
    SNAPSHOT = "SNAPSHOT"
    STATE_CHANGED = "STATE_CHANGED"
    SENSOR_CHANGED = "SENSOR_CHANGED"
    INSPECTION_READY = "INSPECTION_READY"
    DECISION_ACCEPTED = "DECISION_ACCEPTED"
    CYCLE_COMPLETED = "CYCLE_COMPLETED"
    CYCLE_ABORTED = "CYCLE_ABORTED"
    LOT_UPDATED = "LOT_UPDATED"
    CONNECTION_LOST = "CONNECTION_LOST"
    CONNECTION_RESTORED = "CONNECTION_RESTORED"
    FAULT = "FAULT"


class Component(StrEnum):
    DEVICE = "device"
    CAMERA = "camera"
    MODEL = "model"
    STORAGE = "storage"


class _Event(BaseModel):
    seq: int = Field(
        ge=1, description="Sequência do servidor; lacuna = cliente deve pedir novo snapshot"
    )
    at: AwareDatetime
    state_version: int = Field(ge=0)
    lot_id: int | None = None
    cycle_id: int | None = None


class SnapshotEvent(_Event):
    """Always the first message after connecting or reconnecting."""

    type: Literal[EventType.SNAPSHOT] = EventType.SNAPSHOT
    data: SystemStatus


class StateChangedData(BaseModel):
    from_state: MachineState
    to_state: MachineState
    trigger: Trigger
    fault: FaultCode | None = None


class StateChangedEvent(_Event):
    type: Literal[EventType.STATE_CHANGED] = EventType.STATE_CHANGED
    data: StateChangedData


class SensorChangedData(BaseModel):
    sensor: Literal["S1", "S2", "ESTOP"]
    active: bool


class SensorChangedEvent(_Event):
    type: Literal[EventType.SENSOR_CHANGED] = EventType.SENSOR_CHANGED
    data: SensorChangedData


class InspectionReadyEvent(_Event):
    type: Literal[EventType.INSPECTION_READY] = EventType.INSPECTION_READY
    data: InspectionOut


class DecisionAcceptedData(BaseModel):
    inspection_id: int
    destination: Destination
    decided_by: DecidedBy


class DecisionAcceptedEvent(_Event):
    type: Literal[EventType.DECISION_ACCEPTED] = EventType.DECISION_ACCEPTED
    data: DecisionAcceptedData


class CycleCompletedData(BaseModel):
    destination: Destination
    summary: LotSummary


class CycleCompletedEvent(_Event):
    type: Literal[EventType.CYCLE_COMPLETED] = EventType.CYCLE_COMPLETED
    data: CycleCompletedData


class CycleAbortedData(BaseModel):
    reason: str
    summary: LotSummary


class CycleAbortedEvent(_Event):
    type: Literal[EventType.CYCLE_ABORTED] = EventType.CYCLE_ABORTED
    data: CycleAbortedData


class LotUpdatedData(BaseModel):
    lot: LotOut
    summary: LotSummary


class LotUpdatedEvent(_Event):
    type: Literal[EventType.LOT_UPDATED] = EventType.LOT_UPDATED
    data: LotUpdatedData


class ConnectionData(BaseModel):
    component: Component
    message: str


class ConnectionLostEvent(_Event):
    type: Literal[EventType.CONNECTION_LOST] = EventType.CONNECTION_LOST
    data: ConnectionData


class ConnectionRestoredEvent(_Event):
    type: Literal[EventType.CONNECTION_RESTORED] = EventType.CONNECTION_RESTORED
    data: ConnectionData


class FaultData(BaseModel):
    code: FaultCode
    message: str = Field(description="Texto para o operador")
    recovery: str | None = None


class FaultEvent(_Event):
    type: Literal[EventType.FAULT] = EventType.FAULT
    data: FaultData


WsEvent = Annotated[
    SnapshotEvent
    | StateChangedEvent
    | SensorChangedEvent
    | InspectionReadyEvent
    | DecisionAcceptedEvent
    | CycleCompletedEvent
    | CycleAbortedEvent
    | LotUpdatedEvent
    | ConnectionLostEvent
    | ConnectionRestoredEvent
    | FaultEvent,
    Field(discriminator="type"),
]
