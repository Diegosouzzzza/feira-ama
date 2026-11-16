# PROMPT — BLOCO 09: INFRAESTRUTURA (Folha 9/9)

## CONTEXTO

Voce esta editando o arquivo unico:
`file:///C:/Users/ponto/OneDrive/Desktop/FEIRA%20-%20AMA/desenho-eletrico/esp32.html`

Os Blocos 1, 2, 3, 4, 5, 6, 7 e 8 ja existem e foram **aprovados**. Voce deve:

1. **INSERIR o Bloco 9** como nova `<section>` logo apos o `</section>` do Bloco 8 (antes do comentario `<!-- BLOCOS 5 A 9 -->`)
2. **Adicionar o pill** no `<nav>` existente, depois do pill do Bloco 8, no formato padrao:
   ```html
   <a href="#bloco-9" class="nav-pill">FOLHA 9/9: INFRAESTRUTURA (E17, E18, E27)</a>
   ```
3. **REMOVER o span placeholder** `<span class="nav-pill" style="opacity: 0.5;">FOLHA 9: (EM DESENVOLVIMENTO)</span>` — esta e a ultima folha, nao ha mais placeholders.

**NAO altere NADA do CSS, do `<script>`, do header nem dos Blocos 1/2/3/4/5/6/7/8 existentes**, exceto o nav.

---

## REGRAS DE ESTILO CAD (manter 100% igual aos Blocos anteriores)

1. **ViewBox**: `0 0 900 600`, width="900" height="600"
2. **Patterns (defs)**: IDs unicos: `grid-b9`, `grid-major-b9`, `hatch-b9`
3. **Grid duplo**: fundo com `grid-b9` (10px) + `grid-major-b9` (50px)
4. **Moldura dupla**: rect externo (20,20,860,560 stroke 1.5) + interno (25,25,850,550 stroke 0.5)
5. **Cores**: SOMENTE variaveis CSS: `var(--bg)`, `var(--fg)`, `var(--line)`, `var(--line-thin)`, `var(--pin-text)`, `var(--grid)`, `var(--grid-major)`, `var(--dim)`, `var(--trace)`, `var(--pad-fill)`, `var(--tag-bg)`. NUNCA cores literais.
6. **Pads through-hole**: dois circulos concentricos (externo r=5, stroke 1; interno r=2, preenchido `var(--bg)`)
7. **Tag badge**: retangulo rx=2, fill=`var(--pad-fill)`, stroke 1.4, texto bold do codigo BOM
8. **Cotas dimensionais**: linhas de extensao, setas (poligonos triangulares), texto em mm
9. **Bloco de titulo**: PROJETO: FEIRA AMA / BLOCO: 09 — INFRAESTRUTURA / ESCALA: N/A / FOLHA: 9/9 / DATA: NOV 2026 / REV: A
10. **Tabela de especificacoes**: mesma estrutura dos blocos anteriores

---

## COMPONENTE 1: E17 — RÉGUA DE BORNES SAK/SINDAL DIN (12 VIAS)

