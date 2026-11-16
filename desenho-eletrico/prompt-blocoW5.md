# PROMPT — BLOCO W5: TABELA GERAL DE FIOS + DIAGRAMA UNIFILAR (FOLHA 5/5)

## PRE-REQUISITO

Este prompt so deve ser executado **depois** do `correcoes-W4.md` (que cria W079-W082 e muda GPIO4/GPIO5, BC337-40 e E12-B). A tabela abaixo ja reflete essas correcoes.

## CONTEXTO

Voce esta editando o arquivo unico:
`file:///C:/Users/ponto/OneDrive/Desktop/FEIRA%20-%20AMA/desenho-eletrico/esp32.html`

O Bloco W5 ainda NAO existe. Logo apos o `</section>` do W4 ha o placeholder:
```html
    <!-- PLACEHOLDER W5 -->
    <!-- sera inserido no proximo prompt -->
```
SUBSTITUA essas 2 linhas de comentario pela secao completa:
```html
<section id="wiring-5" class="sheet-section">
  <h2>BLOCO W5 — TABELA GERAL DE FIOS E DIAGRAMA UNIFILAR (Folha 5/5)</h2>
  <div class="canvas-wrap">
    <svg viewBox="0 0 1400 900" width="1400" height="900" xmlns="http://www.w3.org/2000/svg"> ... </svg>
  </div>
</section>
```
O pill `W5: TABELA DE FIOS` (href="#wiring-5") ja existe na navegacao. Nao mexa nele.

**REGRA ABSOLUTA**: NAO altere NADA fora da nova `<section id="wiring-5">`. NAO toque no CSS, no script, na Tab 1, nem em W1-W4.

**DIFERENCA EM RELACAO A W1-W4**: esta folha e **documental**. Aqui **NAO** se copiam desenhos do Tab 1. O diagrama unifilar usa **simbolos esquematicos IEC 60617 simplificados** (retangulos rotulados, simbolos de disjuntor, fusivel, contato, bobina, diodo, motor, terra) desenhados inline.

---

## FOLHA 5/5 — VIEWBOX, MOLDURA E PADROES

- `viewBox="0 0 1400 900"`
- Moldura dupla:
  - `<rect x="20" y="20" width="1360" height="860" fill="none" stroke="var(--line)" stroke-width="1.5"/>`
  - `<rect x="25" y="25" width="1350" height="850" fill="none" stroke="var(--line)" stroke-width="0.5"/>`
- `<defs>` com IDs unicos: `grid-w5`, `grid-major-w5`, `hatch-w5`, `arrow-w5` (mesmo desenho dos patterns/marker da W4, so troca o sufixo). Dois rects de fundo com `url(#grid-w5)` e `url(#grid-major-w5)`.
- Todos os `<g id>` com sufixo `-w5`.

## ZONAS DE LAYOUT (1400×900)

```
+------------------------------------------------------------------------------+
| LEGENDA (x=35-465, y=30-64)                                                  |
+-----------------------------------------------+------------------------------+
| ZONA 1: DIAGRAMA UNIFILAR                     | ZONA 2: MAPA DE GPIO         |
| x=35-905, y=72-470                            | x=915-1365, y=72-290         |
|                                               +------------------------------+
|                                               | ZONA 3: BORNES X1 / X2       |
|                                               | x=915-1365, y=298-470        |
+-----------------------------------------------+------------------------------+
| ZONA 4: TABELA GERAL DE FIOS W001-W082 (3 colunas de 28 linhas)               |
| x=35-1365, y=480-772                                                         |
+---------------------------------------------------+--------------------------+
| ZONA 5: PENDENCIAS DE PROJETO E NOTAS             | BLOCO DE TITULO          |
| x=35-1040, y=780-865                              | x=1050-1370, y=780-860   |
+---------------------------------------------------+--------------------------+
```

---

## ZONA 1 — DIAGRAMA UNIFILAR (`<g id="unifilar-w5">`)

Fluxo da esquerda para a direita, **potencia em linha grossa** (`wire-power`), **GND em tracejado** (`wire-gnd`), **comando em linha fina** (`wire-signal`). Cada bloco e um retangulo `fill="var(--bg)" stroke="var(--line)"` com a TAG (ex.: `E01`) em negrito e a descricao curta abaixo. Ao lado de cada ligacao, indicar o(s) ID(s) de fio correspondente(s) em `text.wire-label` (ex.: `W004/W005`) e a folha de origem em `var(--dim)` (ex.: `→ W1`).

