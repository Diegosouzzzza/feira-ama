# Pendências que dependem da equipe

Atualizar esta lista conforme as respostas chegarem. Cada resposta relevante vira um ADR.

| # | Pendência | Bloqueia | Precisa estar resolvida antes de | Situação |
|---|---|---|---|---|
| 1 | Data da feira e tamanho/disponibilidade da equipe | Cronograma em dias | Bloco 2 | Aberta |
| 2 | Motor da esteira: tensão, corrente, só liga/desliga ou velocidade/reversão | Escolha do driver (DRV8833 **não** serve para 12 V). O firmware já tem driver liga/desliga (MOSFET/relé) e BTS7960; falta escolher e, se for outro, escrever a classe. O ESP32 pode até ser trocado depois, se precisar — o link serial (ADR 0013) não depende de qual placa | Montagem do Bloco 6 | Aberta (firmware e link serial prontos para os dois casos mais prováveis) |
| 3 | Câmera: webcam USB UVC (recomendado) ou celular | Coleta com a câmera definitiva (o software já aceita qualquer webcam UVC ou URL de vídeo via `AV_CAMERA_SOURCE`) | Coleta das fotos de treino | Aberta (software pronto) |
| 4 | Castanha com ou sem casca; critérios visuais A/B/C dos dois produtos | Rotulagem e treinamento (preencher `docs/manual-rotulagem.md`, confirmar com o teste de concordância em `/concordancia`) | Primeira sessão de coleta rotulada | Aberta (ferramenta de concordância pronta) |
| 5 | Classes B e C na mesma saída (rejeitados) | Política de decisão e firmware | Bloco 2 | Proposta: sim |
| 6 | Notebook da feira: Windows, GPU, RAM, portas USB | Fixação final das dependências; rodar o ensaio offline de `docs/feira.md` no notebook definitivo | Bloco 2 | Aberta |
| 7 | Monitor da feira (tamanho e resolução) | Validação do modo feira | Bloco 5 | Aberta |
| 8 | Botão de emergência físico | Segurança da bancada | Bloco 6 | Proposta: obrigatório; firmware lê o contato auxiliar no GPIO 27 |
| 9 | Pinagem definitiva do ESP32 (S1, S2, emergência, servo, motor) | Montagem e gravação na bancada | Montagem do Bloco 6 | Proposta em `docs/firmware.md`, a confirmar |
