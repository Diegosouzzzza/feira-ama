from fastapi import APIRouter, Response

from amazonvision.core.clock import utc_now
from amazonvision.routes.deps import ServicesDep
from amazonvision.routes.inspections import FiltersDep
from amazonvision.services import inspection_csv
from amazonvision.storage.inspections import export_rows

router = APIRouter(prefix="/exports", tags=["exportação"])


@router.get(
    "/inspections.csv",
    response_class=Response,
    responses={200: {"content": {"text/csv": {}}}},
)
async def inspections_csv(services: ServicesDep, filters: FiltersDep) -> Response:
    """Histórico em CSV (UTF-8 com BOM, separador ";"), com os mesmos filtros da listagem."""
    rows = await services.db.run(lambda conn: export_rows(conn, filters))
    body = inspection_csv.render(rows)
    name = f"inspecoes-{utc_now().astimezone():%Y%m%d-%H%M}.csv"
    return Response(
        body,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )
