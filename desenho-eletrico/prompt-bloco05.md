# PROMPT — BLOCO 05: ATUADORES (Folha 5/9)

## CONTEXTO

Voce esta editando o arquivo unico:
`file:///C:/Users/ponto/OneDrive/Desktop/FEIRA%20-%20AMA/desenho-eletrico/esp32.html`

Os Blocos 1, 2, 3 e 4 ja existem e foram **aprovados**. Voce deve:

1. **INSERIR o Bloco 5** como nova `<section>` logo apos o `</section>` do Bloco 4 (antes do comentario `<!-- BLOCOS 5 A 9 -->`)
2. **Adicionar o pill** no `<nav>` existente, depois do pill do Bloco 4, no formato padrao:
   ```html
   <a href="#bloco-5" class="nav-pill">FOLHA 5/9: ATUADORES (H02, H03, M13)</a>
   ```
3. **Atualizar o span placeholder** de "FOLHAS 5-9" para "FOLHAS 6-9"

**NAO altere NADA do CSS, do `<script>`, do header nem dos Blocos 1/2/3/4 existentes**, exceto o nav.

---

## REGRAS DE ESTILO CAD (manter 100% igual aos Blocos 2, 3 e 4)

1. **ViewBox**: `0 0 900 600`, width="900" height="600"
2. **Patterns (defs)**: IDs unicos: `grid-b5`, `grid-major-b5`, `hatch-b5`
3. **Grid duplo**: fundo com `grid-b5` (10px) + `grid-major-b5` (50px)
4. **Moldura dupla**: rect externo (20,20,860,560 stroke 1.5) + interno (25,25,850,550 stroke 0.5)
5. **Cores**: SOMENTE variaveis CSS: `var(--bg)`, `var(--fg)`, `var(--line)`, `var(--line-thin)`, `var(--pin-text)`, `var(--grid)`, `var(--grid-major)`, `var(--dim)`, `var(--trace)`, `var(--pad-fill)`, `var(--tag-bg)`. NUNCA cores literais.
6. **Pads through-hole**: dois circulos concentricos (externo r=5, stroke 1; interno r=2, preenchido `var(--bg)`)
7. **Tag badge**: retangulo rx=2, fill=`var(--pad-fill)`, stroke 1.4, texto bold do codigo BOM
8. **Cotas dimensionais**: linhas de extensao, setas (poligonos triangulares), texto em mm
9. **Bloco de titulo**: PROJETO: FEIRA AMA / BLOCO: 05 — ATUADORES / ESCALA: N/A / FOLHA: 5/9 / DATA: NOV 2026 / REV: A
10. **Tabela de especificacoes**: mesma estrutura dos blocos anteriores

---

## COMPONENTE 1: H02 — SERVO MG996R (Atuador Principal do Empurrador)

- **Tag badge**: `H02`
- **Descricao no badge**: `SERVO MG996R`
- **Subtitulo**: `ATUADOR DO EMPURRADOR LINEAR DE DESCARTE`
- **Status**: Em maos (ja possui 1 unidade)
- **Dimensoes fisicas**: 40.7 × 19.7 × 42.9 mm (corpo sem abas)
- **Desenhar**:
  - **Corpo retangular** principal com bordas arredondadas rx=3
  - **Abas de fixacao** (orelhas laterais): dois retangulos saindo do corpo, cada um com **2 furos de montagem** (total 4 furos, M3)
  - **Eixo de saida (spline)** no topo: circulo maior com spline 25 dentes desenhado como circulo serrilhado (ou circulo + circulo interno menor)
  - **Engrenagem interna** (indicativa): retangulo interno tracejado com texto "Metal Gear"
  - **Motor DC interno**: pequeno retangulo com simbolo de motor (M em circulo)
  - **Potenciometro de feedback**: circulo pequeno com seta
  - **Placa de controle** (PCB interna): retangulo tracejado fino
  - **Cabo com conector JST** saindo do corpo: 3 fios
  - **Cota do eixo**: indicar spline 25T
- **Terminais** (3 pads through-hole, conector JST):
  - `PWM` — Sinal de controle (pulso 500-2500 us) -> `GPIO18` (conforme board_config.h: AV_PIN_SERVO)
  - `VCC` — Alimentacao +6.0V (do Buck XL4015 E02)
  - `GND` — Terra comum
- **Especificacoes desenhadas** no corpo ou ao lado:
  - Torque: 11 kg·cm @ 6V
  - Velocidade: 0.14 s/60° @ 6V
  - Angulo: 0-180° (PWM 50 Hz)
  - LEDC Channel 0
- **Nota abaixo**: "Empurrador linear via horn metalico 25T (M12) + alavanca R=60mm"
- **Cotas**: 40.7 × 19.7 × 42.9 mm

---

## COMPONENTE 2: H03 — SERVO MG995 (Reserva x2)

- **Tag badge**: `H03`
- **Descricao no badge**: `SERVO MG995 (RESERVA x2)`
- **Subtitulo**: `SUBSTITUICAO IMEDIATA DO MG996R`
- **Status**: Em maos (ja possui 2 unidades de reserva)
- **Dimensoes fisicas**: 40.7 × 19.7 × 42.9 mm (mesma forma do MG996R)
- **Desenhar**:
  - **Mesmo formato do MG996R** (sao fisicamente identicos), mas com diferenciacao visual:
  - **Texto "RESERVA"** em destaque dentro do corpo
  - **"x2"** indicando quantidade
  - Corpo, abas, furos, eixo spline — tudo igual ao H02
  - Engrenagem interna com texto "Metal Gear" (identico)
  - Cabo com conector JST (3 fios)
  - **Hachura diagonal** leve no fundo do corpo para diferenciar visualmente do H02 (usar pattern hatch-b5)
