# PROMPT — BLOCO W4: SINALIZAÇÃO, DADOS E PROTEÇÃO

## CONTEXTO

Voce esta editando o arquivo unico:
`file:///C:/Users/ponto/OneDrive/Desktop/FEIRA%20-%20AMA/desenho-eletrico/esp32.html`

O Bloco W4 ainda NAO existe. Voce deve SUBSTITUIR o placeholder existente:
```html
<section id="wiring-4" class="sheet-section"><h2>W4 — Em construção</h2></section>
```

Pela secao completa `<section id="wiring-4" class="sheet-section">` contendo o diagrama ponto-a-ponto da **Rede de Sinalização, Dados e Proteção: LEDs de Status (H05) + Buzzer NR-12 (E25) + Relé de Segurança (E08/E09) + Ring Light (E13)**.

**REGRA ABSOLUTA**: NAO altere NADA fora da secao `<section id="wiring-4">`. NAO toque no CSS, no script, na Tab 1, no W1, no W2, no W3, nem nos pills de navegacao.

---

## FOLHA 4/5: SINALIZAÇÃO, DADOS E PROTEÇÃO

### VIEWBOX E MOLDURA

```
viewBox="0 0 1400 900"
```

- Moldura dupla:
  - Outer: `<rect x="20" y="20" width="1360" height="860" fill="none" stroke="var(--line)" stroke-width="1.5"/>`
  - Inner: `<rect x="25" y="25" width="1350" height="850" fill="none" stroke="var(--line)" stroke-width="0.5"/>`

### PATTERN IDS (UNICOS PARA W4)

```xml
<defs>
  <pattern id="grid-w4" width="10" height="10" patternUnits="userSpaceOnUse">
    <path d="M 10 0 L 0 0 0 10" fill="none" stroke="var(--grid)" stroke-width="0.3"/>
  </pattern>
  <pattern id="grid-major-w4" width="50" height="50" patternUnits="userSpaceOnUse">
    <path d="M 50 0 L 0 0 0 50" fill="none" stroke="var(--grid-major)" stroke-width="0.6"/>
  </pattern>
  <pattern id="hatch-w4" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <line x1="0" y1="0" x2="0" y2="4" stroke="var(--line-thin)" stroke-width="0.3"/>
  </pattern>
</defs>
```

Aplicar o grid: 2 rects cobrindo todo o viewBox com `fill="url(#grid-w4)"` e `fill="url(#grid-major-w4)"`.

---

## COMPONENTES REAIS (COPIAR DO TAB 1)

**REGRA CRITICA**: Cada componente DEVE ser uma COPIA FIEL do desenho real no Tab 1 (Blocos 1-9), envolvido em um `<g>` com `transform="translate(tx, ty) scale(s) translate(ox, oy)"`. NAO desenhe blocos retangulares simplificados. Copie toda a geometria interna (corpo, terminais, textos, simbolos).

**Formula de conversao**: `SVG_x = tx + (LOCAL_x + ox) * scale` e `SVG_y = ty + (LOCAL_y + oy) * scale`
Ou equivalente: `SVG_x = tx + (LOCAL_x - |ox|) * scale` quando ox e negativo.

---

### COMPONENTE 1: ESP32 H01 — Desenho completo (do Bloco 1)

Copiar o grupo completo do ESP32 que ja foi usado no W2 (secao wiring-2, ~linha 6665) e W3. Este grupo contem TODO o ESP32 incluindo PCB, 30 pinos com nomes e descricoes, cotas de dimensoes, e o conector micro-USB.

No W4, usar id `id="esp32-devkit-w4"` (evitar ID duplicado com W2/W3).

**Transform para W4** (ESP32 na ESQUERDA, identico ao W3):
```
transform="translate(120, 80) scale(0.55) translate(-260, -60)"
```

**Tabela de verificacao dos GPIOs usados no W4**:

| Pino ESP32        | GPIO | Funcao W4          | Local cx | Local cy | SVG x  | SVG y  |
|-------------------|------|--------------------|----------|----------|--------|--------|
| Pino 25 (D5)      | 5    | RELAY_CMD (E08)   | 554      | 380      | 281.7  | 256.0  |
| Pino 26 (D17)     | 17   | LED_R (H05 verm.) | 554      | 410      | 281.7  | 272.5  |
| Pino 27 (D16)     | 16   | LED_G (H05 verde) | 554      | 440      | 281.7  | 289.0  |
| Pino 28 (D4)      | 4    | LED_Y (H05 amar.) | 554      | 470      | 281.7  | 305.5  |
| Pino 15 (D13)     | 13   | BUZZER_CMD (E25)  | 246      | 530      | 112.3  | 338.5  |

