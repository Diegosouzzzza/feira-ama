# PROMPT — BLOCO W3: REDE DE ATUADORES (SERVOS + MOTOR)

## CONTEXTO

Voce esta editando o arquivo unico:
`file:///C:/Users/ponto/OneDrive/Desktop/FEIRA%20-%20AMA/desenho-eletrico/esp32.html`

O Bloco W3 ainda NAO existe. Voce deve SUBSTITUIR o placeholder existente:
```html
<section id="wiring-3" class="sheet-section"><h2>W3 — Em construção</h2></section>
```

Pela secao completa `<section id="wiring-3" class="sheet-section">` contendo o diagrama ponto-a-ponto da **Rede de Atuadores: Servo MG996R + Motor GA37-520**.

**REGRA ABSOLUTA**: NAO altere NADA fora da secao `<section id="wiring-3">`. NAO toque no CSS, no script, na Tab 1, no W1, no W2, nem nos pills de navegacao.

---

## FOLHA 3/5: REDE DE ATUADORES — SERVOS + MOTOR

### VIEWBOX E MOLDURA

```
viewBox="0 0 1400 900"
```

- Moldura dupla:
  - Outer: `<rect x="20" y="20" width="1360" height="860" fill="none" stroke="var(--line)" stroke-width="1.5"/>`
  - Inner: `<rect x="25" y="25" width="1350" height="850" fill="none" stroke="var(--line)" stroke-width="0.5"/>`

### PATTERN IDS (UNICOS PARA W3)

```xml
<defs>
  <pattern id="grid-w3" width="10" height="10" patternUnits="userSpaceOnUse">
    <path d="M 10 0 L 0 0 0 10" fill="none" stroke="var(--grid)" stroke-width="0.3"/>
  </pattern>
  <pattern id="grid-major-w3" width="50" height="50" patternUnits="userSpaceOnUse">
    <path d="M 50 0 L 0 0 0 50" fill="none" stroke="var(--grid-major)" stroke-width="0.6"/>
  </pattern>
  <pattern id="hatch-w3" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <line x1="0" y1="0" x2="0" y2="4" stroke="var(--line-thin)" stroke-width="0.3"/>
  </pattern>
</defs>
```

Aplicar o grid: 2 rects cobrindo todo o viewBox com `fill="url(#grid-w3)"` e `fill="url(#grid-major-w3)"`.

---

## COMPONENTES REAIS (COPIAR DO TAB 1)

**REGRA CRITICA**: Cada componente DEVE ser uma COPIA FIEL do desenho real no Tab 1 (Blocos 1-9), envolvido em um `<g>` com `transform="translate(tx, ty) scale(s) translate(ox, oy)"`. NAO desenhe blocos retangulares simplificados. Copie toda a geometria interna (corpo, terminais, textos, simbolos).

**Formula de conversao**: `SVG_x = tx + (LOCAL_x + ox) * scale` e `SVG_y = ty + (LOCAL_y + oy) * scale`
Ou equivalente: `SVG_x = tx + (LOCAL_x - |ox|) * scale` quando ox e negativo.

---

### COMPONENTE 1: ESP32 H01 — Desenho completo (do Bloco 1)

Copiar o grupo `<g id="esp32-devkit-completo">` que ja foi usado no W2 (secao wiring-2, ~linha 6665). Este grupo contem TODO o ESP32 incluindo PCB verde, 30 pinos com nomes e descricoes, cotas de dimensoes, e o conector micro-USB.

No W3, renomear o id para `id="esp32-devkit-w3"` (evitar ID duplicado com W2).

**Transform para W3** (ESP32 na ESQUERDA, pinos DIREITOS voltados para os atuadores):
```
transform="translate(120, 80) scale(0.55) translate(-260, -60)"
```

**Tabela de verificacao** (formula: `SVG_x = 120 + (LOCAL_x - 260) * 0.55`, `SVG_y = 80 + (LOCAL_y - 60) * 0.55`):