- **Terminais** (3 pads through-hole):
  - `PWM` — Mesmo pino GPIO18 (substitui o H02 no caso de falha)
  - `VCC` — +6.0V (E02)
  - `GND` — Terra
- **Especificacoes**:
  - Torque: 11 kg·cm @ 6V (compativel)
  - Velocidade: 0.16 s/60° @ 6V
  - Angulo: 0-180°
  - "Compativel pino-a-pino com MG996R"
- **Nota abaixo**: "Reserva operacional — troca direta em caso de falha na feira (sem reconfigurar)"
- **Cotas**: 40.7 × 19.7 × 42.9 mm

---

## COMPONENTE 3: M13 — MOTORREDUTOR GA37-520 12V 60RPM

- **Tag badge**: `M13`
- **Descricao no badge**: `MOTORREDUTOR GA37-520`
- **Subtitulo**: `TRACAO DA ESTEIRA TRANSPORTADORA`
- **Status**: Confirmar se ja possui (ver nota na BOM)
- **Dimensoes fisicas**: corpo diam ~37mm × ~73mm comprimento total (com eixo D diam 6mm)
- **Desenhar**:
  - **Vista lateral** do motorredutor:
  - **Motor DC cilindrico** (parte traseira): retangulo com cantos arredondados, com simbolo de motor (M em circulo), 2 terminais de alimentacao saindo
  - **Caixa de reducao** (parte frontal): retangulo mais largo acoplado ao motor, com engrenagens internas indicadas por circulos dentados tracejados
  - **Eixo de saida tipo D**: linha saindo da caixa de reducao, com seccao transversal em D desenhada (circulo com faceta plana)
  - **Seccao transversal do eixo D**: desenhar um pequeno detalhe ampliado mostrando diam 6mm com a faceta plana (flat shaft)
  - **Flange de fixacao** com 2 furos de montagem M3
  - **Polia GT2 20T** indicada no eixo (desenhar acoplada): circulo com dentes na periferia + parafuso grub M3 de fixacao
  - **Especificacoes no corpo ou ao lado**:
    - 12V DC
    - 60 RPM (reducao ~1:50)
    - Eixo D diam 6mm
    - Corrente nominal ~0.8A, stall ~3.5A
- **Terminais** (2 pads through-hole):
  - `M+` — Motor positivo (+12V via MOSFET D4184 E04 ou via BTS7960)
  - `M-` — Motor negativo (GND)
- **Notas abaixo**:
  - "Driver 1 (MOSFET D4184): GPIO19 (AV_PIN_MOTOR_EN), ativo HIGH"
  - "Driver 2 (BTS7960): RPWM=GPIO21, LPWM=GPIO22, EN=GPIO23"
  - "PWM 20 kHz (LEDC Channel 1) — velocidade ajustavel pelo software"
  - "Transmissao: polia GT2 20T (eixo motor) -> GT2 40T (eixo motriz) via correia GT2 200mm"
- **Cotas**: diam 37mm corpo, comprimento total ~73mm, eixo D diam 6mm

---

## TABELA DE ESPECIFICACOES

| TAG | COMPONENTE | ESPECIFICACAO | FUNCAO NO PROJETO |
|-----|-----------|---------------|-------------------|
| H02 | Servo MG996R | 11 kg·cm @ 6V, PWM 50Hz, 25T spline | Empurrador linear (GPIO18, LEDC Ch.0) |
| H03 | Servo MG995 (x2 reserva) | 11 kg·cm @ 6V, compativel MG996R | Substituicao imediata do H02 na feira |
| M13 | Motorredutor GA37-520 | 12V 60RPM, eixo D diam 6mm, ~0.8A | Tracao da esteira (GPIO19 ou BTS7960) |

---

## SECTION WRAPPER

```html
<section id="bloco-5" class="sheet-section">
  <h2>BLOCO 05 — ATUADORES (Folha 5/9)</h2>
  <div class="canvas-wrap">
    <svg viewBox="0 0 900 600" width="900" height="600" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <!-- patterns grid-b5, grid-major-b5, hatch-b5 aqui -->
      </defs>
      <!-- todo o conteudo SVG aqui -->
    </svg>
  </div>
</section>
```

---

## CHECKLIST FINAL

- [ ] Section id="bloco-5" com class="sheet-section"
- [ ] Titulo h2: `BLOCO 05 — ATUADORES (Folha 5/9)`
- [ ] Pattern IDs unicos (grid-b5, grid-major-b5, hatch-b5)
- [ ] Grid duplo + moldura dupla
- [ ] 3 componentes (H02, H03, M13) com badges de tag proeminentes
- [ ] Cotas dimensionais em mm em todos os componentes
- [ ] Todos os terminais com pads through-hole (dois circulos concentricos)
- [ ] Tabela de especificacoes na parte inferior
- [ ] Bloco de titulo (Folha 5/9) no canto inferior direito
- [ ] SOMENTE variaveis CSS — zero cores literais
- [ ] Pill adicionado ao nav no formato longo padrao
- [ ] Span placeholder atualizado para "FOLHAS 6-9"
- [ ] Tema claro/escuro: apenas usar variaveis, nao alterar CSS/script
- [ ] NAO alterou nada nos Blocos 1/2/3/4
- [ ] NAO alterou o CSS nem o script
- [ ] GPIOs corretos: Servo=18, Motor_EN=19, BTS_RPWM=21, BTS_LPWM=22, BTS_EN=23
- [ ] Tensoes corretas: Servo=6.0V (E02), Motor=12V (E01)
