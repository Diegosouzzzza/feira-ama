# PROMPT — BLOCO 06: DRIVERS E DIODOS (Folha 6/9)

## CONTEXTO

Voce esta editando o arquivo unico:
`file:///C:/Users/ponto/OneDrive/Desktop/FEIRA%20-%20AMA/desenho-eletrico/esp32.html`

Os Blocos 1, 2, 3, 4 e 5 ja existem e foram **aprovados**. Voce deve:

1. **INSERIR o Bloco 6** como nova `<section>` logo apos o `</section>` do Bloco 5 (antes do comentario `<!-- BLOCOS 5 A 9 -->`)
2. **Adicionar o pill** no `<nav>` existente, depois do pill do Bloco 5, no formato padrao:
   ```html
   <a href="#bloco-6" class="nav-pill">FOLHA 6/9: DRIVERS E DIODOS (E04, E05, E10)</a>
   ```
3. **Atualizar o span placeholder** de "FOLHAS 6-9" para "FOLHAS 7-9"

**NAO altere NADA do CSS, do `<script>`, do header nem dos Blocos 1/2/3/4/5 existentes**, exceto o nav.

---

## REGRAS DE ESTILO CAD (manter 100% igual aos Blocos anteriores)

1. **ViewBox**: `0 0 900 600`, width="900" height="600"
2. **Patterns (defs)**: IDs unicos: `grid-b6`, `grid-major-b6`, `hatch-b6`
3. **Grid duplo**: fundo com `grid-b6` (10px) + `grid-major-b6` (50px)
4. **Moldura dupla**: rect externo (20,20,860,560 stroke 1.5) + interno (25,25,850,550 stroke 0.5)
5. **Cores**: SOMENTE variaveis CSS: `var(--bg)`, `var(--fg)`, `var(--line)`, `var(--line-thin)`, `var(--pin-text)`, `var(--grid)`, `var(--grid-major)`, `var(--dim)`, `var(--trace)`, `var(--pad-fill)`, `var(--tag-bg)`. NUNCA cores literais.
6. **Pads through-hole**: dois circulos concentricos (externo r=5, stroke 1; interno r=2, preenchido `var(--bg)`)
7. **Tag badge**: retangulo rx=2, fill=`var(--pad-fill)`, stroke 1.4, texto bold do codigo BOM
8. **Cotas dimensionais**: linhas de extensao, setas (poligonos triangulares), texto em mm
9. **Bloco de titulo**: PROJETO: FEIRA AMA / BLOCO: 06 — DRIVERS E DIODOS / ESCALA: N/A / FOLHA: 6/9 / DATA: NOV 2026 / REV: A
10. **Tabela de especificacoes**: mesma estrutura dos blocos anteriores

---

## COMPONENTE 1: E04 — MODULO MOSFET D4184 (Driver do Motor)

- **Tag badge**: `E04`
- **Descricao no badge**: `MODULO MOSFET D4184`
- **Subtitulo**: `DRIVER DE POTENCIA DO MOTOR GA37-520 (M13)`
- **Status**: Comprar (1 unidade, R$ 32,00)
- **Tipo**: Modulo PCB com MOSFET duplo AOD4184A
- **Dimensoes fisicas**: ~33mm x 25mm (placa modulo)
- **Desenhar**:
  - **Placa PCB retangular** com bordas arredondadas rx=2, contorno duplo (borda PCB + trilhas)
  - **2 MOSFETs AOD4184** no centro: dois retangulos com pad de dissipacao termica (TO-252/DPAK), cada um com texto "AOD4184" ou simbolo MOSFET (G/D/S)
  - **Bornes de parafuso** (screw terminals) nos dois lados:
    - Lado de controle (esquerda): 3 terminais — `SIG`, `VCC`, `GND`
    - Lado de potencia (direita): 4 terminais — `VIN+`, `VIN-`, `VOUT+`, `VOUT-`
  - **LED indicador** de ativacao: pequeno circulo na PCB
  - **Resistor de pull-down** no gate: retangulo pequeno com valor "10kΩ"
  - **Resistor de gate**: retangulo com valor "100Ω"
  - **Detalhe do circuito simplificado**: diagrama do MOSFET com Gate, Drain, Source e corpo (body diode) — pode ser um simbolo esquematico ao lado
  - **Especificacoes** no corpo ou ao lado:
    - MOSFET: AOD4184A, N-channel
    - Vds max: 40V
    - Id max: 15A (modulo limitado a ~15A)
    - Vgs(th): 1.0-2.5V (compativel 3.3V do ESP32)
    - Rds(on): ~12mΩ @ Vgs=4.5V
