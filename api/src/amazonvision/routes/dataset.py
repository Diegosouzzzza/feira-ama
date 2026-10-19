from typing import Annotated

from fastapi import APIRouter, Query, status
from fastapi.responses import FileResponse

from amazonvision.domain.quality import Grade
from amazonvision.routes.deps import ControlDep, ServicesDep
from amazonvision.schemas.api import (
    CollectionTag,
    DatasetCapture,
    DatasetExport,
    DatasetExportOut,
    DatasetSampleOut,
    DatasetSamplePage,
    DatasetSampleUpdate,
    DatasetSummary,
    DbId,
    ProductId,
    SampleStatus,
)

router = APIRouter(prefix="/dataset", tags=["coleta"])


@router.post("/capture", response_model=DatasetSampleOut, status_code=status.HTTP_201_CREATED)
async def capture(
    body: DatasetCapture, services: ServicesDep, grant: ControlDep
) -> DatasetSampleOut:
    """Fotografa a peça parada sob a câmera e guarda a foto na coleta de treinamento."""
    return await services.dataset.capture(body, grant.operator)


@router.get("/samples", response_model=DatasetSamplePage)
async def list_samples(
    services: ServicesDep,
    product_id: Annotated[ProductId | None, Query()] = None,
    status: Annotated[SampleStatus | None, Query()] = None,
    label: Annotated[Grade | None, Query()] = None,
    physical_sample_id: Annotated[CollectionTag | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 60,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> DatasetSamplePage:
    return await services.dataset.list_samples(
        product_id=product_id,
        status=status,
        label=label,
        physical_sample_id=physical_sample_id,
        limit=limit,
        offset=offset,
    )


@router.get("/summary", response_model=DatasetSummary)
async def summary(
    services: ServicesDep, product_id: Annotated[ProductId, Query()]
) -> DatasetSummary:
    """Fotos e peças físicas por classe, comparadas com a meta de treinamento."""
    return await services.dataset.summary(product_id)


@router.patch("/samples/{sample_id}", response_model=DatasetSampleOut)
async def update_sample(
    sample_id: DbId, body: DatasetSampleUpdate, services: ServicesDep, grant: ControlDep
) -> DatasetSampleOut:
    """Rotula, corrige a classe ou separa a foto como ambígua ou inutilizável."""
    return await services.dataset.update(sample_id, body, grant.operator)


@router.get(
    "/samples/{sample_id}/image",
    response_class=FileResponse,
    responses={200: {"content": {"image/png": {}, "image/jpeg": {}}}},
)
async def sample_image(sample_id: DbId, services: ServicesDep) -> FileResponse:
    return FileResponse(await services.dataset.image_path(sample_id))


@router.post("/export", response_model=DatasetExportOut)
async def export(body: DatasetExport, services: ServicesDep, grant: ControlDep) -> DatasetExportOut:
    """Gera o manifesto CSV das fotos rotuladas, no formato lido pelo treinamento."""
    result = await services.dataset.export(body.product_id)
    await services.record(
        "DATASET_EXPORTED",
        data={"product_id": body.product_id, "photos": result.photos, "operator": grant.operator},
    )
    return result
