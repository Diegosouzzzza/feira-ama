# PROMPT — BLOCO 07: PASSIVOS (Folha 7/9)

## CONTEXTO

Voce esta editando o arquivo unico:
`file:///C:/Users/ponto/OneDrive/Desktop/FEIRA%20-%20AMA/desenho-eletrico/esp32.html`

Os Blocos 1, 2, 3, 4, 5 e 6 ja existem e foram **aprovados**. Voce deve:

1. **INSERIR o Bloco 7** como nova `<section>` logo apos o `</section>` do Bloco 6 (antes do comentario `<!-- BLOCOS 5 A 9 -->`)
2. **Adicionar o pill** no `<nav>` existente, depois do pill do Bloco 6, no formato padrao:
   ```html
   <a href="#bloco-7" class="nav-pill">FOLHA 7/9: PASSIVOS (E06, E11, H05)</a>
   ```
3. **Atualizar o span placeholder** de "FOLHAS 7-9" para "FOLHAS 8-9"

**NAO altere NADA do CSS, do `<script>`, do header nem dos Blocos 1/2/3/4/5/6 existentes**, exceto o nav.

---

## REGRAS DE ESTILO CAD (manter 100% igual aos Blocos anteriores)

1. **ViewBox**: `0 0 900 600`, width="900" height="600"
2. **Patterns (defs)**: IDs unicos: `grid-b7`, `grid-major-b7`, `hatch-b7`
3. **Grid duplo**: fundo com `grid-b7` (10px) + `grid-major-b7` (50px)
4. **Moldura dupla**: rect externo (20,20,860,560 stroke 1.5) + interno (25,25,850,550 stroke 0.5)
5. **Cores**: SOMENTE variaveis CSS: `var(--bg)`, `var(--fg)`, `var(--line)`, `var(--line-thin)`, `var(--pin-text)`, `var(--grid)`, `var(--grid-major)`, `var(--dim)`, `var(--trace)`, `var(--pad-fill)`, `var(--tag-bg)`. NUNCA cores literais.
6. **Pads through-hole**: dois circulos concentricos (externo r=5, stroke 1; interno r=2, preenchido `var(--bg)`)
7. **Tag badge**: retangulo rx=2, fill=`var(--pad-fill)`, stroke 1.4, texto bold do codigo BOM
8. **Cotas dimensionais**: linhas de extensao, setas (poligonos triangulares), texto em mm
9. **Bloco de titulo**: PROJETO: FEIRA AMA / BLOCO: 07 — PASSIVOS / ESCALA: N/A / FOLHA: 7/9 / DATA: NOV 2026 / REV: A
10. **Tabela de especificacoes**: mesma estrutura dos blocos anteriores

---

## COMPONENTE 1: E06 — CAPACITOR ELETROLITICO 1000 µF / 16V

- **Tag badge**: `E06`
- **Descricao no badge**: `CAP. ELETROLITICO 1000µF/16V`
- **Subtitulo**: `BUFFER DE CORRENTE DO SERVO MG996R — SAIDA DO BUCK E02`
- **Status**: Comprar (2 unidades, R$ 3,00/un)
- **Tipo**: Capacitor eletrolitico radial through-hole, polarizado
- **Dimensoes fisicas**: corpo ~10mm diam x ~16mm altura (radial, terminais para baixo)
- **Desenhar**:
  - **Vista frontal** do capacitor radial:
    - **Corpo cilindrico** representado como retangulo com topo arredondado (semicirculo) para indicar formato cilindrico
    - **Faixa de polaridade negativa (-)**: banda/faixa no lado do terminal negativo com setas "- - -" apontando para o catodo. Usar hachura ou tracos para diferenciar visualmente
    - **Marcacao "+"** na lateral superior, proximo ao terminal positivo
    - **Textos gravados no corpo**: "1000µF", "16V", "105°C"
    - **2 terminais radiais** saindo da base (perna +, perna -)
    - **Selo de alivio** (vent) no topo: 2 linhas finas cruzadas em X
  - **Vista superior** (menor, ao lado): circulo com marca de polaridade (meia-lua sombreada no lado -)
  - **Detalhe de identificacao de polaridade**: legenda mostrando que o terminal mais longo = positivo (+) e mais curto = negativo (-)
  - **Especificacoes** no corpo ou ao lado:
    - Capacitancia: 1000 µF
    - Tensao maxima: 16V (margem OK para 6V do servo)
    - ESR tipico: ~30mΩ a 100kHz
    - Ripple current: ~1.2A (105°C)
    - Temperatura: -40°C a 105°C
- **Terminais** (2 pads through-hole):
  - `+` (Positivo/Anodo) — Saida +6.0V do Buck XL4015 (E02)
  - `-` (Negativo/Catodo) — GND comum