### Coluna A — Entrada AC (x≈45-210)
1. **E19** Plugue NBR 14136 10 A (L / N / PE) — simbolo de tomada.
2. **E15** Disjuntor bipolar 10 A curva C — simbolo de disjuntor (IEC).
3. **E01** Fonte chaveada 12 V 10 A 120 W — retangulo com "AC→DC", entrada L/N e terminal ⏚.
4. PE: linha verde-amarela convencional (usar so `var(--line)` tracejado-ponto `stroke-dasharray="6 2 1 2"`) de **E19:PE** ate o terminal **⏚ da carcaca metalica da E01**. Rotulo `W003 (ver Pendencia 1)`.

### Coluna B — Distribuicao 12 V (x≈230-420)
5. **E16** Fusivel geral (simbolo de fusivel) → **X1** borne de distribuicao (desenhar o borne como barra com vias X1:1/X1:2 = +12V e X1:5/X1:6 = GND, ver Zona 3). IDs `W006/W007/W008/W009/W010`.
6. Barramento **+12V** horizontal saindo do X1 para a direita (y≈150) e barramento **GND** tracejado (y≈440) ao longo de toda a Zona 1.

### Coluna C — Ramos derivados (x≈440-900), de cima para baixo
7. **Ramo 5 V**: +12V → **E03** Buck MP1584 (12→5 V) → **+5V** → `H01:VIN` (ESP32), `H04/E07:VCC` (sensores S1/S2), `E25:+` (buzzer). IDs `W015-W018, W021, W024, W065`.
8. **Ramo 3,3 V**: `H01:3V3` → `E04:VCC` (logica do MOSFET) e rail 3,3 V da protoboard (clamps E10). IDs `W019, W052, W035, W040`.
9. **Ramo servo**: +12V → **E02** Buck XL4015 (12→6 V) → **E06** 1000 µF → **H02** servo MG996R. IDs `W011-W014, W043-W048`. Marcar com triangulo de alerta `!` e texto pequeno `ver Pendencia 2` (hoje o E02 vem do +12V direto, nao do +12V_AT).
10. **Ramo de seguranca (comando do K1)**: +12V → **E12-B** contato NF 21-22 (simbolo de contato NF com acionador cogumelo) → **K1 bobina** (simbolo de bobina 85/86, tag E08) → **Q2** BC337-40 → GND. **E09** 1N4007 em antiparalelo com a bobina. Linha fina de comando `H01:GPIO4 → R_B2 470Ω → Q2:B`. IDs `W069, W082, W070, W071, W072, W073, W074`.
11. **Ramo de potencia dos atuadores**: +12V → **K1 contato 30→87 (NA)** (simbolo de contato NA, ligado por linha tracejada fina a bobina do item 10) → barramento **+12V_AT** → **E04** MOSFET D4184 → **M13** motor GA37 (simbolo de motor, circulo com "M") com **E05** 1N5822 flyback. Comando `H01:GPIO19 → E04:SIG`. IDs `W075, W076, W050, W051, W053-W058`.
12. **Ramo iluminacao**: +12V → **E13** Ring light 12 V (direto, sem rele). IDs `W077, W078`.
13. **Ramo sinalizacao (5 V / 3,3 V)**: `H01:GPIO17/16/5 → H05 LEDs R/G/Y (330 Ω)` e `+5V → E25 buzzer → Q1 BC337-40 ← H01:GPIO13`. IDs `W059-W068`.
14. **Ramo sensores e E-STOP**: `H04/E07:OUT → X2:1/X2:2 → E11 1kΩ + E10 BAT54S → H01:GPIO25/26`; `E12:COM → X2:5 → H01:GPIO27`, `E12:NC → X2:6 → GND` (W081). IDs `W021-W042, W079-W081`.

Representar o **H01 ESP32** como um unico retangulo alto (x≈760-900, y≈90-430) com os pinos usados listados na borda esquerda, de onde saem as linhas finas de comando. Nao desenhar o ESP32 completo nesta folha.

Faixas de tensao: pequenas etiquetas `+12V`, `+12V_AT`, `+6V_SV`, `+5V`, `+3V3`, `GND` sobre cada barramento (fundo `var(--tag-bg)`).

---

## ZONA 2 — MAPA DE GPIO (`<g id="mapa-gpio-w5">`)