**NOTA**: GPIO2 (pino 29, D2) esta atribuido ao LED interno do ESP32 (AV_PIN_LED = 2 em board_config.h). Nao precisa de fio externo — ja esta na placa. Marcar com um badge informativo: "GPIO2 = LED INTERNO (board)".

**Destaques GPIO** (FORA do grupo transform, em coordenadas SVG absolutas):

```svg
<!-- Destaque GPIO5 (Pino 25 = D5) — RELAY CMD -->
<circle cx="282" cy="256" r="6" fill="none" stroke="var(--line)" stroke-width="2.5"/>
<rect x="298" y="249" width="84" height="14" rx="2" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.2"/>
<text x="340" y="259" text-anchor="middle" font-size="6.5" font-weight="bold" fill="var(--fg)">GPIO5 → RELÉ K1</text>

<!-- Destaque GPIO17 (Pino 26 = D17) — LED VERMELHO -->
<circle cx="282" cy="273" r="6" fill="none" stroke="var(--line)" stroke-width="2.5"/>
<rect x="298" y="266" width="78" height="14" rx="2" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.2"/>
<text x="337" y="276" text-anchor="middle" font-size="6.5" font-weight="bold" fill="var(--fg)">GPIO17 → LED R</text>

<!-- Destaque GPIO16 (Pino 27 = D16) — LED VERDE -->
<circle cx="282" cy="289" r="6" fill="none" stroke="var(--line)" stroke-width="2.5"/>
<rect x="298" y="282" width="78" height="14" rx="2" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.2"/>
<text x="337" y="292" text-anchor="middle" font-size="6.5" font-weight="bold" fill="var(--fg)">GPIO16 → LED G</text>

<!-- Destaque GPIO4 (Pino 28 = D4) — LED AMARELO -->
<circle cx="282" cy="306" r="6" fill="none" stroke="var(--line)" stroke-width="2.5"/>
<rect x="298" y="299" width="78" height="14" rx="2" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.2"/>
<text x="337" y="309" text-anchor="middle" font-size="6.5" font-weight="bold" fill="var(--fg)">GPIO4 → LED Y</text>

<!-- Destaque GPIO13 (Pino 15 = D13) — BUZZER (LADO ESQUERDO) -->
<circle cx="112" cy="339" r="6" fill="none" stroke="var(--line)" stroke-width="2.5"/>
<rect x="30" y="332" width="74" height="14" rx="2" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.2"/>
<text x="67" y="342" text-anchor="middle" font-size="6.5" font-weight="bold" fill="var(--fg)">GPIO13 → BUZ</text>

<!-- Badge informativo GPIO2 (LED INTERNO — sem fio externo) -->
<rect x="298" y="315" width="88" height="14" rx="2" fill="var(--bg)" stroke="var(--line-thin)" stroke-width="0.8" stroke-dasharray="3 2"/>
<text x="342" y="325" text-anchor="middle" font-size="5.5" fill="var(--dim)">GPIO2 = LED INTERNO</text>
```

---

### COMPONENTE 2: Kit LEDs H05 (R/G/Y + R330Ω) — Do Bloco 7

Copiar do Bloco 7 (secao `id="bloco-7"`, linhas ~3676-3857) o desenho do kit H05.

**O que copiar**: tag H05, os 3 corpos de LED (vermelho, verde, amarelo) com domes, terminais longos/curtos, lentes, os 6 pads through-hole (R+, R-, G+, G-, Y+, Y-) com seus textos (ANODO, CATODO), o diagrama de circuito serie (GPIO→R330Ω→LED→GND) e a linha de corrente "If = ~3.6-4.5 mA".

**O que NAO copiar**: cotas externas (Ø5mm), box de notas normativas (rect x=600 y=380), box de firmware/integracao.

**Posicao alvo**: Superior-centro (zona LEDs, ~x=480, y=55).
**Transform**: `translate(480, 55) scale(0.60) translate(-616, -80)`

**Verificacao dos terminais H05**:

| Terminal        | Local x | Local y | SVG x                           | SVG y                          |
|-----------------|---------|---------|--------------------------------|-------------------------------|
| R+ (anodo R)    | 616     | 305     | 480 + (616-616)*0.60 = 480.0  | 55 + (305-80)*0.60 = 190.0   |
| R- (catodo R)   | 650     | 305     | 480 + (650-616)*0.60 = 500.4  | 190.0                         |
| G+ (anodo G)    | 700     | 305     | 480 + (700-616)*0.60 = 530.4  | 190.0                         |
| G- (catodo G)   | 734     | 305     | 480 + (734-616)*0.60 = 550.8  | 190.0                         |
| Y+ (anodo Y)    | 784     | 305     | 480 + (784-616)*0.60 = 580.8  | 190.0                         |
| Y- (catodo Y)   | 818     | 305     | 480 + (818-616)*0.60 = 601.2  | 190.0                         |

