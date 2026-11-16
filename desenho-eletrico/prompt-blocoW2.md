# PROMPT — BLOCO W2: REDE DE SENSORES E E-STOP (Folha 2/5 — Interligações)

## CONTEXTO

Voce esta editando o arquivo unico:
`file:///C:/Users/ponto/OneDrive/Desktop/FEIRA%20-%20AMA/desenho-eletrico/esp32.html`

A Aba 2 (Interligações) ja existe com o Bloco W1 inserido. Voce deve:

1. **INSERIR o Bloco W2** como nova `<section>` logo apos o `</section>` do Bloco W1 (antes do comentario `<!-- PLACEHOLDERS W2-W5 -->`)
2. **NAO altere NADA** do CSS, do script, do header, da tab-bar, dos Blocos 1-9 (Aba 1), nem do Bloco W1

---

## ⚠️ REGRA FUNDAMENTAL — DESENHOS REAIS DOS COMPONENTES

**ESTA É A REGRA MAIS IMPORTANTE DESTE PROMPT.**

Os diagramas de fiação da Aba 2 NÃO usam blocos retangulares simplificados.
Cada componente deve ser desenhado **EXATAMENTE como aparece na Aba 1** (nos Blocos 1 a 9), com o mesmo nivel de detalhe CAD:

- O **ESP32 DevKit** deve ser o desenho completo do Bloco 1 (placa com todos os pinos, encapsulamento, pinout)
- Os **Sensores IR** devem ser os desenhos do Bloco 4 (corpo retangular com LED TX/RX, potenciometro, terminais)
- O **E-STOP** deve ser o desenho do Bloco 4 (cogumelo com contatos NC/NA/COM)
- Os **Resistores E11** devem ser os desenhos do Bloco 7 (corpo axial com faixas de cor)
- Os **BAT54S E10** devem ser os desenhos do Bloco 6 (SOT-23 com diagrama interno)
- A **Protoboard E26** deve ser o desenho do Bloco 8 (placa com trilhas e barramentos)
- O **Borne X2** deve ser o desenho do Bloco 9 (regua SAK com vias)

**COMO FAZER:** Copie os grupos SVG (`<g>`) dos componentes das sections dos Blocos 1-9 da Aba 1, aplique `transform="translate(x,y) scale(s)"` para posicionar e redimensionar no layout da folha W2, e depois desenhe as **linhas de fiação** conectando os pads reais dos componentes.

O resultado deve parecer uma **planta elétrica profissional**: voce ve o componente real com seus terminais, e os fios saindo dos pads indo ate o proximo componente.

**ViewBox MAIOR**: como os componentes reais ocupam mais espaço, use `viewBox="0 0 1400 900"` com `width="1400" height="900"` para ter area suficiente. A moldura dupla acompanha: externo (20,20,1360,860 stroke 1.5) + interno (25,25,1350,850 stroke 0.5).

---

## REGRAS DE ESTILO CAD

1. **ViewBox**: `0 0 1400 900`, width="1400" height="900"
2. **Patterns (defs)**: IDs unicos: `grid-w2`, `grid-major-w2`, `hatch-w2`
3. **Grid duplo**: fundo com `grid-w2` (10px) + `grid-major-w2` (50px)
4. **Moldura dupla**: rect externo (20,20,1360,860 stroke 1.5) + interno (25,25,1350,850 stroke 0.5)
5. **Cores**: SOMENTE variaveis CSS. NUNCA cores literais.
6. **Marker de seta**: `id="arrow-w2"` (mesmo formato do arrow-w1)
7. **Estilos de fio**: usar as mesmas classes CSS ja definidas: `wire-power`, `wire-gnd`, `wire-signal`, `wire-label`, `wire-spec`, `wire-tag`, `junction-dot`, `terminal-block`, `terminal-label`, `terminal-pin`, `from-to`
8. **Bloco de titulo**: PROJETO: FEIRA AMA / BLOCO: W2 — REDE DE SENSORES E E-STOP / ESCALA: N/A / FOLHA: 2/5 / DATA: NOV 2026 / REV: A

---

## LAYOUT DO DIAGRAMA

Organizar da **esquerda para a direita** (fluxo do sinal):

```
SENSORES IR  ──>  BORNE X2  ──>  PROTOBOARD E26  ──>  ESP32 H01
(H04, E07)       (E17/X2)       (E11 + E10)           (GPIO25/26/27)
                                                  
E-STOP E12  ──>  BORNE X2  ──>  ──────────────>  ESP32 GPIO27
```

**Distribuicao no viewBox 1400×900:**

