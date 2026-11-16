from enum import StrEnum

from pydantic import BaseModel, Field


class ErrorCode(StrEnum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    INVALID_STATE = "INVALID_STATE"
    CONTROL_LOCKED = "CONTROL_LOCKED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    CAMERA_UNAVAILABLE = "CAMERA_UNAVAILABLE"
    STALE_FRAME = "STALE_FRAME"
    MODEL_NOT_READY = "MODEL_NOT_READY"
    SERIAL_DISCONNECTED = "SERIAL_DISCONNECTED"
    SENSOR_TIMEOUT = "SENSOR_TIMEOUT"
    STORAGE_ERROR = "STORAGE_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


HTTP_STATUS: dict[ErrorCode, int] = {
    ErrorCode.VALIDATION_ERROR: 422,
    ErrorCode.NOT_FOUND: 404,
    ErrorCode.CONFLICT: 409,
    ErrorCode.INVALID_STATE: 409,
    ErrorCode.CONTROL_LOCKED: 423,
    ErrorCode.REVIEW_REQUIRED: 409,
    ErrorCode.CAMERA_UNAVAILABLE: 503,
    ErrorCode.STALE_FRAME: 503,
    ErrorCode.MODEL_NOT_READY: 503,
    ErrorCode.SERIAL_DISCONNECTED: 503,
    ErrorCode.SENSOR_TIMEOUT: 504,
    ErrorCode.STORAGE_ERROR: 507,
    ErrorCode.INTERNAL_ERROR: 500,
}


class ApiErrorBody(BaseModel):
    """Every non-2xx response from /api uses this body."""

    code: ErrorCode
    message: str = Field(description="Texto para o operador, em português, sem detalhes técnicos")
    recovery: str | None = Field(default=None, description="Ação sugerida ao operador")
    trace_id: str = Field(description="Identificador para localizar o erro nos logs")


class ApiError(Exception):
    def __init__(self, code: ErrorCode, message: str, recovery: str | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.recovery = recovery

    @property
    def status_code(self) -> int:
        return HTTP_STATUS[self.code]
