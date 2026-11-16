# -*- coding: utf-8 -*-
"""
Sheet 4: Réguas de Bornes (X1/X2/X3), Tabela de Condutores e Lista de Materiais (BOM)
AmazonVision 4.0 - XXI Feira Tecnológica FUCAPI 2026
"""

from sheet_frame import get_cad_frame

def get_sheet_4():
    frame = get_cad_frame(4, "RÉGUAS DE BORNES (X1/X2/X3), CONDUTORES E LISTA DE MATERIAIS", "Bornes em Trilho DIN TS-35, Tabela De-Para de Cabos e Especificação de Componentes")
    
    svg = f"""
    {frame}
    
    <!-- ========================================================
         FOLHA 04: RÉGUAS DE BORNES, CABOS E LISTA DE MATERIAIS
         ======================================================== -->

    <!-- SEÇÃO SUPERIOR: RÉGUAS DE BORNES EM TRILHO DIN TS-35 -->
    <g transform="translate(60, 55)">
      <rect x="0" y="0" width="480" height="26" fill="#14221b" stroke="#00e5ff" stroke-width="1.2" rx="3"/>
      <text x="12" y="18" font-family="var(--font-mono)" font-size="11" fill="#00e5ff" font-weight="700">DISTRIBUIÇÃO FÍSICA: RÉGUAS DE BORNES EM TRILHO DIN TS-35</text>
    </g>

    <!-- TRILHO DIN METÁLICO TS-35 PERFIL CARTOLA -->
    <g transform="translate(60, 95)">
      <!-- Perfil do Trilho DIN Metálico Galvanizado -->
      <rect x="0" y="35" width="980" height="48" fill="#152019" stroke="#334d3d" stroke-width="1.5"/>
      <line x1="0" y1="42" x2="980" y2="42" stroke="#486854" stroke-width="1"/>
      <line x1="0" y1="75" x2="980" y2="75" stroke="#486854" stroke-width="1"/>
      <g opacity="0.3">
        <rect x="50" y="52" width="25" height="12" rx="4" fill="#080e0a"/>
        <rect x="250" y="52" width="25" height="12" rx="4" fill="#080e0a"/>
        <rect x="450" y="52" width="25" height="12" rx="4" fill="#080e0a"/>
        <rect x="650" y="52" width="25" height="12" rx="4" fill="#080e0a"/>
        <rect x="850" y="52" width="25" height="12" rx="4" fill="#080e0a"/>
      </g>
      <text x="970" y="62" font-family="var(--font-mono)" font-size="8" fill="#5c7967" text-anchor="end">TRILHO DIN TS-35 × 7.5 mm GALVANIZADO</text>

      <!-- ========================================================
           RÉGUA X1: ALIMENTAÇÃO E BARRAMENTOS (10 BORNES)
           ======================================================== -->
      <g transform="translate(20, 10)">
        <rect x="0" y="0" width="280" height="20" fill="#0e1713" stroke="#00e5ff" stroke-width="1.2" rx="2"/>
        <text x="10" y="14" font-family="var(--font-mono)" font-size="9" fill="#00e5ff" font-weight="700">RÉGUA X1: ALIMENTAÇÃO &amp; BARRAMENTOS</text>

        <g transform="translate(5, 25)">
          <!-- X1:1 AC_L -->
          <g transform="translate(0, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#ff80ab" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">1</text>
            <circle cx="12" cy="32" r="3" fill="#ff80ab"/>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="7" fill="#ff80ab" text-anchor="middle">L</text>
            <text x="12" y="-5" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">L01</text>
          </g>
          <!-- X1:2 AC_N -->
          <g transform="translate(26, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#80d8ff" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">2</text>
            <circle cx="12" cy="32" r="3" fill="#80d8ff"/>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="7" fill="#80d8ff" text-anchor="middle">N</text>
            <text x="12" y="-5" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">N01</text>
          </g>
          <!-- X1:3 PE Terra -->
          <g transform="translate(52, 0)">
            <rect x="0" y="0" width="26" height="65" fill="#1f3316" stroke="#c6ff00" stroke-width="1.5"/>
            <text x="13" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">3</text>
            <circle cx="13" cy="32" r="3" fill="#c6ff00"/>
            <text x="13" y="58" font-family="var(--font-mono)" font-size="7" fill="#c6ff00" font-weight="700" text-anchor="middle">PE</text>
            <text x="13" y="-5" font-family="var(--font-mono)" font-size="7" fill="#c6ff00" text-anchor="middle">PE01</text>
          </g>
          <!-- X1:4 RESERVA -->
          <g transform="translate(80, 0)">
            <rect x="0" y="0" width="26" height="65" fill="#141c18" stroke="#3d5a45" stroke-width="1"/>
            <text x="13" y="15" font-family="var(--font-mono)" font-size="8" fill="#8fa699" text-anchor="middle">4</text>
            <circle cx="13" cy="32" r="2.5" fill="#3d5a45"/>
            <text x="13" y="58" font-family="var(--font-mono)" font-size="6" fill="#6d8a75" text-anchor="middle">RES</text>
            <text x="13" y="-5" font-family="var(--font-mono)" font-size="7" fill="#4d6a55" text-anchor="middle">--</text>
          </g>
          <!-- X1:5 +12V_CONT -->
          <g transform="translate(108, 0)">
            <rect x="0" y="0" width="26" height="65" fill="#18261e" stroke="#ff3344" stroke-width="1"/>
            <text x="13" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">5</text>
            <circle cx="13" cy="32" r="3" fill="#ff3344"/>
            <text x="13" y="58" font-family="var(--font-mono)" font-size="6" fill="#ff3344" text-anchor="middle">12C</text>
            <text x="13" y="-5" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">W05</text>
          </g>
          <!-- X1:6 +12V_AT -->
          <g transform="translate(136, 0)">
            <rect x="0" y="0" width="26" height="65" fill="#18261e" stroke="#ff1744" stroke-width="1.5"/>
            <text x="13" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">6</text>
            <circle cx="13" cy="32" r="3" fill="#ff1744"/>
            <text x="13" y="58" font-family="var(--font-mono)" font-size="6" fill="#ff1744" text-anchor="middle">12A</text>
            <text x="13" y="-5" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">W06</text>
          </g>
          <!-- X1:7 +6V_SRV -->
          <g transform="translate(164, 0)">
            <rect x="0" y="0" width="26" height="65" fill="#18261e" stroke="#ff9100" stroke-width="1"/>
            <text x="13" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">7</text>
            <circle cx="13" cy="32" r="3" fill="#ff9100"/>
            <text x="13" y="58" font-family="var(--font-mono)" font-size="6" fill="#ff9100" text-anchor="middle">+6V</text>
            <text x="13" y="-5" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">W07</text>
          </g>
          <!-- X1:8 +5V_ESP -->
          <g transform="translate(192, 0)">
            <rect x="0" y="0" width="26" height="65" fill="#18261e" stroke="#ffd600" stroke-width="1"/>
            <text x="13" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">8</text>
            <circle cx="13" cy="32" r="3" fill="#ffd600"/>
            <text x="13" y="58" font-family="var(--font-mono)" font-size="6" fill="#ffd600" text-anchor="middle">+5V</text>
            <text x="13" y="-5" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">W08</text>
          </g>
          <!-- X1:9 0V_COMUM -->
          <g transform="translate(220, 0)">
            <rect x="0" y="0" width="26" height="65" fill="#14261b" stroke="#00e676" stroke-width="1.2"/>
            <text x="13" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">9</text>
            <circle cx="13" cy="32" r="3" fill="#00e676"/>
            <text x="13" y="58" font-family="var(--font-mono)" font-size="7" fill="#00e676" text-anchor="middle">0V</text>
            <text x="13" y="-5" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">W09</text>
          </g>
          <!-- X1:10 0V_COMUM -->
          <g transform="translate(248, 0)">
            <rect x="0" y="0" width="26" height="65" fill="#14261b" stroke="#00e676" stroke-width="1.2"/>
            <text x="13" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">10</text>
            <circle cx="13" cy="32" r="3" fill="#00e676"/>
            <text x="13" y="58" font-family="var(--font-mono)" font-size="7" fill="#00e676" text-anchor="middle">0V</text>
            <text x="13" y="-5" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">W10</text>
          </g>
        </g>
      </g>

      <!-- ========================================================
           RÉGUA X2: COMANDO E CAMPO (10 BORNES)
           ======================================================== -->
      <g transform="translate(330, 10)">
        <rect x="0" y="0" width="280" height="20" fill="#0e1713" stroke="#00e676" stroke-width="1.2" rx="2"/>
        <text x="10" y="14" font-family="var(--font-mono)" font-size="9" fill="#00e676" font-weight="700">RÉGUA X2: Sensores IR Retangulares (5V) &amp; Botão S0</text>

        <g transform="translate(5, 25)">
          <g transform="translate(0, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#ffd600" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">1</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#ffd600" text-anchor="middle">S1_BN</text>
          </g>
          <g transform="translate(26, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#00e676" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">2</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#29b6f6" text-anchor="middle">S1_BU</text>
          </g>
          <g transform="translate(52, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#00e5ff" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">3</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#fff" text-anchor="middle">S1_BK</text>
          </g>
          <g transform="translate(80, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#ffd600" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">4</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#ffd600" text-anchor="middle">S2_BN</text>
          </g>
          <g transform="translate(106, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#00e676" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">5</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#29b6f6" text-anchor="middle">S2_BU</text>
          </g>
          <g transform="translate(132, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#00e5ff" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">6</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#fff" text-anchor="middle">S2_BK</text>
          </g>
          <g transform="translate(160, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#ff1744" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">7</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#ff1744" text-anchor="middle">S0_11</text>
          </g>
          <g transform="translate(186, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#ff1744" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">8</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#ff1744" text-anchor="middle">S0_12</text>
          </g>
          <g transform="translate(212, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#b388ff" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">9</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#b388ff" text-anchor="middle">S0_13</text>
          </g>
          <g transform="translate(238, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#b388ff" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">10</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#b388ff" text-anchor="middle">S0_14</text>
          </g>
        </g>
      </g>

      <!-- ========================================================
           RÉGUA X3: ATUADORES E ILUMINAÇÃO (8 BORNES)
           ======================================================== -->
      <g transform="translate(640, 10)">
        <rect x="0" y="0" width="230" height="20" fill="#0e1713" stroke="#ff9100" stroke-width="1.2" rx="2"/>
        <text x="10" y="14" font-family="var(--font-mono)" font-size="9" fill="#ff9100" font-weight="700">RÉGUA X3: ATUADORES &amp; CÚPULA</text>

        <g transform="translate(5, 25)">
          <g transform="translate(0, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#ff1744" stroke-width="1.5"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">1</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#ff1744" text-anchor="middle">MOT+</text>
          </g>
          <g transform="translate(26, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#8fa699" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">2</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#8fa699" text-anchor="middle">MOT-</text>
          </g>
          <g transform="translate(52, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#1f3316" stroke="#c6ff00" stroke-width="1.5"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">3</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#c6ff00" text-anchor="middle">PE</text>
          </g>
          <g transform="translate(78, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#ff9100" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">4</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#ff9100" text-anchor="middle">+6V</text>
          </g>
          <g transform="translate(104, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#00e676" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">5</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#00e676" text-anchor="middle">GND</text>
          </g>
          <g transform="translate(130, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#d500f9" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">6</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#d500f9" text-anchor="middle">PWM</text>
          </g>
          <g transform="translate(156, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#ff3344" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">7</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#ff3344" text-anchor="middle">L+</text>
          </g>
          <g transform="translate(182, 0)">
            <rect x="0" y="0" width="24" height="65" fill="#18261e" stroke="#00e676" stroke-width="1"/>
            <text x="12" y="15" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">8</text>
            <text x="12" y="58" font-family="var(--font-mono)" font-size="6" fill="#00e676" text-anchor="middle">L-</text>
          </g>
        </g>
      </g>
    </g>

    <!-- ========================================================
         SE??O INTERMEDI?RIA ESQUERDA: TORQUES & CHECKLIST PR?-START (NBR 5410 / NR-12)
         ======================================================== -->
    <g transform="translate(60, 205)">
      <!-- T?tulo do Bloco -->
      <rect x="0" y="0" width="980" height="24" fill="#1e1e12" stroke="#ffd600" stroke-width="1.2" rx="3"/>
      <text x="12" y="16" font-family="var(--font-mono)" font-size="10" fill="#ffd600" font-weight="700">COMISSIONAMENTO EL?TRICO, TORQUES DE APERTO EM BORNES &amp; CHECKLIST PR?-ENERGIZA??O (NBR 5410 / NR-12)</text>

      <!-- Painel Interno -->
      <rect x="0" y="28" width="980" height="152" fill="#0e1713" stroke="#33473a" stroke-width="1.2" rx="3"/>

      <!-- Painel Esquerdo: Torques & Termo (w=465, h=136) -->
      <g transform="translate(10, 36)">
        <rect x="0" y="0" width="465" height="74" fill="#132219" stroke="#253a2f" rx="3"/>
        <rect x="0" y="0" width="465" height="18" fill="#1b2e22" rx="3 3 0 0"/>
        <text x="10" y="13" font-family="var(--font-mono)" font-size="8.5" fill="#00e5ff" font-weight="700">TABELA DE TORQUES DE APERTO EM BORNES &amp; BITOLAS (NBR 5410 / IEC 60947)</text>
        <text x="10" y="32" font-family="var(--font-mono)" font-size="7.5" fill="#fff">? <tspan fill="var(--c-ac-l)" font-weight="700">BORNES AC (Q0, DPS, Fonte PS1):</tspan> 1,0 mm? ? Parafuso M3/M3.5 ? Torque: <tspan fill="var(--c-gnd)" font-weight="700">0,5 a 0,6 N?m</tspan></text>
        <text x="10" y="47" font-family="var(--font-mono)" font-size="7.5" fill="#fff">? <tspan fill="var(--c-12v-at)" font-weight="700">BORNES FOR?A DC (X1, X3 Atuadores, Motor M1):</tspan> 0,75?1,0 mm? ? Torque: <tspan fill="var(--c-gnd)" font-weight="700">0,4 a 0,5 N?m</tspan></text>
        <text x="10" y="62" font-family="var(--font-mono)" font-size="7.5" fill="#fff">? <tspan fill="var(--c-sig)" font-weight="700">BORNES SINAL &amp; COMANDO (X2, Sensores, ESP32):</tspan> 0,5 mm? ? Bornes Mola/Parafuso ? Torque: <tspan fill="var(--c-gnd)" font-weight="700">0,25 a 0,3 N?m</tspan></text>

        <rect x="0" y="80" width="465" height="56" fill="#1b2a20" stroke="var(--c-gnd)" stroke-width="1" rx="2"/>
        <text x="10" y="96" font-family="var(--font-mono)" font-size="8" fill="var(--c-gnd)" font-weight="700">? TERMO DE LIBERA??O DA BANCADA INDUSTRIAL ? FEIRA FUCAPI 2026</text>
        <text x="10" y="110" font-family="var(--font-mono)" font-size="7.5" fill="#a0b8aa">Atendimento integral ?s normas NBR 5410, NR-10 e NR-12 (Seguran?a em M?quinas).</text>
        <text x="10" y="124" font-family="var(--font-mono)" font-size="7.5" fill="#8fa699">Laudo t?cnico emitido: Sistema liberado para opera??o cont?nua e demonstra??o p?blica.</text>
      </g>

      <!-- Painel Direito: Protocolo Mult?metro 6 Passos (w=485, h=136) -->
      <g transform="translate(485, 36)">
        <rect x="0" y="0" width="485" height="136" fill="#111c16" stroke="#ffd600" stroke-width="1.2" rx="3"/>
        <rect x="0" y="0" width="485" height="18" fill="#1b2e22" rx="3 3 0 0"/>
        <text x="10" y="13" font-family="var(--font-mono)" font-size="8.5" fill="#ffd600" font-weight="700">ROTEIRO OBRIGAT?RIO DE AFERI??O NO MULT?METRO (PR?-START):</text>
        
        <text x="10" y="34" font-family="var(--font-mono)" font-size="7.5" fill="#fff"><tspan fill="#ffd600" font-weight="700">01. REDE AC &amp; PE:</tspan> 115?127V / 220V AC no disjuntor Q0; continuidade PE na carca?a &lt; 0,1 ?.</text>
        <text x="10" y="52" font-family="var(--font-mono)" font-size="7.5" fill="#fff"><tspan fill="var(--c-sig)" font-weight="700">02. MONO-FONTE PS1:</tspan> Ligar Q0 sem carga; aferir barramento PS1 em 12,0V ? 0,1V DC.</text>
        <text x="10" y="70" font-family="var(--font-mono)" font-size="7.5" fill="#fff"><tspan fill="var(--c-6v)" font-weight="700">03. TRIMPOT BUCK U2 (SERVO):</tspan> Desconectar servo M2; calibrar XL4015 para exatamente 6,00V DC.</text>
        <text x="10" y="88" font-family="var(--font-mono)" font-size="7.5" fill="#fff"><tspan fill="#ffd600" font-weight="700">04. TRIMPOT BUCK U4 (ESP/SENS):</tspan> Desconectar ESP/sensores; calibrar MP1584EN para 5,02V DC.</text>
        <text x="10" y="106" font-family="var(--font-mono)" font-size="7.5" fill="#fff"><tspan fill="var(--c-12v-at)" font-weight="700">05. CORTE NR-12 (S0 + K1):</tspan> Pressionar cogumelo S0: desenergizar +12V_AT e aterrar GPIO 27.</text>
        <text x="10" y="124" font-family="var(--font-mono)" font-size="7.5" fill="#fff"><tspan fill="var(--c-gnd)" font-weight="700">06. PARTIDA COM CARGA:</tspan> Reconectar atuadores e sensores; ligar Q0 e validar telemetria serial.</text>
      </g>
    </g>

    <!-- ========================================================
         SE??O SUPERIOR DIREITA: ARQUITETURA DE TERRA & CABO USB
         ======================================================== -->
    <g transform="translate(1080, 50)">
      <!-- T?tulo do Bloco 1 -->
      <rect x="0" y="0" width="560" height="24" fill="#14221b" stroke="#00e5ff" stroke-width="1.2" rx="3"/>
      <text x="12" y="16" font-family="var(--font-mono)" font-size="10.5" fill="#00e5ff" font-weight="700">ARQUITETURA DE TERRA: STAR-POINT (0V_COMUM) &amp; ISOLAMENTO USB</text>

      <!-- Painel Interno Bloco 1 -->
      <rect x="0" y="28" width="560" height="307" fill="#0c1611" stroke="#253a2f" stroke-width="1.5" rx="4"/>

      <!-- 1.1 Barramento PE (Terra de Prote??o Met?lico) -->
      <g transform="translate(15, 36)">
        <rect x="0" y="0" width="530" height="28" fill="#182c16" stroke="#c6ff00" stroke-width="1.5" rx="3"/>
        <line x1="10" y1="21" x2="520" y2="21" stroke="#c6ff00" stroke-width="3" stroke-dasharray="12 4"/>
        <text x="12" y="14" font-family="var(--font-mono)" font-size="8.5" fill="#c6ff00" font-weight="700">BARRAMENTO PE (TERRA DE PROTE??O) ? TRILHO DIN TS-35 / ESTRUTURA</text>
        <circle cx="90" cy="21" r="3.5" fill="#c6ff00"/>
        <text x="98" y="20" font-family="var(--font-mono)" font-size="7" fill="#fff">PE Plugue</text>
        <circle cx="210" cy="21" r="3.5" fill="#c6ff00"/>
        <text x="218" y="20" font-family="var(--font-mono)" font-size="7" fill="#fff">PE Fontes</text>
        <circle cx="330" cy="21" r="3.5" fill="#c6ff00"/>
        <text x="338" y="20" font-family="var(--font-mono)" font-size="7" fill="#fff">PE Trilho</text>
        <circle cx="450" cy="21" r="3.5" fill="#c6ff00"/>
        <text x="458" y="20" font-family="var(--font-mono)" font-size="7" fill="#fff">PE Esteira</text>
      </g>

      <!-- 1.2 Ponto Estrela Central ?nico (Star-Point 0V_COMUM) -->
      <g transform="translate(15, 68)">
        <rect x="0" y="0" width="530" height="118" fill="#101d16" stroke="#00e676" stroke-width="1.2" rx="3"/>
        <text x="12" y="15" font-family="var(--font-mono)" font-size="9" fill="#00e676" font-weight="700">PONTO ESTRELA CENTRAL ?NICO (STAR-POINT 0V_COMUM ? BORNES X1:9 &amp; X1:10)</text>
        
        <!-- Ponto Estrela Central -->
        <circle cx="265" cy="58" r="13" fill="#00e676" stroke="#fff" stroke-width="2"/>
        <text x="265" y="62" font-family="var(--font-mono)" font-size="9.5" fill="#000" font-weight="700" text-anchor="middle">0V</text>

        <!-- Raios / Condutores convergindo para o ponto estrela -->
        <path d="M 40 40 L 252 58" stroke="#00e676" stroke-width="2.5"/>
        <circle cx="40" cy="40" r="3.5" fill="#00e676"/>
        <text x="46" y="36" font-family="var(--font-mono)" font-size="7.2" fill="#fff">PS1 12V 10A (0V) [1,0 mm?]</text>

        <path d="M 40 80 L 252 58" stroke="#00e676" stroke-width="2"/>
        <circle cx="40" cy="80" r="3.5" fill="#00e676"/>
        <text x="46" y="88" font-family="var(--font-mono)" font-size="7.2" fill="#ffd600">0V Sensores IR Retangulares (X2:2/5)</text>

        <path d="M 490 36 L 278 58" stroke="#00e676" stroke-width="2"/>
        <circle cx="490" cy="36" r="3.5" fill="#00e676"/>
        <text x="484" y="32" font-family="var(--font-mono)" font-size="7.2" fill="#ff9100" text-anchor="end">GND Buck U2 XL4015 (6V)</text>

        <path d="M 490 58 L 278 58" stroke="#00e676" stroke-width="2"/>
        <circle cx="490" cy="58" r="3.5" fill="#00e676"/>
        <text x="484" y="54" font-family="var(--font-mono)" font-size="7.2" fill="#ffd600" text-anchor="end">GND Buck U4 5V ESP32</text>

        <path d="M 490 82 L 278 58" stroke="#00e676" stroke-width="2"/>
        <circle cx="490" cy="82" r="3.5" fill="#00e676"/>
        <text x="484" y="90" font-family="var(--font-mono)" font-size="7.2" fill="#b388ff" text-anchor="end">GND L?gico ESP32 DevKit</text>

        <rect x="10" y="96" width="510" height="16" fill="#0b140f" rx="2"/>
        <text x="15" y="108" font-family="var(--font-mono)" font-size="7.2" fill="#7ba88a">REGRA: Retornos negativos unidos EXCLUSIVAMENTE nos bornes X1:9/10. Elimina ground loops e ru?dos.</text>
      </g>

      <!-- 1.3 Cabo USB Modificado (Comunica??o Host PC -> ESP32) -->
      <g transform="translate(15, 190)">
        <rect x="0" y="0" width="530" height="140" fill="#1c1313" stroke="#ff5252" stroke-width="1.2" rx="3"/>
        <text x="12" y="15" font-family="var(--font-mono)" font-size="9" fill="#ff5252" font-weight="700">DETALHE CONSTRUTIVO: CABO USB DADOS MODIFICADO (NOTEBOOK ? ESP32)</text>

        <!-- Conector USB-A Lado Notebook -->
        <g transform="translate(15, 24)">
          <rect x="0" y="0" width="48" height="74" fill="#122538" stroke="#00e5ff" rx="3"/>
          <text x="24" y="32" font-family="var(--font-mono)" font-size="7.5" fill="#fff" text-anchor="middle">USB-A</text>
          <text x="24" y="45" font-family="var(--font-mono)" font-size="6.5" fill="#8fa699" text-anchor="middle">NOTEBOOK</text>
        </g>

        <!-- Conector Micro-USB Lado ESP32 -->
        <g transform="translate(465, 24)">
          <rect x="0" y="0" width="48" height="74" fill="#1a2e1d" stroke="#ffd600" rx="3"/>
          <text x="24" y="32" font-family="var(--font-mono)" font-size="7.5" fill="#fff" text-anchor="middle">MICRO</text>
          <text x="24" y="45" font-family="var(--font-mono)" font-size="6.5" fill="#ffd600" text-anchor="middle">ESP32</text>
        </g>

        <!-- Fio 1: VBUS (+5V) SECCIONADO E ISOLADO -->
        <g transform="translate(63, 36)">
          <line x1="0" y1="0" x2="160" y2="0" stroke="#ff1744" stroke-width="2.5"/>
          <circle cx="170" cy="0" r="10" fill="#381010" stroke="#ff1744" stroke-width="1.5"/>
          <line x1="164" y1="-6" x2="176" y2="6" stroke="#ff1744" stroke-width="2.5"/>
          <line x1="176" y1="-6" x2="164" y2="6" stroke="#ff1744" stroke-width="2.5"/>
          <line x1="180" y1="0" x2="340" y2="0" stroke="#555" stroke-width="1.5" stroke-dasharray="4 4"/>
          <rect x="185" y="-10" width="145" height="18" fill="#300" stroke="#ff1744" rx="2"/>
          <text x="190" y="2" font-family="var(--font-mono)" font-size="7.5" fill="#ff8a80" font-weight="700">VBUS (+5V) CORTADO / ISOLADO</text>
          <text x="35" y="-5" font-family="var(--font-mono)" font-size="7" fill="#ff8a80">+5V VBUS</text>
        </g>

        <!-- Fio 2: D- (Branco) -->
        <g transform="translate(63, 58)">
          <line x1="0" y1="0" x2="402" y2="0" stroke="#ffffff" stroke-width="2"/>
          <text x="35" y="-4" font-family="var(--font-mono)" font-size="7" fill="#fff">D- (Dados USB -)</text>
          <text x="380" y="-4" font-family="var(--font-mono)" font-size="7" fill="#00e676" text-anchor="end">ATIVO (SERIAL 115200)</text>
        </g>

        <!-- Fio 3: D+ (Verde) -->
        <g transform="translate(63, 76)">
          <line x1="0" y1="0" x2="402" y2="0" stroke="#00e676" stroke-width="2"/>
          <text x="35" y="-4" font-family="var(--font-mono)" font-size="7" fill="#00e676">D+ (Dados USB +)</text>
          <text x="380" y="-4" font-family="var(--font-mono)" font-size="7" fill="#00e676" text-anchor="end">ATIVO (SERIAL 115200)</text>
        </g>

        <!-- Fio 4: GND (Preto/Azul) -->
        <g transform="translate(63, 94)">
          <line x1="0" y1="0" x2="402" y2="0" stroke="#78909c" stroke-width="2.5"/>
          <text x="35" y="-4" font-family="var(--font-mono)" font-size="7" fill="#b0bec5">GND (Terra de Sinal Serial)</text>
          <text x="380" y="-4" font-family="var(--font-mono)" font-size="7" fill="#00e676" text-anchor="end">COMUM EST?VEL</text>
        </g>

        <!-- Advert?ncia de Seguran?a -->
        <rect x="15" y="112" width="500" height="20" fill="#291212" stroke="#ff3344" stroke-width="1" rx="2"/>
        <text x="25" y="125" font-family="var(--font-mono)" font-size="7.5" fill="#ff8a80" font-weight="700">?? FINALIDADE: IMPEDE QUE A FONTE 12V/5V RETROALIMENTE E QUEIME AS PORTAS USB DO NOTEBOOK.</text>
      </g>
    </g>

    <!-- ========================================================
         SE??O INFERIOR ESQUERDA: TABELA DE CONDUTORES (DE-PARA)
         ======================================================== -->
    <foreignObject x="35" y="400" width="790" height="575">
      <div xmlns="http://www.w3.org/1999/xhtml" class="bom-table-wrap">
        <table class="cad-table">
          <thead>
            <tr>
              <th colspan="7" class="cad-table-banner">TABELA 1 ? TABELA DE CONDUTORES, BITOLAS E ROTEAMENTO DE BORNES (24 CIRCUITOS)</th>
            </tr>
            <tr>
              <th>ANILHA</th>
              <th>SE??O</th>
              <th>COR</th>
              <th>ORIGEM</th>
              <th>DESTINO</th>
              <th>FUN??O</th>
            </tr>
          </thead>
          <tbody>
            <tr><td><span class="tag-badge" style="color:var(--c-ac-l);border-color:var(--c-ac-l);">L01</span></td><td>1,0 mm?</td><td>Marrom</td><td>Plugue AC / X1:1</td><td>Q0 ? S_MAIN ? PS1(L)</td><td>Fase AC 127/220V</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-ac-n);border-color:var(--c-ac-n);">N01</span></td><td>1,0 mm?</td><td>Azul Claro</td><td>Plugue AC / X1:2</td><td>Q0 ? S_MAIN ? PS1(N)</td><td>Neutro AC</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-pe);border-color:var(--c-pe);">PE01</span></td><td>1,0 mm?</td><td>Verde/Am</td><td>Plugue AC / X1:3</td><td>PS1(PE) / Trilho DIN</td><td>Terra Prote??o PE</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-12v-cont);border-color:var(--c-12v-cont);">W05</span></td><td>1,0 mm?</td><td>Vermelho</td><td>PS1 +12V (p?s-F1)</td><td>X1:5 (+12V_CONT)</td><td>Barramento 12V Cont.</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-12v-at);border-color:var(--c-12v-at);">W06</span></td><td>1,0 mm?</td><td>Vermelho</td><td>K1 Contato 87</td><td>X1:6 (+12V_AT)</td><td>12V Seccion?vel NR-12</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-6v);border-color:var(--c-6v);">W07</span></td><td>0,75 mm?</td><td>Laranja</td><td>XL4015 OUT+</td><td>X1:7 / X3:4 (+6V_SRV)</td><td>Barramento 6,0V Servo</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-5v);border-color:var(--c-5v);">W08</span></td><td>0,5 mm?</td><td>Amarelo</td><td>MP1584 OUT+</td><td>X1:8 ? ESP VIN / X2:1,4</td><td>Barramento +5V_ESP</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-gnd);border-color:var(--c-gnd);">W09/W10</span></td><td>1,0 mm?</td><td>Preto</td><td>PS1 0V (COM)</td><td>X1:9 / X1:10 (Star-Point)</td><td>Refer?ncia 0V_COMUM</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-12v-at);border-color:var(--c-12v-at);">W101</span></td><td>1,0 mm?</td><td>Vermelho</td><td>X1:6 (+12V_AT)</td><td>F3 (5A) ? X3:1 (MOT+)</td><td>Pot?ncia Motor M1 (+)</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-gnd);border-color:var(--c-gnd);">W102</span></td><td>1,0 mm?</td><td>Preto</td><td>X3:2 (MOT-)</td><td>D4184 LOAD- (Dreno)</td><td>Retorno Chaveado M1</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-gnd);border-color:var(--c-gnd);">W103</span></td><td>1,0 mm?</td><td>Preto</td><td>D4184 GND-IN</td><td>X1:9 (0V_COMUM)</td><td>Retorno Pot?ncia M1</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-12v-at);border-color:var(--c-12v-at);">W104</span></td><td>0,75 mm?</td><td>Vermelho</td><td>X1:6 (+12V_AT)</td><td>F2 (3A) ? XL4015 IN+</td><td>Entrada 12V Buck U2</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-gnd);border-color:var(--c-gnd);">W105</span></td><td>0,75 mm?</td><td>Preto</td><td>X1:9 (0V_COMUM)</td><td>XL4015 IN- (U2)</td><td>Retorno Buck Servo</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-6v);border-color:var(--c-6v);">W106</span></td><td>0,5 mm?</td><td>Vermelho</td><td>XL4015 OUT+ / C1+</td><td>X3:4 (+6V_SRV ? M2)</td><td>Pot?ncia +6V Servo M2</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-gnd);border-color:var(--c-gnd);">W107</span></td><td>0,5 mm?</td><td>Marrom</td><td>XL4015 OUT- / C1-</td><td>X3:5 (GND_SRV ? M2)</td><td>Retorno 0V Servo M2</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-12v-cont);border-color:var(--c-12v-cont);">W108</span></td><td>0,5 mm?</td><td>Vermelho</td><td>X1:5 ? F5 ? S_LED</td><td>X3:7 (L+ Ring Light)</td><td>Alim. +12V Ring Light</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-gnd);border-color:var(--c-gnd);">W109</span></td><td>0,5 mm?</td><td>Preto</td><td>X3:8 (L- Ring Light)</td><td>X1:9 (0V_COMUM)</td><td>Retorno 0V Ring Light</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-sig);border-color:var(--c-sig);">W201</span></td><td>0,5 mm?</td><td>Azul</td><td>ESP32 GPIO 19</td><td>D4184 TRIG (PWM)</td><td>Comando Motor M1</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-sig);border-color:var(--c-sig);">W202</span></td><td>0,5 mm?</td><td>Laranja</td><td>ESP32 GPIO 18</td><td>X3:6 (PWM_SRV ? M2)</td><td>Sinal PWM Servo 50Hz</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-sig);border-color:var(--c-sig);">W203</span></td><td>0,5 mm?</td><td>Preto</td><td>X2:3 (B1/S1_BK)</td><td>R1(1k?)+BAT54S ? IO25</td><td>Sinal S1 (Clamp 3,3V)</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-sig);border-color:var(--c-sig);">W204</span></td><td>0,5 mm?</td><td>Preto</td><td>X2:6 (B2/S2_BK)</td><td>R2(1k?)+BAT54S ? IO26</td><td>Sinal S2 (Clamp 3,3V)</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-sig);border-color:var(--c-sig);">W205</span></td><td>0,5 mm?</td><td>Violeta</td><td>X2:9(13) / X2:10(14)</td><td>ESP32 GPIO 27 (ESTOP)</td><td>Alarme Firmware S0 NA</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-12v-cont);border-color:var(--c-12v-cont);">W206</span></td><td>0,5 mm?</td><td>Vermelho</td><td>X1:5 (+12V_CONT)</td><td>X2:7 (S0_11 NF)</td><td>Linha Seguran?a S0 NF</td></tr>
            <tr><td><span class="tag-badge" style="color:var(--c-12v-at);border-color:var(--c-12v-at);">W207</span></td><td>0,5 mm?</td><td>Vermelho</td><td>X2:8 (S0_12 NF)</td><td>K1 Bobina (A1)</td><td>Acionamento Rel? K1</td></tr>
          </tbody>
        </table>
      </div>
    </foreignObject>

    <!-- ========================================================
         SE??O INFERIOR DIREITA: LISTA OFICIAL DE MATERIAIS (BOM)
         ======================================================== -->
    <foreignObject x="840" y="400" width="795" height="465">
      <div xmlns="http://www.w3.org/1999/xhtml" class="bom-table-wrap">
        <table class="cad-table">
          <thead>
            <tr>
              <th colspan="7" class="cad-table-banner">TABELA 2 ? LISTA MESTRA DE MATERIAIS (BOM) CONSOLIDADA NO ESQUEMA</th>
            </tr>
            <tr>
              <th>TAG</th>
              <th>COMPONENTE / ESPECIFICA??O</th>
              <th>MODELO / FAB.</th>
              <th>ESPECIFICA??O T?CNICA</th>
              <th>QTD</th>
              <th>STATUS</th>
            </tr>
          </thead>
          <tbody>
            <tr><td><span class="tag-badge">PS1</span></td><td style="color:var(--text-main);font-weight:700">Fonte Chaveada Colmeia</td><td>Mean Well LRS-120</td><td>12V DC / 10A (120W) ? Mono-Fonte</td><td style="color:var(--text-main);font-weight:700;text-align:center">1 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">Q0</span></td><td style="color:var(--text-main);font-weight:700">Disjuntor Bipolar DIN</td><td>Schneider iK60N</td><td>10A Curva C / 4.5kA ? IEC 60947</td><td style="color:var(--text-main);font-weight:700;text-align:center">1 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">S_MAIN</span></td><td style="color:var(--text-main);font-weight:700">Filtro RFI/EMI + Chave Geral</td><td>IEC C14 c/ Chave</td><td>250V AC / 10A Bipolar Luminosa</td><td style="color:var(--text-main);font-weight:700;text-align:center">1 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">DPS</span></td><td style="color:var(--text-main);font-weight:700">Protetor Surtos Classe II</td><td>Clamper Front Tec</td><td>275V / 20kA (L-PE e N-PE)</td><td style="color:var(--text-main);font-weight:700;text-align:center">2 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">S0</span></td><td style="color:var(--text-main);font-weight:700">Bot?o Emerg?ncia Cogumelo</td><td>Siemens 3SB3 ?22</td><td>1 NF (K1) + 1 NA (IO27) NR-12</td><td style="color:var(--text-main);font-weight:700;text-align:center">1 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">K1</span></td><td style="color:var(--text-main);font-weight:700">Rel? Auxiliar + Soquete</td><td>DNI / Bosch 40A</td><td>Bobina 12V DC / Contato NA 40A</td><td style="color:var(--text-main);font-weight:700;text-align:center">1 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">U1</span></td><td style="color:var(--text-main);font-weight:700">Microcontrolador ESP32</td><td>Espressif DevKit V1</td><td>ESP-WROOM-32 Dual-Core 30p</td><td style="color:var(--text-main);font-weight:700;text-align:center">1 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">U2</span></td><td style="color:var(--text-main);font-weight:700">Conversor Buck Servo</td><td>XLSEMI XL4015</td><td>12V ? 6,00V DC / 5A Ajust?vel</td><td style="color:var(--text-main);font-weight:700;text-align:center">1 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">U4</span></td><td style="color:var(--text-main);font-weight:700">Conversor Buck L?gica</td><td>MP1584EN Step-Down</td><td>12V ? 5,02V DC / 2A (ESP+Sens)</td><td style="color:var(--text-main);font-weight:700;text-align:center">1 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">D4184</span></td><td style="color:var(--text-main);font-weight:700">M?dulo Driver MOSFET</td><td>AOD4184 Duplo N-Ch</td><td>40V / 15A ? Rds(on)&lt;8.5m? PWM</td><td style="color:var(--text-main);font-weight:700;text-align:center">1 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">M1</span></td><td style="color:var(--text-main);font-weight:700">Motorredutor DC Esteira</td><td>Bohao GA37-550</td><td>12V DC 60 RPM ? 12 kgf?cm nom.</td><td style="color:var(--text-main);font-weight:700;text-align:center">1 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">M2</span></td><td style="color:var(--text-main);font-weight:700">Empurrador Linear Servo</td><td>MG996R + Biela</td><td>6,0V ? Curso 120mm (R=60/L=110)</td><td style="color:var(--text-main);font-weight:700;text-align:center">1 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">B1, B2</span></td><td style="color:var(--text-main);font-weight:700">Sensor ?ptico IR Retangular</td><td>5V NPN NA Reflexivo</td><td>5V DC ? Alcance 3?80cm ? Pull-up 10k?</td><td style="color:var(--text-main);font-weight:700;text-align:center">2 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">D2, D3</span></td><td style="color:var(--text-main);font-weight:700">Diodo Schottky Duplo Clamp</td><td>BAT54S (SOT-23)</td><td>Clamp 3,3V p/ GPIOs 25 e 26</td><td style="color:var(--text-main);font-weight:700;text-align:center">2 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">R1, R2</span></td><td style="color:var(--text-main);font-weight:700">Resistor S?rie Prote??o</td><td>Filme Met?lico 1k?</td><td>1 k? 1/4W 1% (Limita I &lt; 2 mA)</td><td style="color:var(--text-main);font-weight:700;text-align:center">2 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">D1</span></td><td style="color:var(--text-main);font-weight:700">Diodo Schottky Flyback M1</td><td>Vishay 1N5822</td><td>40V / 3A Antiparalelo X3:1?X3:2</td><td style="color:var(--text-main);font-weight:700;text-align:center">1 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">D_K1</span></td><td style="color:var(--text-main);font-weight:700">Diodo Roda Livre Bobina K1</td><td>Diotec 1N4007</td><td>1000V / 1A Antiparalelo A1?A2</td><td style="color:var(--text-main);font-weight:700;text-align:center">1 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">C1</span></td><td style="color:var(--text-main);font-weight:700">Capacitor Filtro de Pico</td><td>Nichicon Low-ESR</td><td>1000 ?F ? 16V 105?C (Buffer 6V)</td><td style="color:var(--text-main);font-weight:700;text-align:center">1 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">F1..F5</span></td><td style="color:var(--text-main);font-weight:700">Fus?veis L?mina + Porta-Fus.</td><td>Littelfuse DIN</td><td>F1:10A, F2:3A, F3:5A, F5:1A</td><td style="color:var(--text-main);font-weight:700;text-align:center">4 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">LED/S_LED</span></td><td style="color:var(--text-main);font-weight:700">Ring Light C?pula + Chave</td><td>Anel LED 12V 6000K</td><td>Luz Difusa 0,6A + Chave S_LED</td><td style="color:var(--text-main);font-weight:700;text-align:center">1 cj</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">CAM</span></td><td style="color:var(--text-main);font-weight:700">C?mera de Vis?o Artificial</td><td>Webcam Full HD UVC</td><td>1080p 30FPS USB 2.0 Foco 180mm</td><td style="color:var(--text-main);font-weight:700;text-align:center">1 un</td><td>Homologado</td></tr>
            <tr><td><span class="tag-badge">X1..X3</span></td><td style="color:var(--text-main);font-weight:700">R?guas Bornes + Trilho DIN</td><td>Sakura 2,5mm? TS-35</td><td>28 Bornes DIN (X1:10, X2:10, X3:8)</td><td style="color:var(--text-main);font-weight:700;text-align:center">1 cj</td><td>Homologado</td></tr>
          </tbody>
        </table>
      </div>
    </foreignObject>
    """
    return svg
