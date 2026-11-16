from fastapi import APIRouter

from amazonvision.routes.deps import ControlDep, ServicesDep
from amazonvision.schemas.api import (
    ProductConfigOut,
    ProductConfigUpdate,
    ProductId,
    ProductOut,
    SystemStatus,
)
from amazonvision.storage.products import list_products

router = APIRouter(tags=["sistema"])


@router.get("/status", response_model=SystemStatus)
async def status(services: ServicesDep) -> SystemStatus:
    return await services.current_status()


@router.get("/products", response_model=list[ProductOut], tags=["produtos"])
async def products(services: ServicesDep) -> list[ProductOut]:
    return await services.db.run(list_products)


@router.get("/products/{product_id}/config", response_model=ProductConfigOut, tags=["produtos"])
async def product_config(product_id: ProductId, services: ServicesDep) -> ProductConfigOut:
    return await services.product_config.get(product_id)


@router.put("/products/{product_id}/config", response_model=ProductConfigOut, tags=["produtos"])
async def update_product_config(
    product_id: ProductId, body: ProductConfigUpdate, services: ServicesDep, grant: ControlDep
) -> ProductConfigOut:
    """Salva o perfil do produto. Vale a partir do próximo lote; recusado em operação."""
    config, changes = await services.product_config.update(product_id, body)
    if changes:
        await services.record(
            "CONFIG_CHANGED",
            data={"product_id": product_id, "operator": grant.operator, "changes": changes},
        )
    await services.resync_all()
    return config
