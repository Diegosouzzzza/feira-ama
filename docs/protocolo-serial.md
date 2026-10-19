# Protocolo serial computador ↔ ESP32 — v1

Fonte de verdade em código: `api/src/amazonvision/machine/protocol.py`. Exemplos de contrato em `docs/protocolo/exemplos/` (válidos e inválidos), usados nos testes da API e, a partir do Bloco 6, nos testes do firmware. A máquina de estados está em `docs/maquina-de-estados.md`.

## Camada física e enquadramento

| Item | Valor |
|---|---|
| Meio | USB serial (CDC/UART do DevKit) |
| Velocidade | 115200 baud, 8N1 |
| Abertura da porta | `dtr=False, rts=False` (evita reiniciar o ESP32) |
| Enquadramento | um objeto JSON compacto por linha, UTF-8, terminado em `\n` (`\r` é ignorado) |
| Tamanho máximo | 1024 bytes por linha, incluindo o `\n` |
| Imagens | **nunca** trafegam pela serial |

Linha acima do limite → `nak LINE_TOO_LONG`, descartada por inteiro. JSON inválido → `nak BAD_JSON` sem `cmd_id`.

## Identificadores

| Campo | Formato | Quem gera | Uso |
|---|---|---|---|
| `protocol_version` | `1` | ambos | Mensagem com outra versão → `nak UNSUPPORTED_VERSION` |
| `boot_id` | 8 hex minúsculos | ESP32, aleatório a cada inicialização | Detecta reinício da placa; invalida a sessão anterior |
| `session_id` | 8 hex minúsculos | computador, a cada conexão (`HELLO`) | Toda mensagem do computador carrega a sessão atual |
| `cmd_id` | 1–24 caracteres `[A-Za-z0-9_-]` | computador | Idempotência: o mesmo `cmd_id` nunca executa duas vezes |
| `seq` | inteiro 0…2³²−1 | ESP32, crescente por `boot_id` | Ordenação e descarte de duplicatas no computador |
| `lot_id`, `cycle_id` | inteiro ≥ 1 (IDs do banco) | computador | Amarram decisão e eventos à peça certa |

## Tipos de mensagem

### Computador → ESP32

| `type` | Uso |
|---|---|
| `cmd` | Comando (campo `name`); resposta obrigatória `ack` ou `nak` com o mesmo `cmd_id` |
| `hb` | Heartbeat do computador, a cada **500 ms**. Sem heartbeat por `link_timeout_ms` → gatilho `LINK_LOST` |

### ESP32 → computador

Toda mensagem do ESP32 carrega `boot_id`, `session_id` (ausente antes do primeiro `HELLO`), `seq` e `state` (estado atual após processar a mensagem).

| `type` | Uso |
|---|---|
| `ack` | Comando **aceito**. Não significa movimento concluído. Ecoa `cmd_id` e `name`. |
| `nak` | Comando **recusado**, com `code` e `detail` curto. Nada muda na máquina. |
| `evt` | Evento (campo `name`). |
| `hb` | Heartbeat do ESP32, a cada **1000 ms**, com o retrato dos sensores (`DeviceStatus`). Sem heartbeat por 3000 ms, o computador considera a placa desconectada. |

## Comandos

| `name` | Campos extras | Estados aceitos | Efeito |
|---|---|---|---|
| `HELLO` | — | todos | Adota o `session_id` da mensagem. Durante um ciclo, aborta (`SESSION_REPLACED`). `ack.payload.fw_version` |
| `CONFIGURE` | `payload` = parâmetros (abaixo) | `DISARMED`, `READY` | Valida e grava os parâmetros. `ack.payload.config_hash` |
| `ARM` | — | `DISARMED` | → `READY`. Exige configuração, S1/S2 livres e emergência solta (`PRECONDITION_FAILED`) |
| `STOP` | — | `READY`, ciclo, `MAINTENANCE` | Parada por software → `DISARMED`; aborta o ciclo com `STOP` |
| `START_CYCLE` | `lot_id`, `cycle_id` | `READY` | → `TO_S1`. Recusado se S2 estiver ocupado |
| `DECISION` | `cycle_id`, `payload.destination` | `INSPECTING`, `REVIEW_HOLD` | Memoriza o destino → `TO_S2`. `cycle_id` diferente → `CYCLE_MISMATCH` |
| `HOLD_FOR_REVIEW` | `cycle_id` | `INSPECTING` | → `REVIEW_HOLD` (sem prazo de decisão) |
| `CLEAR_FAULT` | — | `FAULT` | → `DISARMED`, se a causa não persistir |
| `ENTER_MAINTENANCE` / `EXIT_MAINTENANCE` | — | `DISARMED` / `MAINTENANCE` | Modo de testes manuais |
| `GET_STATUS` | — | todos | `ack.payload.status` com o retrato completo |
| `TEST_MOTOR` | `payload.run_ms` (1–5000) | `MAINTENANCE` | Liga o motor pelo tempo pedido |
| `TEST_SERVO` | `payload.angle_deg`, `payload.hold_ms` | `MAINTENANCE` | Move o servo e volta ao repouso |

