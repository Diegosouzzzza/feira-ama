# Máquina de estados da bancada — v1

Fonte de verdade em código: `api/src/amazonvision/domain/machine.py`. O firmware (ESP32) e o simulador implementam **esta** tabela. Um teste automático compara a tabela abaixo com o código; qualquer mudança precisa atualizar os dois.

O ESP32 é a autoridade sobre o estado físico. O computador só pede transições com comandos; quem decide se a transição acontece é o firmware.

## Estados

| Estado | Nome na tela | Motor | Servo | Descrição |
|---|---|---|---|---|
| `DISARMED` | Desarmada | parado | repouso | Estado inicial após ligar, parar ou resolver falha. Aceita configuração. Nunca se move sozinha. |
| `READY` | Pronta | parado | repouso | Armada e aguardando o pedido de um novo ciclo. |
| `TO_S1` | Levando à inspeção | ligado | repouso | Transporta a peça até o sensor S1. Se S1 já estiver ativo ao entrar, avança na hora. |
| `SETTLING` | Estabilizando | parado | repouso | Espera o tempo de estabilização; ao final, emite `CAPTURE_READY`. |
| `INSPECTING` | Analisando | parado | repouso | Aguarda a decisão do computador para o ciclo atual, com prazo. |
| `REVIEW_HOLD` | Aguardando revisão | parado | repouso | Resultado inconclusivo; espera a decisão do operador, sem prazo de decisão. |
| `TO_S2` | Levando à separação | ligado | repouso | Destino memorizado; transporta até o sensor S2. |
| `SORTING` | Separando | conforme destino | conforme destino | Executa a sequência do destino (desvio ou passagem). |
| `RELEASING` | Liberando | ligado | repouso | Leva a peça para fora e confirma que S1 e S2 ficaram livres. |
| `FAULT` | Falha | parado | repouso | Algo saiu do previsto. Exige `CLEAR_FAULT` (rearme explícito). |
| `ESTOP` | Emergência | sem energia | sem energia | Botão de emergência pressionado. Ao soltar, volta para `DISARMED`. |
| `MAINTENANCE` | Manutenção | por teste | por teste | Testes manuais de motor, servo e sensores. |

Grupos usados no código:

- **Estados de ciclo**: `TO_S1`, `SETTLING`, `INSPECTING`, `REVIEW_HOLD`, `TO_S2`, `SORTING`, `RELEASING`.
- **Estados com movimento**: `TO_S1`, `TO_S2`, `SORTING`, `RELEASING`.

## Gatilhos

| Gatilho | Origem | Significado |
|---|---|---|
| `HELLO` | computador | Nova sessão serial. Durante um ciclo, aborta o ciclo (`SESSION_REPLACED`). |
| `ARM` | computador | Armar a máquina (exige configuração válida, sensores livres e emergência solta). |
| `STOP` | computador | Parada por software: interrompe o ciclo e desarma. |
| `START_CYCLE` | computador | Inicia o ciclo informado (`cycle_id`). Recusado se S2 estiver ocupado. |
| `DECISION` | computador | Destino da peça do ciclo atual: `APPROVED` ou `REJECTED`. |
| `HOLD_FOR_REVIEW` | computador | Resultado inconclusivo: aguardar o operador. |
| `CLEAR_FAULT` | computador | Rearme após falha (recusado se a causa persistir). |
| `ENTER_MAINTENANCE` / `EXIT_MAINTENANCE` | computador | Entrar e sair do modo de testes. |
| `S1_PRESENT` / `S2_PRESENT` | sensor | Peça presente no ponto (após filtro de ruído). |
| `SETTLED` | tempo | Fim da estabilização. |
| `SORT_DONE` | tempo | Sequência de separação concluída. |
| `RELEASED` | tempo + sensores | Tempo de saída cumprido e sensores livres. |
| `TIMEOUT` | tempo | Prazo do estado esgotado (ver códigos de falha). |
| `LINK_LOST` | tempo | Sem heartbeat do computador dentro do prazo. |
| `ESTOP_PRESSED` / `ESTOP_RELEASED` | entrada de emergência | Botão de emergência. |

Prazos esgotados viram estes códigos de falha:

| Estado | Código |
|---|---|
| `TO_S1` | `S1_TIMEOUT` |
| `INSPECTING` | `DECISION_TIMEOUT` |
| `TO_S2` | `S2_TIMEOUT` |
| `RELEASING` | `EXIT_BLOCKED` |

Outros códigos de falha: `LINK_LOST`, `SESSION_REPLACED`, `SENSOR_CONFLICT` (sensor ativo onde não deveria), `INTERNAL`.

## Regras gerais

1. Qualquer gatilho que não esteja na tabela é **recusado** (`INVALID_STATE`) e não muda nada.
2. Entrar em `FAULT`, `ESTOP` ou `DISARMED` a partir de um estado de ciclo **aborta o ciclo** e emite `CYCLE_ABORTED`.
3. Nenhuma transição de saída de `DISARMED`, `FAULT` ou `ESTOP` liga o motor. Voltar a mover exige `ARM` e `START_CYCLE`.
4. Perder o computador com a máquina pronta (`READY`) apenas desarma; durante um ciclo gera falha.
5. A emergência física corta a energia dos atuadores por hardware; o estado `ESTOP` só registra e bloqueia comandos.

