# ENTREGA 2 — Especificação da Planta Geral (Folha Única A1) — AmazonVision 4.0

> **STATUS DE IMPLEMENTAÇÃO (CONCLUÍDA E AUDITADA):** Esta especificação foi integralmente implementada na **Aba 3 (`#tab-planta` / `<section id="planta-geral">`)** de `desenho-eletrico/esp32.html`, contendo todos os componentes compactos (`-pg`), os 6 barramentos horizontais (`+12V`, `+12V_AT`, `+6V_SV`, `+5V`, `+3V3`, `GND`), todos os **82 condutores (`W001–W082`)** em `<g id="fios-pg">`, legenda, notas técnicas NR-12 e carimbo FUCAPI 2026. Auditada via `python desenho-eletrico/auditar_folha.py planta-geral fios-pg` com **0 ocorrências (`fios analisados: 82 | elementos: 969 | OK`)**.

**Projeto:** Esteira Seletora Inteligente de Maçãs — AmazonVision 4.0 (Feira FUCAPI 2026)  
**Objetivo:** Especificar, até o nível de coordenadas SVG, pinos e fios (`W001–W082`), uma folha esquemática mestra única ("Planta Geral") que represente todo o sistema elétrico do AmazonVision 4.0 sem a protoboard física `E26`, pronta para ser implementada em blocos (`G1` a `G7`) e auditada automaticamente por `auditar_folha.py`.

---

## 1. Onde Fica, ViewBox, Estilo e Navegação

### 1.1 Decisão de Localização no `esp32.html`
- **Proposta recomendada:** **Criar uma 3ª Aba dedicada `"Planta Geral"` (`id="tab-planta"`)** na barra de navegação superior (`.tab-bar`), acionada por `switchTab('planta')`, contendo o `<svg id="planta-geral" viewBox="0 0 2378 1682">`.
- **Justificativa técnica:**
  1. **Separação clara de função:** A Aba 1 (`Componentes`, `900×600`) documenta a mecânica/pinagem de cada peça; a Aba 2 (`Interligações`, `1400×900`) mostra a montagem física de bancada fio a fio (incluindo a protoboard `E26`); a **Aba 3 (`Planta Geral`, `2378×1682`)** é o diagrama esquemático industrial mestre para entendimento global, defesa técnica na Feira FUCAPI 2026 e conferência rápida de bancada.
  2. **CSS de largura independente:** Nas abas 1 e 2, `.sheet-container svg { max-width: 1100px; }` funciona bem para `900` e `1400` unidades, mas comprimiria uma folha A1 (`2378` unidades) a 46% da escala. Em uma 3ª aba `#tab-planta`, podemos aplicar `.sheet-container.planta-a1 svg { max-width: 2378px; width: 100%; }` com controles rápidos de zoom (`100%`, `Ajustar à tela`, `Imprimir A1`), garantindo **leitura perfeitamente nítida a 100%**.

### 1.2 Dimensões, Proporção A1 Paisagem e Regras de Estilo
- **ViewBox:** `viewBox="0 0 2378 1682"` (proporção ISO A1 paisagem $\sqrt{2}:1 = 841\text{ mm} \times 594\text{ mm}$ em escala $1\text{ mm} \approx 2,8276\text{ un}$).
- **Moldura Dupla Padrão:**
  - Moldura externa: `<rect x="14" y="14" width="2350" height="1654" fill="none" stroke="var(--line)" stroke-width="1.8"/>`
  - Moldura interna: `<rect x="20" y="20" width="2338" height="1642" fill="none" stroke="var(--line-thin)" stroke-width="0.7"/>`
  - Coordenadas de borda no topo/base (A–H na horizontal, 1–6 na vertical) entre as duas molduras.
- **Regras Estritas de Estilo (mesmas das folhas W):**
  - **Proibido cores literais (`#hex`, `rgb()`):** usar exclusivamente `var(--bg)`, `var(--fg)`, `var(--line)`, `var(--line-thin)`, `var(--pin-text)`, `var(--grid)`, `var(--grid-major)`, `var(--dim)`, `var(--trace)`, `var(--pad-fill)`, `var(--tag-bg)`, `var(--header-bg)`, `var(--header-border)`.
  - **Classes obrigatórias de fiação:** `class="wire-power"` (`stroke-width: 1.8`), `class="wire-gnd"` (`stroke-width: 1.4; stroke-dasharray: 6,3`), `class="wire-signal"` (`stroke-width: 1.0`), `class="junction-dot"` (`r="2.8"`).
  - **Sufixo de IDs:** todos os grupos `<g>` da Planta Geral terminam obrigatoriamente com o sufixo `-pg` (ex.: `id="esp32-h01-pg"`, `id="fios-pg"`).
  - **Fonte mínima:** nenhum texto visível pode ter tamanho efetivo menor que **`5.0` unidades SVG** (`>= 4.4` exigido pelo auditor).
  - **Protoboard `E26` omitida:** os trilhos de `E26` viram barramentos esquemáticos (`+5V`, `+3V3`, `GND`) e os componentes nela montados (`E11`, `E10`, `E28`, `E29`, `E30`) aparecem como símbolos esquemáticos com pinos numerados. Nota obrigatória no rodapé:  
    `"NOTA DE MONTAGEM: Circuitos de clamp (E10/E11), drivers low-side (Q1/Q2 E28, E29), pull-downs (E30) e barramentos lógicos (+5V, +3V3, GND) estão fisicamente montados na protoboard E26 — ver detalhes construtivos nas Folhas W2 e W4."`

---

## 2. Mapa de Zoneamento da Folha (`2378 × 1682`)

Fluxo funcional rigoroso da **esquerda para a direita** (Potência AC → Conversão/Distribuição DC → Segurança NR-12 → Controle Central ESP32 → Sensores/Entradas → Atuadores Seccionados → Sinalização/Iluminação), com **barramentos horizontais de alimentação no topo** e **barramento GND na base**:

