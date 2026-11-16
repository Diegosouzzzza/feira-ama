# PROMPT — BLOCO W1: REDE DE ALIMENTAÇÃO (Folha 1/5 — Interligações)

## CONTEXTO

Voce esta editando o arquivo unico:
`file:///C:/Users/ponto/OneDrive/Desktop/FEIRA%20-%20AMA/desenho-eletrico/esp32.html`

As 9 folhas de componentes (Blocos 1-9) estao **COMPLETAS E APROVADAS** na Aba 1.
Agora voce vai criar a **ABA 2 — INTERLIGAÇÕES PONTO A PONTO** com 5 folhas de diagramas de fiação.

Este prompt cobre:
1. **Infraestrutura de abas** (tab system) no HTML
2. **Bloco W1** — Rede de Alimentação (Folha 1/5 da Aba 2)

---

## PARTE 1: SISTEMA DE ABAS

### 1.1 — CSS ADICIONAL (acrescentar DENTRO do `<style>` existente, DEPOIS de `.sheet-section`)

```css
/* ========================================================== */
/*           SISTEMA DE ABAS (COMPONENTES / INTERLIGAÇÕES)      */
/* ========================================================== */
.tab-bar {
  display: flex;
  gap: 0;
  margin: 0 auto 0;
  max-width: 940px;
  width: 100%;
  border-bottom: 2px solid var(--header-border);
}

.tab-btn {
  flex: 1;
  padding: 12px 16px;
  background: var(--tag-bg);
  color: var(--dim);
  border: 1px solid var(--header-border);
  border-bottom: none;
  cursor: pointer;
  font-family: 'Courier New', monospace;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  text-align: center;
  transition: background 0.2s, color 0.2s;
  position: relative;
  top: 2px;
}

.tab-btn:first-child {
  border-radius: 4px 0 0 0;
}

.tab-btn:last-child {
  border-radius: 0 4px 0 0;
}

.tab-btn.active {
  background: var(--bg);
  color: var(--fg);
  border-bottom: 2px solid var(--bg);
  top: 2px;
}

.tab-btn:not(.active):hover {
  background: var(--pad-fill);
  color: var(--fg);
}

.tab-content {
  display: none;
}

.tab-content.active {
  display: block;
}

/* Navegação interna da Aba 2 */
.nav-pills-w {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  max-width: 940px;
  margin: 16px auto;
  padding: 0 16px;
}

.nav-pills-w .nav-pill {
  /* herda o mesmo estilo do .nav-pill existente */
}

/* ---- FIO / WIRE styles (Aba 2) ---- */
.wire-label {
  font-family: 'Courier New', monospace;
  font-size: 7px;
  font-weight: 700;
  fill: var(--fg);
}

.wire-spec {
  font-family: 'Courier New', monospace;
  font-size: 6px;
  fill: var(--dim);
}

.wire-power {
  stroke: var(--line);
  stroke-width: 1.8;
  fill: none;
}

.wire-gnd {
  stroke: var(--line);
  stroke-width: 1.4;
  fill: none;
  stroke-dasharray: 8 3;
}

.wire-signal {
  stroke: var(--line-thin);
  stroke-width: 1.0;
  fill: none;
}

.junction-dot {
  fill: var(--fg);
  stroke: none;
}

.terminal-block {
  fill: var(--pad-fill);
  stroke: var(--line);
  stroke-width: 1.2;
}

.terminal-label {
  font-family: 'Courier New', monospace;
  font-size: 7px;
  font-weight: 700;
  fill: var(--fg);
}

.terminal-pin {
  font-family: 'Courier New', monospace;
  font-size: 6px;
  fill: var(--dim);
}

.wire-tag {
  fill: var(--tag-bg);
  stroke: var(--line-thin);
  stroke-width: 0.8;
}

.from-to {
  font-family: 'Courier New', monospace;
  font-size: 5.5px;
  fill: var(--dim);
}
```

### 1.2 — REESTRUTURAR O HTML (header → tab-bar → conteudo)

