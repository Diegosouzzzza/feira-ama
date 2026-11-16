# PROMPT — BLOCO 04 + CORREÇÕES DO BLOCO 01

## CONTEXTO

Voce esta editando o arquivo unico:
`file:///C:/Users/ponto/OneDrive/Desktop/FEIRA%20-%20AMA/desenho-eletrico/esp32.html`

Os Blocos 1, 2 e 3 ja existem e foram **aprovados pela auditoria**. Voce deve:

1. **CORRIGIR 2 ressalvas no Bloco 1** (detalhadas abaixo)
2. **INSERIR o Bloco 4** como nova `<section>` logo apos o `</section>` do Bloco 3 (antes do comentario `<!-- BLOCOS 4 A 9 -->`)
3. **Adicionar o pill** `Bloco 4` no `<nav>` existente

**IMPORTANTE — NAO altere NADA do CSS, do `<script>`, do header nem dos Blocos 2 e 3**, exceto o pill no nav.

---

## PARTE 1: CORREÇÕES DO BLOCO 1

### Ressalva 1 — ViewBox inconsistente

O Bloco 1 atualmente usa `viewBox="0 0 800 780"` width="800" height="780".
Os Blocos 2 e 3 usam `viewBox="0 0 900 600"` width="900" height="600".

**Corrigir**: altere o SVG do Bloco 1 para `viewBox="0 0 900 780"` width="900" height="780".
Ajuste a moldura dupla do Bloco 1 para acompanhar a nova largura (860px de largura interna, igual aos outros blocos):
- Rect externo: x=20, y=20, width=860, height (manter o que ja tem, so ajustar width)
- Rect interno: x=25, y=25, width=850, height (manter, so ajustar width)

Reposicione os elementos que ficarem desalinhados com a nova largura (bloco de titulo, tabela BOM, legenda — empurrar para a direita se necessario para caber nos 900px).

### Ressalva 2 — Tag BOM "H01" ausente

Os Blocos 2 e 3 tem badges proeminentes no topo de cada componente (retangulo com "E01", "E15", etc).
O Bloco 1 nao tem essa badge.

**Corrigir**: adicionar no topo do Bloco 1, acima do corpo do ESP32, uma badge identica ao estilo dos outros blocos:

```xml
<!-- TAG H01 EM DESTAQUE -->
<rect x="95" y="42" width="55" height="20" rx="2" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.4"/>
<text x="122" y="56" text-anchor="middle" font-size="11" font-weight="bold" fill="var(--fg)">H01</text>
<text x="158" y="52" font-size="8" font-weight="bold" fill="var(--dim)">ESP32-DEVKIT V1</text>
<text x="158" y="60" font-size="6.5" fill="var(--dim)">MICROCONTROLADOR PRINCIPAL</text>
```

Ajuste as coordenadas Y dos elementos existentes do Bloco 1 se necessario para nao sobrepor a nova badge.

---

## PARTE 2: BLOCO 04 — SENSORES E ENTRADA (Folha 4/9)

### REGRAS DE ESTILO CAD (manter 100% igual aos Blocos 2 e 3)

1. **ViewBox**: `0 0 900 600`, width="900" height="600"
2. **Patterns (defs)**: criar IDs unicos: `grid-b4`, `grid-major-b4`, `hatch-b4` — copiar estrutura dos blocos anteriores
3. **Grid duplo**: fundo com `grid-b4` (10px) + `grid-major-b4` (50px)
4. **Moldura dupla**: rect externo (20,20,860,560 stroke 1.5) + interno (25,25,850,550 stroke 0.5)
5. **Cores**: usar SOMENTE variaveis CSS ja definidas: `var(--bg)`, `var(--fg)`, `var(--line)`, `var(--line-thin)`, `var(--pin-text)`, `var(--grid)`, `var(--grid-major)`, `var(--dim)`, `var(--trace)`, `var(--pad-fill)`, `var(--tag-bg)`. NUNCA cores literais.
6. **Pads through-hole**: dois circulos concentricos (externo r=5, stroke 1; interno r=2, preenchido `var(--bg)`)
7. **Tag badge**: retangulo com rx=2, fill=`var(--pad-fill)`, stroke 1.4 — texto bold do codigo BOM
8. **Cotas dimensionais**: linhas de extensao, setas (poligonos triangulares), texto em mm
9. **Bloco de titulo** (canto inferior direito): PROJETO: FEIRA AMA / BLOCO: 04 — SENSORES E ENTRADA / ESCALA: N/A / FOLHA: 4/9 / DATA: NOV 2026 / REV: A
10. **Tabela de especificacoes** (parte inferior esquerda): mesma estrutura dos blocos anteriores