| Zona | Nome da Região Funcional | Retângulo `(x1, y1) → (x2, y2)` | Largura × Altura | Conteúdo Principal |
| :--- | :--- | :---: | :---: | :--- |
| **BARR-TOPO** | **Barramentos Horizontais Positivos** | `(420, 45) → (2330, 145)` | `1910 × 100` | 5 trilhos horizontais (`wire-power`): **`+12V`** (`y=60`), **`+12V_AT`** (`y=80`), **`+6V_SV`** (`y=100`), **`+5V`** (`y=120`), **`+3V3`** (`y=140`). |
| **ZONA 1** | **Entrada AC 127/220V e Proteção Primária** | `(35, 170) → (395, 760)` | `360 × 590` | Cabo AC `E19` (`L, N, PE`), Disjuntor Bipolar `E15 (10A Curva C)`, entrada AC e aterramento `PE` na carcaça metálica da Fonte `E01`. |
| **ZONA 2** | **Fonte 12V, Fusíveis Seletivos e Bucks DC** | `(410, 170) → (830, 980)` | `420 × 810` | Saída DC da Fonte `E01 (12V 10A)`, Porta-Fusíveis DIN `E16 (F1 10A Geral, F2 5A Motor, F3 3A Servo, F4 2A Lógica/LED)`, Borne `X1 (12 vias)`, Buck 5V `E03 (MP1584)` e Buck 6V `E02 (LM2596)` + Capacitor `E06 (1000µF)`. |
| **ZONA 3** | **Segurança NR-12 (Parada de Emergência e K1)** | `(410, 1000) → (830, 1430)` | `420 × 430` | Botão de Emergência `E12` (Bloco 1: `NF 11-12` Sinal GPIO27; Bloco 2: `E12-B / E31 NF 21-22` Corte Bobina), Driver Low-Side `Q2 (BC337-40 E28 + R_B2 E29 + R_PD2 E30)`, Relé `K1 (E08)` + Diodo `E09` seccionando `+12V` → `+12V_AT`. |
| **ZONA 4** | **Controle Central (ESP32 DevKit V1 + Câmera)** | `(860, 320) → (1340, 1280)` | `480 × 960` | Bloco central `H01 (ESP32 30 pinos na ordem física da placa)`, destacando `VIN`, `3V3`, `GND.1`, `GND.2`, `GPIO32`, `GPIO33`, `GPIO27`, `GPIO13`, `GPIO25`, `GPIO18`, `GPIO5`, `GPIO17`, `GPIO16`, `GPIO4` + link USB Serial com `H03 (Câmera USB Visão Computacional)`. |
| **ZONA 5** | **Sensores Ópticos IR e Clamps Schottky** | `(1370, 170) → (1830, 740)` | `460 × 570` | Sensores `H04 (S1 Entrada)` e `E07 (S2 Ejeção)`, Régua de Bornes `X2 (8 vias)`, Resistores Série `E11 (R1, R2 1kΩ)` e Duplos Diodos Schottky `E10 (D1, D2 BAT54S SOT-23)` protegendo `GPIO32` e `GPIO33`. |
| **ZONA 6** | **Atuadores Seccionados (`+12V_AT` e `+6V_SV`)** | `(1370, 760) → (1830, 1430)` | `460 × 670` | Módulo MOSFET `E04 (D4184)` com pull-down interno `R_G (W058)`, Diodo Schotkky Flyback `E05 (1N5822)`, Motor DC `M13 (GA37-520 12V)` e Servo Empurrador `H02 (MG996R 6V)`. |
| **ZONA 7** | **Sinalização Luminosa, Alarme Sonoro e Iluminação** | `(1850, 170) → (2330, 1300)` | `480 × 1130` | Sinaleiros LED `H05 (H05-R, H05-G, H05-Y + resistores 330Ω)`, Driver `Q1 (BC337-40 E28 + R_B1 E29 + R_PD1 E30)` + Buzzer 5V `E25`, e Ring Light LED `E13 (12V 8W)`. |
| **BARR-BASE** | **Barramento Horizontal de Retorno (`GND`)** | `(420, 1460) → (2330, 1500)` | `1910 × 40` | Trilho horizontal `GND` (`y=1480`, `class="wire-gnd"`) interligado a `X1:7..11` com pontos de junção (`junction-dot`) para cada retorno vertical. |
| **RODAPÉ** | **Legenda de Símbolos/Cores, Notas NR-12 e Carimbo** | `(35, 1515) → (2345, 1650)` | `2310 × 135` | Legenda de linhas/cores (`x=35..850`), Quadro de Notas Técnicas e Nota da Protoboard `E26` (`x=865..1780`) e Carimbo Oficial FUCAPI 2026 (`x=1795..2345`). |

---

## 3. Lista Completa de Componentes da Planta Geral

Todos os componentes mantêm a identidade visual, os nomes e a numeração real de terminais da Aba 1 (`bloco-1` a `bloco-9`), em escala compacta legível a 100%, com IDs terminados em `-pg`:

| Tag | Nome / Função | ID do Grupo SVG | Origem (Aba 1) | Posição `(x, y)` e Caixa `(w × h)` | Terminais Usados e Coordenadas Exatas `(cx, cy)` no SVG |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **E19** | Tomada / Cabo AC Tripolar NBR 14136 | `bloco-e19-pg` | Bloco 3 / W1 | `(55, 280)` (`90×140`) | `L: (145, 310)`, `N: (145, 350)`, `PE: (145, 390)` |
| **E15** | Disjuntor Bipolar DIN 10A Curva C | `bloco-e15-pg` | `#bloco-3` (`scale 0.65`) | `(210, 260)` (`110×180`) | `1 (IN_L): (240, 260)`, `3 (IN_N): (290, 260)`, `2 (OUT_L): (240, 440)`, `4 (OUT_N): (290, 440)` |
| **E01** | Fonte Chaveada Colmeia 12V 10A (120W) | `bloco-e01-pg` | `#bloco-2` (`scale 0.65`) | `(160, 520)` (`210×220`) | `L: (160, 560)`, `N: (160, 600)`, `PE: (160, 640)`, `+V1: (370, 550)`, `+V2: (370, 580)`, `-V1: (370, 630)`, `-V2: (370, 660)` |
| **E16** | Bloco 4 Porta-Fusíveis DIN 5×20mm (`F1..F4`) | `bloco-e16-pg` | `#bloco-3` (`scale 0.60`) | `(440, 220)` (`150×240`) | `F1_IN (10A Geral): (440, 260)`, `F1_OUT: (590, 260)`, `F2_IN (5A Motor): (440, 310)`, `F2_OUT: (590, 310)`, `F3_IN (3A Servo): (440, 360)`, `F3_OUT: (590, 360)`, `F4_IN (2A Lógica/LED): (440, 410)`, `F4_OUT: (590, 410)` |
| **X1** | Régua de Bornes Sak 2,5mm² — Potência (12 vias) | `bloco-x1-pg` | `#bloco-9` | `(460, 500)` (`110×380`) | **12V (`X1:1..6`):** `1: (460,530)`, `2: (570,530)`, `3: (570,560)`, `4: (570,590)`, `5: (570,620)`, `6: (570,650)`; **GND (`X1:7..12`):** `7: (460,710)`, `8: (460,740)`/`(570,740)`, `9: (570,770)`, `10: (570,800)`, `11: (570,830)`, `12 (Res): (570,860)` |
| **E03** | Conversor Buck Step-Down 5V 3A (MP1584EN) | `bloco-e03-pg` | `#bloco-2` (`scale 0.65`) | `(640, 500)` (`160×130`) | `IN+: (640, 535)`, `IN-: (640, 595)`, `OUT+: (800, 535)`, `OUT-: (800, 595)` |
| **E02** | Conversor Buck Step-Down 6V 3A (LM2596) | `bloco-e02-pg` | `#bloco-2` (`scale 0.65`) | `(640, 680)` (`160×130`) | `IN+ (+12V_AT): (640, 715)`, `IN-: (640, 775)`, `OUT+ (+6V_SV): (800, 715)`, `OUT-: (800, 775)` |
| **E06** | Capacitor Eletrolítico 1000µF / 25V (Buffer 6V) | `bloco-e06-pg` | `#bloco-7` (`scale 0.65`) | `(680, 845)` (`80×95`) | `+ (Anodo): (680, 875)`, `- (Catodo): (680, 915)` |
| **E12** | Botão Emergência Cogumelo 22mm (`NF 11-12` + `E12-B 21-22`) | `bloco-e12-pg` | `#bloco-4` (`scale 0.65`) | `(435, 1040)` (`150×190`) | **Bloco 1 (`E12` Sinal):** `11 (COM): (585, 1085)`, `12 (NC): (585, 1125)`; **Bloco 2 (`E12-B / E31` Bobina K1):** `21 (NF_IN): (435, 1175)`, `22 (NF_OUT): (585, 1175)` |
| **Q2 + R_B2 + R_PD2** | Driver Low-Side Relé K1 (`E28 BC337-40` + `E29 470Ω` + `E30 10kΩ`) | `driver-q2-pg` | W4 (Esquemático) | `(630, 1250)` (`170×150`) | `CMD_IN (GPIO4): (800, 1310)`, `R_B2_1: (760, 1310)`, `R_B2_2 / Q2_B (Pino 2): (700, 1310)`, `R_PD2_1: (775, 1310)`, `R_PD2_2 (GND): (775, 1380)`, `Q2_C (Pino 1): (670, 1270)`, `Q2_E (Pino 3): (670, 1350)` |
| **E08 + E09** | Relé Automotivo 12V 40A (`K1`) + Diodo Flyback `1N4007` | `bloco-e08-e09-pg` | `#bloco-3` (`scale 0.65`) | `(630, 1030)` (`170×190`) | `85 (Bobina +): (630, 1175)`, `86 (Bobina -): (670, 1220)`, `30 (COM +12V): (630, 1075)`, `87 (NO +12V_AT): (800, 1075)`, `87a (NC isolado): (800, 1115)`, `E09_CAT (Faixa): (650, 1175)`, `E09_ANO: (650, 1220)` |
| **H01** | Módulo Controlador ESP32 DevKit V1 (30 Pinos) | `esp32-h01-pg` | `#bloco-1` (`scale 0.85`) | `(960, 380)` (`260×680`) | **Coluna Esquerda (`x=960`):** `GPIO32 (P8): (960, 620)`, `GPIO33 (P9): (960, 650)`, `GPIO25 (P10): (960, 680)`, `GPIO27 (P11): (960, 710)`, `GPIO13 (P15): (960, 830)`, `GND.1 (P14): (960, 800)`, `VIN (P15): (960, 860)`. **Coluna Direita (`x=1220`):** `GPIO18 (P9): (1220, 650)`, `GPIO5 (P8): (1220, 620)`, `GPIO17 (P11): (1220, 710)`, `GPIO16 (P12): (1220, 740)`, `GPIO4 (P13): (1220, 770)`, `GND.2 (P1): (1220, 410)`, `3V3 (P15): (1220, 860)`. **Topo:** `J1 (Micro-USB): (1090, 380)` |
| **H03** | Câmera USB 2MP HD + Host Visão Computacional | `bloco-h03-pg` | `#bloco-5` (`scale 0.60`) | `(980, 210)` (`220×110`) | `USB_DATA: (1090, 320)` (ligado a `H01:J1` via cabo USB serial / protocolo de decisão de descarte) |
| **H04** | Sensor Óptico IR Reflexivo Entrada (`S1` E18-D80NK) | `sensor-s1-h04-pg` | `#bloco-4` (`scale 0.65`) | `(1390, 210)` (`140×110`) | `VCC (Marrom): (1530, 235)`, `OUT (Preto): (1530, 265)`, `GND (Azul): (1530, 295)` |
| **E07** | Sensor Óptico IR Reflexivo Ejeção (`S2` E18-D80NK) | `sensor-s2-e07-pg` | `#bloco-4` (`scale 0.65`) | `(1390, 360)` (`140×110`) | `VCC (Marrom): (1530, 385)`, `OUT (Preto): (1530, 415)`, `GND (Azul): (1530, 445)` |
| **X2** | Régua de Bornes Sak 2,5mm² — Sinais e E-STOP (8 vias) | `bloco-x2-pg` | `#bloco-9` | `(1575, 220)` (`75×290`) | `1 (S1_OUT): (1575, 250)/(1650, 250)`, `2 (S2_OUT): (1575, 285)/(1650, 285)`, `3 (S1_GND): (1575, 320)/(1650, 320)`, `4 (S2_GND): (1575, 355)/(1650, 355)`, `5 (ESTOP_COM): (1575, 390)/(1650, 390)`, `6 (ESTOP_NC): (1575, 425)/(1650, 425)`, `7-8 (Res): (1575, 460..490)` |
| **E11 + E10 (S1)** | Clamp Schottky Sensor S1 (`R1 1kΩ` + `D1 BAT54S SOT-23`) | `clamp-s1-pg` | `#bloco-6` / `#bloco-7` | `(1685, 210)` (`125×120`) | `R1_IN: (1685, 250)`, `R1_OUT / D1_P3 (COM): (1755, 250)`, `D1_P2 (CAT +3V3): (1755, 215)`, `D1_P1 (ANO GND): (1755, 285)`, `S1_GPIO32: (1810, 250)` |
| **E11 + E10 (S2)** | Clamp Schottky Sensor S2 (`R2 1kΩ` + `D2 BAT54S SOT-23`) | `clamp-s2-pg` | `#bloco-6` / `#bloco-7` | `(1685, 360)` (`125×120`) | `R2_IN: (1685, 400)`, `R2_OUT / D2_P3 (COM): (1755, 400)`, `D2_P2 (CAT +3V3): (1755, 365)`, `D2_P1 (ANO GND): (1755, 435)`, `S2_GPIO33: (1810, 400)` |
| **E04** | Módulo Driver MOSFET PWM (`D4184` 15A + `R_G 10kΩ`) | `mosfet-e04-pg` | `#bloco-6` (`scale 0.65`) | `(1390, 820)` (`160×180`) | `PWM (Gate): (1390, 865)`, `GND (Ctrl): (1390, 915)`, `R_G (10kΩ interno W058): (1425, 890)`, `VIN+ (+12V_AT): (1550, 850)`, `VIN- (GND): (1550, 890)`, `OUT+: (1550, 935)`, `OUT-: (1550, 975)` |
| **E05** | Diodo Schottky Roda-Livre Motor (`1N5822` 3A 40V) | `diodo-e05-pg` | `#bloco-6` (`scale 0.65`) | `(1600, 915)` (`60×80`) | `CAT (Faixa → M+): (1630, 935)`, `ANO (→ M-): (1630, 975)` |
| **M13** | Motorredutor DC 12V 100 RPM (`GA37-520`) | `motor-m13-pg` | `#bloco-5` (`scale 0.65`) | `(1690, 885)` (`125×130`) | `M+ (Vermelho): (1690, 935)`, `M- (Preto): (1690, 975)` |
| **H02** | Servomotor Empurrador de Descarte (`MG996R` 6V) | `servo-h02-pg` | `#bloco-5` (`scale 0.65`) | `(1480, 1140)` (`180×160`) | `1 (GND Marrom): (1480, 1250)`, `2 (VCC +6V_SV Vermelho): (1480, 1210)`, `3 (PWM Laranja): (1480, 1170)` |
| **H05** | Conjunto 3 Sinaleiros LED 22mm (`H05-R`, `H05-G`, `H05-Y` + `330Ω`) | `leds-h05-pg` | `#bloco-7` (`scale 0.65`) | `(1880, 220)` (`220×310`) | `R_R_IN: (1880, 270)`, `H05-R_CAT: (2100, 270)`, `R_G_IN: (1880, 360)`, `H05-G_CAT: (2100, 360)`, `R_Y_IN: (1880, 450)`, `H05-Y_CAT: (2100, 450)` |
| **Q1 + R_B1 + R_PD1** | Driver Low-Side Buzzer (`E28 BC337-40` + `E29 470Ω` + `E30 10kΩ`) | `driver-q1-pg` | W4 (Esquemático) | `(1880, 620)` (`170×150`) | `CMD_IN (GPIO13): (1880, 680)`, `R_B1_1: (1910, 680)`, `R_B1_2 / Q1_B (Pino 2): (1970, 680)`, `R_PD1_1: (1895, 680)`, `R_PD1_2 (GND): (1895, 750)`, `Q1_C (Pino 1): (2010, 640)`, `Q1_E (Pino 3): (2010, 720)` |
| **E25** | Buzzer Ativo Contínuo 5V DC (Alarme Sonoro) | `bloco-e25-pg` | `#bloco-8` (`scale 0.65`) | `(2110, 580)` (`140×120`) | `+ (VCC +5V): (2110, 610)`, `- (Coletor Q1): (2110, 640)` |
| **E13** | Iluminação Ring Light LED 12V 8W (Câmara de Visão) | `bloco-e13-pg` | `#bloco-8` (`scale 0.65`) | `(1920, 880)` (`180×160`) | `12V+ (Fio Vermelho): (1920, 920)`, `GND (Fio Preto): (1920, 980)` |

