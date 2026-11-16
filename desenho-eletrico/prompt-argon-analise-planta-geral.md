# PROMPT — ARGON: AUDITORIA COMPLETA DA PLANTA ELÉTRICA + ESPECIFICAÇÃO DA PLANTA GERAL

## SEU PAPEL

Você é o **engenheiro revisor sênior** da planta elétrica do AmazonVision 4.0: uma esteira seletora de maçãs com ESP32, visão computacional, servo empurrador, motor DC e parada de emergência NR-12, que será apresentada na Feira FUCAPI 2026.
Seu trabalho tem **duas entregas**, nesta ordem:

1. **Auditoria**: visual, de ligações, de coerência e de detalhes de TUDO o que já existe no desenho.
2. **Especificação da Planta Geral**: uma folha única com o sistema inteiro, pronta para ser implementada depois, em blocos.

**NÃO edite `esp32.html` nem nenhum outro arquivo existente nesta tarefa.** Você só cria os 3 arquivos de saída listados no fim. A implementação será feita em outra rodada, depois que a especificação for aprovada.

---

## ARQUIVOS (tudo em `C:\Users\ponto\OneDrive\Desktop\FEIRA - AMA\`)

| Arquivo | O que é |
|---|---|
| `desenho-eletrico/esp32.html` | **Desenho oficial.** Aba 1 "Componentes" = Blocos 1–9 (desenho real de cada peça, com pinos). Aba 2 "Interligações" = folhas W1–W5 (fiação ponto a ponto W001–W082 + tabela geral + unifilar). |
| `desenho-eletrico/prompt-bloco04..09.md`, `prompt-blocoW1..W5.md`, `correcoes-W2.md`, `correcoes-W4.md` | O que foi pedido em cada bloco. Serve para comparar "pedido × entregue". |
| `desenho-eletrico/auditar_folha.py` | Auditor geométrico: `python auditar_folha.py wiring-N [grupo-de-fios]` (fio atravessando componente/texto, fora da moldura, XML, cores literais). Hoje passa limpo em W2 (`fios-gnd-x2-w2`), W4 e W5 (`unifilar-w5`). Use como ponto de partida, mas ele NÃO verifica eletricidade nem fidelidade dos desenhos. |
| `BOM_AmazonVision_v2.html` | Lista de materiais oficial (tags E01–E31, H01–H06, M01–M32). Os itens ficam no `<script>` (`ELETRONICA_ITEMS`, `MECANICA_ITEMS`, `INHAND_ITEMS`). |
| `amazonvision/firmware/src/board_config.h`, `main.cpp`, `motor_drivers.h` | Pinos e lógica reais do firmware (ex.: `AV_PIN_ESTOP 27`, `read_estop()`). |
| `Kit_Impressao_3D_Esteira_AmazonVision/MANUAL_IMPRESSAO_3D_BAMBU_P2S.md` §3 | Arquitetura elétrica "mono-fonte 12 V", fusíveis F1/F2/F3, sensores, servo. |
| `Planta_Eletrica_Esteira_AmazonVision.html` | **Versão antiga** (06/11), com outra nomenclatura (Q0, PS1, F1, K1, U1…). Use só para achar algo que foi esquecido na versão nova. Não é referência de verdade. |

**Como ver o desenho renderizado**: `python -m http.server 8765 --bind 127.0.0.1 --directory "C:\Users\ponto\OneDrive\Desktop\FEIRA - AMA\desenho-eletrico"` e abra `http://localhost:8765/esp32.html`. Troque de aba com `switchTab('componentes')` / `switchTab('interligacoes')` e de tema com `toggleTheme()`. Para inspecionar detalhes, amplie o SVG (ex.: `svg.style.width='4200px'`) e role até a região, em vez de dar zoom na captura reduzida. **Revise cada folha nos temas claro E escuro.**

---

## ENTREGA 1 — AUDITORIA (arquivo `desenho-eletrico/analise-argon.md`)

