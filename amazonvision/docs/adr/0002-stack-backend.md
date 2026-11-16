# ADR 0002 — Stack do backend

Data: 2026-10-18 · Situação: aceita

## Decisão

| Uso | Escolha |
|---|---|
| Linguagem | Python 3.12 (`requires-python = ">=3.12,<3.13"`) |
| Dependências | uv, com `uv.lock` versionado |
| Servidor | FastAPI + Uvicorn, **um único worker** (dono único da câmera e da serial) |
| Configuração | pydantic-settings, prefixo `AV_`, arquivo `.env` opcional |
| Testes e lint | pytest + httpx2 (TestClient), Ruff |
| Inferência (a partir do Bloco 8) | ONNX Runtime; treino em PyTorch e exportação para ONNX |
| Banco (a partir do Bloco 3) | SQLite em WAL, migrações SQL numeradas |

## Por que Python e não Node no backend

O treinamento só é viável em Python (PyTorch, torchvision, scikit-learn). Manter o backend na mesma linguagem permite compartilhar o pré-processamento entre treino e operação e evita um segundo serviço só para a inferência.

## Observações

- `httpx` foi trocado por `httpx2` porque o Starlette atual emite aviso de depreciação com o `httpx`.
- O esquema OpenAPI é exportado com `uv run amazonvision --dump-openapi openapi.json` e versionado, para gerar os tipos do `web/`.
