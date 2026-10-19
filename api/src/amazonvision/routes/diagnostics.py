from typing import Annotated

from fastapi import APIRouter, Query

from amazonvision.routes.deps import ServicesDep
from amazonvision.schemas.api import EventOut, EventSource, Severity
from amazonvision.storage.events import list_events

router = APIRouter(prefix="/diagnostics", tags=["diagnóstico"])


@router.get("/events", response_model=list[EventOut])
async def events(
    services: ServicesDep,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
    severity: Severity | None = None,
    source: EventSource | None = None,
    type: Annotated[
        str | None, Query(max_length=40, description="Ex.: FAULT, CONFIG_CHANGED")
    ] = None,
    lot_id: Annotated[int | None, Query(ge=1)] = None,
) -> list[EventOut]:
    return await services.db.run(
        lambda conn: list_events(
            conn,
            limit=limit,
            offset=offset,
            severity=severity,
            source=source,
            type=type,
            lot_id=lot_id,
        )
    )
