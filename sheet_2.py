# -*- coding: utf-8 -*-
"""
Sheet 2: Diagrama Multifilar de Potência — Atuadores M1 e M2 (Corrigido)
AmazonVision 4.0 - XXI Feira Tecnológica FUCAPI 2026
"""

from sheet_frame import get_cad_frame

def get_sheet_2():
    frame = get_cad_frame(2, "DIAGRAMA MULTIFILAR DE POTÊNCIA — ATUADORES M1 E M2", "Motorredutor da Esteira, Módulo MOSFET D4184, Empurrador Linear MG996R e Buck XL4015")
    
    svg = f"""
    {frame}
    
    <!-- ========================================================
         FOLHA 02: DIAGRAMA DE POTÊNCIA (ATUADORES M1 E M2)
         ======================================================== -->

    <!-- SEÇÃO 1: CIRCUITO DO MOTORREDUTOR DA ESTEIRA (M1) -->
    <g transform="translate(60, 55)">
      <rect x="0" y="0" width="460" height="26" fill="#14221b" stroke="#ff1744" stroke-width="1.2" rx="3"/>
      <text x="12" y="18" font-family="var(--font-mono)" font-size="11" fill="#ff1744" font-weight="700">CIRCUITO 01: ACIONAMENTO DO MOTORREDUTOR DC 12V (M1)</text>
    </g>

    <!-- ENTRADA DE BARRAMENTO +12V_AT E RETORNO 0V_COMUM -->
    <g transform="translate(60, 100)">
      <!-- Barra +12V_AT -->
      <line x1="0" y1="20" x2="60" y2="20" class="wire w-12v-at" id="s2_wire_12v_at_entry"/>
      <circle cx="60" cy="20" r="3" class="wire-junction"/>
      <rect x="0" y="5" width="80" height="15" fill="#1b1212" rx="2"/>
      <text x="4" y="16" class="lbl-wire" fill="#ff1744">+12V_AT (FL01)</text>

      <!-- Fusível F3 (5A) -->
      <g transform="translate(70, 10)">
        <rect x="0" y="0" width="55" height="22" class="symbol-box"/>
        <line x1="0" y1="11" x2="55" y2="11" stroke="#ff1744" stroke-width="2.2"/>
        <text x="27" y="-3" font-family="var(--font-mono)" font-size="10" fill="#fff" font-weight="700" text-anchor="middle">F3 (5A)</text>
        <text x="27" y="32" font-family="var(--font-mono)" font-size="8" fill="#8fa699" text-anchor="middle">Lâmina DIN</text>
      </g>

      <!-- Anilha W101 e Borne X3:1 -->
      <path id="s2_wire_w101" d="M 125 21 L 180 21" class="wire w-12v-at"/>
      <rect x="130" y="10" width="40" height="13" fill="#1e2c24" rx="2"/>
      <text x="150" y="20" font-family="var(--font-mono)" font-size="8" fill="#00e5ff" font-weight="700" text-anchor="middle">W101 (1mm²)</text>

      <!-- Borne X3:1 (MOT+) -->
      <g transform="translate(180, 10)">
        <circle cx="10" cy="11" r="5" class="symbol-terminal"/>
        <text x="10" y="2" font-family="var(--font-mono)" font-size="9" fill="#fff" font-weight="700" text-anchor="middle">X3:1</text>
        <text x="10" y="30" font-family="var(--font-mono)" font-size="8" fill="#ff1744" text-anchor="middle">MOT+</text>
      </g>

      <!-- Fio para o Motor M1 -->
      <path id="s2_wire_mot_plus" d="M 195 21 L 270 21 L 270 60" class="wire w-12v-at"/>
      <circle cx="270" cy="60" r="3" class="wire-junction"/>

      <!-- SÍMBOLO DO MOTORREDUTOR DC 12V (M1) COM ANIMAÇÃO CENTRADA CORRIGIDA -->
      <g transform="translate(230, 60)" id="svg_motor_group">
        <rect x="0" y="0" width="80" height="80" class="symbol-box-accent"/>
        <!-- Círculo do Motor DC -->
        <circle cx="40" cy="40" r="26" fill="#15241b" stroke="#00e676" stroke-width="2"/>
        <!-- Escovas de Carvão -->
        <rect x="11" y="34" width="6" height="12" fill="#8fa699"/>
        <rect x="63" y="34" width="6" height="12" fill="#8fa699"/>
        
        <!-- Rotor Interno com Engrenagem Animada (Grupo Duplo Corrigido: gira no centro exato) -->
        <g transform="translate(40,40)">
          <g id="motor_rotor_spin">
            <circle cx="0" cy="0" r="16" fill="#1b3324" stroke="#00e5ff" stroke-width="1.5"/>
            <line x1="-12" y1="0" x2="12" y2="0" stroke="#00e676" stroke-width="2"/>
            <line x1="0" y1="-12" x2="0" y2="12" stroke="#00e676" stroke-width="2"/>
            <circle cx="0" cy="0" r="4" fill="#fff"/>
          </g>
        </g>
        
        <text x="40" y="16" font-family="var(--font-mono)" font-size="11" fill="#fff" font-weight="700" text-anchor="middle">M1</text>
        <text x="40" y="74" font-family="var(--font-mono)" font-size="8" fill="#8fa699" text-anchor="middle">DC 12V 60RPM</text>

        <!-- Redutor de Engrenagens Acoplado -->
        <rect x="80" y="25" width="22" height="30" fill="#1f3026" stroke="#4e6b5a" rx="2"/>
        <text x="91" y="43" font-family="var(--font-mono)" font-size="7" fill="#00e5ff" text-anchor="middle">GEAR</text>
      </g>

      <!-- Borne X3:2 (MOT-) -->
      <path id="s2_wire_mot_minus" d="M 270 140 L 270 180 L 195 180" class="wire" stroke="#859a8e" stroke-width="2"/>
      <circle cx="270" cy="140" r="3" class="wire-junction"/>
      <g transform="translate(180, 170)">
        <circle cx="10" cy="10" r="5" class="symbol-terminal"/>
        <text x="10" y="2" font-family="var(--font-mono)" font-size="9" fill="#fff" font-weight="700" text-anchor="middle">X3:2</text>
        <text x="10" y="28" font-family="var(--font-mono)" font-size="8" fill="#859a8e" text-anchor="middle">MOT-</text>
      </g>

      <!-- DIODO SCHOTTKY FLYBACK 1N5822 (40V / 3A) AFASTADO 50px PARA A DIREITA (ZERO COLISÃO) -->
      <g transform="translate(375, 75)">
        <rect x="0" y="0" width="85" height="50" fill="#101914" stroke="#ff9100" stroke-width="1.5" rx="3"/>
        <text x="42" y="12" font-family="var(--font-mono)" font-size="8" fill="#ff9100" font-weight="700" text-anchor="middle">DIODO FLYBACK</text>
        <text x="42" y="22" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">1N5822 (3A/40V)</text>
        
        <!-- Símbolo do Diodo Schottky Antiparalelo -->
        <g transform="translate(42, 35)">
          <line x1="0" y1="-12" x2="0" y2="12" stroke="#ff9100" stroke-width="2"/>
          <polygon points="-8,-4 8,-4 0,8" fill="#ff9100"/>
          <line x1="-8" y1="-4" x2="8" y2="-4" stroke="#fff" stroke-width="2"/>
          <line x1="-8" y1="-4" x2="-8" y2="-1" stroke="#fff" stroke-width="1.5"/>
          <line x1="8" y1="-4" x2="8" y2="-7" stroke="#fff" stroke-width="1.5"/>
        </g>
      </g>
      <!-- Fios do Diodo Flyback perfeitamente ortogonais conectando a MOT+ e MOT- -->
      <path d="M 270 60 L 417 60 L 417 75" class="wire w-12v-at"/>
      <path d="M 417 125 L 417 180 L 270 180" class="wire" stroke="#859a8e" stroke-width="2"/>
      <circle cx="417" cy="60" r="2.5" class="wire-junction"/>
      <circle cx="417" cy="180" r="2.5" class="wire-junction"/>

      <!-- Cabo W102 de X3:2 para o Módulo MOSFET D4184 -->
      <path id="s2_wire_w102" d="M 180 180 L 120 180 L 120 220 L 490 220 L 490 170 L 520 170" class="wire" stroke="#859a8e" stroke-width="2.2"/>
      <rect x="230" y="212" width="70" height="14" fill="#1e2c24" rx="2"/>
      <text x="265" y="222" font-family="var(--font-mono)" font-size="8" fill="#00e5ff" font-weight="700" text-anchor="middle">W102 (Preto 1mm²)</text>

      <!-- ========================================================
           MÓDULO DRIVER MOSFET D4184 (AOD4184 DUPLO 40V / 15A)
           ======================================================== -->
      <g transform="translate(520, 80)" id="svg_mosfet_module">
        <rect x="0" y="0" width="220" height="150" class="symbol-box-accent" id="box_mosfet"/>
        <text x="12" y="20" font-family="var(--font-mono)" font-size="11" fill="#fff" font-weight="700">MÓDULO MOSFET D4184</text>
        <text x="12" y="32" font-family="var(--font-mono)" font-size="8" fill="#00e5ff">AOD4184 DUPLO N-CHANNEL (40V / 15A)</text>
        <text x="12" y="43" font-family="var(--font-mono)" font-size="8" fill="#8fa699">Rds(on) &lt; 8.5 mΩ | Trigger: 3,3V a 12V</text>

        <!-- Terminais de Potência do Módulo -->
        <g transform="translate(10, 60)">
          <circle cx="10" cy="30" r="4.5" class="symbol-terminal"/>
          <text x="22" y="33" class="lbl-pin">LOAD- (DRENO)</text>
          <circle cx="10" cy="65" r="4.5" class="symbol-terminal"/>
          <text x="22" y="68" class="lbl-pin" fill="#00e676">GND-IN (SOURCE)</text>
        </g>

        <!-- Esquema Interno do Transistor MOSFET N -->
        <g transform="translate(120, 65)">
          <rect x="0" y="0" width="85" height="70" fill="#0e1713" stroke="#253a2f" rx="3"/>
          <text x="42" y="14" font-family="var(--font-mono)" font-size="8" fill="#00e676" text-anchor="middle">2x AOD4184</text>
          <line x1="18" y1="25" x2="18" y2="55" stroke="#fff" stroke-width="2"/>
          <line x1="26" y1="22" x2="26" y2="30" stroke="#00e5ff" stroke-width="2"/>
          <line x1="26" y1="36" x2="26" y2="44" stroke="#00e5ff" stroke-width="2"/>
          <line x1="26" y1="50" x2="26" y2="58" stroke="#00e5ff" stroke-width="2"/>
          <line x1="26" y1="26" x2="48" y2="26" stroke="#fff" stroke-width="1.8"/>
          <line x1="26" y1="54" x2="48" y2="54" stroke="#fff" stroke-width="1.8"/>
          <polygon points="26,40 36,36 36,44" fill="#00e5ff"/>
          <line x1="36" y1="40" x2="48" y2="40" stroke="#fff" stroke-width="1.5"/>
          <line x1="48" y1="40" x2="48" y2="54" stroke="#fff" stroke-width="1.5"/>
          <line x1="8" y1="40" x2="18" y2="40" stroke="#d500f9" stroke-width="2"/>
        </g>

        <!-- Terminais de Controle Lógico -->
        <g transform="translate(180, 25)">
          <circle cx="30" cy="15" r="4" class="symbol-terminal"/>
          <text x="20" y="10" class="lbl-pin" fill="#d500f9" text-anchor="end">TRIG (PWM)</text>
          <circle cx="30" cy="35" r="4" class="symbol-terminal"/>
          <text x="20" y="38" class="lbl-pin" fill="#00e676" text-anchor="end">GND-SIG</text>
        </g>
      </g>

      <!-- Fio de aterramento do GND-SIG do MOSFET para o barramento 0V_COMUM (Zero Terminal Flutuante) -->
      <path d="M 730 140 L 760 140 L 760 250 L 530 250" class="wire w-gnd"/>
      <circle cx="760" cy="140" r="2.5" class="wire-junction"/>
      <circle cx="530" cy="250" r="3" class="wire-junction"/>
      <text x="765" y="195" font-family="var(--font-mono)" font-size="7" fill="#00e676">GND-SIG ➔ 0V</text>

      <!-- Fio de Saída do MOSFET GND-IN para Barramento 0V_COMUM -->
      <path id="s2_wire_w103" d="M 530 205 L 530 250 L 0 250" class="wire w-gnd"/>
      <rect x="230" y="242" width="70" height="14" fill="#1e2c24" rx="2"/>
      <text x="265" y="252" font-family="var(--font-mono)" font-size="8" fill="#00e676" font-weight="700" text-anchor="middle">W103 (0V Retorno)</text>

      <!-- Sinal de Disparo do ESP32: GPIO 19 -->
      <path id="s2_wire_w201" d="M 730 120 L 780 120" class="wire w-sig"/>
      <text x="790" y="124" font-family="var(--font-mono)" font-size="9" fill="#d500f9" font-weight="700">W201: GPIO 19 (PIN_MOTOR_ONOFF)</text>

      <!-- Indicador de Status Dinâmico do Motor -->
      <g transform="translate(770, 55)">
        <rect x="0" y="0" width="180" height="50" fill="#0e1813" stroke="#2a3d31" rx="4"/>
        <text x="12" y="18" font-family="var(--font-mono)" font-size="9" fill="#8fa699">TELEMETRIA MOTOR M1:</text>
        <text x="12" y="36" font-family="var(--font-mono)" font-size="12" fill="#00e676" font-weight="700" id="s2_motor_current_val">CORRENTE: 1.2A (NOM)</text>
      </g>
    </g>

    <!-- ========================================================
         SEÇÃO 2: EMPURRADOR LINEAR (SERVO MG996R BIELA-MANIVELA) E BUCK
         ======================================================== -->
    <g transform="translate(60, 420)">
      <rect x="0" y="0" width="460" height="26" fill="#14221b" stroke="#ff9100" stroke-width="1.2" rx="3"/>
      <text x="12" y="18" font-family="var(--font-mono)" font-size="11" fill="#ff9100" font-weight="700">CIRCUITO 02: EMPURRADOR LINEAR (MG996R) &amp; BUCK XL4015 (6V)</text>
    </g>

    <g transform="translate(60, 465)">
      <!-- Entrada Barramento +12V_AT -->
      <line x1="0" y1="20" x2="60" y2="20" class="wire w-12v-at" id="s2_wire_12v_at_servo_entry"/>
      <rect x="0" y="5" width="80" height="15" fill="#1b1212" rx="2"/>
      <text x="4" y="16" class="lbl-wire" fill="#ff1744">+12V_AT (FL01)</text>

      <!-- Fusível F2 (3A) Dedicado ao Servomotor -->
      <g transform="translate(70, 10)">
        <rect x="0" y="0" width="55" height="22" class="symbol-box"/>
        <line x1="0" y1="11" x2="55" y2="11" stroke="#ff1744" stroke-width="2.2"/>
        <text x="27" y="-3" font-family="var(--font-mono)" font-size="10" fill="#fff" font-weight="700" text-anchor="middle">F2 (3A)</text>
        <text x="27" y="32" font-family="var(--font-mono)" font-size="8" fill="#8fa699" text-anchor="middle">Proteção Servo</text>
      </g>

      <!-- Anilha W104 para Buck XL4015 -->
      <path id="s2_wire_w104" d="M 125 21 L 180 21" class="wire w-12v-at"/>
      <rect x="130" y="10" width="45" height="13" fill="#1e2c24" rx="2"/>
      <text x="152" y="20" font-family="var(--font-mono)" font-size="8" fill="#00e5ff" font-weight="700" text-anchor="middle">W104 (12V)</text>

      <!-- MÓDULO CONVERSOR BUCK STEP-DOWN XL4015 5A (U2) -->
      <g transform="translate(180, 0)">
        <rect x="0" y="0" width="220" height="135" class="symbol-box-accent" id="box_xl4015"/>
        <text x="12" y="20" font-family="var(--font-mono)" font-size="11" fill="#fff" font-weight="700">U2: BUCK XL4015 5A</text>
        <text x="12" y="32" font-family="var(--font-mono)" font-size="8" fill="#ff9100">STEP-DOWN DC-DC ALTA POTÊNCIA</text>
        <text x="12" y="44" font-family="var(--font-mono)" font-size="8" fill="#8fa699">Fsw: 180 kHz | Rendimento: 92%</text>

        <!-- Terminais de Entrada -->
        <circle cx="10" cy="65" r="4.5" class="symbol-terminal"/>
        <text x="22" y="68" class="lbl-pin" fill="#ff1744">IN+ (+12V_AT)</text>
        <circle cx="10" cy="105" r="4.5" class="symbol-terminal"/>
        <text x="22" y="108" class="lbl-pin" fill="#00e676">IN- (0V_COM)</text>

        <!-- Indutor Toroidal e Trimpot de Ajuste -->
        <g transform="translate(100, 50)">
          <circle cx="20" cy="20" r="16" fill="#152019" stroke="#ff9100" stroke-width="2"/>
          <text x="20" y="23" font-family="var(--font-mono)" font-size="7" fill="#ff9100" text-anchor="middle">47µH</text>
          <rect x="45" y="10" width="18" height="20" fill="#122538" stroke="#00e5ff" rx="2"/>
          <circle cx="54" cy="20" r="3" fill="#fff"/>
          <text x="54" y="38" font-family="var(--font-mono)" font-size="6" fill="#00e5ff" text-anchor="middle">Ajuste 6V</text>
        </g>

        <!-- Terminais de Saída -->
        <circle cx="210" cy="65" r="4.5" class="symbol-terminal"/>
        <text x="198" y="68" class="lbl-pin" fill="#ff9100" text-anchor="end">OUT+ (+6,0V)</text>
        <circle cx="210" cy="105" r="4.5" class="symbol-terminal"/>
        <text x="198" y="108" class="lbl-pin" fill="#00e676" text-anchor="end">OUT- (0V)</text>
      </g>

      <!-- Fio de Entrada IN- para 0V_COMUM -->
      <path d="M 190 105 L 0 105" class="wire w-gnd"/>

      <!-- CAPACITOR ELETROLÍTICO C1 (1000 µF × 16V) COM FIAÇÃO ROTEADA POR FORA E CONEXÃO DIRETA -->
      <g transform="translate(430, 40)">
        <rect x="-15" y="0" width="155" height="90" fill="#0f1914" stroke="#ff9100" stroke-width="1.5" rx="3"/>
        <text x="20" y="26" font-family="var(--font-mono)" font-size="7.5" fill="#ff9100" font-weight="700" text-anchor="middle">FILTRO DE</text>
        <text x="20" y="38" font-family="var(--font-mono)" font-size="7.5" fill="#ff9100" font-weight="700" text-anchor="middle">PICO C1</text>
        <text x="74" y="28" font-family="var(--font-mono)" font-size="7.5" fill="#fff" font-weight="700">1000 µF × 16V</text>
        <text x="74" y="40" font-family="var(--font-mono)" font-size="7" fill="#8fa699">Low-ESR / 105°C</text>

        <!-- Símbolo Capacitor Polarizado (Terminais em global 490,82 e 490,118) -->
        <g transform="translate(60, 60)">
          <line x1="0" y1="-18" x2="0" y2="-5" stroke="#ff9100" stroke-width="2"/>
          <circle cx="0" cy="-18" r="3" class="symbol-terminal"/>
          <line x1="-12" y1="-5" x2="12" y2="-5" stroke="#ff9100" stroke-width="2.5"/>
          <text x="-16" y="-8" font-family="var(--font-mono)" font-size="8" fill="#ff9100">+</text>
          <path d="M -12 2 Q 0 0 12 2" stroke="#fff" stroke-width="2" fill="none"/>
          <line x1="0" y1="2" x2="0" y2="18" stroke="#00e676" stroke-width="2"/>
          <circle cx="0" cy="18" r="3" class="symbol-terminal"/>
        </g>
      </g>

      <!-- Roteamento Limpo de Saída: Barramentos passam acima e abaixo de C1 com derivações verticais diretas aos terminais -->
      <!-- Linha +6V_SERVO passando ACIMA de C1 e conectando ao terminal + (490, 82) -->
      <path id="s2_wire_6v_out" d="M 390 65 L 410 65 L 410 20 L 580 20 L 580 65 L 600 65" class="wire w-6v"/>
      <path d="M 490 20 L 490 82" class="wire w-6v"/>
      <circle cx="490" cy="20" r="3" class="wire-junction"/>

      <!-- Linha 0V_GND passando ABAIXO de C1 e conectando ao terminal - (490, 118) -->
      <path d="M 390 105 L 410 105 L 410 145 L 580 145 L 580 105 L 600 105" class="wire w-gnd"/>
      <path d="M 490 145 L 490 118" class="wire w-gnd"/>
      <circle cx="490" cy="145" r="3" class="wire-junction"/>

      <!-- RÉGUA DE BORNES X3 (SAÍDA PARA O SERVO) - Textos 10px Acima dos Fios -->
      <g transform="translate(600, 45)">
        <!-- X3:4 (+6V) -->
        <circle cx="15" cy="20" r="5" class="symbol-terminal"/>
        <text x="15" y="2" font-family="var(--font-mono)" font-size="8" fill="#fff" font-weight="700" text-anchor="middle">X3:4</text>
        <rect x="23" y="4" width="58" height="13" fill="#0c1410" rx="2"/>
        <text x="25" y="14" font-family="var(--font-mono)" font-size="8" fill="#ff9100" font-weight="700">+6V SRV</text>

        <!-- X3:5 (GND) -->
        <circle cx="15" cy="60" r="5" class="symbol-terminal"/>
        <text x="15" y="42" font-family="var(--font-mono)" font-size="8" fill="#fff" font-weight="700" text-anchor="middle">X3:5</text>
        <rect x="23" y="44" width="58" height="13" fill="#0c1410" rx="2"/>
        <text x="25" y="54" font-family="var(--font-mono)" font-size="8" fill="#00e676" font-weight="700">GND SRV</text>

        <!-- X3:6 (PWM) -->
        <circle cx="15" cy="95" r="5" class="symbol-terminal"/>
        <text x="15" y="77" font-family="var(--font-mono)" font-size="8" fill="#fff" font-weight="700" text-anchor="middle">X3:6</text>
        <rect x="23" y="79" width="58" height="13" fill="#0c1410" rx="2"/>
        <text x="25" y="89" font-family="var(--font-mono)" font-size="8" fill="#d500f9" font-weight="700">PWM SRV</text>
      </g>

      <!-- Sinal PWM vindo do ESP32 GPIO 18 (Roteamento Limpo em Y=670 / Local Y=205, Zero Colisão com 0V_GND) -->
      <g transform="translate(0, 205)">
        <rect x="0" y="-12" width="140" height="22" fill="#22132e" stroke="#d500f9" stroke-width="1.2" rx="3"/>
        <text x="8" y="2" font-family="var(--font-mono)" font-size="9" fill="#d500f9" font-weight="700">W202: GPIO 18 (PWM)</text>
        <text x="8" y="12" font-family="var(--font-mono)" font-size="7" fill="#8fa699">FL03 ESP32 DevKit</text>
      </g>
      <path id="s2_wire_pwm_in" d="M 140 205 L 590 205 L 590 140 L 615 140" class="wire w-sig"/>

      <!-- Conexão Física Direta até os Terminais do Servo (Sem Paradas no Vazio!) -->
      <path d="M 615 65 L 780 65 L 780 70 L 815 70" class="wire w-6v"/>
      <path d="M 615 105 L 795 105 L 795 90 L 815 90" class="wire w-gnd"/>
      <path d="M 615 140 L 810 140 L 810 110 L 815 110" class="wire w-sig"/>

      <!-- ========================================================
           MECANISMO EMPURRADOR LINEAR (SERVO MG996R + BIELA-MANIVELA)
           SUBSTITUIÇÃO DA PÁ GIRATÓRIA POR SAPATA RETILÍNEA REAL
           ======================================================== -->
      <g transform="translate(815, 20)" id="svg_servo_unit">
        <rect x="0" y="0" width="220" height="150" class="symbol-box-accent"/>
        <text x="110" y="18" font-family="var(--font-mono)" font-size="11" fill="#fff" font-weight="700" text-anchor="middle">M2: EMPURRADOR LINEAR</text>
        <text x="110" y="30" font-family="var(--font-mono)" font-size="8" fill="#ff9100" text-anchor="middle">SERVO MG996R + BIELA-MANIVELA</text>

        <!-- Terminais do Servo Conectados Fisicamente -->
        <circle cx="0" cy="50" r="4.5" class="symbol-terminal" fill="#ff9100"/>
        <text x="6" y="53" class="lbl-pin" fill="#ff9100">+6V</text>
        <circle cx="0" cy="70" r="4.5" class="symbol-terminal" fill="#00e676"/>
        <text x="6" y="73" class="lbl-pin" fill="#00e676">GND</text>
        <circle cx="0" cy="90" r="4.5" class="symbol-terminal" fill="#d500f9"/>
        <text x="6" y="93" class="lbl-pin" fill="#d500f9">PWM</text>

        <!-- Corpo do Servomotor MG996R -->
        <rect x="35" y="45" width="50" height="60" fill="#16221b" stroke="#4e6b5a" rx="3"/>
        <circle cx="60" cy="75" r="14" fill="#0f1813" stroke="#ff9100" stroke-width="1.8"/>

        <!-- Disco Manivela (Horn 25T) -->
        <g id="s2_crank_horn" transform="translate(60, 75)">
          <circle cx="0" cy="0" r="11" fill="#1b2c22" stroke="#00e5ff"/>
          <line x1="0" y1="0" x2="10" y2="0" stroke="#ff9100" stroke-width="3" id="s2_crank_pin"/>
          <circle cx="10" cy="0" r="2.5" fill="#fff"/>
        </g>

        <!-- Biela Articulada de Conexão -->
        <line id="s2_connecting_rod" x1="70" y1="75" x2="135" y2="75" stroke="#00e676" stroke-width="3.5" stroke-linecap="round"/>

        <!-- Conjunto da Sapata Empurradora Linear (Avança de 0 mm a 120 mm) -->
        <g id="s2_pusher_group" transform="translate(0, 0)">
          <!-- Patim Deslizante em Guia Linear -->
          <rect x="130" y="65" width="20" height="20" fill="#1f3226" stroke="#00e5ff" rx="2"/>
          <!-- Sapata Retilínea em Acrílico Laranja -->
          <rect x="150" y="40" width="14" height="70" fill="rgba(255, 145, 0, 0.45)" stroke="#ff9100" stroke-width="2" rx="3"/>
          <text x="157" y="78" font-family="var(--font-mono)" font-size="7" fill="#fff" text-anchor="middle" transform="rotate(-90 157 78)">SAPATA</text>
        </g>

        <!-- Escala de Curso Linear -->
        <g transform="translate(130, 125)">
          <line x1="0" y1="0" x2="50" y2="0" stroke="#5c7967" stroke-width="1"/>
          <line x1="0" y1="-3" x2="0" y2="3" stroke="#5c7967" stroke-width="1"/>
          <line x1="50" y1="-3" x2="50" y2="3" stroke="#5c7967" stroke-width="1"/>
          <text x="25" y="10" font-family="var(--font-mono)" font-size="8" fill="#00e676" text-anchor="middle" id="lbl_s2_stroke_text">0 mm [RECOLHIDO]</text>
        </g>
      </g>

      <!-- Oscilograma do Sinal PWM (LEDC Hardware ESP32) -->
      <g transform="translate(1055, 20)">
        <rect x="0" y="0" width="180" height="150" fill="#0a120e" stroke="#253a2f" rx="3"/>
        <text x="12" y="18" font-family="var(--font-mono)" font-size="9" fill="#00e5ff" font-weight="700">FORMA DE ONDA PWM (50 Hz)</text>
        <text x="12" y="30" font-family="var(--font-mono)" font-size="8" fill="#8fa699">Período T = 20,0 ms (50 Hz)</text>
        
        <g transform="translate(15, 45)">
          <rect x="0" y="0" width="150" height="70" fill="#060c08" stroke="#1b2a20"/>
          <line x1="0" y1="35" x2="150" y2="35" stroke="#1b2a20" stroke-dasharray="2 2"/>
          <line x1="75" y1="0" x2="75" y2="70" stroke="#1b2a20" stroke-dasharray="2 2"/>
          
          <path id="svg_pwm_pulse_wave" d="M 0 50 L 20 50 L 20 15 L 45 15 L 45 50 L 150 50" stroke="#d500f9" stroke-width="2.5" fill="none"/>
          <text x="32" y="10" font-family="var(--font-mono)" font-size="8" fill="#d500f9" text-anchor="middle" id="lbl_pwm_pulsewidth">0.8 ms (0 mm)</text>
          <text x="120" y="65" font-family="var(--font-mono)" font-size="7" fill="#8fa699">20 ms</text>
        </g>
      </g>
    </g>

    <!-- ========================================================
         SEÇÃO 3: CIRCUITO DE ILUMINAÇÃO RING LIGHT DA CÚPULA
         ======================================================== -->
    <g transform="translate(60, 680)">
      <rect x="0" y="0" width="460" height="24" fill="#14221b" stroke="#ff3344" stroke-width="1.2" rx="3"/>
      <text x="12" y="16" font-family="var(--font-mono)" font-size="11" fill="#ff3344" font-weight="700">CIRCUITO 03: ILUMINAÇÃO RING LIGHT 12V 6000K (CÚPULA)</text>
    </g>

    <g transform="translate(60, 715)">
      <!-- Linha +12V_CONT vinda da Folha 01 via Borne X1:5 -->
      <line x1="0" y1="15" x2="60" y2="15" class="wire w-12v-cont"/>
      <rect x="0" y="3" width="56" height="14" fill="#1b1212" rx="2"/>
      <text x="4" y="13" class="lbl-wire" fill="#ff3344">+12V_CONT</text>

      <!-- Fusível F5 (1A) -->
      <g transform="translate(60, 5)">
        <rect x="0" y="0" width="45" height="20" class="symbol-box"/>
        <line x1="0" y1="10" x2="45" y2="10" stroke="#ff3344" stroke-width="2"/>
        <text x="22" y="-3" font-family="var(--font-mono)" font-size="9" fill="#fff" text-anchor="middle">F5 (1A)</text>
      </g>

      <!-- Ligação entre F5 (X=105) e S_LED (X=125) -->
      <path d="M 105 15 L 125 15" class="wire w-12v-cont"/>

      <!-- Interruptor Manual S_LED -->
      <g transform="translate(125, 5)">
        <rect x="0" y="0" width="45" height="20" class="symbol-box"/>
        <line x1="5" y1="10" x2="40" y2="10" stroke="#00e676" stroke-width="2" id="s_led_switch_arm"/>
        <circle cx="5" cy="10" r="2" fill="#fff"/>
        <circle cx="40" cy="10" r="2" fill="#fff"/>
        <text x="22" y="-3" font-family="var(--font-mono)" font-size="8" fill="#00e5ff" text-anchor="middle">S_LED</text>
      </g>

      <!-- Bornes X3:7 (+12V) e X3:8 (0V) -->
      <path d="M 170 15 L 195 15" class="wire w-12v-cont"/>
      <g transform="translate(190, 5)">
        <circle cx="10" cy="10" r="4.5" class="symbol-terminal"/>
        <text x="10" y="24" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">X3:7</text>
      </g>
      <path id="wire_light_pos" d="M 205 15 L 273 15" class="wire w-12v-cont"/>

      <!-- Representação da Luminária Ring Light (Anel de LEDs 6000K) -->
      <g transform="translate(260, -10)">
        <circle cx="35" cy="25" r="22" fill="#15241c" stroke="#fff" stroke-width="2" id="ring_light_glow"/>
        <circle cx="35" cy="25" r="14" fill="#0a120e" stroke="#5c7566" stroke-width="1"/>
        <text x="35" y="28" font-family="var(--font-mono)" font-size="7" fill="#fff" text-anchor="middle">6000K</text>
        <text x="75" y="20" font-family="var(--font-mono)" font-size="9" fill="#fff" font-weight="700">RING LIGHT LED 12V</text>
        <text x="75" y="32" font-family="var(--font-sans)" font-size="8" fill="#8fa699">Iluminação Difusa da Cúpula (0,6A)</text>
      </g>

      <!-- Retorno 0V do Anel (X=295, Y=37) para Borne X3:8 (cx=200, cy=55) e Barramento 0V_COMUM -->
      <path d="M 295 37 L 295 55 L 205 55" class="wire w-gnd"/>
      <g transform="translate(190, 45)">
        <circle cx="10" cy="10" r="4.5" class="symbol-terminal"/>
        <text x="10" y="24" font-family="var(--font-mono)" font-size="8" fill="#fff" text-anchor="middle">X3:8</text>
      </g>
      <path d="M 195 55 L 0 55" class="wire w-gnd"/>
    </g>

    <!-- NOTAS TÉCNICAS DA FOLHA 02 -->
    <g transform="translate(680, 680)">
      <rect x="0" y="0" width="380" height="110" fill="#0c120f" stroke="#1f3026" stroke-width="1.2" rx="4"/>
      <text x="12" y="18" font-family="var(--font-mono)" font-size="10" fill="#00e5ff" font-weight="700">NOTAS DE POTÊNCIA E ATUAÇÃO LINEAR:</text>
      <text x="12" y="34" font-family="var(--font-sans)" font-size="9" fill="#8fa699">1. <tspan fill="#ffffff" font-weight="700">DIODO 1N5822:</tspan> É obrigatório conectar o diodo Schottky diretamente nos</text>
      <text x="24" y="46" font-family="var(--font-sans)" font-size="8" fill="#7fa890">bornes do motor para evitar destruição do módulo MOSFET por tensão reversa.</text>
      <text x="12" y="62" font-family="var(--font-sans)" font-size="9" fill="#8fa699">2. <tspan fill="#ffffff" font-weight="700">EMPURRADOR LINEAR (120 mm):</tspan> O mecanismo biela-manivela transforma o giro</text>
      <text x="24" y="74" font-family="var(--font-sans)" font-size="8" fill="#7fa890">de 90° do servo em 120 mm de avanço linear direto, ejetando a fruta ruim.</text>
      <text x="12" y="90" font-family="var(--font-sans)" font-size="9" fill="#8fa699">3. <tspan fill="#ffffff" font-weight="700">CAPACITOR C1 (1000 µF):</tspan> Evita brownout do ESP32 durante o inrush do servo.</text>
    </g>
    """
    return svg