- **Zona Esquerda (x=40-350)**: SENSORES DE CAMPO
  - Sensor S1 (H04) no topo (y=80-280) — desenho real do Bloco 4
  - Sensor S2 (E07) no meio (y=300-500) — mesmo desenho
  - E-STOP E12 na parte inferior (y=520-750) — desenho real do Bloco 4

- **Zona Centro-Esquerda (x=380-550)**: BORNE X2 (E17)
  - Regua SAK vertical com 7 vias numeradas — desenho real do Bloco 9
  - X2:1 = Sinal S1
  - X2:2 = GND S1
  - X2:3 = Sinal S2
  - X2:4 = GND S2
  - X2:5 = E-STOP COM
  - X2:6 = E-STOP NC
  - X2:7 = RESERVA

- **Zona Central (x=580-900)**: PROTOBOARD E26 COM CIRCUITO DE PROTEÇÃO
  - Protoboard desenhada com barramentos +5V, +3.3V, GND — desenho real do Bloco 8
  - **Dentro da protoboard**, os componentes montados:
    - 2× E11 Resistor 1kΩ (um para S1, um para S2) — desenho real do Bloco 7
    - 2× E10 BAT54S SOT-23 (um para S1, um para S2) — desenho real do Bloco 6
  - Mostrar as trilhas internas da protoboard conectando os componentes

- **Zona Direita (x=950-1350)**: ESP32 DEVKIT H01
  - Desenho COMPLETO do ESP32 do Bloco 1 (placa inteira com todos os pinos)
  - Destacar (com stroke mais grosso ou tag) os 3 pinos utilizados:
    - GPIO25 (pino fisico do lado esquerdo)
    - GPIO26 (pino fisico do lado esquerdo)
    - GPIO27 (pino fisico do lado esquerdo)
  - Os demais pinos ficam visiveis mas com stroke normal (nao apagar nenhum)

- **Barra inferior (y=760-880)**: Tabela de fios + Notas + Bloco de titulo

---

## COMPONENTES — O QUE COPIAR DE CADA BLOCO

### H04 — Sensor IR S1 (Bloco 4, Aba 1)
Copiar o desenho do sensor infravermelho retangular:
- Corpo retangular preto com LED TX (IR) e fototransistor RX
- Potenciometro de ajuste no topo
- 3 terminais: VCC (+5V), GND, OUT (sinal digital)
- Badge `H04` e texto "SENSOR IR S1"
- **Escala**: reduzir ~70% do original para caber no layout
- **Posicao**: x=60, y=100

### E07 — Sensor IR S2 (Bloco 4, Aba 1)
Mesmo desenho do H04, mas com:
- Badge `E07` e texto "SENSOR IR S2"
- **Posicao**: x=60, y=320

### E12 — Botao E-STOP (Bloco 4, Aba 1)
Copiar o desenho do cogumelo de emergencia:
- Corpo cilindrico vermelho (representado monocromatico) com cogumelo no topo
- Anel de trava (twist-to-release)
- Contatos: COM (comum), NC (normalmente fechado), NA (normalmente aberto)
- Badge `E12` e texto "E-STOP EMERGÊNCIA"
- **Escala**: reduzir ~65% do original
- **Posicao**: x=60, y=550

### E17/X2 — Borne SAK (Bloco 9, Aba 1)
Copiar o desenho da regua de bornes:
- Regua vertical com vias passantes (parafuso + mola)
- 7 vias numeradas (X2:1 a X2:7)
- Badge `X2` referenciando E17
- Perfil omega no trilho DIN
- **Escala**: ~80% do original
- **Posicao**: x=400, y=80

### E26 — Protoboard (Bloco 8, Aba 1)
Copiar o desenho da protoboard:
- Placa retangular com furos em grid 2.54mm
- Barramentos de alimentacao (+ e -) nas bordas
- Area central com trilhas verticais de 5 furos
- Badge `E26` e texto "PROTOBOARD 830 PONTOS"
- **Escala**: ~75% do original
- **Posicao**: x=580, y=80
- **DENTRO** da protoboard, desenhar montados:
  - 2× E11 (Resistor 1kΩ axial, do Bloco 7, em escala de protoboard)
  - 2× E10 (BAT54S SOT-23, do Bloco 6, em escala de protoboard)

### E11 — Resistor 1kΩ × 2 (Bloco 7, Aba 1)
Copiar o desenho do resistor axial:
- Corpo cilindrico com 4 faixas (Marrom-Preto-Vermelho-Dourado)
- 2 terminais axiais
- Texto "1kΩ" e badge `E11`
- **Escala**: ~50% (tamanho de componente na protoboard)
- Desenhar 2 unidades: E11_S1 e E11_S2

