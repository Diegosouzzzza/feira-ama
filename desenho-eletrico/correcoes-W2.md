# PROMPT DE CORRECOES — BLOCO W2: REDE DE SENSORES E E-STOP

## CONTEXTO

Voce esta editando o arquivo unico:
`file:///C:/Users/ponto/OneDrive/Desktop/FEIRA%20-%20AMA/desenho-eletrico/esp32.html`

O Bloco W2 ja existe (secao `id="wiring-2"`, linhas ~6080-7555). Ele foi desenhado e agora precisa de **CORRECOES** baseadas em auditoria tecnica.

**REGRA ABSOLUTA**: NAO altere NADA fora da secao `<section id="wiring-2">`. NAO toque no CSS, no script, na Tab 1, no W1, nem nos pills de navegacao.

---

## RESULTADO DA AUDITORIA

### ITENS APROVADOS (NAO MEXER)
- ✅ 22 fios presentes (W021-W042) — contagem completa
- ✅ Tabela de fios completa com todos os 22 registros
- ✅ Bloco de titulo correto (FOLHA 2/5, NOV 2026, REV A)
- ✅ Notas tecnicas precisas (board_config.h correto)
- ✅ Zero cores literais — todas variaveis CSS
- ✅ Pattern IDs unicos (grid-w2, grid-major-w2, hatch-w2, arrow-w2)
- ✅ Moldura dupla correta para viewBox 1400x900
- ✅ Fios GND usam classe correta (wire-gnd)
- ✅ Sensores H04 e E07 usam desenhos reais com transform/scale
- ✅ E-STOP E12 usa desenho real com transform/scale
- ✅ Protoboard E26 com E11x2 e E10x2 montados
- ✅ Zoom box do circuito clamp presente com calculos
- ✅ Borne X2 SAK 7 vias desenhado corretamente
- ✅ Legenda de sensores no topo presente

---

## BUG 1 — CRITICO: ESP32 CORTADO NA DIREITA (ULTRAPASSA VIEWBOX)

**O que acontece**: O desenho completo do ESP32 H01 usa transform `translate(1000, 75) scale(0.85) translate(-260, -60)`. Com esta escala e posicao:
- O corpo do ESP32 ocupa x=1000 ate x=1238 (ok)
- Os NOMES dos pinos direitos (ex: "D23", "D22") ficam em x≈1289 (ok)
- As DESCRICOES dos pinos direitos (ex: "GPIO23 VSPI", "GPIO22 SCL") ficam em x≈1378 — **ULTRAPASSA a moldura interna (borda direita = 1375)**
- A COTA de altura (51.4mm, linha vertical + texto em x=745 local) fica em x≈1404-1412 — **ULTRAPASSA O VIEWBOX (1400)! Completamente invisivel!**

**Correcao obrigatoria**: Reduzir a escala do ESP32 de 0.85 para **0.55** e reposicionar. O novo transform deve ser:
```
transform="translate(970, 80) scale(0.55) translate(-260, -60)"
```

Com scale=0.55:
- Corpo: x=970 ate x=970 + 280*0.55 = 970+154 = 1124. Largura confortavel.
- Pinos direitos descricoes (x=705 local): 970 + (705-260)*0.55 = 970 + 244.75 = 1214.75. Dentro do frame.
- Cota altura (x=745 local): 970 + (745-260)*0.55 = 970 + 266.75 = 1236.75. Dentro do frame.
- Pinos esquerdos descricoes (x=95 local): 970 + (95-260)*0.55 = 970 - 90.75 = 879.25. Livre do zoom box.
- Borda inferior do corpo (y=660 local): 80 + (660-60)*0.55 = 80 + 330 = 410. Cabe no frame.

**IMPORTANTE**: Ao reduzir a escala, a font-size dos labels fica menor. Para compensar, considere aumentar a font-size dos 3 pinos usados (GPIO25, GPIO26, GPIO27) ou manter os destaques maiores.

---

## BUG 2 — CRITICO: BADGES GPIO DESALINHADOS (60px ABAIXO DOS PINOS REAIS)

**O que acontece**: Os 3 circulos de destaque (GPIO25←S1, GPIO26←S2, GPIO27←ESTOP) estao posicionados ~60 unidades SVG ABAIXO das posicoes reais dos pinos apos o transform ser aplicado.

**Calculo correto** (com scale=0.55 proposto no Bug 1):

