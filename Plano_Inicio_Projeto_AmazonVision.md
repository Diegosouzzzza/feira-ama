# AmazonVision 4.0 — Auditoria, tecnologias e plano de início

Revisão: 18/10/2026. Base: `AmazonVision_4_0_Apresentacao_do_Projeto_v2.pdf`, `Lista_de_Materiais_AmazonVision.html` e a especificação completa (seções 1–24).

Regra de organização adotada: **todo o software segue a divisão backend/frontend, com as pastas `api/` (backend) e `web/` (frontend)**. Firmware e documentação ficam como pastas irmãs, porque não são nem uma coisa nem outra.

---

## Parte 1 — Auditoria

### 1.1 Situação da pasta

| Item | Existe? | Observação |
|---|---|---|
| PDF de apresentação | Sim | Fonte das funções e da arquitetura original |
| Especificação completa (.md) | Sim | Requisitos detalhados; boa base |
| Lista de materiais (HTML) | Sim | Checklist de compras |
| Bancada 3D / Prévia do painel (HTML) | Sim | Material de apresentação, não é sistema |
| Código do backend, frontend ou firmware | **Não** | Projeto começa do zero |
| Dataset, modelos treinados | **Não** | Coleta ainda não começou |
| Git | **Não** | Pasta não é repositório; está dentro do OneDrive |

### 1.2 O que a especificação acerta (manter)

- Classificação de imagem (não detecção) para uma peça parada por ciclo: correto e muito mais barato de rotular.
- ESP32 como autoridade do estado físico; computador decide e registra.
- Separar previsão do modelo, decisão operacional e revisão humana.
- "Inconclusivo" como estado de decisão, não como classe.
- Divisão do dataset por amostra física (evita vazamento entre treino e teste).
- Protocolo com `boot_id`, `session_id`, `command_id` para não reaplicar decisões antigas.
- Funcionamento 100% local e offline.

### 1.3 Problemas e conflitos encontrados