---

## 4. Lista Completa de Ligações (`W001` a `W082`) na Planta Geral

Cada um dos 82 fios (`W001–W082`) aparece na Planta Geral com sua classe CSS, sua tag `<g class="wire-tag">` e a referência cruzada para a folha de montagem (`→ W1`, `→ W2`, `→ W3`, `→ W4`). As ligações curtas dentro da mesma zona usam **traço contínuo ortogonal**, enquanto as ligações que cruzariam zonas distantes usam **barramento horizontal no topo/base** ou **par de rótulos de rede nomeada (`Net Label`)** nas duas pontas:

| ID Fio | Origem (`DE`) | Destino (`PARA`) | Rede (`Net`) | Classe CSS | Bitola e Cor Padronizada | Modo na Planta Geral | Ref. Folha |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- | :---: |
| **W001** | `E19:L` `(145,310)` | `E15:1 (IN_L)` `(240,260)` | `AC_L` | `wire-power` | `1,0 mm² MR` | Fio contínuo (Zona 1) | `→ W1` |
| **W002** | `E19:N` `(145,350)` | `E15:3 (IN_N)` `(290,260)` | `AC_N` | `wire-power` | `1,0 mm² AZ` | Fio contínuo (Zona 1) | `→ W1` |
| **W003** | `E19:PE` `(145,390)` | `E01:PE` `(160,640)` *(Corrigido ACH-01)* | `PE` | `wire-gnd` | `1,0 mm² VD/AM` | Fio contínuo (Zona 1) | `→ W1` |
| **W004** | `E15:2 (OUT_L)` `(240,440)` | `E01:L` `(160,560)` | `AC_L_PROT` | `wire-power` | `1,0 mm² MR` | Fio contínuo (Zona 1) | `→ W1` |
| **W005** | `E15:4 (OUT_N)` `(290,440)` | `E01:N` `(160,600)` | `AC_N_PROT` | `wire-power` | `1,0 mm² AZ` | Fio contínuo (Zona 1) | `→ W1` |
| **W006** | `E01:+V1` `(370,550)` | `E16:F1_IN` `(440,260)` | `+12V_FONTE` | `wire-power` | `1,5 mm² VM` | Fio contínuo (Zona 1→2) | `→ W1` |
| **W007** | `E16:F1_OUT` `(590,260)` | `X1:1 (+12V)` `(460,530)` + Trilho `+12V` `(y=60)` | `+12V` | `wire-power` | `1,5 mm² VM` | Fio contínuo ao Trilho `+12V` | `→ W1` |
| **W008** | `E01:-V1` `(370,630)` | `X1:7 (GND)` `(460,710)` | `GND` | `wire-gnd` | `1,5 mm² PT` | Fio contínuo (Zona 2) | `→ W1` |
| **W009** | `E01:-V2` `(370,660)` | `X1:8 (GND)` `(460,740)` | `GND` | `wire-gnd` | `1,5 mm² PT` | Fio contínuo (Zona 2) | `→ W1` |
| **W010** | `X1:8 (GND)` `(570,740)` | Trilho Horizontal `GND` `(y=1480)` | `GND` | `wire-gnd` | `1,0 mm² PT` | Descida p/ Barramento `GND` | `→ W1/W2` |
| **W011** | `E16:F3_OUT` `(590,360)` *(pós-`+12V_AT`, ACH-02/05)* | `E02:IN+` `(640,715)` | `+12V_AT_SV` | `wire-power` | `0,5 mm² VM` | Fio contínuo (Zona 2) | `→ W1/W3` |
| **W012** | `E02:IN-` `(640,775)` | `X1:9 (GND)` `(570,770)` | `GND` | `wire-gnd` | `0,5 mm² PT` | Fio contínuo (Zona 2) | `→ W1` |
| **W013** | `E02:OUT+` `(800,715)` | `E06:+ (Anodo)` `(680,875)` | `+6V_SV` | `wire-power` | `0,5 mm² LJ` | Fio contínuo (Zona 2) | `→ W1/W3` |
| **W014** | `E02:OUT-` `(800,775)` | `E06:- (Catodo)` `(680,915)` | `GND` | `wire-gnd` | `0,5 mm² PT` | Fio contínuo (Zona 2) | `→ W1/W3` |
| **W015** | `X1:3` → `E16:F4_IN/OUT` `(590,410)` | `E03:IN+` `(640,535)` | `+12V_LOG` | `wire-power` | `0,5 mm² VM` | Fio contínuo (Zona 2) | `→ W1` |
| **W016** | `E03:IN-` `(640,595)` | `X1:10 (GND)` `(570,800)` | `GND` | `wire-gnd` | `0,5 mm² PT` | Fio contínuo (Zona 2) | `→ W1` |
| **W017** | `E03:OUT+` `(800,535)` | Trilho `+5V` `(y=120)` → `H01:VIN` `(960,860)` | `+5V` | `wire-power` | `0,5 mm² VM` | Subida ao Trilho `+5V` + descida `H01:VIN` | `→ W1/W2` |
| **W018** | `E03:OUT-` `(800,595)` | `H01:GND.1` `(960,800)` + Trilho `GND` `(y=1480)` | `GND` | `wire-gnd` | `0,5 mm² PT` | Fio contínuo / Barramento `GND` | `→ W1` |
| **W019** | `H01:3V3` `(1220,860)` | Trilho Horizontal `+3V3` `(y=140)` | `+3V3` | `wire-power` | `22 AWG LJ` | Subida ao Trilho `+3V3` | `→ W1/W2` |
| **W020** | `H01:GND.2` `(1220,410)` | Trilho Horizontal `GND` `(y=1480)` | `GND` | `wire-gnd` | `22 AWG PT` | Descida ao Barramento `GND` | `→ W1/W2` |
| **W021** | Trilho `+5V` `(1530, 120)` | `H04:VCC` `(1530,235)` | `+5V` | `wire-power` | `0,5 mm² MR` | Descida do Trilho `+5V` (Zona 5) | `→ W2` |
| **W022** | `H04:GND` `(1530,295)` | `X2:3 (S1_GND)` `(1575,320)` *(Corrigido ACH-08)* | `GND` | `wire-gnd` | `0,5 mm² AZ (anilha GND)` | Fio contínuo (Zona 5) | `→ W2` |
| **W023** | `H04:OUT` `(1530,265)` | `X2:1 (S1_OUT)` `(1575,250)` | `S1_RAW` | `wire-signal` | `0,5 mm² PT` | Fio contínuo (Zona 5) | `→ W2` |
| **W024** | Trilho `+5V` `(1510, 120)` | `E07:VCC` `(1530,385)` | `+5V` | `wire-power` | `0,5 mm² MR` | Descida do Trilho `+5V` (Zona 5) | `→ W2` |
| **W025** | `E07:GND` `(1530,445)` | `X2:4 (S2_GND)` `(1575,355)` *(Corrigido ACH-08)* | `GND` | `wire-gnd` | `0,5 mm² AZ (anilha GND)` | Fio contínuo (Zona 5) | `→ W2` |
| **W026** | `E07:OUT` `(1530,415)` | `X2:2 (S2_OUT)` `(1575,285)` | `S2_RAW` | `wire-signal` | `0,5 mm² PT` | Fio contínuo (Zona 5) | `→ W2` |
| **W027** | `E12:11 (COM)` `(585,1085)` | `X2:5 (ESTOP_COM)` `(1575,390)` | `ESTOP` | `wire-signal` | `0,5 mm² VM` | Rede nomeada `ESTOP_COM` (Zona 3 → Zona 5) | `→ W2` |
| **W028** | `E12:12 (NC)` `(585,1125)` | `X2:6 (ESTOP_NC)` `(1575,425)` | `GND` | `wire-gnd` | `0,5 mm² PT` | Rede nomeada `ESTOP_NC` (Zona 3 → Zona 5) | `→ W2` |
| **W029 + W032** | `X2:1 (S1_OUT)` `(1650,250)` | `E11 (R1 1kΩ):IN` `(1685,250)` | `S1_RAW` | `wire-signal` | `22/26 AWG AM` | Segmento contínuo com tags `W029` / `W032` | `→ W2` |
| **W030 + W037** | `X2:2 (S2_OUT)` `(1650,285)` | `E11 (R2 1kΩ):IN` `(1685,400)` | `S2_RAW` | `wire-signal` | `22/26 AWG VI` | Segmento contínuo com tags `W030` / `W037` | `→ W2` |
| **W031 + W042** | `X2:5 (ESTOP_COM)` `(1650,390)` | `H01:GPIO27` `(960,710)` | `ESTOP` | `wire-signal` | `22 AWG LJ` | Rede nomeada `ESTOP (GPIO27)` com tags `W031`/`W042` | `→ W2` |
| **W033** | `E11 (R1):OUT` `(1735,250)` | `E10 (D1):P3 (COM)` `(1755,250)` | `S1_CLAMP` | `wire-signal` | `26 AWG AM` | Fio contínuo (Zona 5) | `→ W2` |
| **W034** | `E10 (D1):P2 (CAT)` `(1755,215)` | Trilho `+3V3` `(1755, 140)` | `+3V3` | `wire-power` | `26 AWG LJ` | Subida ao Trilho `+3V3` | `→ W2` |
| **W035** | `E10 (D1):P1 (ANO)` `(1755,285)` | Trilho `GND` `(1755, 1480)` | `GND` | `wire-gnd` | `26 AWG PT` | Descida ao Barramento `GND` | `→ W2` |
| **W036** | `E10 (D1):P3 (COM)` `(1810,250)` | `H01:GPIO32` `(960,620)` | `S1` | `wire-signal` | `22 AWG AM` | Rede nomeada `S1 (GPIO32)` (Zona 5 → Zona 4) | `→ W2` |
| **W038** | `E11 (R2):OUT` `(1735,400)` | `E10 (D2):P3 (COM)` `(1755,400)` | `S2_CLAMP` | `wire-signal` | `26 AWG VI` | Fio contínuo (Zona 5) | `→ W2` |
| **W039** | `E10 (D2):P2 (CAT)` `(1755,365)` | Trilho `+3V3` `(1775, 140)` | `+3V3` | `wire-power` | `26 AWG LJ` | Subida ao Trilho `+3V3` | `→ W2` |
| **W040** | `E10 (D2):P1 (ANO)` `(1755,435)` | Trilho `GND` `(1775, 1480)` | `GND` | `wire-gnd` | `26 AWG PT` | Descida ao Barramento `GND` | `→ W2` |
| **W041** | `E10 (D2):P3 (COM)` `(1810,400)` | `H01:GPIO33` `(960,650)` | `S2` | `wire-signal` | `22 AWG VI` | Rede nomeada `S2 (GPIO33)` (Zona 5 → Zona 4) | `→ W2` |
| **W043** | `X1:2 (+12V_AT pós-K1:87)` | `E16:F2_IN (5A Motor)` `(440,310)` *(Unificado ACH-05/07)* | `+12V_AT` | `wire-power` | `1,0 mm² VM` | Alimentação do fusível `F2` a partir de `+12V_AT` | `→ W1/W3` |
| **W044** | `X1:2 (+12V_AT pós-K1:87)` | `E16:F3_IN (3A Servo)` `(440,360)` *(Unificado ACH-05/07)* | `+12V_AT` | `wire-power` | `0,5 mm² VM` | Alimentação do fusível `F3` a partir de `+12V_AT` | `→ W1/W3` |
| **W045** | `E06:+ (Anodo)` `(680,875)` | Trilho `+6V_SV` `(y=100)` | `+6V_SV` | `wire-power` | `0,5 mm² LJ` | Subida ao Trilho `+6V_SV` | `→ W3` |
| **W046** | `E06:- (Catodo)` `(680,915)` | Trilho `GND` `(y=1480)` / `X1:9` | `GND` | `wire-gnd` | `0,5 mm² PT` | Descida ao Barramento `GND` | `→ W3` |
| **W047** | Trilho `+6V_SV` `(1450, 100)` | `H02:2 (VCC)` `(1480,1210)` | `+6V_SV` | `wire-power` | `0,5 mm² VM` | Descida do Trilho `+6V_SV` (Zona 6) | `→ W3` |
| **W048** | `H02:1 (GND)` `(1480,1250)` | Trilho `GND` `(1450, 1480)` | `GND` | `wire-gnd` | `0,5 mm² MR/PT` | Descida ao Barramento `GND` (Zona 6) | `→ W3` |
| **W049** | `H01:GPIO18` `(1220,650)` | `H02:3 (PWM)` `(1480,1170)` | `PWM_SERVO` | `wire-signal` | `22 AWG LJ` | Fio contínuo ou rede `PWM_SERVO` (Zona 4 → Zona 6) | `→ W3` |
| **W050** | Trilho `+12V_AT` `(1550, 80)` *(via `F2_OUT`)* | `E04:VIN+` `(1550,850)` | `+12V_AT` | `wire-power` | `1,0 mm² VM` | Descida do Trilho `+12V_AT` (Zona 6) | `→ W3` |
| **W051** | `E04:GND (Ctrl)` `(1390,915)` | Trilho `GND` `(1390, 1480)` | `GND` | `wire-gnd` | `22 AWG PT` | Descida ao Barramento `GND` (Zona 6) | `→ W3` |
| **W052** | `E04:VIN-` `(1550,890)` | Trilho `GND` `(1550, 1480)` | `GND` | `wire-gnd` | `1,0 mm² PT` | Descida ao Barramento `GND` (Zona 6) | `→ W3` |
| **W053** | `H01:GPIO25` `(960,680)` | `E04:PWM (Gate)` `(1390,865)` | `PWM_MOTOR` | `wire-signal` | `22 AWG AM` | Rede nomeada `PWM_MOTOR (GPIO25)` (Zona 4 → Zona 6) | `→ W3` |
| **W054** | `E04:OUT+` `(1550,935)` | `M13:M+` `(1690,935)` | `MOTOR+` | `wire-power` | `1,0 mm² VM` | Fio contínuo horizontal (Zona 6) | `→ W3` |
| **W055** | `E04:OUT-` `(1550,975)` | `M13:M-` `(1690,975)` | `MOTOR-` | `wire-power` | `1,0 mm² PT` | Fio contínuo horizontal (Zona 6) | `→ W3` |
| **W056** | `E05:CAT (Faixa)` `(1630,935)` | Nó `MOTOR+` `(1630,935)` | `MOTOR+` | `wire-power` | `Terminal Axial` | Ligação antiparalela no barramento `MOTOR+` | `→ W3` |
| **W057** | `E05:ANO` `(1630,975)` | Nó `MOTOR-` `(1630,975)` | `MOTOR-` | `wire-power` | `Terminal Axial` | Ligação antiparalela no barramento `MOTOR-` | `→ W3` |
| **W058** | `E04:PWM (Gate)` `(1425,865)` | `E04:GND (Ctrl)` `(1425,915)` via `R_G 10kΩ` | `PWM_MOTOR` | `wire-signal` | `Trilha PCB` | Pull-down interno representado em `mosfet-e04-pg` | `→ W3` |
| **W059** | `H01:GPIO17` `(1220,710)` | `H05:R_R_IN (330Ω → LED_R)` `(1880,270)` | `LED_R` | `wire-signal` | `22 AWG VM` | Rede nomeada `LED_R (GPIO17)` (Zona 4 → Zona 7) | `→ W4` |
| **W060** | `H05-R:CAT (-)` `(2100,270)` | Trilho `GND` `(2100, 1480)` | `GND` | `wire-gnd` | `22 AWG PT` | Descida ao Barramento `GND` (tag em `y=270`) | `→ W4` |
| **W061** | `H01:GPIO16` `(1220,740)` | `H05:R_G_IN (330Ω → LED_G)` `(1880,360)` | `LED_G` | `wire-signal` | `22 AWG VD` | Rede nomeada `LED_G (GPIO16)` (Zona 4 → Zona 7) | `→ W4` |
| **W062** | `H05-G:CAT (-)` `(2100,360)` | Trilho `GND` `(2100, 1480)` | `GND` | `wire-gnd` | `22 AWG PT` | Descida ao Barramento `GND` (tag em `y=360`) | `→ W4` |
| **W063** | `H01:GPIO5` `(1220,620)` | `H05:R_Y_IN (330Ω → LED_Y)` `(1880,450)` | `LED_Y` | `wire-signal` | `22 AWG AM` | Rede nomeada `LED_Y (GPIO5)` (Zona 4 → Zona 7) | `→ W4` |
| **W064** | `H05-Y:CAT (-)` `(2100,450)` | Trilho `GND` `(2100, 1480)` | `GND` | `wire-gnd` | `22 AWG PT` | Descida ao Barramento `GND` (tag em `y=450`) | `→ W4` |
| **W065** | Trilho `+5V` `(2110, 120)` | `E25:+ (VCC 5V)` `(2110,610)` | `+5V` | `wire-power` | `26 AWG VM` | Descida do Trilho `+5V` (Zona 7) | `→ W4` |
| **W066** | `E25:-` `(2110,640)` | `Q1:C (Pino 1 Coletor)` `(2010,640)` | `BUZ_COL` | `wire-signal` | `26 AWG MR` | Fio contínuo horizontal (Zona 7) | `→ W4` |
| **W067** | `H01:GPIO13` `(960,830)` | `R_B1 (470Ω)` → `Q1:B (Pino 2)` `(1970,680)` | `BUZ_CMD` | `wire-signal` | `22 AWG VI` | Rede nomeada `BUZ_CMD (GPIO13)` (Zona 4 → Zona 7) | `→ W4` |
| **W068** | `Q1:E (Pino 3 Emissor)` `(2010,720)` | Trilho `GND` `(2010, 1480)` | `GND` | `wire-gnd` | `26 AWG PT` | Descida ao Barramento `GND` (Zona 7) | `→ W4` |
| **W069** | Nó `BUZ_CMD` `(1895,680)` | `R_PD1 (10kΩ)` → Trilho `GND` `(1895, 1480)` | `GND` | `wire-gnd` | `Terminal Axial` | Pull-down de `GPIO13` para `GND` (Zona 7) | `→ W4` |
| **W070** | `E08 (K1):86 (Bobina -)` `(670,1220)` | `Q2:C (Pino 1)` `(670,1270)` + `E09:ANO` | `K1_COIL-` | `wire-signal` | `22 AWG LJ` | Fio contínuo vertical (Zona 3) | `→ W4` |
| **W071** | `H01:GPIO4` `(1220,770)` | `R_B2 (470Ω)` → `Q2:B (Pino 2)` `(700,1310)` | `RELAY_CMD` | `wire-signal` | `22 AWG AZ` | Fio contínuo / Rede `RELAY_CMD (GPIO4)` (Zona 4 → 3) | `→ W4` |
| **W072** | `Q2:E (Pino 3 Emissor)` `(670,1350)` | Trilho `GND` `(670, 1480)` | `GND` | `wire-gnd` | `26 AWG PT` | Descida ao Barramento `GND` (Zona 3) | `→ W4` |
| **W073** | `X1:4 (+12V)` `(570,590)` | `E12-B:21 (NF_IN)` `(435,1175)` | `+12V` | `wire-power` | `0,5 mm² VM` | Fio contínuo vertical pela Zona 2 → Zona 3 | `→ W4` |
| **W074** | `E12-B:22 (NF_OUT)` `(585,1175)` | `E08 (K1):85 (Bobina +)` `(630,1175)` + `E09:CAT` | `K1_COIL+` | `wire-power` | `0,5 mm² VM` | Fio contínuo horizontal (Zona 3) | `→ W4` |
| **W075** | `X1:5 (+12V)` `(570,620)` | `E08 (K1):30 (COM)` `(630,1075)` | `+12V` | `wire-power` | `1,0 mm² VM` | Fio contínuo vertical (Zona 2 → Zona 3) | `→ W4` |
| **W076** | `E08 (K1):87 (NO)` `(800,1075)` | Trilho Horizontal `+12V_AT` `(y=80)` + `F2/F3_IN` | `+12V_AT` | `wire-power` | `1,0 mm² VM` | Subida ao Barramento Seccionado `+12V_AT` | `→ W3/W4` |
| **W077** | Trilho `+12V` `(1920, 60)` *(via `X1:6` / `F4_OUT`)* | `E13:12V+ (Ring Light)` `(1920,920)` | `+12V_LOG` | `wire-power` | `0,5 mm² VM` | Descida ao Ring Light `E13` (Zona 7) | `→ W4` |
| **W078** | `E13:GND (-)` `(1920,980)` | Trilho `GND` `(1920, 1480)` *(ligado a `X1:11`)* | `GND` | `wire-gnd` | `0,5 mm² PT` | Descida ao Barramento `GND` (Zona 7) | `→ W4` |
| **W079** | `X2:3 (S1_GND)` `(1650,320)` | Trilho `GND` `(1650, 1480)` | `GND` | `wire-gnd` | `22 AWG PT` | Descida ao Barramento `GND` (Zona 5) | `→ W2` |
| **W080** | `X2:4 (S2_GND)` `(1650,355)` | Trilho `GND` `(1665, 1480)` | `GND` | `wire-gnd` | `22 AWG PT` | Descida ao Barramento `GND` (Zona 5) | `→ W2` |
| **W081** | `X2:6 (ESTOP_NC)` `(1650,425)` | Trilho `GND` `(1680, 1480)` | `GND` | `wire-gnd` | `22 AWG PT` | Descida ao Barramento `GND` (Zona 5) | `→ W2` |
| **W082** | Nó `RELAY_CMD` `(775,1310)` | `R_PD2 (10kΩ)` → Trilho `GND` `(775, 1480)` | `GND` | `wire-gnd` | `Terminal Axial` | Pull-down de `GPIO4` para `GND` (Zona 3) | `→ W4` |

