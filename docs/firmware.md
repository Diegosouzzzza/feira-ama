# Firmware do ESP32

## Organização

| Parte | Onde | O que faz |
|---|---|---|
| Lógica | `firmware/lib/av_core/` | Máquina de estados (`av_machine`), protocolo (`av_protocol`) e controlador do ciclo (`av_controller`). C++17 puro, sem Arduino: compila no ESP32 e no PC. |
| Placa | `firmware/src/` | Serial, pinos, servo (LEDC) e drivers do motor (`motor_drivers.h`). Configuração em `board_config.h`. |
| Testes nativos | `firmware/test/native/` | `unit_tests.cpp` (relógio e sensores manuais) e `harness.cpp` (lógica real sobre uma esteira simulada, falando o protocolo por stdin/stdout). |
| Build nativo | `firmware/tools/build_native.py` | Compila os testes com o C++ do pacote `ziglang` (dependência de desenvolvimento do `api/`). |

O controlador não bloqueia: tudo avança em `tick(now_ms)`, chamado a cada ~1 ms. Comandos chegam por linha (`handle_line`).

## Pinos (provisórios)

Confirmar na montagem e atualizar esta tabela e `board_config.h`.

| Função | GPIO | Observação |
|---|---|---|
| Sensor S1 | 25 | Saída do PC817, ativa em nível baixo, pull-up interno |
| Sensor S2 | 26 | Igual ao S1 |
| Emergência (contato auxiliar) | 27 | Ativo em nível baixo; o botão corta a energia dos atuadores **por hardware** |
| Servo da pá | 18 | LEDC canal 0, 50 Hz, 500–2500 µs ↔ 0–180° |
| Motor, driver 1 (liga/desliga) | 19 | MOSFET de nível lógico ou módulo relé |
| Motor, driver 2 (BTS7960) | 21 RPWM, 22 LPWM, 23 EN | PWM 20 kHz só para frente |
| LED de estado | 2 | Aceso: pronto/ciclo; pisca lento: desarmada; pisca rápido: falha/emergência |

Evitar os pinos de *strapping* (0, 2\*, 12, 15) para entradas e os 34–39 (sem pull-up). \*O GPIO 2 é só saída de LED.

## Escolha do driver do motor

Definida em tempo de compilação por `AV_MOTOR_DRIVER` (pendência 2 de `docs/pendencias.md`):

```powershell
cd firmware
pio run                                              # driver 1 (padrão)
$env:PLATFORMIO_BUILD_FLAGS="-DAV_MOTOR_DRIVER=2"; pio run   # BTS7960
```

Um driver novo é uma classe que implementa `av::MotorDriver` em `src/motor_drivers.h`. O controlador só pede liga/desliga e, se o driver aceitar, uma potência (`motor_power_pct` do `CONFIGURE`).

## Gravar e acompanhar

```powershell
cd firmware
pio run -t upload
pio device monitor        # 115200; envie {"protocol_version":1,...} para testar à mão
```

Na inicialização a placa fica `DISARMED`, motor desligado e servo sem sinal até receber `CONFIGURE`. Nada se move sem `ARM` + `START_CYCLE`.

## Testes

Rodam junto com a suíte da API (`scripts/testar.ps1` ou `uv run pytest` em `api/`):

- **Unitários em C++** (16 casos): ciclo completo, filtro de ruído dos sensores, prazos, idempotência, perda de comunicação, emergência, rearme.
- **Tabela de estados** C++ comparada com a Python.
- **Contrato**: todos os exemplos de `docs/protocolo/exemplos` passam pela lógica real do firmware; cada linha que ela gera é validada pelo Pydantic do servidor.
- **Sistema**: a API completa opera o firmware nativo pelo harness (`ProcessLink`), com ciclos aprovados, rejeitados, revisão de inconclusivo, emergência, retirada de peça e reinício da placa.

Para usar o firmware nativo no lugar do simulador Python ao rodar a API (modo simulado):

```powershell
cd api
uv run python ..\firmware\tools\build_native.py harness
$env:AV_FIRMWARE_HARNESS='["../firmware/.pio/native/harness.exe","--belt-mm-s","200"]'
uv run amazonvision
```

## Ainda não validado

- Leitura real dos sensores PNP via PC817 (polaridade e filtro).
- Tempos e ângulos reais (calibração no Bloco 9).
- Driver do motor real e comportamento da esteira ao parar (inércia).
- Ensaio de 50 ciclos físicos e testes de falha na bancada (cabo USB, S2 ausente, emergência).
