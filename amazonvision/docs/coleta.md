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

## Região de inspeção (ROI)

Na tela **Configuração**, cada produto pode ter uma janela de recorte (x, y, largura, altura em % do quadro), com uma prévia da câmera mostrando o retângulo. Isso recorta o fundo e a esteira antes de analisar, deixando o modelo ver só onde a peça fica.

O recorte **não** é aplicado à foto gravada (ela fica inteira, para auditoria); ele é aplicado como parte do pré-processamento, igual no treino e na bancada. Por isso, ao exportar, o comando de treino já vem com `--roi x,y,largura,altura` quando o produto tem um configurado — é só copiar e colar. Mudar o ROI depois não invalida as fotos já coletadas: o próximo treino simplesmente recorta de novo, com o valor atual.

## Teste de concordância na rotulagem

Antes da coleta grande, vale confirmar que o critério A/B/C está claro: a tela **Concordância** (`/concordancia`) deixa duas pessoas rotularem as mesmas fotos já coletadas, cada uma sem ver a resposta da outra (mesmo produto e mesmo nome de "rodada"). O resumo, visto só depois que as duas terminarem, mostra a taxa de concordância e cada foto onde elas discordaram, lado a lado. Não precisa do controle da estação: é uma atividade separada, pode rodar em paralelo com a operação. Detalhes em `docs/manual-rotulagem.md`.

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
| `POST /api/dataset/agreement/labels` | Registra o rótulo às cegas de um revisor (sem controle) |
| `GET /api/dataset/agreement/next` | Próxima foto que o revisor ainda não rotulou nesta rodada |
| `GET /api/dataset/agreement/summary` | Compara os rótulos; exige 2 revisores na rodada |

## Privacidade

A câmera da bancada aponta para a esteira. Evite rostos e mãos nas fotos; fotos assim devem ser marcadas como **Inutilizável**.