**ENTRE o `</header>` e o `<!-- NAVEGAÇÃO ENTRE FOLHAS -->` (antes do `<nav>`), inserir:**

```html
<!-- BARRA DE ABAS -->
<div class="tab-bar">
  <button class="tab-btn active" onclick="switchTab('componentes')" id="tab-btn-componentes">
    ABA 1 — COMPONENTES (9 FOLHAS)
  </button>
  <button class="tab-btn" onclick="switchTab('interligacoes')" id="tab-btn-interligacoes">
    ABA 2 — INTERLIGAÇÕES PONTO A PONTO (5 FOLHAS)
  </button>
</div>
```

**ENVOLVER todo o conteudo existente (do `<nav class="nav-pills">` ate o ultimo `</section>` do Bloco 9) com:**

```html
<div id="tab-componentes" class="tab-content active">
  <!-- nav-pills existente + 9 sections existentes, SEM ALTERAR NADA -->
</div>
```

**DEPOIS do `</div>` do tab-componentes, inserir a Aba 2:**

```html
<div id="tab-interligacoes" class="tab-content">
  <!-- NAVEGAÇÃO FOLHAS INTERLIGAÇÕES -->
  <nav class="nav-pills nav-pills-w">
    <a href="#wiring-1" class="nav-pill" onclick="switchTab('interligacoes')">W1: ALIMENTAÇÃO</a>
    <a href="#wiring-2" class="nav-pill" onclick="switchTab('interligacoes')">W2: SENSORES</a>
    <a href="#wiring-3" class="nav-pill" onclick="switchTab('interligacoes')">W3: ATUADORES</a>
    <a href="#wiring-4" class="nav-pill" onclick="switchTab('interligacoes')">W4: SINALIZAÇÃO</a>
    <a href="#wiring-5" class="nav-pill" onclick="switchTab('interligacoes')">W5: TABELA DE FIOS</a>
  </nav>

  <!-- BLOCO W1 sera inserido aqui (ver Parte 2) -->

  <!-- PLACEHOLDERS W2-W5 -->
  <!-- serao inseridos nos proximos prompts -->
</div>
```

### 1.3 — ATUALIZAR O HEADER

Trocar o texto do `<p>` no header de:
```
SISTEMA ELETRÔNICO E ELETROTÉCNICO MONOCROMÁTICO | CONJUNTO DE 9 FOLHAS TÉCNICAS
```
Para:
```
SISTEMA ELETRÔNICO E ELETROTÉCNICO MONOCROMÁTICO | COMPONENTES (9) + INTERLIGAÇÕES (5)
```

### 1.4 — JAVASCRIPT DA ABA (acrescentar DENTRO do `<script>` existente, DEPOIS de `initTheme();`)

```javascript
function switchTab(tabName) {
  document.querySelectorAll('.tab-content').forEach(function(el) {
    el.classList.remove('active');
  });
  document.querySelectorAll('.tab-btn').forEach(function(el) {
    el.classList.remove('active');
  });
  var content = document.getElementById('tab-' + tabName);
  var btn = document.getElementById('tab-btn-' + tabName);
  if (content) content.classList.add('active');
  if (btn) btn.classList.add('active');
}
```

---

## PARTE 2: BLOCO W1 — REDE DE ALIMENTAÇÃO (Folha 1/5)

### REGRAS DE ESTILO CAD (MESMAS dos blocos anteriores + estilos de fio)