Audite as 14 folhas (Blocos 1–9 e W1–W5) nos 4 eixos abaixo. Cada achado precisa de **evidência concreta** (folha, linha do HTML ou coordenada SVG, texto exato) e de uma **correção proposta**. Não liste impressões genéricas.

### Eixo A — Visual
- Sobreposições: texto × texto, texto × linha, linha × corpo de componente, tags de fio encostadas.
- Legibilidade a 100% de zoom: fonte menor que 4,4 un, contraste baixo no tema escuro, cores que somem.
- Consistência entre folhas: moldura, carimbo (FOLHA n/5, data, REV), escala, espessura de linha por classe (`wire-power` 1,8, `wire-gnd` 1,4 tracejado, `wire-signal` 1,0), estilo de junction dots e pads. Atenção: a W1 usa `viewBox` 900×600 e as outras 1400×900. Avalie se isso é aceitável ou se deve ser padronizado.
- Fidelidade: cada componente copiado na W1–W4 deve bater com o desenho real do Bloco correspondente na Aba 1 (mesma geometria, mesmos nomes e posições de pinos). Verifique principalmente os que mudaram de tamanho ou foram simplificados.

### Eixo B — Ligações (elétrica de verdade)
Monte a **netlist** a partir dos paths desenhados **e** das tabelas, e confira:
- Todo fio começa e termina exatamente num pad ou terminal existente. Nenhuma ponta solta, nenhum pad de componente usado sem fio.
- Todo pino de entrada tem nível definido (pull-up/pull-down). Todo GND chega ao GND comum. Nenhuma rede flutuante.
- Níveis de tensão: saídas de 5 V dos sensores chegando a GPIO de 3,3 V só via clamp (E11 + E10 BAT54S); servo em 6 V; lógica do MOSFET D4184 em 3,3 V.
- Pinos do ESP32: strapping (0, 2, 5, 12, 15), estado no boot, pinos só-entrada (34–39), serial (1/3) e corrente por GPIO.
- Proteções: fusível por ramo × corrente real; bitola (AWG/mm²) × corrente de cada fio; diodos de roda-livre (E05 no motor, E09 no relé); capacitor E06 no servo.
- Balanço de potência da fonte E01 (12 V 10 A): motor GA37 (incluindo travado), servo em pico via buck 6 V, ring light, relé, ESP32, sensores. Os bucks E02/E03 suportam?
- **NR-12 / segurança**:
  - categoria da parada de emergência (E12 NF + E12-B em série com a bobina do K1);
  - o que o K1 corta e o que fica energizado (hoje o buck do servo E02 vem do +12V direto, Pendência 2 da W5);
  - aterramento PE da carcaça metálica da fonte (Pendência 1: W003 vai para "E27", que é a caixa plástica);
  - comportamento em falha (fio rompido, ESP32 travado, boot).
- Firmware × hardware: `read_estop()` em `main.cpp` lê `== LOW`. Com o NF do E-STOP ligado ao GND (W081), qual deve ser a lógica? Confira também a ordem de inicialização dos pinos de relé/buzzer/LEDs no boot.

### Eixo C — Coerência entre fontes
Faça a matriz e aponte cada divergência:
- Tabelas de fios de cada folha (W1–W4) × paths desenhados × tabela geral da W5 (82 linhas).
- Mapa de GPIO da W5 × destaques de GPIO nas folhas × `board_config.h`.
- Tags e quantidades da BOM × componentes desenhados. Há componente desenhado sem item na BOM, ou item da BOM sem lugar no desenho? Inclua os novos E28–E31 (BC337-40, 470 Ω, 10 kΩ, bloco NF).
- Manual §3 (F1 5 A / F2 3 A / F3 2 A, mono-fonte, sensores) × W1 (que tem um único fusível E16).
- Códigos de cor dos condutores: PT × BK, AZ × BU (neutro AC e +5 V DC ambos azuis?) e cores que a BOM não tem (E22 só tem BN/BU/BK/Vi; W3/W4 usam VD/AM/LJ).
- Numeração: W001–W082 sem buracos nem duplicatas; nomes de componentes iguais em todas as folhas (ex.: "E12-B", "Q1/Q2", "R_B2").