Esses 6 pads sao os pontos de conexao dos fios W059-W064.

---

### COMPONENTE 3: Buzzer 5V Ativo E25 — Do Bloco 8

Copiar do Bloco 8 (secao `id="bloco-8"`, linhas ~4092-4231) o desenho do buzzer E25.

**O que copiar**: tag E25, corpo cilindrico com dome (rect + path curvo), marca de polaridade (+), textos (ATIVO, 5V DC), terminais radiais (pinos longos e curtos), vista superior/simbolo, circuito de acionamento com transistor NPN (o retangulo com o esquematico completo: +5V→Buzzer→Coletor Q1, 1kΩ na base, emissor→GND), tabela NR-12, e os 2 pads through-hole (+, -) com textos.

**O que NAO copiar**: cotas externas (Ø12mm, 9.5mm, pitch 6.5mm).

**Posicao alvo**: Centro-esquerda (zona buzzer, ~x=520, y=280).
**Transform**: `translate(520, 280) scale(0.50) translate(-395, -95)`

**Verificacao dos terminais E25**:

| Terminal | Local x | Local y | SVG x                          | SVG y                          |
|----------|---------|---------|-------------------------------|-------------------------------|
| + (pos)  | 380     | 325     | 520 + (380-395)*0.50 = 512.5  | 280 + (325-95)*0.50 = 395.0  |
| - (neg)  | 480     | 325     | 520 + (480-395)*0.50 = 562.5  | 395.0                         |

---

### COMPONENTE 4: Relé Automotivo 12V/40A E08 + Soquete — Do Bloco 3

Copiar do Bloco 3 (secao `id="bloco-3"`, linhas ~1655-1794) o desenho completo do rele E08 incluindo corpo do rele, soquete 5 terminais, esquema de contatos (COM/NA/NF), e diodo flyback E09.

**O que copiar**: tag E08, corpo do rele (rect 120×110 com texto "RELÉ 12V / 40A", simbolo bobina, esquema de contatos COM/NF/NA), soquete abaixo (rect 120×120 com os 5 slots de pino), os 5 terminais through-hole pads (85, 86, 30, 87a, 87), E09 flyback (corpo, simbolo diodo, pads K e A, textos "1N4007 DIODO FLYBACK").

**O que NAO copiar**: cotas externas (28mm largura, 28mm altura), texto de rodape "Relé K1 — Seccionamento NR-12".

**Posicao alvo**: Centro-direita (zona rele, ~x=750, y=260).
**Transform**: `translate(750, 260) scale(0.50) translate(-690, -120)`

**Verificacao dos terminais E08 e E09**:

| Terminal                     | Local x | Local y | SVG x                          | SVG y                          |
|------------------------------|---------|---------|-------------------------------|-------------------------------|
| E08:85 (bobina+ COMANDO)     | 600     | 285     | 750 + (600-690)*0.50 = 705.0  | 260 + (285-120)*0.50 = 342.5  |
| E08:86 (bobina- GND)         | 772     | 285     | 750 + (772-690)*0.50 = 791.0  | 342.5                         |
| E08:30 (COM +12V IN)         | 642     | 402     | 750 + (642-690)*0.50 = 726.0  | 260 + (402-120)*0.50 = 401.0  |
| E08:87a (NF — N.C.)          | 690     | 402     | 750 + (690-690)*0.50 = 750.0  | 401.0                         |
| E08:87 (NA +12V_AT)          | 738     | 402     | 750 + (738-690)*0.50 = 774.0  | 401.0                         |
| E09:K (catodo 1N4007)        | 830     | 212     | 750 + (830-690)*0.50 = 820.0  | 260 + (212-120)*0.50 = 306.0  |
| E09:A (anodo 1N4007)         | 830     | 268     | 750 + (830-690)*0.50 = 820.0  | 260 + (268-120)*0.50 = 334.0  |

---

### COMPONENTE 5: Ring Light LED 12V E13 — Do Bloco 8

Copiar do Bloco 8 (secao `id="bloco-8"`, linhas ~3950-4079) o desenho do ring light E13.

**O que copiar**: tag E13, anel circular externo (circle r=42), furo central (circle r=24), LEDs SMD distribuidos (16 quadradinhos rotacionados), terminais soldados no anel (+, -), mira optica "WEBCAM E14", vista lateral em corte simplificada, diagrama de ligacao simplificado (bloco retangular), e os 2 pads through-hole (+12V, GND) com textos.

**O que NAO copiar**: cotas externas (Ø80-90mm, Ø50mm furo, 8mm espessura), box de especificacoes tecnicas (rect x=40 y=244), notas de aplicacao/visao (rect x=40 y=375).

**Posicao alvo**: Inferior-centro (zona iluminacao, ~x=500, y=480).
**Transform**: `translate(500, 480) scale(0.50) translate(-115, -42)`