1. **ViewBox**: `0 0 900 600`, width="900" height="600"
2. **Patterns (defs)**: IDs unicos: `grid-w1`, `grid-major-w1`, `hatch-w1`
3. **Grid duplo**: fundo com `grid-w1` (10px) + `grid-major-w1` (50px)
4. **Moldura dupla**: rect externo (20,20,860,560 stroke 1.5) + interno (25,25,850,550 stroke 0.5)
5. **Cores**: SOMENTE variaveis CSS. NUNCA cores literais.
6. **Pads through-hole**: dois circulos concentricos (externo r=5, stroke 1; interno r=2, preenchido `var(--bg)`)
7. **Tag badge**: retangulo rx=2, fill=`var(--pad-fill)`, stroke 1.4, texto bold do codigo BOM
8. **Bloco de titulo**: PROJETO: FEIRA AMA / BLOCO: W1 — REDE DE ALIMENTAÇÃO / ESCALA: N/A / FOLHA: 1/5 / DATA: NOV 2026 / REV: A
9. **Estilos de fio** (usar as classes CSS definidas acima):
   - Fio de potencia: `class="wire-power"` (stroke 1.8, solido)
   - Fio GND: `class="wire-gnd"` (stroke 1.4, tracejado 8 3)
   - Fio de sinal: `class="wire-signal"` (stroke 1.0, solido)
10. **Etiqueta de fio**: retangulo `class="wire-tag"` com texto `class="wire-label"` (ex: "W001")
11. **Especificacao do cabo**: texto `class="wire-spec"` ao lado (ex: "1.0mm² VM")
12. **Juncao**: circulo r=2.5, `class="junction-dot"` onde fios se conectam
13. **Terminal block**: retangulo `class="terminal-block"` com pinos numerados

### CONVENÇÕES DE FIO

| TIPO | CLASSE CSS | BITOLA | COR CABO | USO |
|------|-----------|--------|----------|-----|
| AC Fase | wire-power | 1.0mm² (E21) | VM (Vermelho) | AC 127/220V |
| AC Neutro | wire-power | 1.0mm² (E21) | AZ (Azul) | AC Neutro |
| AC Terra | wire-gnd | 1.0mm² (E21) | VD (Verde) | PE |
| DC +12V | wire-power | 1.0mm² (E21) | VM (Vermelho) | Barramento 12V |
| DC GND | wire-gnd | 1.0mm² (E21) | PT (Preto) | GND comum |
| DC +6V | wire-signal | 0.5mm² (E22) | BN (Marrom) | Servo 6V |
| DC +5V | wire-signal | 0.5mm² (E22) | BU (Azul) | Logica 5V |
| DC +3.3V | wire-signal | 0.5mm² (E22) | Vi (Violeta) | Logica 3.3V ESP32 |

### LAYOUT DO DIAGRAMA

O diagrama deve ser organizado da **esquerda para a direita** (fluxo de energia):

```
AC ──> DISJUNTOR ──> FUSÍVEIS ──> FONTE 12V ──> BORNE X1 ──> BUCKS ──> BARRAMENTOS
(E19)   (E15)        (E16)        (E01)         (E17)        (E02/E03)
```

**Distribuicao no viewBox 900x600:**

- Coluna 1 (x=50-150): ENTRADA AC (E19, prensa-cabo PG13.5)
- Coluna 2 (x=170-270): PROTEÇÃO (E15 disjuntor 10A + E16 porta-fusíveis)
- Coluna 3 (x=290-410): FONTE (E01 Mean Well 12V 10A)
- Coluna 4 (x=430-570): BORNE X1 (E17, 6 vias de distribuição)
- Coluna 5 (x=590-750): CONVERSORES (E02 Buck→6V + E03 Buck→5V)
- Coluna 6 (x=770-870): BARRAMENTOS de saída (+6V, +5V, +3.3V, GND)

### COMPONENTES E TERMINAIS NO DIAGRAMA

Cada componente e representado como um **bloco retangular simplificado** (nao o desenho detalhado — esse ja esta na Aba 1). Dentro do bloco: tag badge (E01, E15, etc.) + nome curto + terminais de conexao.

#### BLOCO "E19 — CABO AC"
- Retangulo com badge `E19`
- Terminais: `L` (Fase), `N` (Neutro), `PE` (Terra)
- Texto: "CABO FORÇA 3×1.0mm²"

#### BLOCO "E15 — DISJUNTOR"
- Retangulo com badge `E15`
- Terminais: `IN_L`, `IN_N` (entrada) | `OUT_L`, `OUT_N` (saida)
- Texto: "DISJ. BIPOLAR 10A"

