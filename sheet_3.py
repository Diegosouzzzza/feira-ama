# -*- coding: utf-8 -*-
"""
Sheet 3: Diagrama Multifilar de Comando, Sensores Ópticos IR e Pinagem do ESP32
AmazonVision 4.0 - XXI Feira Tecnológica FUCAPI 2026
Arquitetura Simplificada Mono-Fonte 12V DC — Proteção Clamp BAT54S + R1kΩ
"""

from sheet_frame import get_cad_frame

def get_sheet_3():
    frame = get_cad_frame(3, "DIAGRAMA MULTIFILAR DE COMANDO — SENSORES E ESP32", "Sensores Ópticos Retangulares IR (5V NPN), Pinagem ESP32, Clamp BAT54S e Interface USB")
    
    svg = f"""
    {frame}
    
    <!-- ========================================================
         FOLHA 03: COMANDO, SENSORES ÓPTICOS IR E ESP32
         ======================================================== -->

    <!-- SEÇÃO ESQUERDA: SENSORES ÓPTICOS REFLEXIVOS 5V DC -->
    <g transform="translate(60, 55)">
      <rect x="0" y="0" width="370" height="26" fill="#14221b" stroke="#00e5ff" stroke-width="1.2" rx="3"/>
      <text x="12" y="18" font-family="var(--font-mono)" font-size="11" fill="#00e5ff" font-weight="700">CAMPO 5V: SENSORES ÓPTICOS IR RETANGULARES (NPN NA)</text>
    </g>

    <!-- SENSOR B1 / S1 (CÂMERA X = -150 mm) -->
    <g transform="translate(60, 95)" id="svg_sensor_s1_block" class="cad-component-card">
      <rect x="0" y="0" width="280" height="155" class="symbol-box-accent" id="box_sensor_s1"/>
      <text x="12" y="20" font-family="var(--font-mono)" font-size="10.5" fill="#fff" font-weight="700">B1 (S1): SENSOR ÓPTICO CÂMERA</text>
      <text x="12" y="32" font-family="var(--font-mono)" font-size="7.5" fill="#00e5ff">Sensor Óptico IR Retangular 5V NPN NA (c/ pull-up interno 10kΩ)</text>
      <text x="12" y="44" font-family="var(--font-mono)" font-size="8" fill="#8fa699">Posição Esteira: X = -150 mm | Alcance Regulável: 3 a 80 cm</text>

      <!-- Desenho Sensor IR Retangular -->
      <g transform="translate(15, 60)">
        <rect x="0" y="0" width="65" height="28" fill="#1d2e24" stroke="#4e6b5a" rx="2"/>
        <line x1="50" y1="0" x2="50" y2="28" stroke="#00e5ff" stroke-width="1.5"/>
        <circle cx="58" cy="14" r="5" fill="#0f1813" stroke="#ff3344" id="s1_sensor_led"/>
        <text x="58" y="17" font-family="var(--font-mono)" font-size="6" fill="#fff" text-anchor="middle">LED</text>
        <text x="22" y="18" font-family="var(--font-mono)" font-size="7" fill="#8fa699">IR 5V</text>
      </g>

      <!-- Textos dos Cabos com Área Limpa e Livre -->
      <g transform="translate(90, 60)">
        <text x="0" y="12" class="lbl-pin" fill="#ffd600">BN (MARROM): +5V (+5V_ESP)</text>
        <text x="0" y="36" class="lbl-pin" fill="#29b6f6">BU (AZUL): 0V (0V_COMUM)</text>
        <text x="0" y="60" class="lbl-pin" fill="#fff" id="lbl_s1_sig_pin">BK (PRETO): SINAL NPN COLETOR ABERTO</text>
      </g>

      <!-- Terminais de Saída na Parede Direita da Caixa (X = 280) -->
      <circle cx="280" cy="72" r="4.5" class="symbol-terminal" fill="#ffd600"/>
      <circle cx="280" cy="96" r="4.5" class="symbol-terminal" fill="#00e676"/>
      <circle cx="280" cy="120" r="4.5" class="symbol-terminal" fill="#00e5ff"/>
    </g>

    <!-- Bornes Régua X2 (X2:1 a X2:3) para Sensor S1 -->
    <g transform="translate(360, 140)">
      <!-- X2:1 (+5V) -->
      <circle cx="10" cy="27" r="4.5" class="symbol-terminal" fill="#ffd600"/>
      <text x="10" y="18" font-family="var(--font-mono)" font-size="8" fill="#ffd600" text-anchor="middle">X2:1</text>
      <!-- X2:2 (0V) -->
      <circle cx="10" cy="51" r="4.5" class="symbol-terminal" fill="#00e676"/>
      <text x="10" y="42" font-family="var(--font-mono)" font-size="8" fill="#00e676" text-anchor="middle">X2:2</text>
      <!-- X2:3 (Sinal BK) -->
      <circle cx="10" cy="75" r="4.5" class="symbol-terminal" fill="#00e5ff"/>
      <text x="10" y="66" font-family="var(--font-mono)" font-size="8" fill="#00e5ff" text-anchor="middle">X2:3</text>
    </g>

    <!-- Fios do Sensor S1 saindo da Parede Direita (X=344.5) para Bornes X2 (X=365.5) -->
    <path d="M 344.5 167 L 365.5 167" class="wire w-5v"/>
    <path d="M 344.5 191 L 365.5 191" class="wire w-gnd"/>
    <path id="s3_wire_s1_bk" d="M 344.5 215 L 365.5 215" class="wire" stroke="#00e5ff" stroke-width="2"/>

    <!-- Linha de Alimentação Geral Chegando em X2:1 (+5V_ESP) e X2:2 (0V_COMUM) -->
    <path d="M 40 167 L 60 167" class="wire w-5v"/>
    <text x="10" y="170" font-family="var(--font-mono)" font-size="8" fill="#ffd600">+5V</text>
    <path d="M 40 191 L 60 191" class="wire w-gnd"/>
    <text x="10" y="194" font-family="var(--font-mono)" font-size="8" fill="#00e676">0V</text>

    <!-- SENSOR B2 / S2 (DESVIO X = +100 mm) -->
    <g transform="translate(60, 275)" id="svg_sensor_s2_block" class="cad-component-card">
      <rect x="0" y="0" width="280" height="155" class="symbol-box" id="box_sensor_s2"/>
      <text x="12" y="20" font-family="var(--font-mono)" font-size="10.5" fill="#fff" font-weight="700">B2 (S2): SENSOR ÓPTICO DESVIO</text>
      <text x="12" y="32" font-family="var(--font-mono)" font-size="7.5" fill="#00e5ff">Sensor Óptico IR Retangular 5V NPN NA (c/ pull-up interno 10kΩ)</text>
      <text x="12" y="44" font-family="var(--font-mono)" font-size="8" fill="#8fa699">Posição Esteira: X = +100 mm | Gatilho Empurrador Linear</text>

      <!-- Desenho Sensor IR Retangular -->
      <g transform="translate(15, 60)">
        <rect x="0" y="0" width="65" height="28" fill="#1d2e24" stroke="#4e6b5a" rx="2"/>
        <line x1="50" y1="0" x2="50" y2="28" stroke="#00e5ff" stroke-width="1.5"/>
        <circle cx="58" cy="14" r="5" fill="#0f1813" stroke="#ff3344" id="s2_sensor_led"/>
        <text x="58" y="17" font-family="var(--font-mono)" font-size="6" fill="#fff" text-anchor="middle">LED</text>
        <text x="22" y="18" font-family="var(--font-mono)" font-size="7" fill="#8fa699">IR 5V</text>
      </g>

      <!-- Textos dos Cabos com Área Limpa -->
      <g transform="translate(90, 60)">
        <text x="0" y="12" class="lbl-pin" fill="#ffd600">BN (MARROM): +5V (+5V_ESP)</text>
        <text x="0" y="36" class="lbl-pin" fill="#29b6f6">BU (AZUL): 0V (0V_COMUM)</text>
        <text x="0" y="60" class="lbl-pin" fill="#fff" id="lbl_s2_sig_pin">BK (PRETO): SINAL NPN COLETOR ABERTO</text>
      </g>

      <!-- Terminais de Saída na Parede Direita (X = 280) -->
      <circle cx="280" cy="72" r="4.5" class="symbol-terminal" fill="#ffd600"/>
      <circle cx="280" cy="96" r="4.5" class="symbol-terminal" fill="#00e676"/>
      <circle cx="280" cy="120" r="4.5" class="symbol-terminal" fill="#00e5ff"/>
    </g>

    <!-- Bornes Régua X2 (X2:4 a X2:6) para Sensor S2 -->
    <g transform="translate(360, 320)">
      <circle cx="10" cy="27" r="4.5" class="symbol-terminal" fill="#ffd600"/>
      <text x="10" y="18" font-family="var(--font-mono)" font-size="8" fill="#ffd600" text-anchor="middle">X2:4</text>
      <circle cx="10" cy="51" r="4.5" class="symbol-terminal" fill="#00e676"/>
      <text x="10" y="42" font-family="var(--font-mono)" font-size="8" fill="#00e676" text-anchor="middle">X2:5</text>
      <circle cx="10" cy="75" r="4.5" class="symbol-terminal" fill="#00e5ff"/>
      <text x="10" y="66" font-family="var(--font-mono)" font-size="8" fill="#00e5ff" text-anchor="middle">X2:6</text>
    </g>

    <!-- Fios do Sensor S2 saindo de X=344.5 para Bornes X2 (X=365.5) -->
    <path d="M 344.5 347 L 365.5 347" class="wire w-5v"/>
    <path d="M 344.5 371 L 365.5 371" class="wire w-gnd"/>
    <path id="s3_wire_s2_bk" d="M 344.5 395 L 365.5 395" class="wire" stroke="#00e5ff" stroke-width="2"/>

    <!-- Linha de Alimentação Geral Chegando em X2:4 (+5V_ESP) e X2:5 (0V_COMUM) para S2 -->
    <path d="M 40 347 L 60 347" class="wire w-5v"/>
    <text x="10" y="350" font-family="var(--font-mono)" font-size="8" fill="#ffd600">+5V</text>
    <path d="M 40 371 L 60 371" class="wire w-gnd"/>
    <text x="10" y="374" font-family="var(--font-mono)" font-size="8" fill="#00e676">0V</text>

    <!-- ========================================================
         SEÇÃO CENTRAL: PROTEÇÃO CLAMP SCHOTTKY 3,3V & PULL-UP
         ======================================================== -->
    <g transform="translate(420, 55)">
      <rect x="0" y="0" width="480" height="26" fill="#14221b" stroke="#00e676" stroke-width="1.2" rx="3"/>
      <text x="12" y="18" font-family="var(--font-mono)" font-size="11" fill="#00e676" font-weight="700">PROTEÇÃO CLAMP SCHOTTKY 3,3V (BAT54S + R1kΩ) &amp; PULL-UP INTERNO</text>
    </g>

    <g transform="translate(420, 95)" id="svg_npn_interface">
      <rect x="0" y="0" width="480" height="345" class="symbol-box-accent" id="box_npn_interface"/>
      <text x="16" y="22" font-family="var(--font-mono)" font-size="12" fill="#fff" font-weight="700">PROTEÇÃO CONTRA SOBRETENSÃO — CLAMP SCHOTTKY 3,3V</text>
      <text x="16" y="36" font-family="var(--font-mono)" font-size="8.5" fill="#00e5ff">Clamp Superior a +3,3V (BAT54S) + Resistor Série 1kΩ contra Pull-up 10kΩ do Sensor</text>

      <!-- CANAL 1: SINAL DO SENSOR S1 (CÂMERA ➔ GPIO 25 COM CLAMP BAT54S) -->
      <g transform="translate(20, 48)" id="npn_canal_s1">
        <rect x="0" y="0" width="440" height="78" fill="#0f1814" stroke="#1f3226" rx="3"/>
        <text x="10" y="15" font-family="var(--font-mono)" font-size="8.5" fill="#00e5ff" font-weight="700">CANAL 01: SENSOR B1 (S1 IR 5V) ➔ R1=1kΩ ➔ CLAMP BAT54S (3,3V) ➔ GPIO 25</text>
        
        <!-- Entrada do borne X2:3 (BK do Sensor 5V) -->
        <circle cx="18" cy="40" r="4" class="symbol-terminal" fill="#00e5ff"/>
        <text x="18" y="29" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">X2:3</text>
        <text x="26" y="43" class="lbl-pin">BK (5V)</text>

        <!-- Linha até Resistor R1 -->
        <line x1="18" y1="40" x2="68" y2="40" stroke="#00e5ff" stroke-width="1.8"/>

        <!-- RESISTOR SÉRIE DE PROTEÇÃO R1 = 1 kΩ (Limitador &lt; 2 mA) -->
        <g id="r_prot_s1" transform="translate(68, 32)" class="cad-component-card">
          <rect x="0" y="0" width="38" height="16" fill="#182c20" stroke="#00e676" stroke-width="1.2" rx="2"/>
          <text x="19" y="11" font-family="var(--font-mono)" font-size="7.5" fill="#00e676" font-weight="700" text-anchor="middle">R1: 1kΩ</text>
        </g>
        <text x="87" y="27" font-family="var(--font-mono)" font-size="6.5" fill="#8fa699" text-anchor="middle">1/4W 1%</text>

        <!-- Linha do Resistor até o Nó de Clamp -->
        <line x1="106" y1="40" x2="160" y2="40" stroke="#00e5ff" stroke-width="2"/>
        <circle cx="160" cy="40" r="3" fill="#00e5ff"/>

        <!-- DIODO SCHOTTKY DUPLO BAT54S (SOT-23) — CLAMP 3,3V / GND -->
        <g id="bat54s_s1" transform="translate(145, 18)" class="cad-component-card">
          <rect x="0" y="0" width="95" height="46" fill="#131e18" stroke="#ffd600" stroke-width="1.2" rx="3"/>
          <text x="47" y="10" font-family="var(--font-mono)" font-size="7" fill="#ffd600" font-weight="700" text-anchor="middle">BAT54S (SOT-23)</text>

          <!-- Diodo Superior (Clamp para +3,3V: Anodo no nó BK, Catodo em +3,3V) -->
          <g transform="translate(24, 13)">
            <line x1="0" y1="9" x2="0" y2="0" stroke="#d500f9" stroke-width="1.2"/>
            <polygon points="-4,6 4,6 0,1" fill="#ffd600"/>
            <line x1="-4" y1="1" x2="4" y2="1" stroke="#ffd600" stroke-width="1.2"/>
            <line x1="-4" y1="1" x2="-4" y2="3" stroke="#ffd600" stroke-width="1"/>
            <line x1="4" y1="1" x2="4" y2="-1" stroke="#ffd600" stroke-width="1"/>
            <text x="7" y="5" font-family="var(--font-mono)" font-size="6" fill="#d500f9">+3,3V</text>
          </g>

          <!-- Diodo Inferior (Clamp para GND: Anodo em GND, Catodo no nó BK) -->
          <g transform="translate(24, 25)">
            <line x1="0" y1="12" x2="0" y2="19" stroke="#00e676" stroke-width="1.2"/>
            <polygon points="-4,14 4,14 0,9" fill="#ffd600"/>
            <line x1="-4" y1="9" x2="4" y2="9" stroke="#ffd600" stroke-width="1.2"/>
            <line x1="-4" y1="9" x2="-4" y2="11" stroke="#ffd600" stroke-width="1"/>
            <line x1="4" y1="9" x2="4" y2="7" stroke="#ffd600" stroke-width="1"/>
            <text x="7" y="17" font-family="var(--font-mono)" font-size="6" fill="#00e676">0V (GND)</text>
          </g>

          <text x="56" y="38" font-family="var(--font-mono)" font-size="6" fill="#8fa699">Vf ≈ 0,25V</text>
        </g>

        <!-- Linha pós-clamp até Terminal GPIO 25 do ESP32 -->
        <line x1="240" y1="40" x2="315" y2="40" stroke="#00e5ff" stroke-width="2"/>
        <circle cx="315" cy="40" r="2.5" fill="#00e5ff"/>

        <!-- Indicação de Nível Lógico Seguro pós-clamp -->
        <g transform="translate(245, 23)">
          <rect x="0" y="0" width="85" height="13" fill="#1b2a1e" rx="2"/>
          <text x="42" y="9" font-family="var(--font-mono)" font-size="6.5" fill="#00e676" font-weight="700" text-anchor="middle">MÁX 3,55V (SEGURO)</text>
        </g>

        <!-- Pull-Up Interno ESP32 -->
        <g transform="translate(325, 20)">
          <line x1="12" y1="0" x2="12" y2="6" stroke="#d500f9" stroke-width="1"/>
          <text x="12" y="-2" font-family="var(--font-mono)" font-size="6" fill="#d500f9" text-anchor="middle">+3,3V</text>
          <rect x="8" y="6" width="8" height="14" fill="#1b1226" stroke="#d500f9" stroke-width="0.8" rx="1"/>
          <text x="12" y="16" font-family="var(--font-mono)" font-size="5" fill="#fff" text-anchor="middle">45k</text>
          <line x1="12" y1="20" x2="12" y2="28" stroke="#00e5ff" stroke-width="1"/>
          <circle cx="12" cy="28" r="2" fill="#00e5ff"/>
          <text x="20" y="16" font-family="var(--font-mono)" font-size="5.5" fill="#d500f9">PULLUP</text>
        </g>

        <line x1="315" y1="40" x2="340" y2="40" stroke="#00e5ff" stroke-width="1.8"/>
        <line x1="337" y1="48" x2="340" y2="40" stroke="#00e5ff" stroke-width="1.5"/>
        <line x1="340" y1="40" x2="415" y2="40" stroke="#00e5ff" stroke-width="2"/>

        <circle cx="415" cy="40" r="4.5" class="symbol-terminal" fill="#00e5ff"/>
        <text x="405" y="32" class="lbl-pin" fill="#00e5ff" text-anchor="end">➔ GPIO 25 (ESP32)</text>
        <text x="405" y="52" font-family="var(--font-mono)" font-size="6.5" fill="#00e676" text-anchor="end">0V (det.) / 3,3V (rep.)</text>

        <!-- Rótulo Obrigatório Conforme Problema 1-B -->
        <text x="10" y="70" font-family="var(--font-mono)" font-size="7.5" fill="#ffd600" font-weight="700">BAT54S + R1kΩ · Clamp 3,3V contra pull-up interno 10kΩ do Sensor IR 5V</text>
      </g>

      <!-- CANAL 2: SINAL DO SENSOR S2 (DESVIO ➔ GPIO 26 COM CLAMP BAT54S) -->
      <g transform="translate(20, 132)" id="npn_canal_s2">
        <rect x="0" y="0" width="440" height="78" fill="#0f1814" stroke="#1f3226" rx="3"/>
        <text x="10" y="15" font-family="var(--font-mono)" font-size="8.5" fill="#00e5ff" font-weight="700">CANAL 02: SENSOR B2 (S2 IR 5V) ➔ R2=1kΩ ➔ CLAMP BAT54S (3,3V) ➔ GPIO 26</text>
        
        <!-- Entrada do borne X2:6 (BK do Sensor 5V) -->
        <circle cx="18" cy="40" r="4" class="symbol-terminal" fill="#00e5ff"/>
        <text x="18" y="29" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">X2:6</text>
        <text x="26" y="43" class="lbl-pin">BK (5V)</text>

        <!-- Linha até Resistor R2 -->
        <line x1="18" y1="40" x2="68" y2="40" stroke="#00e5ff" stroke-width="1.8"/>

        <!-- RESISTOR SÉRIE DE PROTEÇÃO R2 = 1 kΩ (Limitador &lt; 2 mA) -->
        <g id="r_prot_s2" transform="translate(68, 32)" class="cad-component-card">
          <rect x="0" y="0" width="38" height="16" fill="#182c20" stroke="#00e676" stroke-width="1.2" rx="2"/>
          <text x="19" y="11" font-family="var(--font-mono)" font-size="7.5" fill="#00e676" font-weight="700" text-anchor="middle">R2: 1kΩ</text>
        </g>
        <text x="87" y="27" font-family="var(--font-mono)" font-size="6.5" fill="#8fa699" text-anchor="middle">1/4W 1%</text>

        <!-- Linha do Resistor até o Nó de Clamp -->
        <line x1="106" y1="40" x2="160" y2="40" stroke="#00e5ff" stroke-width="2"/>
        <circle cx="160" cy="40" r="3" fill="#00e5ff"/>

        <!-- DIODO SCHOTTKY DUPLO BAT54S (SOT-23) — CLAMP 3,3V / GND -->
        <g id="bat54s_s2" transform="translate(145, 18)" class="cad-component-card">
          <rect x="0" y="0" width="95" height="46" fill="#131e18" stroke="#ffd600" stroke-width="1.2" rx="3"/>
          <text x="47" y="10" font-family="var(--font-mono)" font-size="7" fill="#ffd600" font-weight="700" text-anchor="middle">BAT54S (SOT-23)</text>

          <!-- Diodo Superior (Clamp para +3,3V) -->
          <g transform="translate(24, 13)">
            <line x1="0" y1="9" x2="0" y2="0" stroke="#d500f9" stroke-width="1.2"/>
            <polygon points="-4,6 4,6 0,1" fill="#ffd600"/>
            <line x1="-4" y1="1" x2="4" y2="1" stroke="#ffd600" stroke-width="1.2"/>
            <line x1="-4" y1="1" x2="-4" y2="3" stroke="#ffd600" stroke-width="1"/>
            <line x1="4" y1="1" x2="4" y2="-1" stroke="#ffd600" stroke-width="1"/>
            <text x="7" y="5" font-family="var(--font-mono)" font-size="6" fill="#d500f9">+3,3V</text>
          </g>

          <!-- Diodo Inferior (Clamp para GND) -->
          <g transform="translate(24, 25)">
            <line x1="0" y1="12" x2="0" y2="19" stroke="#00e676" stroke-width="1.2"/>
            <polygon points="-4,14 4,14 0,9" fill="#ffd600"/>
            <line x1="-4" y1="9" x2="4" y2="9" stroke="#ffd600" stroke-width="1.2"/>
            <line x1="-4" y1="9" x2="-4" y2="11" stroke="#ffd600" stroke-width="1"/>
            <line x1="4" y1="9" x2="4" y2="7" stroke="#ffd600" stroke-width="1"/>
            <text x="7" y="17" font-family="var(--font-mono)" font-size="6" fill="#00e676">0V (GND)</text>
          </g>

          <text x="56" y="38" font-family="var(--font-mono)" font-size="6" fill="#8fa699">Vf ≈ 0,25V</text>
        </g>

        <!-- Linha pós-clamp até Terminal GPIO 26 do ESP32 -->
        <line x1="240" y1="40" x2="315" y2="40" stroke="#00e5ff" stroke-width="2"/>
        <circle cx="315" cy="40" r="2.5" fill="#00e5ff"/>

        <!-- Indicação de Nível Lógico Seguro pós-clamp -->
        <g transform="translate(245, 23)">
          <rect x="0" y="0" width="85" height="13" fill="#1b2a1e" rx="2"/>
          <text x="42" y="9" font-family="var(--font-mono)" font-size="6.5" fill="#00e676" font-weight="700" text-anchor="middle">MÁX 3,55V (SEGURO)</text>
        </g>

        <!-- Pull-Up Interno ESP32 -->
        <g transform="translate(325, 20)">
          <line x1="12" y1="0" x2="12" y2="6" stroke="#d500f9" stroke-width="1"/>
          <text x="12" y="-2" font-family="var(--font-mono)" font-size="6" fill="#d500f9" text-anchor="middle">+3,3V</text>
          <rect x="8" y="6" width="8" height="14" fill="#1b1226" stroke="#d500f9" stroke-width="0.8" rx="1"/>
          <text x="12" y="16" font-family="var(--font-mono)" font-size="5" fill="#fff" text-anchor="middle">45k</text>
          <line x1="12" y1="20" x2="12" y2="28" stroke="#00e5ff" stroke-width="1"/>
          <circle cx="12" cy="28" r="2" fill="#00e5ff"/>
          <text x="20" y="16" font-family="var(--font-mono)" font-size="5.5" fill="#d500f9">PULLUP</text>
        </g>

        <line x1="315" y1="40" x2="340" y2="40" stroke="#00e5ff" stroke-width="1.8"/>
        <line x1="337" y1="48" x2="340" y2="40" stroke="#00e5ff" stroke-width="1.5"/>
        <line x1="340" y1="40" x2="415" y2="40" stroke="#00e5ff" stroke-width="2"/>

        <circle cx="415" cy="40" r="4.5" class="symbol-terminal" fill="#00e5ff"/>
        <text x="405" y="32" class="lbl-pin" fill="#00e5ff" text-anchor="end">➔ GPIO 26 (ESP32)</text>
        <text x="405" y="52" font-family="var(--font-mono)" font-size="6.5" fill="#00e676" text-anchor="end">0V (det.) / 3,3V (rep.)</text>

        <!-- Rótulo Obrigatório Conforme Problema 1-B -->
        <text x="10" y="70" font-family="var(--font-mono)" font-size="7.5" fill="#ffd600" font-weight="700">BAT54S + R1kΩ · Clamp 3,3V contra pull-up interno 10kΩ do Sensor IR 5V</text>
      </g>

      <!-- QUADRO TÉCNICO: PROTEÇÃO CONTRA SOBRETENSÃO — CLAMP 3,3V OBRIGATÓRIO (PROBLEMA 1-C) -->
      <g transform="translate(20, 216)">
        <rect x="0" y="0" width="440" height="120" fill="#132019" stroke="#ffd600" stroke-width="1.4" rx="4"/>
        <text x="12" y="18" font-family="var(--font-mono)" font-size="9" fill="#ffd600" font-weight="700">PROTEÇÃO CONTRA SOBRETENSÃO — CLAMP 3,3V OBRIGATÓRIO</text>
        <text x="12" y="34" font-family="var(--font-sans)" font-size="8.5" fill="#e0e8e3">O Sensor Óptico IR Retangular 5V NPN NA traz pull-up interno de 10 kΩ para +5V.</text>
        <text x="12" y="48" font-family="var(--font-sans)" font-size="8.5" fill="#e0e8e3">Sem proteção externa, a GPIO do ESP32 recebe 5V em repouso</text>
        <text x="12" y="62" font-family="var(--font-sans)" font-size="8.5" fill="#e0e8e3">(sobretensão &gt; absoluto máximo 3,6 V, risco de queima).</text>
        <text x="12" y="76" font-family="var(--font-sans)" font-size="8.5" fill="#e0e8e3">O par BAT54S + R=1kΩ em cada canal grampeia o sinal a 3,3V + Vf</text>
        <text x="12" y="90" font-family="var(--font-sans)" font-size="8.5" fill="#e0e8e3">Schottky ≈ 3,55 V, garantindo nível lógico seguro.</text>
        <text x="12" y="104" font-family="var(--font-sans)" font-size="8" fill="#8fa699">Alternativa: divisor R1=10kΩ série + R2=20kΩ para GND (atenuação 0,667, nível resultante 3,33 V).</text>
      </g>
    </g>

    <!-- Ligações Físicas de Entrada e Saída do Bloco de Proteção Clamp BAT54S para os Pinos do ESP32 -->
    <!-- Canal 01: X2:3 (370, 215) ➔ Entrada Clamp (458, 183) e Saída Clamp (855, 183) ➔ GPIO 25 (1025, 305) -->
    <path id="s3_wire_s1_to_clamp" d="M 374.5 215 L 400 215 L 400 183 L 454 183" class="wire" stroke="#00e5ff" stroke-width="2"/>
    <path id="s3_wire_out1_gpio25" d="M 859.5 183 L 950 183 L 950 305 L 1020.5 305" class="wire" stroke="#00e5ff" stroke-width="2"/>

    <!-- Canal 02: X2:6 (370, 395) ➔ Entrada Clamp (458, 267) e Saída Clamp (855, 267) ➔ GPIO 26 (1025, 330) -->
    <path id="s3_wire_s2_to_clamp" d="M 374.5 395 L 400 395 L 400 267 L 454 267" class="wire" stroke="#00e5ff" stroke-width="2"/>
    <path id="s3_wire_out2_gpio26" d="M 859.5 267 L 935 267 L 935 330 L 1020.5 330" class="wire" stroke="#00e5ff" stroke-width="2"/>

    <!-- ========================================================
         CANAL DE FIRMWARE DO BOTÃO DE EMERGÊNCIA S0
         ======================================================== -->
    <g transform="translate(60, 445)">
      <rect x="0" y="0" width="280" height="95" class="symbol-box"/>
      <text x="12" y="18" font-family="var(--font-mono)" font-size="10" fill="#ff1744" font-weight="700">CANAL DE FIRMWARE DO BOTÃO S0</text>
      <text x="12" y="30" font-family="var(--font-mono)" font-size="8" fill="#8fa699">Bloco NA (13-14) — Monitoramento ESP32</text>
      
      <!-- Contato NA 13-14 (Terminal 13 em global 115,500 e Terminal 14 em global 158,500) -->
      <g transform="translate(20, 45)">
        <text x="0" y="12" font-family="var(--font-mono)" font-size="8" fill="#fff">NA 13</text>
        <circle cx="35" cy="10" r="3.5" class="symbol-terminal"/>
        <line x1="38.5" y1="10" x2="48" y2="10" stroke="#00e676" stroke-width="2"/>
        <line id="s3_s0_na_arm" x1="48" y1="10" x2="68" y2="0" stroke="#ff1744" stroke-width="2.2" class="relay-arm"/>
        <circle cx="48" cy="10" r="2.2" fill="#fff"/>
        <circle cx="68" cy="10" r="2.2" fill="#fff"/>
        <line x1="68" y1="10" x2="74.5" y2="10" stroke="#b388ff" stroke-width="2"/>
        <circle cx="78" cy="10" r="3.5" class="symbol-terminal"/>
        <text x="86" y="12" font-family="var(--font-mono)" font-size="8" fill="#fff">14</text>
      </g>
    </g>

    <!-- Bornes Régua X2:9 e X2:10 para S0 -->
    <g transform="translate(360, 480)">
      <circle cx="10" cy="10" r="4.5" class="symbol-terminal"/>
      <text x="10" y="1" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">X2:9 (0V)</text>
      <circle cx="10" cy="35" r="4.5" class="symbol-terminal"/>
      <text x="10" y="49" font-family="var(--font-mono)" font-size="8" fill="#b388ff" text-anchor="middle">X2:10</text>
    </g>
    <!-- Fio 0V do Terminal 13 (115, 500) passando por X2:9 (370, 490) -->
    <path d="M 115 496.5 L 115 490 L 365.5 490" class="wire w-gnd"/>
    <path d="M 374.5 490 L 405 490" class="wire w-gnd"/>
    <text x="410" y="493" font-family="var(--font-mono)" font-size="7.5" fill="#00e676">0V_COMUM</text>
    <!-- Fio de S0 NA Terminal 14 (158, 500) passando por X2:10 (370, 515) até GPIO 27 (1020.5, 355) -->
    <path d="M 158 503.5 L 158 515 L 365.5 515" class="wire w-sig"/>
    <path id="s3_wire_s0_gpio27" d="M 374.5 515 L 965 515 L 965 355 L 1020.5 355" class="wire w-sig"/>

    <!-- ========================================================
         SEÇÃO DIREITA: MICROCONTROLADOR ESP32 DEVKIT V1 (U1)
         ======================================================== -->
    <g transform="translate(1000, 55)">
      <rect x="0" y="0" width="410" height="26" fill="#14221b" stroke="#ffd600" stroke-width="1.2" rx="3"/>
      <text x="12" y="18" font-family="var(--font-mono)" font-size="11" fill="#ffd600" font-weight="700">CONTROLE &amp; PROCESSAMENTO: ESP32 DEVKIT V1 (U1)</text>
    </g>

    <g transform="translate(1000, 95)" id="svg_esp32_module">
      <rect x="0" y="0" width="370" height="430" fill="#0d1812" stroke="#ffd600" stroke-width="2" rx="6" id="box_esp32"/>
      <text x="16" y="24" font-family="var(--font-mono)" font-size="12" fill="#fff" font-weight="700">U1: ESP32 DEVKIT V1</text>
      <text x="16" y="38" font-family="var(--font-mono)" font-size="9" fill="#ffd600">Dual-Core Tensilica LX6 240 MHz | 30 Pinos</text>

      <!-- Antena PCB e Blindagem RF -->
      <g transform="translate(15, 50)">
        <rect x="0" y="0" width="70" height="40" fill="#182c20" stroke="#3d5a47" rx="3"/>
        <text x="35" y="24" font-family="var(--font-mono)" font-size="8" fill="#8fa699" text-anchor="middle">ANTENA PCB</text>
        <rect x="80" y="0" width="100" height="50" fill="#1e3025" stroke="#72a88d" rx="2"/>
        <text x="130" y="20" font-family="var(--font-mono)" font-size="9" fill="#fff" font-weight="700" text-anchor="middle">ESP-WROOM-32</text>
        <text x="130" y="34" font-family="var(--font-mono)" font-size="7" fill="#00e5ff" text-anchor="middle">CE / FCC / ANATEL</text>
      </g>

      <!-- LED Onboard GPIO 2 -->
      <g transform="translate(200, 55)">
        <circle cx="15" cy="15" r="7" fill="#00e5ff" id="esp32_led_gpio2"/>
        <text x="30" y="19" font-family="var(--font-mono)" font-size="8" fill="#fff">GPIO 2 (LED STATUS)</text>
      </g>

      <!-- Mapeamento Milimétrico dos Pinos Utilizados (Y absoluto a partir de 95) -->
      <g transform="translate(15, 110)">
        <!-- PINO VIN (Alimentação 5,0V) -> Y local = 25 -> Y global = 230 -->
        <g transform="translate(0, 25)">
          <circle cx="10" cy="0" r="4.5" class="symbol-terminal" fill="#ffd600"/>
          <text x="22" y="3" font-family="var(--font-mono)" font-size="10" fill="#ffd600" font-weight="700">VIN (5V)</text>
          <text x="130" y="3" font-family="var(--font-sans)" font-size="8" fill="#8fa699">Alim local Buck U4 (5,0V 2A)</text>
        </g>

        <!-- PINO GND -> Y local = 50 -> Y global = 255 -->
        <g transform="translate(0, 50)">
          <circle cx="10" cy="0" r="4.5" class="symbol-terminal" fill="#00e676"/>
          <text x="22" y="3" font-family="var(--font-mono)" font-size="10" fill="#00e676" font-weight="700">GND</text>
          <text x="130" y="3" font-family="var(--font-sans)" font-size="8" fill="#8fa699">Barramento 0V_COMUM</text>
        </g>

        <!-- PINO 3V3 -> Y local = 75 -> Y global = 280 -->
        <g transform="translate(0, 75)">
          <circle cx="10" cy="0" r="4.5" class="symbol-terminal" fill="#d500f9"/>
          <text x="22" y="3" font-family="var(--font-mono)" font-size="10" fill="#d500f9" font-weight="700">3V3</text>
          <text x="130" y="3" font-family="var(--font-sans)" font-size="8" fill="#8fa699">Saída regulador interno LDO</text>
        </g>

        <!-- GPIO 25: PIN_SENSOR_S1 -> Y local = 100 -> Y global = 305 -->
        <g transform="translate(0, 100)">
          <circle cx="10" cy="0" r="4.5" class="symbol-terminal" fill="#00e5ff"/>
          <text x="22" y="3" font-family="var(--font-mono)" font-size="10" fill="#00e5ff" font-weight="700">GPIO 25</text>
          <text x="80" y="3" font-family="var(--font-mono)" font-size="9" fill="#fff">PIN_SENSOR_S1</text>
          <text x="210" y="3" font-family="var(--font-mono)" font-size="8" fill="#00e676" id="val_gpio_25">[INPUT_PULLUP: HIGH]</text>
        </g>

        <!-- GPIO 26: PIN_SENSOR_S2 -> Y local = 125 -> Y global = 330 -->
        <g transform="translate(0, 125)">
          <circle cx="10" cy="0" r="4.5" class="symbol-terminal" fill="#00e5ff"/>
          <text x="22" y="3" font-family="var(--font-mono)" font-size="10" fill="#00e5ff" font-weight="700">GPIO 26</text>
          <text x="80" y="3" font-family="var(--font-mono)" font-size="9" fill="#fff">PIN_SENSOR_S2</text>
          <text x="210" y="3" font-family="var(--font-mono)" font-size="8" fill="#00e676" id="val_gpio_26">[INPUT_PULLUP: HIGH]</text>
        </g>

        <!-- GPIO 27: PIN_ESTOP -> Y local = 150 -> Y global = 355 -->
        <g transform="translate(0, 150)">
          <circle cx="10" cy="0" r="4.5" class="symbol-terminal" fill="#ff1744"/>
          <text x="22" y="3" font-family="var(--font-mono)" font-size="10" fill="#ff1744" font-weight="700">GPIO 27</text>
          <text x="80" y="3" font-family="var(--font-mono)" font-size="9" fill="#fff">PIN_ESTOP</text>
          <text x="210" y="3" font-family="var(--font-mono)" font-size="8" fill="#00e676" id="val_gpio_27">[NORMAL: HIGH]</text>
        </g>

        <!-- GPIO 18: PIN_SERVO -> Y local = 180 -> Y global = 385 -->
        <g transform="translate(0, 180)">
          <circle cx="10" cy="0" r="4.5" class="symbol-terminal" fill="#ff9100"/>
          <text x="22" y="3" font-family="var(--font-mono)" font-size="10" fill="#ff9100" font-weight="700">GPIO 18</text>
          <text x="80" y="3" font-family="var(--font-mono)" font-size="9" fill="#fff">PIN_SERVO</text>
          <text x="210" y="3" font-family="var(--font-mono)" font-size="8" fill="#ff9100">[PWM EMPURRADOR 50Hz]</text>
        </g>

        <!-- GPIO 19: PIN_MOTOR_ONOFF -> Y local = 205 -> Y global = 410 -->
        <g transform="translate(0, 205)">
          <circle cx="10" cy="0" r="4.5" class="symbol-terminal" fill="#ff3344"/>
          <text x="22" y="3" font-family="var(--font-mono)" font-size="10" fill="#ff3344" font-weight="700">GPIO 19</text>
          <text x="80" y="3" font-family="var(--font-mono)" font-size="9" fill="#fff">PIN_MOTOR_ONOFF</text>
          <text x="210" y="3" font-family="var(--font-mono)" font-size="8" fill="#00e676" id="val_gpio_19">[OUT: HIGH 3,3V]</text>
        </g>
      </g>

      <!-- Conector Micro-USB Integrado -->
      <g transform="translate(130, 375)">
        <rect x="0" y="0" width="80" height="40" fill="#1f3226" stroke="#fff" rx="3"/>
        <text x="40" y="18" font-family="var(--font-mono)" font-size="9" fill="#fff" font-weight="700" text-anchor="middle">PORTA USB</text>
        <text x="40" y="30" font-family="var(--font-mono)" font-size="7" fill="#00e5ff" text-anchor="middle">CP2102 UART</text>
      </g>
    </g>

    <!-- Alimentação VIN (5V), GND (0V_COMUM) e 3V3 (REF CLAMP BAT54S) do ESP32 -->
    <path d="M 970 230 L 1020.5 230" class="wire w-5v"/>
    <text x="965" y="226" font-family="var(--font-mono)" font-size="7.5" fill="#ffd600" text-anchor="end">+5V_ESP</text>

    <path d="M 970 255 L 1020.5 255" class="wire w-gnd"/>
    <text x="965" y="251" font-family="var(--font-mono)" font-size="7.5" fill="#00e676" text-anchor="end">0V_COMUM</text>

    <path d="M 970 280 L 1020.5 280" class="wire w-3v3"/>
    <text x="965" y="276" font-family="var(--font-mono)" font-size="7" fill="#d500f9" text-anchor="end">+3,3V (REF CLAMP BAT54S)</text>

    <!-- Fio de saída GPIO 18 (PWM do Empurrador Linear) -->
    <path d="M 1020.5 385 L 980 385 L 980 440 L 940 440" class="wire w-sig"/>
    <text x="830" y="445" font-family="var(--font-mono)" font-size="9" fill="#ff9100" font-weight="700">W202 ➔ SERVO (PWM)</text>

    <!-- Fio de saída GPIO 19 (Disparo do Motorredutor) -->
    <path d="M 1020.5 410 L 970 410 L 970 465 L 940 465" class="wire w-sig"/>
    <text x="830" y="470" font-family="var(--font-mono)" font-size="9" fill="#d500f9" font-weight="700">W201 ➔ MOSFET D4184</text>

    <!-- ========================================================
         SEÇÃO CRÍTICA: CABO USB ISOLADO COM PROTEÇÃO ANTIRRETORNO
         ======================================================== -->
    <g transform="translate(1410, 55)">
      <rect x="0" y="0" width="250" height="26" fill="#14221b" stroke="#ff3344" stroke-width="1.2" rx="3"/>
      <text x="12" y="18" font-family="var(--font-mono)" font-size="11" fill="#ff3344" font-weight="700">PROTEÇÃO ANTIRRETORNO USB</text>
    </g>

    <g transform="translate(1410, 95)">
      <rect x="0" y="0" width="250" height="430" fill="#111c15" stroke="#ff3344" stroke-width="1.5" rx="5"/>
      <text x="14" y="22" font-family="var(--font-mono)" font-size="11" fill="#fff" font-weight="700">CABO USB HOST PC</text>
      <text x="14" y="34" font-family="var(--font-sans)" font-size="8" fill="#00e5ff">Conexão com Notebook Host (115200 bps)</text>

      <g transform="translate(15, 60)">
        <!-- Via 1: VBUS +5V SECCIONADA / CORTADA -->
        <g transform="translate(0, 0)">
          <line x1="0" y1="15" x2="60" y2="15" stroke="#ff3344" stroke-width="2.5"/>
          <g transform="translate(70, 15)">
            <text x="0" y="4" font-family="var(--font-mono)" font-size="14" fill="#ff1744" text-anchor="middle">✂️</text>
            <circle cx="0" cy="0" r="10" stroke="#ff1744" stroke-width="1.5" fill="none" stroke-dasharray="2 2"/>
          </g>
          <line x1="85" y1="15" x2="150" y2="15" stroke="#ff3344" stroke-width="2" stroke-dasharray="3 3"/>
          <text x="0" y="8" font-family="var(--font-mono)" font-size="8" fill="#ff3344" font-weight="700">VBUS (+5V): BLOQUEADO</text>
        </g>

        <!-- Via 2: D- (Dados Branco) -->
        <g transform="translate(0, 45)">
          <line x1="0" y1="15" x2="180" y2="15" stroke="#ffffff" stroke-width="2"/>
          <text x="0" y="8" font-family="var(--font-mono)" font-size="8" fill="#ffffff">D- (DADOS BRANCO)</text>
        </g>

        <!-- Via 3: D+ (Dados Verde) -->
        <g transform="translate(0, 85)">
          <line x1="0" y1="15" x2="180" y2="15" stroke="#00e676" stroke-width="2"/>
          <text x="0" y="8" font-family="var(--font-mono)" font-size="8" fill="#00e676">D+ (DADOS VERDE)</text>
        </g>

        <!-- Via 4: GND (Referência Preto) -->
        <g transform="translate(0, 125)">
          <line x1="0" y1="15" x2="180" y2="15" stroke="#8fa699" stroke-width="2.2"/>
          <text x="0" y="8" font-family="var(--font-mono)" font-size="8" fill="#8fa699">GND (MALHA BLINDADA)</text>
        </g>
      </g>

      <!-- Selo de Advertência -->
      <g transform="translate(15, 235)">
        <rect x="0" y="0" width="220" height="175" fill="#1d1212" stroke="#ff1744" stroke-width="1.2" rx="4"/>
        <text x="12" y="20" font-family="var(--font-mono)" font-size="10" fill="#ff1744" font-weight="800">⚠️ ADVERTÊNCIA TÉCNICA:</text>
        <text x="12" y="38" font-family="var(--font-sans)" font-size="9" fill="#ff8a80" font-weight="700">PROTEÇÃO DA PORTA USB DO PC</text>
        <text x="12" y="55" font-family="var(--font-sans)" font-size="8" fill="#e0e8e3">O ESP32 é alimentado com 5,0V</text>
        <text x="12" y="68" font-family="var(--font-sans)" font-size="8" fill="#e0e8e3">dedicados pelo módulo Buck U4.</text>
        <text x="12" y="85" font-family="var(--font-sans)" font-size="8" fill="#e0e8e3">A via VBUS (+5V) do cabo USB</text>
        <text x="12" y="98" font-family="var(--font-sans)" font-size="8" fill="#e0e8e3">deve ser fisicamente cortada para</text>
        <text x="12" y="111" font-family="var(--font-sans)" font-size="8" fill="#e0e8e3">evitar injeção reversa de corrente</text>
        <text x="12" y="124" font-family="var(--font-sans)" font-size="8" fill="#e0e8e3">na placa-mãe do notebook host</text>
        <text x="12" y="137" font-family="var(--font-sans)" font-size="8" fill="#e0e8e3">(risco de queima do chipset USB).</text>
      </g>
    </g>

    <!-- Ligações USB da Placa ESP32 contornando por baixo da placa (Zero Atravessamento) -->
    <path d="M 1170 510 L 1170 540 L 1390 540 L 1390 490 L 1410 490" class="wire" stroke="#00e5ff" stroke-width="2"/>
    <text x="1275" y="534" font-family="var(--font-mono)" font-size="8" fill="#00e5ff" font-weight="700">CABO USB ISOLADO (115200 bps)</text>

    <!-- NOTAS DE ENGENHARIA DESTA FOLHA -->
    <g transform="translate(60, 560)">
      <rect x="0" y="0" width="990" height="240" fill="#0f1612" stroke="#2a3d31" stroke-width="1.5" rx="5"/>
      <rect x="0" y="0" width="990" height="26" fill="#14221b" stroke="#2a3d31" stroke-width="1" rx="5 5 0 0"/>
      <text x="16" y="17" font-family="var(--font-mono)" font-size="11" fill="#00e5ff" font-weight="700">NOTAS TÉCNICAS: PROTOCOLO DE FIRMWARE, TEMPOS DE RESPOSTA E TRATAMENTO DE RUÍDO</text>

      <g transform="translate(20, 42)">
        <text x="0" y="15" font-family="var(--font-mono)" font-size="10" fill="#00e676" font-weight="700">1. DEBOUNCE E FILTRAGEM DIGITAL POR SOFTWARE:</text>
        <text x="15" y="30" font-family="var(--font-sans)" font-size="9" fill="#8fa699">• Os sensores ópticos reflexivos S1 e S2 possuem filtro de debounce de 25 ms por software no ESP32 para eliminar transientes de passagem rápida ou vibrações mecânicas da correia.</text>
        <text x="15" y="44" font-family="var(--font-sans)" font-size="9" fill="#8fa699">• A interrupção do botão de emergência S0 (GPIO 27) não possui debounce longo (&lt; 2 ms) para garantir tempo de reação imediato conforme NBR ISO 13849-1.</text>

        <text x="0" y="70" font-family="var(--font-mono)" font-size="10" fill="#00e676" font-weight="700">2. PROTOCOLO SERIAL COM O APLICATIVO PYTHON (OPENCV / PYTORCH):</text>
        <text x="15" y="85" font-family="var(--font-sans)" font-size="9" fill="#8fa699">• Baud rate fixado em 115200 bps, 8 bits de dados, sem paridade, 1 stop bit (8N1).</text>
        <text x="15" y="99" font-family="var(--font-sans)" font-size="9" fill="#8fa699">• Evento Sensor S1 disparado: ESP32 envia evento `["EVT", "S1_DETECTED", timestamp]`. O script Python efetua a captura do frame na cúpula, classifica o fruto e envia a decisão de desvio antes que o item atinja o Sensor S2.</text>

        <text x="0" y="125" font-family="var(--font-mono)" font-size="10" fill="#00e676" font-weight="700">3. PROTEÇÃO CONTRA SOBRETENSÃO (CLAMP SCHOTTKY BAT54S + R=1kΩ):</text>
        <text x="15" y="140" font-family="var(--font-sans)" font-size="9" fill="#8fa699">• Os sensores B1 (S1) e B2 (S2) — Sensor Óptico IR Retangular 5V NPN NA (c/ pull-up interno 10kΩ) — puxam a saída a +5V em repouso. Para proteger a GPIO do ESP32 (máx 3,6V), cada canal utiliza BAT54S + R=1kΩ, grampeando em 3,55V.</text>
        <text x="15" y="154" font-family="var(--font-sans)" font-size="9" fill="#8fa699">• O pino do ESP32 opera com INPUT_PULLUP interno garantindo nível lógico estável (HIGH 3,3V em repouso / LOW 0V na detecção) com total segurança de hardware contra sobretensão.</text>
      </g>
    </g>
    """
    return svg