**Verificacao dos terminais E13**:

| Terminal       | Local x | Local y | SVG x                         | SVG y                          |
|----------------|---------|---------|------------------------------|-------------------------------|
| +12V           | 95      | 325     | 500 + (95-115)*0.50 = 490.0  | 480 + (325-42)*0.50 = 621.5  |
| GND            | 195     | 325     | 500 + (195-115)*0.50 = 540.0 | 621.5                         |

---

## CIRCUITOS DE DRIVER (TRANSISTORES NPN)

Os componentes E25 (buzzer) e E08 (rele) requerem transistores NPN para acionamento, pois suas correntes excedem o limite de 12mA dos GPIOs do ESP32. Estes NAO tem desenho de Block no Tab 1 — devem ser desenhados como **simbolos esquematicos inline** no diagrama W4.

### TRANSISTOR Q1 — Driver do Buzzer E25

Desenhar um simbolo NPN padrao (circulo r~10, linhas B/C/E com seta no emissor) posicionado abaixo do pad E25:-, em **SVG (562, 430)**. Label "Q1" acima e "BC547" abaixo.

- **Q1:B (base)**: ponto de conexao na esquerda (~SVG 552, 430)
- **Q1:C (coletor)**: ponto de conexao no topo (~SVG 562, 420) — conecta ao E25:- (pad 562.5, 395)
- **Q1:E (emissor)**: ponto de conexao na base (~SVG 562, 440) — desce ate GND rail

Entre GPIO13 e Q1:B, desenhar um **resistor inline** (retangulo 24×8 com texto "1kΩ") rotulado "E11" na posicao aproximada SVG (450, 426). O fio W067 vai do GPIO13 (112, 339) horizontalmente ate o resistor, e depois ate Q1:B.

### TRANSISTOR Q2 — Driver do Relé E08

Desenhar um simbolo NPN padrao posicionado abaixo do pad E08:86, em **SVG (791, 380)**. Label "Q2" acima e "BC547" abaixo.

- **Q2:B (base)**: ponto de conexao na esquerda (~SVG 781, 380)
- **Q2:C (coletor)**: ponto de conexao no topo (~SVG 791, 370) — conecta ao E08:86 (pad 791, 342.5)
- **Q2:E (emissor)**: ponto de conexao na base (~SVG 791, 390) — desce ate GND rail

Entre GPIO5 e Q2:B, desenhar um **resistor inline** (retangulo 24×8 com texto "1kΩ") rotulado "E11" na posicao aproximada SVG (650, 376). O fio W071 vai do GPIO5 (282, 256) com curvas ate o resistor, e depois ate Q2:B.

**Estilo dos transistores**: circulo `fill="var(--bg)" stroke="var(--line)" stroke-width="1"`. Linhas internas: `stroke="var(--line)" stroke-width="1"`. Seta do emissor: `fill="var(--line)"`. Textos: `fill="var(--fg)"` para labels, `fill="var(--dim)"` para tipo (BC547).

**Estilo dos resistores inline**: `fill="var(--bg)" stroke="var(--line)" stroke-width="1"`. Texto: `fill="var(--fg)" font-size="5" font-weight="bold"`.

---

## ZONAS DE LAYOUT (1400×900)

```
+---------------------------------------------------------------------+
|  LEGENDA (x=40-800, y=30-50)                                        |
|  "SINALIZAÇÃO, DADOS E PROTEÇÃO — LEDs + BUZZER + RELÉ + RING"     |
+----------+------------------------------------------+---------------+
|          |  ZONA SUPERIOR: LEDS DE STATUS             |               |
|  ESP32   |  H05 (R/G/Y + R330Ω, x=470-610, y=50-200)|               |
|  H01     |  3 fios signal + 3 fios GND               |    TABELA     |
|  (LEFT)  |                                            |    DE FIOS    |
|  x=30    |  +12V RAIL (y~230, x=400-850)              |    (20 regs   |
|  -387    |  +5V RAIL (y~260, x=400-570, curto)        |    W059-W078) |
|  y=80    |                                            |    x=1050     |
|  -410    |  ZONA CENTRAL: BUZZER + RELÉ               |    -1370      |
|          |  E25 Buzzer+Q1 (x=500-580, y=280-450)      |    y=40-560   |
|          |  E08 Relé+E09+Q2 (x=700-840, y=260-420)    |               |
|          |                                            |               |
|          |  +12V_AT RAIL (y~450, x=750-1040)           |               |
|          |                                            |               |
|          |  ZONA INFERIOR: RING LIGHT                  |               |
|          |  E13 (x=480-560, y=480-630)                 |               |
|          |                                            |               |
|          |  GND RAIL (y~660, x=40-1040, tracejado)     |               |
+----------+------------------------------------------+               |
|  NOTAS TECNICAS (5 itens)                                           |
|  x=40-1040, y=690-830                                               |
+---------------------------------------------+-----------------------+
|                                              |  BLOCO DE TITULO      |
|                                              |  x=1050-1370          |
|                                              |  y=780-860            |
+----------------------------------------------+-----------------------+
```

