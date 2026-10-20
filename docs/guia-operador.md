# Guia rápido do operador

Uma página para quem vai operar a bancada no dia da feira, sem precisar ler o resto da documentação.

## Ligar

1. Dê duplo clique no atalho de inicialização (ou rode `scripts\iniciar-feira.ps1`).
2. Se aparecer algo em vermelho (**[falta]**), chame alguém da equipe técnica antes de continuar — a esteira ainda não liga sozinha, então não tem perigo, mas a bancada pode não funcionar direito.
3. O navegador abre sozinho na tela de **Operação**.

## Operar

1. **Operar a estação** (canto da tela) → digite seu nome. Só uma pessoa opera por vez; as outras telas acompanham.
2. **Abrir lote**: escolha o produto. Se já havia um lote aberto de outro produto, encerre-o primeiro.
3. **Iniciar**: a esteira começa a passar as peças. Coloque as peças uma de cada vez na entrada.
4. Cada peça aparece na tela com a classe (A, B ou C) assim que é analisada.
5. **Peça com "?"**: a bancada não teve certeza e está **parada**, esperando você decidir. Olhe a foto na tela e escolha **Aprovar** ou **Rejeitar**. A peça só anda depois disso.
6. **Pausar**: termina a peça que já está na esteira e não inicia a próxima. **Parar**: para na hora.
7. No fim do lote, **Encerrar lote**.

## Se der problema

| Na tela aparece | O que fazer |
|---|---|
| "Placa sem comunicação" | Confira o cabo USB. Se persistir, chame a equipe técnica — a tela **Diagnóstico** mostra as portas disponíveis. |
| Uma mensagem de falha (fundo vermelho) | Leia a mensagem: ela diz o que fazer (ex.: "retire a peça do sensor"). Resolva e clique em **Rearmar**. |
| Botão de emergência apertado | Solte o botão primeiro; a tela só deixa rearmar depois disso. |
| "Câmera indisponível" | Confira o cabo da câmera e a luz do ambiente. |
| Peça travada ou posição errada | Pare a máquina (**Parar**), retire a peça com a mão, **Rearmar** e **Iniciar** de novo. |

Nunca force a esteira ou as peças com a máquina ligada. Em qualquer dúvida de segurança, use o botão físico de emergência.

## Desligar no fim do dia

1. **Parar** a esteira e **encerrar o lote**.
2. Feche a janela do serviço (ou `Ctrl+C` no terminal onde ele está rodando).
3. Faça o backup do dia: tela **Configuração** → **Backups e limpeza** → **Fazer backup agora**, e copie o arquivo baixado para um pendrive (`docs/feira.md` tem os detalhes).

## Outras telas (para quem acompanha ou ajusta)

- **Histórico**: todas as peças já inspecionadas, com foto, filtros e exportação para planilha.
- **Modo feira**: a mesma informação da Operação, em tela grande e só leitura — para o público ver.
- **Coleta**, **Concordância**, **Modelos**: usadas antes da feira, para treinar o modelo (não durante a operação).
- **Configuração**: prazos da bancada, limiar de decisão, backups. Só mexa parado, fora do horário de operação.
- **Diagnóstico**: estado de cada equipamento e o registro completo de eventos, para quem for investigar um problema.