### E10 — BAT54S × 2 (Bloco 6, Aba 1)
Copiar o desenho do SOT-23:
- Corpo retangular pequeno com marca no pino 1
- 3 pinos: A1 (pino 1), COM (pino 2), K2 (pino 3)
- Diagrama interno (2 diodos em serie)
- Badge `E10`
- **Escala**: ~60% (tamanho de componente na protoboard)
- Desenhar 2 unidades: E10_S1 e E10_S2

### H01 — ESP32 DevKit V1 (Bloco 1, Aba 1)
Copiar o desenho COMPLETO do ESP32:
- Placa com modulo ESP32-WROOM-32 no centro
- Conector Micro-USB no topo
- 2 fileiras de pinos (15+15 = 30 pinos)
- Todos os rotulos de pinos visiveis
- Badge `H01`
- **Escala**: ~80% do original
- **Posicao**: x=950, y=80
- **DESTAQUE** nos pinos usados nesta folha:
  - GPIO25 → circulo ao redor com stroke 2 e texto "← S1"
  - GPIO26 → circulo ao redor com stroke 2 e texto "← S2"
  - GPIO27 → circulo ao redor com stroke 2 e texto "← E-STOP"

---

## TABELA DE FIOS (W021 a W040)

### FIAÇÃO DE CAMPO (cabos E22 0.5mm², terminados com ilhós E23)

| FIO | DE (ORIGEM) | PARA (DESTINO) | BITOLA | COR | TIPO | TERMINAL |
|-----|-------------|----------------|--------|-----|------|----------|
| W021 | H04:VCC | +5V (barr. E26) | 0.5mm² | BU | E22 | Ilhós E23 |
| W022 | H04:GND | GND (barr. E26) | 0.5mm² | PT | E22 | Ilhós E23 |
| W023 | H04:OUT | X2:1 | 0.5mm² | BK | E22 | Ilhós E23 |
| W024 | E07:VCC | +5V (barr. E26) | 0.5mm² | BU | E22 | Ilhós E23 |
| W025 | E07:GND | GND (barr. E26) | 0.5mm² | PT | E22 | Ilhós E23 |
| W026 | E07:OUT | X2:2 | 0.5mm² | BK | E22 | Ilhós E23 |
| W027 | E12:COM | X2:5 | 0.5mm² | BK | E22 | Ilhós E23 |
| W028 | E12:NC | X2:6 | 0.5mm² | BK | E22 | Ilhós E23 |

### FIAÇÃO BORNE → PROTOBOARD (cabos E22 0.5mm²)

| FIO | DE (ORIGEM) | PARA (DESTINO) | BITOLA | COR | TIPO | TERMINAL |
|-----|-------------|----------------|--------|-----|------|----------|
| W029 | X2:1 | E26:fileira S1_IN | 0.5mm² | BK | E22 | Header pin |
| W030 | X2:2 | E26:fileira S2_IN | 0.5mm² | BK | E22 | Header pin |
| W031 | X2:5 | E26:fileira ESTOP | 0.5mm² | BK | E22 | Header pin |

### FIAÇÃO INTERNA DA PROTOBOARD (jumpers H06)

| FIO | DE (ORIGEM) | PARA (DESTINO) | BITOLA | COR | TIPO | TERMINAL |
|-----|-------------|----------------|--------|-----|------|----------|
| W032 | E26:S1_IN | E11_S1:IN | jumper | — | H06 | Header pin |
| W033 | E11_S1:OUT | E10_S1:COM (pino 2) | jumper | — | H06 | Header pin |
| W034 | E10_S1:A1 (pino 1) | GND rail (E26) | jumper | — | H06 | Header pin |
| W035 | E10_S1:K2 (pino 3) | +3.3V rail (E26) | jumper | — | H06 | Header pin |
| W036 | E10_S1:COM (pino 2) | H01:GPIO25 | jumper | — | H06 | Header pin |
| W037 | E26:S2_IN | E11_S2:IN | jumper | — | H06 | Header pin |
| W038 | E11_S2:OUT | E10_S2:COM (pino 2) | jumper | — | H06 | Header pin |
| W039 | E10_S2:A1 (pino 1) | GND rail (E26) | jumper | — | H06 | Header pin |
| W040 | E10_S2:K2 (pino 3) | +3.3V rail (E26) | jumper | — | H06 | Header pin |

### FIAÇÃO ESP32 (jumpers H06)

