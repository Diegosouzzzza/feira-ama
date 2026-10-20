from typing import Annotated

from fastapi import APIRouter, Query, status
from fastapi.responses import FileResponse

from amazonvision.routes.deps import ControlDep, ServicesDep
from amazonvision.schemas.api import BackupOut, PurgeOut

router = APIRouter(tags=["manutenção"])


@router.post("/backups", response_model=BackupOut, status_code=status.HTTP_201_CREATED)
async def create_backup(services: ServicesDep, grant: ControlDep) -> BackupOut:
    """Gera um .zip com o banco (cópia consistente), as fotos, os modelos e a coleta."""
    backup = await services.backups.create()
    await services.record(
        "BACKUP_CREATED",
        data={"name": backup.name, "size_bytes": backup.size_bytes, "operator": grant.operator},
    )
    return backup


@router.get("/backups", response_model=list[BackupOut])
async def list_backups(services: ServicesDep) -> list[BackupOut]:
    return await services.backups.list()


@router.get(
    "/backups/{name}/file",
    response_class=FileResponse,
    responses={200: {"content": {"application/zip": {}}}},
)
async def download_backup(name: str, services: ServicesDep) -> FileResponse:
    path = services.backups.file_path(name)
    return FileResponse(path, media_type="application/zip", filename=name)


@router.delete("/backups/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_backup(name: str, services: ServicesDep, grant: ControlDep) -> None:
    services.backups.file_path(name)  # 404 before recording an event for nothing
    await services.backups.delete(name)
    await services.record("BACKUP_DELETED", data={"name": name, "operator": grant.operator})


@router.post("/images/purge", response_model=PurgeOut)
async def purge_images(
    services: ServicesDep,
    grant: ControlDep,
    max_age_days: Annotated[
        int | None, Query(ge=1, description="Padrão: AV_IMAGE_RETENTION_DAYS")
    ] = None,
) -> PurgeOut:
    """Apaga fotos de inspeções antigas (lote já encerrado); o registro no banco é mantido."""
    return await services.retention.purge_old_images(
        max_age_days=max_age_days, operator=grant.operator
    )