| # | Problema | Onde | Impacto | Correção adotada |
|---|---|---|---|---|
| A1 | **DRV8833 não serve para motor de 12 V.** O PDF (pág. 3, 8, 9) lista o DRV8833, mas ele trabalha até ~10,8 V e ~1,5 A por canal. A própria lista de materiais diz "para motor 12 V, não usar DRV8833". | PDF × lista de materiais | Driver queima ou não liga a esteira | Escolher driver depois de saber o motor: BTS7960 (IBT-2) para DC 12/24 V com reversão, ou módulo MOSFET (IRF520/IRLZ44N com lógica 3,3 V) se for só liga/desliga. Atualizar o PDF/apresentação. |
| A2 | **Estrutura de pastas da especificação** (`amazonvision/app`, `web/`, `training/`…) não segue a regra backend/frontend. | Espec. §17 | Organização divergente | Reorganizado em `api/` + `web/` (ver Parte 3). Treinamento vai **dentro de `api/`** para compartilhar o mesmo código de pré-processamento da inferência. |
| A3 | **Celular como câmera** ajusta exposição, foco e balanço de branco sozinho. Isso muda as imagens entre capturas e contamina o dataset. | PDF pág. 3–4 | IA aprende variação de câmera, não de qualidade | Recomendo **webcam USB UVC** (ex.: Logitech C920/C922) com exposição/foco/balanço travados via OpenCV. Celular fica como plano B (DroidCam por USB, nunca Wi-Fi da feira). Decidir **antes** de coletar. |
| A4 | **ESP32 reinicia ao abrir a porta serial** (sinais DTR/RTS do conversor USB). | Não citado | Cada reconexão do backend reinicia a máquina | Abrir porta com `dtr=False, rts=False`; tratar o reinício via `boot_id` mesmo assim. |
| A5 | **PyTorch na operação** exige CUDA, drivers e ~2–3 GB de dependências no notebook da feira. | Espec. §5 | Ponto de falha no dia | Treinar em PyTorch, **exportar para ONNX** e operar com **ONNX Runtime**. MobileNetV3 Small roda em poucos ms em CPU; GPU vira opcional. |
| A6 | **YOLO (Ultralytics)** é citado no PDF; a licença é AGPL-3.0. | PDF pág. 7 | Obrigações de licença se distribuído | Usar torchvision (BSD). Mencionar YOLO só como alternativa avaliada. |
| A7 | **Arduino IDE 2** não fixa versões de core e bibliotecas de forma reproduzível. | Espec. §5 | "Funciona na minha máquina" | **PlatformIO** com versões fixadas no `platformio.ini`. Arduino core continua sendo o framework. |
| A8 | **Sem simulador de bancada.** A espec. só cita "dados de ensaio separados". | Espec. §11 | Web e API ficam travadas esperando hardware | Criar **ESP32 simulado + câmera simulada + modelo stub** no backend, com o mesmo protocolo. Modo `SIMULADO` aparece de forma explícita na tela. |
| A9 | **Frame antigo no buffer**: OpenCV entrega frames enfileirados, não o atual. | Espec. §6, §11 | Foto não corresponde à peça | Thread de captura que guarda só o último frame com timestamp; inspeção só aceita frame com timestamp **posterior** ao fim da estabilização. |
| A10 | **Banco no OneDrive**: sincronização de SQLite aberto corrompe. | Espec. §10 | Perda de histórico | Dados em `%LOCALAPPDATA%\AmazonVision\`; backup consistente (API `sqlite3.backup`) para pasta sincronizada. |
| A11 | **Parada de emergência**: o PDF não tem; a lista marca como "Recomendado". | Lista de materiais | Risco físico na feira com público | Tornar **obrigatório**: botão NF cortando alimentação de motor e servo, com contato auxiliar lido pelo ESP32. |
| A12 | **Fluxo do "inconclusivo"** não diz o que acontece com a peça parada em S1. | Espec. §3, §8 | Máquina trava sem saída | Operador escolhe destino na tela (aprovar/rejeitar) → vira revisão humana registrada → ciclo continua. |
| A13 | **Três produtos no PDF × dois na espec.** (açaí ficou para depois). | PDF × espec. | Apresentação promete mais do que entrega | Perfis de produto 100% por configuração; açaí entra só com dataset e modelo. Ajustar o discurso da feira. |
| A14 | **Números de exemplo no PDF** (1.284 analisados, 96%, "deformação superficial") podem ser lidos como resultados. | PDF pág. 4, 10, 11 | Alegação sem evidência | Marcar como "ilustração" na apresentação; painel começa vazio. |
| A15 | **Data da feira não informada**. | — | Cronograma impossível | Pendência nº 1 do Bloco 1. |

### 1.4 Decisões pendentes (bloqueiam partes específicas)

| Pendência | Bloqueia | Prazo ideal |
|---|---|---|
| Data da feira e tamanho da equipe | Cronograma em dias | Bloco 1 |
| Motor da esteira (tensão, corrente, liga/desliga ou PWM) | Driver, firmware de acionamento | Antes do Bloco 6 |
| Webcam USB ou celular | Início da coleta de dados | Antes do Bloco 7 |
| Castanha com ou sem casca; critérios A/B/C | Rotulagem e treino | Antes do Bloco 7 |
| B e C na mesma saída (rejeitados) | Firmware e regras | Bloco 2 |
| Notebook da feira (Windows? GPU? RAM) | Pinagem de dependências | Bloco 1 |

---

## Parte 2 — Tecnologias escolhidas

### 2.1 Backend — `api/`

| Função | Tecnologia | Por quê |
|---|---|---|
| Linguagem | **Python 3.12** | Ecossistema de visão e IA; versão estável com suporte amplo |
| Ambiente e dependências | **uv** (`pyproject.toml` + `uv.lock`) | Lockfile real com hashes, instala offline a partir do cache, lida com o índice CUDA do PyTorch |
| Servidor HTTP/WebSocket | **FastAPI + Uvicorn** (1 worker) | WebSocket nativo, OpenAPI automático, validação via Pydantic |
| Validação e configuração | **Pydantic v2 + pydantic-settings** | Contratos da API, mensagens seriais e config `.env`/YAML |
| Captura | **OpenCV** (`opencv-python-headless`) | Backends DirectShow/MSMF no Windows; controle de exposição/foco |
| Inferência na operação | **ONNX Runtime** (CPU; DirectML/CUDA opcional) | Leve, sem depender de CUDA no dia da feira |
| Serial | **pySerial** | Timeout de leitura, controle de DTR/RTS |
| Banco | **SQLite (módulo `sqlite3`) em modo WAL** | Local, transacional, sem servidor |
| Migrações | **Arquivos SQL numerados + `PRAGMA user_version`** | Simples e auditável; sem ORM |
| Logs | **`logging` da stdlib em JSON Lines** | Sem dependência extra, fácil de anexar a relatórios |
| Testes | **pytest + pytest-asyncio + httpx** | Unidade, integração e contrato da API |
| Qualidade de código | **Ruff** (lint + format) + **mypy** (módulos de domínio) | Rápido, uma ferramenta só |

### 2.2 Treinamento — `api/training/`

| Função | Tecnologia |
|---|---|
| Treino | **PyTorch + torchvision** (CUDA na RTX), modelo **MobileNetV3 Small** pré-treinado; ResNet18 só se necessário |
| Avaliação | **scikit-learn** (matriz de confusão, precision/recall/F1, `StratifiedGroupKFold`/`GroupShuffleSplit`), **NumPy**, **Matplotlib** |
| Exportação | **torch.onnx** → `.onnx` + `model.json` (classes, resolução, normalização, hash, versão do dataset, métricas) |
| Verificação | Teste automático: saída ONNX ≈ saída PyTorch nas mesmas imagens |

O treino é um grupo de dependências separado (`uv sync --group training`). O notebook da feira instala só o grupo de operação.

### 2.3 Frontend — `web/`

| Função | Tecnologia | Por quê |
|---|---|---|
| Base | **React + TypeScript + Vite** | Seis telas com muitos estados; build estático servido pelo próprio FastAPI, **sem Node em produção** |
| Rotas | **React Router** | Operação, Feira, Histórico, Modelos, Coleta, Configuração, Diagnóstico |
| Dados HTTP | **TanStack Query** | Cache, paginação, estados de carregando/erro prontos |
| Estado em tempo real | **Zustand** alimentado pelo WebSocket | Snapshot + eventos incrementais, sem re-render global |
| Tipos da API | **openapi-typescript** gerado do `/openapi.json` | Web e API nunca divergem em silêncio |
| Estilo | **Tailwind CSS** com tokens da paleta AmazonVision em CSS variables | Consistência; tema único |
| Fonte | **Inter** empacotada localmente (`@fontsource`) | Offline; sem Google Fonts no dia |
| Gráficos | **Chart.js** via `react-chartjs-2` | Escolha da espec.; leve |
| Ícones | **lucide-react** | Sempre com rótulo |
| Componentes | **shadcn/ui** (Radix + Tailwind, código copiado no projeto) | Diálogos, abas, tabelas e toasts acessíveis e com acabamento profissional, personalizados com a paleta |
| Testes | **Vitest** (componentes/lógica) + **Playwright** (fluxos ponta a ponta contra o simulador) | |
| Gerenciador | **pnpm**, Node 22+ (apenas desenvolvimento) | |

TypeScript fixado na linha **6.x**: o TypeScript 7 (compilador nativo) ainda não é compatível com o openapi-typescript.

### 2.4 Firmware — `firmware/`

| Função | Tecnologia |
|---|---|
| Toolchain | **PlatformIO** (VS Code), `framework = arduino`, plataforma ESP32 fixada |
| Core | **Arduino-ESP32 2.0.17** via `espressif32@7.0.1` (linha estável oficial do PlatformIO; API LEDC clássica) |
| Protocolo | **ArduinoJson 7**, JSON por linha, 115200 baud |
| Servo | **ESP32Servo** (ou LEDC direto a 50 Hz) |
| Motor | Módulo próprio conforme o driver (BTS7960 / MOSFET / relé) |
| Testes | `pio test` em ambiente `native` para máquina de estados e parser |

### 2.5 Ferramentas gerais

Git (com `.gitignore` para dados/pesos), VS Code, GitHub (privado) para backup do código. Pesos e dataset **fora do Git**, versionados por hash em manifesto.

### 2.6 Fora do escopo inicial (P2)

- **Copiloto industrial**: API Claude com *tool use* restrito a consultas pré-definidas (nunca SQL livre, nunca comando de máquina). Exige internet → recurso opcional que não pode bloquear o ciclo.
- **Detecção de anomalias**: PatchCore/PaDiM via biblioteca Anomalib, só depois do classificador validado.

---

## Parte 3 — Estrutura do repositório

```text
amazonvision/
├─ api/                              ← BACKEND
│  ├─ pyproject.toml / uv.lock
│  ├─ src/amazonvision/
│  │  ├─ main.py                     app factory + lifespan (abre/fecha recursos)
│  │  ├─ config.py                   pydantic-settings; pasta de dados
│  │  ├─ core/                       barramento de eventos, erros, relógio, IDs
│  │  ├─ domain/                     enums, estados, política A/B/C → destino (puro, sem I/O)
│  │  ├─ camera/                     fonte OpenCV, fonte simulada (pasta de imagens), buffer do último frame
│  │  ├─ vision/                     preprocess.py (compartilhado com treino), classificador ONNX, stub
│  │  ├─ machine/                    protocolo, link serial, ESP32 simulado, coordenador do ciclo
│  │  ├─ storage/                    conexão, migrations/*.sql, repositórios, gravação de imagens
│  │  ├─ schemas/                    DTOs Pydantic da API
│  │  └─ routes/                     status, lots, machine, inspections, dataset, config, diagnostics, ws
│  ├─ training/                      manifesto, divisão por grupos, treino, avaliação, export ONNX
│  └─ tests/                         unit/, integration/, contract/
├─ web/                              ← FRONTEND
│  ├─ package.json / pnpm-lock.yaml / vite.config.ts
│  ├─ src/
│  │  ├─ app/                        rotas, layout, providers
│  │  ├─ pages/                      operacao, feira, historico, modelos, coleta, configuracao, diagnostico
│  │  ├─ components/                 design system (cartões, badges A/B/C, estados vazios/erro)
│  │  ├─ lib/api/                    cliente + tipos gerados do OpenAPI
│  │  ├─ lib/realtime/               WebSocket + store Zustand
│  │  └─ styles/tokens.css
│  └─ e2e/                           Playwright contra o modo simulado
├─ firmware/                         PlatformIO (src/, include/, lib/protocol/, test/)
├─ docs/                             protocolo-serial.md, api.md, calibracao.md, operacao.md, adr/
└─ scripts/                          dev.ps1, iniciar-feira.ps1, verificar-ambiente.ps1, backup.ps1
```

Dados em execução (fora do repositório e do OneDrive): `%LOCALAPPDATA%\AmazonVision\{db, images, models, logs, backups, dataset}`.

**Recomendo também mover o código para fora do OneDrive** (ex.: `C:\dev\amazonvision`). `node_modules` e `.venv` dentro do OneDrive geram sincronização pesada e travamentos de arquivo.

### Fluxo de execução do backend (um processo)

```text
Thread câmera ──► último frame + timestamp
Thread serial ──► fila asyncio ──► Coordenador (task asyncio, máquina de estados)
                                     ├─► Executor de inferência (1 thread, ONNX)
                                     ├─► Writer do banco (1 thread, transações curtas)
                                     └─► Barramento de eventos ──► WebSocket /api/events
HTTP /api/* ──► comandos validados ──► Coordenador
GET /api/camera/stream (MJPEG) ── canal separado das mensagens críticas
```

---

## Parte 4 — Plano de início em 10 blocos

Legenda de frentes: **[API]** backend · **[WEB]** frontend · **[FW]** firmware/eletrônica · **[IA]** dados e treino · **[INT]** integração.

Blocos 1–4 são sequenciais. Depois do Bloco 4, os Blocos **5, 6 e 7 andam em paralelo**.

---

### Bloco 1 — Fundação e decisões

> **Situação (18/10/2026):** parte técnica concluída em `C:\dev\amazonvision` (API com `/api/health`, web com shadcn/ui e tokens, firmware compilando, scripts, ADRs 0001–0004). Pendências da equipe em `docs/pendencias.md`, ainda abertas.

**Objetivo:** ambiente pronto e pendências críticas respondidas.

- Criar repositório Git (fora do OneDrive), `.gitignore`, `README`, estrutura de pastas da Parte 3.
- `api/`: `uv init`, Python 3.12, Ruff, pytest; app FastAPI mínimo com `GET /api/health`.
- `web/`: Vite + React + TS + Tailwind + Router; tela "olá" servida pelo FastAPI após `pnpm build`.
- `firmware/`: projeto PlatformIO compilando um *blink* + eco serial.
- `scripts/dev.ps1` sobe API (com reload) e Vite (com proxy para a API).
- Levantar o notebook da feira: Windows, GPU, RAM, portas USB.
- Responder pendências: data da feira, equipe, motor da esteira, webcam × celular, B/C na mesma saída.
- Registrar decisões em `docs/adr/` (uma página por decisão).

**Pronto quando:** `dev.ps1` sobe tudo, firmware grava no ESP32, pendências registradas (respondidas ou com data).

---

### Bloco 2 — Contratos

> **Situação (18/10/2026):** concluído. Máquina de estados (12 estados, tabela testada contra o documento), protocolo serial v1 com 41 exemplos de contrato, política A/B/C, esquemas REST/WebSocket/erros publicados no OpenAPI e tipados no `web/`, migração 001 com 9 tabelas e regras de integridade. SQLite mantido (Docker avaliado e descartado para o banco; ver ADR 0005).

**Objetivo:** todas as frentes trabalham contra o mesmo contrato, sem esperar umas pelas outras.

- `docs/protocolo-serial.md` v1: envelope (`v`, `type`, `msg_id`, `boot_id`, `session_id`, `cmd_id`, `lot_id`, `cycle_id`, `state`, `payload`), handshake, lista de comandos/eventos/erros, prazos, regra de idempotência.
- Modelos Pydantic do protocolo em `api/.../machine/protocol.py` + exemplos válidos e inválidos (servem de teste para API **e** firmware).
- Máquina de estados oficial (diagrama + tabela de transições) — mesma para firmware e simulador.
- Esquemas da API REST e eventos WebSocket (`STATE_CHANGED`, `INSPECTION_READY`, …) e códigos de erro padronizados.
- Migração `001_inicial.sql`: perfis, modelos, lotes, ciclos, inspeções, revisões, eventos, amostras de dataset, com chaves únicas e FKs.
- Política de qualidade: A → aprovado; B, C → rejeitado; abaixo do limiar → inconclusivo.

**Pronto quando:** documento revisado pela equipe; testes de contrato (exemplos JSON) passando.

---

### Bloco 3 — Núcleo da API

> **Situação (18/10/2026):** concluído. Banco com thread única e migração automática, rotas de status, produtos, lotes, controle e diagnóstico, WebSocket com snapshot e ressincronização, controle de operador com tomada explícita, logs JSON, proteção de Host/Origin e pastas de dados separadas por modo. 164 testes na API; fluxo conferido no navegador.

**Objetivo:** backend real rodando sem hardware.

- `config.py` + pasta de dados em `%LOCALAPPDATA%`; criação automática de diretórios.
- Banco: conexão WAL, `foreign_keys=ON`, executor de migrações, repositórios, writer único.
- Barramento de eventos com número de sequência; WebSocket com **snapshot completo na conexão** e eventos incrementais depois.
- Rotas: `health`, `status`, `products`, `lots` (criar, listar, resumo, encerrar), `diagnostics/events`.
- Erros padronizados (código, mensagem ao operador, ação sugerida, `trace_id`).
- Logs JSON Lines com rotação.
- Bind em `127.0.0.1` por padrão; "controle de operador" (um único token de sessão em memória; demais conexões são leitura).

**Pronto quando:** testes de integração cobrem criação de lote, contadores derivados do banco e reconexão do WebSocket.

---

### Bloco 4 — Coordenador do ciclo + simulador de bancada

> **Situação (18/10/2026):** concluído. ESP32 simulado com o mesmo protocolo e falhas injetáveis, câmera simulada (imagens sintéticas), classificador stub, coordenador do ciclo, rotas de máquina e de revisão. 201 testes na API, incluindo mais de 100 ciclos simulados sem divergência; ciclo em velocidade real conferido no navegador (~5 s por peça).

**Objetivo:** o coração do sistema funcionando ponta a ponta em modo simulado.

- **ESP32 simulado** (mesma interface do link serial real): estados, S1/S2 com atraso configurável, injeção de falhas (timeout, mensagem duplicada, fragmentada, reinício com novo `boot_id`).
- **Câmera simulada**: lê imagens de uma pasta, com timestamp.
- **Classificador stub** (resultado configurável) atrás da mesma interface do ONNX.
- Coordenador: lote → ciclo → S1 → estabilização → captura de frame **novo** → inferência → política → decisão ao ESP32 → S2 → separação → registro.
- Rotas `machine/start|pause|stop|rearm` com `command_id` e estado esperado.
- Fluxo de inconclusivo com decisão do operador (revisão registrada).
- Testes pytest dos cenários da §13 da espec.: duplicatas não contam duas vezes, decisão atrasada recusada, reconexão sem reaplicar comando, falta de S2 gera falha por prazo.

**Pronto quando:** 100 ciclos simulados seguidos sem divergência entre banco, contadores e eventos; todos os cenários de falha testados.

---

### Bloco 5 — Interface: design system, Operação e Modo feira [WEB]

> **Situação (19/10/2026):** concluído. Tela de Operação (lote, controle, iniciar/pausar/parar/rearmar, revisão de inconclusivos, esquema da esteira com sensores reais, totais, últimas peças, equipamentos e avisos) e Modo feira escuro e somente leitura. Fonte Archivo local. 15 testes unitários e 5 testes de navegador no Edge (recarregar sem duplicar, segunda tela só leitura, Full HD sem rolagem, celular sem rolagem horizontal). Falta conferir no monitor real da feira a 2–3 m (pendência 7).

**Objetivo:** painel principal bonito e correto, alimentado pelo simulador.

- Tokens (paleta da espec. §21), tipografia Inter local, componentes: cartão de resultado A/B/C/inconclusivo, indicadores, faixa do ciclo, badges de conexão, estados vazio/carregando/erro.
- Distinção visual clara: **rejeição (resultado normal)** × **falha da máquina** × **dado antigo**.
- Tela **Operação**: produto/lote, imagem analisada (separada do vídeo ao vivo), resultado, confiança estimada, destino comandado, contadores, últimas inspeções, ações (iniciar/pausar/parar/encerrar lote).
- **Modo feira**: somente leitura, resultado 40–64 px, sem rolagem em 1920×1080, `prefers-reduced-motion`.
- Responsivo: Full HD, 1366×768, celular (leitura).
- Banner permanente "MODO SIMULADO" quando aplicável.
- Playwright: atualizar página e abrir segunda aba não duplica comandos nem contagens.

**Pronto quando:** fluxo completo visível em simulação; conferido no monitor previsto a 2–3 m.

---

### Bloco 6 — Firmware e bancada física [FW]

> **Situação (19/10/2026):** lógica do firmware concluída (máquina de estados, protocolo e controlador em C++ portátil, motor plugável com drivers liga/desliga e BTS7960). Testada no PC: 16 testes unitários, tabela idêntica à do servidor, todos os exemplos de contrato e ciclos completos da API sobre o firmware real. Compila para o ESP32 (RAM 9,4 %, flash 22,8 %). **Falta:** escolher o motor/driver, confirmar a pinagem, montar e fazer os 50 ciclos físicos e os testes de falha.
> **Situação (20/10/2026):** link serial real com a placa pronto no software (`AV_SERIAL_PORT`, pyserial, reconexão automática sozinha se o cabo cair ou a placa reiniciar; porta descoberta pela tela Diagnóstico). ADR 0013. O ESP32 em si pode ser trocado depois sem afetar isso — a pendência de montagem (motor, pinagem, ensaio físico) continua da equipe.

**Objetivo:** ESP32 executando o ciclo físico com segurança.

- Montagem elétrica conforme lista: fontes separadas, fusíveis, GND comum, **botão de emergência NF obrigatório** cortando motor e servo.
- Pinos: evitar strapping pins (GPIO 0, 2, 12, 15); entradas S1/S2 via clamp BAT54S+R=1kΩ com INPUT_PULLUP interno do ESP32.
- Leitura de sensores com filtro (debounce) e detecção de borda.
- Módulo de motor conforme o driver escolhido no Bloco 1 (A1).
- Servo com posições calibradas dentro do limite mecânico real.
- Máquina de estados do Bloco 2, sem `delay()` longos (loop não bloqueante).
- Protocolo: handshake, `boot_id` aleatório por inicialização, idempotência por `cmd_id`, *heartbeat*; sem comunicação → para o transporte.
- Na volta de energia: nenhum movimento automático, aguarda rearme.
- `pio test` (native) para parser e transições.
- Teste de bancada com um script Python simples antes de ligar à API completa.

**Pronto quando:** 50 ciclos físicos manuais (com decisão enviada por script) + teste de cada falha (cabo USB removido, S2 ausente, emergência pressionada).

---

### Bloco 7 — Câmera real e coleta de dados [API + WEB + IA]

**Objetivo:** dataset real sendo construído na bancada definitiva.

- Fixar câmera, suporte, iluminação difusa e fundo **definitivos** (mudar depois invalida o dataset).
- Fonte OpenCV real: travar exposição, foco e balanço de branco; detectar frame congelado e desconexão; reconexão automática.
- Região de inspeção (ROI) configurável por perfil.
- Rotas `dataset/capture` e `dataset/samples/{id}/label`; tela **Coleta** (produto, lote de coleta, ID da amostra física, classe, revisão, marcação de ambígua/inutilizável).
- `docs/manual-rotulagem.md` com fotos de referência e casos limítrofes por produto; teste de concordância entre duas pessoas.
- Coleta piloto (~30 imagens por classe por produto) para validar enquadramento antes da coleta grande.
- Meta de coleta: 300–500 imagens úteis por produto/classe, de **muitas amostras físicas diferentes**.

**Pronto quando:** manifesto exportado com produto, amostra, classe, sessão; coleta piloto aprovada; coleta grande em andamento.

> **Situação (19/10/2026):** software pronto. Câmera OpenCV (quadro mais recente, recusa de quadro antigo, reabertura automática, foco/balanço automáticos desligados quando o driver permite) configurada por `AV_CAMERA_SOURCE`, inclusive no modo simulado. Tela **Coleta** com vídeo ao vivo, etiqueta da peça com "próxima peça", A/B/C e "rotular depois" por botão ou teclado, progresso por classe (fotos e peças), revisão (ambígua/inutilizável) e exportação do manifesto no formato do treino. Uma classe por peça física garantida pela API. `docs/coleta.md`, modelo de `docs/manual-rotulagem.md` e ADR 0011. **Falta:** câmera, suporte e luz definitivos; critérios A/B/C da equipe; coleta piloto e coleta grande.
> **Situação (20/10/2026):** região de inspeção (ROI) por produto pronta (recorte relativo configurável na tela Configuração, com prévia da câmera; aplicado igual no treino e na inferência; baked no pacote do modelo). Teste de concordância pronto (`/concordancia`): duas pessoas rotulam as mesmas fotos às cegas, resumo mostra taxa de concordância e as discordâncias lado a lado, sem precisar do controle da estação. ADRs 0015–0016.

---

### Bloco 8 — Treinamento, avaliação e exportação [IA]

> **Situação (19/10/2026):** software pronto e testado com fotos sintéticas: divisão por peça física, treino MobileNetV3 Small, exportação ONNX (diferença ao PyTorch ~10⁻⁸), escolha do limiar na validação, relatório com parecer pelas metas do plano, instalação/validação/ativação pela tela de Modelos e bancada operando com o ONNX (~4 ms por peça na CPU). **Falta:** fotos reais (Bloco 7) e o treino/validação de verdade de cada produto.

**Objetivo:** dois modelos versionados com relatório honesto.

- `training/split.py`: 70/15/15 por amostra física (agrupado e estratificado); conjunto de teste congelado.
- `training/train.py`: MobileNetV3 Small, *augmentation* só no treino (sem alterar cor de forma que apague o sinal de qualidade), semente fixa, melhor época por F1 macro na validação.
- `training/evaluate.py`: matriz de confusão, precision/recall/F1 por classe, **B/C aprovados como A**, **A rejeitados**, taxa de revisão por limiar, latência p50/p95.
- Escolha do limiar na **validação**; congelado antes do teste.
- `training/export_onnx.py` + `model.json` + teste de equivalência ONNX × PyTorch.
- Tela **Modelos** (web) listando versões, métricas e situação de validação.
- Metas iniciais (a confirmar): ≥ 90 % de B/C encaminhados à rejeição, ≤ 5 % de B/C falsamente aprovados.

**Pronto quando:** relatório por produto gerado de forma reproduzível; modelos carregam no backend e passam no teste de equivalência.

---

### Bloco 9 — Integração ponta a ponta e telas de operação [INT]

**Objetivo:** peça real → imagem → IA → ESP32 → separação → registro.

- Trocar simuladores pelos componentes reais por configuração (sem alterar o coordenador).
- Calibrar prazos: chegada a S1, estabilização, inferência, chegada a S2, servo, liberação.
- Troca de produto só com máquina parada; carrega e verifica o modelo correto.
- Telas **Histórico** (filtros, paginação, foto, versão do modelo), **Revisão** de inconclusivos, **Exportação CSV** (UTF-8 com BOM, proteção contra injeção de fórmula), **Diagnóstico** (sensores, comunicação, modelo, eventos, testes manuais só em modo manutenção), **Configuração** (perfis e parâmetros, só em repouso).
- Gráfico de distribuição de classes por lote (Chart.js), com tabela equivalente.

**Pronto quando:** os dois produtos completam ciclos reais com rastreabilidade (foto + modelo + decisão + eventos coincidem com a peça).

> **Situação (19/10/2026):** telas prontas no software, testadas na bancada simulada: **Histórico** (filtros por produto, lote, classe, decisão e período; foto, escores e modelo de cada peça; correção registrada sem apagar a previsão; distribuição de classes por lote em barras com tabela equivalente; CSV UTF-8 com BOM, `;` e proteção contra fórmula), **Configuração** (perfil e calibração da bancada por produto, só com a máquina parada e sem lote aberto do produto, com versão contra edição simultânea e registro do antes/depois) e **Diagnóstico** (equipamentos, sensores ao vivo, modo manutenção com teste de motor e servo, registro de eventos filtrável). Gráfico feito em CSS em vez de Chart.js (sem dependência nova). **Falta:** trocar os simuladores pelos componentes reais (link serial), calibrar os prazos na bancada e os ciclos reais com rastreabilidade.
> **Situação (20/10/2026):** link serial real pronto (ver Bloco 6); a tela Diagnóstico já mostra as portas USB disponíveis quando a placa não responde. Resta calibrar os prazos (Configuração) e rodar os ciclos reais na bancada montada.

---

### Bloco 10 — Estabilização, ensaio final e preparação da feira

**Objetivo:** confiável no dia, sem internet, com qualquer membro da equipe operando.

- `scripts/iniciar-feira.ps1`: verifica ambiente, integridade dos modelos (hash), câmera, porta serial, espaço em disco; abre o navegador; explica o que falta sem acionar a bancada.
- Instalação offline validada (cache do uv, `web` já compilado).
- Backup/restauração testados de verdade.
- Retenção de imagens e alerta de disco; falha de gravação bloqueia novos ciclos.
- Ensaio: ≥ 100 ciclos distribuídos entre produtos/classes + 1 hora contínua + todos os cenários de falha da §13.
- Avaliar separadamente: acerto da IA, execução da sequência, destino físico observado.
- Documentação: manual rápido do operador, roteiro de demonstração, limitações declaradas, versões das dependências e licenças.
- Ajustar o PDF/apresentação (DRV8833, números ilustrativos, açaí como evolução).
- **Somente se sobrar tempo (P2):** copiloto de consulta e detecção de anomalias.

**Pronto quando:** checklist final executado e evidências guardadas em `docs/ensaios/`.

> **Situação (20/10/2026):** software pronto. `scripts/iniciar-feira.ps1` confere interface compilada, modo, porta serial, câmera, integridade dos modelos (SHA-256 contra o manifesto) e espaço em disco, sem nunca acionar a bancada. Backup consistente pela tela Configuração (`VACUUM INTO`) ou `scripts/backup.ps1`/`restaurar.ps1` com o serviço parado (sempre guarda os dados atuais antes de sobrescrever). Limpeza automática de fotos de inspeção antigas de lotes encerrados (`AV_IMAGE_RETENTION_DAYS`), nunca toca no lote aberto; falha de gravação já bloqueava novos ciclos desde o Bloco 3. Checklist de instalação offline e guia rápido do operador em `docs/feira.md` e `docs/guia-operador.md`. ADR 0014. **Falta:** rodar o checklist offline no notebook definitivo e o ensaio de ≥ 100 ciclos com peças reais.

---

## Parte 5 — Dependências entre blocos

```text
1 ─► 2 ─► 3 ─► 4 ─┬─► 5 (WEB) ───────────────┐
                   ├─► 6 (FW) ────────────────┼─► 9 ─► 10
                   └─► 7 (coleta) ─► 8 (IA) ──┘
```

O caminho mais longo costuma ser **7 → 8** (coletar e rotular leva tempo de calendário). Por isso câmera, iluminação e critérios A/B/C precisam ser decididos o mais cedo possível, mesmo antes de o backend estar pronto.