- **Notas abaixo**:
  - "Instalado NA SAIDA do Buck XL4015 (E02) — absorve picos de corrente do MG996R"
  - "Servo consome ~2.5A de pico durante movimento rapido — o capacitor estabiliza a tensao"
  - "Reserva: 2 unidades na BOM (1 por canal de saida do Buck ou ambos em paralelo)"
- **Cotas**: diam 10mm corpo, altura 16mm, pitch 5mm (espacamento entre terminais)

---

## COMPONENTE 2: E11 — RESISTOR 1 kΩ 1/4W

- **Tag badge**: `E11`
- **Descricao no badge**: `RESISTOR 1kΩ 1/4W`
- **Subtitulo**: `SERIE COM BAT54S (E10) NA LINHA DO SENSOR IR`
- **Status**: Comprar (10 unidades, R$ 0,20/un — 2 em uso + 8 reserva)
- **Tipo**: Resistor de filme carbono/metal, axial through-hole
- **Dimensoes fisicas**: corpo ~6.3mm comprimento x ~2.3mm diam (encapsulamento 1/4W padrao)
- **Desenhar**:
  - **Vista lateral** do resistor axial:
    - **Corpo cilindrico** representado como retangulo com cantos arredondados rx=3
    - **4 faixas de cor** (representar como retangulos verticais dentro do corpo, com rotulos de texto pois o desenho e monocromatico):
      - Faixa 1: MARROM (1)
      - Faixa 2: PRETO (0)
      - Faixa 3: VERMELHO (x100)
      - Faixa 4: DOURADO (±5%)
    - Como o desenho e monocromatico, usar espessuras de stroke ou patterns diferentes para cada faixa, e rotular com texto ao lado:
      - "1 | 0 | x100 | ±5% = 1.000Ω"
    - **Terminais axiais** saindo de cada lado
  - **Simbolo esquematico** ao lado (retangulo com terminais, valor "1kΩ")
  - **Circuito de aplicacao** (mini-esquema, referencia cruzada com Bloco 6):
    - Sensor IR (H04/E07) → **R 1kΩ (E11)** → BAT54S (E10) → GPIO25/26 ESP32
    - Texto: "Limita corrente de clamp a ~1.7mA max quando Vsensor=5V"
    - Texto: "Ja desenhado no circuito de aplicacao do Bloco 6 (E10)"
  - **Especificacoes**:
    - Resistencia: 1.000Ω (1 kΩ)
    - Tolerancia: ±5% (faixa dourada)
    - Potencia: 1/4W (0.25W)
    - Potencia dissipada real: P = (5V-3.3V)²/1000 = 2.89 mW (margem enorme)
    - Coeficiente de temperatura: ±200 ppm/°C (filme carbono)
- **Terminais** (2 pads through-hole):
  - `IN` — Entrada do sinal vindo do sensor IR (via fio BK)
  - `OUT` — Saida para pino 2 (COM) do BAT54S (E10)
- **Notas abaixo**:
  - "1 resistor por canal: S1 (GPIO25) e S2 (GPIO26) — total 2 em uso + 8 reserva"
  - "OBRIGATORIO em conjunto com E10 (BAT54S) — ver circuito no Bloco 6"
  - "Componente nao polarizado — qualquer orientacao funciona"
- **Cotas**: 6.3mm corpo, 2.3mm diam, terminais axiais

---

## COMPONENTE 3: H05 — KIT LEDs 5mm (R/G/Y) + RESISTOR 330Ω

- **Tag badge**: `H05`
- **Descricao no badge**: `KIT LEDs 5mm + R330Ω`
- **Subtitulo**: `SINALIZACAO VISUAL DE PAINEL E STATUS OPERACIONAL`
- **Status**: Em maos (ja possui 1 kit)
- **Tipo**: LEDs difusos 5mm through-hole (Vermelho, Verde, Amarelo) + resistores limitadores 330Ω
- **Dimensoes fisicas**: LED = diam 5mm x ~8.6mm altura (T-1 3/4); Resistor = 1/4W axial
- **Desenhar**:
  - **3 LEDs lado a lado** (R, G, Y), cada um com:
    - **Corpo do LED** (vista frontal): formato de "bala" — retangulo com topo semicircular (dome), base plana com flange
    - **Lente epoxy** no topo (dome arredondado)
    - **Chanfro/flat no catodo**: marca plana na base do lado do catodo (terminal mais curto)
    - **2 terminais**: Anodo (+, mais longo) e Catodo (-, mais curto, lado do flat)
    - **Simbolo do LED** (triangulo com seta de emissao de luz) ao lado de cada um
    - **Rotulo de cor** como texto (ja que o desenho e monocromatico):
      - LED 1: "VERM" — Status: ERRO / E-STOP
      - LED 2: "VERDE" — Status: OPERANDO / OK
      - LED 3: "AMAR" — Status: PROCESSANDO / ALERTA
  - **Resistor 330Ω** desenhado UMA VEZ como componente generico (um resistor por LED):
    - Corpo axial com faixas de cor (rotuladas como texto):
      - Faixa 1: LARANJA (3)
      - Faixa 2: LARANJA (3)
      - Faixa 3: MARROM (x10)
      - Faixa 4: DOURADO (±5%)
      - "3 | 3 | x10 | ±5% = 330Ω"
    - Texto: "1 resistor por LED (330Ω 1/4W)"
  - **Calculo de corrente** em destaque:
    - "I = (3.3V - Vf) / 330Ω"
    - "Vermelho (Vf=1.8V): I = 4.5 mA"
    - "Verde (Vf=2.1V): I = 3.6 mA"
    - "Amarelo (Vf=2.0V): I = 3.9 mA"
    - "Luminosidade adequada e dentro do limite de 12mA por GPIO do ESP32"
  - **Especificacoes**:
    - Diametro: 5 mm (T-1 3/4)
    - Angulo de visao: ~30° (difuso)
    - Corrente direta max: 20 mA
    - Corrente de operacao: ~3.6-4.5 mA (via R 330Ω)