| Elemento                        | Local x  | Local y | SVG x   | SVG y   | OK?           |
|---------------------------------|----------|---------|---------|---------|---------------|
| Desc pino esquerdo (x=95)       | 95       | —       | 29.25   | —       | ✅ (> 25)     |
| Corpo PCB esquerda (x=260)      | 260      | —       | 120     | —       | ✅            |
| Corpo PCB direita (x=540)       | 540      | —       | 274     | —       | ✅            |
| Pad pino direito (cx=554)       | 554      | —       | 281.7   | —       | ✅            |
| Desc pino direito (x=705)       | 705      | —       | 364.75  | —       | ✅            |
| Cota de altura (x=745)          | 745      | —       | 386.75  | —       | ✅ (< 1350)   |
| Corpo topo (y=100)              | —        | 100     | —       | 102     | ✅ (> 25)     |
| Corpo base (y=660)              | —        | 660     | —       | 410     | ✅ (< 850)    |
| **GPIO18 pad (pino 24, D18)**   | **554**  | **350** | **282** | **239.5** | ✅ SERVO    |
| **GPIO19 pad (pino 23, D19)**   | **554**  | **320** | **282** | **223**   | ✅ MOTOR    |

**Destaques GPIO** (FORA do grupo transform, em coordenadas SVG absolutas):

```svg
<!-- Destaque GPIO18 (Pino 24 = D18) — SERVO PWM -->
<circle cx="282" cy="240" r="6" fill="none" stroke="var(--line)" stroke-width="2.5"/>
<rect x="298" y="233" width="82" height="14" rx="2" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.2"/>
<text x="339" y="243" text-anchor="middle" font-size="6.5" font-weight="bold" fill="var(--fg)">GPIO18 → SERVO</text>

<!-- Destaque GPIO19 (Pino 23 = D19) — MOTOR EN -->
<circle cx="282" cy="223" r="6" fill="none" stroke="var(--line)" stroke-width="2.5"/>
<rect x="298" y="216" width="84" height="14" rx="2" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.2"/>
<text x="340" y="226" text-anchor="middle" font-size="6.5" font-weight="bold" fill="var(--fg)">GPIO19 → MOTOR</text>
```

---

### COMPONENTE 2: Servo MG996R H02 — Do Bloco 5

Copiar do Bloco 5 (secao `id="bloco-5"`, linhas ~2334-2455) o desenho do servo H02.

**O que copiar**: tag H02, corpo principal (rect 100×110), abas de fixacao (com 4 furos M3), eixo de saida spline 25T, engrenagens internas (Metal Gear), potenciometro de feedback, motor DC interno, placa controle PCB, conector JST 3P, terminais through-hole (PWM, VCC, GND) com seus textos.

**O que NAO copiar**: cotas externas de largura (40.7mm, 54mm), cota de altura (42.9mm), box de especificacoes tecnicas (rect x=75 y=240). Esses elementos ocupam espaco excessivo no diagrama de fiacao.

**Posicao alvo**: Centro-superior (zona servo, ~x=580, y=40).
**Transform**: `translate(580, 40) scale(0.50) translate(-155, -96)`

**Verificacao dos terminais H02** (formula: `SVG_x = 580 + (LOCAL_x - 155) * 0.50`):

| Terminal | Local x | Local y | SVG x              | SVG y              |
|----------|---------|---------|--------------------|--------------------|
| PWM      | 95      | 345     | 580 + (-60)*0.5 = 550   | 40 + (345-96)*0.5 = 164.5  |
| VCC      | 155     | 345     | 580 + 0 = 580           | 164.5              |
| GND      | 215     | 345     | 580 + 30 = 610          | 164.5              |

Esses 3 pads sao os pontos de conexao dos fios W047 (VCC), W048 (GND) e W049 (PWM→GPIO18).

---

### COMPONENTE 3: Motorredutor GA37-520 M13 — Do Bloco 5

Copiar do Bloco 5 (linhas ~2598-2721) o desenho do motor M13.

**O que copiar**: tag M13, motor cilindrico (rect), tampa traseira (arco), simbolo M em circulo, terminais +/- traseiros, caixa de reducao, engrenagens planetarias, flange com furos M3, eixo D, polia GT2 20T com parafuso grub, detalhe do eixo D, terminais through-hole (M+, M-) com textos.