## Tabela de transições

| Estado | Gatilho | Próximo |
|---|---|---|
| `DISARMED` | `HELLO` | `DISARMED` |
| `DISARMED` | `ARM` | `READY` |
| `DISARMED` | `ENTER_MAINTENANCE` | `MAINTENANCE` |
| `DISARMED` | `ESTOP_PRESSED` | `ESTOP` |
| `READY` | `HELLO` | `DISARMED` |
| `READY` | `STOP` | `DISARMED` |
| `READY` | `START_CYCLE` | `TO_S1` |
| `READY` | `LINK_LOST` | `DISARMED` |
| `READY` | `ESTOP_PRESSED` | `ESTOP` |
| `TO_S1` | `HELLO` | `FAULT` |
| `TO_S1` | `STOP` | `DISARMED` |
| `TO_S1` | `S1_PRESENT` | `SETTLING` |
| `TO_S1` | `TIMEOUT` | `FAULT` |
| `TO_S1` | `LINK_LOST` | `FAULT` |
| `TO_S1` | `ESTOP_PRESSED` | `ESTOP` |
| `SETTLING` | `HELLO` | `FAULT` |
| `SETTLING` | `STOP` | `DISARMED` |
| `SETTLING` | `SETTLED` | `INSPECTING` |
| `SETTLING` | `LINK_LOST` | `FAULT` |
| `SETTLING` | `ESTOP_PRESSED` | `ESTOP` |
| `INSPECTING` | `HELLO` | `FAULT` |
| `INSPECTING` | `STOP` | `DISARMED` |
| `INSPECTING` | `DECISION` | `TO_S2` |
| `INSPECTING` | `HOLD_FOR_REVIEW` | `REVIEW_HOLD` |
| `INSPECTING` | `TIMEOUT` | `FAULT` |
| `INSPECTING` | `LINK_LOST` | `FAULT` |
| `INSPECTING` | `ESTOP_PRESSED` | `ESTOP` |
| `REVIEW_HOLD` | `HELLO` | `FAULT` |
| `REVIEW_HOLD` | `STOP` | `DISARMED` |
| `REVIEW_HOLD` | `DECISION` | `TO_S2` |
| `REVIEW_HOLD` | `LINK_LOST` | `FAULT` |
| `REVIEW_HOLD` | `ESTOP_PRESSED` | `ESTOP` |
| `TO_S2` | `HELLO` | `FAULT` |
| `TO_S2` | `STOP` | `DISARMED` |
| `TO_S2` | `S2_PRESENT` | `SORTING` |
| `TO_S2` | `TIMEOUT` | `FAULT` |
| `TO_S2` | `LINK_LOST` | `FAULT` |
| `TO_S2` | `ESTOP_PRESSED` | `ESTOP` |
| `SORTING` | `HELLO` | `FAULT` |
| `SORTING` | `STOP` | `DISARMED` |
| `SORTING` | `SORT_DONE` | `RELEASING` |
| `SORTING` | `LINK_LOST` | `FAULT` |
| `SORTING` | `ESTOP_PRESSED` | `ESTOP` |
| `RELEASING` | `HELLO` | `FAULT` |
| `RELEASING` | `STOP` | `DISARMED` |
| `RELEASING` | `RELEASED` | `READY` |
| `RELEASING` | `TIMEOUT` | `FAULT` |
| `RELEASING` | `LINK_LOST` | `FAULT` |
| `RELEASING` | `ESTOP_PRESSED` | `ESTOP` |
| `FAULT` | `HELLO` | `FAULT` |
| `FAULT` | `CLEAR_FAULT` | `DISARMED` |
| `FAULT` | `ESTOP_PRESSED` | `ESTOP` |
| `ESTOP` | `HELLO` | `ESTOP` |
| `ESTOP` | `ESTOP_RELEASED` | `DISARMED` |
| `MAINTENANCE` | `HELLO` | `DISARMED` |
| `MAINTENANCE` | `STOP` | `DISARMED` |
| `MAINTENANCE` | `EXIT_MAINTENANCE` | `DISARMED` |
| `MAINTENANCE` | `LINK_LOST` | `DISARMED` |
| `MAINTENANCE` | `ESTOP_PRESSED` | `ESTOP` |

## Fluxo normal de um ciclo

```text
DISARMED --ARM--> READY --START_CYCLE--> TO_S1 --S1_PRESENT--> SETTLING --SETTLED--> INSPECTING
   (CAPTURE_READY emitido; computador captura, classifica e decide)
INSPECTING --DECISION--> TO_S2 --S2_PRESENT--> SORTING --SORT_DONE--> RELEASING --RELEASED--> READY
   (CYCLE_COMPLETED emitido)

Inconclusivo:  INSPECTING --HOLD_FOR_REVIEW--> REVIEW_HOLD --DECISION (do operador)--> TO_S2
```