---

## 5. Correções Incorporadas na Planta Geral e Retroalimentação (Back-port)

A Planta Geral **já nasce com todas as correções técnicas aplicadas**:
1. **Aterramento PE correto (`ACH-01`):** `W003` conecta `E19:PE` diretamente ao terminal `E01:PE` da carcaça metálica da fonte chaveada 12V.
2. **Seccionamento total de atuadores por `K1` (`ACH-02`):** A saída `87 (NO)` do relé `K1` (`W076`) alimenta o barramento `+12V_AT`, que supre **tanto o módulo MOSFET `E04` / motor `M13` (via fusível `F2 5A`) quanto o Buck `E02` / servo `H02` (via fusível `F3 3A`)**.
3. **Lógica E-STOP Fail-Safe documentada (`ACH-03`):** Quadro de notas na Zona 3 / Zona 4 especifica: `"E12 (NF 11-12 ao GND): Normal (fechado) = GPIO27 LOW (0V); Emergência ou cabo rompido (aberto) = GPIO27 HIGH (3,3V via INPUT_PULLUP) -> read_estop() == HIGH"`.
4. **Proteção seletiva por ramo (`ACH-05` e `ACH-07`):** O bloco de 4 porta-fusíveis `E16 (F1 10A Geral, F2 5A Motor, F3 3A Servo, F4 2A Lógica/Ring Light)` do Bloco 3 é integrado sem criar novos números além de `W001–W082` (reaproveitando os IDs `W043` e `W044` que estavam duplicados com `W013/W014`).
5. **Identidade fiel de todos os componentes (`ACH-04`, `ACH-13`, `ACH-14`):** `H01` com os 30 pinos visíveis, sensores `H04/E07` rotulados como `"ÓPTICO IR 5V"`, buzzer `E25` em `+5V` e `E12` com os blocos `NF 11-12` e `E12-B 21-22` claramente distintos.