#### BLOCO "E16 — PORTA-FUSÍVEIS"
- Retangulo com badge `E16`
- Terminais: `IN` (entrada) | `OUT` (saida)
- Texto: "FUSÍVEL 10A"

#### BLOCO "E01 — FONTE"
- Retangulo com badge `E01`
- Terminais: `AC_L`, `AC_N` (entrada) | `+12V`, `GND` (saida DC)
- Texto: "FONTE 12V 10A"

#### BLOCO "E17/X1 — BORNE DE DISTRIBUIÇÃO"
- Retangulo MAIOR (e o ponto central da rede)
- Badge `X1` (referencia E17)
- **6 vias** numeradas e rotuladas:
  - `X1:1` — +12V_GERAL (entrada da fonte)
  - `X1:2` — +12V_BUCK (saida para E02 e E03)
  - `X1:3` — +12V_AT (saida do rele E08, para atuadores de potencia)
  - `X1:4` — RESERVA
  - `X1:5` — GND (entrada da fonte)
  - `X1:6` — GND_DIST (distribuição GND)

#### BLOCO "E02 — BUCK 6V"
- Retangulo com badge `E02`
- Terminais: `IN+`, `IN-` (entrada) | `OUT+`, `OUT-` (saida)
- Texto: "XL4015 → 6.0V"

#### BLOCO "E06 — CAPACITOR BUFFER"
- Retangulo pequeno com badge `E06`
- Terminais: `+`, `-`
- Texto: "1000µF/16V"
- Posicao: entre E02 OUT e barramento 6V

#### BLOCO "E03 — BUCK 5V"
- Retangulo com badge `E03`
- Terminais: `IN+`, `IN-` (entrada) | `OUT+`, `OUT-` (saida)
- Texto: "MP1584EN → 5.0V"

#### BLOCO "H01 — ESP32" (parcial, so alimentacao)
- Retangulo com badge `H01`
- Terminais mostrados: `VIN` (entrada 5V), `GND`, `3V3` (saida 3.3V interna)
- Texto: "ESP32 DEVKIT"

#### BARRAMENTO GND
- Barra horizontal na parte inferior do diagrama
- Simbolo de terra (3 linhas decrescentes) nas pontas
- Rotulo "GND COMUM" com texto "0V REF"

---

### TABELA DE FIOS (W001 a W020)

Esta tabela deve ser representada como uma **tabela SVG** na parte inferior do diagrama (acima do bloco de titulo), e cada fio deve aparecer no diagrama como uma **linha conectando os terminais**.

| FIO | DE (ORIGEM) | PARA (DESTINO) | BITOLA | COR | TIPO | TERMINAL |
|-----|-------------|----------------|--------|-----|------|----------|
| W001 | E19:L | E15:IN_L | 1.0mm² | VM | E21 | Ilhós E23 |
| W002 | E19:N | E15:IN_N | 1.0mm² | AZ | E21 | Ilhós E23 |
| W003 | E19:PE | E27:CARCAÇA | 1.0mm² | VD | E21 | Ilhós E23 |
| W004 | E15:OUT_L | E01:AC_L | 1.0mm² | VM | E21 | Ilhós E23 |
| W005 | E15:OUT_N | E01:AC_N | 1.0mm² | AZ | E21 | Ilhós E23 |
| W006 | E01:+12V | E16:IN | 1.0mm² | VM | E21 | Ilhós E23 |
| W007 | E16:OUT | X1:1 | 1.0mm² | VM | E21 | Ilhós E23 |
| W008 | E01:GND | X1:5 | 1.0mm² | PT | E21 | Ilhós E23 |
| W009 | X1:1 | X1:2 | 1.0mm² | VM | E21 | Jumper int. |
| W010 | X1:5 | X1:6 | 1.0mm² | PT | E21 | Jumper int. |
| W011 | X1:2 | E02:IN+ | 0.5mm² | BN | E22 | Ilhós E23 |
| W012 | X1:6 | E02:IN- | 0.5mm² | PT | E22 | Ilhós E23 |
| W013 | E02:OUT+ | E06:+ | 0.5mm² | BN | E22 | Soldado |
| W014 | E02:OUT- | E06:- | 0.5mm² | PT | E22 | Soldado |
| W015 | X1:2 | E03:IN+ | 0.5mm² | BU | E22 | Ilhós E23 |
| W016 | X1:6 | E03:IN- | 0.5mm² | PT | E22 | Ilhós E23 |
| W017 | E03:OUT+ | H01:VIN | 0.5mm² | BU | E22 | Header pin |
| W018 | E03:OUT- | GND COMUM | 0.5mm² | PT | E22 | Header pin |
| W019 | H01:3V3 | BARR. 3.3V | 0.5mm² | Vi | E22 | Header pin |
| W020 | H01:GND | GND COMUM | 0.5mm² | PT | E22 | Header pin |