| FIO | DE (ORIGEM) | PARA (DESTINO) | BITOLA | COR | TIPO | TERMINAL |
|-----|-------------|----------------|--------|-----|------|----------|
| W041* | E10_S2:COM (pino 2) | H01:GPIO26 | jumper | — | H06 | Header pin |
| W042* | E26:ESTOP_IN | H01:GPIO27 | jumper | — | H06 | Header pin |

> **NOTA**: A numeracao W041-W042 substitui o range original W041-W056 do W3. Ajustar na tabela geral da Folha W5. No total esta folha tem **22 fios** (W021 a W042).

---

## COMO REPRESENTAR OS FIOS

### Fios de campo (W021-W028): cabos reais
- Saem dos terminais dos componentes (sensores, E-STOP) com **path ortogonal**
- Linha `class="wire-signal"` (0.5mm²)
- Etiqueta `[Wnnn]` no meio do fio
- Texto de especificacao "0.5mm² COR" abaixo
- Terminam nos terminais do borne X2
- Representar o cabo como linha com ponto de juncao em cada extremidade

### Fios borne → protoboard (W029-W031): cabos curtos
- Saem do lado direito do borne X2
- Entram no lado esquerdo da protoboard E26
- Linha `class="wire-signal"`

### Fios internos da protoboard (W032-W042): jumpers
- Desenhados como **linhas curtas DENTRO** da area da protoboard
- Usar `class="wire-signal"` com stroke-dasharray="3 2" (tracejado curto para diferenciar de cabos externos)
- Etiqueta menor (font-size 4.5)
- Conectam os furos/pads dos componentes montados na protoboard

### Fios protoboard → ESP32 (W036, W041, W042):
- Saem do lado direito da protoboard
- Entram nos pinos especificos do ESP32 (GPIO25, GPIO26, GPIO27)
- Linha `class="wire-signal"` solida
- Etiqueta proeminente pois sao as conexoes GPIO criticas

---

## CIRCUITO DE PROTEÇÃO — DETALHE AMPLIADO

Na area central da protoboard, desenhar um **detalhe ampliado** (zoom box) mostrando o circuito de protecao de UM canal (S1):

```
Sensor OUT → [R 1kΩ E11] → Junção → [BAT54S E10] → GPIO25
                                |         |    |
                                |     A1→GND  K2→+3.3V
                                |
                            (pino 2 COM)
```

- Circuito dentro de um retangulo com borda tracejada e texto "DETALHE: CIRCUITO CLAMP S1"
- Setas indicando a direcao do sinal
- Texto explicativo:
  - "Se Vsensor > 3.6V → D2 conduz para 3.3V (protege GPIO)"
  - "Se Vsensor < -0.3V → D1 conduz para GND (protege GPIO)"
  - "I_clamp max = (5V - 3.3V) / 1kΩ = 1.7 mA"

---

## LEGENDAS E NOTAS

### Legenda de Sensores (canto superior direito)
```
TIPOS DE SENSOR:
H04 — Sensor IR (EM MÃOS, pull-up 10kΩ interno a 5V)
E07 — Sensor IR (COMPRAR, mesmo modelo)
E12 — E-STOP cogumelo (COMPRAR, NC fail-safe)
```

### Notas Técnicas (parte inferior, dentro da moldura)
1. "SENSORES IR: saida digital 5V com pull-up 10kΩ interno — OBRIGATORIO protecao BAT54S + R1kΩ"
2. "board_config.h: AV_PIN_S1=GPIO25, AV_PIN_S2=GPIO26, AV_PIN_ESTOP=GPIO27"
3. "AV_INPUTS_ACTIVE_LOW = 1 → logica invertida (LOW = ativo, HIGH = inativo)"
4. "E-STOP: contato NC (fail-safe) — se o fio romper, o circuito abre e o sistema PARA"
5. "Todos os jumpers internos da protoboard sao H06 (kit jumpers em maos)"

---

## SECTION WRAPPER

```html
<section id="wiring-2" class="sheet-section">
  <h2>BLOCO W2 — REDE DE SENSORES E E-STOP (Folha 2/5)</h2>
  <div class="canvas-wrap">
    <svg viewBox="0 0 1400 900" width="1400" height="900" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <pattern id="grid-w2" width="10" height="10" patternUnits="userSpaceOnUse">
          <path d="M 10 0 L 0 0 0 10" fill="none" stroke="var(--grid)" stroke-width="0.3"/>
        </pattern>
        <pattern id="grid-major-w2" width="50" height="50" patternUnits="userSpaceOnUse">
          <path d="M 50 0 L 0 0 0 50" fill="none" stroke="var(--grid-major)" stroke-width="0.6"/>
        </pattern>
        <pattern id="hatch-w2" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <line x1="0" y1="0" x2="0" y2="4" stroke="var(--line-thin)" stroke-width="0.3"/>
        </pattern>
        <marker id="arrow-w2" viewBox="0 0 10 6" refX="10" refY="3"
                markerWidth="8" markerHeight="5" orient="auto-start-reverse">
          <polygon points="0,0 10,3 0,6" fill="var(--line)"/>
        </marker>
      </defs>
      <!-- todo o conteudo SVG aqui -->
    </svg>
  </div>
</section>
```