**O que deve voltar (Back-port) para as folhas W1–W5 e Blocos 2–9 na fase de implementação:**
- Atualizar `W003`, `W011`, `W043/W044` e `E16 (F1..F4)` na **W1**, **W3** e na tabela geral da **W5**.
- Restaurar `#esp32-devkit-w4` e corrigir `W065/W066/W068` na `#tabela-fios-w4` da **W4**.
- Corrigir `X2:3/X2:4` nas tabelas de **W2/W5** e corrigir `"INDUTIVO 5V"` → `"ÓPTICO IR 5V"` no unifilar da **W5**.

---

## 6. Plano de Implementação em Blocos (`G1` a `G7`) e Auditoria Automática

Para garantir zero erros de XML, zero colisões geométricas e revisão incremental, a construção da Planta Geral será dividida em **7 blocos sequenciais**:

| Bloco | Escopo de Implementação no `esp32.html` | Grupos `<g id="...-pg">` Criados | Critério de Aceite e Verificação (`auditar_folha.py`) |
| :---: | :--- | :--- | :--- |
| **G1** | Criar botão da 3ª Aba `"Planta Geral"` (`switchTab('planta')`), container `#tab-planta`, `<svg id="planta-geral" viewBox="0 0 2378 1682">`, moldura dupla A1, barramentos horizontais (`+12V, +12V_AT, +6V_SV, +5V, +3V3, GND`), divisórias tracejadas de zonas, legenda, notas e carimbo. | `moldura-pg`, `barramentos-topo-pg`, `barramento-gnd-pg`, `legenda-pg`, `notas-pg`, `carimbo-pg` | XML válido, `0` cores literais, todos os textos `>= 5.0 un`, troca de aba e tema claro/escuro funcionando. |
| **G2** | Implementar **Zona 1 (Entrada AC)** e **Zona 2 (Fonte 12V, Fusíveis `F1..F4`, Borne `X1`, Bucks `E03`/`E02`, Cap `E06`)** + fios `W001–W016`, `W043–W046`. | `bloco-e19-pg`, `bloco-e15-pg`, `bloco-e01-pg`, `bloco-e16-pg`, `bloco-x1-pg`, `bloco-e03-pg`, `bloco-e02-pg`, `bloco-e06-pg` | `python auditar_folha.py planta-geral fios-pg` com `0` colisões `FIO × CORPO` e `0` colisões `FIO × TEXTO`. |
| **G3** | Implementar **Zona 3 (Segurança NR-12: `E12`, `E12-B`, Driver `Q2`, Relé `K1 E08` + `E09`)** + fios `W070`, `W072–W076`, `W082`. | `bloco-e12-pg`, `driver-q2-pg`, `bloco-e08-e09-pg` | `python auditar_folha.py planta-geral fios-pg` com `0` erros. |
| **G4** | Implementar **Zona 4 (Controle Central: `H01 ESP32 30 pinos` + `H03 Câmera USB`)** + fios de alimentação `W017–W020` e comando `W071`. | `esp32-h01-pg`, `bloco-h03-pg` | Todos os 30 pinos visíveis e destacados; `python auditar_folha.py planta-geral fios-pg` com `0` erros. |
| **G5** | Implementar **Zona 5 (Sensores `H04/E07`, Borne `X2`, Clamps `E11+E10`)** + fios `W021–W042`, `W079–W081`. | `sensor-s1-h04-pg`, `sensor-s2-e07-pg`, `bloco-x2-pg`, `clamp-s1-pg`, `clamp-s2-pg` | `python auditar_folha.py planta-geral fios-pg` com `0` erros. |
| **G6** | Implementar **Zona 6 (Atuadores: `E04 D4184`, `E05`, `M13 Motor DC`, `H02 Servo`)** e **Zona 7 (`H05 LEDs`, Driver `Q1` + `E25 Buzzer`, `E13 Ring Light`)** + fios `W047–W069`, `W077–W078`. | `mosfet-e04-pg`, `diodo-e05-pg`, `motor-m13-pg`, `servo-h02-pg`, `leds-h05-pg`, `driver-q1-pg`, `bloco-e25-pg`, `bloco-e13-pg` | Todos os 82 fios (`W001–W082`) presentes; `python auditar_folha.py planta-geral fios-pg` passando `100% LIMPO`. |
| **G7** | **Back-port para Blocos 2–9 e W1–W5** + atualização de `board_config.h` / `main.cpp` (se autorizado). | Correção dos achados `ACH-01` a `ACH-32` nas folhas existentes | `auditar_folha.py` passando com `0` erros em `wiring-1`, `wiring-2`, `wiring-3`, `wiring-4`, `wiring-5` e `planta-geral`. |