**O que NAO copiar**: cotas externas (73mm, Ø37mm), box de especificacoes tecnicas (rect x=620 y=240).

**Posicao alvo**: Centro-direita-inferior (zona motor, ~x=920, y=430).
**Transform**: `translate(920, 430) scale(0.45) translate(-700, -185)`

**Verificacao dos terminais M13**:

| Terminal | Local x | Local y | SVG x                     | SVG y                      |
|----------|---------|---------|---------------------------|----------------------------|
| M+       | 660     | 345     | 920 + (660-700)*0.45 = 902 | 430 + (345-185)*0.45 = 502 |
| M-       | 740     | 345     | 920 + (740-700)*0.45 = 938 | 502                        |

---

### COMPONENTE 4: Modulo MOSFET D4184 E04 — Do Bloco 6

Copiar do Bloco 6 (secao `id="bloco-6"`, linhas ~2808-3004) o desenho do modulo MOSFET E04.

**O que copiar**: tag E04, placa PCB (rect 170×120), furos de montagem, bornes de parafuso lado controle (SIG, VCC, GND), bornes de parafuso lado potencia (VIN+, VIN-, VOUT+, VOUT-), 2x AOD4184 (MOSFET N-CH Q1 e Q2), componentes onboard (R_PD 10kΩ, R_GATE 100Ω, LED ACT), diagrama esquematico do FET, terminais through-hole (7 pads) com textos.

**O que NAO copiar**: cotas externas (33mm, 25mm), box de especificacoes tecnicas, notas normativas de texto solto.

**Posicao alvo**: Centro-inferior (zona motor, ~x=550, y=430).
**Transform**: `translate(550, 430) scale(0.55) translate(-160, -165)`

**Verificacao dos terminais E04**:

| Terminal | Local x | Local y | SVG x                      | SVG y                       |
|----------|---------|---------|----------------------------|-----------------------------|
| SIG      | 48      | 325     | 550 + (48-160)*0.55 = 488  | 430 + (325-165)*0.55 = 518  |
| VCC      | 84      | 325     | 550 + (84-160)*0.55 = 508  | 518                         |
| GND      | 120     | 325     | 550 + (120-160)*0.55 = 528 | 518                         |
| VIN+     | 162     | 325     | 550 + (162-160)*0.55 = 551 | 518                         |
| VIN-     | 200     | 325     | 550 + (200-160)*0.55 = 572 | 518                         |
| VOUT+    | 238     | 325     | 550 + (238-160)*0.55 = 593 | 518                         |
| VOUT-    | 276     | 325     | 550 + (276-160)*0.55 = 614 | 518                         |

---

### COMPONENTE 5: Diodo Schottky 1N5822 E05 — Do Bloco 6

Copiar do Bloco 6 (linhas ~3010-3068) o desenho do diodo E05.

**O que copiar**: tag E05, corpo cilindrico DO-201AD (rect), faixa do catodo, textos gravados (1N5822 SCHOTTKY 40V 3A), terminais axiais (linhas grossas), rotulos K/A, simbolo esquematico Schottky (triangulo + barra com ganchinhos S).

**O que NAO copiar**: cotas externas (Ø5.2mm, 9.5mm corpo), box de especificacoes tecnicas.

**Posicao alvo**: Entre E04 e M13, abaixo dos terminais (~x=750, y=560).
**Transform**: `translate(750, 560) scale(0.55) translate(-427, -138)`

**Verificacao dos terminais E05**:

| Terminal     | Local x | Local y | SVG x                       | SVG y                       |
|--------------|---------|---------|-----------------------------|-----------------------------|
| K (catodo)   | 345     | 138     | 750 + (345-427)*0.55 = 705  | 560 + (138-138)*0.55 = 560  |
| A (anodo)    | 510     | 138     | 750 + (510-427)*0.55 = 796  | 560                         |

---

### COMPONENTE 6: Buck XL4015 E02 (saida 6V) — Do Bloco 2 no W1

Copiar do W1 (linhas ~5479-5504) o grupo `<g id="bloco-e02">` contendo o Buck converter E02.

