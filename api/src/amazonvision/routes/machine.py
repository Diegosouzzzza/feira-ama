from fastapi import APIRouter

from amazonvision.routes.deps import ControlDep, ServicesDep
from amazonvision.schemas.api import MachineCommandRequest, MachineCommandResult

router = APIRouter(prefix="/machine", tags=["máquina"])


@router.post("/start", response_model=MachineCommandResult)
async def start(
    body: MachineCommandRequest, services: ServicesDep, grant: ControlDep
) -> MachineCommandResult:
    """Arma (se preciso) e liga a operação automática: um ciclo após o outro."""
    result = await services.coordinator.execute("start", body.request_id, body.expected_state)
    if not result.duplicate:
        await services.record("MACHINE_START", data={"operator": grant.operator})
    return result


@router.post("/pause", response_model=MachineCommandResult)
async def pause(
    body: MachineCommandRequest, services: ServicesDep, grant: ControlDep
) -> MachineCommandResult:
    """Termina o ciclo já autorizado e não inicia o próximo."""
    result = await services.coordinator.execute("pause", body.request_id, body.expected_state)
    if not result.duplicate:
        await services.record("MACHINE_PAUSE", data={"operator": grant.operator})
    return result


@router.post("/stop", response_model=MachineCommandResult)
async def stop(
    body: MachineCommandRequest, services: ServicesDep, grant: ControlDep
) -> MachineCommandResult:
    """Parada por software imediata: interrompe o ciclo e desarma."""
    result = await services.coordinator.execute("stop", body.request_id, body.expected_state)
    if not result.duplicate:
        await services.record("MACHINE_STOP", data={"operator": grant.operator})
    return result


@router.post("/rearm", response_model=MachineCommandResult)
async def rearm(
    body: MachineCommandRequest, services: ServicesDep, grant: ControlDep
) -> MachineCommandResult:
    """Limpa a falha e arma de novo, sem iniciar movimento."""
    result = await services.coordinator.execute("rearm", body.request_id, body.expected_state)
    if not result.duplicate:
        await services.record("MACHINE_REARM", data={"operator": grant.operator})
    return result
