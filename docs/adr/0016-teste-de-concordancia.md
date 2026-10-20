# ADR 0016 — Teste de concordância na rotulagem

Data: 2026-10-20 · Situação: aceita

## Contexto

O modelo aprende exatamente o que a equipe rotula. Se duas pessoas rotulam a mesma peça de formas diferentes, o modelo aprende essa dúvida. O plano previa confirmar que o critério A/B/C está claro **antes** da coleta grande, comparando os rótulos de duas pessoas sobre as mesmas fotos, sem uma ver a resposta da outra.

## Decisões

1. **Tabela separada** (`label_agreement`), não o campo `label` de `dataset_samples`: o rótulo de concordância é um exercício, nunca a verdade de treino. `UNIQUE (sample_id, session, reviewer)` deixa cada pessoa rotular de novo (atualiza a resposta) sem nunca ver a de outra.
2. **"Sessão" nomeada pela equipe** (mesma ideia de `collection_session` da Coleta), não uma sessão de usuário: quem entra com o mesmo produto e o mesmo nome de rodada está, por definição, comparando com quem também entrou nela. Sem contas nem login, consistente com o resto do sistema.
3. **Cego por construção**: a rota que grava um rótulo nunca devolve o de outro revisor; a de resumo só existe comparando, nunca lista "quem disse o quê" antes de haver pelo menos dois revisores na rodada (`409 INVALID_STATE` até lá). Não é uma trava técnica impossível de furar (não há contas), mas o fluxo normal da tela nunca expõe a resposta alheia.
4. **Não exige o controle da estação**: é uma atividade de equipe, separada da operação da bancada — pode rodar em paralelo, inclusive com a esteira funcionando.
5. **Fotos de qualquer status da Coleta** entram na fila, não só as já rotuladas: o objetivo é testar o critério em peças reais, não validar um rótulo existente.

## Evidências

- Testes da API: rótulo sem controle, atualização ao rotular de novo, fila por revisor independente, resumo recusado com um revisor só, concordância e discordância calculadas certas, rodadas diferentes nunca se misturam.
- Teste de navegador: duas "pessoas" (uma pela tela, outra pela API) rotulam a mesma foto com classes diferentes; o resumo mostra 50 % de concordância e a foto em disputa com os dois rótulos lado a lado.
