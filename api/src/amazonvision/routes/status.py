from fastapi import APIRouter

from amazonvision.routes.deps import ServicesDep
from amazonvision.schemas.api import ProductOut, SystemStatus
from amazonvision.storage.products import list_products

router = APIRouter(tags=["sistema"])


@router.get("/status", response_model=SystemStatus)
async def status(services: ServicesDep) -> SystemStatus:
    return await services.current_status()


@router.get("/products", response_model=list[ProductOut], tags=["produtos"])
async def products(services: ServicesDep) -> list[ProductOut]:
    return await services.db.run(list_products)
