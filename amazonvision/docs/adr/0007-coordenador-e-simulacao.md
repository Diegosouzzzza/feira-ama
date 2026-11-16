# ADR 0007 — Coordenador do ciclo e bancada simulada

Data: 2026-10-18 · Situação: aceita

## Decisões

1. **A placa simulada fala o mesmo protocolo e segue a mesma tabela de estados** do firmware (`machine/simulated_device.py`). O coordenador não sabe se do outro lado há um ESP32 ou o simulador: troca-se só o `Link` (serial no Bloco 6).
2. **Física simulada acelerável** (`AV_SIM_SPEED`): percursos, estabilização, separação, liberação e os prazos físicos (S1, S2, saída) são divididos pela velocidade. Prazos de **comunicação** (decisão, heartbeat) nunca são acelerados, para os testes não esconderem problemas de latência.
3. **Injeção de falhas no simulador**: S1/S2 ausentes, saída bloqueada, eventos duplicados, placa muda, reinício (novo `boot_id`), emergência. As entradas físicas (S1, S2, emergência) sobrevivem a um reinício, como na bancada real.
4. **Cenário compartilhado** (`simulation/scenario.py`): a câmera simulada desenha o item planejado e o classificador stub devolve os scores do mesmo item, então imagem e previsão são coerentes. As imagens são PNG sintéticos gerados em Python puro, claramente artificiais.
5. **Operação automática**: `start` mantém ciclos em sequência; o próximo `START_CYCLE` só sai depois de `CYCLE_COMPLETED`. Toda interrupção desliga a operação automática.
6. **Ordem na inspeção**: captura (quadro com horário ≥ `CAPTURE_READY`) → inferência numa thread dedicada → política → imagem gravada atomicamente → inspeção registrada → `INSPECTION_READY` → `DECISION` ou `HOLD_FOR_REVIEW`. Falha de câmera, modelo ou gravação para a bancada (`STOP`) e registra o motivo real no ciclo.
7. **Revisão move antes de registrar**: a decisão do operador é entregue à placa primeiro; só então a revisão é gravada. Assim, uma decisão registrada nunca deixa a peça parada na esteira.
8. **Nada é reaplicado**: placa reiniciada ou muda interrompe o ciclo no banco (`DEVICE_REBOOTED`/`DEVICE_SILENT`); a nova sessão começa desarmada e exige `rearm`. Decisões pendentes nunca são reenviadas.
9. **Ciclos órfãos**: ao iniciar o serviço, ciclos que ficaram `running` são marcados como `SERVICE_RESTARTED`.
10. **Silêncio da placa ≥ 1,5 s** (`AV_DEVICE_SILENCE_MS`, padrão 3 s): o heartbeat da placa é de 1 s; um limite menor faz uma placa parada em revisão parecer muda e interrompe o ciclo (defeito encontrado em teste em 2026-10-19 e bloqueado na validação da configuração).
11. **Status lê o ciclo atual antes dos totais**: o fim do ciclo é gravado antes de o coordenador soltá-lo, então "nenhum ciclo na esteira" garante totais atualizados.
12. **Idempotência dos comandos de máquina** em memória (últimos 256 `request_id`), suficiente para atualizar a página ou repetir um clique; um reinício do serviço zera o registro, e a máquina também volta desarmada.

## Evidências

- 16 testes do simulador contra o protocolo, 20 testes de ponta a ponta pela API (incluindo 100+ ciclos sem divergência entre banco, eventos e destino comandado), repetidos 3× sem instabilidade.
- Ciclo em velocidade real no navegador: ~5 s por peça, revisão de inconclusivo funcionando.
