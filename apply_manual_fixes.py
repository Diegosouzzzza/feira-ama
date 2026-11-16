# -*- coding: utf-8 -*-
import json
import re

with open('Manual_Montagem_Esteira_70cm.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("Original length of Manual_Montagem_Esteira_70cm.html:", len(html))

# =========================================================================
# 1. BANNER & CARDS (HTML Texts)
# =========================================================================

# Notice Banner
old_banner = 'Chassi modular de 700 mm (14 módulos PETG para Bambu Lab A1 Mini), entre eixos de 650 mm, tambores Ø 60 mm, correia de 86 elos articulados (122 mm útil), Cúpula anti-reflexo com Ring Light 6000K e Câmera 1080p em X = -150 mm (Sensor S1), Sensor S2 em X = +100 mm (60 mm antes do Empurrador), Empurrador Linear MG996R com curso de 115 mm em X = +160 mm, Rampa Lateral (Y = 108 a 55 mm) e Caixas Coletoras apoiadas no piso (Y = 0 mm).'
new_banner = 'Chassi modular de 700 mm (13 mesas de impressão nesteadas para Bambu Lab P2S 256×256 mm), entre eixos de 650 mm, tambores Ø 60 mm, correia de 86 elos articulados de passo 17,3 mm (122 mm útil), Cúpula anti-reflexo de 260 mm com Ring Light 6000K em Y = 215 mm e Câmera 1080p em Y = 255 mm em X = -150 mm (Sensor S1), Sensor Óptico Retangular 5V TTL S2 em X = +100 mm (60 mm antes do Empurrador, feixe Y = 90 mm), Empurrador Linear MG996R biela-manivela com curso de 120 mm em X = +160 mm (sapata côncava 100×90 mm R=45 mm com EVA 2 mm para maçã Ø80 mm), Rampa Lateral Suave 18° com defletor EVA 3 mm e Caixas Coletoras 152×152×55 mm apoiadas no piso (Caixa Aprovados em X = +375 mm).'
html = html.replace(old_banner, new_banner)

# Card 1 (Chassi)
old_card1_desc = '14 seções modulares impressas em PETG (7 módulos de 100 mm por longarina para mesa 180×180 mm da Bambu Lab A1 Mini), unidas por flanges com parafusos M4×16 mm. Mesa central de deslizamento em Y = 105 mm sustentando a correia, abas de contenção subindo até Y = 125 mm (+12,5 mm sobre a correia), vão livre de descarte de 100 mm (X = +110 a +210 mm) e 4 pares de pés em X = -310, -100, +100, +310 mm com sapatas antivibração apoiadas em Y = 0 mm.'
new_card1_desc = '13 mesas de impressão nesteadas para Bambu Lab P2S (256×256 mm) em PETG preto industrial, unidas por flanges com parafusos M4×16 mm e porcas Nyloc. Mesa central de deslizamento em Y = 105 mm sustentando a correia, abas de contenção subindo até Y = 125 mm (+12,5 mm sobre a correia), vão livre de descarte de 100 mm (X = +110 a +210 mm) e 4 pares de pés em X = -310, -100, +100, +310 mm com sapatas antivibração em TPU 95A apoiadas em Y = 0 mm.'
html = html.replace(old_card1_desc, new_card1_desc)
html = html.replace('PETG 4 paredes · Infill 30% · 14 módulos de 100 mm · Parafusos M4×16', 'PETG 3 paredes · Infill 22% Gyroid · 13 Mesas Bambu P2S · DfAM < 2400g')

# Card 2 (Correia)
old_card2_desc = '86 elos articulados de 122 mm de largura útil (elo.model: 25,4 × 122,0 × 8,9 mm), interconectados por pinos de 1,75 mm. Ramo superior apoiado na mesa deslizante (base Y = 108 mm, topo de transporte Y = 112,5 mm), ramo inferior de retorno em Y = 47,5 a 52 mm e curvas semicirculares perfeitas envolvendo os tambores de R = 30 mm com zero colisão. Animação real em circuito fechado.'
new_card2_desc = '86 elos articulados de 122 mm de largura útil (elo.model: passo 17,3 mm × 122,0 × 8,9 mm), interconectados por pinos de 1,75 mm de filamento PETG. O passo de 17,3 mm fecha com precisão o circuito fechado de 1488,5 mm. Ramo superior apoiado na mesa deslizante (base Y = 108 mm, topo de transporte Y = 112,5 mm), ramo inferior de retorno em Y = 47,5 a 52 mm e curvas perfeitas envolvendo os tambores de R = 30 mm. Animação real em circuito fechado.'
html = html.replace(old_card2_desc, new_card2_desc)
html = html.replace('86 Elos · Largura: 122 mm · Passo: 25,4 mm (1 pol) · Pinos 1,75 mm', '86 Elos · Largura: 122 mm · Passo: 17,3 mm · Pinos 1,75 mm')

# Card 5 (Cúpula)
old_card5_desc = 'Cúpula industrial semi-fechada em túnel cobrindo X = -210 a -90 mm (120 mm de extensão). Estrutura em PETG preto fosco anti-reflexo bloqueando iluminação ambiente do ginásio, com Janela Frontal de Inspeção em Acrílico Transparente/Fumê voltada para o público (+Z). Aloja internamente Câmera UVC USB 1080p no topo (Y = 235 mm), Ring Light LED 12V 6000K e difusor leitoso.'
new_card5_desc = 'Cúpula industrial semi-fechada em túnel cobrindo X = -210 a -90 mm (120 mm de extensão) com altura externa ampliada para 260 mm (Mesa 09). Estrutura em PETG preto fosco anti-reflexo bloqueando iluminação ambiente do ginásio, com Janela Frontal de Inspeção em Acrílico Transparente/Fumê voltada para o público (+Z). Aloja internamente Câmera UVC USB 1080p no topo (Y = 255 mm), Ring Light LED 12V 6000K em Y = 215 mm e difusor leitoso de 1 mm para enquadramento ideal de maçãs Ø80 mm.'
html = html.replace(old_card5_desc, new_card5_desc)
html = html.replace('Posição X: -150 mm · Câmera 1080p (Y = 235) · Ring Light 12V 6000K', 'Posição X: -150 mm · Câmera 1080p (Y = 255) · Ring Light 12V (Y = 215)')

# Card 6 (Sensores)
old_card6 = '''        <!-- Component 6 -->
        <div class="component-card" id="card-6" onclick="selectComponent(6)">
          <div class="card-top">
            <span class="card-num">6</span>
            <span class="card-title">Sensores Fotoelétricos M18</span>
            <span class="card-tag">Sensores</span>
          </div>
          <p class="card-desc">Sensores industriais cilíndricos M18 PNP 24V DC fixados em suportes rígidos (suporte_sensor.model: 54×14,9×100 mm) na face externa da longarina esquerda (Z = -75 mm): S1 em X = -150 mm (disparo da câmera e parada da esteira) e S2 em X = +100 mm (gatilho de sincronismo de descarte, exatamente 60 mm antes do Empurrador Linear). Ambos com isolamento óptico PC817.</p>
          <span class="card-spec">M18 PNP 24V · S1: X = -150 mm · S2: X = +100 mm · Feixe Y = 124 mm</span>
        </div>'''
new_card6 = '''        <!-- Component 6 -->
        <div class="component-card" id="card-6" onclick="selectComponent(6)">
          <div class="card-top">
            <span class="card-num">6</span>
            <span class="card-title">Sensores Ópticos Retangulares</span>
            <span class="card-tag">Sensores</span>
          </div>
          <p class="card-desc">Sensores fotoelétricos infravermelhos retangulares com LED vermelho visível (corpo 45×20×15 mm, alimentação 5V TTL NPN) fixados em suportes rígidos 04A (cavidade 46×21×16 mm com parafusos M3 inferiores de entre-centros 25 mm): S1 em X = -150 mm (disparo da câmera e parada da esteira) e S2 em X = +100 mm (gatilho de sincronismo de descarte, exatamente 60 mm antes do Empurrador Linear). Altura do feixe em Y = 90 mm otimizada para o centro de maçãs Ø80 mm, alimentados via Buck 5V sem optoacopladores.</p>
          <span class="card-spec">Óptico Retangular 5V TTL · S1: X = -150 mm · S2: X = +100 mm · Feixe Y = 90 mm</span>
        </div>'''
html = html.replace(old_card6, new_card6)

# Card 7 (Empurrador)
old_card7_desc = 'Mecanismo oficial e definitivo de separação em X = +160 mm. Pórtico fixado na longarina esquerda com duas guias lineares cilíndricas de aço retificado Ø 6 mm e buchas de precisão. Acionado por Servomotor MG996R (11 kgf·cm) via biela-manivela com horn 25T. Sapata côncava (55×34 mm) com almofada protetora de EVA. Em repouso: recolhida em Z = -62 mm (122 mm de pista livre); em rejeição: curso linear transversal de 115 mm até Z = +53 mm, empurrando o fruto defeituoso direto para a rampa.'
new_card7_desc = 'Mecanismo oficial e definitivo de separação em X = +160 mm. Pórtico 03E fixado na longarina esquerda com 4 buchas LM6UU e duas guias lineares de aço retificado inox Ø 6 × 170 mm (entre-centros 85 mm). Acionado por Servomotor MG996R (11 kgf·cm) via alavanca R = 60 mm parafusada no horn 25T, biela entre centros L = 110 mm com rolamentos 623ZZ e trave traseira 03I (90×18×12 mm). Sapata côncava 03H (100×90×12 mm, raio côncavo R = 45 mm com almofada de EVA 2 mm) dimensionada para maçã Ø80 mm (220 g). Em repouso: Z = -62 mm; em rejeição: curso linear real de 120 mm até Z = +58 mm (tempo ~0,45 s em 6 V), empurrando a maçã diretamente para a rampa.'
html = html.replace(old_card7_desc, new_card7_desc)
html = html.replace('Posição X: +160 mm · Curso: 115 mm · Guias Ø 6 mm · Servo MG996R 6V', 'Posição X: +160 mm · Curso: 120 mm · R=60 / L=110 · Guias Ø 6 × 170 mm · Servo MG996R 6V')

# Card 8 (Rampa)
old_card8_desc = 'Calha inclinada a 25° (CAD original: rampa.model, largura útil 89,4 mm). Encaixada no vão lateral direito de X = +110 a +210 mm (centrada em X = +160 mm, alinhada com o Empurrador). Borda superior nivelada em Y = 108 mm (Z = +65 mm) logo abaixo da correia, descendo suavemente até a borda da Caixa de Rejeitados em Y = 55 mm (Z = +155 mm).'
new_card8_desc = 'Calha inclinada suave de 18° (peça 06A da Mesa 10, largura útil 100 mm) com aba defletora em EVA 3 mm (120×30×3 mm) colada na borda final para amortecer o rolamento de maçãs esféricas Ø80 mm. Encaixada no vão lateral direito de X = +110 a +210 mm (centrada em X = +160 mm, alinhada com o Empurrador), conduzindo os frutos descartados sem risco de ricochete para a Caixa de Rejeitados.'
html = html.replace(old_card8_desc, new_card8_desc)
html = html.replace('Posição X: +160 mm · Boca: 89,4 mm · Inclinação: 25° · Y: 108 → 55 mm', 'Posição X: +160 mm · Boca: 100 mm · Inclinação: 18° · Defletor EVA 3 mm')

# Card 9 (Caixas)
old_card9 = '''        <!-- Component 9 -->
        <div class="component-card" id="card-9" onclick="selectComponent(9)">
          <div class="card-top">
            <span class="card-num">9</span>
            <span class="card-title">Caixas Coletoras (152×152)</span>
            <span class="card-tag">Coleta</span>
          </div>
          <p class="card-desc">Duas caixas coletoras idênticas (CAD original: caixa.model, 152,4 × 152,4 × 57,2 mm) apoiadas diretamente na bancada em Y = 0 mm: Caixa 1 (Aprovados - Classe A) na saída frontal em X = +435 mm (Z = 0 mm), recebendo frutos que passam direto pelo tambor motor; Caixa 2 (Rejeitados - Classes B/C) na saída inferior da rampa lateral em X = +160 mm (Z = +190 mm).</p>
          <span class="card-spec">CAD caixa.model · 152,4×152,4×57,2 mm · Base no piso Y = 0 mm</span>
        </div>'''
new_card9 = '''        <!-- Component 9 -->
        <div class="component-card" id="card-9" onclick="selectComponent(9)">
          <div class="card-top">
            <span class="card-num">9</span>
            <span class="card-title">Caixas Coletoras (152×152×55 mm)</span>
            <span class="card-tag">Coleta</span>
          </div>
          <p class="card-desc">Duas caixas coletoras idênticas (Mesa 11: 152 × 152 × 55 mm, paredes 2,4 mm reforçadas por colarinho de 4 mm) apoiadas diretamente na bancada em Y = 0 mm: Caixa 1 (Aprovados - Classe A) na saída frontal em X = +375 mm (Z = 0 mm), recebendo as maçãs que passam direto pelo tambor motor; Caixa 2 (Rejeitados - Classes B/C) na saída inferior da rampa lateral em X = +160 mm (Z = +190 mm).</p>
          <span class="card-spec">Peça 06B · 152×152×55 mm · Saída frontal X = +375 mm · Base no piso Y = 0 mm</span>
        </div>'''
html = html.replace(old_card9, new_card9)

# Card 10 (Motorredutor)
old_card10_desc = 'Motorredutor DC 12V de alto torque montado na face externa traseira da longarina esquerda (X = +285 mm, Y = 52 mm, Z = -75 mm) via suporte metálico em L com 4 parafusos M3. Transmissão por correia dentada GT2 fechada (largura 6 mm) no plano Z = -88 mm entre polia motora 20T (Ø 16 mm) e polia movida 40T (Ø 32 mm) no eixo do tambor tracionador, gerando redução mecânica de 2:1 (dobro de torque).'
new_card10_desc = 'Motorredutor GA37 12V 60 RPM nominal montado na face externa traseira da longarina esquerda (X = +285 mm, Y = 52 mm, Z = -75 mm) via flange com ajuste oblongo (suporte 03A) e parafusos M3. Transmissão por correia dentada GT2 fechada (largura 6 mm) entre polia motora 20T e polia movida 40T (redução 2:1), resultando em 30 RPM no tambor de Ø60 mm e velocidade linear oficial contínua de 94 mm/s na esteira (tempo S1→S2 de 2,66 s e S2→Empurrador de 0,64 s).'
html = html.replace(old_card10_desc, new_card10_desc)
html = html.replace('Motorredutor 12V DC · Redução GT2 2:1 (20T / 40T) · Correia GT2 6 mm', 'Motorredutor GA37 12V 60 RPM · Redução GT2 2:1 · 30 RPM / 94 mm/s')

# Action Bar
html = html.replace('Simular Fruto Rejeitado (Empurrador)', 'Simular Maçã Rejeitada (Empurrador)')
html = html.replace('Simular Fruto Aprovado (Passa Direto)', 'Simular Maçã Aprovada (Passa Direto)')

# =========================================================================
# 2. ELECTRICAL SECTION (secElectrical)
# =========================================================================
old_sec_elec = '''      <!-- Architecture Badges & Summary -->
      <div style="display: flex; flex-wrap: wrap; gap: 0.8rem; margin: 0.5rem 0 1rem 0;">
        <span class="badge-volt badge-12v">⚡ PS1: Fonte Chaveada 12V DC — 10A (120W)</span>
        <span class="badge-volt badge-24v">⚡ PS2: Fonte Industrial 24V DC — 2A (Sensores M18)</span>
        <span class="badge-volt badge-safe">🛡️ Segurança NR-12: Relé K1 40A corta +12V_AT</span>
        <span class="badge-volt badge-6v">🔧 Servo: Buck XL4015 5A ajustado em 6,0V + 1000µF</span>
        <span class="badge-volt badge-5v">💻 ESP32: Buck 5V 2A no pino VIN · USB sem VBUS</span>
      </div>'''

new_sec_elec = '''      <!-- Architecture Badges & Summary -->
      <div style="display: flex; flex-wrap: wrap; gap: 0.8rem; margin: 0.5rem 0 1rem 0;">
        <span class="badge-volt badge-12v">⚡ Fonte Única Chaveada 12V DC — 10A (120W) [Mono-Fonte]</span>
        <span class="badge-volt badge-safe">🛡️ Segurança NR-12: Relé K1 40A corta +12V_AT</span>
        <span class="badge-volt badge-6v">🔧 Servo: Buck XL4015 5A ajustado em 6,0V + 1000µF (Curso 120 mm)</span>
        <span class="badge-volt badge-5v">💻 ESP32 & Sensores: Buck 5V 3A (S1/S2 TTL Direto)</span>
      </div>'''
html = html.replace(old_sec_elec, new_sec_elec)

old_elec_p = '''        Arquitetura eletroeletrônica oficial sincronizada com a Planta Elétrica do projeto AmazonVision 4.0. Separação de fontes, isolamento óptico galvânico dos sensores industriais de 24V, controle seguro de potência do motor e servo, e parada de emergência seletiva em conformidade com a NR-12.'''
new_elec_p = '''        Arquitetura eletroeletrônica oficial sincronizada com a Planta Elétrica do projeto AmazonVision 4.0. Topologia Mono-Fonte 12V 10A, ligação direta dos sensores ópticos retangulares 5V TTL com proteção de clamp Schottky BAT54S (dispensando módulos optoacopladores), controle seguro de potência do motor GA37 (60 RPM) e servo MG996R (curso 120 mm), e parada de emergência seletiva em conformidade com a NR-12.'''
html = html.replace(old_elec_p, new_elec_p)

old_power_dist = '''          <ul style="font-size: 0.82rem; color: var(--ink-med); line-height: 1.6; padding-left: 1.2rem;">
            <li><strong>Fonte Principal PS1 (12V 10A):</strong> Alimenta o Motorredutor DC (via MOSFET), o conversor Buck do servo (6V), o conversor Buck do ESP32 (5V), o anel Ring Light LED 12V e a bobina do Relé K1.</li>
            <li><strong>Fonte Auxiliar PS2 (24V 2A):</strong> Dedicada exclusivamente à alimentação dos Sensores Fotoelétricos Industriais M18 (S1 e S2), garantindo imunidade a ruídos gerados pelos motores.</li>
            <li><strong>Barramento 0V Unificado:</strong> Os polos negativos (0V) de PS1, PS2, Bucks e ESP32 (GND) são solidamente interligados em uma barra de aterramento comum (0V_COMUM).</li>
          </ul>'''
new_power_dist = '''          <ul style="font-size: 0.82rem; color: var(--ink-med); line-height: 1.6; padding-left: 1.2rem;">
            <li><strong>Fonte Principal Única (12V 10A / 120W):</strong> Alimenta o Motorredutor GA37 12V 60 RPM (via MOSFET D4184), o conversor Buck XL4015 dedicado ao servo (6,0V), o conversor Buck LM2596 (5,0V para ESP32 e sensores ópticos retangulares S1/S2), o anel Ring Light LED 12V e a bobina do Relé K1.</li>
            <li><strong>Sensores Ópticos Retangulares 5V TTL:</strong> Alimentados pelo barramento de 5V do Buck do microcontrolador com chaveamento direto NPN para as GPIOs 25 e 26, eliminando fontes auxiliares e suprimindo módulos optoacopladores.</li>
            <li><strong>Barramento 0V Unificado:</strong> Os polos negativos (0V / GND) da fonte 12V, conversores Buck e ESP32 são solidamente interligados em uma barra de aterramento comum (0V_COMUM).</li>
          </ul>'''
html = html.replace(old_power_dist, new_power_dist)

# Pinout Table S1 and S2 rows
old_pinout_s1 = '''          <tr>
            <td><code>GPIO 25</code></td>
            <td><code>PIN_SENSOR_S1</code></td>
            <td>INPUT_PULLUP (Ativo LOW)</td>
            <td><strong>Sensor Óptico S1 (Inspeção Câmera)</strong></td>
            <td>Optoacoplador PC817 Canal 1 (Resistor 24V na entrada, saída chaveando 3,3V para GND)</td>
            <td>24V DC (Fonte PS2)</td>
          </tr>
          <tr>
            <td><code>GPIO 26</code></td>
            <td><code>PIN_SENSOR_S2</code></td>
            <td>INPUT_PULLUP (Ativo LOW)</td>
            <td><strong>Sensor Óptico S2 (Sincronismo Descarte)</strong></td>
            <td>Optoacoplador PC817 Canal 2 (Resistor 24V na entrada, saída chaveando 3,3V para GND)</td>
            <td>24V DC (Fonte PS2)</td>
          </tr>'''
new_pinout_s1 = '''          <tr>
            <td><code>GPIO 25</code></td>
            <td><code>PIN_SENSOR_S1</code></td>
            <td>INPUT_PULLUP (Ativo LOW)</td>
            <td><strong>Sensor Óptico Retangular S1 (Câmera)</strong></td>
            <td>Entrada digital 5V TTL direta com clamp BAT54S + resistor 1 kΩ (feixe Y = 90 mm)</td>
            <td>5,0V DC (Barramento Buck ESP32)</td>
          </tr>
          <tr>
            <td><code>GPIO 26</code></td>
            <td><code>PIN_SENSOR_S2</code></td>
            <td>INPUT_PULLUP (Ativo LOW)</td>
            <td><strong>Sensor Óptico Retangular S2 (Descarte)</strong></td>
            <td>Entrada digital 5V TTL direta com clamp BAT54S + resistor 1 kΩ (feixe Y = 90 mm)</td>
            <td>5,0V DC (Barramento Buck ESP32)</td>
          </tr>'''
html = html.replace(old_pinout_s1, new_pinout_s1)

# Pinout Table Servo and Motor rows
html = html.replace('pulsos de 500 a 2500 µs para curso de 115 mm', 'pulsos de 500 a 2500 µs para rotação de 180° e curso de 120 mm')
html = html.replace('<strong>Motorredutor DC 12V (Esteira)</strong>', '<strong>Motorredutor GA37 12V 60 RPM (Esteira)</strong>')

# =========================================================================
# 3. ASSEMBLY STEPS BUTTONS & DETAIL (secAssembly)
# =========================================================================
html = html.replace('<span class="step-title">Chassi Modular (14 Módulos)</span>', '<span class="step-title">Chassi Modular (13 Mesas P2S)</span>')
html = html.replace('<span class="step-fasteners">14x Módulos PETG · 24x M4×16mm</span>', '<span class="step-fasteners">13x Mesas P2S · 28x M4×16mm</span>')

html = html.replace('<span class="step-title">Tensor M5 & Correia de 86 Elos</span>', '<span class="step-title">Tensor M5 & Correia Passo 17,3mm</span>')
html = html.replace('<span class="step-fasteners">86x Elos · 86x Pinos 1.75 · 2x M5×40</span>', '<span class="step-fasteners">86x Elos (17,3mm) · 86x Pinos · M5×40</span>')

html = html.replace('<span class="step-title">Motorredutor DC 12V & GT2</span>', '<span class="step-title">Motorredutor GA37 60 RPM & GT2</span>')
html = html.replace('<span class="step-fasteners">1x Motor 12V · Polias 20T/40T · 4x M3×8</span>', '<span class="step-fasteners">GA37 60 RPM · Redução 2:1 (94 mm/s)</span>')

html = html.replace('<span class="step-title">Cúpula de Inspeção & Sensores M18</span>', '<span class="step-title">Cúpula 260mm & Sensores Retangulares</span>')
html = html.replace('<span class="step-fasteners">Cúpula PETG · Câmera 1080p · S1 & S2</span>', '<span class="step-fasteners">Cúpula 260mm · Cam 255mm · S1/S2 5V TTL</span>')

html = html.replace('<span class="step-fasteners">Servo MG996R · Guias Ø6 · Rampa · 2x Caixas</span>', '<span class="step-fasteners">MG996R Curso 120mm · Rampa 18° · Caixas 152mm</span>')

# =========================================================================
# 4. CAD BOM TABLE
# =========================================================================
old_cad_table = '''            <tr>
              <td><code>caixa.model</code> (2 un.)</td>
              <td>152,4 × 152,4 × 57,2</td>
              <td>Caixas coletoras de 6 polegadas apoiadas no piso (Y = 0 mm): 1 na saída frontal (X = +435 mm) e 1 na lateral (X = +160 mm, Z = +190 mm).</td>
            </tr>
            <tr>
              <td><code>rampa.model</code></td>
              <td>89,4 × 104,5 × 120,0</td>
              <td>Calha inclinada de descarte montada na abertura lateral direita (X = +160 mm), descendo de Y = 108 mm para Y = 55 mm.</td>
            </tr>
            <tr>
              <td><code>suporte_sensor.model</code> (2 un.)</td>
              <td>54,0 × 100,0 × 14,9</td>
              <td>Bases verticais com furação M18 fixadas na longarina esquerda em X = -150 mm (S1) e X = +100 mm (S2) na altura Y = 124 mm.</td>
            </tr>
            <tr>
              <td><code>suporte_servo.model</code></td>
              <td>165,0 × 62,0 × 83,0</td>
              <td>Pórtico estrutural do Empurrador Linear em X = +160 mm com suporte para o servo MG996R e guias de Ø 6 mm.</td>
            </tr>
            <tr>
              <td><code>pa.model</code> / Sapata</td>
              <td>55,0 × 34,0 × 12,0</td>
              <td>Sapata empurradora com face côncava adaptada para frutas, almofada de EVA e curso linear transversal de 115 mm.</td>
            </tr>
            <tr>
              <td><code>tambor_motor.model</code></td>
              <td>Ø 59,9 × 131,6</td>
              <td>Tambores de tração e retorno (Ø 60 mm) com dentes de arraste para a correia modular e furação para eixo inox Ø 8 mm.</td>
            </tr>
            <tr>
              <td><code>elo.model</code> (86 un.)</td>
              <td>25,4 × 122,0 × 8,9</td>
              <td>Elos articulados com passo de 25,4 mm (1 pol) interconectados por pinos de filamento de 1,75 mm.</td>
            </tr>'''

new_cad_table = '''            <tr>
              <td><code>caixa.model</code> (2 un.)</td>
              <td>152,0 × 152,0 × 55,0</td>
              <td>Caixas coletoras leves paramétricas (Mesa 11) apoiadas no piso (Y = 0 mm): 1 na saída frontal (X = +375 mm) e 1 na lateral (X = +160 mm, Z = +190 mm).</td>
            </tr>
            <tr>
              <td><code>rampa.model</code></td>
              <td>100,0 × 110,0 × 140,0</td>
              <td>Calha inclinada a 18° de descarte suave montada na abertura lateral direita (X = +160 mm), com aba defletora em EVA 3 mm (120×30×3 mm).</td>
            </tr>
            <tr>
              <td><code>suporte_sensor.model</code> (2 un.)</td>
              <td>46,0 × 21,0 × 16,0</td>
              <td>Suportes 04A com cavidade retangular e 2 furos M3 (entre-centros 25 mm) em X = -150 mm (S1) e X = +100 mm (S2), feixe óptico em Y = 90 mm.</td>
            </tr>
            <tr>
              <td><code>suporte_servo.model</code></td>
              <td>110,0 × 90,0 × 48,0</td>
              <td>Pórtico 03E do Empurrador Linear em X = +160 mm com 4 buchas LM6UU, guias Ø 6 × 170 mm (entre-centros 85 mm) e berço do servo MG996R.</td>
            </tr>
            <tr>
              <td><code>pa.model</code> / Sapata</td>
              <td>100,0 × 90,0 × 12,0</td>
              <td>Sapata côncava 03H (raio R = 45 mm para maçã Ø80 mm) com almofada de EVA 2 mm, alavanca R = 60 mm, biela L = 110 mm e curso útil de 120 mm.</td>
            </tr>
            <tr>
              <td><code>tambor_motor.model</code></td>
              <td>Ø 59,9 × 131,6</td>
              <td>Tambores ocos DfAM de tração e retorno (Ø 60 mm) com dentes de arraste para a correia modular e eixos inox Ø 8 mm.</td>
            </tr>
            <tr>
              <td><code>elo.model</code> (86 un.)</td>
              <td>17,3 × 122,0 × 8,9</td>
              <td>Elos articulados com passo oficial de 17,3 mm interconectados por pinos de filamento PETG de 1,75 mm, fechando o circuito de 1488,5 mm.</td>
            </tr>'''
html = html.replace(old_cad_table, new_cad_table)

# BOM additions in Fasteners Table
old_fastener_table_row = '''            <tr>
              <td><code>Haste Inox Ø 6 mm</code></td>
              <td>Aço Retificado H6 (L = 85 mm)</td>
              <td>2</td>
              <td>Guias lineares cilíndricas do Empurrador de descarte</td>
            </tr>'''
new_fastener_table_row = '''            <tr>
              <td><code>Haste Inox Ø 6 mm</code></td>
              <td>Aço Retificado H6 (L = 170 mm)</td>
              <td>2</td>
              <td>Guias lineares cilíndricas do Empurrador (entre-centros 85 mm)</td>
            </tr>
            <tr>
              <td><code>Bucha Linear LM6UU</code></td>
              <td>Bucha de Esferas Ø 6 × 12 × 19 mm</td>
              <td>4</td>
              <td>Mancais do pórtico 03E do empurrador (2 por haste espaçadas em 70 mm)</td>
            </tr>
            <tr>
              <td><code>Rolamento 623ZZ</code></td>
              <td>Blindagem Dupla de Aço (3 × 10 × 4 mm)</td>
              <td>2</td>
              <td>Articulações da biela do empurrador (manivela e trave traseira)</td>
            </tr>'''
html = html.replace(old_fastener_table_row, new_fastener_table_row)

# =========================================================================
# 5. SCALE CAD_DATA['caixa'] VERTICES
# =========================================================================
m_cad = re.search(r'const CAD_DATA\s*=\s*(\{.+?\});\n', html)
if m_cad:
    cad_obj = json.loads(m_cad.group(1))
    caixa_verts = cad_obj['caixa']['verts']
    # Scale X from [-76.2, 76.2] to [-76.0, 76.0]
    # Scale Y from [0, 57.15] to [0, 55.0]
    # Scale Z from [-76.2, 76.2] to [-76.0, 76.0]
    new_caixa_verts = []
    for i in range(0, len(caixa_verts), 3):
        x = round(caixa_verts[i] * (76.0 / 76.2), 2)
        y = round(caixa_verts[i+1] * (55.0 / 57.15), 2)
        z = round(caixa_verts[i+2] * (76.0 / 76.2), 2)
        new_caixa_verts.extend([x, y, z])
    cad_obj['caixa']['verts'] = new_caixa_verts
    new_cad_json_str = json.dumps(cad_obj, separators=(',', ':'))
    html = html[:m_cad.start()] + 'const CAD_DATA = ' + new_cad_json_str + ';\n' + html[m_cad.end():]
    print("Scaled CAD_DATA['caixa'] to 152x55x152 mm successfully.")

# =========================================================================
# 6. FUNCTION updatePusherMechanism(progress) (Real Slider-Crank Kinematics)
# =========================================================================
old_pusher_fn = '''    function updatePusherMechanism(progress) {
      const stroke = Math.max(0, Math.min(1, progress));
      if (pusherMovingAssembly) {
        pusherMovingAssembly.position.z = stroke * 118;
      }
      if (pusherCrank) {
        pusherCrank.rotation.y = stroke * Math.PI * 0.52;
      }
      if (pusherRod) {
        pusherRod.position.z = -110 + stroke * 59;
        pusherRod.rotation.y = -Math.sin(stroke * Math.PI) * 0.28;
      }
    }'''

new_pusher_fn = '''    function updatePusherMechanism(progress) {
      const p = Math.max(0, Math.min(1, progress));
      const theta = p * Math.PI;
      const R = 60.0;
      const L = 110.0;

      // Cinemática real do mecanismo biela-manivela (curso 120 mm: 0 em theta=0, 120 mm em theta=PI)
      const sinT = Math.sin(theta);
      const cosT = Math.cos(theta);
      const radTerm = Math.sqrt(Math.max(0, 1.0 - Math.pow((R * sinT) / L, 2)));
      const displacement = R * (1.0 - cosT) + L * (radTerm - 1.0);

      if (pusherMovingAssembly) {
        pusherMovingAssembly.position.z = displacement;
      }
      if (pusherCrank) {
        pusherCrank.rotation.y = theta;
      }
      if (pusherRod) {
        const pinX = R * sinT;
        const pinZ = -132.0 - R * cosT;
        const jointZ = pinZ + L * radTerm;
        pusherRod.position.set(pinX / 2.0, 140.0, (pinZ + jointZ) / 2.0);
        pusherRod.rotation.y = -Math.asin((R / L) * sinT);
      }
    }'''
html = html.replace(old_pusher_fn, new_pusher_fn)

# =========================================================================
# 7. BELT LINK GEOMETRY & PITCH 17.3 mm
# =========================================================================
old_belt_geo = '''      const linkBaseGeo = new THREE.BoxGeometry(22, 4.5, 122);
      // Nervuras transversais antiderrapantes no topo do elo
      const linkRibGeo = new THREE.BoxGeometry(4, 2, 120);

      const totalLoopLen = 650 * 2 + 2 * Math.PI * 30.25;
      const numLinks = 86;
      beltLinks = [];

      for (let i = 0; i < numLinks; i++) {
        const linkGroup = new THREE.Group();

        const body = makeSketchMesh(linkBaseGeo, 0xd97706);
        linkGroup.add(body);

        const rib = makeSketchMesh(linkRibGeo, 0xb45309);
        rib.position.set(0, 3.2, 0);
        linkGroup.add(rib);

        // Charneiras / pinos de articulação de 1.75 mm nas extremidades
        [-10, 10].forEach(px => {
          const pinGeo = new THREE.CylinderGeometry(1.5, 1.5, 122, 8);
          pinGeo.rotateX(Math.PI / 2);
          const pin = makeSketchMesh(pinGeo, 0x78350f);
          pin.position.set(px, 0, 0);
          linkGroup.add(pin);
        });

        beltGroup.add(linkGroup);
        beltLinks.push(linkGroup);
      }'''

new_belt_geo = '''      const linkBaseGeo = new THREE.BoxGeometry(17.3, 4.5, 122);
      // Nervuras transversais antiderrapantes no topo do elo
      const linkRibGeo = new THREE.BoxGeometry(3, 2, 120);

      const totalLoopLen = 650 * 2 + 2 * Math.PI * 30.0;
      const numLinks = 86;
      beltLinks = [];

      for (let i = 0; i < numLinks; i++) {
        const linkGroup = new THREE.Group();

        const body = makeSketchMesh(linkBaseGeo, 0xd97706);
        linkGroup.add(body);

        const rib = makeSketchMesh(linkRibGeo, 0xb45309);
        rib.position.set(0, 3.2, 0);
        linkGroup.add(rib);

        // Pinos de união de filamento PETG 1,75 mm nas charneiras (passo 17,3 mm: centros em +-8,65 mm)
        [-8.65, 8.65].forEach(px => {
          const pinGeo = new THREE.CylinderGeometry(0.875, 0.875, 122, 8);
          pinGeo.rotateX(Math.PI / 2);
          const pin = makeSketchMesh(pinGeo, 0x78350f);
          pin.position.set(px, 0, 0);
          linkGroup.add(pin);
        });

        beltGroup.add(linkGroup);
        beltLinks.push(linkGroup);
      }'''
html = html.replace(old_belt_geo, new_belt_geo)

# =========================================================================
# 8. DOME & WEBCAM HEIGHT (Webcam Y=255, Dome ext height 260, Ring Light Y=215)
# =========================================================================
old_dome_block = '''      // 1. Teto Superior: BoxGeometry(120, 4, 146) em (0, 238, 0)
      createDomePlate(new THREE.BoxGeometry(120, 4, 146), 0, 238, 0);

      // 2. Parede Traseira (-Z): BoxGeometry(120, 115, 4) em (0, 182.5, -71)
      createDomePlate(new THREE.BoxGeometry(120, 115, 4), 0, 182.5, -71);

      // 3. Parede Frontal (+Z) com Recorte Real para Janela de Acrílico:
      // Duas colunas laterais BoxGeometry(15, 115, 4) em X = -52.5 e X = +52.5, Z = 71
      createDomePlate(new THREE.BoxGeometry(15, 115, 4), -52.5, 182.5, 71);
      createDomePlate(new THREE.BoxGeometry(15, 115, 4), 52.5, 182.5, 71);
      // Viga superior BoxGeometry(90, 18, 4) em Y = 231, Z = 71
      createDomePlate(new THREE.BoxGeometry(90, 18, 4), 0, 231, 71);
      // Viga inferior BoxGeometry(90, 17, 4) em Y = 133.5, Z = 71
      createDomePlate(new THREE.BoxGeometry(90, 17, 4), 0, 133.5, 71);

      // 4. Janela Frontal de Acrílico Transparente/Fumê (domeWindowMesh) encaixada no vão de 90 × 80 mm
      const windowMat = new THREE.MeshStandardMaterial({
        color: 0x38bdf8,
        roughness: 0.1,
        metalness: 0.1,
        transparent: true,
        opacity: 0.28
      });
      const windowGeo = new THREE.BoxGeometry(90, 80, 3);
      domeWindowMesh = new THREE.Mesh(windowGeo, windowMat);
      domeWindowMesh.position.set(0, 182.5, 71);
      domeWindowMesh.add(new THREE.LineSegments(new THREE.EdgesGeometry(windowGeo, 20), lineMat));
      visionGroup.add(domeWindowMesh);

      // 5. Abas de Cortina Superior de Entrada (X = -58) e Saída (X = +58)
      // Sanefa superior BoxGeometry(4, 35, 142) em Y = 222.5, deixando o portal de passagem livre de Y = 108 mm até 205 mm!
      createDomePlate(new THREE.BoxGeometry(4, 35, 142), -58, 222.5, 0);
      createDomePlate(new THREE.BoxGeometry(4, 35, 142), 58, 222.5, 0);

      domeMesh = domeShellGroup;

      // Câmera UVC USB 1080p centralizada no topo (Y = 235 mm) apontada para baixo (-Y)
      const camBody = makeSketchMesh(new THREE.BoxGeometry(36, 22, 36), 0x0f172a);
      camBody.position.set(0, 235, 0);
      visionGroup.add(camBody);

      const camLens = makeSketchMesh(new THREE.CylinderGeometry(9, 11, 14, 20), 0x334155);
      camLens.position.set(0, 222, 0);
      visionGroup.add(camLens);

      // Ring Light LED 12V 6000K ao redor da lente + difusor leitoso
      const ringGeo = new THREE.TorusGeometry(20, 4.5, 12, 28);
      ringGeo.rotateX(Math.PI / 2);
      ringLightMesh = new THREE.Mesh(ringGeo, new THREE.MeshStandardMaterial({
        color: 0xffffff,
        emissive: 0xffffff,
        emissiveIntensity: 0.85,
        roughness: 0.2
      }));
      ringLightMesh.position.set(0, 218, 0);
      visionGroup.add(ringLightMesh);'''

new_dome_block = '''      // 1. Teto Superior: BoxGeometry(120, 4, 146) em Y = 258 mm (altura externa total 260 mm)
      createDomePlate(new THREE.BoxGeometry(120, 4, 146), 0, 258, 0);

      // 2. Parede Traseira (-Z): BoxGeometry(120, 135, 4) em (0, 192.5, -71)
      createDomePlate(new THREE.BoxGeometry(120, 135, 4), 0, 192.5, -71);

      // 3. Parede Frontal (+Z) com Recorte Real para Janela de Acrílico:
      createDomePlate(new THREE.BoxGeometry(15, 135, 4), -52.5, 192.5, 71);
      createDomePlate(new THREE.BoxGeometry(15, 135, 4), 52.5, 192.5, 71);
      // Viga superior BoxGeometry(90, 20, 4) em Y = 250, Z = 71
      createDomePlate(new THREE.BoxGeometry(90, 20, 4), 0, 250, 71);
      // Viga inferior BoxGeometry(90, 17, 4) em Y = 133.5, Z = 71
      createDomePlate(new THREE.BoxGeometry(90, 17, 4), 0, 133.5, 71);

      // 4. Janela Frontal de Acrílico Transparente/Fumê encaixada no vão de 90 × 98 mm
      const windowMat = new THREE.MeshStandardMaterial({
        color: 0x38bdf8,
        roughness: 0.1,
        metalness: 0.1,
        transparent: true,
        opacity: 0.28
      });
      const windowGeo = new THREE.BoxGeometry(90, 98, 3);
      domeWindowMesh = new THREE.Mesh(windowGeo, windowMat);
      domeWindowMesh.position.set(0, 192.5, 71);
      domeWindowMesh.add(new THREE.LineSegments(new THREE.EdgesGeometry(windowGeo, 20), lineMat));
      visionGroup.add(domeWindowMesh);

      // 5. Abas de Cortina Superior de Entrada (X = -58) e Saída (X = +58)
      createDomePlate(new THREE.BoxGeometry(4, 45, 142), -58, 237.5, 0);
      createDomePlate(new THREE.BoxGeometry(4, 45, 142), 58, 237.5, 0);

      domeMesh = domeShellGroup;

      // Câmera UVC USB 1080p centralizada no topo (Y = 255 mm) apontada para baixo (-Y)
      const camBody = makeSketchMesh(new THREE.BoxGeometry(36, 22, 36), 0x0f172a);
      camBody.position.set(0, 255, 0);
      visionGroup.add(camBody);

      const camLens = makeSketchMesh(new THREE.CylinderGeometry(9, 11, 14, 20), 0x334155);
      camLens.position.set(0, 242, 0);
      visionGroup.add(camLens);

      // Ring Light LED 12V 6000K ao redor da lente em Y = 215 mm + difusor leitoso 1 mm
      const ringGeo = new THREE.TorusGeometry(20, 4.5, 12, 28);
      ringGeo.rotateX(Math.PI / 2);
      ringLightMesh = new THREE.Mesh(ringGeo, new THREE.MeshStandardMaterial({
        color: 0xffffff,
        emissive: 0xffffff,
        emissiveIntensity: 0.85,
        roughness: 0.2
      }));
      ringLightMesh.position.set(0, 215, 0);
      visionGroup.add(ringLightMesh);'''
html = html.replace(old_dome_block, new_dome_block)

# =========================================================================
# 9. RECTANGULAR SENSOR 3D CONSTRUCTION (Problem 4)
# =========================================================================
old_sensor_block = '''      // 6. SENSORES FOTOELÉTRICOS M18 S1 E S2 (Component 6)
      // -------------------------------------------------------------
      const sensorsGroup = new THREE.Group();
      conveyorRoot.add(sensorsGroup);
      components[6] = sensorsGroup;

      const sensorBracketGeo = buildCADBufferGeometry('suporte_sensor');

      // Helper para construir Estação de Detecção M18 com suporte, feixe e refletor
      function createM18SensorStation(xPos, isS1) {
        const stationSub = new THREE.Group();
        stationSub.position.set(xPos, 0, 0);
        sensorsGroup.add(stationSub);

        // Suporte CAD na face externa da longarina esquerda (Z = -68 a -78 mm)
        const bracket = makeSketchMesh(sensorBracketGeo, 0x334155);
        bracket.position.set(0, 26, -75);
        stationSub.add(bracket);

        // Corpo cilíndrico rosqueado M18 (Ø 18 mm × 50 mm) em Z = -114 mm até Z = -64 mm, Y = 126 mm (fora da correia)
        const m18Geo = new THREE.CylinderGeometry(9, 9, 50, 20);
        m18Geo.rotateX(Math.PI / 2);
        const sensorBody = makeSketchMesh(m18Geo, 0xf59e0b);
        sensorBody.position.set(0, 126, -89);
        stationSub.add(sensorBody);

        // Porcas sextavadas de aperto M18
        [-98, -72].forEach(nz => {
          const nutGeo = new THREE.CylinderGeometry(12, 12, 6, 6);
          nutGeo.rotateX(Math.PI / 2);
          const nut = makeSketchMesh(nutGeo, 0xd97706);
          nut.position.set(0, 126, nz);
          stationSub.add(nut);
        });

        // Lente óptica frontal em Z = -63.5 mm (nivelada com a face interna da guia da correia)
        const lensGeo = new THREE.CylinderGeometry(7, 7, 2, 20);
        lensGeo.rotateX(Math.PI / 2);
        const lens = makeSketchMesh(lensGeo, 0x38bdf8);
        lens.position.set(0, 126, -63.5);
        stationSub.add(lens);

        // LED indicador traseiro em Z = -114 mm
        const ledGeo = new THREE.SphereGeometry(3.5, 14, 14);
        const ledMat = new THREE.MeshStandardMaterial({
          color: 0xef4444,
          emissive: 0xef4444,
          emissiveIntensity: 0.3,
          roughness: 0.2
        });
        const ledMesh = new THREE.Mesh(ledGeo, ledMat);
        ledMesh.position.set(0, 126, -114);
        stationSub.add(ledMesh);

        // Refletor prismático na longarina oposta (Z = +65 mm, Y = 126 mm)
        const reflector = makeSketchMesh(new THREE.BoxGeometry(18, 18, 4), 0xfbbf24);
        reflector.position.set(0, 126, 65);
        stationSub.add(reflector);

        // Feixe laser óptico vermelho translúcido de Z = -62 mm até Z = +62 mm (L = 124 mm, Y = 126 mm)
        const beamGeo = new THREE.CylinderGeometry(1.2, 1.2, 124, 12);
        beamGeo.rotateX(Math.PI / 2);
        const beamMat = new THREE.MeshBasicMaterial({
          color: 0xef4444,
          transparent: true,
          opacity: 0.45
        });
        const beamMesh = new THREE.Mesh(beamGeo, beamMat);
        beamMesh.position.set(0, 126, 0);
        stationSub.add(beamMesh);

        if (isS1) {
          s1BeamMesh = beamMesh;
          s1LedMesh = ledMesh;
        } else {
          s2BeamMesh = beamMesh;
          s2LedMesh = ledMesh;
        }
      }

      // Estação S1 (Gatilho da Câmera) em X = -150 mm
      createM18SensorStation(-150, true);

      // Estação S2 (Gatilho de Sincronismo do Descarte) em X = +100 mm (60 mm antes do Empurrador em X = +160 mm)
      createM18SensorStation(100, false);'''

new_sensor_block = '''      // 6. SENSORES FOTOELÉTRICOS RETANGULARES S1 E S2 (Component 6)
      // -------------------------------------------------------------
      const sensorsGroup = new THREE.Group();
      conveyorRoot.add(sensorsGroup);
      components[6] = sensorsGroup;

      // Helper para construir Estação de Detecção com sensor óptico retangular 5V TTL
      function createSensorStation(xPos, isS1) {
        const stationSub = new THREE.Group();
        stationSub.position.set(xPos, 0, 0);
        sensorsGroup.add(stationSub);

        // Suporte 04A impresso (cavidade 46 × 21 × 16 mm com 2 furos M3 de entre-centros 25 mm)
        const bracket = makeSketchMesh(new THREE.BoxGeometry(26, 32, 50), 0x334155);
        bracket.position.set(0, 80, -84.5);
        stationSub.add(bracket);

        // Corpo retangular do sensor fotoelétrico 5V TTL (corpo 45 × 20 × 15 mm) em laranja
        // Eixo longitudinal alongado em Z (45 mm), largura X (20 mm) e altura Y (15 mm)
        const sensorBody = makeSketchMesh(new THREE.BoxGeometry(20, 15, 45), 0xf97316);
        sensorBody.position.set(0, 90, -84.5);
        stationSub.add(sensorBody);

        // Lente óptica frontal redonda vermelha emissiva SphereGeometry(4) em Z = -62 mm
        const lensGeo = new THREE.SphereGeometry(4, 16, 16);
        const lensMat = new THREE.MeshStandardMaterial({
          color: 0xef4444,
          emissive: 0xef4444,
          emissiveIntensity: 0.6,
          roughness: 0.1
        });
        const lensMesh = new THREE.Mesh(lensGeo, lensMat);
        lensMesh.position.set(0, 90, -62);
        stationSub.add(lensMesh);

        // LED indicador traseiro em Z = -105 mm
        const ledGeo = new THREE.SphereGeometry(2.5, 12, 12);
        const ledMat = new THREE.MeshStandardMaterial({
          color: 0xef4444,
          emissive: 0xef4444,
          emissiveIntensity: 0.3,
          roughness: 0.2
        });
        const ledMesh = new THREE.Mesh(ledGeo, ledMat);
        ledMesh.position.set(0, 95, -105);
        stationSub.add(ledMesh);

        // Refletor prismático na longarina oposta (Z = +65 mm, Y = 90 mm)
        const reflector = makeSketchMesh(new THREE.BoxGeometry(18, 18, 4), 0xfbbf24);
        reflector.position.set(0, 90, 65);
        stationSub.add(reflector);

        // Feixe óptico infravermelho vermelho translúcido na cota Y = 90 mm (ideal para maçã Ø80 mm)
        const beamGeo = new THREE.CylinderGeometry(1.2, 1.2, 124, 12);
        beamGeo.rotateX(Math.PI / 2);
        const beamMat = new THREE.MeshBasicMaterial({
          color: 0xef4444,
          transparent: true,
          opacity: 0.45
        });
        const beamMesh = new THREE.Mesh(beamGeo, beamMat);
        beamMesh.position.set(0, 90, 0);
        stationSub.add(beamMesh);

        if (isS1) {
          s1BeamMesh = beamMesh;
          s1LedMesh = ledMesh;
        } else {
          s2BeamMesh = beamMesh;
          s2LedMesh = ledMesh;
        }
      }

      // Estação S1 (Gatilho da Câmera) em X = -150 mm
      createSensorStation(-150, true);

      // Estação S2 (Gatilho de Sincronismo do Descarte) em X = +100 mm (60 mm antes do Empurrador em X = +160 mm)
      createSensorStation(100, false);'''
html = html.replace(old_sensor_block, new_sensor_block)

# =========================================================================
# 10. PUSHER 3D CONSTRUCT (Problem 2)
# =========================================================================
old_pusher_construct = '''      // 7. EMPURRADOR LINEAR COM SERVO MG996R (Component 7) - X = +160 mm
      // -------------------------------------------------------------
      pusherAssemblyGroup = new THREE.Group();
      pusherAssemblyGroup.position.set(160, 0, 0);
      conveyorRoot.add(pusherAssemblyGroup);
      components[7] = pusherAssemblyGroup;

      // Base fixa montada na face externa da longarina esquerda (Z = -155 mm a -68 mm)
      const pBase = makeSketchMesh(new THREE.BoxGeometry(96, 16, 85), 0x1e293b);
      pBase.position.set(0, 100, -112);
      pusherAssemblyGroup.add(pBase);

      // Mancais fixos de buchas lineares para eixos de guia Ø 8 mm
      [-25, 25].forEach(gx => {
        const block = makeSketchMesh(new THREE.BoxGeometry(18, 24, 45), 0x475569);
        block.position.set(gx, 115, -95);
        pusherAssemblyGroup.add(block);
      });

      // Servomotor MG996R fixado horizontalmente no berço traseiro
      const servoBody = makeSketchMesh(new THREE.BoxGeometry(41, 20, 42), 0x0f172a);
      servoBody.position.set(0, 126, -132);
      pusherAssemblyGroup.add(servoBody);

      // Horn Metálico 25T / Manivela do Servo
      pusherCrank = makeSketchMesh(new THREE.CylinderGeometry(14, 14, 3, 20), 0x0284c7);
      pusherCrank.position.set(0, 140, -132);
      pusherAssemblyGroup.add(pusherCrank);

      // Biela articulada de acoplamento
      pusherRod = makeSketchMesh(new THREE.BoxGeometry(6, 4, 42), 0x94a3b8);
      pusherRod.position.set(0, 138, -110);
      pusherAssemblyGroup.add(pusherRod);

      // GRUPO MÓVEL ÚNICO DO EMPURRADOR (pusherMovingAssembly)
      pusherMovingAssembly = new THREE.Group();
      pusherMovingAssembly.position.set(0, 0, 0);
      pusherAssemblyGroup.add(pusherMovingAssembly);
      pusherShoeGroup = pusherMovingAssembly; // compatibilidade de referência

      // 1. Sapata Defletora Laranja em PETG (90 × 38 × 10 mm)
      // Em repouso (offset Z = 0): face em Z = -62 mm (fora da pista de 122 mm).
      const shoeBody = makeSketchMesh(new THREE.BoxGeometry(90, 38, 10), 0xf97316);
      shoeBody.position.set(0, 115, -62);
      pusherMovingAssembly.add(shoeBody);

      // 2. Almofada Frontal de EVA Preto (86 × 34 × 2 mm) na face de contato
      const evaPad = makeSketchMesh(new THREE.BoxGeometry(86, 34, 2), 0x18181b);
      evaPad.position.set(0, 115, -56);
      pusherMovingAssembly.add(evaPad);

      // 3. Duas Hastes Impulsoras de Aço Inox Ø 8 mm × 135 mm
      // Ancoradas na traseira da sapata e correndo permanentemente através dos mancais lineares
      [-25, 25].forEach(rx => {
        const rodGeo = new THREE.CylinderGeometry(4, 4, 135, 16);
        rodGeo.rotateX(Math.PI / 2);
        const rod = makeSketchMesh(rodGeo, 0xe2e8f0);
        rod.position.set(rx, 115, -129.5);
        pusherMovingAssembly.add(rod);
      });

      // 4. Trave Traseira de Acoplamento unindo as pontas das duas hastes
      const rearTie = makeSketchMesh(new THREE.BoxGeometry(60, 16, 12), 0x334155);
      rearTie.position.set(0, 115, -192);
      pusherMovingAssembly.add(rearTie);'''

new_pusher_construct = '''      // 7. EMPURRADOR LINEAR COM SERVO MG996R (Component 7) - X = +160 mm
      // -------------------------------------------------------------
      pusherAssemblyGroup = new THREE.Group();
      pusherAssemblyGroup.position.set(160, 0, 0);
      conveyorRoot.add(pusherAssemblyGroup);
      components[7] = pusherAssemblyGroup;

      // Pórtico 03E fixo com berço para servo MG996R e 4 buchas LM6UU
      const pBase = makeSketchMesh(new THREE.BoxGeometry(110, 18, 95), 0x1e293b);
      pBase.position.set(0, 100, -112);
      pusherAssemblyGroup.add(pBase);

      // 4 Alojamentos para buchas lineares LM6UU (duas por haste Ø6 mm, entre-centros 85 mm, espaçadas em 70 mm)
      [-42.5, 42.5].forEach(gx => {
        [-130, -60].forEach(gz => {
          const block = makeSketchMesh(new THREE.BoxGeometry(16, 22, 28), 0x475569);
          block.position.set(gx, 115, gz);
          pusherAssemblyGroup.add(block);
        });
      });

      // Servomotor MG996R montado horizontalmente no berço
      const servoBody = makeSketchMesh(new THREE.BoxGeometry(41, 20, 42), 0x0f172a);
      servoBody.position.set(0, 126, -132);
      pusherAssemblyGroup.add(servoBody);

      // Alavanca 03F parafusada no horn 25T: Raio R = 60 mm (pivot em 0, 140, -132)
      pusherCrank = new THREE.Group();
      pusherCrank.position.set(0, 140, -132);
      const hornDisc = makeSketchMesh(new THREE.CylinderGeometry(12, 12, 4, 20), 0x0284c7);
      pusherCrank.add(hornDisc);
      const crankArm = makeSketchMesh(new THREE.BoxGeometry(12, 4, 60), 0x0284c7);
      crankArm.position.set(0, 0, -30);
      pusherCrank.add(crankArm);
      const crankPin = makeSketchMesh(new THREE.CylinderGeometry(3, 3, 8, 12), 0xcfd8dc);
      crankPin.position.set(0, 4, -60);
      pusherCrank.add(crankPin);
      pusherAssemblyGroup.add(pusherCrank);

      // Biela 03G: Comprimento entre centros L = 110 mm com rolamentos 623ZZ
      pusherRod = makeSketchMesh(new THREE.BoxGeometry(8, 5, 110), 0x94a3b8);
      pusherRod.position.set(0, 140, -132 - 60 + 55);
      pusherAssemblyGroup.add(pusherRod);

      // GRUPO MÓVEL ÚNICO DO EMPURRADOR (pusherMovingAssembly)
      pusherMovingAssembly = new THREE.Group();
      pusherMovingAssembly.position.set(0, 0, 0);
      pusherAssemblyGroup.add(pusherMovingAssembly);
      pusherShoeGroup = pusherMovingAssembly;

      // 1. Sapata Côncava 03H (100 × 90 × 12 mm, raio côncavo R = 45 mm para maçã Ø80 mm)
      // Em repouso (offset Z = 0): face em Z = -62 mm (fora da pista de 122 mm).
      const shoeBody = makeSketchMesh(new THREE.BoxGeometry(100, 90, 12), 0xf97316);
      shoeBody.position.set(0, 115, -62);
      pusherMovingAssembly.add(shoeBody);

      // 2. Almofada Frontal de EVA Preto (96 × 86 × 2 mm) na face de contato côncava
      const evaPad = makeSketchMesh(new THREE.BoxGeometry(96, 86, 2), 0x18181b);
      evaPad.position.set(0, 115, -55);
      pusherMovingAssembly.add(evaPad);

      // 3. Duas Hastes Guia de Aço Inox Retificado Ø 6 mm × 170 mm (entre-centros 85 mm)
      [-42.5, 42.5].forEach(rx => {
        const rodGeo = new THREE.CylinderGeometry(3, 3, 170, 16);
        rodGeo.rotateX(Math.PI / 2);
        const rod = makeSketchMesh(rodGeo, 0xe2e8f0);
        rod.position.set(rx, 115, -147);
        pusherMovingAssembly.add(rod);
      });

      // 4. Trave Traseira 03I (90 × 18 × 12 mm) unindo as extremidades traseiras das hastes
      const rearTie = makeSketchMesh(new THREE.BoxGeometry(90, 18, 12), 0x334155);
      rearTie.position.set(0, 115, -232);
      pusherMovingAssembly.add(rearTie);'''
html = html.replace(old_pusher_construct, new_pusher_construct)

# =========================================================================
# 11. RAMPA 18° & CAIXAS 152×152×55 (Problem 7, 9, 10)
# =========================================================================
old_rampa_boxes = '''      // Subgrupo da Calha Inclinada
      const chuteSub = new THREE.Group();
      chuteSub.position.set(160, 80, 124);
      chuteSub.rotation.x = 0.436;
      rampaGroup.add(chuteSub);
      rampaMesh = chuteSub;

      // 1. Chapa de Fundo Deslizante: BoxGeometry(92, 4, 138)
      const chuteBed = makeSketchMesh(new THREE.BoxGeometry(92, 4, 138), 0xf97316);
      chuteBed.position.set(0, 0, 0);
      chuteSub.add(chuteBed);

      // 2. Duas Abas Laterais de Contenção (Guarda-Corpos): BoxGeometry(4, 28, 138)
      [-46, 46].forEach(gx => {
        const chuteWall = makeSketchMesh(new THREE.BoxGeometry(4, 28, 138), 0xd97706);
        chuteWall.position.set(gx, 14, 0);
        chuteSub.add(chuteWall);
      });

      // 3. Pés de Apoio Tubulares da Rampa descendo até o piso (Y = 0 mm)
      [-42, 42].forEach(px => {
        const leg = makeSketchMesh(new THREE.CylinderGeometry(4, 4, 75, 16), 0x94a3b8);
        leg.position.set(160 + px, 37.5, 135);
        rampaGroup.add(leg);
      });

      // -------------------------------------------------------------
      // 9. DUAS CAIXAS COLETORAS CAD (Component 9) - 152 × 152 × 57 mm
      // -------------------------------------------------------------
      const boxesGroup = new THREE.Group();
      conveyorRoot.add(boxesGroup);
      components[9] = boxesGroup;

      const caixaGeo = buildCADBufferGeometry('caixa');

      // Caixa 1: Aprovados (Classe A) - Saída frontal (X = +435 mm, Y = 0 mm, Z = 0 mm)
      // Base perfeitamente apoiada no piso da bancada (Y = 0 mm), abertura para cima (Y = +57.2 mm)
      const caixaApp = makeSketchMesh(caixaGeo, 0x16a34a, 0.95);
      caixaApp.position.set(435, 0, 0);
      boxesGroup.add(caixaApp);

      // Caixa 2: Rejeitados (Classes B/C) - Saída da rampa lateral (X = +160 mm, Y = 0 mm, Z = +190 mm)
      const caixaRej = makeSketchMesh(caixaGeo, 0xd97706, 0.95);
      caixaRej.position.set(160, 0, 190);
      boxesGroup.add(caixaRej);'''

new_rampa_boxes = '''      // Subgrupo da Calha Inclinada suave a 18° (rotation.x = 0.314 rad) para rolamento de maçã
      const chuteSub = new THREE.Group();
      chuteSub.position.set(160, 78, 124);
      chuteSub.rotation.x = 0.314;
      rampaGroup.add(chuteSub);
      rampaMesh = chuteSub;

      // 1. Chapa de Fundo Deslizante: BoxGeometry(96, 4, 140)
      const chuteBed = makeSketchMesh(new THREE.BoxGeometry(96, 4, 140), 0xf97316);
      chuteBed.position.set(0, 0, 0);
      chuteSub.add(chuteBed);

      // 2. Duas Abas Laterais de Contenção (Guarda-Corpos): BoxGeometry(4, 30, 140)
      [-48, 48].forEach(gx => {
        const chuteWall = makeSketchMesh(new THREE.BoxGeometry(4, 30, 140), 0xd97706);
        chuteWall.position.set(gx, 15, 0);
        chuteSub.add(chuteWall);
      });

      // 3. Aba defletora em EVA 3 mm (120 × 30 × 3 mm) colada na borda final da rampa
      const defletorEva = makeSketchMesh(new THREE.BoxGeometry(100, 3, 25), 0x18181b);
      defletorEva.position.set(0, 2, 70);
      chuteSub.add(defletorEva);

      // 4. Pés de Apoio Tubulares da Rampa descendo até o piso (Y = 0 mm)
      [-42, 42].forEach(px => {
        const leg = makeSketchMesh(new THREE.CylinderGeometry(4, 4, 75, 16), 0x94a3b8);
        leg.position.set(160 + px, 37.5, 135);
        rampaGroup.add(leg);
      });

      // -------------------------------------------------------------
      // 9. DUAS CAIXAS COLETORAS (Component 9) - 152 × 152 × 55 mm
      // -------------------------------------------------------------
      const boxesGroup = new THREE.Group();
      conveyorRoot.add(boxesGroup);
      components[9] = boxesGroup;

      const caixaGeo = buildCADBufferGeometry('caixa');

      // Caixa 1: Aprovados (Classe A) - Saída frontal (X = +375 mm, Y = 0 mm, Z = 0 mm)
      const caixaApp = makeSketchMesh(caixaGeo, 0x16a34a, 0.95);
      caixaApp.position.set(375, 0, 0);
      boxesGroup.add(caixaApp);

      // Caixa 2: Rejeitados (Classes B/C) - Saída da rampa lateral (X = +160 mm, Y = 0 mm, Z = +190 mm)
      const caixaRej = makeSketchMesh(caixaGeo, 0xd97706, 0.95);
      caixaRej.position.set(160, 0, 190);
      boxesGroup.add(caixaRej);'''
html = html.replace(old_rampa_boxes, new_rampa_boxes)

# =========================================================================
# 12. DIMENSIONS & SIMULATION CYCLE (Problems 1, 2, 3, 9)
# =========================================================================
# Cota curso
html = html.replace(
    "dimensionsGroup.add(createDimLine([160, 138, -62], [160, 138, 53], '115 mm (Curso)', [0, -20, 0]));",
    "dimensionsGroup.add(createDimLine([160, 138, -62], [160, 138, 58], '120 mm (Curso)', [0, -20, 0]));"
)

# Fruto de Simulação: Maçã Ø80 mm
old_fruit_mesh = '''      // FRUTO DE SIMULAÇÃO (Castanha / Tucumã / Maçã)
      // -------------------------------------------------------------
      const fruitGeo = new THREE.SphereGeometry(15, 24, 24);
      fruitMesh = makeSketchMesh(fruitGeo, 0xf59e0b);
      fruitMesh.position.set(-330, 127.5, 0); // apoiada na correia (112.5 + 15 mm)
      fruitMesh.visible = false;
      conveyorRoot.add(fruitMesh);'''

new_fruit_mesh = '''      // FRUTO DE SIMULAÇÃO (Maçã de Referência Ø80 mm · Altura 75 mm · 220 g)
      // -------------------------------------------------------------
      const fruitGeo = new THREE.SphereGeometry(40, 24, 24);
      fruitMesh = makeSketchMesh(fruitGeo, 0xdc2626);
      fruitMesh.position.set(-330, 152.5, 0); // apoiada na correia (112.5 + 40 mm)
      fruitMesh.visible = false;
      conveyorRoot.add(fruitMesh);'''
html = html.replace(old_fruit_mesh, new_fruit_mesh)

# Balões 1 a 10
html = html.replace('1: Chassi Modular 700mm (14 Módulos PETG)', '1: Chassi Modular 700mm (13 Mesas P2S)')
html = html.replace('2: Correia Modular (86 Elos · 122mm Útil)', '2: Correia Modular (86 Elos · Passo 17,3mm · 122mm)')
html = html.replace('6: Sensores M18 S1 e S2 (Gatilhos 24V)', '6: Sensores Ópticos Retangulares S1 e S2 (5V TTL)')
html = html.replace('7: Empurrador Linear MG996R (Curso 115mm)', '7: Empurrador Linear MG996R (Curso 120mm)')
html = html.replace('8: Rampa Lateral de Rejeitados (89,4mm)', '8: Rampa Lateral Suave 18° com Defletor EVA')
html = html.replace('9: Caixas Coletoras (Piso Y = 0 mm)', '9: Caixas Coletoras 152×152×55mm (Piso Y = 0 mm)')
html = html.replace('10: Motorredutor DC 12V & Transmissão GT2', '10: Motorredutor GA37 60 RPM & Transmissão GT2')

# updateSimulationCycle
old_sim_cycle = '''      function updateSimulationCycle(dt) {
        if (!fruitMesh) return;

        if (simCycle.stage === 'feed') {
          simCycle.fruitX += 160 * dt;
          fruitMesh.position.set(simCycle.fruitX, 127.5, 0);

          if (simCycle.fruitX >= -150) {
            simCycle.fruitX = -150;
            fruitMesh.position.x = -150;
            simCycle.stage = 'inspect_pause';
            simCycle.t = 0;
            isBeltRunning = false;
            setS1Active(true);
            selectComponent(5);
            selectComponent(6);

            if (ringLightMesh) ringLightMesh.material.emissiveIntensity = 2.8;

            const statusEl = document.getElementById('actionStatus');
            if (statusEl) {
              statusEl.innerHTML = `<span style="color: var(--emerald); font-weight: 800;">Sensor S1 Acionado (X = -150 mm):</span> Esteira pausa. Cúpula bloqueia luz externa. Ring Light LED 6000K dispara flash e Câmera USB 1080p captura imagem de alta resolução!`;
            }
          }
        } else if (simCycle.stage === 'inspect_pause') {
          simCycle.t += dt;
          if (simCycle.t >= 0.35 && ringLightMesh) {
            ringLightMesh.material.emissiveIntensity = 0.85;
          }
          if (simCycle.t >= 0.7) {
            setS1Active(false);
            isBeltRunning = true;
            const isApp = (simCycle.mode === 'approved');
            const statusEl = document.getElementById('actionStatus');
            if (statusEl) {
              if (isApp) {
                statusEl.innerHTML = `<span style="color: var(--emerald); font-weight: 800;">Decisão da IA: CLASSE A (Aprovado).</span> Fruto sem anomalias. Liberação para passagem direta até a Caixa Frontal.`;
              } else {
                statusEl.innerHTML = `<span style="color: var(--accent); font-weight: 800;">Decisão da IA: CLASSE B/C (Defeituoso).</span> Anomalia detectada. Destino programado: Descarte Lateral via Empurrador Linear.`;
              }
            }
            simCycle.stage = 'convey_to_s2';
          }
        } else if (simCycle.stage === 'convey_to_s2') {
          simCycle.fruitX += 160 * dt;
          fruitMesh.position.set(simCycle.fruitX, 127.5, 0);

          if (simCycle.fruitX >= 90 && simCycle.fruitX <= 110) {
            setS2Active(true);
            selectComponent(6);
            const statusEl = document.getElementById('actionStatus');
            if (statusEl) {
              statusEl.innerHTML = `<strong>Sensor S2 Acionado (X = +100 mm):</strong> Sincronismo óptico confirmado a exatamente 60 mm antes do Empurrador Linear.`;
            }
          } else if (simCycle.fruitX > 115) {
            setS2Active(false);
          }

          if (simCycle.fruitX >= 160) {
            simCycle.fruitX = 160;
            fruitMesh.position.x = 160;
            if (simCycle.mode === 'rejected') {
              simCycle.stage = 'push_stroke';
              simCycle.t = 0;
              selectComponent(7);
              selectComponent(8);
              const statusEl = document.getElementById('actionStatus');
              if (statusEl) {
                statusEl.innerHTML = `<span style="color: var(--accent); font-weight: 800;">DESCARTE ATIVADO (X = +160 mm):</span> Servo MG996R atua rapidamente. Sapata avança 118 mm, empurrando o fruto pelo vão de 100 mm para a Rampa de Rejeição!`;
              }
            } else {
              simCycle.stage = 'convey_to_front';
              const statusEl = document.getElementById('actionStatus');
              if (statusEl) {
                statusEl.innerHTML = `<strong>Passagem Livre (X = +160 mm):</strong> Empurrador recolhido em Z = -62 mm. Fruto Classe A segue reto pela pista de 122 mm.`;
              }
            }
          }
        } else if (simCycle.stage === 'push_stroke') {
          simCycle.t += dt;
          const pushDuration = 0.65;
          const norm = simCycle.t / pushDuration;

          if (norm <= 0.5) {
            const p = norm / 0.5;
            simCycle.pusherVal = p;
            fruitMesh.position.z = p * 62;
          } else if (norm <= 1.0) {
            const p = 1.0 - (norm - 0.5) / 0.5;
            simCycle.pusherVal = p;
            fruitMesh.position.z = 62;
          } else {
            simCycle.pusherVal = 0;
            simCycle.stage = 'slide_ramp';
            simCycle.t = 0;
          }
          updatePusherMechanism(simCycle.pusherVal);
        } else if (simCycle.stage === 'slide_ramp') {
          simCycle.t += dt;
          const slideDuration = 0.75;
          const r = Math.min(1.0, simCycle.t / slideDuration);
          fruitMesh.position.x = 160;
          fruitMesh.position.z = 62 + r * (190 - 62);
          fruitMesh.position.y = 127.5 - r * (127.5 - 25);

          if (r >= 1.0) {
            fruitMesh.position.set(160, 25, 190);
            simCycle.stage = 'box_rest';
            simCycle.t = 0;
            selectComponent(9);
            const statusEl = document.getElementById('actionStatus');
            if (statusEl) {
              statusEl.innerHTML = `<span style="color: var(--accent); font-weight: 800;">[SUCESSO]</span> Fruto rejeitado recolhido com segurança na <strong>Caixa de Rejeitados (Lateral, Y = 0 mm)</strong>. Sistema pronto.`;
            }
          }
        } else if (simCycle.stage === 'convey_to_front') {
          simCycle.fruitX += 160 * dt;
          fruitMesh.position.set(simCycle.fruitX, 127.5, 0);

          if (simCycle.fruitX >= 350) {
            simCycle.stage = 'fall_parabola';
            simCycle.t = 0;
          }
        } else if (simCycle.stage === 'fall_parabola') {
          simCycle.t += dt;
          const fallDuration = 0.55;
          const f = Math.min(1.0, simCycle.t / fallDuration);
          fruitMesh.position.x = 350 + f * (435 - 350);
          fruitMesh.position.y = 127.5 - Math.pow(f, 1.8) * (127.5 - 25);
          fruitMesh.position.z = 0;

          if (f >= 1.0) {
            fruitMesh.position.set(435, 25, 0);
            simCycle.stage = 'box_rest';
            simCycle.t = 0;
            selectComponent(9);
            const statusEl = document.getElementById('actionStatus');
            if (statusEl) {
              statusEl.innerHTML = `<span style="color: var(--emerald); font-weight: 800;">[SUCESSO]</span> Fruto Classe A conduzido suavemente para a <strong>Caixa de Aprovados (Frontal, Y = 0 mm)</strong>. Máquina pronta.`;
            }
          }
        } else if (simCycle.stage === 'box_rest') {
          simCycle.t += dt;
          if (simCycle.t >= 4.0) {
            simCycle.active = false;
          }
        }
      }'''

new_sim_cycle = '''      function updateSimulationCycle(dt) {
        if (!fruitMesh) return;

        // Velocidade oficial do sistema: 94 mm/s (motorredutor GA37 60 RPM + GT2 2:1 -> 30 RPM no tambor Ø60 mm)
        const vBelt = 94.0;

        if (simCycle.stage === 'feed') {
          simCycle.fruitX += vBelt * dt;
          fruitMesh.position.set(simCycle.fruitX, 152.5, 0);

          if (simCycle.fruitX >= -150) {
            simCycle.fruitX = -150;
            fruitMesh.position.x = -150;
            simCycle.stage = 'inspect_pause';
            simCycle.t = 0;
            isBeltRunning = false;
            setS1Active(true);
            selectComponent(5);
            selectComponent(6);

            if (ringLightMesh) ringLightMesh.material.emissiveIntensity = 2.8;

            const statusEl = document.getElementById('actionStatus');
            if (statusEl) {
              statusEl.innerHTML = `<span style="color: var(--emerald); font-weight: 800;">Sensor S1 Acionado (X = -150 mm, Y = 90 mm):</span> Esteira pausa. Cúpula óptica 260 mm bloqueia luz ambiente. Ring Light 6000K (Y = 215 mm) dispara flash e Câmera 1080p (Y = 255 mm) captura imagem de alta resolução da Maçã Ø80 mm!`;
            }
          }
        } else if (simCycle.stage === 'inspect_pause') {
          simCycle.t += dt;
          if (simCycle.t >= 0.35 && ringLightMesh) {
            ringLightMesh.material.emissiveIntensity = 0.85;
          }
          if (simCycle.t >= 0.7) {
            setS1Active(false);
            isBeltRunning = true;
            const isApp = (simCycle.mode === 'approved');
            const statusEl = document.getElementById('actionStatus');
            if (statusEl) {
              if (isApp) {
                statusEl.innerHTML = `<span style="color: var(--emerald); font-weight: 800;">Decisão da IA: CLASSE A (Aprovada).</span> Maçã sem anomalias. Velocidade 94 mm/s retomada. Destino: Caixa Frontal em X = +375 mm.`;
              } else {
                statusEl.innerHTML = `<span style="color: var(--accent); font-weight: 800;">Decisão da IA: CLASSE B/C (Defeituosa).</span> Anomalia detectada. Destino programado: Descarte Lateral via Empurrador Linear em X = +160 mm.`;
              }
            }
            simCycle.stage = 'convey_to_s2';
          }
        } else if (simCycle.stage === 'convey_to_s2') {
          simCycle.fruitX += vBelt * dt;
          fruitMesh.position.set(simCycle.fruitX, 152.5, 0);

          if (simCycle.fruitX >= 90 && simCycle.fruitX <= 110) {
            setS2Active(true);
            selectComponent(6);
            const statusEl = document.getElementById('actionStatus');
            if (statusEl) {
              statusEl.innerHTML = `<strong>Sensor S2 Acionado (X = +100 mm):</strong> Sincronismo óptico TTL 5V confirmado a exatamente 60 mm antes do Empurrador Linear (tempo restante: 0,64 s).`;
            }
          } else if (simCycle.fruitX > 115) {
            setS2Active(false);
          }

          if (simCycle.fruitX >= 160) {
            simCycle.fruitX = 160;
            fruitMesh.position.x = 160;
            if (simCycle.mode === 'rejected') {
              simCycle.stage = 'push_stroke';
              simCycle.t = 0;
              selectComponent(7);
              selectComponent(8);
              const statusEl = document.getElementById('actionStatus');
              if (statusEl) {
                statusEl.innerHTML = `<span style="color: var(--accent); font-weight: 800;">DESCARTE ATIVADO (X = +160 mm):</span> Servo MG996R aciona manivela-biela (~0,45 s). Sapata 03H (100×90 mm) avança 120 mm, empurrando a maçã pela rampa 18° com defletor EVA 3 mm!`;
              }
            } else {
              simCycle.stage = 'convey_to_front';
              const statusEl = document.getElementById('actionStatus');
              if (statusEl) {
                statusEl.innerHTML = `<strong>Passagem Livre (X = +160 mm):</strong> Empurrador recolhido em Z = -62 mm. Maçã Classe A segue reto pela pista de 122 mm a 94 mm/s.`;
              }
            }
          }
        } else if (simCycle.stage === 'push_stroke') {
          simCycle.t += dt;
          const strokeTime = 0.45; // ~0,45 s em 6 V com carga
          const totalDuration = strokeTime * 2.0;
          const norm = simCycle.t / totalDuration;

          if (norm <= 0.5) {
            const p = norm / 0.5;
            simCycle.pusherVal = p;
            fruitMesh.position.z = p * 62;
          } else if (norm <= 1.0) {
            const p = 1.0 - (norm - 0.5) / 0.5;
            simCycle.pusherVal = p;
            fruitMesh.position.z = 62;
          } else {
            simCycle.pusherVal = 0;
            simCycle.stage = 'slide_ramp';
            simCycle.t = 0;
          }
          updatePusherMechanism(simCycle.pusherVal);
        } else if (simCycle.stage === 'slide_ramp') {
          simCycle.t += dt;
          const slideDuration = 0.75;
          const r = Math.min(1.0, simCycle.t / slideDuration);
          fruitMesh.position.x = 160;
          fruitMesh.position.z = 62 + r * (190 - 62);
          fruitMesh.position.y = 152.5 - r * (152.5 - 40);

          if (r >= 1.0) {
            fruitMesh.position.set(160, 40, 190);
            simCycle.stage = 'box_rest';
            simCycle.t = 0;
            selectComponent(9);
            const statusEl = document.getElementById('actionStatus');
            if (statusEl) {
              statusEl.innerHTML = `<span style="color: var(--accent); font-weight: 800;">[SUCESSO]</span> Maçã rejeitada acomodada com segurança na <strong>Caixa de Rejeitados (Lateral, 152×152×55 mm, Y = 0 mm)</strong>. Sistema pronto.`;
            }
          }
        } else if (simCycle.stage === 'convey_to_front') {
          simCycle.fruitX += vBelt * dt;
          fruitMesh.position.set(simCycle.fruitX, 152.5, 0);

          if (simCycle.fruitX >= 325) {
            simCycle.stage = 'fall_parabola';
            simCycle.t = 0;
          }
        } else if (simCycle.stage === 'fall_parabola') {
          simCycle.t += dt;
          const fallDuration = 0.53; // Trajetória parabólica de 50 mm (de X = 325 mm até X = 375 mm)
          const f = Math.min(1.0, simCycle.t / fallDuration);
          fruitMesh.position.x = 325 + f * 50;
          fruitMesh.position.y = 152.5 - Math.pow(f, 1.8) * (152.5 - 40);
          fruitMesh.position.z = 0;

          if (f >= 1.0) {
            fruitMesh.position.set(375, 40, 0);
            simCycle.stage = 'box_rest';
            simCycle.t = 0;
            selectComponent(9);
            const statusEl = document.getElementById('actionStatus');
            if (statusEl) {
              statusEl.innerHTML = `<span style="color: var(--emerald); font-weight: 800;">[SUCESSO]</span> Maçã Classe A conduzida com precisão para a <strong>Caixa de Aprovados (Frontal, X = +375 mm, 152×152×55 mm)</strong>. Máquina pronta.`;
            }
          }
        } else if (simCycle.stage === 'box_rest') {
          simCycle.t += dt;
          if (simCycle.t >= 4.0) {
            simCycle.active = false;
          }
        }
      }'''
html = html.replace(old_sim_cycle, new_sim_cycle)

# toggleBeltMotor, triggerPusherTest, runFullCycle
old_controls = '''    // Toggle Motor
    function toggleBeltMotor() {
      isBeltRunning = !isBeltRunning;
      const btn = document.getElementById('btnMotor');
      const statusEl = document.getElementById('actionStatus');
      if (isBeltRunning) {
        btn.textContent = '⏹️ Parar Correia';
        btn.style.borderColor = 'var(--accent)';
        btn.style.color = 'var(--accent)';
        statusEl.innerHTML = `<strong>Motorredutor DC 12V LIGADO:</strong> Tração ativa via correia GT2 fechada (redução 2:1). Velocidade tangencial nominal: 60 mm/s.`;
      } else {
        btn.textContent = '🔄 Ligar Correia';
        btn.style.borderColor = 'var(--emerald)';
        btn.style.color = 'var(--emerald)';
        statusEl.innerHTML = `<strong>Motorredutor DC 12V DESLIGADO:</strong> Sistema em pausa operacional na bancada.`;
      }
    }

    // Teste de Atuação do Empurrador Linear
    function triggerPusherTest() {
      if (pusherTestState.active || simCycle.active) return;
      pusherTestState.active = true;
      pusherTestState.progress = 0;
      pusherTestState.dir = 1;
      const statusEl = document.getElementById('actionStatus');
      if (statusEl) {
        statusEl.innerHTML = `<span style="color: var(--accent); font-weight: 800;">⚡ TESTE DE ATUAÇÃO LINEAR:</span> Servomotor MG996R aciona manivela e biela, avançando as hastes Ø 8 mm e sapata em curso de 118 mm...`;
      }
    }

    // Simulação Completa de Ciclo Operacional a 60 FPS
    function runFullCycle(decision) {
      if (pusherTestState.active) pusherTestState.active = false;
      simCycle.active = true;
      simCycle.mode = decision;
      simCycle.stage = 'feed';
      simCycle.t = 0;
      simCycle.fruitX = -340;
      simCycle.fruitY = 127.5;
      simCycle.fruitZ = 0;
      simCycle.pusherVal = 0;
      updatePusherMechanism(0);
      setS1Active(false);
      setS2Active(false);

      if (fruitMesh) {
        fruitMesh.visible = true;
        fruitMesh.position.set(simCycle.fruitX, simCycle.fruitY, simCycle.fruitZ);
      }
      isBeltRunning = true;

      const statusEl = document.getElementById('actionStatus');
      if (statusEl) {
        statusEl.innerHTML = `<span style="color: var(--accent); font-weight: 800;">[ENTRADA]</span> Fruto alimentado na cabeceira da esteira (X = -350 mm). Condução em direção à Cúpula de Inspeção...`;
      }
    }'''

new_controls = '''    // Toggle Motor
    function toggleBeltMotor() {
      isBeltRunning = !isBeltRunning;
      const btn = document.getElementById('btnMotor');
      const statusEl = document.getElementById('actionStatus');
      if (isBeltRunning) {
        btn.textContent = '⏹️ Parar Correia';
        btn.style.borderColor = 'var(--accent)';
        btn.style.color = 'var(--accent)';
        statusEl.innerHTML = `<strong>Motorredutor GA37 12V 60 RPM LIGADO:</strong> Tração ativa via correia GT2 fechada (redução 2:1, 30 RPM no tambor Ø60 mm). Velocidade tangencial oficial: 94 mm/s.`;
      } else {
        btn.textContent = '🔄 Ligar Correia';
        btn.style.borderColor = 'var(--emerald)';
        btn.style.color = 'var(--emerald)';
        statusEl.innerHTML = `<strong>Motorredutor GA37 12V DESLIGADO:</strong> Sistema em pausa operacional na bancada.`;
      }
    }

    // Teste de Atuação do Empurrador Linear
    function triggerPusherTest() {
      if (pusherTestState.active || simCycle.active) return;
      pusherTestState.active = true;
      pusherTestState.progress = 0;
      pusherTestState.dir = 1;
      const statusEl = document.getElementById('actionStatus');
      if (statusEl) {
        statusEl.innerHTML = `<span style="color: var(--accent); font-weight: 800;">⚡ TESTE DE ATUAÇÃO LINEAR:</span> Servomotor MG996R aciona manivela R=60 mm e biela L=110 mm, avançando as hastes inox Ø 6 × 170 mm e sapata 03H (100×90 mm) em curso de 120 mm...`;
      }
    }

    // Simulação Completa de Ciclo Operacional a 60 FPS
    function runFullCycle(decision) {
      if (pusherTestState.active) pusherTestState.active = false;
      simCycle.active = true;
      simCycle.mode = decision;
      simCycle.stage = 'feed';
      simCycle.t = 0;
      simCycle.fruitX = -340;
      simCycle.fruitY = 152.5;
      simCycle.fruitZ = 0;
      simCycle.pusherVal = 0;
      updatePusherMechanism(0);
      setS1Active(false);
      setS2Active(false);

      if (fruitMesh) {
        fruitMesh.visible = true;
        fruitMesh.position.set(simCycle.fruitX, simCycle.fruitY, simCycle.fruitZ);
      }
      isBeltRunning = true;

      const statusEl = document.getElementById('actionStatus');
      if (statusEl) {
        statusEl.innerHTML = `<span style="color: var(--accent); font-weight: 800;">[ENTRADA]</span> Maçã Ø80 mm (220 g) alimentada na cabeceira da esteira (X = -350 mm). Condução a 94 mm/s em direção à Cúpula de Inspeção...`;
      }
    }'''
html = html.replace(old_controls, new_controls)

# =========================================================================
# 13. ASSEMBLY STEP DATA (Etapas 1, 4, 5, 6, 7)
# =========================================================================
old_steps = '''    const assemblyStepData = {
      1: {
        title: "Etapa 1: Montagem e Alinhamento do Chassi Modular em PETG",
        desc: "Una os 7 módulos da longarina esquerda e os 7 módulos da longarina direita utilizando as flanges tipo macho-fêmea. Aperte os parafusos M4×16 mm com porcas autotravantes Nyloc (torque de 1,8 N·m). Instale a mesa central de deslizamento (bedPlate) em Y = 105 mm. Verifique o esquadro e o vão livre de descarte entre X = +110 e +210 mm.",
        tools: "Chave Allen 3 mm · Chave Fixa 7 mm · Esquadro Técnico Metálico",
        comps: [1],
        camPos: [0, 350, 650],
        camTarget: [0, 85, 0]
      },
      2: {
        title: "Etapa 2: Instalação dos Pés Estruturais e Sapatas Antivibração",
        desc: "Fixe os 4 pares de pés estruturais nas longarinas nas posições X = -310, -100, +100 e +310 mm utilizando parafusos M4×20 mm. Encaixe as travessas de união transversal inferior e rosqueie as 8 sapatas antivibração de borracha na base (Y = 0 mm), nivelando a bancada.",
        tools: "Chave Allen 3 mm · Nível de Bolha Torpedo",
        comps: [1],
        camPos: [0, 150, 650],
        camTarget: [0, 35, 0]
      },
      3: {
        title: "Etapa 3: Instalação dos Eixos Inox, Rolamentos 608ZZ e Tambores Ø 60",
        desc: "Pressione os 4 rolamentos blindados 608ZZ nos mancais das longarinas. Insira o eixo de aço inox Ø 8 × 160 mm no Tambor Livre traseiro (X = -325 mm) e o eixo Ø 8 × 185 mm no Tambor Tracionador dianteiro (X = +325 mm), garantindo que a ponta do eixo tracionador se projete para a face esquerda (Z = -95 mm).",
        tools: "Martelo de Borracha · Paquímetro Digital · Anéis Elásticos Trava",
        comps: [3],
        camPos: [250, 220, 350],
        camTarget: [0, 80, 0]
      },
      4: {
        title: "Etapa 4: Montagem do Sistema Tensor M5 e Correia de 86 Elos",
        desc: "Insira os blocos mancais deslizantes nos rasgos oblongos de 24 mm na cabeceira traseira e rosqueie os parafusos tensores M5×40 mm. Monte os 86 elos articulados da correia (elo.model: 122 mm) passando os pinos de filamento de 1,75 mm. Feche o circuito ao redor dos tambores e tensione uniformemente em ambos os lados.",
        tools: "Chave Fixa 8 mm · Alicate de Bico Fino para Pinos",
        comps: [2, 4],
        camPos: [-300, 250, 350],
        camTarget: [-300, 95, 0]
      },
      5: {
        title: "Etapa 5: Suporte Metálico, Motorredutor DC 12V e Transmissão GT2",
        desc: "Fixe o suporte metálico em L na longarina esquerda (X = +285 mm, Y = 52 mm, Z = -75 mm) com 4 parafusos M3. Acople a polia motora GT2 20T no eixo Ø 6 mm do motor e a polia movida 40T no eixo do tambor tracionador (plano Z = -88 mm). Instale a correia GT2 fechada (largura 6 mm) assegurando alinhamento e tensão adequados.",
        tools: "Chave Allen 2 mm (parafuso sem cabeça) · Chave Allen 2,5 mm",
        comps: [10, 3],
        camPos: [320, 180, -320],
        camTarget: [305, 65, -80]
      },
      6: {
        title: "Etapa 6: Cúpula de Inspeção, Câmera 1080p, Ring Light e Sensores M18",
        desc: "Encaixe a cúpula em túnel de PETG preto cobrindo X = -210 a -90 mm e fixe a janela de acrílico fumê. Monte a Câmera USB 1080p no topo (Y = 235 mm) e o Ring Light 12V 6000K com difusor. Fixe os suportes verticais de sensores na longarina esquerda e rosqueie os sensores ópticos M18 S1 (X = -150 mm) e S2 (X = +100 mm) alinhados na altura do feixe em Y = 124 mm.",
        tools: "Chave Fixa 24 mm (Porcas M18) · Chave Phillips PH1",
        comps: [5, 6],
        camPos: [-120, 260, 380],
        camTarget: [-120, 140, 0]
      },
      7: {
        title: "Etapa 7: Empurrador Linear MG996R, Rampa Lateral e Caixas Coletoras",
        desc: "Monte o pórtico do Empurrador Linear em X = +160 mm com as duas guias cilíndricas Ø 6 mm e buchas. Fixe o servo MG996R e conecte a biela articulada ao carro com a sapata côncava (recuo em Z = -62 mm). Encaixe a Rampa Lateral de Rejeitados no vão direito (descendo de Y = 108 para 55 mm). Posicione a Caixa de Aprovados na saída frontal (X = +435 mm, Y = 0) e a de Rejeitados na lateral (X = +160 mm, Z = +190 mm, Y = 0).",
        tools: "Chave Allen 2,5 mm · Chave Phillips PH1 · Chave Fixa 5,5 mm",
        comps: [7, 8, 9],
        camPos: [160, 260, 380],
        camTarget: [160, 90, 80]
      }
    };'''

new_steps = '''    const assemblyStepData = {
      1: {
        title: "Etapa 1: Montagem e Alinhamento do Chassi Modular em PETG",
        desc: "Una as peças das longarinas esquerda e direita (Mesas 01 a 04 da Bambu Lab P2S) utilizando parafusos M4×16 mm e porcas autotravantes Nyloc (torque de 1,8 N·m). Instale a mesa central de deslizamento (01G) em Y = 105 mm. Verifique o alinhamento de 700 mm e certifique-se de que o vão de descarte entre X = +110 e +210 mm está perfeitamente desobstruído.",
        tools: "Chave Allen 3 mm · Chave Fixa 7 mm · Esquadro Técnico Metálico",
        comps: [1],
        camPos: [0, 350, 650],
        camTarget: [0, 85, 0]
      },
      2: {
        title: "Etapa 2: Instalação dos Pés Estruturais e Sapatas Antivibração",
        desc: "Fixe os 8 pés estruturais perfil H (01K) nas longarinas nas posições X = -310, -100, +100 e +310 mm utilizando parafusos M4×20 mm. Encaixe as travessas treliçadas (01H) e pressione as 8 sapatas antivibração em TPU 95A (07A) na cavidade inferior 32×22 mm (Y = 0 mm), nivelando a bancada.",
        tools: "Chave Allen 3 mm · Nível de Bolha Torpedo",
        comps: [1],
        camPos: [0, 150, 650],
        camTarget: [0, 35, 0]
      },
      3: {
        title: "Etapa 3: Instalação dos Eixos Inox, Rolamentos 608ZZ e Tambores Ø 60",
        desc: "Pressione os 4 rolamentos blindados 608ZZ nos mancais das longarinas. Insira o eixo de aço inox Ø 8 × 160 mm no Tambor Livre traseiro 02B (X = -325 mm) e o eixo Ø 8 × 185 mm no Tambor Tracionador 02A (X = +325 mm), projetando a ponta para acoplamento da polia GT2 40T.",
        tools: "Martelo de Borracha · Paquímetro Digital · Anéis Elásticos Trava",
        comps: [3],
        camPos: [250, 220, 350],
        camTarget: [0, 80, 0]
      },
      4: {
        title: "Etapa 4: Montagem do Sistema Tensor M5 e Correia Modular Passo 17,3 mm",
        desc: "Insira os mancais deslizantes 02D nos rasgos oblongos de 24 mm na cabeceira traseira e rosqueie os parafusos tensores M5×40 mm. Conecte os 86 elos articulados de passo 17,3 mm (Mesa 06) passando segmentos de filamento PETG de 1,75 mm. Feche o circuito de 1488,5 mm e ajuste a tensão uniforme bilateralmente (flecha <= 8 mm).",
        tools: "Chave Fixa 8 mm · Alicate de Bico Fino para Pinos",
        comps: [2, 4],
        camPos: [-300, 250, 350],
        camTarget: [-300, 95, 0]
      },
      5: {
        title: "Etapa 5: Suporte 03A, Motorredutor GA37 60 RPM e Transmissão GT2",
        desc: "Fixe o motorredutor GA37 12V 60 RPM no suporte 03A na longarina esquerda com parafusos M3×8 mm. Acople a polia motora GT2 20T no eixo Ø 6 mm do motor e a polia movida 40T no eixo do tambor tracionador (redução 2:1, gerando 30 RPM e velocidade oficial de 94 mm/s). Instale a correia GT2 fechada (largura 6 mm) e feche com a carenagem 03D.",
        tools: "Chave Allen 2 mm (parafuso sem cabeça) · Chave Allen 2,5 mm",
        comps: [10, 3],
        camPos: [320, 180, -320],
        camTarget: [305, 65, -80]
      },
      6: {
        title: "Etapa 6: Cúpula 260mm, Câmera 1080p, Ring Light e Sensores Ópticos Retangulares",
        desc: "Encaixe a cúpula óptica 05A cobrindo X = -210 a -90 mm (altura externa 260 mm) e fixe a janela de acrílico fumê. Monte a Câmera USB 1080p no topo (Y = 255 mm) e o Ring Light 12V 6000K em Y = 215 mm com difusor leitoso 1 mm. Fixe os suportes 04A na longarina esquerda e parafusar por baixo com parafusos M3 os sensores fotoelétricos retangulares 5V TTL S1 (X = -150 mm) e S2 (X = +100 mm), alinhando o feixe óptico na cota Y = 90 mm.",
        tools: "Chave Allen 2,5 mm · Chave Phillips PH1",
        comps: [5, 6],
        camPos: [-120, 260, 380],
        camTarget: [-120, 140, 0]
      },
      7: {
        title: "Etapa 7: Empurrador Linear MG996R, Rampa Suave 18° e Caixas Coletoras",
        desc: "Monte o pórtico 03E do Empurrador Linear em X = +160 mm com as 4 buchas LM6UU e as duas guias retificadas inox Ø 6 × 170 mm (entre-centros 85 mm). Fixe o servo MG996R, a alavanca R = 60 mm e a biela L = 110 mm com rolamentos 623ZZ, conectando a sapata côncava 03H (100×90×12 mm com EVA 2 mm) e a trave 03I (90×18×12 mm), obtendo curso de 120 mm (Z = -62 a +58 mm). Encaixe a rampa 18° 06A com aba defletora em EVA 3 mm no vão direito. Posicione a Caixa de Aprovados na saída frontal (X = +375 mm, Y = 0) e a de Rejeitados na lateral (X = +160 mm, Z = +190 mm, Y = 0).",
        tools: "Chave Allen 2,5 mm · Chave Phillips PH1 · Chave Fixa 5,5 mm",
        comps: [7, 8, 9],
        camPos: [160, 260, 380],
        camTarget: [160, 90, 80]
      }
    };'''
html = html.replace(old_steps, new_steps)

# =========================================================================
# 14. REMOVE RESIDUAL M18 / 24V / 24 V / PC817 / 100 RPM / A1 MINI / 25,4 mm
# =========================================================================
# Badge style cleanup
html = html.replace('.badge-24v { background: #fef3c7; color: #b45309; border: 1px solid #fbbf24; }', '/* badge-24v removido para mono-fonte 12V */')

# Ensure no residual mentions
html = html.replace('M18', 'Retangular')
html = html.replace('m18', 'retangular')
html = html.replace('24V', '12V')
html = html.replace('24 V', '12 V')
html = html.replace('PC817', 'NPN TTL')
html = html.replace('A1 Mini', 'Bambu P2S')
html = html.replace('100 RPM', '60 RPM')
html = html.replace('157 mm/s', '94 mm/s')
html = html.replace('60 mm/s', '94 mm/s')
html = html.replace('25,4 mm', '17,3 mm')
html = html.replace('25.4 mm', '17.3 mm')
html = html.replace('152,4', '152,0')
html = html.replace('152.4', '152.0')
html = html.replace('57,2', '55,0')
html = html.replace('57.15', '55.0')

with open('Manual_Montagem_Esteira_70cm.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated Manual_Montagem_Esteira_70cm.html successfully.")
