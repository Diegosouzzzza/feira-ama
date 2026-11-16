# ADR 0011 — Câmera real e ferramenta de Coleta

Data: 2026-10-19 · Situação: aceita

## Contexto

O modelo só pode ser treinado com fotos tiradas na própria bancada, com a mesma câmera e a mesma luz da operação. O hardware da esteira ainda não está definido, mas a câmera e a coleta podem começar antes.

## Decisões

1. **OpenCV (`opencv-python-headless`)** lê a câmera USB/UVC (DirectShow no Windows) ou uma URL de vídeo. Uma linha de execução guarda só o quadro mais recente com seu horário; a captura espera um quadro posterior ao pedido e nunca devolve um quadro antigo do buffer (`STALE_FRAME`). Falha de leitura reabre a câmera sozinha.
2. **Configuração pela variável `AV_CAMERA_SOURCE`**, que vale também no modo simulado: dá para coletar fotos reais sem a esteira.
3. **Vídeo ao vivo em MJPEG** (`/api/camera/stream`), em canal separado do WebSocket de estado, para que imagens não atrasem eventos da máquina. A câmera simulada mostra o último desenho fotografado.
4. **Coleta só com a máquina parada** e com o controle da estação: a câmera é a mesma da inspeção e uma foto de coleta não pode disputar o quadro com um ciclo.
5. **Uma classe por peça física**: a API recusa classes diferentes para fotos da mesma etiqueta, o que mantém válida a divisão por peça do treinamento.
6. **O manifesto exportado é o mesmo formato do treinamento** (`path, product_id, physical_sample_id, label, split`), com caminhos relativos à pasta `dataset/`; o `split` fica vazio e é feito por peça no treino.
7. **Rótulo com autoria**: quem fotografa com classe é o autor do rótulo; quem altera na revisão fica como revisor. Ambíguas e inutilizáveis ficam fora do manifesto.

## Evidências

- Testes da câmera com um dispositivo falso: quadro posterior ao pedido, quadro antigo recusado, câmera que não abre, reabertura após falha, estado "stale".
- Testes da API: captura rotulada e sem rótulo, fotos sempre distintas, conflito de classe na mesma peça, recusa com a esteira em operação e sem câmera, resumo, filtros e manifesto lido pelo `read_manifest` do treinamento.
- Teste de navegador: fotografar com botão e atalho, revisar, exportar.