### COMO REPRESENTAR CADA FIO NO DIAGRAMA

Cada fio e uma **polyline ou path** conectando dois terminais, com:

1. **Linha de rota**: saindo do terminal de origem, percorrendo caminhos ortogonais (horizontal/vertical, nunca diagonal — estilo CAD eletrico), ate chegar ao terminal de destino
2. **Etiqueta do fio**: retangulo pequeno `class="wire-tag"` posicionado no meio do fio, com texto `class="wire-label"` (ex: "W001")
3. **Especificacao**: texto `class="wire-spec"` abaixo da etiqueta (ex: "1.0mm² VM")
4. **Ponto de juncao**: circulo `class="junction-dot"` r=2.5 nos terminais de inicio e fim

**REGRA DE ROTEAMENTO DOS FIOS:**
- Fios NUNCA se cruzam no mesmo nivel (reroute se necessario)
- Fios paralelos mantêm 6px de distancia entre si
- Fios AC (W001-W005) passam pela **parte superior** do diagrama
- Fios DC +12V (W006-W010) passam pelo **terco medio**
- Fios DC baixa tensao (W011-W020) passam pela **parte inferior**
- Fios GND sempre na parte mais baixa, tracejados

### LEGENDA DE CONVENÇÕES

No canto superior direito (dentro da moldura), inserir uma legenda compacta:

```
LEGENDA DE FIOS:
──────── (solido grosso)   = Potencia (1.0mm²)
─ ─ ─ ─ (tracejado)       = GND
──────── (solido fino)     = Sinal (0.5mm²)
●                          = Juncao / conexao
[W001]                     = Numero do fio
```

### NOTAS TECNICAS

Abaixo do diagrama (dentro da moldura, acima do bloco de titulo), inserir:

- "TENSÃO DE ENTRADA: 127/220V AC (50/60Hz) — verificar tensão local antes da instalação"
- "CORRENTE MÁXIMA DO BARRAMENTO 12V: 10A (limitada pela fonte E01)"
- "TODOS OS FIOS DE POTÊNCIA (E21): terminados com ilhós tubulares (E23) nos bornes"
- "FIOS DE SINAL (E22): podem usar header pins na protoboard (E26)"
- "REGRA DE OURO: correntes de potência FORA da protoboard, só GND comum compartilhado"

---

## SECTION WRAPPER