Tabela com cabecalho `MAPA DE PINOS DO ESP32 (H01) — VERSAO FINAL APOS W4 REV B`. Colunas: GPIO | PINO | FUNCAO | FIO | FOLHA | CONSTANTE FIRMWARE.

| GPIO | PINO | FUNCAO                         | FIO          | FOLHA | CONSTANTE FIRMWARE            |
|------|------|--------------------------------|--------------|-------|-------------------------------|
| 25   | 9    | Sensor S1 (entrada, clamp)     | W036         | W2    | AV_PIN_S1 = 25 (definido)     |
| 26   | 10   | Sensor S2 (entrada, clamp)     | W041         | W2    | AV_PIN_S2 = 26 (definido)     |
| 27   | 11   | E-STOP NF (entrada, pull-up)   | W042         | W2    | AV_PIN_ESTOP = 27 (definido)  |
| 18   | 24   | Servo MG996R PWM 50 Hz         | W049         | W3    | AV_PIN_SERVO = 18 (definido)  |
| 19   | 23   | MOSFET D4184 PWM 20 kHz        | W054         | W3    | AV_PIN_MOTOR_EN = 19 (definido)|
| 4    | 28   | Rele K1 via Q2                 | W071         | W4    | AV_PIN_RELAY = 4 (a criar)    |
| 13   | 15   | Buzzer via Q1                  | W067         | W4    | AV_PIN_BUZZER = 13 (a criar)  |
| 17   | 26   | LED vermelho                   | W059         | W4    | AV_PIN_LED_R = 17 (a criar)   |
| 16   | 27   | LED verde                      | W061         | W4    | AV_PIN_LED_G = 16 (a criar)   |
| 5    | 25   | LED amarelo                    | W063         | W4    | AV_PIN_LED_Y = 5 (a criar)    |
| 2    | 29   | LED interno da placa           | —            | —     | AV_PIN_LED = 2 (definido)     |

Rodape da tabela (font-size 4.5, `var(--dim)`): "GPIO 21/22/23 reservados no firmware para o driver alternativo BTS7960 (nao ligados). Strapping: GPIO 0, 2, 5, 12, 15 — nenhum comanda atuador. GPIO 1/3 = USB serial."

## ZONA 3 — BORNES (`<g id="bornes-w5">`)

Duas mini-tabelas lado a lado:
- **X1 — Distribuicao 12 V (W1)**: copiar via por via exatamente como esta desenhado na W1 (X1:1 a X1:6, com o que entra e o que sai de cada via e os IDs de fio). Ler a W1 para preencher; nao invente vias.
- **X2 — Sensores e E-STOP (W2)**: X2:1 Sinal S1 (W023→W029) · X2:2 Sinal S2 (W026→W030) · X2:3 GND S1 (W022→W079) · X2:4 GND S2 (W025→W080) · X2:5 ESTOP COM (W027→W031) · X2:6 ESTOP NC (W028→W081) · X2:7 Reserva.

---

## ZONA 4 — TABELA GERAL DE FIOS (`<g id="tabela-geral-w5">`)

Titulo: `TABELA GERAL DE FIAÇÃO — 82 CONDUTORES (W001–W082)`.
3 colunas de tabela lado a lado (x≈35-470, 480-915, 925-1365), 28 linhas cada (a ultima coluna com 26). Cada coluna com cabecalho: **ID | DE | PARA | SEÇÃO | COR | FL.** (a coluna "FUNÇÃO" abaixo NAO vai para o desenho, e so para voce conferir). Linhas com passo ≈9,5 px, font-size 4.4-4.6, ID em negrito, linhas separadoras `var(--line-thin)` 0.3. Linhas dos fios NOVOS (W079-W082) e dos ALTERADOS (W063, W067, W069, W071, W073) com um marcador `●` antes do ID e legenda "● = alterado/novo na revisao B".

Use EXATAMENTE estes dados:

