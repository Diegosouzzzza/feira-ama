# ADR 0006 — Núcleo da API

Data: 2026-10-18 · Situação: aceita

## Decisões

1. **Uma conexão SQLite servida por uma thread dedicada** (`storage/db.py`). Toda leitura e escrita passa por ela: há exatamente um gravador e o loop assíncrono nunca bloqueia. Transações curtas com `BEGIN IMMEDIATE`.
2. **Falha de banco é persistente até reiniciar.** Um erro de armazenamento marca o banco como não saudável, o status mostra `storage.status = "error"` e os próximos ciclos poderão ser bloqueados (Bloco 4). Um sucesso posterior não esconde a falha.
3. **Pasta de dados por modo**: `%LOCALAPPDATA%\AmazonVision\simulado` e `...\real`. Ensaio nunca compartilha banco com operação real. O campo `is_simulated` do lote continua como segunda proteção.
4. **Controle de operador em memória**, token aleatório de 24 bytes, expiração de 30 min sem uso (renovação a cada uso), tomada explícita (`takeover`) registrada como aviso. Reiniciar o serviço libera o controle, o que é aceitável numa estação única.
5. **Barramento de eventos no próprio processo**, com `seq` e `state_version`. Cada cliente WebSocket tem uma fila limitada; cliente lento é desconectado para ressincronizar, em vez de atrasar os outros.
6. **Snapshot sem condição de corrida**: `seq` e `state_version` são capturados *antes* de ler o estado; eventos publicados durante a leitura chegam depois, com `seq` maior.
7. **Proteção local**: `TrustedHostMiddleware` (só `127.0.0.1`, `localhost`, `[::1]`) e verificação de `Origin` no WebSocket.
8. **Logs** no console e em JSON Lines com rotação (5 × 5 MB) em `<dados>\logs\amazonvision.jsonl`, configurados no início do app (funciona também com `--reload`).
9. **Equipamentos ausentes são reportados como ausentes**: até os Blocos 4, 7 e 8, o status mostra placa desconectada, câmera indisponível e modelo não carregado, nunca um estado inventado.