Comando aceito em estado não listado → `nak INVALID_STATE`. Comando de teste fora da manutenção → `nak INVALID_STATE`.

### Parâmetros de `CONFIGURE`

Todos obrigatórios, exceto `motor_power_pct`. Os valores são **calibrados na bancada** por perfil de produto; não há padrão no firmware.

| Campo | Faixa | Significado |
|---|---|---|
| `sensor_debounce_ms` | 1–200 | Tempo estável para aceitar mudança de sensor |
| `s1_timeout_ms` | 500–30000 | Prazo de `TO_S1` |
| `settle_ms` | 0–5000 | Estabilização antes da captura |
| `decision_timeout_ms` | 500–30000 | Prazo de `INSPECTING` |
| `s2_timeout_ms` | 500–30000 | Prazo de `TO_S2` |
| `servo_rest_deg` / `servo_reject_deg` | 0–180, diferentes | Posições do servo (respeitar o limite mecânico real) |
| `reject_hold_ms` | 100–5000 | Tempo com a pá na posição de desvio |
| `reject_motor_ms` | 0–10000 | Motor ligado durante o desvio (0 se a pá empurra sozinha) |
| `release_ms` | 0–10000 | Motor ligado em `RELEASING` |
| `release_max_ms` | ≥ `release_ms`, até 30000 | Prazo para S1/S2 ficarem livres (`EXIT_BLOCKED`) |
| `link_timeout_ms` | 500–10000 | Prazo sem heartbeat do computador |
| `motor_power_pct` | 1–100, opcional | Só se o driver aceitar PWM; ausente = liga/desliga |

## Eventos (`evt`)

| `name` | `cycle_id` | `payload` | Quando |
|---|---|---|---|
| `STATE_CHANGED` | se houver ciclo | `from_state`, `to_state`, `trigger`, `fault?` | Toda transição |
| `SENSOR_CHANGED` | se houver ciclo | `sensor` (`S1`/`S2`/`ESTOP`), `active` | Mudança filtrada de entrada |
| `CAPTURE_READY` | obrigatório | — | Fim de `SETTLING`: a peça está parada sob a câmera |
| `CYCLE_COMPLETED` | obrigatório | `destination` | Fim de `RELEASING`: sequência executada para o destino comandado |
| `CYCLE_ABORTED` | obrigatório | `reason` (`STOP`, `ESTOP` ou código de falha) | Ciclo interrompido |
| `FAULT` | se houver ciclo | `code`, `detail?` | Entrada em `FAULT` |

`CYCLE_COMPLETED` informa **sequência concluída e destino comandado**. Sem sensor na saída, o sistema não afirma que a peça caiu no recipiente certo.

## Regras de confiabilidade

1. **Idempotência.** O ESP32 guarda os últimos 16 `cmd_id` com o resultado. Um `cmd_id` repetido recebe a mesma resposta com `duplicate: true` e **não executa de novo**.
2. **Sessão.** Antes do primeiro `HELLO` só são aceitos `HELLO` e `GET_STATUS` (`nak NO_SESSION`). Com sessão ativa, `session_id` diferente → `nak SESSION_MISMATCH`.
3. **Reinício.** Um `boot_id` novo significa que a placa reiniciou: o computador descarta a sessão, marca o ciclo em andamento como interrompido e refaz `HELLO` → `CONFIGURE`. **Nunca** reenvia decisões pendentes.
4. **Duplicatas de eventos.** O computador ignora mensagens com `(boot_id, seq)` já processado; contadores vêm do banco, nunca de incremento direto.
5. **Ordem de conexão.** `HELLO` → `CONFIGURE` → `ARM` (por ação do operador) → `START_CYCLE` por ciclo.
6. **Prazos no computador.** Resposta a comando: 300 ms (senão, reenvia o mesmo `cmd_id` até 3 vezes e depois marca a comunicação como falha).
7. **Nenhum comando livre.** Só existem os comandos desta tabela; a interface nunca envia texto arbitrário à placa.

## Sequência típica

```text
PC  → cmd HELLO (session_id=5e1a9c03)            ESP → ack HELLO {fw_version}
PC  → cmd CONFIGURE {…}                           ESP → ack CONFIGURE {config_hash}
PC  → cmd ARM                                     ESP → ack ARM;  evt STATE_CHANGED DISARMED→READY
PC  → cmd START_CYCLE lot 3, cycle 41             ESP → ack;      evt STATE_CHANGED READY→TO_S1
                                                  ESP → evt SENSOR_CHANGED S1 ativo; STATE_CHANGED → SETTLING
                                                  ESP → evt STATE_CHANGED → INSPECTING; evt CAPTURE_READY 41
PC  (captura, classifica, aplica a política)
PC  → cmd DECISION 41 REJECTED                    ESP → ack;      evt STATE_CHANGED → TO_S2 … SORTING … RELEASING
                                                  ESP → evt STATE_CHANGED → READY; evt CYCLE_COMPLETED 41 REJECTED
PC  (só depois de CYCLE_COMPLETED) → cmd START_CYCLE lot 3, cycle 42 …
```
