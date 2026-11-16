# -*- coding: utf-8 -*-
"""
Sheet Overview (Visão 00): Planta Geral Integrada do Projeto Todo Montado na Bancada
AmazonVision 4.0 - XXI Feira Tecnológica FUCAPI 2026
Engenharia de Automação / CAD / ECAD (IEC 60617 / NBR 5410 / NR-12)
"""

from sheet_frame import get_cad_frame

def get_sheet_overview():
    # Carimbo oficial com código normatizado
    frame = get_cad_frame(0, "PLANTA GERAL DO PROJETO MONTADO NA BANCADA", "Layout Físico Integrado: Mecânica 3D, Quadro DIN, Sensores, Atuadores e Notebook Host", dwg_code="PE-AV4-2026")
    
    # Ajuste de documento: PE-AV4-2026-FL00 -> PE-AV4-2026-VIS00
    frame = frame.replace("00 / 04", "VISÃO 00").replace("FL00", "VIS00")

    svg = f"""
    {frame}

    <!-- ========================================================
         VISÃO 00: PLANTA GERAL INTEGRADA DO PROJETO MONTADO
         ORGANIZADA EM 4 ZONAS LIMPAS E SEM SOBREPOSIÇÕES
         ======================================================== -->

    <!-- ========================================================
         ZONE BADGES & FLOW ARROWS (Visitor-friendly overview)
         ======================================================== -->
    <g id="zone_badges_and_flow" class="public-label" style="display:none">
      <!-- Zone 1 Badge -->
      <g transform="translate(50, 37)">
        <rect x="0" y="0" width="24" height="18" fill="#00e676" rx="9"/>
        <text x="12" y="13" font-family="var(--font-mono)" font-size="10" fill="#000" font-weight="800" text-anchor="middle">1</text>
        <text x="30" y="13" font-family="var(--font-mono)" font-size="9" fill="#00e676" font-weight="700">PAINEL ELETRICO</text>
      </g>
      <!-- Zone 2 Badge -->
      <g transform="translate(540, 37)">
        <rect x="0" y="0" width="24" height="18" fill="#00e5ff" rx="9"/>
        <text x="12" y="13" font-family="var(--font-mono)" font-size="10" fill="#000" font-weight="800" text-anchor="middle">2</text>
        <text x="30" y="13" font-family="var(--font-mono)" font-size="9" fill="#00e5ff" font-weight="700">ESTEIRA SELETORA (VISTA SUPERIOR)</text>
      </g>
      <!-- Zone 3 Badge -->
      <g transform="translate(540, 477)">
        <rect x="0" y="0" width="24" height="18" fill="#ff9100" rx="9"/>
        <text x="12" y="13" font-family="var(--font-mono)" font-size="10" fill="#000" font-weight="800" text-anchor="middle">3</text>
        <text x="30" y="13" font-family="var(--font-mono)" font-size="9" fill="#ff9100" font-weight="700">PERFIL LATERAL DA MONTAGEM</text>
      </g>
      <!-- Zone 4 Badge -->
      <g transform="translate(50, 667)">
        <rect x="0" y="0" width="24" height="18" fill="#ffd600" rx="9"/>
        <text x="12" y="13" font-family="var(--font-mono)" font-size="10" fill="#000" font-weight="800" text-anchor="middle">4</text>
        <text x="30" y="13" font-family="var(--font-mono)" font-size="9" fill="#ffd600" font-weight="700">GUIA DE MONTAGEM E CHICOTES</text>
      </g>
      <!-- Flow arrow: Zone 1 -> Zone 2 -->
      <g transform="translate(506, 250)">
        <line x1="0" y1="0" x2="24" y2="0" stroke="#00e676" stroke-width="3"/>
        <polygon points="24,-6 36,0 24,6" fill="#00e676"/>
        <text x="18" y="-8" font-family="var(--font-mono)" font-size="7" fill="#00e676" text-anchor="middle">ENERGIA</text>
      </g>
      <!-- Flow arrow: Zone 2 -> Zone 3 -->
      <g transform="translate(1090, 458)">
        <line x1="0" y1="0" x2="0" y2="22" stroke="#ff9100" stroke-width="3"/>
        <polygon points="-6,22 0,34 6,22" fill="#ff9100"/>
        <text x="14" y="18" font-family="var(--font-mono)" font-size="7" fill="#ff9100">PERFIL</text>
      </g>
    </g>

    <!-- ========================================================
         ZONA 1.1: ZONA ESQUERDA (X = 50 a 500, Y = 55 a 660)
         QUADRO DE FORÇA DIN + BOTOEIRA S0 NR-12 + NOTEBOOK HOST IA
         ======================================================== -->
    <g id="zone_1_left_control">
      <!-- 1.1.1 QUADRO DE COMANDO INDUSTRIAL (X=50, Y=55, W=450, H=390) -->
      <g id="group_painel_eletrico" transform="translate(50, 55)">
        <!-- Fundo e Borda do Armário Industrial -->
        <rect x="0" y="0" width="450" height="390" fill="#0d1612" stroke="#253a2e" stroke-width="2" rx="6"/>
        <!-- Barra de Cabeçalho do Quadro -->
        <rect x="0" y="0" width="450" height="28" fill="#15261d" stroke="#253a2e" stroke-width="1" rx="6 6 0 0"/>
        <text x="14" y="19" font-family="var(--font-mono)" font-size="11" fill="#00e5ff" font-weight="700">QUADRO DE FORÇA &amp; CONTROLE (TRILHO DIN TS-35)</text>
        <text x="436" y="19" font-family="var(--font-mono)" font-size="8" fill="#8fa699" text-anchor="end">MONTAGEM EM BANCADA / TRILHO DIN</text>

        <!-- ==========================================
             ANDAR SUPERIOR: ENTRADA AC & PROTEÇÃO NR-12
             ========================================== -->
        <!-- Perfil Metálico Trilho DIN 1 -->
        <rect x="15" y="65" width="420" height="18" fill="#1b2820" stroke="#334d3d"/>
        <text x="18" y="58" font-family="var(--font-mono)" font-size="8" fill="#5c7967" class="tech-only">TRILHO DIN 1: ENTRADA AC, PROTEÇÃO GERAL &amp; MONO-FONTE 12V PS1</text>
        <text x="18" y="58" font-family="var(--font-mono)" font-size="8" fill="#5c7967" class="public-label" style="display:none">ANDAR 1: ENTRADA DE ENERGIA E PROTECOES</text>

        <!-- Q0: Disjuntor Bipolar 10A Curva C -->
        <g transform="translate(20, 42)" class="cad-component-card" id="card_Q0">
          <rect x="0" y="0" width="48" height="66" fill="#16241c" stroke="#00e676" stroke-width="1.4" rx="3"/>
          <text x="24" y="15" font-family="var(--font-mono)" font-size="10" fill="#fff" font-weight="700" text-anchor="middle" class="tech-only">Q0</text>
          <text x="24" y="15" font-family="var(--font-mono)" font-size="9" fill="#fff" font-weight="700" text-anchor="middle" class="public-label" style="display:none">Disjuntor</text>
          <text x="24" y="27" font-family="var(--font-mono)" font-size="7" fill="#00e676" text-anchor="middle" class="tech-only">10A 2P</text>
          <rect x="10" y="33" width="28" height="22" fill="#0b120e" stroke="#2d4234"/>
          <line x1="24" y1="36" x2="24" y2="52" stroke="#ff80ab" stroke-width="2"/>
          <text x="24" y="62" font-family="var(--font-mono)" font-size="6" fill="#8fa699" text-anchor="middle">Curva C</text>
        </g>

        <!-- S_MAIN: Filtro RFI/EMI + Chave Geral -->
        <g transform="translate(74, 42)" class="cad-component-card" id="card_S_MAIN">
          <rect x="0" y="0" width="52" height="66" fill="#16241c" stroke="#00e5ff" stroke-width="1.4" rx="3"/>
          <text x="26" y="15" font-family="var(--font-mono)" font-size="9" fill="#fff" font-weight="700" text-anchor="middle" class="tech-only">S_MAIN</text>
          <text x="26" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" font-weight="700" text-anchor="middle" class="public-label" style="display:none">Filtro</text>
          <text x="26" y="26" font-family="var(--font-mono)" font-size="7" fill="#00e5ff" text-anchor="middle" class="tech-only">FILTRO RFI</text>
          <text x="26" y="26" font-family="var(--font-mono)" font-size="7" fill="#00e5ff" text-anchor="middle" class="public-label" style="display:none">Liga/Desliga</text>
          <rect x="8" y="32" width="36" height="18" fill="#101e16" stroke="#00e5ff" rx="2"/>
          <line x1="14" y1="41" x2="38" y2="41" stroke="#00e676" stroke-width="2"/>
          <circle cx="14" cy="41" r="2" fill="#fff"/>
          <circle cx="38" cy="41" r="2" fill="#fff"/>
          <text x="26" y="61" font-family="var(--font-mono)" font-size="6" fill="#8fa699" text-anchor="middle">10A / IEC</text>
        </g>

        <!-- PS1: Fonte Colmeia 12V 10A (120W) — MONO-FONTE PRINCIPAL -->
        <g transform="translate(134, 40)" class="cad-component-card" id="card_PS1">
          <rect x="0" y="0" width="168" height="70" fill="#18221b" stroke="#ff3344" stroke-width="1.8" rx="4"/>
          <text x="10" y="16" font-family="var(--font-mono)" font-size="10" fill="#fff" font-weight="700" class="tech-only">PS1: MONO-FONTE 12V 10A</text>
          <text x="10" y="16" font-family="var(--font-mono)" font-size="10" fill="#fff" font-weight="700" class="public-label" style="display:none">FONTE DE ENERGIA 12V</text>
          <text x="10" y="28" font-family="var(--font-sans)" font-size="8" fill="#ff8a80" class="tech-only">120W Colmeia Industrial (Fonte Única)</text>
          <text x="10" y="28" font-family="var(--font-sans)" font-size="8" fill="#ff8a80" class="public-label" style="display:none">Alimenta toda a bancada</text>
          <!-- Terminais da Fonte PS1 -->
          <g transform="translate(10, 40)">
            <rect x="0" y="0" width="25" height="24" fill="#0d1712" stroke="#253a2f" rx="1"/>
            <text x="12.5" y="16" font-family="var(--font-mono)" font-size="7.5" fill="#ff80ab" text-anchor="middle">L</text>
            <rect x="30" y="0" width="25" height="24" fill="#0d1712" stroke="#253a2f" rx="1"/>
            <text x="42.5" y="16" font-family="var(--font-mono)" font-size="7.5" fill="#80d8ff" text-anchor="middle">N</text>
            <rect x="60" y="0" width="25" height="24" fill="#0d1712" stroke="#253a2f" rx="1"/>
            <text x="72.5" y="16" font-family="var(--font-mono)" font-size="7.5" fill="#c6ff00" text-anchor="middle">PE</text>
            <rect x="90" y="0" width="27" height="24" fill="#0d1712" stroke="#253a2f" rx="1"/>
            <text x="103.5" y="16" font-family="var(--font-mono)" font-size="7.5" fill="#00e676" text-anchor="middle">-V (0V)</text>
            <rect x="122" y="0" width="27" height="24" fill="#0d1712" stroke="#253a2f" rx="1"/>
            <text x="135.5" y="16" font-family="var(--font-mono)" font-size="7.5" fill="#ff3344" text-anchor="middle">+V (12V)</text>
          </g>
        </g>

        <!-- F1: Fusível Geral 10A -->
        <g transform="translate(310, 42)" class="cad-component-card" id="card_F1">
          <rect x="0" y="0" width="46" height="66" fill="#18201a" stroke="#ff3344" stroke-width="1.4" rx="3"/>
          <text x="23" y="15" font-family="var(--font-mono)" font-size="10" fill="#fff" font-weight="700" text-anchor="middle" class="tech-only">F1</text>
          <text x="23" y="15" font-family="var(--font-mono)" font-size="9" fill="#fff" font-weight="700" text-anchor="middle" class="public-label" style="display:none">Fusivel</text>
          <text x="23" y="28" font-family="var(--font-mono)" font-size="8" fill="#ff8a80" text-anchor="middle" class="tech-only">10A</text>
          <rect x="10" y="34" width="26" height="18" fill="#101913" stroke="#ff3344" rx="2"/>
          <line x1="12" y1="43" x2="34" y2="43" stroke="#ff3344" stroke-width="2"/>
          <text x="23" y="61" font-family="var(--font-mono)" font-size="6" fill="#8fa699" text-anchor="middle">LÂMINA</text>
        </g>

        <!-- K1: Relé de Segurança Auxiliar NR-12 (40A) -->
        <g transform="translate(364, 40)" class="cad-component-card" id="card_K1">
          <rect x="0" y="0" width="70" height="70" fill="#1e1414" stroke="#ff1744" stroke-width="1.8" rx="4"/>
          <text x="35" y="16" font-family="var(--font-mono)" font-size="10" fill="#fff" font-weight="700" text-anchor="middle" class="tech-only">RELÉ K1</text>
          <text x="35" y="16" font-family="var(--font-mono)" font-size="9" fill="#fff" font-weight="700" text-anchor="middle" class="public-label" style="display:none">Rele Segur.</text>
          <text x="35" y="27" font-family="var(--font-mono)" font-size="7" fill="#ff8a80" text-anchor="middle" class="tech-only">12V / 40A</text>
          <rect x="10" y="33" width="50" height="22" fill="#0f1612" stroke="#ff1744" rx="2"/>
          <text x="35" y="47" font-family="var(--font-mono)" font-size="7" fill="#00e676" font-weight="700" text-anchor="middle" id="ov_k1_state">30-87 FECH</text>
          <text x="35" y="64" font-family="var(--font-mono)" font-size="6" fill="#ff8a80" text-anchor="middle">FAIL-SAFE</text>
        </g>

        <!-- ========================================================
             ANDAR CENTRAL: ELETRÔNICA DE CONTROLE E POTÊNCIA
             ======================================================== -->
        <!-- Perfil Metálico Trilho DIN 2 -->
        <rect x="15" y="160" width="420" height="18" fill="#1b2820" stroke="#334d3d"/>
        <text x="18" y="152" font-family="var(--font-mono)" font-size="8" fill="#5c7967" class="tech-only">TRILHO DIN 2: PROCESSAMENTO ESP32, BUCK CONVERTERS &amp; DRIVER DC</text>
        <text x="18" y="152" font-family="var(--font-mono)" font-size="8" fill="#5c7967" class="public-label" style="display:none">ANDAR 2: CONTROLADOR E CONVERSORES DE TENSAO</text>

        <!-- U1: ESP32 DevKit V1 (IO25:B1(S1) | IO26:B2(S2) [Clamp 3,3V]) -->
        <g transform="translate(20, 138)" class="cad-component-card" id="card_U1">
          <rect x="0" y="0" width="92" height="76" fill="#112217" stroke="#ffd600" stroke-width="1.8" rx="4"/>
          <text x="46" y="15" font-family="var(--font-mono)" font-size="10" fill="#fff" font-weight="700" text-anchor="middle" class="tech-only">U1: ESP32</text>
          <text x="46" y="15" font-family="var(--font-mono)" font-size="9" fill="#fff" font-weight="700" text-anchor="middle" class="public-label" style="display:none">Controlador</text>
          <text x="46" y="26" font-family="var(--font-mono)" font-size="7" fill="#ffd600" text-anchor="middle" class="tech-only">DevKit V1</text>
          <text x="46" y="26" font-family="var(--font-mono)" font-size="7" fill="#ffd600" text-anchor="middle" class="public-label" style="display:none">Cerebro da esteira</text>
          <!-- Antena PCB -->
          <rect x="26" y="30" width="40" height="12" fill="#1b2820" stroke="#3d5a47"/>
          <text x="46" y="39" font-family="var(--font-mono)" font-size="6" fill="#8fa699" text-anchor="middle">PCB ANT</text>
          <!-- LED GPIO 2 Heartbeat -->
          <circle cx="16" cy="51" r="3" fill="#00e5ff" id="ov_esp32_heartbeat"/>
          <text x="23" y="54" font-family="var(--font-mono)" font-size="5.5" fill="#00e5ff">GPIO 2</text>
          <!-- Entradas dos sensores B1(S1)/B2(S2) com Clamp 3,3V -->
          <text x="46" y="63" font-family="var(--font-mono)" font-size="4.6" fill="#00e676" text-anchor="middle" class="tech-only">IO25:B1(S1) | IO26:B2(S2) [Clamp 3,3V]</text>
          <text x="46" y="63" font-family="var(--font-mono)" font-size="5.5" fill="#00e676" text-anchor="middle" class="public-label" style="display:none">2 Sensores</text>
          <!-- Porta Micro-USB na base -->
          <rect x="33" y="67" width="26" height="7" fill="#253a2f" stroke="#fff" rx="1"/>
          <text x="46" y="73" font-family="var(--font-mono)" font-size="4.5" fill="#fff" text-anchor="middle">USB UART</text>
        </g>

        <!-- U2: Buck XL4015 (6,0V Servo + Cap 1000µF) -->
        <g transform="translate(122, 138)" class="cad-component-card" id="card_U2">
          <rect x="0" y="0" width="92" height="76" fill="#18221a" stroke="#ff9100" stroke-width="1.8" rx="4"/>
          <text x="46" y="15" font-family="var(--font-mono)" font-size="9" fill="#fff" font-weight="700" text-anchor="middle" class="tech-only">U2: BUCK 6V</text>
          <text x="46" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" font-weight="700" text-anchor="middle" class="public-label" style="display:none">Conv. 6V</text>
          <text x="46" y="26" font-family="var(--font-mono)" font-size="7" fill="#ff9100" text-anchor="middle" class="tech-only">XL4015 5A + C1</text>
          <text x="46" y="26" font-family="var(--font-mono)" font-size="7" fill="#ff9100" text-anchor="middle" class="public-label" style="display:none">p/ Empurrador</text>
          <circle cx="28" cy="42" r="10" fill="#101a14" stroke="#ff9100" stroke-width="1.2"/>
          <text x="28" y="44" font-family="var(--font-mono)" font-size="5" fill="#ff9100" text-anchor="middle">47µH</text>
          <!-- Capacitor 1000uF -->
          <circle cx="64" cy="42" r="9" fill="#122018" stroke="#ff9100" stroke-width="1.2"/>
          <text x="64" y="44" font-family="var(--font-mono)" font-size="5" fill="#fff" text-anchor="middle">1000µF</text>
          <rect x="10" y="57" width="72" height="15" fill="#0f1914" stroke="#253a2f" rx="2"/>
          <text x="46" y="68" font-family="var(--font-mono)" font-size="7" fill="#00e676" font-weight="700" text-anchor="middle">OUT: 6,00V</text>
        </g>

        <!-- U4: Buck MP1584 (5,0V ESP32 + Sensores IR 5V) -->
        <g transform="translate(224, 138)" class="cad-component-card" id="card_U4">
          <rect x="0" y="0" width="114" height="76" fill="#16221a" stroke="#ffd600" stroke-width="1.8" rx="4"/>
          <text x="57" y="15" font-family="var(--font-mono)" font-size="9" fill="#fff" font-weight="700" text-anchor="middle" class="tech-only">U4: BUCK 5V (ESP + SENS)</text>
          <text x="57" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" font-weight="700" text-anchor="middle" class="public-label" style="display:none">Conversor 5V</text>
          <text x="57" y="26" font-family="var(--font-mono)" font-size="7" fill="#ffd600" text-anchor="middle" class="tech-only">MP1584EN 2A Regulado</text>
          <text x="57" y="26" font-family="var(--font-mono)" font-size="7" fill="#ffd600" text-anchor="middle" class="public-label" style="display:none">p/ Controlador e Sensores</text>
          <rect x="15" y="33" width="84" height="20" fill="#0d1711" stroke="#334d3d" rx="2"/>
          <text x="57" y="45" font-family="var(--font-mono)" font-size="6" fill="#8fa699" text-anchor="middle">ALIM: ESP32 + 2x Sensores IR</text>
          <rect x="12" y="57" width="90" height="15" fill="#0f1914" stroke="#253a2f" rx="2"/>
          <text x="57" y="68" font-family="var(--font-mono)" font-size="7" fill="#ffd600" font-weight="700" text-anchor="middle">OUT: 5,02V (+5V_ESP)</text>
        </g>

        <!-- D4184: Driver MOSFET D4184 (Motor) -->
        <g transform="translate(348, 138)" class="cad-component-card" id="card_D4184">
          <rect x="0" y="0" width="86" height="76" fill="#18221b" stroke="#ff3344" stroke-width="1.8" rx="4"/>
          <text x="43" y="15" font-family="var(--font-mono)" font-size="9" fill="#fff" font-weight="700" text-anchor="middle" class="tech-only">D4184: MOSFET</text>
          <text x="43" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" font-weight="700" text-anchor="middle" class="public-label" style="display:none">Driver Motor</text>
          <text x="43" y="26" font-family="var(--font-mono)" font-size="7" fill="#ff8a80" text-anchor="middle" class="tech-only">AOD4184 15A</text>
          <rect x="12" y="32" width="62" height="20" fill="#0e1713" stroke="#253a2f" rx="2"/>
          <text x="43" y="44" font-family="var(--font-mono)" font-size="6" fill="#8fa699" text-anchor="middle">CHAVEIA M1</text>
          <rect x="10" y="57" width="66" height="15" fill="#0f1914" stroke="#ff3344" rx="2"/>
          <text x="43" y="68" font-family="var(--font-mono)" font-size="7" fill="#00e676" font-weight="700" text-anchor="middle" id="ov_mosfet_state">GATE ON</text>
        </g>

        <!-- ========================================================
             ANDAR INFERIOR: RÉGUAS DE BORNES DE PASSAGEM X1, X2, X3
             ======================================================== -->
        <!-- Perfil Metálico Trilho DIN 3 -->
        <rect x="15" y="255" width="420" height="18" fill="#1b2820" stroke="#334d3d"/>
        <text x="18" y="247" font-family="var(--font-mono)" font-size="8" fill="#5c7967" class="tech-only">TRILHO DIN 3: RÉGUAS DE BORNES MODULARES TS-35</text>
        <text x="18" y="247" font-family="var(--font-mono)" font-size="8" fill="#5c7967" class="public-label" style="display:none">ANDAR 3: REGUAS DE CONEXAO</text>

        <!-- Régua X1 (Alimentação & Barramentos - 10 Bornes) -->
        <g transform="translate(20, 235)" class="cad-component-card" id="card_X1">
          <rect x="0" y="0" width="132" height="60" fill="#122019" stroke="#00e5ff" stroke-width="1.5" rx="3"/>
          <text x="8" y="14" font-family="var(--font-mono)" font-size="9" fill="#00e5ff" font-weight="700">RÉGUA X1 (10x)</text>
          <text x="8" y="24" font-family="var(--font-mono)" font-size="6.5" fill="#8fa699">Alimentação &amp; Barramentos</text>
          <g transform="translate(6, 30)">
            <rect x="0" y="0" width="10" height="22" fill="#ff80ab" rx="1"/>
            <rect x="12" y="0" width="10" height="22" fill="#80d8ff" rx="1"/>
            <rect x="24" y="0" width="10" height="22" fill="#c6ff00" rx="1"/>
            <rect x="36" y="0" width="10" height="22" fill="#00e5ff" rx="1"/>
            <rect x="48" y="0" width="10" height="22" fill="#ff3344" rx="1"/>
            <rect x="60" y="0" width="10" height="22" fill="#ff1744" rx="1"/>
            <rect x="72" y="0" width="10" height="22" fill="#ff9100" rx="1"/>
            <rect x="84" y="0" width="10" height="22" fill="#ffd600" rx="1"/>
            <rect x="96" y="0" width="10" height="22" fill="#00e676" rx="1"/>
            <rect x="108" y="0" width="10" height="22" fill="#00e676" rx="1"/>
          </g>
        </g>

        <!-- Régua X2 (Campo e Sensores IR Retangulares 5V / Botão S0 - 10 Bornes) -->
        <g transform="translate(160, 235)" class="cad-component-card" id="card_X2">
          <rect x="0" y="0" width="136" height="60" fill="#122019" stroke="#00e676" stroke-width="1.5" rx="3"/>
          <text x="8" y="14" font-family="var(--font-mono)" font-size="9" fill="#00e676" font-weight="700">RÉGUA X2 (10x)</text>
          <text x="8" y="24" font-family="var(--font-mono)" font-size="6.5" fill="#8fa699">Sensores IR Retangulares (5V) &amp; Botão S0</text>
          <g transform="translate(6, 30)">
            <rect x="0" y="0" width="10" height="22" fill="#ffd600" rx="1"/>
            <rect x="12" y="0" width="10" height="22" fill="#29b6f6" rx="1"/>
            <rect x="24" y="0" width="10" height="22" fill="#fff" rx="1"/>
            <rect x="36" y="0" width="10" height="22" fill="#ffd600" rx="1"/>
            <rect x="48" y="0" width="10" height="22" fill="#29b6f6" rx="1"/>
            <rect x="60" y="0" width="10" height="22" fill="#fff" rx="1"/>
            <rect x="72" y="0" width="10" height="22" fill="#ff1744" rx="1"/>
            <rect x="84" y="0" width="10" height="22" fill="#ff1744" rx="1"/>
            <rect x="96" y="0" width="10" height="22" fill="#b388ff" rx="1"/>
            <rect x="108" y="0" width="10" height="22" fill="#b388ff" rx="1"/>
          </g>
        </g>

        <!-- Régua X3 (Atuadores e Cúpula - 8 Bornes) -->
        <g transform="translate(304, 235)" class="cad-component-card" id="card_X3">
          <rect x="0" y="0" width="132" height="60" fill="#122019" stroke="#ff9100" stroke-width="1.5" rx="3"/>
          <text x="8" y="14" font-family="var(--font-mono)" font-size="9" fill="#ff9100" font-weight="700">RÉGUA X3 (8x)</text>
          <text x="8" y="24" font-family="var(--font-mono)" font-size="6.5" fill="#8fa699">Motor M1, Servo M2 &amp; Luz</text>
          <g transform="translate(6, 30)">
            <rect x="0" y="0" width="12" height="22" fill="#ff1744" rx="1"/>
            <rect x="15" y="0" width="12" height="22" fill="#8fa699" rx="1"/>
            <rect x="30" y="0" width="12" height="22" fill="#c6ff00" rx="1"/>
            <rect x="45" y="0" width="12" height="22" fill="#ff9100" rx="1"/>
            <rect x="60" y="0" width="12" height="22" fill="#00e676" rx="1"/>
            <rect x="75" y="0" width="12" height="22" fill="#d500f9" rx="1"/>
            <rect x="90" y="0" width="12" height="22" fill="#ff3344" rx="1"/>
            <rect x="105" y="0" width="12" height="22" fill="#00e676" rx="1"/>
          </g>
        </g>

        <!-- ========================================================
             BASE DO QUADRO ELÉTRICO: 5 PRENSA-CABOS NUMERADOS (PG1..PG5)
             ======================================================== -->
        <g transform="translate(0, 340)">
          <!-- Faixa Metálica da Base -->
          <rect x="0" y="0" width="450" height="50" fill="#0a120e" stroke="#253a2e" rx="0 0 6 6"/>
          <text x="225" y="12" font-family="var(--font-mono)" font-size="8" fill="#8fa699" text-anchor="middle" class="tech-only">SAÍDA DE CHICOTES POR PRENSA-CABOS INDUSTRIAIS (BASE DO PAINEL)</text>
          <text x="225" y="12" font-family="var(--font-mono)" font-size="8" fill="#8fa699" text-anchor="middle" class="public-label" style="display:none">SAIDA DOS CABOS (BASE DO PAINEL)</text>

          <!-- PG1: Entrada AC -->
          <g transform="translate(45, 20)">
            <circle cx="0" cy="10" r="10" fill="#1b2820" stroke="#ff80ab" stroke-width="1.5"/>
            <circle cx="0" cy="10" r="4" fill="#0a120e"/>
            <text x="0" y="30" font-family="var(--font-mono)" font-size="7" fill="#ff80ab" font-weight="700" text-anchor="middle">PG1</text>
            <text x="0" y="-3" font-family="var(--font-mono)" font-size="6" fill="#8fa699" text-anchor="middle">AC 127/220V</text>
          </g>

          <!-- PG2: CH-01 Sensores IR Retangulares (5V NPN) -->
          <g transform="translate(135, 20)">
            <circle cx="0" cy="10" r="10" fill="#1b2820" stroke="#00e5ff" stroke-width="1.5"/>
            <circle cx="0" cy="10" r="4" fill="#0a120e"/>
            <text x="0" y="30" font-family="var(--font-mono)" font-size="7" fill="#00e5ff" font-weight="700" text-anchor="middle">PG2</text>
            <text x="0" y="-3" font-family="var(--font-mono)" font-size="6" fill="#8fa699" text-anchor="middle">CH-01 (IR S1/S2)</text>
          </g>

          <!-- PG3: CH-02 Motor Esteira 12V -->
          <g transform="translate(225, 20)">
            <circle cx="0" cy="10" r="10" fill="#1b2820" stroke="#ff1744" stroke-width="1.5"/>
            <circle cx="0" cy="10" r="4" fill="#0a120e"/>
            <text x="0" y="30" font-family="var(--font-mono)" font-size="7" fill="#ff1744" font-weight="700" text-anchor="middle">PG3</text>
            <text x="0" y="-3" font-family="var(--font-mono)" font-size="6" fill="#8fa699" text-anchor="middle">CH-02 (M1)</text>
          </g>

          <!-- PG4: CH-03 Servo 6V + Ring Light -->
          <g transform="translate(315, 20)">
            <circle cx="0" cy="10" r="10" fill="#1b2820" stroke="#ff9100" stroke-width="1.5"/>
            <circle cx="0" cy="10" r="4" fill="#0a120e"/>
            <text x="0" y="30" font-family="var(--font-mono)" font-size="7" fill="#ff9100" font-weight="700" text-anchor="middle">PG4</text>
            <text x="0" y="-3" font-family="var(--font-mono)" font-size="6" fill="#8fa699" text-anchor="middle">CH-03 (M2/Luz)</text>
          </g>

          <!-- PG5: CH-04 Emergência S0 -->
          <g transform="translate(405, 20)">
            <circle cx="0" cy="10" r="10" fill="#1b2820" stroke="#ffd600" stroke-width="1.5"/>
            <circle cx="0" cy="10" r="4" fill="#0a120e"/>
            <text x="0" y="30" font-family="var(--font-mono)" font-size="7" fill="#ffd600" font-weight="700" text-anchor="middle">PG5</text>
            <text x="0" y="-3" font-family="var(--font-mono)" font-size="6" fill="#8fa699" text-anchor="middle">CH-04 (S0)</text>
          </g>
        </g>
      </g>

      <!-- 1.1.2 BOTOEIRA DE EMERGÊNCIA EXTERNA NR-12 S0 (X=50, Y=490, W=195, H=165) -->
      <g id="card_S0_conveyor" transform="translate(50, 490)" class="cad-component-card">
        <!-- Caixa Amarela Industrial NR-12 -->
        <rect x="0" y="0" width="195" height="165" fill="#fbc02d" stroke="#f57f17" stroke-width="2" rx="6"/>
        <rect x="8" y="24" width="179" height="133" fill="#141010" stroke="#d50000" stroke-width="1.2" rx="4"/>
        <text x="97" y="17" font-family="var(--font-mono)" font-size="9" fill="#000" font-weight="800" text-anchor="middle">BOTOEIRA S0 (NR-12)</text>
        
        <!-- Colarinho Amarelo com Inscrição Regulamentar -->
        <circle cx="97" cy="80" r="38" fill="#ffd600" stroke="#f57f17" stroke-width="2"/>
        <text x="97" y="52" font-family="var(--font-mono)" font-size="6.5" fill="#000" font-weight="800" text-anchor="middle">PARADA DE EMERGÊNCIA</text>
        <text x="97" y="112" font-family="var(--font-mono)" font-size="6.5" fill="#000" font-weight="800" text-anchor="middle">EMERGENCY STOP</text>

        <!-- Botão Cogumelo 22mm Vermelho Clicável -->
        <circle cx="97" cy="80" r="24" fill="#d50000" stroke="#ff1744" stroke-width="2.5" id="ov_estop_mushroom"/>
        <circle cx="97" cy="80" r="10" fill="#ff5252"/>
        <!-- Setas de Destravamento por Giro -->
        <path d="M 85 74 A 14 14 0 0 1 109 74" fill="none" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="3 2"/>
        <polygon points="110,72 113,76 107,76" fill="#fff"/>

        <!-- Indicação dos 2 Blocos de Contato Técnicos -->
        <g transform="translate(14, 126)">
          <rect x="0" y="0" width="78" height="24" fill="#1b1212" stroke="#ff1744" rx="2"/>
          <text x="39" y="11" font-family="var(--font-mono)" font-size="6.5" fill="#ff8a80" font-weight="700" text-anchor="middle" class="tech-only">NF (11-12)</text>
          <text x="39" y="11" font-family="var(--font-mono)" font-size="6.5" fill="#ff8a80" font-weight="700" text-anchor="middle" class="public-label" style="display:none">Corte</text>
          <text x="39" y="20" font-family="var(--font-mono)" font-size="6" fill="#00e676" text-anchor="middle" class="tech-only">Corta K1 (Pot)</text>
          <text x="39" y="20" font-family="var(--font-mono)" font-size="6" fill="#00e676" text-anchor="middle" class="public-label" style="display:none">Desliga motor</text>

          <rect x="88" y="0" width="78" height="24" fill="#1b1212" stroke="#b388ff" rx="2"/>
          <text x="127" y="11" font-family="var(--font-mono)" font-size="6.5" fill="#b388ff" font-weight="700" text-anchor="middle" class="tech-only">NA (13-14)</text>
          <text x="127" y="11" font-family="var(--font-mono)" font-size="6.5" fill="#b388ff" font-weight="700" text-anchor="middle" class="public-label" style="display:none">Alerta</text>
          <text x="127" y="20" font-family="var(--font-mono)" font-size="6" fill="#ffd600" text-anchor="middle" class="tech-only">Alerta GPIO 27</text>
          <text x="127" y="20" font-family="var(--font-mono)" font-size="6" fill="#ffd600" text-anchor="middle" class="public-label" style="display:none">Avisa o sistema</text>
        </g>
      </g>

      <!-- 1.1.3 ESTAÇÃO NOTEBOOK HOST — IA & DASHBOARD (X=265, Y=490, W=235, H=165) -->
      <g id="card_notebook_host" transform="translate(265, 490)">
        <rect x="0" y="0" width="235" height="165" fill="#111c16" stroke="#00e5ff" stroke-width="1.8" rx="6"/>
        <rect x="0" y="0" width="235" height="24" fill="#15261d" stroke="#253a2e" rx="6 6 0 0"/>
        <text x="12" y="16" font-family="var(--font-mono)" font-size="9" fill="#00e5ff" font-weight="700">ESTAÇÃO NOTEBOOK HOST (IA &amp; DASHBOARD)</text>

        <!-- Tela do Notebook com o Sistema AmazonVision 4.0 -->
        <g transform="translate(15, 32)">
          <rect x="0" y="0" width="205" height="85" fill="#0a120e" stroke="#253a2f" rx="3"/>
          <rect x="0" y="0" width="205" height="16" fill="#14261d" rx="3 3 0 0"/>
          <circle cx="8" cy="8" r="3" fill="#ff1744"/>
          <circle cx="16" cy="8" r="3" fill="#ffd600"/>
          <circle cx="24" cy="8" r="3" fill="#00e676"/>
          <text x="34" y="11" font-family="var(--font-mono)" font-size="7" fill="#00e5ff" font-weight="700">AmazonVision 4.0 — FastAPI + React</text>
          
          <!-- Mockup da Interface de IA -->
          <rect x="8" y="22" width="75" height="55" fill="#0e1713" stroke="#00e676" stroke-width="1" rx="2"/>
          <circle cx="45" cy="48" r="14" fill="#ff6d00"/>
          <rect x="25" y="28" width="40" height="40" fill="none" stroke="#00e5ff" stroke-width="1.2" stroke-dasharray="2 2"/>
          <text x="45" y="26" font-family="var(--font-mono)" font-size="6" fill="#00e5ff" text-anchor="middle">Tucumã 97.4%</text>

          <text x="90" y="32" font-family="var(--font-mono)" font-size="7" fill="#00e676" font-weight="700">STATUS: INFERÊNCIA ATIVA</text>
          <text x="90" y="44" font-family="var(--font-mono)" font-size="6.5" fill="#8fa699">• YOLOv8 / MobileNetV3: 30 FPS</text>
          <text x="90" y="55" font-family="var(--font-mono)" font-size="6.5" fill="#8fa699">• Latência Total: 32 ms</text>
          <text x="90" y="66" font-family="var(--font-mono)" font-size="6.5" fill="#00e5ff">• Serial: 115200 bps CP2102</text>
        </g>

        <!-- Base do Notebook e Teclado -->
        <g transform="translate(15, 122)">
          <rect x="0" y="0" width="205" height="34" fill="#1b2820" stroke="#334d3d" rx="2"/>
          <rect x="15" y="4" width="175" height="14" fill="#101913" stroke="#253a2f" rx="1"/>
          <rect x="75" y="21" width="55" height="10" fill="#14221a" stroke="#253a2f" rx="1"/>
        </g>

        <!-- Portas USB Laterais Destacadas -->
        <g transform="translate(225, 45)">
          <rect x="0" y="0" width="8" height="14" fill="#00e5ff" rx="1"/>
          <text x="-6" y="10" font-family="var(--font-mono)" font-size="6" fill="#00e5ff" text-anchor="end">USB 1 (CÂMERA)</text>
          <rect x="0" y="24" width="8" height="14" fill="#ffd600" rx="1"/>
          <text x="-6" y="34" font-family="var(--font-mono)" font-size="6" fill="#ffd600" text-anchor="end">USB 2 (ESP ✂️)</text>
        </g>
      </g>
    </g>

    <!-- ========================================================
         ZONA 1.2: ZONA DIREITA SUPERIOR (X = 540 a 1645, Y = 55 a 455)
         VISTA SUPERIOR (PLANTA BAIXA) DA ESTEIRA 700 mm MONTADA
         ======================================================== -->
    <g id="zone_2_conveyor_top">
      <!-- Container da Vista Superior -->
      <rect x="540" y="55" width="1105" height="400" fill="#0e1713" stroke="#253a2e" stroke-width="2" rx="6"/>
      <rect x="540" y="55" width="1105" height="28" fill="#15261d" stroke="#253a2e" stroke-width="1" rx="6 6 0 0"/>
      <text x="555" y="74" font-family="var(--font-mono)" font-size="11" fill="#00e676" font-weight="700">VISTA SUPERIOR (PLANTA BAIXA) — ESTEIRA SELETORA 700 mm (KIT 3D PETG / 86 ELOS MODULARES)</text>
      <text x="1630" y="74" font-family="var(--font-mono)" font-size="9" fill="#8fa699" text-anchor="end">ESCALA 1:1 mm (DIAGRAMÁTICA)</text>

      <!-- BANNER DE STATUS DO CICLO AUTOMÁTICO (INTEGRADO NO TOPO) -->
      <g transform="translate(555, 88)" id="cycle_status_banner_group">
        <rect x="0" y="0" width="1075" height="30" fill="#13231a" stroke="#00e5ff" stroke-width="1.5" rx="4"/>
        <circle cx="18" cy="15" r="7" fill="#00e676" id="cycle_pulse_dot"/>
        <text x="35" y="19" font-family="var(--font-mono)" font-size="9.5" fill="#fff" font-weight="700" id="cycle_banner_title">FLUXO NOMINAL DE INSPEÇÃO: ENTRADA (-350 mm) ➔ VISÃO S1 (-150 mm) ➔ DESVIO S2 (+100 mm) ➔ EMPURRADOR M2 (+160 mm)</text>
        <text x="1062" y="19" font-family="var(--font-mono)" font-size="9.5" fill="#00e5ff" font-weight="700" text-anchor="end" id="cycle_step_text">CADÊNCIA: 45 FRUTOS/MIN (v = 0,18 m/s)</text>
      </g>

      <!-- ========================================================
           GRUPO DA ESTEIRA SELETORA EM PLANTA BAIXA (ORIGEM: X=640, Y=165)
           ======================================================== -->
      <g transform="translate(640, 165)" id="group_esteira_top_view">
        <!-- 1. RÉGUA DE COORDENADAS DE PROJETO (X = -350 mm a X = +350 mm) -->
        <g id="cad_top_ruler" transform="translate(0, 10)">
          <line x1="30" y1="0" x2="710" y2="0" stroke="#3d5a47" stroke-width="1.5"/>
          <!-- Ticks da Régua -->
          <line x1="30" y1="-5" x2="30" y2="5" stroke="#00e676" stroke-width="2"/>
          <text x="30" y="-8" font-family="var(--font-mono)" font-size="7.5" fill="#00e676" text-anchor="middle">-350 mm (Entrada)</text>

          <line x1="180" y1="-5" x2="180" y2="5" stroke="#00e5ff" stroke-width="2"/>
          <text x="180" y="-8" font-family="var(--font-mono)" font-size="7.5" fill="#00e5ff" text-anchor="middle">-150 mm (Câmera S1)</text>

          <line x1="370" y1="-5" x2="370" y2="5" stroke="#8fa699" stroke-width="1.5"/>
          <text x="370" y="-8" font-family="var(--font-mono)" font-size="7.5" fill="#8fa699" text-anchor="middle">0 mm (Centro)</text>

          <line x1="440" y1="-5" x2="440" y2="5" stroke="#00e5ff" stroke-width="2"/>
          <text x="440" y="-8" font-family="var(--font-mono)" font-size="7.5" fill="#00e5ff" text-anchor="middle">+100 mm (Sensor S2)</text>

          <line x1="510" y1="-5" x2="510" y2="5" stroke="#ff9100" stroke-width="2"/>
          <text x="510" y="-8" font-family="var(--font-mono)" font-size="7.5" fill="#ff9100" text-anchor="middle">+160 mm (Empurrador M2)</text>

          <line x1="710" y1="-5" x2="710" y2="5" stroke="#00e676" stroke-width="2"/>
          <text x="710" y="-8" font-family="var(--font-mono)" font-size="7.5" fill="#00e676" text-anchor="middle">+350 mm (Saída)</text>
        </g>

        <!-- 2. CHASSI MODULAR PETG (01A–01F) E CORREIA TRANSPORTADORA -->
        <!-- Longarina Superior Estrutural PETG com Nervuras Treliçadas -->
        <g id="top_rail_upper">
          <rect x="15" y="26" width="700" height="14" fill="#18291f" stroke="#3d5a47" stroke-width="1.5" rx="2"/>
          <!-- Nervuras Treliçadas 3D -->
          <line x1="50" y1="26" x2="60" y2="40" stroke="#2d4536" stroke-width="1.2"/>
          <line x1="100" y1="26" x2="110" y2="40" stroke="#2d4536" stroke-width="1.2"/>
          <line x1="150" y1="26" x2="160" y2="40" stroke="#2d4536" stroke-width="1.2"/>
          <line x1="200" y1="26" x2="210" y2="40" stroke="#2d4536" stroke-width="1.2"/>
          <line x1="250" y1="26" x2="260" y2="40" stroke="#2d4536" stroke-width="1.2"/>
          <line x1="300" y1="26" x2="310" y2="40" stroke="#2d4536" stroke-width="1.2"/>
          <line x1="350" y1="26" x2="360" y2="40" stroke="#2d4536" stroke-width="1.2"/>
          <line x1="400" y1="26" x2="410" y2="40" stroke="#2d4536" stroke-width="1.2"/>
          <line x1="450" y1="26" x2="460" y2="40" stroke="#2d4536" stroke-width="1.2"/>
          <line x1="550" y1="26" x2="560" y2="40" stroke="#2d4536" stroke-width="1.2"/>
          <line x1="600" y1="26" x2="610" y2="40" stroke="#2d4536" stroke-width="1.2"/>
          <line x1="650" y1="26" x2="660" y2="40" stroke="#2d4536" stroke-width="1.2"/>
        </g>

        <!-- Longarina Inferior Estrutural PETG com Abertura de Descarte -->
        <g id="top_rail_lower">
          <!-- Trecho Esquerdo até Rampa -->
          <rect x="15" y="100" width="465" height="14" fill="#18291f" stroke="#3d5a47" stroke-width="1.5" rx="2"/>
          <!-- Trecho Direito pós Rampa -->
          <rect x="555" y="100" width="160" height="14" fill="#18291f" stroke="#3d5a47" stroke-width="1.5" rx="2"/>
          <!-- Abertura Lateral de Ejeção entre X=480 e X=555 -->
          <line x1="480" y1="100" x2="480" y2="114" stroke="#ff1744" stroke-width="2"/>
          <line x1="555" y1="100" x2="555" y2="114" stroke="#ff1744" stroke-width="2"/>
        </g>

        <!-- Correia Central de 86 Elos Plásticos Modulares (Largura Útil 122 mm / 60 px) -->
        <g id="ov_conveyor_belt_group">
          <rect x="30" y="40" width="680" height="60" fill="#0c1410" stroke="#1f3226" stroke-width="1.5" id="ov_conveyor_belt"/>
          <!-- Representação dos Elos Articulados Modulares com Pinos -->
          <line x1="60" y1="40" x2="60" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <line x1="90" y1="40" x2="90" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <line x1="120" y1="40" x2="120" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <line x1="150" y1="40" x2="150" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <line x1="210" y1="40" x2="210" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <line x1="240" y1="40" x2="240" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <line x1="270" y1="40" x2="270" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <line x1="300" y1="40" x2="300" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <line x1="330" y1="40" x2="330" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <line x1="360" y1="40" x2="360" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <line x1="390" y1="40" x2="390" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <line x1="420" y1="40" x2="420" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <line x1="470" y1="40" x2="470" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <line x1="560" y1="40" x2="560" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <line x1="590" y1="40" x2="590" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <line x1="620" y1="40" x2="620" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <line x1="650" y1="40" x2="650" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <line x1="680" y1="40" x2="680" y2="100" stroke="#18281e" stroke-width="1.5"/>
          <!-- Setas de Transporte Suave -->
          <text x="320" y="73" font-family="var(--font-mono)" font-size="8" fill="#2d4536" font-weight="700">FLUXO: v = 0,18 m/s ➔ ➔ ➔</text>
        </g>

        <!-- 3. PONTA ESQUERDA — ROLO MOVIDO TRASEIRO (02B) E ESTICADORES M5 (01G) -->
        <g id="top_tail_tensioner">
          <!-- Cilindro Rolo Movido 02B visto de cima -->
          <rect x="22" y="38" width="16" height="64" fill="#1e2c24" stroke="#4e6b5a" rx="3"/>
          <line x1="30" y1="20" x2="30" y2="120" stroke="#fff" stroke-width="2"/>
          <!-- Blocos Tensores 01G com Parafusos M5x40mm -->
          <rect x="10" y="20" width="22" height="14" fill="#253a2f" stroke="#00e676" rx="2"/>
          <line x1="0" y1="27" x2="10" y2="27" stroke="#00e676" stroke-width="2"/>
          <text x="8" y="16" font-family="var(--font-mono)" font-size="6" fill="#8fa699">M5×40</text>

          <rect x="10" y="106" width="22" height="14" fill="#253a2f" stroke="#00e676" rx="2"/>
          <line x1="0" y1="113" x2="10" y2="113" stroke="#00e676" stroke-width="2"/>
          <text x="8" y="130" font-family="var(--font-mono)" font-size="6" fill="#8fa699">M5×40</text>
        </g>

        <!-- 4. ESTAÇÃO 01: CÚPULA DE VISÃO (05A), WEBCAM, RING LIGHT E SENSOR S1 -->
        <g id="top_station_1_vision">
          <!-- Cúpula Translúcida 05A cobrindo a seção de inspeção -->
          <rect x="125" y="20" width="110" height="100" fill="rgba(0, 229, 255, 0.05)" stroke="#00e5ff" stroke-width="1.8" stroke-dasharray="4 2" rx="6"/>
          <text x="180" y="34" font-family="var(--font-mono)" font-size="7.5" fill="#00e5ff" font-weight="700" text-anchor="middle">CÚPULA ÓPTICA 05A</text>

          <!-- Luminária Ring Light LED 12V 6000K -->
          <ellipse cx="180" cy="70" rx="36" ry="24" fill="#ffffff" stroke="#00e5ff" stroke-width="2" id="ov_ring_light"/>
          <ellipse cx="180" cy="70" rx="20" ry="12" fill="#0c1410"/>
          <text x="180" y="73" font-family="var(--font-mono)" font-size="6.5" fill="#000" font-weight="800" text-anchor="middle">RING LIGHT 6000K</text>

          <!-- Webcam Full HD 1080p Centralizada -->
          <rect x="170" y="60" width="20" height="20" fill="#1b2820" stroke="#fff" rx="3"/>
          <circle cx="180" cy="70" r="5" fill="#00e5ff" id="ov_camera_flash"/>
          <text x="180" y="56" font-family="var(--font-mono)" font-size="6" fill="#00e5ff" text-anchor="middle">CÂMERA 1080p</text>

          <!-- Sensor Óptico IR Retangular S1 (Gatilho de Câmera 5V NPN) -->
          <g transform="translate(162, 105)" class="cad-component-card" id="card_B1_conveyor">
            <rect x="0" y="0" width="36" height="42" fill="#16241c" stroke="#00e5ff" stroke-width="1.5" rx="3"/>
            <text x="18" y="12" font-family="var(--font-mono)" font-size="8" fill="#fff" font-weight="700" text-anchor="middle">S1</text>
            <circle cx="18" cy="22" r="3.5" fill="#00e676" id="ov_s1_sensor_led"/>
            <text x="18" y="35" font-family="var(--font-mono)" font-size="5.5" fill="#00e5ff" text-anchor="middle">IR 5V</text>
            <!-- Feixe Óptico Infravermelho S1 Cruzando a Esteira -->
            <line x1="18" y1="0" x2="18" y2="-65" stroke="#00e5ff" stroke-width="1.8" stroke-dasharray="3 3" id="ov_s1_beam"/>
          </g>
          <text x="180" y="158" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">Suporte 04A (Sensor S1)</text>
        </g>

        <!-- 5. ESTAÇÃO 02: SENSOR DE SINCRONISMO DE DESVIO S2 (B2) -->
        <g id="top_station_2_sensor">
          <!-- Sensor Óptico IR Retangular S2 (Gatilho Empurrador 5V NPN) -->
          <g transform="translate(422, 105)" class="cad-component-card" id="card_B2_conveyor">
            <rect x="0" y="0" width="36" height="42" fill="#16241c" stroke="#00e5ff" stroke-width="1.5" rx="3"/>
            <text x="18" y="12" font-family="var(--font-mono)" font-size="8" fill="#fff" font-weight="700" text-anchor="middle">S2</text>
            <circle cx="18" cy="22" r="3.5" fill="#1b2820" stroke="#00e676" id="ov_s2_sensor_led"/>
            <text x="18" y="35" font-family="var(--font-mono)" font-size="5.5" fill="#00e5ff" text-anchor="middle">IR 5V</text>
            <!-- Feixe Óptico S2 Cruzando a Esteira -->
            <line x1="18" y1="0" x2="18" y2="-65" stroke="#00e5ff" stroke-width="1.8" stroke-dasharray="3 3" id="ov_s2_beam"/>
          </g>
          <text x="440" y="158" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">Suporte 04A (Sensor S2)</text>
        </g>

        <!-- 6. ESTAÇÃO 03: MECANISMO EMPURRADOR LINEAR (M2) FORA DA FAIXA DA CORREIA -->
        <!-- Posicionado na parte externa superior (Y = -95 a 26) para ZERO OBSTRUÇÃO DA CORREIA -->
        <g id="card_M2_conveyor" transform="translate(415, -95)" class="cad-component-card">
          <rect x="0" y="0" width="190" height="120" fill="#101914" stroke="#ff9100" stroke-width="2" rx="4"/>
          <text x="95" y="16" font-family="var(--font-mono)" font-size="9" fill="#fff" font-weight="700" text-anchor="middle">M2: EMPURRADOR LINEAR</text>
          <text x="95" y="27" font-family="var(--font-mono)" font-size="7" fill="#ff9100" text-anchor="middle">Servo MG996R + Biela-Manivela</text>

          <!-- Corpo do Servomotor MG996R com Eixo Estriado -->
          <rect x="15" y="34" width="55" height="50" fill="#1a271f" stroke="#4e6b5a" rx="3"/>
          <circle cx="42" cy="59" r="13" fill="#0f1612" stroke="#ff9100" stroke-width="1.5"/>
          
          <!-- Disco Manivela Giratório (0° a 90°) -->
          <g id="ov_crank_disc" transform="translate(42, 59)">
            <circle cx="0" cy="0" r="11" fill="#15241b" stroke="#00e5ff"/>
            <line x1="0" y1="0" x2="10" y2="0" stroke="#ff9100" stroke-width="3" id="ov_crank_pin_line"/>
            <circle cx="10" cy="0" r="2.5" fill="#fff"/>
          </g>

          <!-- Biela de Conexão Articulada -->
          <line id="ov_connecting_rod" x1="52" y1="59" x2="110" y2="59" stroke="#00e676" stroke-width="3.5" stroke-linecap="round"/>

          <!-- CONJUNTO MÓVEL: SAPATA EMPURRADORA CÔNCAVA (0 a 120 mm) -->
          <!-- Quando recolhida (0 mm): posicionada rente à borda superior da esteira (Y=26) -->
          <g id="ov_pusher_shoe_group" transform="translate(0, 0)">
            <!-- Guias Lineares Ø4 mm e Buchas LM4UU -->
            <rect x="105" y="50" width="22" height="18" fill="#1f3026" stroke="#4e6b5a" rx="2"/>
            <line x1="85" y1="59" x2="175" y2="59" stroke="#486151" stroke-width="1" stroke-dasharray="2 2"/>
            
            <!-- Sapata Empurradora Côncava em Acrílico Laranja -->
            <rect x="127" y="27" width="16" height="65" fill="rgba(255, 145, 0, 0.45)" stroke="#ff9100" stroke-width="2" rx="3"/>
            <text x="135" y="62" font-family="var(--font-mono)" font-size="6.5" fill="#fff" text-anchor="middle" transform="rotate(-90 135 62)">SAPATA</text>
          </g>

          <!-- Indicação de Curso Linear e Status -->
          <text x="95" y="98" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">Curso Linear: 0 a 120 mm</text>
          <text x="95" y="112" font-family="var(--font-mono)" font-size="8" fill="#00e676" font-weight="700" text-anchor="middle" id="ov_pusher_status_text">0 mm [RECOLHIDO]</text>
        </g>

        <!-- 7. SAÍDA LATERAL DE DESCARTE — RAMPA 25° (06A) + CAIXA COLETORA DE REJEITADOS (06B) -->
        <g id="top_reject_chute_and_bin" transform="translate(465, 114)">
          <!-- Rampa de Descarte Inclinada 25° (06A) -->
          <polygon points="15,0 90,0 95,35 10,35" fill="#221214" stroke="#ff1744" stroke-width="1.5"/>
          <text x="52" y="18" font-family="var(--font-mono)" font-size="7" fill="#ff1744" font-weight="700" text-anchor="middle">RAMPA 25° (06A)</text>
          <text x="52" y="28" font-family="var(--font-mono)" font-size="6" fill="#ff8a80" text-anchor="middle">DESCARTE REJEITOS</text>

          <!-- Caixa Coletora de Rejeitados (06B — Vermelha) -->
          <!-- O fruto animado cai em translate(510, 150), pousando exatamente no centro desta caixa -->
          <rect x="0" y="35" width="105" height="55" fill="#1e1012" stroke="#ff1744" stroke-width="2" rx="4"/>
          <rect x="0" y="35" width="105" height="15" fill="#2d1417" rx="4 4 0 0"/>
          <text x="52" y="46" font-family="var(--font-mono)" font-size="7" fill="#ff1744" font-weight="800" text-anchor="middle">CAIXA DE REJEITADOS (06B)</text>
          <text x="52" y="65" font-family="var(--font-mono)" font-size="7.5" fill="#ff8a80" font-weight="700" text-anchor="middle">[FRUTOS RUINS]</text>
          <text x="52" y="78" font-family="var(--font-mono)" font-size="6" fill="#8fa699" text-anchor="middle">Defeitos / Injúrias</text>
        </g>

        <!-- 8. PONTA DIREITA — TAMBOR MOTRIZ (02A) + TRANSMISSÃO GT2 + MOTOR M1 -->
        <!-- Posicionado na lateral externa superior (X=650..770, Y=-95..26) para ZERO COLISÃO COM A SAÍDA -->
        <g id="top_drive_and_motor">
          <!-- Tambor Motriz 02A no Chassi -->
          <rect x="702" y="38" width="16" height="64" fill="#1e2c24" stroke="#4e6b5a" rx="3"/>
          <line x1="710" y1="20" x2="710" y2="105" stroke="#fff" stroke-width="2"/>

          <!-- Transmissão Lateral GT2 e Motorredutor GA37 (M1) na Lateral Superior -->
          <g id="card_M1_conveyor" transform="translate(635, -95)" class="cad-component-card">
            <rect x="0" y="0" width="145" height="120" fill="#14241b" stroke="#ff1744" stroke-width="1.8" rx="4"/>
            <text x="72" y="16" font-family="var(--font-mono)" font-size="9" fill="#fff" font-weight="700" text-anchor="middle">M1: MOTORREDUTOR DC</text>
            <text x="72" y="27" font-family="var(--font-mono)" font-size="7" fill="#ff8a80" text-anchor="middle">GA37 12V 60RPM (Alto Torque)</text>

            <!-- Correia Dentada GT2 e Polias 20T/40T -->
            <rect x="15" y="34" width="55" height="42" fill="#16221a" stroke="#253a2f" rx="3"/>
            <circle cx="30" cy="55" r="10" fill="#1b3022" stroke="#00e676" stroke-width="1.2"/>
            <text x="30" y="57" font-family="var(--font-mono)" font-size="6" fill="#00e676" text-anchor="middle">20T</text>
            <circle cx="58" cy="55" r="14" fill="#1b3022" stroke="#00e676" stroke-width="1.2"/>
            <text x="58" y="57" font-family="var(--font-mono)" font-size="6" fill="#00e676" text-anchor="middle">40T</text>
            <path d="M 30 45 L 58 41 A 14 14 0 0 1 58 69 L 30 65 A 10 10 0 0 1 30 45" fill="none" stroke="#ffd600" stroke-width="1.5"/>

            <!-- Engrenagem Animada do Motor -->
            <g id="ov_motor_gear_spin" transform="translate(108, 55)">
              <g id="ov_motor_gear">
                <circle cx="0" cy="0" r="18" fill="#1b3022" stroke="#00e676" stroke-width="1.8"/>
                <line x1="-14" y1="0" x2="14" y2="0" stroke="#00e676" stroke-width="2"/>
                <line x1="0" y1="-14" x2="0" y2="14" stroke="#00e676" stroke-width="2"/>
                <circle cx="0" cy="0" r="5" fill="#fff"/>
              </g>
            </g>
            <text x="108" y="80" font-family="var(--font-mono)" font-size="6" fill="#8fa699" text-anchor="middle">Redução 2:1</text>
            <text x="72" y="98" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">Velocidade: 30 RPM na Esteira</text>
            <text x="72" y="112" font-family="var(--font-mono)" font-size="8" fill="#00e676" font-weight="700" text-anchor="middle" id="ov_motor_status_text">STATUS: RODANDO (1.2A)</text>
          </g>

          <!-- SAÍDA FRONTAL LIVRE — CAIXA COLETORA DE APROVADOS (06B — VERDE) -->
          <!-- O fruto animado viaja até translate(740, 70) e cai perfeitamente dentro desta caixa -->
          <g id="top_approved_exit_and_bin" transform="translate(718, 40)">
            <!-- Rampa Frontal de Aprovados -->
            <polygon points="0,5 25,5 30,55 0,55" fill="#14261b" stroke="#00e676" stroke-width="1.5"/>
            <text x="15" y="32" font-family="var(--font-mono)" font-size="7" fill="#00e676" font-weight="700">RAMPA</text>

            <!-- Caixa Coletora de Aprovados (06B — Verde) -->
            <rect x="25" y="0" width="95" height="60" fill="#0e2015" stroke="#00e676" stroke-width="2" rx="4"/>
            <rect x="25" y="0" width="95" height="15" fill="#163422" rx="4 4 0 0"/>
            <text x="72" y="11" font-family="var(--font-mono)" font-size="7" fill="#00e676" font-weight="800" text-anchor="middle">CAIXA DE APROVADOS (06B)</text>
            <text x="72" y="32" font-family="var(--font-mono)" font-size="8" fill="#00e676" font-weight="700" text-anchor="middle">[FRUTOS BONS]</text>
            <text x="72" y="46" font-family="var(--font-mono)" font-size="6.5" fill="#80e8aa" text-anchor="middle">Tucumã / Castanha</text>
            <text x="72" y="55" font-family="var(--font-mono)" font-size="6" fill="#8fa699" text-anchor="middle">Classe A Comercial</text>
          </g>
        </g>

        <!-- 9. FRUTO INTERATIVO ANIMADO NA ESTEIRA (TUCUMÃ / DEFEITO) -->
        <!-- Manipulado pelo JS: (30,70) -> (180,70) -> (440,70) -> Good:(740,70) / Bad:(510,150) -->
        <g id="ov_animated_fruit" transform="translate(30, 70)">
          <circle cx="15" cy="15" r="14" fill="#ff6d00" stroke="#ffd600" stroke-width="2" id="ov_fruit_body"/>
          <circle cx="12" cy="11" r="3.5" fill="#ffe082"/>
          <text x="15" y="18" font-family="var(--font-mono)" font-size="6" fill="#000" font-weight="800" text-anchor="middle" id="ov_fruit_label">FRUTO</text>
        </g>
      </g>
    </g>

    <!-- ========================================================
         ZONA 1.3: ZONA DIREITA INFERIOR (X = 540 a 1645, Y = 490 a 660)
         VISTA EM ELEVAÇÃO LATERAL (PERFIL LONGITUDINAL) DO PROJETO MONTADO
         ======================================================== -->
    <g id="zone_3_conveyor_profile">
      <!-- Container da Vista Lateral -->
      <rect x="540" y="490" width="1105" height="170" fill="#0e1713" stroke="#253a2e" stroke-width="2" rx="6"/>
      <rect x="540" y="490" width="1105" height="24" fill="#15261d" stroke="#253a2e" stroke-width="1" rx="6 6 0 0"/>
      <text x="555" y="506" font-family="var(--font-mono)" font-size="10" fill="#00e5ff" font-weight="700">VISTA EM ELEVAÇÃO LATERAL (PERFIL LONGITUDINAL) — MONTAGEM NA BANCADA COM PÉS 01H E SAPATAS TPU 01I</text>
      <text x="1630" y="506" font-family="var(--font-mono)" font-size="8" fill="#8fa699" text-anchor="end">ALINHADA HORIZONTALMENTE COM A VISTA SUPERIOR</text>

      <!-- TAMPO DA BANCADA INDUSTRIAL DE TESTES NA BASE (Y = 646) -->
      <g id="table_surface">
        <rect x="555" y="644" width="1075" height="10" fill="#1a251f" stroke="#334d3d" rx="2"/>
        <line x1="555" y1="644" x2="1630" y2="644" stroke="#486854" stroke-width="1.5"/>
        <text x="565" y="652" font-family="var(--font-mono)" font-size="7" fill="#5c7967">BANCADA DE APOIO INDUSTRIAL (TAMPÃO 30 mm COM PONTOS DE FIXAÇÃO M6)</text>
      </g>

      <!-- ELEMENTOS EM ELEVAÇÃO (ALINHADOS COM X_ORIGIN = 640) -->
      <g transform="translate(640, 490)">
        <!-- 4 PARES DE PÉS DE SUSTENTAÇÃO (01H) COM SAPATAS TPU (01I) -->
        <!-- Pé 1 (Ponta Traseira X = 30) -->
        <g transform="translate(30, 60)">
          <rect x="-6" y="0" width="12" height="94" fill="#1f3226" stroke="#4e6b5a" rx="2"/>
          <line x1="0" y1="5" x2="0" y2="90" stroke="#2a4534" stroke-width="1.5"/>
          <!-- Sapata Antivibração TPU 01I Laranja -->
          <rect x="-10" y="86" width="20" height="8" fill="#ff9100" stroke="#ffd600" rx="2"/>
          <text x="0" y="102" font-family="var(--font-mono)" font-size="6" fill="#ff9100" text-anchor="middle">01I TPU</text>
        </g>

        <!-- Pé 2 (Cúpula de Visão X = 180) -->
        <g transform="translate(180, 60)">
          <rect x="-6" y="0" width="12" height="94" fill="#1f3226" stroke="#4e6b5a" rx="2"/>
          <line x1="0" y1="5" x2="0" y2="90" stroke="#2a4534" stroke-width="1.5"/>
          <!-- Sapata Antivibração TPU 01I Ciano -->
          <rect x="-10" y="86" width="20" height="8" fill="#00e5ff" stroke="#fff" rx="2"/>
          <text x="0" y="102" font-family="var(--font-mono)" font-size="6" fill="#00e5ff" text-anchor="middle">01I TPU</text>
        </g>

        <!-- Pé 3 (Apoio Central / S2 X = 440) -->
        <g transform="translate(440, 60)">
          <rect x="-6" y="0" width="12" height="94" fill="#1f3226" stroke="#4e6b5a" rx="2"/>
          <line x1="0" y1="5" x2="0" y2="90" stroke="#2a4534" stroke-width="1.5"/>
          <!-- Sapata TPU Laranja -->
          <rect x="-10" y="86" width="20" height="8" fill="#ff9100" stroke="#ffd600" rx="2"/>
          <text x="0" y="102" font-family="var(--font-mono)" font-size="6" fill="#ff9100" text-anchor="middle">01I TPU</text>
        </g>

        <!-- Pé 4 (Ponta Dianteira Tração X = 710) -->
        <g transform="translate(710, 60)">
          <rect x="-6" y="0" width="12" height="94" fill="#1f3226" stroke="#4e6b5a" rx="2"/>
          <line x1="0" y1="5" x2="0" y2="90" stroke="#2a4534" stroke-width="1.5"/>
          <!-- Sapata TPU Ciano -->
          <rect x="-10" y="86" width="20" height="8" fill="#00e5ff" stroke="#fff" rx="2"/>
          <text x="0" y="102" font-family="var(--font-mono)" font-size="6" fill="#00e5ff" text-anchor="middle">01I TPU</text>
        </g>

        <!-- PERFIL DA LONGARINA LONGITUDINAL PETG (01A–01F) -->
        <rect x="20" y="55" width="700" height="24" fill="#16241c" stroke="#3d5a47" stroke-width="1.8" rx="3"/>
        <text x="370" y="70" font-family="var(--font-mono)" font-size="7.5" fill="#5c7967" text-anchor="middle">LONGARINAS PETG ESTRUTURAIS 700 mm COM APOIOS INTERNOS (ALTURA ÚTIL = 120 mm)</text>

        <!-- LOOP FECHADO DA CORREIA MODULAR DE 86 ELOS -->
        <!-- Ramo Superior de Transporte (Horizontal a Y = 52) -->
        <line x1="30" y1="52" x2="710" y2="52" stroke="#00e676" stroke-width="3"/>
        <!-- Ramo Inferior de Retorno com Apoios e Curvatura Suave -->
        <path d="M 30 78 Q 200 84 370 80 Q 540 84 710 78" fill="none" stroke="#2a4534" stroke-width="2.5" stroke-dasharray="6 3"/>

        <!-- Rolo Movido Traseiro 02B (Ø40 mm) -->
        <circle cx="30" cy="65" r="14" fill="#101913" stroke="#4e6b5a" stroke-width="2"/>
        <circle cx="30" cy="65" r="4" fill="#fff"/>
        <text x="30" y="44" font-family="var(--font-mono)" font-size="6.5" fill="#8fa699" text-anchor="middle">Rolo 02B</text>

        <!-- Rolo Central de Apoio 02C (X = 370) -->
        <circle cx="370" cy="78" r="8" fill="#101913" stroke="#4e6b5a" stroke-width="1.5"/>
        <circle cx="370" cy="78" r="2.5" fill="#fff"/>

        <!-- Tambor Motriz Dianteiro 02A (Ø40 mm) -->
        <circle cx="710" cy="65" r="14" fill="#101913" stroke="#ff1744" stroke-width="2"/>
        <circle cx="710" cy="65" r="4" fill="#fff"/>
        <text x="710" y="44" font-family="var(--font-mono)" font-size="6.5" fill="#ff8a80" text-anchor="middle">Tambor 02A</text>

        <!-- ELEVAÇÃO DA CÚPULA ÓPTICA 05A (X = 180) -->
        <g transform="translate(180, 52)">
          <!-- Perfil da Cúpula Semicircular Branca Fosca -->
          <path d="M -45 0 L -45 -35 Q 0 -50 45 -35 L 45 0 Z" fill="rgba(255, 255, 255, 0.08)" stroke="#00e5ff" stroke-width="1.5"/>
          <!-- Webcam 1080p e Altura Focal de 180 mm -->
          <rect x="-10" y="-48" width="20" height="12" fill="#1b2820" stroke="#fff" rx="2"/>
          <line x1="-30" y1="-42" x2="-30" y2="0" stroke="#ffd600" stroke-width="1" stroke-dasharray="2 2"/>
          <text x="-35" y="-20" font-family="var(--font-mono)" font-size="6" fill="#ffd600" text-anchor="end">Foco = 180mm</text>
          <!-- Feixe Cônico Uniforme da Ring Light 6000K -->
          <polygon points="-8,-36 8,-36 35,0 -35,0" fill="rgba(255, 255, 255, 0.12)"/>
          <text x="0" y="-12" font-family="var(--font-mono)" font-size="6" fill="#fff" font-weight="700" text-anchor="middle">LUZ 6000K</text>
          <!-- Fruto de teste sendo inspecionado sob a cúpula -->
          <circle cx="0" cy="-6" r="8" fill="#ff6d00" stroke="#ffd600" stroke-width="1.2"/>
        </g>

        <!-- RAMPA DE DESCARTE LATERAL 06A EM ELEVAÇÃO (X = 510) -->
        <g transform="translate(510, 52)">
          <line x1="0" y1="0" x2="35" y2="35" stroke="#ff1744" stroke-width="3"/>
          <text x="40" y="24" font-family="var(--font-mono)" font-size="6.5" fill="#ff1744" font-weight="700">Rampa 25°</text>
          <!-- Caixa Coletora de Rejeitados Apoiada na Bancada -->
          <rect x="25" y="40" width="45" height="52" fill="#1a1012" stroke="#ff1744" stroke-width="1.5" rx="3"/>
          <text x="47" y="65" font-family="var(--font-mono)" font-size="6" fill="#ff1744" font-weight="700" text-anchor="middle">REJEITADOS</text>
        </g>

        <!-- SAÍDA FRONTAL E CAIXA DE APROVADOS APOIADA NA BANCADA (X = 740) -->
        <g transform="translate(725, 52)">
          <line x1="0" y1="0" x2="20" y2="15" stroke="#00e676" stroke-width="2.5"/>
          <!-- Caixa Coletora de Aprovados Apoiada na Bancada -->
          <rect x="20" y="25" width="55" height="67" fill="#0d1f14" stroke="#00e676" stroke-width="1.8" rx="3"/>
          <text x="47" y="55" font-family="var(--font-mono)" font-size="6.5" fill="#00e676" font-weight="700" text-anchor="middle">APROVADOS</text>
          <text x="47" y="68" font-family="var(--font-mono)" font-size="5.5" fill="#a5d6a7" text-anchor="middle">(FRUTOS BONS)</text>
        </g>
      </g>
    </g>

    <!-- ========================================================
         ZONA 1.4: ROTEAMENTO LIMPO DOS CHICOTES (ELETROCALHA Y = 465)
         E GUIA DE MONTAGEM NO RODAPÉ (X = 50 a 1055, Y = 680 a 935)
         ======================================================== -->

    <!-- ELETROCALHA HORIZONTAL PRINCIPAL DE DISTRIBUIÇÃO (Y = 465) -->
    <g id="cable_tray_trunk">
      <rect x="50" y="462" width="1595" height="14" fill="#131e18" stroke="#253a2f" stroke-width="1.2" rx="2"/>
      <line x1="50" y1="469" x2="1645" y2="469" stroke="#1d2d24" stroke-dasharray="6 4"/>
      <text x="545" y="473" font-family="var(--font-mono)" font-size="7" fill="#4d6b59">ELETROCALHA DE DISTRIBUIÇÃO DEDICADA — ROTEAMENTO 100% ORTOGONAL DOS CHICOTES DA BANCADA</text>
    </g>

    <!-- CHICOTES DE INTERLIGAÇÃO INDUSTRIAIS COM IDS PRESERVADOS -->
    <g id="overview_interconnection_wires">
      <!-- CH-01: Cabo dos Sensores S1 e S2 (5V + Sinais NPN): Régua X2 / PG2 ➔ Sensores IR Retangulares 5V -->
      <path id="wire_ov_sensors" d="M 225 395 L 225 466 L 820 466 L 820 270" class="wire w-5v" stroke="#ffd600" stroke-dasharray="6 4"/>
      <!-- Derivação para Sensor S2 em X=1080 -->
      <path d="M 820 466 L 1080 466 L 1080 270" class="wire w-5v" stroke="#ffd600" stroke-dasharray="6 4"/>
      <circle cx="820" cy="466" r="3" class="wire-junction"/>

      <!-- CH-02: Cabo de Potência do Motor M1 (12V Atuadores): Régua X3 / PG3 ➔ Motorredutor GA37 -->
      <path id="wire_ov_motor" d="M 300 395 L 300 468 L 1380 468 L 1380 160 L 1345 160" class="wire w-12v-at" stroke-dasharray="6 4"/>

      <!-- CH-03: Cabo de Potência e PWM do Servo M2 (6V + PWM): Régua X3 / PG4 ➔ Empurrador Linear -->
      <path id="wire_ov_servo" d="M 380 395 L 380 470 L 1150 470 L 1150 160 L 1125 160" class="wire w-6v" stroke-dasharray="6 4"/>

      <!-- Cabo de Alimentação 12V da Ring Light: Régua X3 / PG4 ➔ Cúpula 05A -->
      <path d="M 380 470 L 800 470 L 800 235" class="wire w-12v-cont" stroke-dasharray="4 3"/>
      <circle cx="800" cy="470" r="2.5" class="wire-junction"/>

      <!-- CH-04: Cabo de Parada de Emergência S0 (NR-12): Botoeira S0 ➔ Régua X2 / PG5 -->
      <path d="M 147 490 L 147 472 L 455 472 L 455 395" class="wire" stroke="#ffd600" stroke-width="2"/>

      <!-- CH-05A: Cabo de Vídeo USB 2.0 da Webcam: Notebook Host ➔ Webcam 1080p Cúpula -->
      <path d="M 500 535 L 530 535 L 530 474 L 840 474 L 840 235" class="wire" stroke="#00e5ff" stroke-width="1.8"/>

      <!-- CH-05B: Cabo Serial Modificado (VBUS Cortado ✂️): Notebook Host ➔ Micro-USB ESP32 U1 -->
      <path d="M 500 550 L 520 550 L 520 464 L 115 464 L 115 270" class="wire" stroke="#ffd600" stroke-width="1.8" stroke-dasharray="5 3"/>
      <!-- Símbolo de Tesoura de Corte VBUS -->
      <g transform="translate(315, 464)">
        <circle cx="0" cy="0" r="7" fill="#1b1212" stroke="#ff1744" stroke-width="1"/>
        <text x="0" y="3" font-family="var(--font-mono)" font-size="9" fill="#ff1744" text-anchor="middle">✂️</text>
      </g>

      <!-- ANILHAS DE IDENTIFICAÇÃO DOS CHICOTES NA ELETROCALHA -->
      <g transform="translate(680, 461)">
        <rect x="0" y="-8" width="180" height="14" fill="#0d1712" stroke="#00e5ff" stroke-width="1" rx="2"/>
        <text x="90" y="2" font-family="var(--font-mono)" font-size="6.5" fill="#00e5ff" font-weight="700" text-anchor="middle">CH-01: Sensores IR Retangulares (5V + Sinais NPN)</text>
      </g>

      <g transform="translate(930, 461)">
        <rect x="0" y="-8" width="125" height="14" fill="#0d1712" stroke="#ff9100" stroke-width="1" rx="2"/>
        <text x="62" y="2" font-family="var(--font-mono)" font-size="6.5" fill="#ff9100" font-weight="700" text-anchor="middle">CH-03: Servo 6V + Ring</text>
      </g>

      <g transform="translate(1220, 461)">
        <rect x="0" y="-8" width="110" height="14" fill="#0d1712" stroke="#ff1744" stroke-width="1" rx="2"/>
        <text x="55" y="2" font-family="var(--font-mono)" font-size="6.5" fill="#ff1744" font-weight="700" text-anchor="middle">CH-02: Motor 12V</text>
      </g>
    </g>

    <!-- GUIA RÁPIDO DE COMISSIONAMENTO E TABELA DE CHICOTES NO RODAPÉ ESQUERDO (X = 50 a 1055, Y = 680 a 935) -->
    <g id="footer_commissioning_guide" transform="translate(50, 680)">
      <rect x="0" y="0" width="1005" height="255" fill="#0c1510" stroke="#253a2e" stroke-width="1.8" rx="6"/>
      <rect x="0" y="0" width="1005" height="26" fill="#15261d" stroke="#253a2e" stroke-width="1" rx="6 6 0 0"/>
      <text x="14" y="17" font-family="var(--font-mono)" font-size="10" fill="#00e5ff" font-weight="700">GUIA RÁPIDO DE MONTAGEM, LIGAÇÃO E IDENTIFICAÇÃO DOS 5 CHICOTES DA BANCADA INDUSTRIAL</text>
      <text x="990" y="17" font-family="var(--font-mono)" font-size="8" fill="#8fa699" text-anchor="end">CONFORME NBR 5410 &amp; NR-12</text>

      <!-- COLUNA 1: PASSO A PASSO DE ENERGIZAÇÃO E OPERAÇÃO (X = 15 a 470) -->
      <g transform="translate(15, 36)">
        <rect x="0" y="0" width="455" height="205" fill="#0f1914" stroke="#1d2e24" rx="4"/>
        <text x="12" y="18" font-family="var(--font-mono)" font-size="9" fill="#00e676" font-weight="700">PASSO A PASSO DE COMISSIONAMENTO DA BANCADA:</text>

        <g transform="translate(12, 32)">
          <!-- Passo 1 -->
          <circle cx="8" cy="8" r="7" fill="#162c1e" stroke="#00e676"/>
          <text x="8" y="11" font-family="var(--font-mono)" font-size="7.5" fill="#00e676" font-weight="700" text-anchor="middle">1</text>
          <text x="22" y="7" font-family="var(--font-mono)" font-size="7.5" fill="#fff" font-weight="700">FIXAÇÃO MECÂNICA E ATERRAMENTO PE:</text>
          <text x="22" y="18" font-family="var(--font-sans)" font-size="7" fill="#8fa699">Assentar os 4 pares de pés 01H com as sapatas TPU 01I na bancada. Interligar condutor PE ao trilho DIN.</text>

          <!-- Passo 2 -->
          <circle cx="8" cy="42" r="7" fill="#162c1e" stroke="#00e676"/>
          <text x="8" y="45" font-family="var(--font-mono)" font-size="7.5" fill="#00e676" font-weight="700" text-anchor="middle">2</text>
          <text x="22" y="41" font-family="var(--font-mono)" font-size="7.5" fill="#fff" font-weight="700">ENTRADA AC E FONTE MONO-FONTE PS1:</text>
          <text x="22" y="52" font-family="var(--font-sans)" font-size="7" fill="#8fa699">Energizar plugue NBR 14136, ligar disjuntor Q0 e chave S_MAIN. Checar LED de status da Fonte PS1 (12V 10A).</text>

          <!-- Passo 3 -->
          <circle cx="8" cy="76" r="7" fill="#162c1e" stroke="#00e676"/>
          <text x="8" y="79" font-family="var(--font-mono)" font-size="7.5" fill="#00e676" font-weight="700" text-anchor="middle">3</text>
          <text x="22" y="75" font-family="var(--font-mono)" font-size="7.5" fill="#fff" font-weight="700">ROTEAMENTO PELA ELETROCALHA:</text>
          <text x="22" y="86" font-family="var(--font-sans)" font-size="7" fill="#8fa699">Passar os chicotes CH-01 a CH-05 pelos prensa-cabos PG1-PG5 até os sensores, atuadores e notebook.</text>

          <!-- Passo 4 -->
          <circle cx="8" cy="110" r="7" fill="#162c1e" stroke="#ff1744"/>
          <text x="8" y="113" font-family="var(--font-mono)" font-size="7.5" fill="#ff1744" font-weight="700" text-anchor="middle">4</text>
          <text x="22" y="109" font-family="var(--font-mono)" font-size="7.5" fill="#fff" font-weight="700">TESTE DE SEGURANÇA NR-12 (BOTÃO S0 &amp; RELÉ K1):</text>
          <text x="22" y="120" font-family="var(--font-sans)" font-size="7" fill="#8fa699">Pressionar S0: K1 deve desarmar cortando +12V_AT instantaneamente. Girar S0 para rearmar.</text>

          <!-- Passo 5 -->
          <circle cx="8" cy="144" r="7" fill="#162c1e" stroke="#ffd600"/>
          <text x="8" y="147" font-family="var(--font-mono)" font-size="7.5" fill="#ffd600" font-weight="700" text-anchor="middle">5</text>
          <text x="22" y="143" font-family="var(--font-mono)" font-size="7.5" fill="#fff" font-weight="700">CONEXÃO IA NOTEBOOK HOST &amp; CICLO AUTOMÁTICO:</text>
          <text x="22" y="154" font-family="var(--font-sans)" font-size="7" fill="#8fa699">Conectar cabo serial isolado (sem VBUS) ao ESP32. Iniciar serviço FastAPI + Dashboard React e validar telemetria serial 115200 bps.</text>
        </g>
      </g>

      <!-- COLUNA 2: TABELA DE CHICOTES INDUSTRIAIS DA BANCADA (X = 485 a 990) -->
      <g transform="translate(485, 36)">
        <rect x="0" y="0" width="505" height="205" fill="#0f1914" stroke="#1d2e24" rx="4"/>
        <text x="12" y="18" font-family="var(--font-mono)" font-size="9" fill="#00e5ff" font-weight="700">TABELA DE ESPECIFICAÇÃO DOS 5 CHICOTES (DE-PARA):</text>

        <!-- Cabeçalho da Tabela -->
        <g transform="translate(10, 28)">
          <rect x="0" y="0" width="485" height="18" fill="#18281e" rx="2"/>
          <text x="8" y="12" font-family="var(--font-mono)" font-size="7" fill="#00e5ff" font-weight="700">CÓDIGO</text>
          <text x="65" y="12" font-family="var(--font-mono)" font-size="7" fill="#00e5ff" font-weight="700">CONDUTORES</text>
          <text x="150" y="12" font-family="var(--font-mono)" font-size="7" fill="#00e5ff" font-weight="700">ORIGEM ➔ DESTINO</text>
          <text x="290" y="12" font-family="var(--font-mono)" font-size="7" fill="#00e5ff" font-weight="700">TENSÃO</text>
          <text x="360" y="12" font-family="var(--font-mono)" font-size="7" fill="#00e5ff" font-weight="700">FUNÇÃO NO SISTEMA</text>
        </g>

        <!-- Linha 1: CH-01 Sensores IR Retangulares (5V NPN) -->
        <g transform="translate(10, 52)">
          <rect x="0" y="0" width="485" height="26" fill="#121e17" rx="2"/>
          <text x="8" y="17" font-family="var(--font-mono)" font-size="7.5" fill="#00e5ff" font-weight="700">CH-01</text>
          <text x="65" y="13" font-family="var(--font-mono)" font-size="7" fill="#fff">6x 0,5 mm²</text>
          <text x="65" y="22" font-family="var(--font-mono)" font-size="6" fill="#8fa699">BN(+5V),BU(0V),BK(NPN)</text>
          <text x="150" y="13" font-family="var(--font-mono)" font-size="7" fill="#fff">Régua X2 (PG2)</text>
          <text x="150" y="22" font-family="var(--font-mono)" font-size="6" fill="#8fa699">➔ Sensores B1(S1) e B2(S2)</text>
          <text x="290" y="17" font-family="var(--font-mono)" font-size="7.5" fill="#ffd600" font-weight="700">+5V DC</text>
          <text x="360" y="13" font-family="var(--font-sans)" font-size="6.5" fill="#e0e8e3">Alimentação 5V dos sensores reflexivos</text>
          <text x="360" y="22" font-family="var(--font-sans)" font-size="6" fill="#8fa699">e sinal NPN via R=1kΩ + Clamp BAT54S (3,3V) p/ GPIOs 25/26</text>
        </g>

        <!-- Linha 2: CH-02 Motor -->
        <g transform="translate(10, 82)">
          <rect x="0" y="0" width="485" height="26" fill="#121e17" rx="2"/>
          <text x="8" y="17" font-family="var(--font-mono)" font-size="7.5" fill="#ff1744" font-weight="700">CH-02</text>
          <text x="65" y="13" font-family="var(--font-mono)" font-size="7" fill="#fff">2x 1,0 mm² + PE</text>
          <text x="65" y="22" font-family="var(--font-mono)" font-size="6" fill="#8fa699">Vermelho / Preto</text>
          <text x="150" y="13" font-family="var(--font-mono)" font-size="7" fill="#fff">Régua X3 (PG3)</text>
          <text x="150" y="22" font-family="var(--font-mono)" font-size="6" fill="#8fa699">➔ Motorredutor M1</text>
          <text x="290" y="17" font-family="var(--font-mono)" font-size="7.5" fill="#ff1744" font-weight="700">+12V_AT</text>
          <text x="360" y="13" font-family="var(--font-sans)" font-size="6.5" fill="#e0e8e3">Alimentação seccionada por K1 e</text>
          <text x="360" y="22" font-family="var(--font-sans)" font-size="6" fill="#8fa699">chaveamento PWM por MOSFET D4184</text>
        </g>

        <!-- Linha 3: CH-03 Servo e Luz -->
        <g transform="translate(10, 112)">
          <rect x="0" y="0" width="485" height="26" fill="#121e17" rx="2"/>
          <text x="8" y="17" font-family="var(--font-mono)" font-size="7.5" fill="#ff9100" font-weight="700">CH-03</text>
          <text x="65" y="13" font-family="var(--font-mono)" font-size="7" fill="#fff">5x 0,75 mm²</text>
          <text x="65" y="22" font-family="var(--font-mono)" font-size="6" fill="#8fa699">Potência + Sinal</text>
          <text x="150" y="13" font-family="var(--font-mono)" font-size="7" fill="#fff">Régua X3 (PG4)</text>
          <text x="150" y="22" font-family="var(--font-mono)" font-size="6" fill="#8fa699">➔ Servo M2 / Cúpula</text>
          <text x="290" y="17" font-family="var(--font-mono)" font-size="7.5" fill="#ff9100" font-weight="700">+6V / +12V</text>
          <text x="360" y="13" font-family="var(--font-sans)" font-size="6.5" fill="#e0e8e3">Alimentação 6,0V Buck Servo + PWM</text>
          <text x="360" y="22" font-family="var(--font-sans)" font-size="6" fill="#8fa699">e 12V contínuo da Ring Light 6000K</text>
        </g>

        <!-- Linha 4: CH-04 Emergência S0 -->
        <g transform="translate(10, 142)">
          <rect x="0" y="0" width="485" height="26" fill="#121e17" rx="2"/>
          <text x="8" y="17" font-family="var(--font-mono)" font-size="7.5" fill="#ffd600" font-weight="700">CH-04</text>
          <text x="65" y="13" font-family="var(--font-mono)" font-size="7" fill="#fff">4x 0,5 mm²</text>
          <text x="65" y="22" font-family="var(--font-mono)" font-size="6" fill="#8fa699">2x Verm, 2x Roxo</text>
          <text x="150" y="13" font-family="var(--font-mono)" font-size="7" fill="#fff">Régua X2 (PG5)</text>
          <text x="150" y="22" font-family="var(--font-mono)" font-size="6" fill="#8fa699">➔ Botoeira S0</text>
          <text x="290" y="17" font-family="var(--font-mono)" font-size="7.5" fill="#ffd600" font-weight="700">12V / 3,3V</text>
          <text x="360" y="13" font-family="var(--font-sans)" font-size="6.5" fill="#e0e8e3">Loop duplo fail-safe NR-12: NF corta K1</text>
          <text x="360" y="22" font-family="var(--font-sans)" font-size="6" fill="#8fa699">e NA alerta GPIO 27 do ESP32</text>
        </g>

        <!-- Linha 5: CH-05 Comunicação IA -->
        <g transform="translate(10, 172)">
          <rect x="0" y="0" width="485" height="26" fill="#121e17" rx="2"/>
          <text x="8" y="17" font-family="var(--font-mono)" font-size="7.5" fill="#00e5ff" font-weight="700">CH-05</text>
          <text x="65" y="13" font-family="var(--font-mono)" font-size="7" fill="#fff">2x Cabos USB</text>
          <text x="65" y="22" font-family="var(--font-mono)" font-size="6" fill="#8fa699">Blindados C/ Malha</text>
          <text x="150" y="13" font-family="var(--font-mono)" font-size="7" fill="#fff">Notebook Host</text>
          <text x="150" y="22" font-family="var(--font-mono)" font-size="6" fill="#8fa699">➔ Câmera &amp; ESP32</text>
          <text x="290" y="17" font-family="var(--font-mono)" font-size="7.5" fill="#00e5ff" font-weight="700">USB 2.0</text>
          <text x="360" y="13" font-family="var(--font-sans)" font-size="6.5" fill="#e0e8e3">Cabo 1: Vídeo Full HD Webcam 1080p</text>
          <text x="360" y="22" font-family="var(--font-sans)" font-size="6" fill="#8fa699">Cabo 2: Serial UART (✂️ VBUS Cortado)</text>
        </g>
      </g>
    </g>
    """
    return svg