**Fluxo de sinais** (esquerda → direita):
- LEDs: ESP32 GPIO17/16/4 → fios signal → H05 anodos R+/G+/Y+ (via R330Ω interno) → catodos → GND
- Buzzer: ESP32 GPIO13 → 1kΩ E11 → Q1:B → Q1 comuta → E25 ativado por +5V
- Rele: ESP32 GPIO5 → 1kΩ E11 → Q2:B → Q2 comuta → E08 bobina energizada → pino 87 (NA) fecha → +12V_AT ativo
- Ring Light: +12V direto → E13 (sempre ligado)

---

## BARRAMENTOS DE REFERENCIA

Desenhar 4 barramentos visuais:

1. **+12V** (rail principal): linha horizontal grossa (~y=230, x=400-850)
   - Classe: `wire-power` (stroke 1.8)
   - Label retangular: "+12V (FONTE E01)"
   - Conecta: E08:85 (bobina), E08:30 (COM), E13:+12V
   - Indicar com seta "← W1" na extremidade esquerda

2. **+5V** (rail logica/buzzer): linha horizontal grossa (~y=260, x=400-570)
   - Classe: `wire-power` (stroke 1.8)
   - Label retangular: "+5V (BUCK E03)"
   - Conecta: E25:+ (buzzer)
   - Segmento curto (so vai ate o buzzer)
   - Indicar com seta "← W1" na extremidade esquerda

3. **+12V_AT** (rail atuadores, saida rele): linha horizontal grossa (~y=450, x=774-1040)
   - Classe: `wire-power` (stroke 1.8)
   - Label retangular: "+12V_AT (SAÍDA RELÉ → W3)"
   - Vem do E08:87 (NA)
   - Indicar com seta "→ W3 (Atuadores)" na extremidade direita

4. **GND** (terra comum): linha horizontal tracejada (~y=660, x=40-1040)
   - Classe: `wire-gnd` (stroke 1.4 dashed)
   - Label: "GND (COMUM)"
   - Simbolo de terra (3 linhas horizontais decrescentes) nas extremidades

---

## TABELA DE FIOS (20 CABOS: W059 — W078)

### CIRCUITO LEDs DE STATUS H05 (6 fios: W059-W064)

| ID    | DE                              | PARA                      | CLASSE      | COR REAL    | SECAO   | NOTA                                                  |
|-------|---------------------------------|---------------------------|-------------|-------------|---------|-------------------------------------------------------|
| W059  | H01:GPIO17 (D17, pino 26)      | H05:R+ (anodo vermelho)   | wire-signal | Vermelho    | 26 AWG  | GPIO→R330Ω→LED R (ERRO / E-STOP ativo)               |
| W060  | H05:R- (catodo vermelho)        | Barramento GND             | wire-gnd    | Preto       | 26 AWG  | Retorno GND LED vermelho                             |
| W061  | H01:GPIO16 (D16, pino 27)      | H05:G+ (anodo verde)      | wire-signal | Verde       | 26 AWG  | GPIO→R330Ω→LED G (OPERANDO / OK)                     |
| W062  | H05:G- (catodo verde)           | Barramento GND             | wire-gnd    | Preto       | 26 AWG  | Retorno GND LED verde                                |
| W063  | H01:GPIO4 (D4, pino 28)        | H05:Y+ (anodo amarelo)    | wire-signal | Amarelo     | 26 AWG  | GPIO→R330Ω→LED Y (PROCESSANDO / Classificando)       |
| W064  | H05:Y- (catodo amarelo)         | Barramento GND             | wire-gnd    | Preto       | 26 AWG  | Retorno GND LED amarelo                              |

### CIRCUITO BUZZER NR-12 E25 (4 fios: W065-W068)

| ID    | DE                              | PARA                      | CLASSE      | COR REAL    | SECAO   | NOTA                                                  |
|-------|---------------------------------|---------------------------|-------------|-------------|---------|-------------------------------------------------------|
| W065  | +5V rail (E03 Buck)             | E25:+ (buzzer positivo)   | wire-power  | Vermelho    | 22 AWG  | Alimentação buzzer 5V ativo                          |
| W066  | E25:- (buzzer negativo)         | Q1:C (coletor NPN)        | wire-signal | — (curto)   | 26 AWG  | Buzzer negativo → coletor Q1                         |
| W067  | H01:GPIO13 (D13, pino 15)      | Q1:B (base NPN via 1kΩ)  | wire-signal | Laranja     | 26 AWG  | Comando buzzer: GPIO13→E11(1kΩ)→base Q1             |
| W068  | Q1:E (emissor NPN)             | Barramento GND             | wire-gnd    | Preto       | 26 AWG  | Terra circuito buzzer via emissor Q1                 |