- **Tag badge**: `E17`
- **Descricao no badge**: `RÉGUA BORNES SAK 12 VIAS`
- **Subtitulo**: `DISTRIBUIÇÃO DE FORÇA, SINAIS E ATUADORES — 3 RÉGUAS (X1, X2, X3)`
- **Status**: Comprar (3 unidades, R$ 18,00/un)
- **Tipo**: Regua de bornes de passagem, encaixe snap-in em trilho DIN TS-35
- **Dimensoes fisicas**: ~12 vias × ~8mm pitch por via = ~96mm largura total; altura ~45mm; profundidade ~35mm (padrao SAK)
- **Desenhar**:
  - **Vista frontal** de UMA regua de bornes genérica (12 vias):
    - **Corpo retangular** em plastico com divisorias entre cada via
    - **12 bornes de parafuso** na face frontal: representar como 12 retangulos pequenos com furo central (parafuso) alinhados
    - **Encaixe DIN** na base (clip/mola para trilho TS-35): indicar com perfil em T invertido
    - **Numeracao das vias**: 1 a 12, cada via rotulada
    - **Terminais ilhos** (E23) crimpados nas pontas dos cabos inseridos nos bornes
  - **3 reguas lado a lado** com designacoes diferentes (representar como 3 blocos menores com rotulos):
    - **X1 — FORCA 12V**: distribuicao de +12V e GND da Fonte E01 para todos os circuitos de potencia
      - Vias sugeridas: +12V (vias 1-3), GND (vias 4-6), reserva (vias 7-12)
      - Conecta: Fonte E01 → Disjuntor E15 → X1 → Buck E02/E03, MOSFET E04, Ring Light E13, Rele E08
    - **X2 — SENSORES / S0**: sinais dos sensores e emergencia
      - Vias sugeridas: S1 sinal (via 1), S1 GND (via 2), S2 sinal (via 3), S2 GND (via 4), E-STOP NA (via 5), E-STOP NF (via 6), E-STOP COM (via 7), reserva (vias 8-12)
      - Conecta: Sensores IR H04/E07 → X2 → Clamp E10/E11 → ESP32 GPIO25/26; Botao E-STOP E12 → X2 → GPIO27
    - **X3 — ATUADORES**: sinais de comando e potencia dos atuadores
      - Vias sugeridas: Servo1 sinal (via 1), Servo1 +6V (via 2), Servo1 GND (via 3), Servo2 (vias 4-6), Motor+ (via 7), Motor- (via 8), Motor EN (via 9), reserva (vias 10-12)
      - Conecta: ESP32 GPIO18/19 → X3 → Servos H02/H03, Motor M13 via MOSFET E04
  - **Especificacoes**:
    - Tipo: SAK / Sindal (borne de passagem, encaixe DIN)
    - Vias: 12 por regua
    - Secao maxima do condutor: 2.5 mm² (adequado para 12V/10A)
    - Tensao de isolamento: 500V AC
    - Corrente nominal por via: ~20A (SAK padrao)
    - Material: Poliamida PA66 (retardante de chama UL94-V0)
    - Fixacao: snap-in em trilho DIN TS-35 (E18)
- **Terminais** (6 pads through-hole representando os 3 blocos principais):
  - `X1+` — Entrada +12V no borne X1 (vindo do disjuntor E15)
  - `X1-` — Entrada GND no borne X1
  - `X2_S` — Entrada de sinais dos sensores no borne X2
  - `X2_ES` — Entrada do E-STOP no borne X2
  - `X3_SV` — Saida dos servos pelo borne X3
  - `X3_MT` — Saida do motor pelo borne X3
- **Notas abaixo**:
  - "3 reguas fisicas separadas: X1 (forca), X2 (sensores/emergencia), X3 (atuadores)"
  - "Todas montadas sobre o trilho DIN (E18) dentro do Quadro de Comando (E27)"
  - "Terminais ilhos (E23) crimpados em todas as pontas de cabo antes de inserir nos bornes"
  - "Identificacao obrigatoria: etiquetas adesivas em cada via com funcao e destino"
  - "Secao do cabo: 1.0 mm² potencia (E21), 0.5 mm² sinal (E22)"
- **Cotas**: ~96mm largura (12 vias × 8mm), ~45mm altura, ~35mm profundidade

---

## COMPONENTE 2: E18 — TRILHO DIN TS-35 (1 m) + 4 BATENTES FINAIS

- **Tag badge**: `E18`
- **Descricao no badge**: `TRILHO DIN TS-35 (1 m)`
- **Subtitulo**: `BASE DE FIXAÇÃO DO PAINEL ELÉTRICO — SUPORTE UNIVERSAL DIN`
- **Status**: Comprar (1 unidade + 4 batentes, R$ 25,00)
- **Tipo**: Trilho metalico padrao DIN EN 60715 (TS-35), perfil omega (chapeu), aluminio ou aco galvanizado
- **Dimensoes fisicas**: 35mm largura × 7.5mm profundidade × 1000mm comprimento; espessura chapa ~1mm
- **Desenhar**:
  - **Vista frontal** (perfil transversal / corte do trilho):
    - **Perfil omega (chapeu)**: forma de U invertido com abas laterais dobradas para dentro
    - Largura total: 35mm
    - Altura central: 7.5mm
    - Abas laterais: ~5mm cada
    - Cotar todas as dimensoes do perfil
  - **Vista superior** (planta) do trilho no painel:
    - **Barra horizontal** de 1000mm de comprimento
    - **4 batentes finais** (end stops) nas extremidades: 2 em cada ponta, representar como blocos trapezoidais que travam os componentes
    - **Componentes snap-in** montados ao longo do trilho (representar como retangulos posicionados no trilho):
      - Disjuntor (E15, Bloco 3)
      - Porta-fusiveis (E16, Bloco 3)
      - Regua X1 (E17)
      - Regua X2 (E17)
      - Regua X3 (E17)
      - Espacos livres para expansao
    - **Furos de fixacao** do trilho na placa de fundo do quadro: indicar com circulos ao longo do trilho (~3-4 furos)
  - **Detalhe de encaixe snap-in** (ampliado):
    - Mostrar como a mola/clip do componente (ex: borne SAK) encaixa na aba do trilho
    - Texto: "Encaixe sem ferramentas — snap-in / snap-out rapido"
  - **Especificacoes**:
    - Norma: DIN EN 60715
    - Designacao: TS-35 (Top-hat Section, 35mm)
    - Comprimento: 1000 mm (cortar conforme necessidade)
    - Largura: 35.0 mm
    - Altura (profundidade): 7.5 mm
    - Material: Aco galvanizado ou aluminio
    - Espessura: ~1.0 mm
    - Furos de fixacao: oblongos, para parafusos M4