---

### COMPONENTE 1: H04/E07 — SENSOR IR REFLEXIVO (x2 unidades: S1 e S2)

- **Tag badge**: `H04/E07`
- **Descricao no badge**: `SENSOR IR REFLEXIVO (Par S1/S2)`
- **Subtitulo**: `DETECCAO DE CASTANHA NA ESTEIRA`
- **Tipo**: Modulo sensor infravermelho reflexivo. **Forma: RETANGULAR** (NAO e cilindrico M18 — e um sensor retangular vermelho)
- **Dimensoes fisicas**: ~50mm x 30mm x 18mm (corpo retangular)
- **Desenhar**:
  - Corpo retangular com bordas arredondadas rx=3
  - **LED emissor IR** interno: desenhar como LED com seta para fora (emissao)
  - **Fototransistor receptor** interno: desenhar com seta para dentro (recepcao)
  - **Trimpot de sensibilidade** (potenciometro): circulo com seta de ajuste
  - **LED indicador** de deteccao: pequeno circulo na PCB
  - **Lente optica frontal**: retangulo com stroke-dasharray (transparente)
  - 2 furos de montagem nos cantos
- **Terminais** (3 fios cada, through-hole pads):
  - `VCC` — Alimentacao (+5V do Buck E03)
  - `GND` — Terra comum
  - `OUT` — Saida digital (NPN, ativo LOW)
- **IMPORTANTE**: Desenhar **dois sensores lado a lado** dentro da mesma folha, com texto indicando:
  - Sensor esquerdo: `S1 -> GPIO25`
  - Sensor direito: `S2 -> GPIO26`
  - Texto entre eles: "Opto-acoplamento via PC817 — saida puxa LOW quando ativo"
  - Texto: "Conforme board_config.h: AV_INPUTS_ACTIVE_LOW = 1"
- **Cotas**: dimensao do corpo em mm

---

### COMPONENTE 2: E12 — BOTAO DE EMERGENCIA E-STOP (Cogumelo NR-12)

- **Tag badge**: `E12`
- **Descricao no badge**: `BOTAO E-STOP COGUMELO`
- **Subtitulo**: `EMERGENCIA NR-12 — DUPLA FUNCAO`
- **Dimensoes fisicas**: cabeca diam 40mm (cogumelo), base diam 22mm (furo painel)
- **Desenhar**:
  - **Vista superior** do cogumelo: circulo grande (diam 40) com hachura cruzada para indicar vermelho (usar pattern hatch-b4)
  - **Base cilindrica**: circulo menor (diam 22) concentrico
  - **Mecanismo de trava**: indicar "push-lock / twist-release" com setas curvas ao redor
  - **Contatos internos** (desenhar como simbolos eletricos):
    - **NF1 (potencia)**: simbolo de contato normalmente fechado — este corta fisicamente o +12V dos atuadores no hardware
    - **NF2 (sinal)**: simbolo de contato normalmente fechado — este vai ao ESP32 para monitoramento
  - **Triangulo de alerta** com texto "NR-12" dentro ou ao lado
- **Terminais** (4 pads through-hole):
  - `NF1-COM` — Comum do contato de potencia (+12V entrada)
  - `NF1-NC` — Normal fechado do contato de potencia (saida para atuadores — abre ao pressionar)
  - `NF2-COM` — Comum do contato auxiliar (3.3V via pull-up interno ESP32)
  - `NF2-NC` — Normal fechado do contato auxiliar -> `GPIO27`
- **Notas abaixo do desenho**:
  - "NF1: Corte fisico do barramento +12V_AT (seguranca NR-12)"
  - "NF2: Monitoramento via ESP32 GPIO27 — Active LOW com pull-up interno"
  - "Dupla funcao: hardware + software"
- **Cotas**: diam 40mm cabeca, diam 22mm base

---

### COMPONENTE 3: E14 — WEBCAM USB (Classificacao por Visao Computacional)