**O que copiar**: corpo retangular (rect 90×65), tag E02, textos (BUCK 6V, XL4015 → 6.0V, 5A MAX), 4 terminais through-hole (IN+, IN-, OUT+, OUT-).

No W3 mostramos o modulo COMPLETO mas os fios partem apenas do lado de SAIDA (OUT+, OUT-). O lado de entrada (IN+, IN-) recebe anotacao "← +12V (W1)" indicando que a alimentacao ja esta no diagrama W1.

**Posicao alvo**: Superior-centro (zona servo, ~x=460, y=50).
**Transform**: `translate(460, 50) scale(0.70) translate(-655, -115)`

**Verificacao dos terminais E02 (lado saida)**:

| Terminal | Local x | Local y | SVG x                       | SVG y                       |
|----------|---------|---------|-----------------------------|-----------------------------|
| OUT+     | 700     | 135     | 460 + (700-655)*0.70 = 491.5 | 50 + (135-115)*0.70 = 64    |
| OUT-     | 700     | 165     | 491.5                        | 50 + (165-115)*0.70 = 85    |
| IN+      | 610     | 135     | 460 + (610-655)*0.70 = 428.5 | 64                          |
| IN-      | 610     | 165     | 428.5                        | 85                          |

---

### COMPONENTE 7: Capacitor Buffer E06 (1000µF/16V) — Do Bloco 2 no W1

Copiar do W1 (linhas ~5507-5523) o grupo `<g id="bloco-e06">` contendo o capacitor E06.

**O que copiar**: corpo retangular (rect 36×52), tag E06, textos (1000µF, 16V ELETR), 2 terminais through-hole (+, -) com simbolos de polaridade.

**Posicao alvo**: Ao lado direito do Buck E02 (~x=540, y=50).
**Transform**: `translate(540, 50) scale(0.80) translate(-718, -122)`

**Verificacao dos terminais E06**:

| Terminal | Local x | Local y | SVG x                        | SVG y                       |
|----------|---------|---------|------------------------------|-----------------------------|
| +        | 718     | 135     | 540 + (718-718)*0.80 = 540   | 50 + (135-122)*0.80 = 60.4  |
| -        | 718     | 165     | 540                          | 50 + (165-122)*0.80 = 84.4  |

---

## ZONAS DE LAYOUT (1400×900)

```
+---------------------------------------------------------------------+
|  LEGENDA (x=40-800, y=30-55)                                        |
|  "REDE DE ATUADORES — SERVO MG996R (H02) + MOTOR GA37 (M13)"      |
+----------+------------------------------------------+---------------+
|          |  ZONA SUPERIOR: CIRCUITO SERVO            |               |
|  ESP32   |  E02 (Buck 6V) → E06 (Cap) → H02 (Servo) |               |
|  H01     |  x=420-700, y=40-300                      |    TABELA     |
|  (LEFT)  |  Rail +6V_SV horizontal ~y=110            |    DE FIOS    |
|  x=30    |                                           |    (16 regs   |
|  -387    |  Barras: +6V_SV, GND servo                |    W043-W058) |
|  y=80    |                                           |    x=1050     |
|  -410    |-------------------------------------------+    -1370      |
|          |  ZONA INFERIOR: CIRCUITO MOTOR             |    y=40-550   |
|          |  E04 (MOSFET D4184) → M13 (Motor GA37)    |               |
|          |  E05 (Flyback 1N5822) antiparalelo motor   |               |
|          |  x=420-1050, y=400-650                     |               |
|          |  Rail +12V_AT horizontal ~y=430            |               |
+----------+------------------------------------------+               |
|  NOTAS TECNICAS (5 itens)                                           |
|  x=40-1040, y=680-810                                               |
+---------------------------------------------+-----------------------+
|                                              |  BLOCO DE TITULO      |
|                                              |  x=1050-1370          |
|                                              |  y=780-860            |
+----------------------------------------------+-----------------------+
|  GND rail (barramento terra) ao longo de y~850 ou inferior           |
+---------------------------------------------------------------------+
```

