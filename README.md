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

Dados de execução (banco, imagens, modelos, logs, backups) ficam fora do repositório, em `%LOCALAPPDATA%\AmazonVision\<modo>` (`simulado` ou `real`, separados de propósito).

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

Blocos 1 a 5 concluídos: fundação, contratos, núcleo da API, coordenador do ciclo com bancada simulada e interface (tela de **Operação** em `/` e **Modo feira** em `/feira`). No modo simulado, o sistema executa ciclos completos de ponta a ponta pela tela.

Bloco 6 em andamento: a **lógica do firmware** está pronta e testada no PC contra o contrato e a API (ver `docs/firmware.md`); faltam a escolha do motor, a pinagem definitiva e os ensaios na bancada.

Bloco 7 (software) pronto: **câmera real** por OpenCV (`AV_CAMERA_SOURCE`, também no modo simulado) e **tela de Coleta** (`/coleta`) para fotografar, rotular, revisar e exportar o manifesto de treino (ver `docs/coleta.md` e `docs/manual-rotulagem.md`). Faltam a câmera definitiva e os critérios A/B/C da equipe.

Telas do Bloco 9 prontas no software: **Histórico** (`/historico`, filtros, foto, correção de decisão, distribuição por lote e CSV), **Configuração** (`/configuracao`, perfil e calibração da bancada por produto, com versão e registro) e **Diagnóstico** (`/diagnostico`, equipamentos, sensores ao vivo, modo manutenção com teste de motor e servo, registro de eventos). Falta a integração com a bancada real.

Bloco 8 (software) pronto: **pipeline de treinamento** (divisão por peça física, MobileNetV3, ONNX, limiar calibrado, relatório com parecer) e **tela de Modelos** para instalar, validar e ativar. Falta treinar com fotos reais (ver `docs/treinamento.md`).

Testes de navegador (Playwright, usa o Microsoft Edge instalado):

```powershell
cd web; pnpm test:e2e
``` Plano completo e auditoria: `Plano_Inicio_Projeto_AmazonVision.md` na pasta da feira. Decisões em `docs/adr/`, pendências em `docs/pendencias.md`.

| Contrato | Documento | Código |
|---|---|---|
| Máquina de estados | `docs/maquina-de-estados.md` | `api/src/amazonvision/domain/machine.py` |
| Protocolo serial | `docs/protocolo-serial.md` + `docs/protocolo/exemplos/` | `api/src/amazonvision/machine/protocol.py` |
| Política de qualidade | `docs/adr/0005-contratos-v1.md` | `api/src/amazonvision/domain/quality.py` |
| API REST, WebSocket e erros | `docs/api.md` | `api/src/amazonvision/schemas/` |
| Banco de dados | `docs/dados.md` | `api/src/amazonvision/storage/migrations/` |