- **Tag badge**: `E14`
- **Descricao no badge**: `WEBCAM USB`
- **Subtitulo**: `CAPTURA DE IMAGEM PARA CLASSIFICACAO A.I.`
- **Tipo**: Webcam USB generica (640x480 minimo, sem marca especifica)
- **Dimensoes fisicas**: ~70mm x 30mm x 25mm (corpo retangular com lente)
- **Desenhar**:
  - **Corpo retangular** com bordas arredondadas
  - **Lente circular** frontal: circulo com aneis concentricos (lente + sensor CMOS interno)
  - **LED indicador** de atividade (ponto ao lado da lente)
  - **Cabo USB saindo** do corpo: linha ondulada ou curvada
  - **Conector USB-A** na ponta do cabo: retangulo com detalhe interno (4 contatos)
  - **Suporte/clip de fixacao**: forma de C ou L na base
  - **FOV (Campo de visao)**: 2 linhas tracejadas divergentes saindo da lente, com angulo indicado (~60 graus)
  - **Texto interno no corpo**: "CMOS", "640x480", "30fps"
- **Terminais** (conector USB desenhado como 4 pads through-hole):
  - `USB_5V` — Alimentacao via USB do notebook (vermelho)
  - `USB_D-` — Dados USB (branco)
  - `USB_D+` — Dados USB (verde)
  - `USB_GND` — Terra USB (preto)
  - OBS: como o desenho e monocromatico, indicar as cores entre parenteses como texto ao lado de cada terminal
- **Nota abaixo em destaque**: "Conecta ao NOTEBOOK via USB — NAO ao ESP32. Processamento de imagem por ONNX Runtime (AmazonVision 4.0)"
- **Cotas**: dimensoes do corpo em mm

---

### TABELA DE ESPECIFICACOES (parte inferior, mesma estrutura dos blocos anteriores)

| TAG | COMPONENTE | ESPECIFICACAO | FUNCAO NO PROJETO |
|-----|-----------|---------------|-------------------|
| H04/E07 | Sensor IR Reflexivo (x2) | NPN Ativo LOW, 5V, Retangular | Deteccao S1 (GPIO25) + S2 (GPIO26) |
| E12 | Botao E-STOP Cogumelo | diam 40mm, 2xNF, Push-Lock | NR-12: Corte +12V_AT + Sinal GPIO27 |
| E14 | Webcam USB | 640x480, USB-A, 30fps | Classificacao A.I. via Notebook (ONNX) |

---

### NAV PILL

Adicionar ao `<nav>` existente, depois do pill do Bloco 3:

```html
<a href="#bloco-4" class="nav-pill">04 Sensores</a>
```

---

### SECTION WRAPPER

```html
<section id="bloco-4" class="sheet-section">
  <h2>BLOCO 04 — SENSORES E ENTRADA (Folha 4/9)</h2>
  <div class="canvas-wrap">
    <svg viewBox="0 0 900 600" width="900" height="600" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <!-- patterns grid-b4 e grid-major-b4 aqui -->
      </defs>
      <!-- todo o conteudo SVG aqui -->
    </svg>
  </div>
</section>
```

---

### CHECKLIST FINAL (verificar antes de entregar)

- [ ] Section id="bloco-4" com class="sheet-section"
- [ ] Titulo h2: `BLOCO 04 — SENSORES E ENTRADA (Folha 4/9)`
- [ ] Pattern IDs unicos (grid-b4, grid-major-b4, hatch-b4)
- [ ] Grid duplo + moldura dupla
- [ ] 3 componentes (H04/E07, E12, E14) com badges de tag proeminentes
- [ ] Cotas dimensionais em mm em todos os componentes
- [ ] Todos os terminais com pads through-hole (dois circulos concentricos)
- [ ] Tabela de especificacoes na parte inferior
- [ ] Bloco de titulo (Folha 4/9) no canto inferior direito
- [ ] SOMENTE variaveis CSS — zero cores literais
- [ ] Pill "04 Sensores" adicionado ao nav existente
- [ ] Tema claro/escuro JA FUNCIONA (nao precisa adicionar nada, apenas usar as variaveis)
- [ ] NAO alterou nada nos Blocos 2 ou 3
- [ ] NAO alterou o CSS nem o script
- [ ] Bloco 1: viewBox corrigido para 900px de largura
- [ ] Bloco 1: badge H01 adicionada no topo
- [ ] Bloco 1: moldura dupla ajustada para width 860/850
