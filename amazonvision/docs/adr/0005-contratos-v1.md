# ADR 0005 — Contratos v1 (protocolo, API, banco)

Data: 2026-10-18 · Situação: aceita

## Decisões

1. **Códigos em inglês no fio e no banco** (`READY`, `APPROVED`, `S1_TIMEOUT`…), textos para o operador em português. Evita traduções divergentes entre firmware, API e interface.
2. **ESP32 é dono do estado físico.** A tabela de transições (`docs/maquina-de-estados.md`) é única para firmware e simulador e é testada contra o código.
3. **B e C vão para a mesma saída (rejeitados)**, mas continuam separados no banco e na tela. Configurável por perfil (`QualityPolicy.destinations`). Pendência 5 tratada como proposta aceita até a equipe dizer o contrário.
4. **Inconclusivo não é classe.** Abaixo do limiar, empate no topo ou imagem inválida → `REVIEW`; a placa fica em `REVIEW_HOLD` até o operador decidir.
5. **Previsão original imutável.** Correções entram como revisões (somente acréscimo).
6. **SQLite local, sem Docker.** Um processo e um gravador; nenhum serviço extra para iniciar na feira. Migração para PostgreSQL só se houver várias máquinas.
7. **SPA servida como fallback de 404** fora de `/api`, sem rota "pega-tudo", para que nenhuma rota de API seja sombreada.
8. **Esquemas publicados antes das rotas** (`openapi.py`), para o `web/` gerar tipos já agora.

## Valores provisórios

- Limiar de decisão 0,80 nos dois perfis: recalibrar na validação (Bloco 8).
- Prazos do protocolo (heartbeat 500/1000 ms, resposta 300 ms): confirmar na bancada (Bloco 6).
