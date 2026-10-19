"""REST contract (spec §18). Routes are implemented from Block 3 on."""

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Literal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, StringConstraints

from amazonvision.config import RunMode
from amazonvision.domain.machine import FaultCode, MachineState
from amazonvision.domain.quality import AutoDecision, Destination, Grade, ReviewReason

DbId = Annotated[int, Field(ge=1)]
ProductId = Annotated[str, StringConstraints(pattern=r"^[a-z][a-z0-9_]{1,31}$")]
PersonName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=60)]


class _In(BaseModel):
    model_config = ConfigDict(extra="forbid")


# ---------------------------------------------------------------- products and models


class ModelValidationStatus(StrEnum):
    PENDING = "pending"
    VALIDATED = "validated"
    REJECTED = "rejected"


class ProductOut(BaseModel):
    id: ProductId
    name: str
    presentation: str | None = Field(description="Ex.: com casca / sem casca")
    active_model_id: str | None
    decision_threshold: float = Field(gt=0, le=1)
    version: int


class ModelOut(BaseModel):
    id: str
    product_id: ProductId
    architecture: str
    class_order: list[Grade]
    dataset_version: str
    validation_status: ModelValidationStatus
    metrics: dict[str, float] | None
    created_at: AwareDatetime


# ---------------------------------------------------------------- lots


class LotStatus(StrEnum):
    OPEN = "open"
    CLOSED = "closed"


class LotCreate(_In):
    request_id: UUID
    product_id: ProductId
    operator: PersonName
    notes: Annotated[str, StringConstraints(max_length=500)] | None = None


class LotOut(BaseModel):
    id: DbId
    product_id: ProductId
    model_id: str | None
    operator: str
    status: LotStatus
    is_simulated: bool
    started_at: AwareDatetime
    ended_at: AwareDatetime | None
    notes: str | None


class LotSummary(BaseModel):
    """Counters derived from stored records, never from client-side increments."""

    lot_id: DbId
    inspected: int = Field(ge=0, description="Inspeções registradas")
    approved: int = Field(ge=0, description="Decisão final aprovada (automática ou revisada)")
    rejected: int = Field(ge=0, description="Decisão final rejeitada")
    review_pending: int = Field(ge=0, description="Inconclusivos ainda sem decisão do operador")
    reviewed: int = Field(ge=0, description="Inspeções com revisão humana")
    by_grade: dict[Grade, int] = Field(description="Previsões do modelo por classe")
    cycles_completed: int = Field(ge=0)
    cycles_aborted: int = Field(ge=0)
    approval_rate: float | None = Field(
        ge=0, le=1, description="approved / (approved + rejected); nulo se o denominador é zero"
    )
    approval_rate_denominator: int = Field(ge=0)


# ---------------------------------------------------------------- machine control


class MachineCommandRequest(_In):
    request_id: UUID = Field(description="Repetir o mesmo id devolve o resultado original")
    expected_state: MachineState | None = Field(
        default=None, description="Recusa com INVALID_STATE se o estado atual for outro"
    )


class MachineCommandResult(BaseModel):
    request_id: UUID
    accepted: bool
    duplicate: bool
    state: MachineState


class ControlClaim(_In):
    operator: PersonName


class ControlGrant(BaseModel):
    token: str = Field(description="Enviar no cabeçalho X-Control-Token nas rotas de controle")
    operator: str
    expires_at: AwareDatetime


# ---------------------------------------------------------------- cycles and inspections


class CycleStatus(StrEnum):
    RUNNING = "running"
    COMPLETED = "completed"
    ABORTED = "aborted"


class CycleOut(BaseModel):
    id: DbId
    lot_id: DbId
    seq_in_lot: int = Field(ge=1)
    status: CycleStatus
    machine_state: MachineState | None
    commanded_destination: Destination | None
    abort_reason: str | None
    started_at: AwareDatetime
    ended_at: AwareDatetime | None


class DecidedBy(StrEnum):
    AUTO = "auto"
    OPERATOR = "operator"


class InspectionOut(BaseModel):
    id: DbId
    cycle_id: DbId
    lot_id: DbId
    product_id: ProductId
    captured_at: AwareDatetime
    image_url: str
    model_id: str | None
    predicted_grade: Grade | None
    scores: dict[Grade, float] | None
    confidence: float | None = Field(description="Confiança estimada do modelo, não taxa de acerto")
    latency_ms: float | None
    auto_decision: AutoDecision
    review_reason: ReviewReason | None
    final_decision: Destination | None
    decided_by: DecidedBy | None
    cycle_status: CycleStatus


class InspectionReviewCreate(_In):
    request_id: UUID
    decision: Destination
    reviewer: PersonName
    reason: Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=200)]


class ReviewOut(BaseModel):
    id: DbId
    inspection_id: DbId
    reviewer: str
    previous_decision: Destination | None
    new_decision: Destination
    reason: str
    created_at: AwareDatetime


class InspectionPage(BaseModel):
    items: list[InspectionOut]
    total: int = Field(ge=0)
    limit: int = Field(ge=1, le=200)
    offset: int = Field(ge=0)


# ---------------------------------------------------------------- status snapshot


class SensorSnapshot(BaseModel):
    s1: bool
    s2: bool
    estop: bool


class DeviceLink(BaseModel):
    connected: bool
    port: str | None
    boot_id: str | None
    firmware_version: str | None
    last_seen_at: AwareDatetime | None = Field(description="Última mensagem recebida da placa")


class MachineInfo(BaseModel):
    state: MachineState | None = Field(description="Nulo se a placa nunca respondeu")
    fault: FaultCode | None
    sensors: SensorSnapshot | None
    link: DeviceLink


class CameraInfo(BaseModel):
    status: Literal["ok", "unavailable", "stale"]
    source: str | None
    last_frame_at: AwareDatetime | None


class ModelInfo(BaseModel):
    status: Literal["ready", "not_loaded", "loading", "error"]
    model_id: str | None
    product_id: ProductId | None


class StorageInfo(BaseModel):
    status: Literal["ok", "low_space", "error"]
    free_bytes: int | None


class SystemStatus(BaseModel):
    mode: RunMode
    generated_at: datetime
    state_version: int = Field(ge=0, description="Cresce a cada mudança relevante de estado")
    machine: MachineInfo
    camera: CameraInfo
    model: ModelInfo
    storage: StorageInfo
    control_locked: bool = Field(description="Há um operador com o controle ativo")
    active_lot: LotOut | None
    active_lot_summary: LotSummary | None
    current_cycle: CycleOut | None