### Melhorias Especificadas para o `auditar_folha.py` (no Bloco G1)
Hoje o `auditar_folha.py` possui 4 pontos cegos que deixaram passar erros nas folhas W1–W4. No Bloco G1 ele deve ser estendido com:
1. **Suporte a `planta-geral` (`2378×1682`):** aceitar `planta-geral` como argumento de folha e ler automaticamente `W, H` do atributo `viewBox`.
2. **Detecção de fios órfãos fora de `<g id="fios-...">`:** alertar qualquer `<line>`/`<path>` com `class="wire-..."` que esteja solto na raiz do `<svg>` (o que mascarou os erros de W1 e W2).
3. **Verificação `TEXTO × TEXTO` e `TAG × TAG`:** testar sobreposição de bounding boxes entre quaisquer dois elementos `<text>` e entre caixas `.wire-tag` (pegando colisões como `W060/W062/W064` na W4 e cotas do Bloco 3).
4. **Verificação de fonte mínima efetiva (`< 4.4 un`):** alertar qualquer `<text>` cujo `font-size * scale` seja inferior a `4.4` unidades.

---

## 7. Riscos e Decisões em Aberto para o Dono do Projeto

Antes de iniciar o Bloco G1, confirme apenas estas **3 decisões rápidas de engenharia**:
1. **Botão Pulsador Verde Start (`E14` da BOM / Bloco 4):** Ele consta na lista de materiais e no Bloco 4, mas não está ligado em W1–W5. Deseja **(a)** mantê-lo apenas como reserva documentada (partida via interface Web/Câmera) ou **(b)** conectá-lo a um pino livre do ESP32 (ex.: `GPIO14` ou `GPIO26` com `INPUT_PULLUP`) já na Planta Geral?
2. **Arquitetura do Porta-Fusíveis `E16`:** Confirma o uso dos **4 fusíveis do Bloco 3** (`F1 10A Geral`, `F2 5A Motor DC`, `F3 3A Servo Buck`, `F4 2A Lógica 5V + Ring Light`) para proteger individualmente os cabos de `0,5 mm²`?
3. **Pino do LED Amarelo (`H05-Y` no `GPIO5`):** O `GPIO5` emite um pulso curto (~100 ms) no boot do ESP32, fazendo o LED Amarelo piscar uma vez ao ligar. Deseja manter no `GPIO5` (como já está na W4/W5) ou mover para `GPIO19`?
