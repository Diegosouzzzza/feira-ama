from amazonvision.config import RunMode
from amazonvision.domain.machine import FaultCode
from amazonvision.machine.protocol import ConfigurePayload
from amazonvision.schemas.errors import ApiError, ErrorCode

# Only for the simulated bench. Real values come from calibration (product bench_config_json).
SIMULATED_BENCH = ConfigurePayload(
    sensor_debounce_ms=20,
    s1_timeout_ms=15_000,
    settle_ms=400,
    decision_timeout_ms=5_000,
    s2_timeout_ms=8_000,
    servo_rest_deg=10,
    servo_reject_deg=75,
    reject_hold_ms=600,
    reject_motor_ms=800,
    release_ms=1_200,
    release_max_ms=4_000,
    link_timeout_ms=2_000,
)


def bench_config_for(mode: RunMode, bench_config_json: str | None) -> ConfigurePayload:
    if bench_config_json:
        return ConfigurePayload.model_validate_json(bench_config_json)
    if mode is RunMode.SIMULADO:
        return SIMULATED_BENCH
    raise ApiError(
        ErrorCode.INVALID_STATE,
        "A bancada ainda não foi calibrada para este produto.",
        "Calibre os tempos e posições na tela de configuração.",
    )


FAULT_TEXT: dict[FaultCode, tuple[str, str]] = {
    FaultCode.S1_TIMEOUT: (
        "A peça não chegou ao ponto de inspeção (S1) no prazo.",
        "Verifique se há peça na esteira e rearme a máquina.",
    ),
    FaultCode.DECISION_TIMEOUT: (
        "A decisão não chegou à máquina no prazo.",
        "Rearme a máquina.",
    ),
    FaultCode.S2_TIMEOUT: (
        "A peça não chegou ao ponto de separação (S2) no prazo.",
        "Verifique a esteira e rearme a máquina.",
    ),
    FaultCode.EXIT_BLOCKED: (
        "A saída da esteira continua ocupada.",
        "Retire a peça e rearme a máquina.",
    ),
    FaultCode.LINK_LOST: (
        "A placa perdeu a comunicação com o computador.",
        "Rearme a máquina.",
    ),
    FaultCode.SESSION_REPLACED: (
        "A conexão com a placa foi refeita durante um ciclo.",
        "Rearme a máquina.",
    ),
    FaultCode.SENSOR_CONFLICT: (
        "Um sensor ficou ativo em um momento inesperado.",
        "Retire peças sobre os sensores e rearme a máquina.",
    ),
    FaultCode.INTERNAL: (
        "Falha interna da placa.",
        "Reinicie a placa e rearme a máquina.",
    ),
}
