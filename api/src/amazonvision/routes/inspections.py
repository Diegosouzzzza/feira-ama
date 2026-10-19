from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Response, status
from fastapi.responses import FileResponse
from pydantic import AwareDatetime

from amazonvision.core.clock import to_db
from amazonvision.domain.quality import Grade
from amazonvision.routes.deps import ControlDep, ServicesDep
from amazonvision.schemas.api import (
    InspectionOut,
    InspectionOutcome,
    InspectionPage,
    InspectionReviewCreate,
    ProductId,
    ReviewOut,
)
from amazonvision.schemas.errors import ApiError, ErrorCode
from amazonvision.storage.images import resolve_image
from amazonvision.storage.inspections import (
    InspectionFilters,
    get_image_path,
    get_inspection,
    list_inspections,
)

router = APIRouter(prefix="/inspections", tags=["inspeções"])

InspectionId = Annotated[int, Path(ge=1)]
_MEDIA = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}


def _not_found() -> ApiError:
    return ApiError(ErrorCode.NOT_FOUND, "Inspeção não encontrada.")


def inspection_filters(
    lot_id: Annotated[int | None, Query(ge=1)] = None,
    product_id: Annotated[ProductId | None, Query()] = None,
    grade: Annotated[Grade | None, Query(description="Classe prevista pelo modelo")] = None,
    outcome: Annotated[InspectionOutcome | None, Query()] = None,
    captured_from: Annotated[AwareDatetime | None, Query(alias="from")] = None,
    captured_to: Annotated[AwareDatetime | None, Query(alias="to")] = None,
) -> InspectionFilters:
    if captured_from and captured_to and captured_to <= captured_from:
        raise ApiError(ErrorCode.VALIDATION_ERROR, "O fim do período deve ser depois do início.")
    return InspectionFilters(
        lot_id=lot_id,
        product_id=product_id,
        grade=grade,
        outcome=outcome,
        captured_from=to_db(captured_from) if captured_from else None,
        captured_to=to_db(captured_to) if captured_to else None,
    )


FiltersDep = Annotated[InspectionFilters, Depends(inspection_filters)]


@router.get("", response_model=InspectionPage)
async def list_inspections_route(
    services: ServicesDep,
    filters: FiltersDep,
    limit: Annotated[int, Query(ge=1, le=200)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> InspectionPage:
    """Mais recentes primeiro. Período em `from` (inclusive) e `to` (exclusivo)."""
    items, total = await services.db.run(
        lambda conn: list_inspections(conn, filters, limit=limit, offset=offset)
    )
    return InspectionPage(items=items, total=total, limit=limit, offset=offset)


@router.get("/{inspection_id}", response_model=InspectionOut)
async def inspection(inspection_id: InspectionId, services: ServicesDep) -> InspectionOut:
    found = await services.db.run(lambda conn: get_inspection(conn, inspection_id))
    if found is None:
        raise _not_found()
    return found


@router.get(
    "/{inspection_id}/image",
    response_class=FileResponse,
    responses={200: {"content": {"image/png": {}, "image/jpeg": {}}}},
)
async def inspection_image(inspection_id: InspectionId, services: ServicesDep) -> FileResponse:
    found = await services.db.run(lambda conn: get_image_path(conn, inspection_id))
    if found is None:
        raise _not_found()
    relative, purged = found
    path = None if purged else resolve_image(services.settings.data_root, relative)
    if path is None:
        raise ApiError(ErrorCode.NOT_FOUND, "Imagem não está mais disponível.")
    return FileResponse(
        path,
        media_type=_MEDIA.get(path.suffix.lstrip(".").lower(), "application/octet-stream"),
        headers={"Cache-Control": "private, max-age=31536000, immutable"},
    )


@router.post(
    "/{inspection_id}/review",
    response_model=ReviewOut,
    status_code=status.HTTP_201_CREATED,
    responses={200: {"model": ReviewOut, "description": "Mesma solicitação repetida"}},
)
async def review(
    inspection_id: InspectionId,
    body: InspectionReviewCreate,
    services: ServicesDep,
    _: ControlDep,
    response: Response,
) -> ReviewOut:
    """Decide uma peça inconclusiva ou corrige uma decisão anterior (sem apagar a previsão)."""
    result, created, delivered = await services.reviews.review(inspection_id, body)
    if not created:
        response.status_code = status.HTTP_200_OK
    else:
        await services.record(
            "REVIEW_RECORDED",
            data={
                "inspection_id": inspection_id,
                "decision": body.decision.value,
                "reviewer": body.reviewer,
                "delivered_to_machine": delivered,
            },
        )
    return result