- **Terminais** (4 pads through-hole representando os furos de fixacao):
  - `FIX_1` — Parafuso de fixacao esquerdo
  - `FIX_2` — Parafuso de fixacao centro-esquerdo
  - `FIX_3` — Parafuso de fixacao centro-direito
  - `FIX_4` — Parafuso de fixacao direito
- **Notas abaixo**:
  - "Fixado horizontalmente na placa de fundo do Quadro de Comando (E27)"
  - "Componentes DIN montados: Disjuntor E15, Porta-fusiveis E16, 3× Bornes E17 (X1/X2/X3)"
  - "Batentes finais nas extremidades impedem deslizamento lateral dos componentes"
  - "Cortar no comprimento necessario (~300mm para caber no Quadro E27 de 300mm de largura)"
  - "Norma DIN EN 60715 — compativel com todos os componentes industriais padrao"
- **Cotas**: 35mm largura, 7.5mm profundidade, 1000mm comprimento (cortar ~300mm)

---

## COMPONENTE 3: E27 — CAIXA PLÁSTICA DIN / PAINEL 200×300×150 mm

- **Tag badge**: `E27`
- **Descricao no badge**: `QUADRO DE COMANDO 200×300×150mm`
- **Subtitulo**: `ARMÁRIO ELÉTRICO DO SISTEMA — ABRIGA TODOS OS COMPONENTES`
- **Status**: Comprar (1 unidade, R$ 120,00)
- **Tipo**: Caixa plastica para painel eletrico, com placa de montagem interna e tampa transparente
- **Dimensoes fisicas**: 200mm (altura) × 300mm (largura) × 150mm (profundidade)
- **Desenhar**:
  - **Vista frontal** (tampa transparente — mostrando o interior):
    - **Retangulo principal** representando a face frontal da caixa
    - **Tampa transparente** indicada com borda tracejada (transparencia)
    - **Interior visivel** com layout esquematico dos componentes instalados:
      - Trilho DIN (E18) horizontal, com componentes snap-in
      - Protoboard (E26) fixada abaixo do trilho, com ESP32 visivel
      - Buzzer (E25) e LEDs (H05) no painel frontal
      - Botao E-STOP (E12) no painel frontal (acessivel sem abrir)
    - **Prensa-cabos** (E24) nos cantos inferiores: PG7 e PG9 para entrada de cabos
    - **Dobradiças** da tampa no lado esquerdo
    - **Fecho/trinco** no lado direito
  - **Vista lateral** (corte, menor, ao lado):
    - Placa de fundo com trilho DIN fixado
    - Profundidade de 150mm
    - Tampa transparente articulada
  - **Diagrama de distribuicao interna** (layout de instalacao dentro do quadro):
    - **Zona superior**: Trilho DIN com Disjuntor E15, Porta-fusiveis E16, Bornes X1/X2/X3
    - **Zona central**: Protoboard E26 com ESP32 (H01) + clamps + LEDs
    - **Zona inferior**: Espaco para cabos e amarracoes
    - **Painel frontal**: Botao E-STOP (E12), LEDs indicadores (H05), Buzzer (E25)
    - **Entrada de cabos**: Prensa-cabos PG7/PG9 (E24) na base
  - **Especificacoes**:
    - Dimensoes externas: 200 × 300 × 150 mm (A × L × P)
    - Material: ABS ou policarbonato
    - Grau de protecao: IP65 (com tampa fechada)
    - Tampa: Transparente (policarbonato) para inspecao visual
    - Placa de montagem: Metalica galvanizada (removivel)
    - Cor da base: Cinza RAL 7035 (padrao industrial)
    - Dobradiças: integradas na tampa
    - Fecho: trinco com chave ou quarter-turn
    - Entradas de cabo: 4× prensa-cabos (PG7 para sinal, PG9 para potencia)