- **Terminais** (6 pads through-hole para os 3 LEDs):
  - `LED_R+` (Anodo Vermelho) — Via R 330Ω a GPIO (ou painel)
  - `LED_R-` (Catodo Vermelho) — GND
  - `LED_G+` (Anodo Verde) — Via R 330Ω a GPIO (ou painel)
  - `LED_G-` (Catodo Verde) — GND
  - `LED_Y+` (Anodo Amarelo) — Via R 330Ω a GPIO (ou painel)
  - `LED_Y-` (Catodo Amarelo) — GND
- **Notas abaixo**:
  - "board_config.h: AV_PIN_LED = GPIO2 (LED onboard do ESP32 DevKit)"
  - "LEDs externos do painel compartilham GPIO2 ou usam GPIOs extras (definir no firmware)"
  - "Cada LED SEMPRE com resistor 330Ω em serie — nunca conectar direto ao GPIO"
  - "Montagem no painel frontal do Quadro de Comando (E27, Bloco 9)"
- **Cotas**: LED = diam 5mm x 8.6mm; R330Ω = 6.3mm x 2.3mm

---

## TABELA DE ESPECIFICACOES

| TAG | COMPONENTE | ESPECIFICACAO | FUNCAO NO PROJETO |
|-----|-----------|---------------|-------------------|
| E06 | Cap. Eletrolitico 1000µF/16V (x2) | Radial, 16V, ESR ~30mΩ, 105°C | Buffer de corrente do servo (saida E02) |
| E11 | Resistor 1kΩ 1/4W (x10) | Axial, ±5%, filme carbono | Serie com E10 (BAT54S) — clamp S1/S2 |
| H05 | Kit LEDs 5mm R/G/Y + R330Ω | 5mm difuso, ~4mA via R330 | Sinalizacao de status no painel |

---

## SECTION WRAPPER

```html
<section id="bloco-7" class="sheet-section">
  <h2>BLOCO 07 — PASSIVOS (Folha 7/9)</h2>
  <div class="canvas-wrap">
    <svg viewBox="0 0 900 600" width="900" height="600" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <!-- patterns grid-b7, grid-major-b7, hatch-b7 aqui -->
      </defs>
      <!-- todo o conteudo SVG aqui -->
    </svg>
  </div>
</section>
```

---

## CHECKLIST FINAL

- [ ] Section id="bloco-7" com class="sheet-section"
- [ ] Titulo h2: `BLOCO 07 — PASSIVOS (Folha 7/9)`
- [ ] Pattern IDs unicos (grid-b7, grid-major-b7, hatch-b7)
- [ ] Grid duplo + moldura dupla
- [ ] 3 componentes (E06, E11, H05) com badges de tag proeminentes
- [ ] Cotas dimensionais em mm em todos os componentes
- [ ] Todos os terminais com pads through-hole (dois circulos concentricos)
- [ ] Tabela de especificacoes na parte inferior
- [ ] Bloco de titulo (Folha 7/9) no canto inferior direito
- [ ] SOMENTE variaveis CSS — zero cores literais
- [ ] Pill adicionado ao nav no formato longo padrao
- [ ] Span placeholder atualizado para "FOLHAS 8-9"
- [ ] Tema claro/escuro: apenas usar variaveis, nao alterar CSS/script
- [ ] NAO alterou nada nos Blocos 1/2/3/4/5/6
- [ ] NAO alterou o CSS nem o script
- [ ] E06: polaridade indicada (+ e -), tensao 16V, na saida do Buck E02
- [ ] E11: referencia cruzada com E10 (BAT54S) do Bloco 6
- [ ] H05: 3 LEDs com cores rotuladas como texto (monocromatico), calculo de corrente
- [ ] H05: cada LED com R 330Ω em serie, corrente ~3.6-4.5 mA
- [ ] GPIO2 (AV_PIN_LED) referenciado nas notas do H05