---

## CORREÇÃO RETROATIVA DO BLOCO W1

O Bloco W1 (ja inserido) usou blocos retangulares simplificados para os componentes. O padrao correto (definido acima) e usar os **desenhos reais dos componentes** copiados da Aba 1. Se possivel, atualize o W1 junto com a insercao do W2:

- **E01 (Fonte)** → copiar desenho real do Bloco 2
- **E02 (Buck 6V)** → copiar desenho real do Bloco 2
- **E03 (Buck 5V)** → copiar desenho real do Bloco 2
- **E06 (Capacitor)** → copiar desenho real do Bloco 7
- **E15 (Disjuntor)** → copiar desenho real do Bloco 3
- **E16 (Porta-fusiveis)** → copiar desenho real do Bloco 3
- **E17/X1 (Borne)** → copiar desenho real do Bloco 9
- **E19 (Cabo AC)** → manter simplificado (e apenas um cabo)
- **H01 (ESP32)** → copiar desenho real do Bloco 1 (parcial: VIN/GND/3V3)
- **Aumentar viewBox do W1** para `1400 900` (mesmo do W2)
- **Ajustar moldura** para (20,20,1360,860) e (25,25,1350,850)
- Manter todos os 20 fios (W001-W020) existentes, apenas reconectando aos pads reais dos componentes

**Se a correção do W1 tornar o prompt muito longo, pule esta parte e faca SOMENTE o W2. A correção do W1 pode ser feita num prompt separado depois.**

---

## CHECKLIST FINAL

### Bloco W2
- [ ] Section id="wiring-2" com class="sheet-section"
- [ ] Titulo h2: `BLOCO W2 — REDE DE SENSORES E E-STOP (Folha 2/5)`
- [ ] ViewBox 1400×900
- [ ] Pattern IDs unicos (grid-w2, grid-major-w2, hatch-w2, arrow-w2)
- [ ] Grid duplo + moldura dupla (dimensoes 1400×900)
- [ ] Marker de seta arrow-w2 definido no defs

### Componentes (DESENHOS REAIS)
- [ ] H04 Sensor IR S1 — desenho REAL copiado do Bloco 4 (com scale/translate)
- [ ] E07 Sensor IR S2 — desenho REAL copiado do Bloco 4
- [ ] E12 E-STOP — desenho REAL copiado do Bloco 4
- [ ] X2 Borne SAK — desenho REAL copiado do Bloco 9 (7 vias)
- [ ] E26 Protoboard — desenho REAL copiado do Bloco 8
- [ ] E11 Resistor 1kΩ × 2 — desenho REAL copiado do Bloco 7 (montados na E26)
- [ ] E10 BAT54S × 2 — desenho REAL copiado do Bloco 6 (montados na E26)
- [ ] H01 ESP32 DevKit — desenho COMPLETO do Bloco 1 (GPIO25/26/27 destacados)
- [ ] NENHUM componente como bloco retangular simplificado

### Fiação
- [ ] 22 fios (W021 a W042) desenhados como linhas entre terminais REAIS
- [ ] Fios de campo (W021-W028) com etiqueta + spec "0.5mm² COR"
- [ ] Fios borne→protoboard (W029-W031) com etiqueta
- [ ] Fios internos protoboard (W032-W042) com tracejado curto diferenciado
- [ ] Fios ortogonais (nunca diagonais), sem cruzamentos
- [ ] Juncoes nos pontos de conexao
- [ ] Detalhe ampliado do circuito clamp S1

### Integridade
- [ ] SOMENTE variaveis CSS — zero cores literais no SVG
- [ ] Tabela de fios na parte inferior
- [ ] Notas tecnicas (5 notas) incluindo GPIOs e AV_INPUTS_ACTIVE_LOW
- [ ] Bloco de titulo (Folha 2/5, REV A, NOV 2026)
- [ ] Legenda de sensores no canto superior direito
- [ ] NAO alterou nada da Aba 1, W1, CSS, script, header, tab-bar
- [ ] Tema claro/escuro funciona corretamente