### Eixo D — Detalhes
Unidades e notação (vírgula decimal, mm²/AWG, Ω, µF), acentuação, erros de digitação, revisão (REV A/B) coerente com o que mudou, notas técnicas desatualizadas depois das correções, textos que ainda citam BC547 ou GPIO5 para o relé.

### Formato da Entrega 1
1. **Veredito por folha**: tabela com folha, status (Aprovada / Aprovada com ressalvas / Reprovada) e nº de achados por severidade.
2. **Achados**: tabela com `ID | Severidade (Crítico/Maior/Menor) | Eixo | Folha + localização | Evidência | Correção proposta`. Crítico = algo que queima, não funciona ou viola a NR-12. Maior = erro de ligação ou de documentação que leva a montar errado. Menor = estética ou clareza.
3. **Netlist consolidada**: em arquivo separado, `desenho-eletrico/netlist-geral.csv`, colunas `net;componente;terminal;fio;folha`. Uma linha por terminal ligado. Redes nomeadas: `+12V`, `+12V_AT`, `+6V_SV`, `+5V`, `+3V3`, `GND`, `PE`, `AC_L`, `AC_N`, `AC_L_PROT`, `AC_N_PROT` e as redes de sinal (`S1`, `S2`, `ESTOP`, `PWM_SERVO`, `PWM_MOTOR`, `RELAY_CMD`, `K1_COIL+`, `K1_COIL-`, `BUZ_CMD`, `LED_R`, `LED_G`, `LED_Y`…).
4. **Lista de correções priorizada**: o que corrigir antes da Planta Geral (bloqueante) × o que pode ir junto.

---

## ENTREGA 2 — ESPECIFICAÇÃO DA PLANTA GERAL (arquivo `desenho-eletrico/spec-planta-geral.md`)

**Objetivo**: uma folha única que mostre o sistema elétrico inteiro de uma vez, como o diagrama esquemático geral de um quadro industrial. Ela serve para entender o funcionamento, conferir na bancada e apresentar na feira. As folhas W1–W4 continuam sendo o detalhe de montagem fio a fio.

### Decisões já tomadas (respeite)
1. **Protoboard E26 não aparece na Planta Geral.** Ela é só meio de montagem e não tem função elétrica. Os trilhos viram **redes nomeadas** (`+5V`, `+3V3`, `GND`) e os circuitos montados nela (resistor E11 + clamp BAT54S E10 de cada sensor) aparecem como **componentes esquemáticos** ligados ao ESP32. Os jumpers W032–W042 aparecem como ligações normais, com o ID do fio. Uma nota no rodapé diz: "Circuitos de clamp, pull-downs e barramentos lógicos montados na protoboard E26 — ver W2". A protoboard continua na W2 e na BOM.
2. **Componentes com a identidade da Aba 1**, em versão compacta: mesmo nome, mesmos números de terminal, mesma orientação lógica dos pinos. Não use retângulos genéricos sem pinos. O ESP32 pode ser um bloco retangular com **apenas os pinos usados**, na ordem física da placa.
3. **Redes nomeadas em vez de fios longos** onde a ligação atravessaria a folha: rótulo de rede igual nas duas pontas, como em esquemáticos grandes. Alimentação com barramentos horizontais no topo (+12V, +12V_AT, +6V_SV, +5V, +3V3) e GND embaixo.
4. **Todo segmento de ligação leva o ID do fio** (W001–W082) e as redes têm a referência da folha de detalhe (ex.: "→ W3").
5. Mesmas regras de estilo das folhas W: só variáveis CSS (`var(--bg)`, `var(--fg)`, `var(--line)`, `var(--line-thin)`, `var(--pin-text)`, `var(--grid)`, `var(--grid-major)`, `var(--dim)`, `var(--trace)`, `var(--pad-fill)`, `var(--tag-bg)`, `var(--header-bg)`, `var(--header-border)`), classes `wire-power`/`wire-gnd`/`wire-signal`/`junction-dot`, IDs com sufixo `-pg`, moldura dupla e carimbo.

