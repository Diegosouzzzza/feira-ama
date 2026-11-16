# ADR 0010 — Pipeline de IA: treino em PyTorch, operação em ONNX

Data: 2026-10-19 · Situação: aceita

## Decisões

1. **Classificador MobileNetV3 Small** (torchvision, BSD) com transferência de aprendizado do ImageNet; saída A/B/C. Detecção/localização de defeitos fica fora do escopo inicial.
2. **Operação em ONNX Runtime na CPU**: ~4 ms por peça no notebook de desenvolvimento, sem depender de CUDA no dia da feira. O modelo é aquecido ao carregar.
3. **Pré-processamento único** (`vision/preprocess.py`) usado pelo treino e pela inferência; o manifesto do pacote registra os parâmetros e a API os reaplica.
4. **Pacote de modelo** = `model.onnx` + `model.json` (classes, pré-processamento, SHA-256 dos pesos, versão do dataset, limiar recomendado, métricas) + `relatorio.md`. Os pesos são conferidos ao instalar e a cada carga.
5. **Limiar calibrado na validação** e adotado pelo produto ao ativar o modelo; cada lote congela o limiar em uso.
6. **Ciclo de vida**: instalar → (validar | reprovar) → ativar. No modo real só modelos validados ativam; nunca durante um lote aberto do mesmo produto.
7. **Dependências**: `onnxruntime`, `numpy` e `Pillow` na execução; PyTorch/torchvision/scikit-learn/onnx no grupo `training`, com o índice CPU do PyTorch por padrão.
8. **No modo simulado**, um produto com modelo ativo usa o ONNX também com a câmera simulada; sem modelo, usa o classificador simulado.

## Evidências

- Treino completo nas fotos sintéticas: 29 s na CPU, exportação ONNX com diferença máxima de 2,4×10⁻⁸ para o PyTorch.
- Bancada simulada operando com o modelo ONNX instalado e ativado pela tela de Modelos.
- Testes: pré-processamento sem corte, pacote adulterado recusado, ciclo pela API usando o ONNX, ativação bloqueada com lote aberto e no modo real sem validação, modelo corrompido reportado e bancada bloqueada, treino completo gerando pacote válido.
