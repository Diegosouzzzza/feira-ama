from typing import Annotated

from fastapi import APIRouter, Query, status

from amazonvision.routes.deps import ServicesDep
from amazonvision.schemas.api import (
    AgreementLabelCreate,
    AgreementLabelOut,
    AgreementQueueItem,
    AgreementSummary,
    CollectionTag,
    PersonName,
    ProductId,
)
from amazonvision.schemas.errors import ApiError, ErrorCode

router = APIRouter(prefix="/dataset/agreement", tags=["coleta"])


@router.post("/labels", response_model=AgreementLabelOut, status_code=status.HTTP_201_CREATED)
async def submit_label(body: AgreementLabelCreate, services: ServicesDep) -> AgreementLabelOut:
    """Registra o rótulo de um revisor para uma foto nesta rodada, sem expor o de outro revisor.

    Não exige o controle da estação: é uma atividade separada da operação da bancada."""
    return await services.agreement.submit(body)


@router.get("/next", response_model=AgreementQueueItem | None)
async def next_photo(
    services: ServicesDep,
    product_id: Annotated[ProductId, Query()],
    session: Annotated[CollectionTag, Query()],
    reviewer: Annotated[PersonName, Query()],
) -> AgreementQueueItem | None:
    """Próxima foto que este revisor ainda não rotulou nesta rodada; nulo quando acabou."""
    return await services.agreement.next(product_id=product_id, session=session, reviewer=reviewer)


@router.get("/summary", response_model=AgreementSummary)
async def summary(
    services: ServicesDep,
    product_id: Annotated[ProductId, Query()],
    session: Annotated[CollectionTag, Query()],
) -> AgreementSummary:
    """Compara os rótulos: só faz sentido olhar depois que todos os revisores terminarem."""
    result = await services.agreement.summary(product_id=product_id, session=session)
    if len(result.reviewers) < 2:
        raise ApiError(
            ErrorCode.INVALID_STATE,
            "Ainda não há duas pessoas rotulando nesta rodada.",
            "Peça para uma segunda pessoa rotular as mesmas fotos antes de ver o resumo.",
        )
    return result
