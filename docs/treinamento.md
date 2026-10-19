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

A ferramenta de Coleta (Bloco 7) vai exportar exatamente este formato.

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

## Limites

- Fotos sintéticas só provam que o pipeline funciona; não dizem nada sobre tucumã ou castanha reais.
- O classificador A/B/C não localiza defeitos nem diz a causa; a tela não mostra "rachadura" ou "fungo".
- A confiança é um escore do modelo, não uma probabilidade de acerto.
