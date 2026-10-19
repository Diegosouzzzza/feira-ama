# Coleta de fotos para treinamento

A tela **Coleta** (`/coleta`) fotografa peças paradas sob a câmera da bancada, guarda cada foto com o produto, a etiqueta da peça física e a classe, e exporta o manifesto que o treinamento lê (`docs/treinamento.md`). Os critérios de classe estão em `docs/manual-rotulagem.md`.

## Câmera

| Variável | Padrão | Uso |
|---|---|---|
| `AV_CAMERA_SOURCE` | vazio | Índice da webcam (`0`, `1`…) ou URL de vídeo. Vazio: câmera simulada no modo simulado, nenhuma no modo real |
| `AV_CAMERA_WIDTH` / `AV_CAMERA_HEIGHT` | 1280 × 720 | Resolução pedida à câmera |
| `AV_CAMERA_EXPOSURE` | vazio | Exposição manual (unidade do driver); vazio mantém a da câmera |

Com `AV_CAMERA_SOURCE` definido, a câmera real é usada também no modo simulado (útil para coletar fotos antes de a esteira existir). Exemplo em `api/.env`:

```
AV_CAMERA_SOURCE=0
```

A câmera é lida por uma linha de execução própria que guarda só o quadro mais recente; uma foto sempre usa um quadro **posterior** ao clique (nunca um quadro antigo do buffer). Se a câmera parar de entregar quadros, ela é reaberta sozinha. Foco e balanço de branco automáticos são desligados quando o driver permite.

## Passo a passo

1. Assuma o controle da estação e confirme que a máquina está **parada** (a coleta é recusada com a esteira em operação).
2. Escolha o produto e a sessão (padrão: data de hoje; use algo como `2026-10-20-tarde` se houver mais de uma no dia).
3. Digite a etiqueta da peça física e coloque a peça sob a câmera.
4. Fotografe com a classe: botões **A**, **B**, **C** ou teclas `1`, `2`, `3`. Na dúvida, **Fotografar e rotular depois** (`0`).
5. Gire a peça e repita (3 a 6 fotos por peça). **Próxima peça** (ou `N`) avança a etiqueta (`T-0007` → `T-0008`).
6. Na **Revisão das fotos**, filtre **Sem rótulo** para decidir as pendentes; marque **Ambígua** ou **Inutilizável** quando for o caso.
7. **Exportar para treinamento** grava `dataset/manifest-<produto>.csv` e mostra o comando de treino.

## Onde ficam os arquivos

```
%LOCALAPPDATA%\AmazonVision\<modo>\dataset\
  manifest-tucuma.csv
  tucuma\<sessão>\<etiqueta>_<sha12>.jpg
```

Cada foto é gravada de forma atômica e registrada no banco (`dataset_samples`) com SHA-256, autor do rótulo, revisor e a configuração da câmera. A mesma imagem não entra duas vezes. O manifesto inclui só fotos **rotuladas**; a divisão treino/validação/teste é feita no treinamento, por peça física.

## Rotas

| Rota | Uso |
|---|---|
| `GET /api/camera/stream` | Vídeo ao vivo (MJPEG, ~5 quadros/s), separado do WebSocket de estado |
| `GET /api/camera/snapshot` | Quadro mais recente (JPEG) |
| `POST /api/dataset/capture` | Fotografa e registra (controle; máquina parada) |
| `GET /api/dataset/samples` | Lista com filtros e paginação |
| `PATCH /api/dataset/samples/{id}` | Rotula, corrige, marca ambígua ou inutilizável (controle) |
| `GET /api/dataset/samples/{id}/image` | Arquivo da foto |
| `GET /api/dataset/summary` | Fotos e peças por classe, comparadas com a meta |
| `POST /api/dataset/export` | Gera o manifesto do produto (controle) |

## Privacidade

A câmera da bancada aponta para a esteira. Evite rostos e mãos nas fotos; fotos assim devem ser marcadas como **Inutilizável**.
