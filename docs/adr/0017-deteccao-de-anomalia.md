# ADR 0017 — Detecção de anomalia com peças boas apenas

Data: 2026-10-21 · Situação: aceita

## Contexto

A equipe ainda não tem frutos para fotografar, e não existe na internet nenhum conjunto público de castanha-do-pará boa × ruim (pesquisado em português e inglês). As fotos livres que existem (NutsBD, Mendeley Data, CC BY 4.0) são todas de castanhas sadias. Um classificador A/B/C precisa de exemplos de B e C; sem eles, aprenderia um critério falso (por exemplo, a cor da película).

## Decisões

1. **Novo modo de treino `anomalia`** (`python -m amazonvision.training anomalia`), ao lado do `treinar`. Ele aprende só com peças da classe A: guarda num banco de memória os retalhos (8×8 px) de uma MobileNetV3 Small pré-treinada, extraídos de duas profundidades (passo 8 e 16). Na inspeção, a distância do pior retalho da foto ao retalho bom mais próximo vira o escore de "fora do padrão". É a ideia do PatchCore, simplificada.
2. **Mesmo contrato de pacote**: o grafo ONNX transforma a distância em logits `[A, B, C] = [0, −30, (d − centro)/escala]`. A API, a regra de decisão, a bancada e as telas não mudam: A vai para aprovados, C para rejeitados, o meio-termo para revisão humana. A classe B nunca é prevista.
3. **Calibração sem peças ruins**: o limite de aprovação é o percentil 95 das distâncias das peças boas da validação; o de rejeição fica 2 desvios-padrão acima. Com o limiar do produto em 0,80, a confiança cruza o limiar exatamente nesses dois pontos. O limite de rejeição é uma estimativa e o relatório diz isso.
4. **Peças B/C do manifesto só no teste**: se houver, nunca entram no banco. Com as fotos da internet, outras nozes do mesmo conjunto (mesmo fundo e luz) servem de "objeto diferente", e o relatório deixa claro que isso **não mede defeitos**.
5. **Nunca "pronto" sozinho**: `ready_for_bench` é sempre falso, e a tela Modelos mostra outros indicadores para esse tipo de modelo (boas rejeitadas, outros objetos rejeitados, revisão) e um aviso para refazê-lo com fotos da bancada.
6. **Câmera simulada com fotos reais** (`AV_SIM_PHOTOS`, só no modo simulado): uma pasta de fotos substitui os desenhos, uma por peça, em ordem embaralhada. Permite ensaiar um modelo treinado de ponta a ponta antes de a bancada existir.

## Consequências

- O modelo é sensível ao fundo, à luz e à câmera das fotos de treino. Antes de usar na bancada é preciso refazê-lo com 15 a 20 peças boas fotografadas nela (procedimento em `docs/treinamento.md`). É rápido: não há épocas de treino, só extração de características.
- Não diz o motivo da rejeição; uma peça boa com formato muito incomum pode ir para revisão.
- Quando a equipe tiver peças ruins de verdade, o classificador A/B/C (`treinar`) continua sendo o caminho para separar B de C e medir defeitos.

## Evidências (fotos do NutsBD, castanhas nunca vistas no treino)

- 19 de 19 castanhas boas do teste aprovadas; latência de 7 a 15 ms por peça.
- 90 fotos de 9 outras nozes: 78 % rejeitadas, 14 % para revisão, 8 % aprovadas (amendoim tailandês e noz são as mais parecidas).
- Defeitos **desenhados** nas castanhas boas (teste de sensibilidade, não são defeitos reais): mancha escura 17 de 19 rejeitadas, pedaço faltando 19 de 19, castanha inteira escurecida só 5 de 19 (o banco já tem muita película marrom).
- Bancada simulada com `AV_SIM_PHOTOS`: 18 peças passaram pela tela de Operação e pelo Modo feira com o modelo ativo; a peça de caju foi para revisão.
- Testes automatizados: calibração cruza o limiar nos dois limites; pacote sintético carrega, devolve A/B/C somando 1 com B nulo; câmera simulada usa cada foto antes de repetir e gera arquivos distintos.
