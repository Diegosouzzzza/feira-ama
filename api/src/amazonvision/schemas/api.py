"""REST contract (spec §18). Routes are implemented from Block 3 on."""

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Literal, Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, StringConstraints, model_validator

from amazonvision.config import RunMode
from amazonvision.domain.machine import FaultCode, MachineState
from amazonvision.domain.quality import AutoDecision, Destination, Grade, ReviewReason
from amazonvision.machine.protocol import ConfigurePayload

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
    validated_by: str | None
    metrics: dict[str, float | bool | None] | None = Field(
        description="Resumo do teste: falsa aprovação, rejeição de B/C, revisão, latência"
    )
    recommended_threshold: float | None = Field(
        description="Limiar escolhido na validação; vira o limiar do produto ao ativar"
    )
    active: bool = Field(description="É o modelo ativo do produto")
    created_at: AwareDatetime


class ModelInstall(_In):
    path: Annotated[str, StringConstraints(min_length=1, max_length=500)] = Field(
        description="Pasta do pacote (model.onnx + model.json) neste computador"
    )


class ModelValidationUpdate(_In):
    status: Literal[ModelValidationStatus.VALIDATED, ModelValidationStatus.REJECTED]
    reviewer: PersonName


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
    takeover: bool = Field(
        default=False, description="Assumir o controle mesmo que outro operador o tenha"
    )


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


class InspectionOutcome(StrEnum):
    APPROVED = "approved"  # final decision: approved
    REJECTED = "rejected"  # final decision: rejected
    PENDING_REVIEW = "pending_review"  # inconclusive, still waiting for the operator
    INCONCLUSIVE = "inconclusive"  # sent to review by the policy (decided or not)
    REVIEWED = "reviewed"  # decided or corrected by a person


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


# ---------------------------------------------------------------- diagnostics


class EventSource(StrEnum):
    DEVICE = "device"
    HOST = "host"
    OPERATOR = "operator"


class Severity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class EventOut(BaseModel):
    id: DbId
    source: EventSource
    type: str
    severity: Severity
    lot_id: int | None
    cycle_id: int | None
    data: dict
    occurred_at: AwareDatetime


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
    fault_message: str | None = Field(default=None, description="Texto da falha para o operador")
    fault_recovery: str | None = Field(default=None, description="Ação sugerida para a falha")
    sensors: SensorSnapshot | None
    link: DeviceLink
    running: bool = Field(description="Operação automática ativa: novos ciclos são iniciados")
    pending_review_inspection_id: int | None = Field(
        description="Inspeção inconclusiva aguardando decisão do operador"
    )


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
    control_holder: str | None = Field(description="Nome do operador com o controle")
    active_lot: LotOut | None
    active_lot_summary: LotSummary | None
    current_cycle: CycleOut | None


# ---------------------------------------------------------------- photo collection (dataset)

# Ends up in file names and in the training manifest: letters, digits, "-" and "_" only.
CollectionTag = Annotated[str, StringConstraints(pattern=r"^[A-Za-z0-9][A-Za-z0-9_-]{0,39}$")]


class SampleStatus(StrEnum):
    PENDING = "pending"  # photographed, not labeled yet
    LABELED = "labeled"
    AMBIGUOUS = "ambiguous"  # the team could not agree: kept out of training
    UNUSABLE = "unusable"  # blurred, cut off, wrong piece: kept out of training


class DatasetCapture(_In):
    product_id: ProductId
    physical_sample_id: CollectionTag = Field(description="Etiqueta da peça física (ex.: T-0042)")
    collection_session: CollectionTag = Field(
        description="Sessão de coleta (ex.: 2026-10-19-manha)"
    )
    label: Grade | None = Field(default=None, description="Vazio: rotular depois")


class DatasetSampleOut(BaseModel):
    id: DbId
    product_id: ProductId
    physical_sample_id: str
    collection_session: str
    image_url: str
    label: Grade | None
    label_author: str | None
    status: SampleStatus
    reviewed_by: str | None
    created_at: AwareDatetime
    updated_at: AwareDatetime


class DatasetSampleUpdate(_In):
    status: SampleStatus
    label: Grade | None = Field(default=None, description="Obrigatório quando status = labeled")


class DatasetSamplePage(BaseModel):
    items: list[DatasetSampleOut]
    total: int = Field(ge=0)
    limit: int = Field(ge=1, le=200)
    offset: int = Field(ge=0)


class DatasetClassCount(BaseModel):
    label: Grade
    photos: int = Field(ge=0)
    pieces: int = Field(ge=0, description="Peças físicas distintas")


