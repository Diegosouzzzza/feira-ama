# AmazonVision 4.0

Esteira seletora com inspeção visual de qualidade (tucumã e castanha-do-pará), controlada por ESP32, com IA local e painel para a Feira Tecnológica FUCAPI 2026.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `api/` | Backend: serviço local em Python (FastAPI), coordenação da bancada, visão, banco e treinamento |
| `web/` | Frontend: painel em React + TypeScript (Vite, Tailwind, shadcn/ui) |
| `firmware/` | Programa do ESP32 (PlatformIO, framework Arduino) |
| `docs/` | Decisões (ADR), protocolo, calibração, operação |
| `scripts/` | Inicialização, testes e verificação do ambiente (PowerShell) |

Dados de execução (banco, imagens, modelos, logs, backups) ficam fora do repositório, em `%LOCALAPPDATA%\AmazonVision`.

## Requisitos de desenvolvimento

- Python 3.12 e [uv](https://docs.astral.sh/uv/) (`python -m pip install --user uv`)
- Node 22+ e pnpm (somente para desenvolver o `web/`; não é usado na feira)
- PlatformIO (`uv tool install platformio`)

Confira tudo com:

```powershell
.\scripts\verificar-ambiente.ps1
```

## Uso

| Objetivo | Comando | Endereço |
|---|---|---|
| Desenvolver (recarga automática) | `.\scripts\dev.ps1` | http://127.0.0.1:5173 |
| Rodar como na feira | `.\scripts\iniciar.ps1` | http://127.0.0.1:8000 |
| Lint e testes de tudo | `.\scripts\testar.ps1` | — |
| Documentação da API | (com a API rodando) | http://127.0.0.1:8000/api/docs |

### Tipos da API no frontend

Os tipos TypeScript são gerados a partir do backend. Depois de mudar rotas ou esquemas no `api/`:

```powershell
cd api;  uv run amazonvision --dump-openapi openapi.json
cd ..\web; pnpm gen:api
```

### Firmware

```powershell
cd firmware
pio run                 # compilar
pio run -t upload       # gravar no ESP32
pio device monitor      # monitor serial (115200)
```

## Situação

Bloco 1 (fundação) concluído. Plano completo e auditoria: `Plano_Inicio_Projeto_AmazonVision.md` na pasta da feira. Decisões em `docs/adr/`, pendências em `docs/pendencias.md`.
