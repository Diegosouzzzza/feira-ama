# -*- coding: utf-8 -*-
"""
Sheet 1: Diagrama Unifilar e Distribuição de Força, Proteções e NR-12 (Corrigido)
AmazonVision 4.0 - XXI Feira Tecnológica FUCAPI 2026
"""

from sheet_frame import get_cad_frame

def get_sheet_1():
    frame = get_cad_frame(1, "DIAGRAMA UNIFILAR — DISTRIBUIÇÃO DE FORÇA, PROTEÇÕES E NR-12", "Alimentação AC, Fonte Chaveada Única PS1 12V DC, Barramentos e Segurança NR-12")
    
    svg = f"""
    {frame}
    
    <!-- ========================================================
         FOLHA 01: DIAGRAMA UNIFILAR & DISTRIBUIÇÃO GERAL (SVG)
         ======================================================== -->

    <!-- TÍTULO DE SEÇÃO SUPERIOR ESQUERDA -->
    <g transform="translate(60, 55)">
      <rect x="0" y="0" width="370" height="26" fill="#14221b" stroke="#00e5ff" stroke-width="1.2" rx="3"/>
      <text x="12" y="18" font-family="var(--font-mono)" font-size="11" fill="#00e5ff" font-weight="700">ZONA 01: ENTRADA GERAL AC &amp; CONDICIONAMENTO</text>
    </g>

    <!-- BLOCO 1: TOMADA AC & PROTEÇÃO DE ENTRADA -->
    <g id="bloco_ac_input">
      <!-- Plugue NBR 14136 -->
      <g transform="translate(60, 105)">
        <rect x="0" y="0" width="110" height="105" class="symbol-box"/>
        <text x="50" y="16" font-family="var(--font-mono)" font-size="11" fill="#fff" font-weight="700" text-anchor="middle">REDE AC</text>
        <text x="50" y="29" font-family="var(--font-mono)" font-size="9" fill="#00e5ff" text-anchor="middle">127V / 220V</text>
        <text x="50" y="40" font-family="var(--font-mono)" font-size="8" fill="#8fa699" text-anchor="middle">60 Hz — NBR 14136</text>
        <text x="46" y="51" font-family="var(--font-mono)" font-size="7.5" fill="#c6ff00" text-anchor="middle">Plugue 3P 10A</text>
        
        <!-- Pinos de Saída Alinhados aos Fios (cy=55->Y=160, cy=73->Y=178, cy=90->Y=195) -->
        <circle cx="110" cy="55" r="4.5" class="symbol-terminal"/>
        <text x="102" y="58" font-family="var(--font-mono)" font-size="8.5" fill="#ff80ab" font-weight="700" text-anchor="end">L</text>
        
        <circle cx="110" cy="73" r="4.5" class="symbol-terminal"/>
        <text x="102" y="76" font-family="var(--font-mono)" font-size="8.5" fill="#80d8ff" font-weight="700" text-anchor="end">N</text>
        
        <circle cx="110" cy="90" r="4.5" class="symbol-terminal"/>
        <text x="102" y="93" font-family="var(--font-mono)" font-size="8.5" fill="#c6ff00" font-weight="700" text-anchor="end">PE</text>
      </g>

      <!-- Fios de Entrada AC até Disjuntor Q0 (Roteamento 100% Ortogonal) -->
      <path id="wire_ac_l_in" d="M 170 160 L 210 160" class="wire w-ac-l"/>
      <path id="wire_ac_n_in" d="M 170 178 L 210 178" class="wire w-ac-n"/>
      <path id="wire_ac_pe_in" d="M 170 195 L 195 195 L 195 480 L 340 480" class="wire w-pe"/>

      <!-- Disjuntor Bipolar Q0 (10A Curva C) - Altura Aumentada e Textos Separados das Lâminas -->
      <g transform="translate(210, 95)">
        <rect x="0" y="0" width="75" height="98" class="symbol-box"/>
        <text x="37" y="16" font-family="var(--font-mono)" font-size="11" fill="#fff" font-weight="700" text-anchor="middle">Q0</text>
        <text x="37" y="27" font-family="var(--font-mono)" font-size="8" fill="#8fa699" text-anchor="middle">DISJUNTOR</text>
        <text x="37" y="38" font-family="var(--font-mono)" font-size="8" fill="#00e676" text-anchor="middle">BIPOLAR 10A</text>
        <text x="37" y="48" font-family="var(--font-mono)" font-size="7" fill="#5c7566" text-anchor="middle">Curva C — IEC 60947</text>
        <line x1="6" y1="53" x2="69" y2="53" stroke="#253a2f" stroke-width="1"/>
        
        <!-- Símbolo de Contato Bipolar na metade inferior (Livre dos textos) -->
        <line x1="0" y1="65" x2="20" y2="65" stroke="#ff80ab" stroke-width="2"/>
        <line x1="20" y1="65" x2="52" y2="58" stroke="#ff80ab" stroke-width="2"/>
        <line x1="52" y1="65" x2="75" y2="65" stroke="#ff80ab" stroke-width="2"/>
        
        <line x1="0" y1="83" x2="20" y2="83" stroke="#80d8ff" stroke-width="2"/>
        <line x1="20" y1="83" x2="52" y2="76" stroke="#80d8ff" stroke-width="2"/>
        <line x1="52" y1="83" x2="75" y2="83" stroke="#80d8ff" stroke-width="2"/>
        <line x1="36" y1="62" x2="36" y2="80" stroke="#5c7566" stroke-dasharray="2 2"/>
      </g>

      <!-- Fios de Q0 para DPS e Filtro de Linha -->
      <path id="wire_ac_l_post_q0" d="M 285 160 L 350 160" class="wire w-ac-l"/>
      <path id="wire_ac_n_post_q0" d="M 285 178 L 350 178" class="wire w-ac-n"/>
      <circle cx="310" cy="160" r="3" class="wire-junction"/>
      <circle cx="325" cy="178" r="3" class="wire-junction"/>

      <!-- DPS Classe II (Proteção contra Surtos) -->
      <g transform="translate(295, 205)">
        <rect x="0" y="0" width="85" height="65" class="symbol-box"/>
        <text x="42" y="16" font-family="var(--font-mono)" font-size="9" fill="#00e5ff" font-weight="700" text-anchor="middle">DPS CLASSE II</text>
        <text x="42" y="28" font-family="var(--font-mono)" font-size="8" fill="#8fa699" text-anchor="middle">275V / 20kA</text>
        <rect x="10" y="34" width="28" height="20" fill="#1b3022" stroke="#00e676" rx="2"/>
        <text x="24" y="47" font-family="var(--font-mono)" font-size="8" fill="#00e676" text-anchor="middle">L-PE</text>
        <rect x="47" y="34" width="28" height="20" fill="#1b3022" stroke="#00e676" rx="2"/>
        <text x="61" y="47" font-family="var(--font-mono)" font-size="8" fill="#00e676" text-anchor="middle">N-PE</text>
      </g>
      <!-- Linhas de derivação para DPS (100% Ortogonais) -->
      <path d="M 310 160 L 310 205" class="wire w-ac-l"/>
      <path d="M 325 178 L 325 205" class="wire w-ac-n"/>
      <path d="M 340 270 L 340 480" class="wire w-pe"/>
      <circle cx="340" cy="480" r="3" class="wire-junction"/>

      <!-- Filtro RFI/EMI & Chave Geral S_MAIN -->
      <g transform="translate(350, 95)">
        <rect x="0" y="0" width="85" height="98" class="symbol-box"/>
        <text x="42" y="16" font-family="var(--font-mono)" font-size="9" fill="#fff" font-weight="700" text-anchor="middle">FILTRO RFI</text>
        <text x="42" y="28" font-family="var(--font-mono)" font-size="8" fill="#8fa699" text-anchor="middle">+ CHAVE S_MAIN</text>
        <line x1="6" y1="53" x2="79" y2="53" stroke="#253a2f" stroke-width="1"/>
        <!-- Chave mecânica animada alinhada a Y=160 e Y=178 -->
        <line x1="20" y1="65" x2="65" y2="65" stroke="#00e676" stroke-width="2.5" id="s_main_contact_1"/>
        <line x1="20" y1="83" x2="65" y2="83" stroke="#00e676" stroke-width="2.5" id="s_main_contact_2"/>
        <circle cx="20" cy="65" r="2.5" fill="#fff"/>
        <circle cx="65" cy="65" r="2.5" fill="#fff"/>
        <circle cx="20" cy="83" r="2.5" fill="#fff"/>
        <circle cx="65" cy="83" r="2.5" fill="#fff"/>
      </g>

      <!-- Fios de S_MAIN para Barramento AC das Fontes -->
      <path id="wire_ac_l_bus" d="M 435 160 L 470 160 L 470 180 L 520 180" class="wire w-ac-l"/>
      <path id="wire_ac_n_bus" d="M 435 178 L 485 178 L 485 205 L 520 205" class="wire w-ac-n"/>
    </g>

    <!-- TÍTULO DE SEÇÃO: MONO-FONTE PS1 12V 10A -->
    <g transform="translate(510, 55)">
      <rect x="0" y="0" width="370" height="26" fill="#14221b" stroke="#00e5ff" stroke-width="1.2" rx="3"/>
      <text x="12" y="18" font-family="var(--font-mono)" font-size="11" fill="#00e5ff" font-weight="700">ZONA 02: CONVERSÃO AC/DC (MONO-FONTE 12V 10A PS1)</text>
    </g>

    <!-- FONTE PS1: 12V 10A (120W) — MONO-FONTE ÚNICA DA BANCADA -->
    <g id="bloco_ps1" transform="translate(510, 100)">
      <rect x="0" y="0" width="165" height="155" class="symbol-box-accent" id="box_ps1"/>
      <text x="12" y="20" font-family="var(--font-mono)" font-size="12" fill="#fff" font-weight="700">PS1 — MONO-FONTE 12V</text>
      <text x="12" y="34" font-family="var(--font-sans)" font-size="9" fill="#ff3344" font-weight="600">COLMEIA 12V DC / 10A (120W)</text>
      <text x="12" y="47" font-family="var(--font-mono)" font-size="8" fill="#8fa699">Fonte Única: Motores, Sensores, ESP32</text>
      <text x="12" y="58" font-family="var(--font-mono)" font-size="8" fill="#5c7566">Ripple &lt; 50mV | Rend: 88%</text>

      <!-- Terminais de Entrada AC -->
      <circle cx="10" cy="80" r="4" class="symbol-terminal"/>
      <text x="20" y="83" class="lbl-pin">L (AC)</text>
      <circle cx="10" cy="105" r="4" class="symbol-terminal"/>
      <text x="20" y="108" class="lbl-pin">N (AC)</text>
      <circle cx="10" cy="130" r="4" class="symbol-terminal"/>
      <text x="20" y="133" class="lbl-pin">PE (Terra)</text>

      <!-- Terminais de Saída DC -->
      <circle cx="155" cy="85" r="4.5" class="symbol-terminal"/>
      <text x="120" y="88" class="lbl-pin" fill="#ff3344">+12V</text>
      <circle cx="155" cy="120" r="4.5" class="symbol-terminal"/>
      <text x="110" y="123" class="lbl-pin" fill="#00e676">0V (COM)</text>
    </g>

    <!-- ========================================================
         INTERLIGAÇÃO AC E ATERRAMENTO PE UNICAMENTE PARA PS1
         ======================================================== -->
    <!-- Fase L para PS1 -->
    <path id="s1_wire_ac_in_l" d="M 470 180 L 520 180" class="wire w-ac-l"/>
    <circle cx="470" cy="180" r="2.5" class="wire-junction"/>

    <!-- Neutro N para PS1 -->
    <path id="s1_wire_ac_in_n" d="M 485 205 L 520 205" class="wire w-ac-n"/>
    <circle cx="485" cy="205" r="2.5" class="wire-junction"/>

    <!-- Aterramento PE: ROTEAMENTO ORTOGONAL PELA COLUNA ESQUERDA PARA PS1 E TRILHO DIN -->
    <path d="M 340 480 L 450 480" class="wire w-pe"/>
    <path d="M 450 480 L 450 230 L 520 230" class="wire w-pe"/>
    <circle cx="450" cy="480" r="3.5" class="wire-junction"/>
    <circle cx="450" cy="230" r="3" class="wire-junction"/>
    <!-- Continuação da Barra PE -->
    <path d="M 450 480 L 1050 480" class="wire w-pe"/>

    <!-- Símbolo de Terra PE Normatizado -->
    <g transform="translate(370, 480)">
      <line x1="0" y1="0" x2="0" y2="15" stroke="#c6ff00" stroke-width="2"/>
      <line x1="-12" y1="15" x2="12" y2="15" stroke="#c6ff00" stroke-width="2.5"/>
      <line x1="-8" y1="19" x2="8" y2="19" stroke="#c6ff00" stroke-width="2"/>
      <line x1="-4" y1="23" x2="4" y2="23" stroke="#c6ff00" stroke-width="1.5"/>
      <text x="16" y="20" font-family="var(--font-mono)" font-size="9" fill="#c6ff00" font-weight="700">PE (TRILHO DIN TS-35)</text>
    </g>

    <!-- ========================================================
         DISTRIBUIÇÃO DA REFERÊNCIA NEGATIVA (0V_COMUM)
         ======================================================== -->
    <g id="bloco_equipotencializacao">
      <!-- Retorno 0V do polo negativo da Fonte PS1 para Barramento Central -->
      <path d="M 665 220 L 710 220 L 710 310 L 1050 310" class="wire w-gnd"/>
      <circle cx="710" cy="220" r="3.5" class="wire-junction"/>
      <path id="wire_0v_bus_main" d="M 710 310 L 1050 310" class="wire w-gnd"/>
      <circle cx="710" cy="310" r="4" fill="#00e676"/>
      <g transform="translate(720, 288)">
        <rect x="0" y="0" width="220" height="22" fill="#0f1d15" stroke="#00e676" stroke-width="1" rx="3"/>
        <text x="8" y="15" font-family="var(--font-mono)" font-size="9" fill="#00e676" font-weight="700">BARRAMENTO CENTRAL 0V_COMUM</text>
        <text x="8" y="32" font-family="var(--font-mono)" font-size="8" fill="#7fa890">Retorno Negativo Unificado (Potência e Lógica)</text>
      </g>
    </g>

    <!-- ========================================================
         ZONA 03: PROTEÇÕES FUSÍVEIS E NR-12 (S0 & K1)
         ======================================================== -->
    <g transform="translate(890, 55)">
      <rect x="0" y="0" width="410" height="26" fill="#14221b" stroke="#00e5ff" stroke-width="1.2" rx="3"/>
      <text x="12" y="18" font-family="var(--font-mono)" font-size="11" fill="#00e5ff" font-weight="700">ZONA 03: PROTEÇÃO FUSÍVEL &amp; SEGURANÇA SELETIVA NR-12</text>
    </g>

    <!-- Saída 12V de PS1 para Fusível F1 (10A Lâmina Geral) -->
    <path id="wire_12v_raw" d="M 665 185 L 750 185" class="wire w-12v-cont"/>
    <g transform="translate(750, 170)">
      <rect x="0" y="5" width="50" height="20" class="symbol-box-accent"/>
      <line x1="0" y1="15" x2="50" y2="15" stroke="#ff3344" stroke-width="2.5"/>
      <text x="25" y="0" font-family="var(--font-mono)" font-size="11" fill="#fff" font-weight="700" text-anchor="middle">F1 (10A)</text>
      <text x="25" y="36" font-family="var(--font-mono)" font-size="8" fill="#8fa699" text-anchor="middle">Geral 12V DC</text>
    </g>

    <!-- Nó pós-F1: divide em +12V_CONT e Circuito de Emergência S0/K1 -->
    <path id="wire_12v_post_f1" d="M 800 185 L 850 185" class="wire w-12v-cont"/>
    <circle cx="850" cy="185" r="3.5" class="wire-junction"/>

    <!-- RAMIFICAÇÃO 1: +12V_CONT (Barramento Contínuo 12V) -->
    <path id="wire_12v_cont_bus" d="M 850 185 L 850 115 L 1050 115" class="wire w-12v-cont"/>
    <circle cx="850" cy="115" r="3" class="wire-junction"/>
    <text x="860" y="110" class="lbl-wire" fill="#ff3344">+12V_CONT (Barramento Contínuo 12V)</text>

    <!-- Derivações a partir de +12V_CONT: F5 (1A Ring Light) e Buck U4 (5V ESP) -->
    <g transform="translate(860, 115)">
      <!-- Fusível F5 (1A Ring Light) -->
      <path d="M 60 0 L 60 25 L 70 25" class="wire w-12v-cont"/>
      <circle cx="60" cy="0" r="2.5" class="wire-junction"/>
      <g transform="translate(70, 15)">
        <rect x="0" y="0" width="35" height="18" class="symbol-box"/>
        <line x1="0" y1="9" x2="35" y2="9" stroke="#ff3344" stroke-width="1.8"/>
        <text x="17" y="-3" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">F5 (1A)</text>
      </g>
      <path id="wire_ring_light_out" d="M 105 24 L 190 24" class="wire w-12v-cont"/>
      <text x="110" y="38" font-family="var(--font-mono)" font-size="8" fill="#ff8a80">Luz Ring Light (Cúpula)</text>
    </g>

    <!-- ========================================================
         MÓDULO BUCK U4: 12V -> 5,0V (ESP32) COM ROTEAMENTO ORTOGONAL
         DESLOCADO PARA Y=125 (LIVRE DO CABEÇALHO DA ZONA 03)
         ======================================================== -->
    <!-- Fio de alimentação vindo do barramento +12V_CONT (Ortogonal) -->
    <path id="s1_wire_u4_in" d="M 1050 115 L 1120 115 L 1120 149 L 1160 149" class="wire w-12v-cont"/>
    <circle cx="1050" cy="115" r="3" class="wire-junction"/>

    <g id="s1_buck_u4" transform="translate(1160, 125)" class="cad-component-card">
      <rect x="0" y="0" width="95" height="48" class="symbol-box-accent" id="box_u4_s1"/>
      <text x="47" y="15" font-family="var(--font-mono)" font-size="9" fill="#ffd600" font-weight="700" text-anchor="middle">BUCK U4</text>
      <text x="47" y="27" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">12V → 5,0V (ESP)</text>
      <text x="47" y="39" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">MP1584EN 2A</text>
      <circle cx="0" cy="24" r="3.5" class="symbol-terminal" fill="#ff3344"/>
      <text x="8" y="27" font-family="var(--font-mono)" font-size="7" fill="#ff3344">IN+</text>
      <circle cx="95" cy="24" r="3.5" class="symbol-terminal" fill="#ffd600"/>
      <text x="87" y="27" font-family="var(--font-mono)" font-size="7" fill="#ffd600" text-anchor="end">OUT+</text>
      <!-- Terminal GND e Referência 0V_COMUM -->
      <circle cx="47" cy="48" r="3" class="symbol-terminal" fill="#00e676"/>
      <line x1="47" y1="51" x2="47" y2="62" stroke="#00e676" stroke-width="1.8"/>
      <line x1="39" y1="62" x2="55" y2="62" stroke="#00e676" stroke-width="2"/>
      <line x1="42" y1="65" x2="52" y2="65" stroke="#00e676" stroke-width="1.5"/>
      <line x1="45" y1="68" x2="49" y2="68" stroke="#00e676" stroke-width="1.2"/>
      <text x="58" y="66" font-family="var(--font-mono)" font-size="7" fill="#00e676">0V_COMUM</text>
    </g>

    <!-- Fio de saída +5V_ESP para Barramento, ESP32 e Sensores Ópticos IR (Ortogonal) -->
    <path id="s1_wire_5v_esp" d="M 1255 149 L 1380 149" class="wire w-5v"/>
    <text x="1265" y="142" class="lbl-wire" fill="#ffd600">+5V_ESP (Alimentação ESP32 DevKit V1 e Sensores Ópticos IR 5V)</text>

    <!-- ========================================================
         CIRCUITO DE PARADA DE EMERGÊNCIA NR-12 (S0 & RELÉ K1)
         COSTA A COSTA, 100% ALINHADO AOS TERMINAIS
         ======================================================== -->
    <g id="circuito_nr12" transform="translate(850, 185)">
      <!-- Linha de alimentação +12V_CONT entrando exatamente no Terminal 11 de S0 -->
      <path id="wire_estop_feed" d="M 0 0 L 0 65 L 55 65" class="wire w-12v-cont"/>
      
      <!-- BOTÃO DE EMERGÊNCIA S0 (Bloco Duplo: 1 NF + 1 NA) -->
      <g transform="translate(30, 25)" id="svg_btn_s0">
        <!-- Moldura de Botão NR-12 -->
        <rect x="0" y="0" width="115" height="95" fill="#1b1212" stroke="#ff1744" stroke-width="1.8" rx="4"/>
        <text x="57" y="15" font-family="var(--font-mono)" font-size="10" fill="#fff" font-weight="700" text-anchor="middle">S0: COGUMELO 22mm</text>
        <text x="57" y="26" font-family="var(--font-mono)" font-size="8" fill="#ff8a80" text-anchor="middle">NR-12 TRAVA GIRATÓRIA</text>

        <!-- Contato 1: NF 11-12 (Hardware Cutoff) -->
        <g transform="translate(10, 40)">
          <text x="0" y="4" font-family="var(--font-mono)" font-size="8" fill="#fff">11</text>
          <!-- Terminal 11 (X=15, Y=0) -->
          <circle cx="15" cy="0" r="3.5" class="symbol-terminal"/>
          <line x1="18" y1="0" x2="30" y2="0" stroke="#ff3344" stroke-width="2"/>
          <line id="s0_arm_nf" x1="30" y1="0" x2="55" y2="0" stroke="#00e676" stroke-width="2.5" class="relay-arm"/>
          <circle cx="30" cy="0" r="2.5" fill="#fff"/>
          <circle cx="55" cy="0" r="2.5" fill="#fff"/>
          <line x1="55" y1="0" x2="70" y2="0" stroke="#ff3344" stroke-width="2"/>
          <!-- Terminal 12 (X=70, Y=0) -->
          <circle cx="70" cy="0" r="3.5" class="symbol-terminal"/>
          <text x="80" y="4" font-family="var(--font-mono)" font-size="8" fill="#fff">12</text>
          <text x="42" y="14" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">Bobina K1</text>
        </g>

        <!-- Contato 2: NA 13-14 (Firmware Monitor) -->
        <g transform="translate(10, 70)">
          <text x="0" y="4" font-family="var(--font-mono)" font-size="8" fill="#fff">13</text>
          <circle cx="15" cy="0" r="3.5" class="symbol-terminal"/>
          <line x1="18" y1="0" x2="30" y2="0" stroke="#b388ff" stroke-width="2"/>
          <line id="s0_arm_na" x1="30" y1="0" x2="52" y2="-10" stroke="#ff1744" stroke-width="2" class="relay-arm"/>
          <circle cx="30" cy="0" r="2.5" fill="#fff"/>
          <circle cx="55" cy="0" r="2.5" fill="#fff"/>
          <line x1="55" y1="0" x2="70" y2="0" stroke="#b388ff" stroke-width="2"/>
          <circle cx="70" cy="0" r="3.5" class="symbol-terminal"/>
          <text x="80" y="4" font-family="var(--font-mono)" font-size="8" fill="#fff">14</text>
          <text x="42" y="14" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">GPIO 27 ESP</text>
        </g>
      </g>

      <!-- Fio perfeitamente horizontal saindo do terminal 12 de S0 para A1 de K1 -->
      <path id="wire_k1_coil_in" d="M 110 65 L 180 65" class="wire w-12v-cont"/>
      
      <!-- Fio saindo do terminal 14 de S0 para GPIO 27 do ESP32 com Bandeira Técnica -->
      <path id="wire_estop_firmware" d="M 110 95 L 200 95 L 200 135 L 250 135" class="wire w-sig"/>
      <g transform="translate(250, 135)">
        <polygon points="0,0 8,-4 8,-2 14,-2 14,2 8,2 8,4" fill="#b388ff"/>
        <rect x="16" y="-10" width="165" height="20" fill="#1b1226" stroke="#b388ff" stroke-width="1.2" rx="3"/>
        <text x="22" y="4" font-family="var(--font-mono)" font-size="8" fill="#b388ff" font-weight="700">➔ VAI P/ FL03 (GPIO 27 ESP32)</text>
      </g>
      <!-- Conexão do terminal 13 de S0 para 0V_COMUM -->
      <path d="M 55 95 L 20 95 L 20 125 L -140 125" class="wire w-gnd"/>

      <!-- RELÉ AUTOMOTIVO AUXILIAR K1 (12V DC — 40A) COM TERMINAIS ALINHADOS -->
      <g transform="translate(160, 25)">
        <rect x="0" y="0" width="90" height="95" class="symbol-box-accent" id="box_k1"/>
        <text x="45" y="16" font-family="var(--font-mono)" font-size="11" fill="#fff" font-weight="700" text-anchor="middle">RELÉ K1</text>
        <text x="45" y="27" font-family="var(--font-mono)" font-size="8" fill="#ff8a80" text-anchor="middle">12V DC / 40A</text>
        
        <!-- Bobina A1-A2 -->
        <g transform="translate(10, 30)">
          <!-- Terminal A1 (Y=10) -->
          <circle cx="10" cy="10" r="4" class="symbol-terminal"/>
          <text x="2" y="6" font-family="var(--font-mono)" font-size="8" fill="#8fa699">A1</text>
          <!-- Caixa da Bobina -->
          <rect x="5" y="15" width="10" height="25" fill="#18261e" stroke="#00e5ff" stroke-width="1.2"/>
          <line x1="5" y1="15" x2="15" y2="40" stroke="#00e5ff" stroke-width="1.2"/>
          <!-- Terminal A2 (Y=45) -->
          <circle cx="10" cy="45" r="4" class="symbol-terminal"/>
          <text x="2" y="55" font-family="var(--font-mono)" font-size="8" fill="#8fa699">A2</text>
          <!-- Diodo 1N4007 Antiparalelo -->
          <line x1="17" y1="12" x2="17" y2="43" stroke="#00e676" stroke-width="1.2"/>
        </g>
        
        <!-- Contato de Potência NA 30-87 -->
        <g transform="translate(45, 30)">
          <!-- Terminal 30 (Entrada de Força) -->
          <circle cx="15" cy="10" r="4" class="symbol-terminal"/>
          <text x="15" y="0" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">30</text>
          <line x1="15" y1="10" x2="22" y2="10" stroke="#ff3344" stroke-width="2"/>
          <line id="k1_contact_arm" x1="22" y1="10" x2="35" y2="10" stroke="#00e676" stroke-width="2.5" class="relay-arm"/>
          <circle cx="22" cy="10" r="2" fill="#fff"/>
          <circle cx="35" cy="10" r="2" fill="#fff"/>
          <line x1="35" y1="10" x2="42" y2="10" stroke="#ff1744" stroke-width="2.5"/>
          <!-- Terminal 87 (Saída de Força para +12V_AT) -->
          <circle cx="42" cy="10" r="4" class="symbol-terminal"/>
          <text x="42" y="0" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">87</text>
        </g>
      </g>

      <!-- Retorno da Bobina A2 de K1 para 0V_COMUM (Ortogonal) -->
      <path d="M 180 100 L 180 125 L -140 125" class="wire w-gnd"/>
      <circle cx="180" cy="125" r="2.5" class="wire-junction"/>

      <!-- Entrada de Força no Terminal 30 de K1 (vinda de +12V_CONT pós-F1) -->
      <path d="M 0 0 L 220 0 L 220 65" class="wire w-12v-cont"/>
      <circle cx="220" cy="0" r="3" class="wire-junction"/>

      <!-- Saída de Potência do Terminal 87 de K1: GERA O BARRAMENTO +12V_AT -->
      <path id="wire_k1_contact_out" d="M 247 65 L 350 65" class="wire w-12v-at"/>
      <text x="252" y="42" font-family="var(--font-mono)" font-size="8.5" font-weight="600" fill="#ff1744">+12V_AT (12V Atuadores Seccionável)</text>
    </g>

    <!-- DERIVAÇÕES A PARTIR DO BARRAMENTO +12V_AT (FOLHA 01) -->
    <g transform="translate(1200, 250)">
      <!-- Ramo 1: Fusível F3 (5A) para Motorredutor Esteira M1 -->
      <g transform="translate(0, 0)">
        <path id="wire_12v_at_to_f3" d="M 0 0 L 30 0" class="wire w-12v-at"/>
        <g transform="translate(30, -10)">
          <rect x="0" y="0" width="40" height="20" class="symbol-box"/>
          <line x1="0" y1="10" x2="40" y2="10" stroke="#ff1744" stroke-width="2"/>
          <text x="20" y="-3" font-family="var(--font-mono)" font-size="9" fill="#fff" text-anchor="middle">F3 (5A)</text>
        </g>
        <path id="wire_f3_out" d="M 70 0 L 120 0" class="wire w-12v-at"/>
        <text x="125" y="4" font-family="var(--font-mono)" font-size="9" fill="#ff8a80">Alimentação Motor M1 (via D4184)</text>
      </g>

      <!-- Ramo 2: Fusível F2 (3A) para Buck XL4015 (Servo MG996R) -->
      <g transform="translate(0, 50)">
        <path id="wire_12v_at_to_f2" d="M 0 -50 L 0 0 L 30 0" class="wire w-12v-at"/>
        <circle cx="0" cy="-50" r="3" class="wire-junction"/>
        <g transform="translate(30, -10)">
          <rect x="0" y="0" width="40" height="20" class="symbol-box"/>
          <line x1="0" y1="10" x2="40" y2="10" stroke="#ff1744" stroke-width="2"/>
          <text x="20" y="-3" font-family="var(--font-mono)" font-size="9" fill="#fff" text-anchor="middle">F2 (3A)</text>
        </g>
        <!-- Buck XL4015 -->
        <path d="M 70 0 L 90 0" class="wire w-12v-at"/>
        <g transform="translate(90, -15)">
          <rect x="0" y="0" width="65" height="30" class="symbol-box-accent"/>
          <text x="32" y="12" font-family="var(--font-mono)" font-size="8" fill="#ff9100" text-anchor="middle">BUCK U2</text>
          <text x="32" y="23" font-family="var(--font-mono)" font-size="7" fill="#8fa699" text-anchor="middle">XL4015 (6,0V)</text>
          <!-- Terminal GND e Referência 0V_COMUM -->
          <circle cx="32" cy="30" r="2.8" class="symbol-terminal" fill="#00e676"/>
          <line x1="32" y1="33" x2="32" y2="42" stroke="#00e676" stroke-width="1.6"/>
          <line x1="25" y1="42" x2="39" y2="42" stroke="#00e676" stroke-width="1.8"/>
          <line x1="28" y1="45" x2="36" y2="45" stroke="#00e676" stroke-width="1.4"/>
          <line x1="30" y1="48" x2="34" y2="48" stroke="#00e676" stroke-width="1.2"/>
          <text x="32" y="57" font-family="var(--font-mono)" font-size="6.5" fill="#00e676" text-anchor="middle">0V_COMUM</text>
        </g>
        <!-- Saída +6V_SERVO com Capacitor 1000uF e Referência 0V_COMUM -->
        <path id="wire_6v_bus_out" d="M 155 0 L 260 0" class="wire w-6v"/>
        <g transform="translate(170, 0)">
          <circle cx="10" cy="0" r="2.5" class="wire-junction"/>
          <line x1="10" y1="0" x2="10" y2="12" stroke="#ff9100" stroke-width="1.6"/>
          <line x1="4" y1="12" x2="16" y2="12" stroke="#ff9100" stroke-width="2"/>
          <line x1="4" y1="16" x2="16" y2="16" stroke="#00e676" stroke-width="2"/>
          <line x1="10" y1="16" x2="10" y2="27" stroke="#00e676" stroke-width="1.6"/>
          <line x1="4" y1="27" x2="16" y2="27" stroke="#00e676" stroke-width="1.8"/>
          <line x1="6" y1="30" x2="14" y2="30" stroke="#00e676" stroke-width="1.4"/>
          <line x1="8" y1="33" x2="12" y2="33" stroke="#00e676" stroke-width="1.2"/>
          <text x="20" y="16" font-family="var(--font-mono)" font-size="8" fill="#ff9100">C1: 1000µF/16V</text>
          <text x="20" y="28" font-family="var(--font-mono)" font-size="6.5" fill="#00e676">0V_COMUM</text>
        </g>
        <text x="265" y="4" class="lbl-wire" fill="#ff9100">+6V_SERVO (Empurrador Linear MG996R)</text>
      </g>
    </g>

    <!-- ========================================================
         QUADRO SINÓPTICO DOS 6 BARRAMENTOS OFICIAIS DO SISTEMA
         ======================================================== -->
    <g transform="translate(60, 520)">
      <rect x="0" y="0" width="990" height="280" fill="#0f1612" stroke="#2a3d31" stroke-width="1.5" rx="5"/>
      <rect x="0" y="0" width="990" height="28" fill="#14221b" stroke="#2a3d31" stroke-width="1" rx="5 5 0 0"/>
      <text x="16" y="18" font-family="var(--font-mono)" font-size="11" fill="#00e5ff" font-weight="700">QUADRO SINÓPTICO DOS 6 BARRAMENTOS ELÉTRICOS OFICIAIS (PADRONIZAÇÃO IEC / NBR 5410)</text>

      <g transform="translate(20, 42)">
        <!-- 1. Barramento +12V_CONT -->
        <g transform="translate(0, 0)">
          <rect x="0" y="0" width="950" height="30" fill="#121e19" rx="3"/>
          <line x1="10" y1="15" x2="60" y2="15" stroke="#ff3344" stroke-width="4"/>
          <text x="75" y="19" font-family="var(--font-mono)" font-size="11" fill="#ff3344" font-weight="700">+12V_CONT</text>
          <text x="200" y="19" font-family="var(--font-sans)" font-size="10" fill="#e0e8e3">Fonte PS1 (12V 10A) pós-fusível F1 (10A). Barramento contínuo (Ring Light 12V, Buck ESP32/Sensores, Comando S0).</text>
          <text x="820" y="19" font-family="var(--font-mono)" font-size="10" fill="#00e676" id="status_bar_12v_cont">STATUS: 12,0V ATIVO</text>
        </g>

        <!-- 2. Barramento +12V_AT -->
        <g transform="translate(0, 38)">
          <rect x="0" y="0" width="950" height="30" fill="#121e19" rx="3"/>
          <line x1="10" y1="15" x2="60" y2="15" stroke="#ff1744" stroke-width="4" id="line_legend_12v_at"/>
          <text x="75" y="19" font-family="var(--font-mono)" font-size="11" fill="#ff1744" font-weight="700">+12V_AT</text>
          <text x="200" y="19" font-family="var(--font-sans)" font-size="10" fill="#e0e8e3">Barramento Seccionável de Atuadores (Chaveado por K1 via emergência S0). Alimenta Motorredutor M1 e Buck U2.</text>
          <text x="820" y="19" font-family="var(--font-mono)" font-size="10" fill="#00e676" id="status_bar_12v_at">STATUS: 12,0V ENERGIZADO</text>
        </g>

        <!-- 3. Barramento +6V_SERVO -->
        <g transform="translate(0, 76)">
          <rect x="0" y="0" width="950" height="30" fill="#121e19" rx="3"/>
          <line x1="10" y1="15" x2="60" y2="15" stroke="#ff9100" stroke-width="4" id="line_legend_6v"/>
          <text x="75" y="19" font-family="var(--font-mono)" font-size="11" fill="#ff9100" font-weight="700">+6V_SERVO</text>
          <text x="200" y="19" font-family="var(--font-sans)" font-size="10" fill="#e0e8e3">Conversor Buck XL4015 (5A) com capacitor de pico 1000µF. Fornece 6,00V DC estáveis p/ Servomotor MG996R.</text>
          <text x="820" y="19" font-family="var(--font-mono)" font-size="10" fill="#00e676" id="status_bar_6v">STATUS: 6,00V ESTÁVEL</text>
        </g>

        <!-- 4. Barramento +5V_ESP -->
        <g transform="translate(0, 114)">
          <rect x="0" y="0" width="950" height="30" fill="#121e19" rx="3"/>
          <line x1="10" y1="15" x2="60" y2="15" stroke="#ffd600" stroke-width="4"/>
          <text x="75" y="19" font-family="var(--font-mono)" font-size="11" fill="#ffd600" font-weight="700">+5V_ESP</text>
          <text x="200" y="19" font-family="var(--font-sans)" font-size="10" fill="#e0e8e3">Conversor Buck U4 MP1584 (12V → 5V 2A). Alimenta tanto o ESP32 quanto os 2x Sensores Ópticos IR 5V.</text>
          <text x="820" y="19" font-family="var(--font-mono)" font-size="10" fill="#00e676" id="status_bar_5v">STATUS: 5,02V REGULADO</text>
        </g>

        <!-- 5. Barramento 0V_COMUM -->
        <g transform="translate(0, 152)">
          <rect x="0" y="0" width="950" height="30" fill="#121e19" rx="3"/>
          <line x1="10" y1="15" x2="60" y2="15" stroke="#00e676" stroke-width="4"/>
          <text x="75" y="19" font-family="var(--font-mono)" font-size="11" fill="#00e676" font-weight="700">0V_COMUM</text>
          <text x="200" y="19" font-family="var(--font-sans)" font-size="10" fill="#e0e8e3">Retorno de Potência e Lógico Unificado (Polo negativo da fonte PS1 e dos conversores DC-DC interligados na régua X1).</text>
          <text x="820" y="19" font-family="var(--font-mono)" font-size="10" fill="#00e676">STATUS: 0,00V REF COMUM</text>
        </g>

        <!-- 6. Barramento PE (Proteção) -->
        <g transform="translate(0, 190)">
          <rect x="0" y="0" width="950" height="30" fill="#121e19" rx="3"/>
          <line x1="10" y1="15" x2="60" y2="15" stroke="#c6ff00" stroke-width="4" stroke-dasharray="6 3"/>
          <text x="75" y="19" font-family="var(--font-mono)" font-size="11" fill="#c6ff00" font-weight="700">PE (TERRA)</text>
          <text x="200" y="19" font-family="var(--font-sans)" font-size="10" fill="#e0e8e3">Aterramento de Carcaça e Trilho DIN TS-35. NBR 5410. Isolado galvanicamente do 0V lógico.</text>
          <text x="820" y="19" font-family="var(--font-mono)" font-size="10" fill="#c6ff00">STATUS: CONECTADO PE</text>
        </g>
      </g>
    </g>

    <!-- NOTAS DE ENGENHARIA DESTA PRANCHA -->
    <g transform="translate(1080, 520)">
      <rect x="0" y="0" width="585" height="280" fill="#0c120f" stroke="#1f3026" stroke-width="1.5" rx="4"/>
      <text x="14" y="20" font-family="var(--font-mono)" font-size="11" fill="#00e5ff" font-weight="700">NOTAS TÉCNICAS DE MONTAGEM &amp; NR-12:</text>
      
      <text x="14" y="42" font-family="var(--font-sans)" font-size="10" fill="#b0c4b8">1. <tspan fill="#ffffff" font-weight="700">CORTE DE SEGURANÇA SELETIVO:</tspan> O botão S0 opera em dois canais:</text>
      <text x="28" y="56" font-family="var(--font-sans)" font-size="9" fill="#8fa699">• Canal de Hardware (NF 11-12): desenergiza a bobina de K1, seccionando +12V_AT.</text>
      <text x="28" y="70" font-family="var(--font-sans)" font-size="9" fill="#8fa699">• Canal de Firmware (NA 13-14): aterra GPIO 27, disparando alarme serial imediato.</text>
      
      <text x="14" y="92" font-family="var(--font-sans)" font-size="10" fill="#b0c4b8">2. <tspan fill="#ffffff" font-weight="700">CONTINUIDADE DA VISÃO &amp; PROCESSAMENTO:</tspan> Mesmo com a emergência</text>
      <text x="28" y="106" font-family="var(--font-sans)" font-size="9" fill="#8fa699">acionada, os barramentos +12V_CONT (luz) e +5V_ESP (ESP32 e sensores ópticos IR 5V)</text>
      <text x="28" y="120" font-family="var(--font-sans)" font-size="9" fill="#8fa699">permanecem energizados para fins de diagnóstico e inspeção visual da bancada.</text>
      
      <text x="14" y="142" font-family="var(--font-sans)" font-size="10" fill="#b0c4b8">3. <tspan fill="#ffffff" font-weight="700">POTÊNCIA DO RELÉ K1:</tspan> Especificado relé automotivo de 40A para suportar</text>
      <text x="28" y="156" font-family="var(--font-sans)" font-size="9" fill="#8fa699">as correntes combinadas de inrush do motor DC e servomotor MG996R sem</text>
      <text x="28" y="170" font-family="var(--font-sans)" font-size="9" fill="#8fa699">risco de colagem de contatos (soldagem por arco elétrico).</text>

      <text x="14" y="192" font-family="var(--font-sans)" font-size="10" fill="#b0c4b8">4. <tspan fill="#ffffff" font-weight="700">ATERRAMENTO FUNCIONAL E PROTEÇÃO:</tspan> A carcaça da fonte PS1 e a estrutura</text>
      <text x="28" y="206" font-family="var(--font-sans)" font-size="9" fill="#8fa699">metálica da esteira devem estar aterradas no barramento PE via terminal olhal.</text>
      <text x="28" y="220" font-family="var(--font-sans)" font-size="9" fill="#8fa699">O 0V_COMUM não deve ser aterrado em múltiplos pontos para evitar laços de terra.</text>

      <!-- BLOCO: HISTÓRICO DA MIGRAÇÃO (2026-Q3) CONFORME AUDITORIA -->
      <g transform="translate(14, 235)">
        <rect x="0" y="0" width="557" height="34" fill="#132019" stroke="#00e676" stroke-width="1" rx="3"/>
        <text x="10" y="14" font-family="var(--font-mono)" font-size="8.5" fill="#00e676" font-weight="700">HISTÓRICO DA MIGRAÇÃO (2026-Q3):</text>
        <text x="10" y="26" font-family="var(--font-sans)" font-size="8" fill="#e0e8e3">Migração 2026-Q3: eliminada fonte PS2 24V, optoacoplador PC817 e fusível F4. Arquitetura atual 100% mono-fonte 12V (PS1 10A).</text>
      </g>
    </g>
    """
    return svg
