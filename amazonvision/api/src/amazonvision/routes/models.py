from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Query, Response, status
from fastapi.responses import PlainTextResponse

from amazonvision.routes.deps import ControlDep, ServicesDep
from amazonvision.schemas.api import ModelInstall, ModelOut, ModelValidationUpdate, ProductId
from amazonvision.schemas.errors import ApiError, ErrorCode

router = APIRouter(prefix="/models", tags=["modelos"])


@router.get("", response_model=list[ModelOut])
async def list_models(
    services: ServicesDep, product_id: Annotated[ProductId | None, Query()] = None
) -> list[ModelOut]:
    return await services.model_registry.list_models(product_id)


@router.post(
    "/install",
    response_model=ModelOut,
    status_code=status.HTTP_201_CREATED,
    responses={200: {"model": ModelOut, "description": "Pacote já instalado"}},
)
async def install(
    body: ModelInstall, services: ServicesDep, grant: ControlDep, response: Response
) -> ModelOut:
    """Instala um pacote gerado pelo treinamento (pasta com model.onnx e model.json)."""
    model, created = await services.model_registry.install(Path(body.path))
    if created:
        await services.record(
            "MODEL_INSTALLED", data={"model_id": model.id, "operator": grant.operator}
        )
    else:
        response.status_code = status.HTTP_200_OK
    return model


@router.post("/{model_id}/validation", response_model=ModelOut)
async def set_validation(
    model_id: str, body: ModelValidationUpdate, services: ServicesDep, _: ControlDep
) -> ModelOut:
    """Registra a decisão da equipe sobre o relatório do modelo."""
    model = await services.model_registry.set_validation(model_id, body.status, body.reviewer)
    await services.record(
        "MODEL_VALIDATION",
        data={"model_id": model_id, "status": body.status.value, "reviewer": body.reviewer},
    )
    return model


@router.post("/{model_id}/activate", response_model=ModelOut)
async def activate(model_id: str, services: ServicesDep, grant: ControlDep) -> ModelOut:
    """Torna o modelo o ativo do produto e adota o limiar calibrado na validação."""
    model = await services.model_registry.activate(model_id)
    await services.record(
        "MODEL_ACTIVATED", data={"model_id": model_id, "operator": grant.operator}
    )
    await services.resync_all()
    return model


@router.get("/{model_id}/report", response_class=PlainTextResponse)
async def report(model_id: str, services: ServicesDep) -> PlainTextResponse:
    path = services.model_registry.report_path(model_id)
    if path is None:
        raise ApiError(ErrorCode.NOT_FOUND, "Relatório não encontrado.")
    return PlainTextResponse(path.read_text(encoding="utf-8"), media_type="text/markdown")