### CIRCUITO RELÉ NR-12 E08 + FLYBACK E09 (6 fios: W069-W074)

| ID    | DE                              | PARA                      | CLASSE      | COR REAL    | SECAO   | NOTA                                                  |
|-------|---------------------------------|---------------------------|-------------|-------------|---------|-------------------------------------------------------|
| W069  | +12V rail (E01)                 | E08:85 (bobina+ COMANDO)  | wire-power  | Vermelho    | 22 AWG  | +12V → bobina+ rele K1 (150-200mA)                  |
| W070  | E08:86 (bobina- GND)           | Q2:C (coletor NPN)        | wire-signal | — (curto)   | 22 AWG  | Bobina- → coletor Q2 (comutacao low-side)            |
| W071  | H01:GPIO5 (D5, pino 25)        | Q2:B (base NPN via 1kΩ)  | wire-signal | Laranja     | 26 AWG  | Comando rele: GPIO5→E11(1kΩ)→base Q2                |
| W072  | Q2:E (emissor NPN)             | Barramento GND             | wire-gnd    | Preto       | 22 AWG  | Terra circuito rele via emissor Q2                   |
| W073  | E09:K (catodo 1N4007)          | Juncao E08:85 (+12V bob)  | wire-signal | — (axial)   | 22 AWG  | Flyback: catodo → bobina+ (supressao surto)          |
| W074  | E09:A (anodo 1N4007)           | Juncao E08:86 (bobina-)   | wire-signal | — (axial)   | 22 AWG  | Flyback: anodo → bobina- (supressao surto)           |

### COMUTAÇÃO DE POTÊNCIA E08 (2 fios: W075-W076)

| ID    | DE                              | PARA                      | CLASSE      | COR REAL    | SECAO   | NOTA                                                  |
|-------|---------------------------------|---------------------------|-------------|-------------|---------|-------------------------------------------------------|
| W075  | +12V rail (E01)                 | E08:30 (COM +12V IN)      | wire-power  | Vermelho    | 14 AWG  | Entrada potencia +12V no rele (ate 40A)              |
| W076  | E08:87 (NA +12V_AT saida)      | +12V_AT rail (atuadores)  | wire-power  | Vermelho    | 14 AWG  | Saida +12V_AT seccionada pelo rele NR-12             |

### RING LIGHT E13 (2 fios: W077-W078)

| ID    | DE                              | PARA                      | CLASSE      | COR REAL    | SECAO   | NOTA                                                  |
|-------|---------------------------------|---------------------------|-------------|-------------|---------|-------------------------------------------------------|
| W077  | +12V rail (E01)                 | E13:+12V (alimentação)    | wire-power  | Vermelho    | 22 AWG  | Alimentação ring light 12V (sempre ligado)           |
| W078  | E13:GND (retorno)              | Barramento GND             | wire-gnd    | Preto       | 22 AWG  | Terra ring light                                      |

### JUNCOES (junction dots obrigatorios)

Colocar `<circle class="junction-dot">` preenchido nos seguintes nos:

1. **+12V rail**: onde W069 (bobina rele), W075 (COM rele), W077 (ring light) saem do barramento +12V
2. **+5V rail**: onde W065 (buzzer) sai do barramento +5V
3. **E08:85**: onde W069 (alimentacao bobina) e W073 (catodo flyback) se encontram
4. **E08:86**: onde W070 (bobina-/coletor Q2) e W074 (anodo flyback) se encontram
5. **GND bus**: pontos onde W060, W062, W064, W068, W072, W078 chegam ao barramento GND (minimo 3 dots agrupados)
6. **GPIO pads**: onde cada fio de sinal (W059, W061, W063, W067, W071) parte do pad do ESP32

---

## WIRE TAGS E LABELS

Cada fio deve ter:
1. **Wire tag**: retangulo `<rect class="wire-tag">` com fill `var(--tag-bg)` proximo ao meio do percurso
2. **Wire label**: `<text class="wire-label">` com o ID do fio (ex: "W059")
3. **Wire spec**: `<text class="wire-spec">` com a especificacao curta (ex: "LED R 26AWG" ou "RELAY 14AWG")

Posicionar os tags para NAO sobrepor outros elementos. Em percursos longos com curvas, colocar o tag no segmento mais longo.

---

## NOTAS TECNICAS (caixa x=40-1040, y=690-830)

Desenhar um retangulo com fundo `var(--bg)`, borda `var(--line)`, titulo "NOTAS TECNICAS — W4" em negrito. Conteudo:

**NOTA 1 — Status LEDs H05 (R/G/Y)**:
3 LEDs de 5mm com resistores de 330Ω em serie (inclusos no kit H05). Corrente por LED: If = (3.3V - Vf) / 330Ω ≈ 3.6-4.5 mA (dentro do limite 12mA GPIO ESP32). Funcoes: Vermelho = ERRO / E-STOP ativo, Verde = OPERANDO / OK, Amarelo = PROCESSANDO / Classificando. GPIOs **propostos** (NAO definidos em board_config.h): GPIO17 (R), GPIO16 (G), GPIO4 (Y). Acionar via `digitalWrite(pin, HIGH)`.

**NOTA 2 — Buzzer NR-12 E25**:
Buzzer ativo 5V com oscilador interno (~2.3kHz, ~85dB @ 10cm). Corrente ~30-80mA excede limite GPIO (12mA), por isso acionado via transistor NPN Q1 (BC547) com resistor de base E11 (1kΩ). Ib = (3.3V - 0.7V) / 1kΩ = 2.6mA, hFE min 100 → Ic max = 260mA (margem ampla). NR-12 exige: som continuo em E-STOP, intermitente em falha de sensor, desligado em operacao normal. GPIO **proposto**: GPIO13. Ref: NAO definido em board_config.h — a definir como `AV_PIN_BUZZER`.

**NOTA 3 — Rele de Seguranca K1 (E08 + E09)**:
Rele automotivo 12V/40A com soquete 5 terminais. Bobina: pinos 85/86, ~150-200mA (excede GPIO → NPN Q2 obrigatorio). E09 (1N4007) em anti-paralelo com a bobina para supressao de surto indutivo (CEMF). Comutacao: pino 30 (COM) recebe +12V da fonte E01, pino 87 (NA) fornece +12V_AT seccionado para os atuadores (W3). Com GPIO5 LOW → rele desarmado → +12V_AT cortado (requisito NR-12: E-STOP desliga atuadores). GPIO **proposto**: GPIO5. Ref: NAO definido em board_config.h — a definir como `AV_PIN_RELAY`.

**NOTA 4 — Ring Light E13 (Iluminacao para Visao Computacional)**:
Anel LED 12V/6000K (~3-5W, ~250-400mA). Montado no teto da cupula optica, ilumina a area da webcam E14. Branco frio 6000K maximiza contraste para deteccao de cor e textura da castanha. Ligacao direta ao barramento +12V (sempre ligado quando sistema energizado). Alternativa: ligar via rele E08:87 para corte NR-12 (ring light desliga junto com atuadores).

**NOTA 5 — Secoes de fio e protecao**:
Comutacao de potencia rele (W075/W076): 14 AWG (ate 40A nominal). Circuito bobina rele (W069-W074): 22 AWG (~200mA). Ring light (W077/W078): 22 AWG (~400mA). Buzzer alimentacao (W065): 22 AWG (~80mA). Sinais GPIO LEDs (W059/W061/W063): 26 AWG (~4.5mA). Sinais comando (W067/W071): 26 AWG (~2.6mA). Retornos GND LEDs/buzzer (W060/W062/W064/W066/W068): 26 AWG. Retorno GND rele (W072): 22 AWG.

---

## BLOCO DE TITULO

Posicao: canto inferior-direito (x=1050, y=780, largura 320, altura 80).

Retangulo com borda `var(--line)` stroke 1.5 e fundo `var(--header-bg)`.
Linha separadora horizontal no topo do bloco.

Conteudo (textos com fill `var(--fg)` e `var(--dim)`):

```
PLANTA ELETRICA — AMAZONVISION 4.0
FOLHA 4/5: SINALIZAÇÃO, DADOS E PROTEÇÃO
ARQUIVO: esp32.html | SECAO: wiring-4
DATA: NOV 2026 | REV A
DES.: D.S. / AMA
```

---

## REGRAS INVIOLAVEIS

1. **SOMENTE** variaveis CSS para cores: `var(--bg)`, `var(--fg)`, `var(--line)`, `var(--line-thin)`, `var(--pin-text)`, `var(--grid)`, `var(--grid-major)`, `var(--dim)`, `var(--trace)`, `var(--pad-fill)`, `var(--tag-bg)`, `var(--header-bg)`, `var(--header-border)`. **NUNCA** cores literais como `#fff`, `black`, `rgb()`, `white`, `red`, etc.

2. **NAO altere** CSS, script, Tab 1, W1, W2, W3, nav pills, nem nada fora de `<section id="wiring-4">`.

3. **Pattern IDs UNICOS**: `grid-w4`, `grid-major-w4`, `hatch-w4`. Se precisar de marker para setas de fluxo: `arrow-w4`.

4. **IDs de grupo UNICOS**: Todos os `<g id="...">` dentro de W4 devem ter sufixo `-w4` ou nomes unicos que NAO colidam com W1, W2 ou W3.