| Pino | Y local | Y final = 80 + (Y-60)*0.55 | X final (pad cx=246) = 970 + (246-260)*0.55 |
|------|---------|---------------------------|----------------------------------------------|
| GPIO25 (pino 9, cy=350) | 350 | 80 + 290*0.55 = **239.5** | 970 - 7.7 = **962.3** |
| GPIO26 (pino 10, cy=380) | 380 | 80 + 320*0.55 = **256** | 962.3 |
| GPIO27 (pino 11, cy=410) | 410 | 80 + 350*0.55 = **272.5** | 962.3 |

**Correcao obrigatoria**: Recalcular TODAS as posicoes dos highlights e wires terminais com o NOVO transform (scale=0.55). Os circulos de destaque, badges e pontos de juncao dos fios W036/W041/W042 devem apontar para as coordenadas corretas dos pinos.

Exemplo para GPIO25:
```svg
<!-- GPIO25 (Pino 9) — RECALCULADO -->
<circle cx="962" cy="240" r="6" fill="none" stroke="var(--line)" stroke-width="2.5"/>
<rect x="880" y="233" width="70" height="14" rx="2" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.2"/>
<text x="915" y="243" text-anchor="middle" font-size="6.5" font-weight="bold" fill="var(--fg)">GPIO25 ← S1</text>
```

E os fios W036, W041, W042 devem terminar nas novas coordenadas:
- W036 termina em: **(962, 240)** (nao mais 1017, 381)
- W041 termina em: **(962, 256)** (nao mais 1017, 406.5)
- W042 termina em: **(962, 273)** (nao mais 1017, 432)

---

## BUG 3 — MODERADO: FIOS W021 E W024 COM CLASSE ERRADA

**O que acontece**: W021 (H04:VCC → +5V) e W024 (E07:VCC → +5V) sao fios de ALIMENTACAO (+5V) mas usam `class="wire-signal"` (stroke 1.0px) em vez de `class="wire-power"` (stroke 1.8px, mais grosso).

**Correcao obrigatoria**:

Linha ~6132 (W021):
```
ANTES: <path d="M 70.5,208 L 40,208 ..." fill="none" class="wire-signal"/>
DEPOIS: <path d="M 70.5,208 L 40,208 ..." fill="none" class="wire-power"/>
```

Linha ~6156 (W024):
```
ANTES: <path d="M 70.5,418 L 48,418 ..." fill="none" class="wire-signal"/>
DEPOIS: <path d="M 70.5,418 L 48,418 ..." fill="none" class="wire-power"/>
```

---

## BUG 4 — MENOR: W024 TEM SUBPATH ORFAO

**O que acontece**: O path do W024 termina com `M 565,60 L 570,60` — uma linha horizontal de 5px desconectada, sem funcao. Cria artefato visual minusculo.

**Correcao obrigatoria**: Remover o trecho `M 565,60 L 570,60` do path:

```
ANTES:  d="M 70.5,418 L 48,418 L 48,60 L 565,60 L 565,120 M 565,60 L 570,60"
DEPOIS: d="M 70.5,418 L 48,418 L 48,60 L 565,60 L 565,120"
```

E adicionar junction dot em (565,120) se nao existir.

---

## BUG 5 — MENOR: COMENTARIO QUEBRADO NA LINHA ~6666

**O que acontece**: A linha tem:
```
CORPO DO ESP32 (PCB)                 -->
```
Faltando o `<!--` de abertura. O SVG ignora texto fora de `<text>` mas e codigo invalido.

**Correcao obrigatoria**:
```
ANTES:  CORPO DO ESP32 (PCB)                 -->
DEPOIS: <!-- CORPO DO ESP32 (PCB)            -->
```

---

## CONSEQUENCIAS EM CASCATA DA MUDANCA DE ESCALA (BUG 1 + BUG 2)

Ao mudar o transform do ESP32 de `scale(0.85)` para `scale(0.55)` e reposicionar, TODAS estas coordenadas absolutas que referenciam posicoes do ESP32 precisam ser recalculadas:

### 1. Destaques GPIO (fora do grupo transform)
- Circulo GPIO25: recalcular cx, cy
- Circulo GPIO26: recalcular cx, cy
- Circulo GPIO27: recalcular cx, cy
- Badge rects e textos: recalcular x, y

### 2. Fios que terminam no ESP32 (coordenadas absolutas)
- **W036**: path termina em `L 1017,381` → recalcular para a nova posicao do GPIO25
- **W041**: path termina em `L 1017,406.5` → recalcular para a nova posicao do GPIO26
- **W042**: path termina em `L 1017,432` → recalcular para a nova posicao do GPIO27

