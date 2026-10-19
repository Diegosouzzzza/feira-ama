from fastapi import APIRouter, status

from amazonvision.core.control import ClaimOutcome
from amazonvision.routes.deps import ControlTokenHeader, ServicesDep
from amazonvision.schemas.api import ControlClaim, ControlGrant, Severity

router = APIRouter(prefix="/control", tags=["controle"])


@router.post("/claim", response_model=ControlGrant)
async def claim(
    body: ControlClaim, services: ServicesDep, token: ControlTokenHeader = None
) -> ControlGrant:
    grant, outcome, previous = services.control.claim(
        body.operator, takeover=body.takeover, token=token
    )
    if outcome != ClaimOutcome.RENEWED:
        await services.record(
            outcome,
            severity=Severity.WARNING if previous else Severity.INFO,
            data={"operator": grant.operator, "previous": previous},
        )
        await services.resync_all()
    return ControlGrant(token=grant.token, operator=grant.operator, expires_at=grant.expires_at)


@router.post("/release", status_code=status.HTTP_204_NO_CONTENT)
async def release(services: ServicesDep, token: ControlTokenHeader = None) -> None:
    operator = services.control.release(token)
    await services.record("CONTROL_RELEASED", data={"operator": operator})
    await services.resync_all()