```html
<section id="wiring-1" class="sheet-section">
  <h2>BLOCO W1 — REDE DE ALIMENTAÇÃO (Folha 1/5)</h2>
  <div class="canvas-wrap">
    <svg viewBox="0 0 900 600" width="900" height="600" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <!-- patterns grid-w1, grid-major-w1, hatch-w1 aqui -->
        <!-- marker seta para direcao do fluxo -->
        <marker id="arrow-w1" viewBox="0 0 10 6" refX="10" refY="3"
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

## CHECKLIST FINAL

### Infraestrutura de Abas
- [ ] CSS das abas inserido DENTRO do `<style>` existente (nao substituir nada)
- [ ] Barra de abas (`<div class="tab-bar">`) entre `</header>` e nav
- [ ] Conteudo existente (nav + 9 sections) envolvido em `<div id="tab-componentes" class="tab-content active">`
- [ ] Nova div `<div id="tab-interligacoes" class="tab-content">` depois do tab-componentes
- [ ] Nav pills da Aba 2 com 5 folhas (W1 a W5)
- [ ] Header `<p>` atualizado para mencionar ambas as abas
- [ ] JavaScript `switchTab()` adicionado ao script existente
- [ ] Abas funcionam: clicar "COMPONENTES" mostra Aba 1, clicar "INTERLIGAÇÕES" mostra Aba 2
- [ ] NAO alterou NENHUM conteudo dos Blocos 1-9
- [ ] NAO alterou o CSS existente (só ACRESCENTOU)
- [ ] NAO alterou as funcoes toggleTheme()/initTheme()

### Bloco W1
- [ ] Section id="wiring-1" com class="sheet-section"
- [ ] Titulo h2: `BLOCO W1 — REDE DE ALIMENTAÇÃO (Folha 1/5)`
- [ ] Pattern IDs unicos (grid-w1, grid-major-w1, hatch-w1)
- [ ] Grid duplo + moldura dupla (mesmas dimensoes dos blocos anteriores)
- [ ] Marker de seta `arrow-w1` definido no defs
- [ ] Componentes representados como blocos simplificados (E19, E15, E16, E01, X1, E02, E03, E06, H01)
- [ ] Cada componente com tag badge e terminais rotulados
- [ ] 20 fios (W001 a W020) desenhados como linhas entre terminais
- [ ] Cada fio com etiqueta `[Wnnn]` e especificacao "bitola COR"
- [ ] Fios ortogonais (nunca diagonais), sem cruzamentos
- [ ] Fios AC na parte superior, DC potencia no meio, DC sinal na inferior
- [ ] Fios GND tracejados (`stroke-dasharray: 8 3`)
- [ ] Juncoes (circulos preenchidos) nos pontos de conexao
- [ ] Barramento GND na base com simbolo de terra
- [ ] Legenda de convenções no canto superior direito
- [ ] Tabela de fios (W001-W020) na parte inferior
- [ ] Notas tecnicas (5 notas)
- [ ] Bloco de titulo (Folha 1/5, REV A, NOV 2026)
- [ ] SOMENTE variaveis CSS — zero cores literais no SVG
- [ ] Borne X1 com 6 vias numeradas e rotuladas
- [ ] Fluxo da esquerda para a direita (AC → DC → Barramentos)
- [ ] Setas de direcao de corrente nos fios de potencia (usar marker arrow-w1)

### Integridade
- [ ] Tema claro/escuro funciona em ambas as abas
- [ ] Scroll entre abas nao quebra a navegacao
- [ ] Pills da Aba 1 continuam funcionando normalmente
- [ ] Pills da Aba 2 levam as sections corretas
- [ ] NAO alterou CSS existente, apenas ACRESCENTOU
- [ ] NAO alterou script existente, apenas ACRESCENTOU switchTab()
- [ ] Todas as 14 variaveis CSS usadas: --bg, --fg, --line, --line-thin, --pin-text, --grid, --grid-major, --dim, --trace, --pad-fill, --tag-bg, --header-bg, --header-border + color-scheme

---

## RESUMO DA ORGANIZAÇÃO DAS 5 FOLHAS (para referência futura)

| FOLHA | ID | BLOCO | CONTEÚDO | FIOS |
|-------|----|-------|----------|------|
| 1/5 | wiring-1 | W1 | Rede de Alimentação (AC→DC→Barramentos) | W001-W020 |
| 2/5 | wiring-2 | W2 | Rede de Sensores e E-STOP | W021-W040 |
| 3/5 | wiring-3 | W3 | Rede de Atuadores (Servos + Motor) | W041-W056 |
| 4/5 | wiring-4 | W4 | Sinalização, Dados e Proteção | W057-W069 |
| 5/5 | wiring-5 | W5 | Tabela Completa de Fios + Diagrama Unifilar | Todas W001-W069 |