| ID | DE (ORIGEM) | PARA (DESTINO) | SEÇÃO | COR | FOLHA | FUNÇÃO / TERMINAÇÃO |
|----|-------------|----------------|-------|-----|-------|---------------------|
| W001 | E19:L | E15:IN_L | 1,0 mm² (≈17 AWG) | VM | W1 | Ilhós E23 |
| W002 | E19:N | E15:IN_N | 1,0 mm² (≈17 AWG) | AZ | W1 | Ilhós E23 |
| W003 | E19:PE | E27:CARCAÇA | 1,0 mm² (≈17 AWG) | VD | W1 | Ilhós E23 |
| W004 | E15:OUT_L | E01:AC_L | 1,0 mm² (≈17 AWG) | VM | W1 | Ilhós E23 |
| W005 | E15:OUT_N | E01:AC_N | 1,0 mm² (≈17 AWG) | AZ | W1 | Ilhós E23 |
| W006 | E01:+12V | E16:IN | 1,0 mm² (≈17 AWG) | VM | W1 | Ilhós E23 |
| W007 | E16:OUT | X1:1 | 1,0 mm² (≈17 AWG) | VM | W1 | Ilhós E23 |
| W008 | E01:GND | X1:5 | 1,0 mm² (≈17 AWG) | PT | W1 | Ilhós E23 |
| W009 | X1:1 | X1:2 | 1,0 mm² (≈17 AWG) | VM | W1 | Jumper int. |
| W010 | X1:5 | X1:6 | 1,0 mm² (≈17 AWG) | PT | W1 | Jumper int. |
| W011 | X1:2 | E02:IN+ | 0,5 mm² (≈20 AWG) | BN | W1 | Ilhós E23 |
| W012 | X1:6 | E02:IN- | 0,5 mm² (≈20 AWG) | PT | W1 | Ilhós E23 |
| W013 | E02:OUT+ | E06:+ | 0,5 mm² (≈20 AWG) | BN | W1 | Soldado |
| W014 | E02:OUT- | E06:- | 0,5 mm² (≈20 AWG) | PT | W1 | Soldado |
| W015 | X1:2 | E03:IN+ | 0,5 mm² (≈20 AWG) | BU | W1 | Ilhós E23 |
| W016 | X1:6 | E03:IN- | 0,5 mm² (≈20 AWG) | PT | W1 | Ilhós E23 |
| W017 | E03:OUT+ | H01:VIN | 0,5 mm² (≈20 AWG) | BU | W1 | Header pin |
| W018 | E03:OUT- | GND COMUM | 0,5 mm² (≈20 AWG) | PT | W1 | Header pin |
| W019 | H01:3V3 | BARR. 3.3V | 0,5 mm² (≈20 AWG) | Vi | W1 | Header pin |
| W020 | H01:GND | GND COMUM | 0,5 mm² (≈20 AWG) | PT | W1 | Header pin |
| W021 | H04:VCC | +5V (barr. E26) | 0,5 mm² (≈20 AWG) | BU | W2 | Ilhós E23 |
| W022 | H04:GND | GND (barr. E26) | 0,5 mm² (≈20 AWG) | PT | W2 | Ilhós E23 |
| W023 | H04:OUT | X2:1 (Sinal S1) | 0,5 mm² (≈20 AWG) | BK | W2 | Ilhós E23 |
| W024 | E07:VCC | +5V (barr. E26) | 0,5 mm² (≈20 AWG) | BU | W2 | Ilhós E23 |
| W025 | E07:GND | GND (barr. E26) | 0,5 mm² (≈20 AWG) | PT | W2 | Ilhós E23 |
| W026 | E07:OUT | X2:2 (Sinal S2) | 0,5 mm² (≈20 AWG) | BK | W2 | Ilhós E23 |
| W027 | E12:COM | X2:5 (ESTOP COM) | 0,5 mm² (≈20 AWG) | BK | W2 | Ilhós E23 |
| W028 | E12:NC | X2:6 (ESTOP NC) | 0,5 mm² (≈20 AWG) | BK | W2 | Ilhós E23 |
| W029 | X2:1 | E26:S1_IN | 0,5 mm² (≈20 AWG) | BK | W2 | Header pin |
| W030 | X2:2 | E26:S2_IN | 0,5 mm² (≈20 AWG) | BK | W2 | Header pin |
| W031 | X2:5 | E26:ESTOP | 0,5 mm² (≈20 AWG) | BK | W2 | Header pin |
| W032 | E26:S1_IN | E11_S1:IN | jumper (H06) | — | W2 | Header pin |
| W033 | E11_S1:OUT | E10_S1:COM (p.2) | jumper (H06) | — | W2 | Header pin |
| W034 | E10_S1:A1 (p.1) | GND rail (E26) | jumper (H06) | — | W2 | Header pin |
| W035 | E10_S1:K2 (p.3) | +3.3V rail (E26) | jumper (H06) | — | W2 | Header pin |
| W036 | E10_S1:COM (p.2) | H01:GPIO25 | jumper (H06) | — | W2 | Header pin |
| W037 | E26:S2_IN | E11_S2:IN | jumper (H06) | — | W2 | Header pin |
| W038 | E11_S2:OUT | E10_S2:COM (p.2) | jumper (H06) | — | W2 | Header pin |
| W039 | E10_S2:A1 (p.1) | GND rail (E26) | jumper (H06) | — | W2 | Header pin |
| W040 | E10_S2:K2 (p.3) | +3.3V rail (E26) | jumper (H06) | — | W2 | Header pin |
| W041 | E10_S2:COM (p.2) | H01:GPIO26 | jumper (H06) | — | W2 | Header pin |
| W042 | E26:ESTOP | H01:GPIO27 | jumper (H06) | — | W2 | Header pin |
| W043 | E02:OUT+ (Buck 6V) | Junção +6V_SV | 22 AWG (0,33 mm²) | VM | W3 | Saída +6V Buck XL4015 para rail servo |
| W044 | E02:OUT- (Buck GND) | Barramento GND | 22 AWG (0,33 mm²) | PT | W3 | Retorno GND do Buck (referência) |
| W045 | E06:+ (Cap buffer) | Junção +6V_SV | 22 AWG (0,33 mm²) | VM | W3 | Cap 1000µF/16V paralelo rail servo |
| W046 | E06:- (Cap buffer) | Barramento GND | 22 AWG (0,33 mm²) | PT | W3 | Terra do capacitor buffer E06 |
| W047 | Junção +6V_SV | H02:VCC (fio verm.) | 22 AWG (0,33 mm²) | VM | W3 | Alimentação +6V do servo MG996R |
| W048 | H02:GND (fio marrom) | Barramento GND | 22 AWG (0,33 mm²) | PT | W3 | Terra do servo MG996R |
| W049 | H01:GPIO18 (D18 p24) | H02:PWM (fio laran) | 26 AWG (0,13 mm²) | LJ | W3 | Sinal PWM 50Hz LEDC CH0 (500-2500µs) |
| W050 | +12V_AT (rail motor) | E04:VIN+ (MOSFET) | 18 AWG (0,82 mm²) | VM | W3 | Alimentação 12V potência para D4184 |
| W051 | Barramento GND | E04:VIN- (MOSFET) | 18 AWG (0,82 mm²) | PT | W3 | Retorno GND potência do driver D4184 |
| W052 | +3.3V (ESP32 H01) | E04:VCC (MOSFET) | 26 AWG (0,13 mm²) | VM | W3 | Lógica 3.3V (pull-up gate opcional) |
| W053 | Barramento GND | E04:GND (MOSFET) | 26 AWG (0,13 mm²) | PT | W3 | Terra lógica (comum com potência) |
| W054 | H01:GPIO19 (D19 p23) | E04:SIG (Gate FET) | 26 AWG (0,13 mm²) | AM | W3 | PWM 20kHz controle motor (LEDC CH1) |
| W055 | E04:VOUT+ (Saída) | M13:M+ (Motor) | 18 AWG (0,82 mm²) | VM | W3 | Saída MOSFET → terminal positivo motor |
| W056 | E04:VOUT- (Drain) | M13:M- (Motor) | 18 AWG (0,82 mm²) | PT | W3 | Retorno motor via drain dos FETs |
| W057 | E05:K (Catodo) | Junção M13:M+ | 22 AWG (0,33 mm²) | AX | W3 | Flyback: catodo diodo no terminal M+ |
| W058 | E05:A (Anodo) | Junção M13:M- | 22 AWG (0,33 mm²) | AX | W3 | Flyback: anodo diodo no terminal M- |
| W059 | H01:GPIO17 (D17 p26) | H05:R+ (Anodo Verm.) | 26 AWG (0,13 mm²) | VM | W4 | GPIO17→R330Ω→LED R (ERRO/E-STOP) |
| W060 | H05:R- (Catodo Verm.) | Barramento GND | 26 AWG (0,13 mm²) | PT | W4 | Retorno terra GND LED vermelho |
| W061 | H01:GPIO16 (D16 p27) | H05:G+ (Anodo Verde) | 26 AWG (0,13 mm²) | VD | W4 | GPIO16→R330Ω→LED G (OPERANDO/OK) |
| W062 | H05:G- (Catodo Verde) | Barramento GND | 26 AWG (0,13 mm²) | PT | W4 | Retorno terra GND LED verde |
| W063 | H01:GPIO5 (D5 p25) | H05:Y+ (Anodo Amar.) | 26 AWG (0,13 mm²) | AM | W4 | GPIO5→R330Ω→LED Y (PROCESSANDO) — trocado com o relé (strapping) |
| W064 | H05:Y- (Catodo Amar.) | Barramento GND | 26 AWG (0,13 mm²) | PT | W4 | Retorno terra GND LED amarelo |
| W065 | +5V rail (Buck E03) | E25:+ (Buzzer Pos.) | 22 AWG (0,33 mm²) | VM | W4 | Alimentação +5V buzzer ativo NR-12 |
| W066 | E25:- (Buzzer Neg.) | Q1:C (Coletor NPN) | 26 AWG (0,13 mm²) | — | W4 | Buzzer negativo → coletor Q1 |
| W067 | H01:GPIO13 (D13 p15) | Q1:B (Base via 1kΩ) | 26 AWG (0,13 mm²) | LJ | W4 | Comando buzzer GPIO13→E11 1kΩ→Q1:B (Q1 = BC337-40, pull-down 10 kΩ) |
| W068 | Q1:E (Emissor NPN) | Barramento GND | 26 AWG (0,13 mm²) | PT | W4 | Terra circuito buzzer via emissor Q1 |
| W069 | +12V rail (Fonte E01) | E12-B:21 (2º NF do E-STOP) | 22 AWG (0,33 mm²) | VM | W4 | +12V → contato NF 21-22 → bobina K1 (corte por hardware NR-12) |
| W070 | E08:86 (Bobina -) | Q2:C (Coletor NPN) | 22 AWG (0,33 mm²) | — | W4 | Bobina- → coletor Q2 (low-side) |
| W071 | H01:GPIO4 (D4 p28) | Q2:B via R_B2 470Ω | 26 AWG (0,13 mm²) | LJ | W4 | Comando relé K1 (GPIO4, sem função de boot) — Q2 = BC337-40, pull-down 10 kΩ |
| W072 | Q2:E (Emissor NPN) | Barramento GND | 22 AWG (0,33 mm²) | PT | W4 | Terra circuito relé via emissor Q2 |
| W073 | E09:K (Catodo Flyb.) | Junção W082 / E08:85 | 22 AWG (0,33 mm²) | AX | W4 | Flyback no lado da bobina, depois do contato NF |
| W074 | E09:A (Anodo Flyb.) | Junção E08:86 (Bob-) | 22 AWG (0,33 mm²) | AX | W4 | Flyback: anodo → bobina- (1N4007) |
| W075 | +12V rail (Fonte E01) | E08:30 (COM +12V IN) | 14 AWG (2,08 mm²) | VM | W4 | Entrada potência +12V relé K1 (até 40A) |
| W076 | E08:87 (NA +12V_AT) | +12V_AT rail (W3) | 14 AWG (2,08 mm²) | VM | W4 | Saída +12V_AT seccionada NR-12 |
| W077 | +12V rail (Fonte E01) | E13:+12V (Ring Light) | 22 AWG (0,33 mm²) | VM | W4 | Alimentação ring light LED 12V (~4W) |
| W078 | E13:GND (Retorno) | Barramento GND | 22 AWG (0,33 mm²) | PT | W4 | Terra ring light LED 12V |
| W079 | X2:3 (GND S1, saída) | GND rail (E26) | jumper (H06) | — | W2 | NOVO: retorno GND do sensor S1 (faltava) |
| W080 | X2:4 (GND S2, saída) | GND rail (E26) | jumper (H06) | — | W2 | NOVO: retorno GND do sensor S2 (faltava) |
| W081 | X2:6 (ESTOP NC, saída) | GND rail (E26) | jumper (H06) | — | W2 | NOVO: fecha o NF do E-STOP no GND (fail-safe) |
| W082 | E12-B:22 (2º NF do E-STOP) | E08:85 (Bobina +) | 22 AWG (0,33 mm²) | VM | W4 | NOVO: E-STOP corta a bobina de K1 sem depender do ESP32 |

