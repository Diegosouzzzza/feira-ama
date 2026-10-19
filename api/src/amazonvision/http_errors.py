import logging
import uuid
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from starlette.exceptions import HTTPException

from amazonvision.schemas.errors import ApiError, ApiErrorBody, ErrorCode
from amazonvision.web import is_api_path

log = logging.getLogger("amazonvision.http")

ERROR_RESPONSES: dict[int | str, dict[str, Any]] = {
    "4XX": {"model": ApiErrorBody, "description": "Erro da requisição"},
    "5XX": {"model": ApiErrorBody, "description": "Erro do serviço ou de um equipamento"},
}

_STATUS_CODES: dict[int, ErrorCode] = {
    404: ErrorCode.NOT_FOUND,
    409: ErrorCode.CONFLICT,
    422: ErrorCode.VALIDATION_ERROR,
}


def _respond(
    status: int, code: ErrorCode, message: str, recovery: str | None = None
) -> JSONResponse:
    body = ApiErrorBody(
        code=code, message=message, recovery=recovery, trace_id=uuid.uuid4().hex[:12]
    )
    return JSONResponse(status_code=status, content=body.model_dump(mode="json"))


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApiError)
    async def _api_error(_: Request, exc: ApiError) -> JSONResponse:
        return _respond(exc.status_code, exc.code, exc.message, exc.recovery)

    @app.exception_handler(RequestValidationError)
    async def _validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        first = exc.errors()[0] if exc.errors() else {"loc": (), "msg": "inválido"}
        where = ".".join(str(p) for p in first["loc"] if p != "body") or "requisição"
        return _respond(422, ErrorCode.VALIDATION_ERROR, f"Dados inválidos em '{where}'.")

    @app.exception_handler(HTTPException)
    async def _http(request: Request, exc: HTTPException) -> Response:
        spa = getattr(request.app.state, "spa", None)
        if (
            exc.status_code == 404
            and spa is not None
            and request.method in ("GET", "HEAD")
            and not is_api_path(request.url.path)
        ):
            return spa.response_for(request.url.path)
        code = _STATUS_CODES.get(exc.status_code)
        if code is None:
            code = (
                ErrorCode.INTERNAL_ERROR if exc.status_code >= 500 else ErrorCode.VALIDATION_ERROR
            )
        message = (
            "Recurso não encontrado." if code is ErrorCode.NOT_FOUND else "Requisição recusada."
        )
        return _respond(exc.status_code, code, message)

    @app.exception_handler(Exception)
    async def _unexpected(request: Request, exc: Exception) -> JSONResponse:
        response = _respond(
            500,
            ErrorCode.INTERNAL_ERROR,
            "Erro interno do serviço.",
            "Tente de novo; se persistir, consulte o diagnóstico.",
        )
        log.exception("erro não tratado em %s %s", request.method, request.url.path)
        return response