### 3. Fios que PASSAM pelo area do ESP32
- **W021**: path topo passa por y=55, vai ate x=570 → verificar se ainda conecta visualmente ao barramento +5V da protoboard
- **W024**: path topo passa por y=60, vai ate x=565 → idem

### Formula geral para converter local → SVG com novo transform:
```
SVG_x = 970 + (LOCAL_x - 260) * 0.55
SVG_y = 80 + (LOCAL_y - 60) * 0.55
```

### Tabela de pinos mais usados (coordenadas finais com novo transform):

| Pino | Local cx,cy | SVG cx | SVG cy |
|------|-------------|--------|--------|
| 3V3 (1) | 246, 110 | 962.3 | 107.5 |
| GND-L (14) | 246, 500 | 962.3 | 322 |
| VIN (16) | 554, 110 | 1131.7 | 107.5 |
| GND-R (17) | 554, 140 | 1131.7 | 124 |
| D23 (18) | 554, 170 | 1131.7 | 140.5 |
| D22 (19) | 554, 200 | 1131.7 | 157 |
| D21 (22) | 554, 290 | 1131.7 | 206.5 |
| D19 (23) | 554, 320 | 1131.7 | 223 |
| D18 (24) | 554, 350 | 1131.7 | 239.5 |
| D2/GPIO2 (29) | 554, 500 | 1131.7 | 322 |
| **D25/GPIO25 (9)** | **246, 350** | **962.3** | **239.5** |
| **D26/GPIO26 (10)** | **246, 380** | **962.3** | **256** |
| **D27/GPIO27 (11)** | **246, 410** | **962.3** | **272.5** |

---

## CHECKLIST DE VALIDACAO APOS CORRECOES

- [ ] ESP32 inteiro visivel dentro da moldura (nenhum elemento ultrapassando x=1350 ou y=850 da moldura interna)
- [ ] Cota de altura (51.4mm) visivel e dentro do frame
- [ ] Descricoes dos pinos direitos (GPIO23 VSPI, etc.) legiveis e dentro do frame
- [ ] Descricoes dos pinos esquerdos (GPIO25 DAC, etc.) NAO sobrepondo o zoom box ou fios
- [ ] 3 circulos de destaque GPIO apontando exatamente nos pads corretos
- [ ] W036 terminando exatamente no pad do GPIO25 (nova coordenada)
- [ ] W041 terminando exatamente no pad do GPIO26 (nova coordenada)
- [ ] W042 terminando exatamente no pad do GPIO27 (nova coordenada)
- [ ] W021 e W024 usando class="wire-power" (stroke mais grosso)
- [ ] W024 sem subpath orfao M 565,60
- [ ] Comentario da linha ~6666 corrigido com `<!--`
- [ ] Nenhum texto ou elemento sobrepondo outro
- [ ] Zoom box (x=560-930, y=525-730) livre de sobreposicao com ESP32
- [ ] Tabela de fios inalterada (ja estava correta)
- [ ] Notas tecnicas inalteradas (ja estavam corretas)
- [ ] Bloco de titulo inalterado (ja estava correto)
- [ ] ZERO cores literais — SOMENTE variaveis CSS
- [ ] Pattern IDs continuam unicos (grid-w2, etc.)
- [ ] Moldura dupla inalterada

---

## REGRAS INVIOLAVEIS

1. **SOMENTE** variaveis CSS para cores: `var(--bg)`, `var(--fg)`, `var(--line)`, `var(--line-thin)`, `var(--pin-text)`, `var(--grid)`, `var(--grid-major)`, `var(--dim)`, `var(--trace)`, `var(--pad-fill)`, `var(--tag-bg)`, `var(--header-bg)`, `var(--header-border)`. NUNCA cores literais como #fff, black, rgb(), etc.
2. **NAO altere** CSS, script, Tab 1, W1, nav pills
3. **NAO altere** a tabela de fios, notas tecnicas, ou bloco de titulo (ja corretos)
4. **NAO altere** os desenhos dos sensores H04, E07, E-STOP E12, borne X2, ou protoboard E26 (ja corretos)
5. **NAO remova** nenhum fio (W021-W042 devem todos existir)
6. Pads through-hole: SEMPRE dois circulos concentricos (r=5 stroke 1 + r=2 fill var(--bg))
7. A secao deve continuar dentro de `<section id="wiring-2" class="sheet-section">`
