from typing import Annotated

from fastapi import APIRouter, Path, Query, Response, status

from amazonvision.routes.deps import ControlDep, ServicesDep
from amazonvision.schemas.api import LotCreate, LotOut, LotSummary, ProductId

router = APIRouter(prefix="/lots", tags=["lotes"])

LotId = Annotated[int, Path(ge=1)]


@router.post(
    "",
    response_model=LotOut,
    status_code=status.HTTP_201_CREATED,
    responses={200: {"model": LotOut, "description": "Mesma solicitação repetida"}},
)
async def create_lot(
    body: LotCreate, services: ServicesDep, _: ControlDep, response: Response
) -> LotOut:
    lot, created = await services.lots.create(body)
    if created:
        # The product's model was loaded: a change outside the event stream.
        await services.resync_all()
    else:
        response.status_code = status.HTTP_200_OK
    return lot


@router.get("", response_model=list[LotOut])
async def list_lots(
    services: ServicesDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    product_id: ProductId | None = None,
) -> list[LotOut]:
    return await services.lots.list_lots(limit=limit, offset=offset, product_id=product_id)


@router.get("/{lot_id}", response_model=LotOut)
async def get_lot(lot_id: LotId, services: ServicesDep) -> LotOut:
    return await services.lots.get(lot_id)


@router.get("/{lot_id}/summary", response_model=LotSummary)
async def lot_summary(lot_id: LotId, services: ServicesDep) -> LotSummary:
    return await services.lots.summary(lot_id)


@router.post("/{lot_id}/close", response_model=LotOut)
async def close_lot(lot_id: LotId, services: ServicesDep, grant: ControlDep) -> LotOut:
    lot = await services.lots.close(lot_id, grant.operator)
    await services.resync_all()
    return lot