- **Terminais** (4 pads through-hole representando as entradas de cabos):
  - `PG9_AC` — Prensa-cabo de entrada AC (cabo de forca E19)
  - `PG9_12V` — Prensa-cabo de saida 12V para atuadores externos (servos, motor)
  - `PG7_SENS` — Prensa-cabo de entrada dos sensores (S1, S2, E-STOP)
  - `PG7_USB` — Prensa-cabo de passagem do cabo USB (E20) para o notebook
- **Notas abaixo**:
  - "Abriga TODOS os componentes eletronicos e eletricos do sistema AmazonVision 4.0"
  - "Tampa transparente permite inspecao visual sem abrir o quadro"
  - "Botao E-STOP (E12) e LEDs (H05) montados NA TAMPA — acessiveis sem abrir"
  - "IP65 com tampa fechada — protege contra poeira e respingos na feira"
  - "Componentes internos: E15, E16, E17(×3), E18, E26+H01, E25, cabos E19-E24"
  - "Fixado na lateral da estrutura da esteira com suportes em L ou parafusos"
- **Cotas**: 200 × 300 × 150 mm (A × L × P), prensa-cabos PG7 (Ø12.5mm) e PG9 (Ø15.5mm)

---

## TABELA DE ESPECIFICACOES

| TAG | COMPONENTE | ESPECIFICACAO | FUNCAO NO PROJETO |
|-----|-----------|---------------|-------------------|
| E17 | Regua Bornes SAK 12 vias (×3) | SAK/Sindal DIN, 12 vias, 20A/via | Distribuicao X1 (forca), X2 (sensor), X3 (atu.) |
| E18 | Trilho DIN TS-35 1m + batentes | 35×7.5mm, aco galv., DIN EN 60715 | Base de fixacao do painel eletrico |
| E27 | Quadro de Comando 200×300×150 | ABS/PC, IP65, tampa transparente | Armario que abriga todos os componentes |

---

## SECTION WRAPPER

```html
<section id="bloco-9" class="sheet-section">
  <h2>BLOCO 09 — INFRAESTRUTURA (Folha 9/9)</h2>
  <div class="canvas-wrap">
    <svg viewBox="0 0 900 600" width="900" height="600" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <!-- patterns grid-b9, grid-major-b9, hatch-b9 aqui -->
      </defs>
      <!-- todo o conteudo SVG aqui -->
    </svg>
  </div>
</section>
```

---

## CHECKLIST FINAL

- [ ] Section id="bloco-9" com class="sheet-section"
- [ ] Titulo h2: `BLOCO 09 — INFRAESTRUTURA (Folha 9/9)`
- [ ] Pattern IDs unicos (grid-b9, grid-major-b9, hatch-b9)
- [ ] Grid duplo + moldura dupla
- [ ] 3 componentes (E17, E18, E27) com badges de tag proeminentes
- [ ] Cotas dimensionais em mm em todos os componentes
- [ ] Todos os terminais com pads through-hole (dois circulos concentricos)
- [ ] Tabela de especificacoes na parte inferior
- [ ] Bloco de titulo (Folha 9/9) no canto inferior direito
- [ ] SOMENTE variaveis CSS — zero cores literais
- [ ] Pill adicionado ao nav no formato longo padrao
- [ ] Span placeholder REMOVIDO (esta e a ultima folha — nao ha mais placeholders)
- [ ] Tema claro/escuro: apenas usar variaveis, nao alterar CSS/script
- [ ] NAO alterou nada nos Blocos 1/2/3/4/5/6/7/8
- [ ] NAO alterou o CSS nem o script
- [ ] E17: 3 reguas diferenciadas (X1 forca, X2 sensores/S0, X3 atuadores)
- [ ] E17: vias sugeridas para cada regua com funcao de cada via
- [ ] E17: referencia a terminais ilhos E23 e secao de cabos E21/E22
- [ ] E18: perfil omega (chapeu) do trilho TS-35 cotado
- [ ] E18: componentes DIN montados: E15, E16, E17(×3)
- [ ] E18: batentes finais nas extremidades
- [ ] E18: nota de corte (~300mm para caber no E27)
- [ ] E27: layout interno mostrando distribuicao de todos os componentes
- [ ] E27: tampa transparente indicada
- [ ] E27: prensa-cabos E24 (PG7/PG9) nas entradas
- [ ] E27: botao E-STOP (E12) e LEDs (H05) no painel frontal acessivel
- [ ] E27: referencia a IP65 e protecao
- [ ] ESTA E A FOLHA FINAL (9/9) — todos os 9 blocos completos
