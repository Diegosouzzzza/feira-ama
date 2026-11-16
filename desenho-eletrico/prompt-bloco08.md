# PROMPT — BLOCO 08: SINALIZAÇÃO E MONTAGEM (Folha 8/9)

## CONTEXTO

Voce esta editando o arquivo unico:
`file:///C:/Users/ponto/OneDrive/Desktop/FEIRA%20-%20AMA/desenho-eletrico/esp32.html`

Os Blocos 1, 2, 3, 4, 5, 6 e 7 ja existem e foram **aprovados**. Voce deve:

1. **INSERIR o Bloco 8** como nova `<section>` logo apos o `</section>` do Bloco 7 (antes do comentario `<!-- BLOCOS 5 A 9 -->`)
2. **Adicionar o pill** no `<nav>` existente, depois do pill do Bloco 7, no formato padrao:
   ```html
   <a href="#bloco-8" class="nav-pill">FOLHA 8/9: SINALIZAÇÃO E MONTAGEM (E13, E25, E26)</a>
   ```
3. **Atualizar o span placeholder** de "FOLHAS 8-9" para "FOLHA 9"

**NAO altere NADA do CSS, do `<script>`, do header nem dos Blocos 1/2/3/4/5/6/7 existentes**, exceto o nav.

---

## REGRAS DE ESTILO CAD (manter 100% igual aos Blocos anteriores)

1. **ViewBox**: `0 0 900 600`, width="900" height="600"
2. **Patterns (defs)**: IDs unicos: `grid-b8`, `grid-major-b8`, `hatch-b8`
3. **Grid duplo**: fundo com `grid-b8` (10px) + `grid-major-b8` (50px)
4. **Moldura dupla**: rect externo (20,20,860,560 stroke 1.5) + interno (25,25,850,550 stroke 0.5)
5. **Cores**: SOMENTE variaveis CSS: `var(--bg)`, `var(--fg)`, `var(--line)`, `var(--line-thin)`, `var(--pin-text)`, `var(--grid)`, `var(--grid-major)`, `var(--dim)`, `var(--trace)`, `var(--pad-fill)`, `var(--tag-bg)`. NUNCA cores literais.
6. **Pads through-hole**: dois circulos concentricos (externo r=5, stroke 1; interno r=2, preenchido `var(--bg)`)
7. **Tag badge**: retangulo rx=2, fill=`var(--pad-fill)`, stroke 1.4, texto bold do codigo BOM
8. **Cotas dimensionais**: linhas de extensao, setas (poligonos triangulares), texto em mm
9. **Bloco de titulo**: PROJETO: FEIRA AMA / BLOCO: 08 — SINALIZAÇÃO E MONTAGEM / ESCALA: N/A / FOLHA: 8/9 / DATA: NOV 2026 / REV: A
10. **Tabela de especificacoes**: mesma estrutura dos blocos anteriores

---

## COMPONENTE 1: E13 — RING LIGHT LED 12V 6000K

- **Tag badge**: `E13`
- **Descricao no badge**: `RING LIGHT LED 12V 6000K`
- **Subtitulo**: `ILUMINAÇÃO DA CÚPULA ÓPTICA — VISÃO COMPUTACIONAL (WEBCAM E14)`
- **Status**: Comprar (1 unidade, R$ 45,00)
- **Tipo**: Anel LED SMD branco frio, alimentacao 12V DC
- **Dimensoes fisicas**: diametro externo ~80-90 mm, espessura ~8 mm
- **Desenhar**:
  - **Vista frontal** do anel LED:
    - **Anel circular** representado como dois circulos concentricos (externo e interno) formando a PCB anelar
    - **LEDs SMD** distribuidos ao redor do anel: representar como pequenos retangulos (pads SMD) espacados uniformemente ao longo do anel (12 a 24 LEDs tipicamente)
    - **Furo central** do anel (onde a webcam E14 mira atraves): circulo central vazio com texto "FURO Ø ~50mm" e nota "(WEBCAM E14 AQUI)"
    - **2 terminais de alimentacao**: fios ou pads marcados `+12V` e `GND` saindo da PCB do anel
    - **Adesivo/fixador de montagem**: indicar que o anel cola na parte interna da cupula optica
  - **Vista lateral** (corte, menor, ao lado):
    - PCB fina do anel com LEDs no topo
    - Dissipador de calor / substrato de aluminio
    - Fios de alimentacao saindo por tras
  - **Diagrama de instalacao** (mini-esquema simplificado):
    - Fonte 12V (E01) → linha +12V → Ring Light E13 → GND
    - Texto: "Ligacao direta ao barramento +12V — sempre ON quando o sistema esta energizado"
    - Texto alternativo: "Ou controlado via rele E08 (Bloco 3) para ligar/desligar com o sistema"
  - **Especificacoes** no corpo ou ao lado:
    - Tensao de operacao: 12V DC
    - Temperatura de cor: 6000K (branco frio)
    - Diametro externo: 80-90 mm
    - Angulo de iluminacao: ~120° (LED SMD)
    - Consumo estimado: ~3-5W
    - Luminosidade: ~300-500 lm (suficiente para iluminacao uniforme da area de classificacao)
