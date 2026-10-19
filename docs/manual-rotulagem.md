# Manual de rotulagem A/B/C

Modelo para a equipe preencher **antes** da primeira sessão de coleta. O modelo de IA aprende exatamente o que este manual descreve: se duas pessoas rotulam a mesma peça de formas diferentes, o modelo aprende essa dúvida.

> Situação: **a preencher pela equipe** (pendência 4 em `docs/pendencias.md`). Até lá, só fotografe sem rótulo.

## Regras gerais

1. **Uma peça física, uma classe.** Todas as fotos da mesma peça levam a mesma classe; o sistema recusa classes diferentes para a mesma etiqueta.
2. **Etiqueta física em cada peça** (ex.: `T-0001` para tucumã, `C-0001` para castanha), escrita num papel ou pote que acompanha a peça. A etiqueta da tela tem que bater com a da peça.
3. **Na dúvida, não rotule.** Use **Fotografar e rotular depois** (tecla `0`) e decida em grupo na revisão. Se o grupo não chegar a um acordo, marque **Ambígua**: a foto fica fora do treinamento.
4. **Foto ruim não entra.** Peça cortada, borrada, duas peças na imagem, mão na frente ou luz diferente: marque **Inutilizável**.
5. **Mesma montagem da operação**: mesma câmera, mesma altura, mesma luz, mesmo fundo da esteira. Fotos tiradas em outro lugar ensinam o modelo a reconhecer o lugar.
6. **Varie a peça, não a cena**: 3 a 6 fotos por peça, girando-a e mostrando lados diferentes.

## Metas de quantidade

| Por produto | Mínimo | Ideal |
|---|---|---|
| Fotos rotuladas por classe | 300 | 500 |
| Peças físicas distintas por classe | 60 | 100 ou mais |

O treinamento divide treino, validação e teste **por peça física**: muitas fotos de poucas peças não ajudam. A tela de Coleta mostra fotos e peças por classe.

## Critérios — Tucumã

| Classe | Significado na esteira | Critérios visuais (preencher) | Exemplos de fotos de referência |
|---|---|---|---|
| A | Dentro do padrão visual (aprovado) | _ex.: casca inteira, cor laranja uniforme, sem manchas…_ | |
| B | Defeito visual (rejeitado) | _ex.: mancha até X % da superfície, pequena rachadura…_ | |
| C | Refugo ou fora do padrão (rejeitado) | _ex.: podridão, fungo, fruto amassado, muito pequeno…_ | |

Casos de fronteira combinados pela equipe (preencher):

- _ex.: mancha escura pequena → B, não C_

## Critérios — Castanha-do-pará

Apresentação usada na feira: _com casca / sem casca_ (preencher; pendência 4).

| Classe | Significado na esteira | Critérios visuais (preencher) | Exemplos de fotos de referência |
|---|---|---|---|
| A | Dentro do padrão visual (aprovado) | | |
| B | Defeito visual (rejeitado) | | |
| C | Refugo ou fora do padrão (rejeitado) | | |

Casos de fronteira combinados pela equipe (preencher):

-

## Revisão cruzada

Antes de exportar para o treinamento, uma segunda pessoa revisa uma amostra de pelo menos 10 % das fotos rotuladas de cada classe (filtro **Rotuladas** na tela de Coleta). Discordâncias voltam para discussão e, se necessário, para **Ambígua**.

| Data | Produto | Quem revisou | Fotos revisadas | Discordâncias | Decisão |
|---|---|---|---|---|---|
| | | | | | |