5. **Pads through-hole**: SEMPRE dois circulos concentricos:
   - Externo: `r="5"` ou `r="4.5"`, `fill="var(--pad-fill)"`, `stroke="var(--line)"`, `stroke-width="1"`
   - Interno: `r="2"` ou `r="1.8"`, `fill="var(--bg)"`, `stroke="var(--line)"`, `stroke-width="0.5"`

6. **Classes de fio** (ja definidas no CSS global):
   - `.wire-power`: stroke 1.8px solido (alimentacao +12V, +5V)
   - `.wire-gnd`: stroke 1.4px tracejado (terra/GND)
   - `.wire-signal`: stroke 1.0px solido (sinais logicos GPIO, curtos entre componentes)

7. **Wire tags**: `<rect class="wire-tag">` com fill `var(--tag-bg)` + `<text class="wire-label">` para ID + `<text class="wire-spec">` para especificacao.

8. **Junction dots**: `<circle class="junction-dot">` preenchido (fill `var(--fg)`) em cada ponto de juncao onde 3+ fios se encontram.

9. **Componentes REAIS**: Usar `transform="translate(tx,ty) scale(s) translate(ox,oy)"` para posicionar copias dos desenhos do Tab 1. NUNCA blocos retangulares simplificados. Copiar TODA a geometria interna fidedignamente. Excecao: transistores Q1/Q2 e resistores de base sao simbolos esquematicos inline (nao tem Block no Tab 1).

10. **Fios conectam terminais**: Os paths dos fios devem INICIAR e TERMINAR exatamente nas coordenadas SVG calculadas dos pads through-hole dos componentes (ou nos terminais dos transistores Q1/Q2). NUNCA em pontos arbitrarios no ar.

11. **Sem sobreposicao**: Nenhum texto ou elemento grafico deve sobrepor outro. Verificar especialmente:
    - Tags de fio NAO sobrepondo componentes
    - Descricoes dos pinos do ESP32 NAO sobrepondo fios
    - Barramentos NAO passando por cima de textos
    - Transistores Q1/Q2 NAO sobrepondo pads dos componentes adjacentes
    - Resistores inline NAO sobrepondo wire tags

12. **Secao wrapper**: `<section id="wiring-4" class="sheet-section">`

---

## CHECKLIST DE VALIDACAO

Antes de finalizar, verificar TODOS os itens:

- [ ] 20 fios presentes (W059-W078) — todos com paths validos
- [ ] 5 componentes reais desenhados com transform (H01, H05, E25, E08+E09, E13)
- [ ] Cada componente e copia fiel do Tab 1 (NAO bloco simplificado)
- [ ] 2 transistores NPN desenhados como simbolos esquematicos (Q1, Q2)
- [ ] 2 resistores de base 1kΩ (E11) desenhados inline
- [ ] ZERO cores literais — somente variaveis CSS em TODO o SVG
- [ ] Pattern IDs unicos (grid-w4, grid-major-w4, hatch-w4)
- [ ] IDs de grupo unicos (sem colisao com W1/W2/W3)
- [ ] Moldura dupla correta para viewBox 1400×900
- [ ] Todos os pads through-hole com 2 circulos concentricos
- [ ] Tabela de fios completa (20 registros com todas as colunas)
- [ ] Bloco de titulo correto (FOLHA 4/5, NOV 2026, REV A)
- [ ] 5 notas tecnicas presentes e precisas
- [ ] 4 barramentos de referencia desenhados (+12V, +5V, +12V_AT, GND)
- [ ] Fios de alimentacao (+12V, +5V) usando classe `wire-power`
- [ ] Fios GND usando classe `wire-gnd` (tracejado)
- [ ] Fios de sinal (GPIO) usando classe `wire-signal`
- [ ] ESP32 inteiro dentro da moldura (todos elementos > x=25, > y=25, < x=1350, < y=850)
- [ ] 5 destaques GPIO com circulos e badges corretos (GPIO5/17/16/4/13)
- [ ] Badge informativo GPIO2 = LED INTERNO
- [ ] Fio W059 terminando no pad H05:R+ (SVG ≈ 480, 190)
- [ ] Fio W067 terminando no Q1:B via resistor 1kΩ
- [ ] Fio W071 terminando no Q2:B via resistor 1kΩ
- [ ] Flyback E09 conectado corretamente: K→E08:85, A→E08:86
- [ ] Comutacao rele: +12V→E08:30(COM), E08:87(NA)→+12V_AT
- [ ] Ring light E13 conectado direto ao +12V (sem rele)
- [ ] Nenhum texto ou elemento sobrepondo outro
- [ ] Transistores Q1/Q2 com simbolo NPN completo (circulo, B/C/E, seta emissor)