- **Terminais** (7 pads through-hole representando bornes de parafuso):
  - Lado controle:
    - `SIG` — Sinal de controle PWM -> `GPIO19` (AV_PIN_MOTOR_EN)
    - `VCC` — Alimentacao logica (3.3V do ESP32, opcional — muitos modulos nao precisam)
    - `GND` — Terra comum (compartilhado controle + potencia)
  - Lado potencia:
    - `VIN+` — Entrada de potencia +12V (da Fonte E01)
    - `VIN-` — Entrada GND potencia
    - `VOUT+` — Saida para Motor M13 terminal M+
    - `VOUT-` — Saida para Motor M13 terminal M-
- **Notas abaixo**:
  - "GPIO19 = AV_PIN_MOTOR_EN, ativo HIGH (conforme board_config.h)"
  - "PWM 20 kHz (LEDC Channel 1) — controle de velocidade da esteira"
  - "Firmware tambem suporta BTS7960 como driver alternativo (GPIO21/22/23)"
- **Cotas**: 33 x 25 mm (PCB modulo)

---

## COMPONENTE 2: E05 — DIODO SCHOTTKY 1N5822 (Flyback do Motor)

- **Tag badge**: `E05`
- **Descricao no badge**: `DIODO SCHOTTKY 1N5822`
- **Subtitulo**: `FLYBACK DO MOTOR GA37-520 (PROTECAO DO MOSFET E04)`
- **Status**: Comprar (2 unidades: 1 uso + 1 reserva, R$ 2,00/un)
- **Tipo**: Diodo Schottky axial through-hole (encapsulamento DO-201AD)
- **Dimensoes fisicas**: corpo ~5.2mm diam x ~9.5mm comprimento, terminais axiais
- **Desenhar**:
  - **Vista lateral** do diodo axial:
    - **Corpo cilindrico** representado como retangulo com cantos arredondados rx=3
    - **Faixa do catodo (K)**: banda/faixa larga numa das extremidades (usar stroke mais grosso ou hachura fina)
    - **Terminais axiais**: linhas saindo de cada lado do corpo
    - **Texto "1N5822"** dentro do corpo
  - **Simbolo esquematico do diodo Schottky** ao lado (referencia visual):
    - Triangulo + barra com "ganchinhos" nas pontas (simbolo Schottky padrao)
    - Anodo (A) e Catodo (K) rotulados
  - **Indicacao de instalacao**: seta tracejada mostrando que este diodo e colocado **em paralelo reverso** com os terminais do motor M13
    - Catodo (K) → terminal M+ do motor
    - Anodo (A) → terminal M- do motor (GND)
  - **Especificacoes** no corpo ou ao lado:
    - Vrrm: 40V
    - If(avg): 3A
    - Vf: 0.525V @ 3A (queda tipica Schottky)
    - Surge: 80A (8.3ms)
    - Encapsulamento: DO-201AD
- **Terminais** (2 pads through-hole):
  - `K` (Catodo) — Liga ao M+ do motor (potencial +12V)
  - `A` (Anodo) — Liga ao M- do motor (GND)
- **Notas abaixo**:
  - "Montado em antiparalelo com o motor M13 — absorve picos de tensao reversa (flyback) quando o MOSFET desliga"
  - "Protege o MOSFET E04 e toda a linha de 12V contra spikes indutivos"
  - "Reserva: 1 unidade adicional (total 2 na BOM)"
- **Cotas**: diam 5.2mm corpo, comprimento 9.5mm, terminais axiais

---

## COMPONENTE 3: E10 — DIODO SCHOTTKY DUPLO BAT54S (Clamp de Protecao GPIO)

- **Tag badge**: `E10`
- **Descricao no badge**: `DIODO BAT54S (SOT-23)`
- **Subtitulo**: `CLAMP ANTISSOBRETENSAO — PROTECAO GPIO25 (S1) E GPIO26 (S2)`
- **Status**: Comprar (5 unidades, R$ 2,00/un — sobras para reserva)
- **Tipo**: Diodo Schottky duplo em serie, encapsulamento SMD SOT-23 (3 pinos)
- **Dimensoes fisicas**: ~3.0mm x 1.4mm x 1.1mm (SOT-23 padrao)
- **Desenhar**:
  - **Vista superior do SOT-23** (representacao ampliada para legibilidade):
    - Corpo retangular pequeno com chanfro/marca no pino 1
    - **3 pinos SMD**: pino 1 (esquerda inferior), pino 2 (direita), pino 3 (esquerda superior)
    - Texto "BAT54S" dentro do corpo
  - **Diagrama interno** do BAT54S ao lado (simbolo esquematico ampliado):
    - Dois diodos Schottky em serie: D1 e D2
    - Pino 1 (A1): Anodo de D1 → conecta ao GND
    - Pino 2 (K1/A2): Juncao comum → conecta a linha do sinal (via resistor E11)
    - Pino 3 (K2): Catodo de D2 → conecta ao +3.3V
    - Mostrar as setas dos diodos no sentido correto
  - **Circuito de aplicacao** (desenhar como mini-esquema simplificado abaixo do componente):
    - Sensor IR (H04/E07) → fio → Resistor 1kΩ (E11, em serie) → Pino 2 do BAT54S → GPIO do ESP32
    - Pino 1 → GND
    - Pino 3 → +3.3V
    - Texto: "Se Vsensor > 3,6V → D2 conduz para 3,3V (protege GPIO)"
    - Texto: "Se Vsensor < -0,3V → D1 conduz para GND (protege GPIO)"
  - **ALERTA OBRIGATORIO** em destaque (retangulo com borda grossa):
    - Texto: "OBRIGATORIO — sensor IR retangular tem pull-up interno 10kΩ a 5V"
    - Texto: "Sem o BAT54S + R 1kΩ (E11), a GPIO 3,3V do ESP32 QUEIMA"
  - **Especificacoes**:
    - Vr: 30V
    - If: 200mA
    - Vf: 0.24V @ 1mA (muito baixa queda Schottky)
    - Encapsulamento: SOT-23
    - Configuracao: Serie (A1→K1/A2→K2)