- **Terminais** (2 pads through-hole para consistencia CAD):
  - `+12V` — Barramento positivo de 12V (Fonte E01 / via rele E08)
  - `GND` — Terra comum
- **Notas abaixo**:
  - "Montado no interior da cupula optica, acima da esteira, iluminando a area de visao da webcam E14"
  - "Iluminacao uniforme e essencial para a classificacao por visao computacional"
  - "Branco frio 6000K: maximiza contraste para deteccao de cor e textura da castanha"
  - "Consumo ~3-5W — cabe na margem da Fonte 12V (E01, 120W total)"
- **Cotas**: diametro externo 80-90mm, furo central ~50mm, espessura ~8mm

---

## COMPONENTE 2: E25 — BUZZER 5V ATIVO

- **Tag badge**: `E25`
- **Descricao no badge**: `BUZZER 5V ATIVO`
- **Subtitulo**: `ALARME SONORO NR-12 — INDICAÇÃO AUDÍVEL DE EMERGÊNCIA`
- **Status**: Comprar (1 unidade, R$ 8,00) — Recomendado
- **Tipo**: Buzzer piezoeletrico ativo (oscilador interno), encapsulamento cilindrico through-hole
- **Dimensoes fisicas**: ~12mm diam x ~9.5mm altura (tipico buzzer ativo 5V)
- **Desenhar**:
  - **Vista frontal** do buzzer:
    - **Corpo cilindrico** representado como retangulo com topo semicircular (dome do diafragma)
    - **Abertura sonora** no topo: pequeno orificio circular ou fenda (indicar com circulo ou linhas radiais)
    - **Marca de polaridade**: simbolo "+" no lado do terminal positivo, ou ponto marcador
    - **2 terminais** saindo da base: pino longo (+) e pino curto (-)
    - **Etiqueta "ATIVO"** (nao precisa de sinal PWM — basta aplicar 5V para soar)
  - **Vista superior** (menor, ao lado):
    - Circulo com marca "+" de polaridade e orificio sonoro no centro
  - **Simbolo esquematico** do buzzer ao lado:
    - Retangulo com simbolo de som (ondas sonoras) e terminais +/-
  - **Circuito de acionamento** (mini-esquema):
    - GPIO (a definir) → Transistor NPN (base com resistor ~1kΩ) → Buzzer 5V → +5V
    - Ou: GPIO → MOSFET N-channel → Buzzer → +5V
    - Texto: "Buzzer ATIVO: oscilador interno, basta aplicar 5V DC para emitir som"
    - Texto: "Acionar via transistor/MOSFET pois corrente do buzzer (~30-80mA) excede limite do GPIO"
    - Texto: "GPIO do buzzer NAO definido no board_config.h atual — reservar GPIO livre"
  - **Tabela de condicoes NR-12**:
    - "E-STOP ativo → buzzer ON (som continuo)"
    - "Falha de sensor → buzzer ON (som intermitente)"
    - "Operacao normal → buzzer OFF"
  - **Especificacoes**:
    - Tensao de operacao: 5V DC (±0.5V)
    - Tipo: Ativo (oscilador interno ~2.3 kHz)
    - Nivel sonoro: ~85 dB @ 10cm
    - Corrente de operacao: ~30-80 mA
    - Frequencia de resonancia: ~2.3 kHz (fixa)
    - Encapsulamento: Cilindrico through-hole