**Fluxo de sinais** (esquerda → direita):
- Topo: ESP32 GPIO18 → sinal PWM 50Hz → H02:PWM
- Base: ESP32 GPIO19 → sinal PWM 20kHz → E04:SIG → E04:VOUT → M13:M+/M-

---

## TABELA DE FIOS (16 CABOS: W043 — W058)

### CIRCUITO SERVO (7 fios: W043-W049)

| ID    | DE                          | PARA                     | CLASSE      | COR REAL    | SECAO   | NOTA                                          |
|-------|-----------------------------|--------------------------|-------------|-------------|---------|-----------------------------------------------|
| W043  | E02:OUT+ (Buck +6V)         | Juncao +6V_SV            | wire-power  | Vermelho    | 22 AWG  | Saida +6V do Buck XL4015 para rail servo      |
| W044  | E02:OUT- (Buck GND)         | Barramento GND           | wire-gnd    | Preto       | 22 AWG  | Retorno GND do Buck (referencia)              |
| W045  | E06:+ (cap buffer)          | Juncao +6V_SV            | wire-power  | Vermelho    | 22 AWG  | Cap 1000uF/16V em paralelo com rail servo     |
| W046  | E06:- (cap buffer)          | Barramento GND           | wire-gnd    | Preto       | 22 AWG  | Terra do capacitor buffer                     |
| W047  | Juncao +6V_SV               | H02:VCC (fio vermelho)   | wire-power  | Vermelho    | 22 AWG  | Alimentacao +6V do servo MG996R               |
| W048  | H02:GND (fio marrom)        | Barramento GND           | wire-gnd    | Preto       | 22 AWG  | Terra do servo                                |
| W049  | H01:GPIO18 (D18, pino 24)   | H02:PWM (fio laranja)    | wire-signal | Laranja     | 26 AWG  | Sinal PWM 50Hz (500-2500us), LEDC CH0        |

### CIRCUITO MOTOR (9 fios: W050-W058)

| ID    | DE                          | PARA                     | CLASSE      | COR REAL    | SECAO   | NOTA                                          |
|-------|-----------------------------|--------------------------|-------------|-------------|---------|-----------------------------------------------|
| W050  | +12V_AT (rail atuadores)    | E04:VIN+ (MOSFET)        | wire-power  | Vermelho    | 18 AWG  | Alimentacao 12V potencia para MOSFET D4184    |
| W051  | Barramento GND              | E04:VIN- (MOSFET)        | wire-gnd    | Preto       | 18 AWG  | Retorno GND potencia do driver                |
| W052  | +3.3V (ESP32)               | E04:VCC (MOSFET)         | wire-power  | Vermelho    | 26 AWG  | Logica 3.3V (pull-up gate, opcional)          |
| W053  | Barramento GND              | E04:GND (MOSFET)         | wire-gnd    | Preto       | 26 AWG  | Terra logica (comum com potencia)             |
| W054  | H01:GPIO19 (D19, pino 23)   | E04:SIG (MOSFET gate)    | wire-signal | Amarelo     | 26 AWG  | PWM 20kHz gate MOSFET (LEDC CH1)             |
| W055  | E04:VOUT+ (saida FET)       | M13:M+ (motor)           | wire-power  | Vermelho    | 18 AWG  | Saida MOSFET → terminal positivo motor        |
| W056  | E04:VOUT- (drain FET)       | M13:M- (motor)           | wire-power  | Preto       | 18 AWG  | Retorno motor via drain dos FETs              |
| W057  | E05:K (catodo 1N5822)       | Juncao M13:M+ / W055     | wire-signal | — (axial)   | 22 AWG  | Flyback: catodo no terminal + do motor        |
| W058  | E05:A (anodo 1N5822)        | Juncao M13:M- / W056     | wire-signal | — (axial)   | 22 AWG  | Flyback: anodo no terminal - do motor         |

### JUNCOES (junction dots obrigatorios)

Colocar `<circle class="junction-dot">` preenchido nos seguintes nos:

1. **+6V_SV**: onde W043, W045 e W047 se encontram (rail de 6V do servo)
2. **GND servo**: onde W044, W046 e W048 chegam ao barramento GND
3. **GND motor**: onde W051 e W053 chegam ao barramento GND
4. **M13:M+**: onde W055 e W057 (catodo E05) se conectam
5. **M13:M-**: onde W056 e W058 (anodo E05) se conectam
6. **GPIO18 pad**: onde W049 termina no pad do ESP32
7. **GPIO19 pad**: onde W054 termina no pad do ESP32

---

## WIRE TAGS E LABELS

Cada fio deve ter:
1. **Wire tag**: retangulo `<rect class="wire-tag">` com fill `var(--tag-bg)` proximo ao meio do percurso
2. **Wire label**: `<text class="wire-label">` com o ID do fio (ex: "W043")
3. **Wire spec**: `<text class="wire-spec">` com a especificacao curta (ex: "+6V 22AWG" ou "PWM 26AWG")

Posicionar os tags para NAO sobrepor outros elementos. Em percursos longos com curvas, colocar o tag no segmento mais longo.

---

## BARRAMENTOS DE REFERENCIA

Desenhar 3 barramentos visuais como linhas horizontais longas:

1. **+6V_SV** (rail servo): linha horizontal grossa (~y=110, x=430-700)
   - Classe: `wire-power` (stroke 1.8)
   - Label retangular: "+6V_SV (E02 BUCK)"
   - Cor de fundo: `var(--tag-bg)`

2. **+12V_AT** (rail motor): linha horizontal grossa (~y=430, x=430-950)
   - Classe: `wire-power` (stroke 1.8)
   - Label retangular: "+12V_AT (MOTOR)"
   - Este rail vem da rede de alimentacao W1 (indicar com seta "← W1")

3. **GND** (terra comum): linha horizontal tracejada (~y=340, x=40-1040, ou ao longo da base)
   - Classe: `wire-gnd` (stroke 1.4 dashed)
   - Label: "GND (COMUM)"
   - Simbolo de terra (3 linhas horizontais decrescentes) nas extremidades

---

## NOTAS TECNICAS (caixa x=40-1040, y=680-830)

Desenhar um retangulo com fundo `var(--bg)`, borda `var(--line)`, titulo "NOTAS TECNICAS — W3" em negrito. Conteudo:

**NOTA 1 — Servo MG996R (H02)**:
Alimentado pelo Buck XL4015 (E02) regulado a 6.0V, 5A max. Capacitor buffer E06 (1000uF/16V) em paralelo absorve picos de corrente transiente do servo (ate 2.5A stall). Sinal PWM 50Hz via GPIO18 (LEDC Channel 0, pulso 500-2500us para 0-180 graus). Ref: `board_config.h: AV_PIN_SERVO = 18`.

**NOTA 2 — Motor GA37-520 (M13) via MOSFET D4184 (E04)**:
Acionamento low-side: o modulo D4184 comuta o retorno GND do motor. Gate do MOSFET dispara com 3.3V do GPIO19 (Vgs(th) = 1.0-2.5V, disparo garantido). PWM 20kHz (LEDC Channel 1) para controle de velocidade sem ruido audivel. Corrente nominal ~0.8A, stall ~3.5A. Ref: `board_config.h: AV_PIN_MOTOR_EN = 19`.

**NOTA 3 — Flyback 1N5822 (E05)**:
Diodo Schottky 40V/3A conectado em antiparalelo ao motor: catodo (K) em M+ e anodo (A) em M-. Vf = 0.525V, Trr ≈ 10ns. Dissipa EMF reversa na desligacao do MOSFET protegendo os FETs AOD4184.

**NOTA 4 — Driver alternativo (modo 2, BTS7960)**:
O firmware suporta BTS7960 (IBT-2) como driver alternativo: GPIO21 (RPWM), GPIO22 (LPWM = LOW, somente avanco), GPIO23 (R_EN + L_EN tied). Configuravel via `AV_MOTOR_DRIVER = 2` em board_config.h. Este diagrama mostra SOMENTE o driver primario (modo 1 = MOSFET D4184, E04).