- **Terminais** (3 pads — estes sao SMD mas desenhar como pads para consistencia CAD):
  - `A1` (Pino 1) — Anodo D1 → GND
  - `COM` (Pino 2) — Juncao K1/A2 → Sinal do sensor (via R 1kΩ E11)
  - `K2` (Pino 3) — Catodo D2 → +3.3V (barramento logico ESP32)
- **Notas abaixo**:
  - "1 BAT54S por canal: S1 (GPIO25) e S2 (GPIO26) — total 2 em uso + 3 reserva"
  - "Sempre instalar COM o resistor E11 (1kΩ 1/4W) em serie ANTES do BAT54S"
  - "Necessario porque AV_INPUTS_ACTIVE_LOW = 1 (board_config.h)"
- **Cotas**: 3.0 x 1.4 x 1.1 mm (SOT-23)

---

## TABELA DE ESPECIFICACOES

| TAG | COMPONENTE | ESPECIFICACAO | FUNCAO NO PROJETO |
|-----|-----------|---------------|-------------------|
| E04 | Modulo MOSFET D4184 | AOD4184A, 40V/15A, Vgs 3.3V | Driver PWM do motor M13 (GPIO19, LEDC Ch.1) |
| E05 | Diodo Schottky 1N5822 (x2) | 40V/3A, DO-201AD, Vf 0.525V | Flyback do motor M13 (protecao MOSFET E04) |
| E10 | Diodo BAT54S SOT-23 (x5) | 30V/200mA, dual serie, Vf 0.24V | Clamp GPIO25/GPIO26 (protecao ESP32 H01) |

---

## SECTION WRAPPER

```html
<section id="bloco-6" class="sheet-section">
  <h2>BLOCO 06 — DRIVERS E DIODOS (Folha 6/9)</h2>
  <div class="canvas-wrap">
    <svg viewBox="0 0 900 600" width="900" height="600" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <!-- patterns grid-b6, grid-major-b6, hatch-b6 aqui -->
      </defs>
      <!-- todo o conteudo SVG aqui -->
    </svg>
  </div>
</section>
```

---

## CHECKLIST FINAL

- [ ] Section id="bloco-6" com class="sheet-section"
- [ ] Titulo h2: `BLOCO 06 — DRIVERS E DIODOS (Folha 6/9)`
- [ ] Pattern IDs unicos (grid-b6, grid-major-b6, hatch-b6)
- [ ] Grid duplo + moldura dupla
- [ ] 3 componentes (E04, E05, E10) com badges de tag proeminentes
- [ ] Cotas dimensionais em mm em todos os componentes
- [ ] Todos os terminais com pads through-hole (dois circulos concentricos)
- [ ] Tabela de especificacoes na parte inferior
- [ ] Bloco de titulo (Folha 6/9) no canto inferior direito
- [ ] SOMENTE variaveis CSS — zero cores literais
- [ ] Pill adicionado ao nav no formato longo padrao
- [ ] Span placeholder atualizado para "FOLHAS 7-9"
- [ ] Tema claro/escuro: apenas usar variaveis, nao alterar CSS/script
- [ ] NAO alterou nada nos Blocos 1/2/3/4/5
- [ ] NAO alterou o CSS nem o script
- [ ] GPIO correto: Motor_EN = GPIO19 (AV_PIN_MOTOR_EN)
- [ ] Tensoes corretas: Motor = 12V (E01), Logica = 3.3V (ESP32)
- [ ] E05 em antiparalelo com motor (Catodo no M+, Anodo no M-)
- [ ] E10 com circuito de aplicacao mostrando R 1kΩ (E11) em serie
- [ ] Alerta OBRIGATORIO sobre pull-up 10kΩ do sensor IR visivel
