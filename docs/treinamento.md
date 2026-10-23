# Treinamento dos modelos

O pipeline transforma um conjunto de fotos rotuladas num **pacote de modelo** (`model.onnx` + `model.json` + relatório) que a API instala, a equipe valida e o produto ativa.

## Instalação

O treino usa o grupo de dependências `training` (PyTorch, torchvision, scikit-learn, onnx). O notebook da feira não precisa dele: só roda o ONNX.

```powershell
cd api
uv sync --group training
```

Por padrão é instalado o PyTorch **CPU** (funciona em qualquer PC; MobileNetV3 Small treina em segundos ou minutos). Para usar a GPU RTX, troque em `api/pyproject.toml` a URL do índice `pytorch-cpu` pela do CUDA compatível com o driver (ex.: `https://download.pytorch.org/whl/cu128`) e rode `uv sync --group training` de novo.

## Formato do conjunto de fotos

Uma pasta com as imagens e um `manifest.csv`:

| Coluna | Conteúdo |
|---|---|
| `path` | Caminho da foto, relativo à pasta do manifesto |
| `product_id` | `tucuma` ou `castanha` |
| `physical_sample_id` | Identificação da **peça física** (todas as fotos da mesma peça têm o mesmo valor) |
| `label` | `A`, `B` ou `C` |
| `split` | `train`, `val` ou `test` (deixe vazio para dividir automaticamente) |

A tela de **Coleta** exporta exatamente este formato (`dataset/manifest-<produto>.csv`, ver `docs/coleta.md`), com o comando de treino pronto para copiar.

## Comandos

```powershell
cd api
# Fotos de teste geradas pelo simulador (só para validar o pipeline)
uv run --group training python -m amazonvision.training sintetico --saida C:\dados\sintetico

# Treinar, exportar ONNX, escolher o limiar e gerar o relatório
uv run --group training python -m amazonvision.training treinar --manifesto C:\dados\sintetico\manifest.csv --produto tucuma
```

Opções do `treinar`: `--epocas` (12), `--lote` (16), `--dispositivo` (`auto`, `cpu`, `cuda`), `--meta-falsa-aprovacao` (0,05), `--sem-pre-treino`, `--saida` (padrão: `%LOCALAPPDATA%\AmazonVision\<modo>\modelos-treinados`).

## O que o treinamento garante

1. **Divisão por peça física** (70/15/15, estratificada por classe): fotos da mesma peça nunca ficam em treino e teste ao mesmo tempo.
2. **Mesmo pré-processamento** no treino e na bancada (`vision/preprocess.py`): imagem inteira com *letterbox*, sem cortar bordas.
3. **Aumento de dados só geométrico** (giros, espelhamentos) e brilho leve: a cor faz parte do sinal de qualidade.
4. **Melhor época pela validação** (F1 macro), nunca pelo teste.
5. **Avaliação no modelo exportado**: as métricas são do ONNX que a bancada vai executar, e a diferença PyTorch × ONNX é registrada.
6. **Limiar escolhido na validação**: o menor que mantém a falsa aprovação de B/C ≤ meta; depois é congelado e aplicado ao teste.
7. **Parecer** no relatório: pronto para ensaio só se, no teste, B/C rejeitadas ≥ 90 %, falsa aprovação ≤ meta e decisões automáticas ≥ 70 %.

## Do pacote à bancada

1. Na tela **Modelos**, informe a pasta do pacote e clique em **Instalar modelo** (o pacote é copiado e o SHA-256 dos pesos é conferido).
2. Leia o relatório. **Validar** registra quem aprovou; **Reprovar** impede a ativação.
3. **Ativar para este produto**: o limiar calibrado vira o limiar do produto. Só é possível sem lote aberto daquele produto; o próximo lote usa o novo modelo.
4. No modo real, só modelos **validados** podem ser ativados.

Se os pesos instalados forem alterados ou corrompidos, o modelo não carrega, o status mostra erro e a bancada não inicia.

## Só com peças boas: detecção de anomalia

Quando ainda não há peças ruins para fotografar, o comando `anomalia` aprende **só com as peças boas** (classe A) e marca como "fora do padrão" o que foge delas: manchas, mofo, pedaço faltando, formato estranho ou um objeto que não é o produto. Detalhes e números em `docs/adr/0017-deteccao-de-anomalia.md`.

```powershell
cd api
uv run --group training python -m amazonvision.training anomalia --manifesto C:\dados\manifest.csv --produto castanha --roi 0.2,0.1,0.6,0.8
```

Opções: `--banco` (4000 retalhos no banco de memória), `--limiar` (0,80), `--roi`, `--sem-pre-treino`, `--saida`. Linhas B ou C do manifesto, se existirem, só são usadas para medir no teste.

O pacote se instala e ativa como qualquer outro: A vai para aprovados, C para rejeitados e o meio-termo para revisão. O relatório nunca dá o parecer "pronto", porque nenhum defeito real foi medido.

### Refazer na bancada (obrigatório antes de deixar decidir)

O modelo depende do fundo, da luz e da câmera. Com a bancada montada:

1. Configure a região de inspeção do produto (tela Configuração).
2. Na tela Coleta, fotografe 15 a 20 peças **boas**, classe A, 3 a 6 fotos cada, girando a peça.
3. Exporte o manifesto e rode `anomalia` com o mesmo `--roi`. Leva poucos minutos: não há épocas de treino.
4. Instale, leia o relatório, ative e passe algumas peças ruins: elas devem ir para rejeitados ou revisão.

### Ensaiar com fotos reais na bancada simulada

No modo simulado, `AV_SIM_PHOTOS` aponta para uma pasta de fotos (JPEG ou PNG) que a câmera simulada mostra no lugar dos desenhos, uma por peça, em ordem embaralhada. Use fotos que o modelo **não** viu no treino:

```
AV_SIM_PHOTOS=C:\Users\<você>\AppData\Local\AmazonVision\referencia\demonstracao-castanha
```

## Limites

- Fotos sintéticas só provam que o pipeline funciona; não dizem nada sobre tucumã ou castanha reais.
- O classificador A/B/C não localiza defeitos nem diz a causa; a tela não mostra "rachadura" ou "fungo".
- A confiança é um escore do modelo, não uma probabilidade de acerto.