- **Terminais** (2 pads through-hole):
  - `+` (Positivo) — Coletor do transistor de acionamento (via +5V do Buck E03)
  - `-` (Negativo/GND) — Via transistor NPN ao GPIO do ESP32
- **Notas abaixo**:
  - "Alarme sonoro obrigatorio pela NR-12 para indicacao auditiva de parada de emergencia"
  - "Alimentacao 5V do Buck MP1584EN (E03) — NAO alimentar dos 3.3V do ESP32"
  - "Corrente de ~30-80mA excede o limite de 12mA por GPIO — usar transistor de acionamento"
  - "GPIO do buzzer a ser definido no firmware (sugestao: GPIO4 ou GPIO5, livres no board_config.h)"
  - "Montagem no painel frontal do Quadro de Comando (E27, Bloco 9)"
- **Cotas**: diam 12mm, altura 9.5mm, pitch entre pinos ~6.5mm

---

## COMPONENTE 3: E26 — PROTOBOARD 830 PONTOS (MB-102)

- **Tag badge**: `E26`
- **Descricao no badge**: `PROTOBOARD 830 PONTOS (MB-102)`
- **Subtitulo**: `BASE CENTRAL DE MONTAGEM LÓGICA DO ESP32 E SINAL`
- **Status**: Comprar (1 unidade, R$ 25,00)
- **Tipo**: Breadboard sem solda, padrao MB-102, 830 pontos de insercao
- **Dimensoes fisicas**: ~165mm x 55mm x ~10mm (padrao MB-102)
- **Desenhar**:
  - **Vista superior** (planta) da protoboard:
    - **Retangulo principal** da placa com bordas arredondadas
    - **2 barramentos laterais** (power rails) em cada lado: linhas vermelha (+) e azul (-) representadas com tracejado diferenciado (monocromatico)
      - Barramento superior: `+5V` e `GND`
      - Barramento inferior: `+3.3V` e `GND`
    - **Canaleta central (DIP groove)**: linha central que separa as duas metades
    - **Furos de insercao**: representar como uma malha de pontos uniformes (simplificado — nao precisa desenhar todos os 830)
    - **Malha de 5 pontos conectados**: indicar com colchete que cada coluna de 5 furos e eletricamente conectada (a-b-c-d-e e f-g-h-i-j)
    - **Orelhas/fixadores** nas 4 pontas: circulos indicando furos de montagem
  - **Mapa de ocupacao** (layout esquematico simplificado mostrando QUEM monta onde):
    - Zona 1 (esquerda): "ESP32 DevKit (H01)" montado atravessando a canaleta central
    - Zona 2 (centro-esquerda): "BAT54S (E10) + R1kΩ (E11) — Clamp S1/S2"
    - Zona 3 (centro-direita): "LEDs (H05) + R330Ω — Sinalizacao"
    - Zona 4 (direita): "Capacitor E06 (buffer) — se necessario"
    - Texto: "Apenas componentes de SINAL e LOGICA na protoboard"
  - **ALERTA OBRIGATORIO** em destaque (retangulo com borda grossa):
    - Texto: "REGRA DE OURO: Correntes de POTENCIA (Servo MG996R / Motor GA37)"
    - Texto: "devem correr por FORA da protoboard!"
    - Texto: "Compartilhar apenas a linha de GND COMUM"
  - **Diagrama de conexao simplificado** mostrando:
    - Barramento +5V ← Buck MP1584EN (E03)
    - Barramento +3.3V ← Regulador interno do ESP32
    - GND COMUM → compartilhado com circuitos de potencia
  - **Especificacoes**:
    - Modelo: MB-102 (padrao generico)
    - Pontos de insercao: 830
    - Pitch: 2.54mm (0.1")
    - Canaleta central DIP: aceita CI de 7.62mm (0.3") a 22.86mm (0.9")
    - Barramentos: 2 laterais × 2 lados = 4 linhas de alimentacao
    - Material: ABS com contatos de bronze fosforoso
    - Corrente max por trilha: ~1A (nao exceder — regra de ouro)
- **Terminais** (4 pads through-hole representando os pontos de alimentacao principais):
  - `+5V` — Barramento positivo 5V (do Buck E03)
  - `+3.3V` — Barramento positivo 3.3V (regulador do ESP32)
  - `GND_1` — Terra comum barramento superior
  - `GND_2` — Terra comum barramento inferior
- **Notas abaixo**:
  - "Base central de montagem: ESP32 (H01), clamps BAT54S (E10), resistores (E11), LEDs (H05)"
  - "REGRA DE OURO: servo MG996R e motor GA37 ficam FORA da protoboard — so GND comum"
  - "Corrente max por trilha da protoboard: ~1A — adequado para sinais e logica, insuficiente para atuadores"
  - "Fixada dentro do Quadro de Comando (E27, Bloco 9) com parafusos nos 4 cantos"
  - "Jumpers Dupont (H06, em maos) para fiacao na protoboard"
- **Cotas**: 165 x 55 x 10 mm, pitch 2.54mm, furos de fixacao nos cantos

---

## TABELA DE ESPECIFICACOES

| TAG | COMPONENTE | ESPECIFICACAO | FUNCAO NO PROJETO |
|-----|-----------|---------------|-------------------|
| E13 | Ring Light LED 12V 6000K (x1) | Anel Ø 80-90mm, 12V DC, 6000K | Iluminacao da cupula optica (webcam E14) |
| E25 | Buzzer 5V Ativo (x1) | Cilindrico, ~85dB, oscilador interno | Alarme sonoro NR-12 (emergencia/falha) |
| E26 | Protoboard 830 pontos MB-102 (x1) | 165×55mm, pitch 2.54mm, 830pts | Base central de montagem logica ESP32 |

---

## SECTION WRAPPER

```html
<section id="bloco-8" class="sheet-section">
  <h2>BLOCO 08 — SINALIZAÇÃO E MONTAGEM (Folha 8/9)</h2>
  <div class="canvas-wrap">
    <svg viewBox="0 0 900 600" width="900" height="600" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <!-- patterns grid-b8, grid-major-b8, hatch-b8 aqui -->
      </defs>
      <!-- todo o conteudo SVG aqui -->
    </svg>
  </div>
</section>
```

---

## CHECKLIST FINAL

- [ ] Section id="bloco-8" com class="sheet-section"
- [ ] Titulo h2: `BLOCO 08 — SINALIZAÇÃO E MONTAGEM (Folha 8/9)`
- [ ] Pattern IDs unicos (grid-b8, grid-major-b8, hatch-b8)
- [ ] Grid duplo + moldura dupla
- [ ] 3 componentes (E13, E25, E26) com badges de tag proeminentes
- [ ] Cotas dimensionais em mm em todos os componentes
- [ ] Todos os terminais com pads through-hole (dois circulos concentricos)
- [ ] Tabela de especificacoes na parte inferior
- [ ] Bloco de titulo (Folha 8/9) no canto inferior direito
- [ ] SOMENTE variaveis CSS — zero cores literais
- [ ] Pill adicionado ao nav no formato longo padrao
- [ ] Span placeholder atualizado para "FOLHA 9"
- [ ] Tema claro/escuro: apenas usar variaveis, nao alterar CSS/script
- [ ] NAO alterou nada nos Blocos 1/2/3/4/5/6/7
- [ ] NAO alterou o CSS nem o script
- [ ] E13: anel LED com furo central, referencia a webcam E14 e cupula optica
- [ ] E13: alimentacao 12V DC (Fonte E01), mencao ao rele E08 como alternativa
- [ ] E25: buzzer ATIVO (nao passivo), 5V do Buck E03
- [ ] E25: circuito de acionamento via transistor (corrente > 12mA do GPIO)
- [ ] E25: condicoes NR-12 (E-STOP → som continuo, falha → intermitente)
- [ ] E26: mapa de ocupacao mostrando quem monta onde na protoboard
- [ ] E26: ALERTA "regra de ouro" — potencia FORA da protoboard, so GND comum
- [ ] E26: barramentos +5V (E03), +3.3V (ESP32), GND comum