### O que a especificação deve conter
1. **Onde fica**: proponha e justifique. As opções são uma 3ª aba "Planta Geral" no `esp32.html` (com botão na `tab-bar` e `switchTab('planta')`) ou uma 6ª folha na Aba 2. Proponha também o `viewBox` (sugestão: proporção A1 paisagem, ex.: 2378×1682, com leitura confortável a 100%) e como fica a navegação.
2. **Zoneamento**: mapa da folha com coordenadas de cada zona. Sugestão de fluxo esquerda → direita: Entrada AC e proteção → Fonte e distribuição (X1, fusíveis) → Controle (ESP32) no centro → Segurança (E12, E12-B, K1) → Atuadores (+12V_AT: D4184 + motor; servo) → Sensores e E-STOP (X2, clamps) → Sinalização (LEDs, buzzer) e Iluminação (ring light). Mais a legenda, as notas e o carimbo.
3. **Lista de componentes**: tag, nome, símbolo/representação, posição (x, y), terminais usados com coordenadas, e de qual Bloco da Aba 1 ele vem.
4. **Lista de ligações**: para cada um dos 82 fios (mais os que a Entrega 1 criar), dizer de qual terminal a qual terminal, a rede, a classe CSS, e se é desenhado como fio ou como rótulo de rede.
5. **Correções incorporadas**: a planta já deve nascer correta. Para cada pendência que a Entrega 1 confirmar (PE da fonte, buck do servo no +12V_AT, fusíveis F1/F2/F3, lógica do E-STOP etc.), diga como ela aparece na Planta Geral. Diga também quais folhas W precisam ser corrigidas para ficar iguais a ela.
6. **Plano de implementação em blocos** (G1, G2, G3…), cada um pequeno o bastante para um prompt: o que desenhar, IDs, coordenadas e critério de aceite. Inclua o comando de verificação. Se precisar, proponha uma extensão do `auditar_folha.py` para a planta geral (ex.: checar que todo rótulo de rede aparece pelo menos 2 vezes e que todo terminal da netlist está desenhado).
7. **Riscos e perguntas em aberto**: decisões que dependem do dono do projeto (ex.: trocar a protoboard por placa perfurada soldada por causa da vibração da esteira; ring light cortado ou não pelo K1).

---

## REGRAS

- Não invente dados: se algo não está no desenho, na BOM, no firmware ou no manual, marque como "**não especificado**" e coloque nas perguntas em aberto.
- Cite sempre a fonte de cada afirmação (arquivo + linha, ou folha + coordenada).
- Datasheets: use valores típicos conhecidos (ex.: BC337-40 Ic 800 mA; MG996R pico ~2,5 A; GA37 12 V travado ~3–5 A; ring light 12 V ~0,3–0,4 A) e diga quando for estimativa.
- Escreva em português do Brasil, direto. Explique cada termo técnico em uma frase curta na primeira vez que ele aparecer, porque o dono do projeto não é eletricista.

## SAÍDAS (só estes 3 arquivos novos)

1. `desenho-eletrico/analise-argon.md`: Entrega 1.
2. `desenho-eletrico/netlist-geral.csv`: netlist consolidada.
3. `desenho-eletrico/spec-planta-geral.md`: Entrega 2.

No fim, responda em até 15 linhas: veredito geral, nº de achados críticos/maiores/menores, as 5 correções mais importantes e se a Planta Geral pode começar já ou depende de correções antes.
