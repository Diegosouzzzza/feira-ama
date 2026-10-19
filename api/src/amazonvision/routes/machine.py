from fastapi import APIRouter

from amazonvision.routes.deps import ControlDep, ServicesDep
from amazonvision.schemas.api import (
    MachineCommandRequest,
    MachineCommandResult,
    MotorTestRequest,
    ServoTestRequest,
)

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


@router.post("/maintenance/enter", response_model=MachineCommandResult)
async def maintenance_enter(
    body: MachineCommandRequest, services: ServicesDep, grant: ControlDep
) -> MachineCommandResult:
    """Modo manutenção: libera os testes manuais de motor e servo. Exige a esteira parada."""
    result = await services.coordinator.execute(
        "maintenance_enter", body.request_id, body.expected_state
    )
    if not result.duplicate:
        await services.record("MAINTENANCE_ENTER", data={"operator": grant.operator})
    return result


@router.post("/maintenance/exit", response_model=MachineCommandResult)
async def maintenance_exit(
    body: MachineCommandRequest, services: ServicesDep, grant: ControlDep
) -> MachineCommandResult:
    result = await services.coordinator.execute(
        "maintenance_exit", body.request_id, body.expected_state
    )
    if not result.duplicate:
        await services.record("MAINTENANCE_EXIT", data={"operator": grant.operator})
    return result


@router.post("/maintenance/test-motor", response_model=MachineCommandResult)
async def test_motor(
    body: MotorTestRequest, services: ServicesDep, grant: ControlDep
) -> MachineCommandResult:
    """Liga a esteira pelo tempo pedido (só em manutenção)."""
    result = await services.coordinator.execute(
        "test_motor", body.request_id, None, {"run_ms": body.run_ms}
    )
    if not result.duplicate:
        await services.record(
            "TEST_MOTOR", data={"operator": grant.operator, "run_ms": body.run_ms}
        )
    return result


@router.post("/maintenance/test-servo", response_model=MachineCommandResult)
async def test_servo(
    body: ServoTestRequest, services: ServicesDep, grant: ControlDep
) -> MachineCommandResult:
    """Move o servo ao ângulo pedido e volta ao repouso (só em manutenção)."""
    params = {"angle_deg": body.angle_deg, "hold_ms": body.hold_ms}
    result = await services.coordinator.execute("test_servo", body.request_id, None, params)
    if not result.duplicate:
        await services.record("TEST_SERVO", data={"operator": grant.operator, **params})
    return result