Legenda de cores abaixo da tabela (1 linha, font-size 4.5): `VM vermelho · PT/BK preto · AZ/BU azul · VD verde · AM amarelo · LJ laranja · BN marrom · Vi violeta · AX terminal axial do componente · — jumper de protoboard`.

---

## ZONA 5 — PENDENCIAS DE PROJETO (`<g id="pendencias-w5">`)

Retangulo `fill="var(--bg)" stroke="var(--line)"`, titulo **PENDÊNCIAS DE PROJETO — NÃO RESOLVIDAS NAS FOLHAS W1–W3** e lista numerada (font-size 5):

1. **W003 (PE) termina em "E27:CARCAÇA", mas E27 é a caixa plástica.** O terra precisa ir ao borne ⏚ da carcaça metálica da fonte E01 (W1).
2. **Buck do servo E02 alimentado por X1:2 (+12V direto).** O relé K1 não corta o servo na emergência; para atender a NR-12, alimentar E02 a partir do +12V_AT (W1/W3).
3. **W1 tem um único fusível (E16) no +12V.** O manual prevê F1 5 A (motor), F2 3 A (bucks) e F3 2 A (ring light). Definir e redesenhar na W1.
4. **Firmware:** com o NF do E-STOP ligado ao GND (W081), GPIO27 lê LOW em operação normal e HIGH quando o botão é apertado ou o fio rompe. Inverter `read_estop()` em `main.cpp` (hoje `== LOW`).
5. **BOM:** BC337-40 (E28), 470 Ω (E29), 10 kΩ (E30) e bloco NF 22 mm (E31) já adicionados. Ainda falta cabinho 26 AWG nas cores VD/AM/LJ usadas na W3/W4 (E22 só tem BN/BU/BK/Vi).
6. **W3:** o auditor (`python auditar_folha.py wiring-3`) aponta W044, W047 e W057 cruzando o corpo de componentes (ajuste fino).

