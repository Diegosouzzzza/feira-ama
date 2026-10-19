# Contrato da API local — v1

Fonte de verdade: `api/src/amazonvision/schemas/` (Pydantic) e o OpenAPI gerado (`api/openapi.json`, também em `/api/docs` com a API rodando). Os tipos do `web/` são gerados desse arquivo (`pnpm gen:api`), **incluindo os eventos WebSocket** (`WsEvent`).

Situação: rotas marcadas com ✅ estão implementadas e testadas. As demais entram nos blocos indicados.

## Princípios

1. O serviço escuta só em `127.0.0.1`. Requisições com cabeçalho `Host` não local são recusadas (`400`, proteção contra DNS rebinding), e o WebSocket recusa `Origin` de outros sites (código `1008`). Outro aparelho na rede, se um dia for habilitado, terá só leitura.
2. **Um operador controla por vez.** `POST /api/control/claim` devolve um token; rotas de controle exigem o cabeçalho `X-Control-Token`. Sem token válido → `423 CONTROL_LOCKED` com o nome de quem tem o controle. O token expira após 30 min **sem uso** (cada uso renova). Reenviar o claim com o próprio token só renova. Outro operador pode assumir com `takeover: true`; o anterior perde o token e o fato fica registrado como aviso no diagnóstico. O controle fica em memória: reiniciar o serviço o libera.
3. **Idempotência.** Toda requisição que muda estado leva `request_id` (UUID). Repetir o mesmo `request_id` devolve o resultado original com `duplicate: true` e não executa de novo. Atualizar a página nunca reenvia movimentos.
4. **Estado esperado.** Comandos de máquina podem levar `expected_state`; se o estado atual for outro → `409 INVALID_STATE`.
5. **Totais vêm do banco** (`LotSummary`), nunca de contagem no navegador.
6. Horários em UTC com fuso (`AwareDatetime`). A interface exibe em `America/Manaus`.
7. O navegador nunca envia SQL, código ou texto livre para a placa.

## Rotas

| Método e rota | Corpo | Resposta | Bloco | Controle? |
|---|---|---|---|---|
| `GET /api/health` | — | `HealthResponse` | 1 ✅ | não |
| `GET /api/status` | — | `SystemStatus` | 3 ✅ | não |
| `POST /api/control/claim` | `ControlClaim` (+ `X-Control-Token` opcional para renovar) | `ControlGrant` | 3 ✅ | — |
| `POST /api/control/release` | — | 204 | 3 ✅ | sim |
| `GET /api/products` | — | `ProductOut[]` | 3 ✅ | não |
| `GET /api/models` | `?product_id=` | `ModelOut[]` | 8 | não |
| `POST /api/lots` | `LotCreate` | `LotOut` (201; 200 se `request_id` repetido) | 3 ✅ | sim |
| `GET /api/lots` | `?limit(1–100)&offset&product_id` | `LotOut[]` (mais recente primeiro) | 3 ✅ | não |
| `GET /api/lots/{id}` | — | `LotOut` | 3 ✅ | não |
| `GET /api/lots/{id}/summary` | — | `LotSummary` | 3 ✅ | não |
| `POST /api/lots/{id}/close` | — | `LotOut` (encerrar de novo devolve o mesmo lote) | 3 ✅ | sim |
| `POST /api/machine/start` | `MachineCommandRequest` | `MachineCommandResult` | 4 ✅ | sim |
| `POST /api/machine/pause` | `MachineCommandRequest` | `MachineCommandResult` | 4 ✅ | sim |
| `POST /api/machine/stop` | `MachineCommandRequest` | `MachineCommandResult` | 4 ✅ | sim |
| `POST /api/machine/rearm` | `MachineCommandRequest` | `MachineCommandResult` | 4 ✅ | sim |
| `GET /api/inspections` | `?lot_id&product_id&grade&decision&from&to&limit&offset` | `InspectionPage` | 9 | não |
| `GET /api/inspections/{id}` | — | `InspectionOut` | 4 ✅ | não |
| `GET /api/inspections/{id}/image` | — | PNG (simulado) ou JPEG | 4 ✅ | não |
| `POST /api/inspections/{id}/review` | `InspectionReviewCreate` | `ReviewOut` (201; 200 se `request_id` repetido) | 4 ✅ | sim |
| `GET /api/exports/inspections.csv` | mesmos filtros | CSV UTF-8 com BOM | 9 | não |
| `GET /api/camera/stream` | — | MJPEG (canal separado) | 7 | não |
| `POST /api/dataset/capture` | (Bloco 7) | (Bloco 7) | 7 | sim |
| `PATCH /api/dataset/samples/{id}/label` | (Bloco 7) | (Bloco 7) | 7 | sim |
| `GET /api/config` / `PUT /api/config` | (Bloco 9) | (Bloco 9) | 9 | `PUT` sim |
| `GET /api/diagnostics/events` | `?limit(1–200)&offset&severity` | `EventOut[]` (mais recente primeiro) | 3 ✅ | não |
| `WS /api/events` | — | `WsEvent` | 3 ✅ | não |