**NOTA 5 — Secoes de fio**:
Circuito potencia motor (W050/W051/W055/W056): 18 AWG (ate 3.5A stall). Circuito servo (W043-W048): 22 AWG (ate 2.5A). Sinais logicos (W049/W052-W054): 26 AWG. Diodo flyback (W057/W058): 22 AWG.

---

## BLOCO DE TITULO

Posicao: canto inferior-direito (x=1050, y=780, largura 320, altura 80).

Retangulo com borda `var(--line)` stroke 1.5 e fundo `var(--header-bg)`.
Linha separadora horizontal no topo do bloco.

Conteudo (textos com fill `var(--fg)` e `var(--dim)`):

```
PLANTA ELETRICA — AMAZONVISION 4.0
FOLHA 3/5: REDE DE ATUADORES (SERVOS + MOTOR)
ARQUIVO: esp32.html | SECAO: wiring-3
DATA: NOV 2026 | REV A
DES.: D.S. / AMA
```

---

## REGRAS INVIOLAVEIS

1. **SOMENTE** variaveis CSS para cores: `var(--bg)`, `var(--fg)`, `var(--line)`, `var(--line-thin)`, `var(--pin-text)`, `var(--grid)`, `var(--grid-major)`, `var(--dim)`, `var(--trace)`, `var(--pad-fill)`, `var(--tag-bg)`, `var(--header-bg)`, `var(--header-border)`. **NUNCA** cores literais como `#fff`, `black`, `rgb()`, `white`, `red`, etc.

2. **NAO altere** CSS, script, Tab 1, W1, W2, nav pills, nem nada fora de `<section id="wiring-3">`.

3. **Pattern IDs UNICOS**: `grid-w3`, `grid-major-w3`, `hatch-w3`. Se precisar de marker para setas de fluxo: `arrow-w3`.

4. **IDs de grupo UNICOS**: Todos os `<g id="...">` dentro de W3 devem ter sufixo `-w3` ou nomes unicos que NAO colidam com W1 ou W2.

5. **Pads through-hole**: SEMPRE dois circulos concentricos:
   - Externo: `r="5"` ou `r="4.5"`, `fill="var(--pad-fill)"`, `stroke="var(--line)"`, `stroke-width="1"`
   - Interno: `r="2"` ou `r="1.8"`, `fill="var(--bg)"`, `stroke="var(--line)"`, `stroke-width="0.5"`

6. **Classes de fio** (ja definidas no CSS global):
   - `.wire-power`: stroke 1.8px solido (alimentacao +6V, +12V, +3.3V)
   - `.wire-gnd`: stroke 1.4px tracejado (terra/GND)
   - `.wire-signal`: stroke 1.0px solido (sinais logicos GPIO)

7. **Wire tags**: `<rect class="wire-tag">` com fill `var(--tag-bg)` + `<text class="wire-label">` para ID + `<text class="wire-spec">` para especificacao.

8. **Junction dots**: `<circle class="junction-dot">` preenchido (fill `var(--fg)`) em cada ponto de juncao onde 3+ fios se encontram.

9. **Componentes REAIS**: Usar `transform="translate(tx,ty) scale(s) translate(ox,oy)"` para posicionar copias dos desenhos do Tab 1. NUNCA blocos retangulares simplificados. Copiar TODA a geometria interna fidedignamente.

10. **Fios conectam terminais**: Os paths dos fios devem INICIAR e TERMINAR exatamente nas coordenadas SVG calculadas dos pads through-hole dos componentes. NUNCA em pontos arbitrarios no ar.

11. **Sem sobreposicao**: Nenhum texto ou elemento grafico deve sobrepor outro. Verificar especialmente:
    - Tags de fio NAO sobrepondo componentes
    - Descricoes dos pinos do ESP32 NAO sobrepondo fios
    - Barramentos NAO passando por cima de textos

12. **Seção wrapper**: `<section id="wiring-3" class="sheet-section">`

---

## CHECKLIST DE VALIDACAO

Antes de finalizar, verificar TODOS os itens:

- [ ] 16 fios presentes (W043-W058) — todos com paths validos
- [ ] 7 componentes reais desenhados com transform (H01, H02, M13, E02, E04, E05, E06)
- [ ] Cada componente e copia fiel do Tab 1 (NAO bloco simplificado)
- [ ] ZERO cores literais — somente variaveis CSS em TODO o SVG
- [ ] Pattern IDs unicos (grid-w3, grid-major-w3, hatch-w3)
- [ ] IDs de grupo unicos (sem colisao com W1/W2)
- [ ] Moldura dupla correta para viewBox 1400x900
- [ ] Todos os pads through-hole com 2 circulos concentricos
- [ ] Tabela de fios completa (16 registros com todas as colunas)
- [ ] Bloco de titulo correto (FOLHA 3/5, NOV 2026, REV A)
- [ ] 5 notas tecnicas presentes e precisas
- [ ] Fios de alimentacao (+6V, +12V, +3.3V) usando classe `wire-power`
- [ ] Fios GND usando classe `wire-gnd` (tracejado)
- [ ] Fios de sinal (GPIO18, GPIO19) usando classe `wire-signal`
- [ ] 3 barramentos de referencia desenhados (+6V_SV, +12V_AT, GND)
- [ ] ESP32 inteiro dentro da moldura (todos elementos < x=1350, < y=850, > x=25, > y=25)
- [ ] Destaques GPIO18 e GPIO19 com circulos e badges corretos
- [ ] Fio W049 terminando no pad GPIO18 (cx≈282, cy≈240)
- [ ] Fio W054 terminando no pad GPIO19 (cx≈282, cy≈223)
- [ ] Diodo E05 em antiparalelo ao motor (K→M+, A→M-)
- [ ] 7 junction dots nos pontos de juncao listados
- [ ] Legenda identificando a folha no topo
- [ ] Nenhum texto/elemento sobrepondo outro
- [ ] Secao dentro de `<section id="wiring-3" class="sheet-section">`
- [ ] Nada alterado fora de `<section id="wiring-3">`

---

## RESUMO DE ENDERECOS DOS TERMINAIS (coordenadas SVG finais)

Tabela consolidada para facilitar o tracado dos fios:

| Componente | Terminal | SVG cx  | SVG cy  | Fios conectados      |
|------------|----------|---------|---------|----------------------|
| H01 ESP32  | GPIO18   | 282     | 240     | W049                 |
| H01 ESP32  | GPIO19   | 282     | 223     | W054                 |
| E02 Buck   | OUT+     | 492     | 64      | W043                 |
| E02 Buck   | OUT-     | 492     | 85      | W044                 |
| E06 Cap    | +        | 540     | 60      | W045                 |
| E06 Cap    | -        | 540     | 84      | W046                 |
| H02 Servo  | PWM      | 550     | 165     | W049                 |
| H02 Servo  | VCC      | 580     | 165     | W047                 |
| H02 Servo  | GND      | 610     | 165     | W048                 |
| E04 MOSFET | SIG      | 488     | 518     | W054                 |
| E04 MOSFET | VCC      | 508     | 518     | W052                 |
| E04 MOSFET | GND      | 528     | 518     | W053                 |
| E04 MOSFET | VIN+     | 551     | 518     | W050                 |
| E04 MOSFET | VIN-     | 572     | 518     | W051                 |
| E04 MOSFET | VOUT+    | 593     | 518     | W055                 |
| E04 MOSFET | VOUT-    | 614     | 518     | W056                 |
| M13 Motor  | M+       | 902     | 502     | W055, W057           |
| M13 Motor  | M-       | 938     | 502     | W056, W058           |
| E05 Diodo  | K (cat)  | 705     | 560     | W057                 |
| E05 Diodo  | A (ano)  | 796     | 560     | W058                 |

**ATENCAO**: Estas coordenadas dependem dos transforms exatos aplicados. Se voce ajustar qualquer transform, RECALCULE todas as coordenadas dependentes usando a formula geral:
```
SVG_x = tx + (LOCAL_x + ox) * scale
SVG_y = ty + (LOCAL_y + oy) * scale
```
onde ox e oy sao NEGATIVOS na maioria dos casos (ex: translate(-260, -60) significa ox = -260).