## BLOCO DE TITULO (`<g id="bloco-titulo-w5">`)

Mesmo formato da W4 (x=1050, y=780, 320×80, borda `var(--line)` 1.5, fundo `var(--header-bg)`):
```
PLANTA ELETRICA — AMAZONVISION 4.0
FOLHA 5/5: TABELA GERAL DE FIOS E DIAGRAMA UNIFILAR
ARQUIVO: esp32.html | SECAO: wiring-5
DATA: NOV 2026 | REV A
DES.: D.S. / AMA
```

---

## REGRAS INVIOLAVEIS

1. **SOMENTE** variaveis CSS para cores: `var(--bg)`, `var(--fg)`, `var(--line)`, `var(--line-thin)`, `var(--pin-text)`, `var(--grid)`, `var(--grid-major)`, `var(--dim)`, `var(--trace)`, `var(--pad-fill)`, `var(--tag-bg)`, `var(--header-bg)`, `var(--header-border)`. Nunca cores literais.
2. NAO alterar nada fora de `<section id="wiring-5">`.
3. IDs com sufixo `-w5`; patterns `grid-w5`, `grid-major-w5`, `hatch-w5`, `arrow-w5`.
4. Nenhum texto sobre outro texto ou sobre linha. Nada fora da moldura interna (x 25-1375, y 25-875).
5. Classes globais: `.wire-power` (1.8), `.wire-gnd` (1.4 tracejado), `.wire-signal` (1.0), `.junction-dot`, `.wire-tag`, `.wire-label`, `.wire-spec`.
6. Os dados da tabela geral sao EXATAMENTE os acima: 82 linhas, sem inventar nem omitir fios.

## CHECKLIST DE VALIDACAO

- [ ] Secao `wiring-5` substituiu o placeholder; pill W5 leva a ela
- [ ] Tabela geral com 82 linhas (W001-W082), 3 colunas, marcador ● nos 9 alterados/novos
- [ ] Unifilar com os 8 ramos (5 V, 3,3 V, servo, seguranca K1, atuadores, iluminacao, sinalizacao, sensores/E-STOP) e IDs de fio em cada ligacao
- [ ] E12-B NF em serie com a bobina K1; K1 30→87 alimentando +12V_AT; E09 e E05 desenhados
- [ ] Mapa de GPIO com 11 linhas, coerente com W2-W4 revisadas
- [ ] Bornes X1 (copiado da W1) e X2 (7 vias)
- [ ] 6 pendencias listadas
- [ ] `python auditar_folha.py wiring-5 unifilar-w5` sem ocorrencias de FIO x CORPO / FIO x TEXTO (o auditor aceita o nome do grupo de linhas como 2º argumento)
- [ ] XML valido (mesmo numero de `<g` e `</g>`), zero cores literais