Regras de estado das rotas de controle:

- Criar/encerrar lote: máquina parada (sem operação automática nem ciclo em andamento). Abrir o lote carrega o modelo do produto; encerrar descarrega. Trocar de produto = encerrar o lote e abrir outro.
- `start`: exige placa conectada, lote aberto, modelo pronto, câmera ok, banco saudável e nenhuma peça aguardando revisão (`409 REVIEW_REQUIRED`). Se a placa estiver desarmada, envia `CONFIGURE` + `ARM`. Liga a **operação automática**: um ciclo após o outro até `pause`, `stop` ou falha.
- `pause`: termina o ciclo já autorizado e não inicia o próximo.
- `stop`: parada por software imediata (`STOP` na placa); o ciclo em andamento é registrado como interrompido.
- `rearm`: `CLEAR_FAULT` (se em falha) + `CONFIGURE` + `ARM` (se houver lote aberto). **Nunca** liga a operação automática nem move a esteira. Recusado com peça sobre sensor ou emergência acionada.
- Qualquer interrupção de ciclo (falha, parada, emergência, reinício da placa, placa muda, câmera/modelo/gravação com falha) desliga a operação automática.
- `review`: decide a peça inconclusiva parada em `REVIEW_HOLD` (a decisão é entregue à placa **antes** de ser registrada) ou corrige uma decisão anterior sem mover nada. A previsão original fica intacta; cada revisão é um registro novo.

## WebSocket `/api/events`

- Somente servidor → cliente. Comandos vão sempre por HTTP.
- A **primeira mensagem** de toda conexão é `SNAPSHOT` com o `SystemStatus` completo. O `seq` do snapshot é o último evento já refletido nele (pode ser `0`); o próximo evento terá `seq + 1`.
- O servidor também envia `SNAPSHOT` a todos quando muda algo fora do fluxo de eventos (ex.: quem tem o controle). O cliente substitui o estado inteiro.
- Cada evento tem `seq` crescente. Se o cliente detectar lacuna em `seq`, reconecta e recebe novo `SNAPSHOT`.
- Cliente lento demais (fila de 256 eventos cheia) é desconectado com código `4000`; deve reconectar.
- `state_version` cresce a cada mudança relevante; a interface ignora mensagem com versão menor que a que já mostrou.
- Tipos: `SNAPSHOT`, `STATE_CHANGED`, `SENSOR_CHANGED`, `INSPECTION_READY`, `DECISION_ACCEPTED`, `CYCLE_COMPLETED`, `CYCLE_ABORTED`, `LOT_UPDATED`, `CONNECTION_LOST`, `CONNECTION_RESTORED`, `FAULT`.
- Vídeo ao vivo **não** passa por aqui (`/api/camera/stream`).

## Erros

Toda resposta não-2xx em `/api` usa `ApiErrorBody`:

```json
{ "code": "MODEL_NOT_READY", "message": "Modelo não carregado.", "recovery": "Selecione o produto.", "trace_id": "3f9a1c2b7d4e" }
```

`message` é para o operador (português, sem pilha de erro). `trace_id` localiza o registro no log.

| Código | HTTP | Quando |
|---|---|---|
| `VALIDATION_ERROR` | 422 | Corpo ou parâmetros inválidos |
| `NOT_FOUND` | 404 | Recurso ou rota inexistente |
| `CONFLICT` | 409 | Conflito de dados (ex.: já existe lote aberto) |
| `INVALID_STATE` | 409 | Ação não permitida no estado atual da máquina |
| `CONTROL_LOCKED` | 423 | Outro operador tem o controle, ou token ausente |
| `REVIEW_REQUIRED` | 409 | Há inconclusivo aguardando decisão do operador |
| `CAMERA_UNAVAILABLE` | 503 | Câmera ausente ou desconectada |
| `STALE_FRAME` | 503 | Imagem antiga demais para a inspeção |
| `MODEL_NOT_READY` | 503 | Modelo do produto não carregado ou inválido |
| `SERIAL_DISCONNECTED` | 503 | Placa sem comunicação |
| `SENSOR_TIMEOUT` | 504 | Prazo de sensor esgotado |
| `STORAGE_ERROR` | 507 | Falha de gravação; novos ciclos ficam bloqueados |
| `INTERNAL_ERROR` | 500 | Erro inesperado (detalhes só no log) |
