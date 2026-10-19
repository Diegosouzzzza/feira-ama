# ADR 0001 — Estrutura do repositório: api/ e web/

Data: 2026-10-18 · Situação: aceita

## Contexto

A especificação propunha `amazonvision/app`, `web/`, `training/` etc. A regra da equipe é separar sempre backend e frontend, com os nomes `api/` e `web/`.

## Decisão

- `api/`: todo o backend Python, **incluindo o treinamento** (`api/training/`), para que treino e operação usem o mesmo código de pré-processamento de imagem.
- `web/`: todo o frontend.
- `firmware/`, `docs/` e `scripts/` como pastas irmãs.
- O repositório fica fora do OneDrive (`C:\dev\amazonvision`) para evitar sincronização de `.venv`, `node_modules` e banco aberto.
- Dados de execução em `%LOCALAPPDATA%\AmazonVision`, nunca no Git.

## Consequências

Um único processo Python serve a API e a interface compilada. Na feira, o Node não é necessário.