class DatasetSummary(BaseModel):
    product_id: ProductId
    target_photos_per_class: int
    classes: list[DatasetClassCount]
    pending: int = Field(ge=0)
    ambiguous: int = Field(ge=0)
    unusable: int = Field(ge=0)
    total: int = Field(ge=0)


class DatasetExport(_In):
    product_id: ProductId


class DatasetExportOut(BaseModel):
    product_id: ProductId
    manifest_path: str = Field(description="Arquivo CSV no formato do treinamento")
    photos: int = Field(ge=0)
    pieces: int = Field(ge=0)
    command: str = Field(description="Comando para treinar a partir deste manifesto")


# ---------------------------------------------------------------- teste de concordância


class AgreementLabelCreate(_In):
    product_id: ProductId
    session: CollectionTag = Field(description="Rodada do teste (ex.: 2026-10-20-criterios)")
    sample_id: DbId
    reviewer: PersonName
    label: Grade


class AgreementLabelOut(BaseModel):
    sample_id: DbId
    reviewer: str
    label: Grade
    created_at: AwareDatetime


class AgreementQueueItem(BaseModel):
    sample: DatasetSampleOut
    remaining: int = Field(ge=0, description="Fotos deste produto ainda sem rótulo deste revisor")


class AgreementSampleResult(BaseModel):
    sample: DatasetSampleOut
    labels: dict[str, Grade] = Field(description="Rótulo de cada revisor nesta rodada")
    agree: bool


class AgreementSummary(BaseModel):
    product_id: ProductId
    session: str
    reviewers: list[str]
    compared: int = Field(ge=0, description="Fotos com rótulo de 2 ou mais revisores")
    agreed: int = Field(ge=0)
    agreement_rate: float | None = Field(ge=0, le=1)
    disagreements: list[AgreementSampleResult]


class SerialPortOut(BaseModel):
    device: str = Field(description='Nome do sistema, ex.: "COM5"')
    description: str | None
    hwid: str | None
    in_use: bool = Field(description="É a porta que a bancada está usando agora")


# ---------------------------------------------------------------- product configuration


class RoiOut(BaseModel):
    """Inspection window as a fraction (0..1) of the camera frame, origin at the top-left.

    Set here as a starting point for training; the value a model actually uses is the one baked
    into its package (training/__main__.py --roi), so changing this does not affect a model
    already trained — only the next one."""

    x: float = Field(ge=0, lt=1)
    y: float = Field(ge=0, lt=1)
    width: float = Field(gt=0, le=1)
    height: float = Field(gt=0, le=1)

    @model_validator(mode="after")
    def _fits_the_frame(self) -> Self:
        if self.x + self.width > 1:
            raise ValueError("x + width deve ser no máximo 1")
        if self.y + self.height > 1:
            raise ValueError("y + height deve ser no máximo 1")
        return self


class ProductConfigOut(BaseModel):
    product: ProductOut
    bench: ConfigurePayload = Field(description="Tempos e posições da bancada")
    bench_is_default: bool = Field(
        description="Ainda não calibrado: valores de partida da bancada simulada. No modo real a "
        "bancada só arma depois que uma calibração for salva"
    )
    roi: RoiOut | None = Field(description="Janela de inspeção; nulo usa o quadro inteiro")
    editable: bool
    locked_reason: str | None = Field(description="Por que não pode ser alterado agora")


class ProductConfigUpdate(_In):
    expected_version: int = Field(ge=1, description="Versão lida; outra versão → CONFLICT")
    presentation: Annotated[str, StringConstraints(strip_whitespace=True, max_length=60)] | None = (
        None
    )
    # Same range the training searches when calibrating (training/evaluate.py).
    decision_threshold: float = Field(ge=0.4, le=0.99)
    bench: ConfigurePayload
    roi: RoiOut | None = None


# ---------------------------------------------------------------- maintenance


class MotorTestRequest(_In):
    request_id: UUID
    run_ms: int = Field(ge=100, le=5_000, description="Tempo com o motor ligado")


class ServoTestRequest(_In):
    request_id: UUID
    angle_deg: int = Field(ge=0, le=180)
    hold_ms: int = Field(ge=0, le=5_000, description="Tempo na posição antes de voltar ao repouso")


# ---------------------------------------------------------------- housekeeping (backup, limpeza)


class PurgeOut(BaseModel):
    purged: int = Field(ge=0, description="Inspeções cuja foto foi apagada")
    freed_bytes: int = Field(ge=0)


class BackupOut(BaseModel):
    name: str = Field(description="Nome do arquivo em backups/")
    size_bytes: int = Field(ge=0)
    created_at: AwareDatetime
    inspections: int = Field(ge=0, description="Inspeções registradas no banco incluído")
    dataset_photos: int = Field(ge=0, description="Fotos de coleta incluídas")
