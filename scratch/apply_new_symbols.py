import re
import xml.dom.minidom
import sys

# Load esp32.html
with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define all 15 authentic schematic symbols
replacements = {}

# 1. E16 — Fusíveis IEC 60127
replacements['bloco-e16-pg'] = """          <g id="bloco-e16-pg">
            <!-- E16 — Módulo de Fusíveis DIN (Norma IEC 60127) -->
            <rect x="448" y="265" width="84" height="125" rx="3" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.4"/>
            <text x="490" y="278" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E16 — FUSÍVEIS</text>
            <text x="490" y="287" text-anchor="middle" font-size="4.8" fill="var(--dim)">TRILHO DIN (IEC 60127)</text>

            <!-- F1: FUSÍVEL GERAL 10A (Símbolo IEC: condutor atravessa o retângulo longitudinalmente) -->
            <line x1="450" y1="300" x2="530" y2="300" stroke="var(--line)" stroke-width="1.4"/>
            <rect x="470" y="294" width="40" height="12" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="1.4"/>
            <text x="490" y="302" text-anchor="middle" font-size="4.5" font-weight="700" fill="var(--fg)">F1 10A</text>
            <text x="490" y="311" text-anchor="middle" font-size="3.5" fill="var(--dim)">GERAL (W006→W007)</text>

            <!-- Fusíveis Derivados de Proteção Setorial (Símbolos IEC) -->
            <!-- F2: 3A Motor TT (W050) -->
            <rect x="456" y="324" width="24" height="8" rx="0.8" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <line x1="452" y1="328" x2="484" y2="328" stroke="var(--line)" stroke-width="0.8"/>
            <text x="486" y="330" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--fg)">F2: 3A MOTOR</text>
            <text x="526" y="330" text-anchor="end" font-size="4" fill="var(--dim)">(W050)</text>

            <!-- F3: 3A Servo MG996R (W011) -->
            <rect x="456" y="344" width="24" height="8" rx="0.8" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <line x1="452" y1="348" x2="484" y2="348" stroke="var(--line)" stroke-width="0.8"/>
            <text x="486" y="350" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--fg)">F3: 3A SERVO</text>
            <text x="526" y="350" text-anchor="end" font-size="4" fill="var(--dim)">(W011)</text>

            <!-- F4: 1A Lógica ESP32/Sensores (W015) -->
            <rect x="456" y="364" width="24" height="8" rx="0.8" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <line x1="452" y1="368" x2="484" y2="368" stroke="var(--line)" stroke-width="0.8"/>
            <text x="486" y="370" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--fg)">F4: 1A LÓGICA</text>
            <text x="526" y="370" text-anchor="end" font-size="4" fill="var(--dim)">(W015)</text>

            <!-- Bornes de Conexão IN e OUT do Barramento Geral -->
            <circle cx="450" cy="300" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="450" cy="300" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="456" y="294" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">IN</text>

            <circle cx="530" cy="300" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="530" cy="300" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="524" y="294" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">OUT</text>
          </g>"""

# 2. E06 — Capacitor Eletrolítico Polarizado IEC
replacements['bloco-e06-pg'] = """          <g id="bloco-e06-pg">
            <!-- E06 — Capacitor Eletrolítico de Filtragem 1000µF (Norma IEC / IEEE) -->
            <!-- Barramentos de passagem superior (+) e inferior (-) -->
            <line x1="460" y1="720" x2="510" y2="720" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="460" y1="750" x2="510" y2="750" stroke="var(--line)" stroke-width="1.4"/>
            <!-- Derivação interna para as placas do capacitor -->
            <line x1="485" y1="720" x2="485" y2="731" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="485" y1="738" x2="485" y2="750" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Placa Positiva: barra reta horizontal -->
            <line x1="474" y1="731" x2="496" y2="731" stroke="var(--line)" stroke-width="2.2" stroke-linecap="round"/>
            <!-- Placa Negativa: arco curvo horizontal (côncavo para baixo) -->
            <path d="M 474,737 Q 485,741 496,737" fill="none" stroke="var(--line)" stroke-width="2" stroke-linecap="round"/>
            <!-- Indicação de Polaridade (+) -->
            <text x="470" y="730" text-anchor="middle" font-size="7" font-weight="800" fill="var(--fg)">+</text>
            <!-- Bornes de entrada / saída com anéis CAD -->
            <circle cx="460" cy="720" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="460" cy="720" r="1.4" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <circle cx="510" cy="720" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="510" cy="720" r="1.4" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <circle cx="460" cy="750" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="460" cy="750" r="1.4" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <circle cx="510" cy="750" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="510" cy="750" r="1.4" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <!-- Rótulo e Especificação -->
            <text x="485" y="714" text-anchor="middle" font-size="6.5" font-weight="700" fill="var(--fg)">E06</text>
            <text x="502" y="736" text-anchor="start" font-size="5" font-weight="600" fill="var(--dim)">1000µF</text>
            <text x="502" y="744" text-anchor="start" font-size="4.2" fill="var(--dim)">16V</text>
          </g>"""

# 3. E12-A — E-STOP Contato NF1 Auxiliar (11-12)
replacements['bloco-e12a-pg'] = """          <g id="bloco-e12a-pg">
            <!-- E12-A — Contato NF1 (11-12) do Botão de Emergência E-STOP (Monitoramento ESP32) -->
            <rect x="680" y="605" width="85" height="70" rx="3" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="3,2"/>
            <text x="722" y="618" text-anchor="middle" font-size="6.8" font-weight="700" fill="var(--fg)">E12-A — E-STOP</text>
            <text x="722" y="627" text-anchor="middle" font-size="4.5" fill="var(--dim)">NF1 AUX (11-12)</text>

            <!-- Atuador Mecânico Tipo Cogumelo (IEC 60947-5-5) -->
            <path d="M 698,645 C 698,635 710,635 710,645 Z" fill="#ef4444" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="704" y1="645" x2="728" y2="645" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="2,2"/>

            <!-- Contato Normalmente Fechado (NF / NC) com ponte mecânica -->
            <line x1="765" y1="630" x2="738" y2="630" stroke="var(--line)" stroke-width="1.4"/>
            <circle cx="738" cy="630" r="2.2" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="765" y1="660" x2="738" y2="660" stroke="var(--line)" stroke-width="1.4"/>
            <circle cx="738" cy="660" r="2.2" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Lâmina de contato NF conectando os dois polos -->
            <line x1="734" y1="626" x2="734" y2="664" stroke="var(--line)" stroke-width="2" stroke-linecap="round"/>

            <!-- Bornes de Conexão 11:COM e 12:NC -->
            <circle cx="765" cy="630" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="765" cy="630" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="758" y="626" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">11:COM</text>

            <circle cx="765" cy="660" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="765" cy="660" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="758" y="667" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">12:NC</text>
          </g>"""

# 4. Clamp S1 — Resistor E11 1kΩ + Duplo Schottky BAT54S
replacements['bloco-clamp-s1-pg'] = """          <g id="bloco-clamp-s1-pg">
            <!-- Circuito de Proteção S1: Resistor Série E11 (1kΩ) + Diodo Duplo Schottky BAT54S (E10) -->
            <!-- Resistor E11 1kΩ (Símbolo IEC) -->
            <line x1="965" y1="350" x2="970" y2="350" stroke="var(--line)" stroke-width="1.2"/>
            <rect x="970" y="345" width="22" height="10" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <text x="981" y="352" text-anchor="middle" font-size="4.5" font-weight="700" fill="var(--fg)">1kΩ</text>
            <text x="981" y="342" text-anchor="middle" font-size="4" fill="var(--dim)">E11</text>
            <line x1="992" y1="350" x2="1041" y2="350" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Diodo Schottky Superior D1: Ânodo no sinal (1041, 350), Cátodo no +3V3 (1041, 330) -->
            <line x1="1041" y1="350" x2="1041" y2="344" stroke="var(--line)" stroke-width="1.2"/>
            <polygon points="1036,344 1046,344 1041,336" fill="var(--fg)" stroke="var(--line)" stroke-width="1"/>
            <polyline points="1035,337 1037,336 1045,336 1047,335" fill="none" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="1041" y1="336" x2="1041" y2="330" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Diodo Schottky Inferior D2: Ânodo no GND (1041, 370), Cátodo no sinal (1041, 350) -->
            <line x1="1041" y1="370" x2="1041" y2="364" stroke="var(--line)" stroke-width="1.2"/>
            <polygon points="1036,364 1046,364 1041,356" fill="var(--fg)" stroke="var(--line)" stroke-width="1"/>
            <polyline points="1035,357 1037,356 1045,356 1047,355" fill="none" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="1041" y1="356" x2="1041" y2="350" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Saída para ESP32 -->
            <line x1="1041" y1="350" x2="1052" y2="350" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Textos de Identificação -->
            <text x="1050" y="342" text-anchor="start" font-size="4.2" font-weight="700" fill="var(--fg)">BAT54S</text>
            <text x="1050" y="362" text-anchor="start" font-size="3.8" fill="var(--dim)">E10</text>
          </g>"""

# 5. Clamp S2 — Resistor E11 1kΩ + Duplo Schottky BAT54S
replacements['bloco-clamp-s2-pg'] = """          <g id="bloco-clamp-s2-pg">
            <!-- Circuito de Proteção S2: Resistor Série E11 (1kΩ) + Diodo Duplo Schottky BAT54S (E10) -->
            <!-- Resistor E11 1kΩ (Símbolo IEC) -->
            <line x1="965" y1="460" x2="970" y2="460" stroke="var(--line)" stroke-width="1.2"/>
            <rect x="970" y="455" width="22" height="10" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <text x="981" y="462" text-anchor="middle" font-size="4.5" font-weight="700" fill="var(--fg)">1kΩ</text>
            <text x="981" y="452" text-anchor="middle" font-size="4" fill="var(--dim)">E11</text>
            <line x1="992" y1="460" x2="1041" y2="460" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Diodo Schottky Superior D1: Ânodo no sinal (1041, 460), Cátodo no +3V3 (1041, 440) -->
            <line x1="1041" y1="460" x2="1041" y2="454" stroke="var(--line)" stroke-width="1.2"/>
            <polygon points="1036,454 1046,454 1041,446" fill="var(--fg)" stroke="var(--line)" stroke-width="1"/>
            <polyline points="1035,447 1037,446 1045,446 1047,445" fill="none" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="1041" y1="446" x2="1041" y2="440" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Diodo Schottky Inferior D2: Ânodo no GND (1041, 480), Cátodo no sinal (1041, 460) -->
            <line x1="1041" y1="480" x2="1041" y2="474" stroke="var(--line)" stroke-width="1.2"/>
            <polygon points="1036,474 1046,474 1041,466" fill="var(--fg)" stroke="var(--line)" stroke-width="1"/>
            <polyline points="1035,467 1037,466 1045,466 1047,465" fill="none" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="1041" y1="466" x2="1041" y2="460" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Saída para ESP32 -->
            <line x1="1041" y1="460" x2="1052" y2="460" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Textos de Identificação -->
            <text x="1050" y="452" text-anchor="start" font-size="4.2" font-weight="700" fill="var(--fg)">BAT54S</text>
            <text x="1050" y="472" text-anchor="start" font-size="3.8" fill="var(--dim)">E10</text>
          </g>"""

# 6. E12-B — E-STOP Contato NF2 Força (21-22)
replacements['bloco-e12b-pg'] = """          <g id="bloco-e12b-pg">
            <!-- E12-B — Contato NF2 (21-22) de Força do Botão de Emergência E-STOP (Corte Bobina K1) -->
            <rect x="1468" y="265" width="80" height="52" rx="3" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="3,2"/>
            <text x="1508" y="277" text-anchor="middle" font-size="6.8" font-weight="700" fill="var(--fg)">E12-B — E-STOP</text>
            <text x="1508" y="286" text-anchor="middle" font-size="4.5" fill="var(--dim)">NF2 FORÇA (21-22)</text>

            <!-- Atuador Mecânico Cogumelo Vermelho -->
            <path d="M 1500,287 C 1500,281 1514,281 1514,287 Z" fill="#ef4444" stroke="var(--line)" stroke-width="1"/>
            <line x1="1507" y1="287" x2="1507" y2="290" stroke="var(--line)" stroke-width="1" stroke-dasharray="1.5,1.5"/>

            <!-- Contato NF (Normalmente Fechado) horizontal na cota y = 290 -->
            <line x1="1470" y1="290" x2="1496" y2="290" stroke="var(--line)" stroke-width="1.4"/>
            <circle cx="1496" cy="290" r="2.2" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1545" y1="290" x2="1518" y2="290" stroke="var(--line)" stroke-width="1.4"/>
            <circle cx="1518" cy="290" r="2.2" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Barra de contato NF repousando sobre os bornes -->
            <line x1="1494" y1="288" x2="1520" y2="288" stroke="var(--line)" stroke-width="2" stroke-linecap="round"/>

            <!-- Bornes de Conexão 21 e 22 -->
            <circle cx="1470" cy="290" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1470" cy="290" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1477" y="284" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">21</text>

            <circle cx="1545" cy="290" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1545" cy="290" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1538" y="284" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">22</text>
          </g>"""

# 7. E08 — Relé de Segurança K1 com Bobina IEC e Contato NA 30-87
replacements['bloco-e08-pg'] = """          <g id="bloco-e08-pg">
            <!-- E08 — Relé de Segurança K1 (Automotivo 12V 40A / NR-12) -->
            <rect x="1600" y="265" width="95" height="135" rx="3" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.4"/>
            <text x="1647" y="279" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E08 — RELÉ K1</text>
            <text x="1647" y="290" text-anchor="middle" font-size="4.8" fill="var(--dim)">12V 40A (NR-12)</text>

            <!-- Símbolo IEC da Bobina (Pinos 85 e 86) -->
            <line x1="1600" y1="290" x2="1628" y2="290" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1628" y1="290" x2="1628" y2="305" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Retângulo da Bobina IEC com barra transversal -->
            <rect x="1620" y="305" width="16" height="28" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1620" y1="305" x2="1636" y2="333" stroke="var(--line)" stroke-width="0.8"/>
            <line x1="1628" y1="333" x2="1628" y2="345" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1628" y1="345" x2="1645" y2="345" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1645" y1="345" x2="1645" y2="400" stroke="var(--line)" stroke-width="1.2"/>

            <!-- Acoplamento Mecânico Tracejado -->
            <line x1="1636" y1="319" x2="1662" y2="319" stroke="var(--line)" stroke-width="1" stroke-dasharray="2,2"/>
            <line x1="1662" y1="319" x2="1662" y2="365" stroke="var(--line)" stroke-width="1" stroke-dasharray="2,2"/>

            <!-- Símbolo do Contato de Potência NA / NO (Pinos 30 e 87) -->
            <line x1="1600" y1="375" x2="1652" y2="375" stroke="var(--line)" stroke-width="1.4"/>
            <circle cx="1652" cy="375" r="2.2" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Lâmina móvel NA em repouso aberta -->
            <line x1="1652" y1="375" x2="1672" y2="363" stroke="var(--line)" stroke-width="2" stroke-linecap="round"/>
            <circle cx="1676" cy="375" r="2.2" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1676" y1="375" x2="1695" y2="375" stroke="var(--line)" stroke-width="1.4"/>

            <!-- Bornes de Conexão: 85, 86, 30, 87 -->
            <circle cx="1600" cy="290" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1600" cy="290" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1607" y="286" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">85</text>

            <circle cx="1645" cy="400" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1645" cy="400" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1645" y="393" text-anchor="middle" font-size="5" font-weight="700" fill="var(--pin-text)">86</text>

            <circle cx="1600" cy="375" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1600" cy="375" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1607" y="371" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">30</text>

            <circle cx="1695" cy="375" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1695" cy="375" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1688" y="371" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">87</text>
          </g>"""

# 8. E09 — Diodo Flyback Relé (1N4007)
replacements['bloco-e09-pg'] = """          <g id="bloco-e09-pg">
            <!-- Diodo Flyback Retificador E09 (1N4007) -->
            <!-- Terminais de conexão verticais -->
            <line x1="1730" y1="345" x2="1730" y2="328" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="1730" y1="312" x2="1730" y2="295" stroke="var(--line)" stroke-width="1.4"/>
            <!-- Triângulo do Diodo (aponta p/ cima: A -> K) -->
            <polygon points="1722,328 1738,328 1730,312" fill="var(--fg)" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Barra de Cátodo linear retificadora -->
            <line x1="1720" y1="312" x2="1740" y2="312" stroke="var(--line)" stroke-width="1.8" stroke-linecap="round"/>
            <!-- Pontos de conexão -->
            <circle cx="1730" cy="295" r="2.5" fill="var(--line)"/>
            <circle cx="1730" cy="345" r="2.5" fill="var(--line)"/>
            <!-- Textos e Identificação -->
            <text x="1744" y="316" text-anchor="start" font-size="6" font-weight="700" fill="var(--fg)">E09</text>
            <text x="1744" y="326" text-anchor="start" font-size="4.8" fill="var(--dim)">1N4007</text>
            <text x="1725" y="304" text-anchor="end" font-size="4.2" font-weight="700" fill="var(--pin-text)">K (faixa)</text>
            <text x="1725" y="342" text-anchor="end" font-size="4.2" font-weight="700" fill="var(--pin-text)">A</text>
          </g>"""

# 9. Q2 — Transistor Driver NPN BC337-40 para Relé K1
replacements['bloco-q2-pg'] = """          <g id="bloco-q2-pg">
            <!-- Transistor Driver Q2 (NPN BC337-40) para Relé K1 -->
            <rect x="1575" y="440" width="105" height="70" rx="3" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="3,2"/>
            <text x="1628" y="451" text-anchor="middle" font-size="5.5" font-weight="700" fill="var(--fg)">Q2 — BC337-40 (NPN)</text>

            <!-- Resistor de Base R_B2 (470Ω) -->
            <line x1="1585" y1="475" x2="1595" y2="475" stroke="var(--line)" stroke-width="1.2"/>
            <rect x="1595" y="471" width="16" height="8" rx="0.8" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <text x="1603" y="477" text-anchor="middle" font-size="3.8" font-weight="600" fill="var(--dim)">470Ω</text>
            <line x1="1611" y1="475" x2="1624" y2="475" stroke="var(--line)" stroke-width="1.2"/>

            <!-- Resistor Pull-Down R_PD2 (10kΩ) da base ao GND -->
            <line x1="1618" y1="475" x2="1618" y2="492" stroke="var(--line)" stroke-width="1"/>
            <rect x="1614" y="492" width="8" height="10" rx="0.6" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <text x="1618" y="499" text-anchor="middle" font-size="3" fill="var(--dim)">10k</text>
            <line x1="1618" y1="502" x2="1618" y2="505" stroke="var(--line)" stroke-width="1"/>
            <line x1="1618" y1="505" x2="1645" y2="505" stroke="var(--line)" stroke-width="1"/>

            <!-- Símbolo Transistor NPN (Círculo + Barra Base + Coletor + Emissor com flecha) -->
            <circle cx="1636" cy="475" r="14" fill="none" stroke="var(--line)" stroke-width="1"/>
            <!-- Barra de Base vertical -->
            <line x1="1626" y1="466" x2="1626" y2="484" stroke="var(--line)" stroke-width="2" stroke-linecap="round"/>
            <!-- Ligação Base interna -->
            <line x1="1624" y1="475" x2="1626" y2="475" stroke="var(--line)" stroke-width="1.4"/>
            <!-- Terminal Coletor: parte da base (1626, 469) diagonal até (1645, 460) e sobe até (1645, 445) -->
            <line x1="1626" y1="469" x2="1645" y2="460" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="1645" y1="460" x2="1645" y2="445" stroke="var(--line)" stroke-width="1.4"/>
            <!-- Terminal Emissor: parte da base (1626, 481) diagonal até (1645, 490) com SETA NPN e desce até (1645, 505) -->
            <line x1="1626" y1="481" x2="1645" y2="490" stroke="var(--line)" stroke-width="1.4"/>
            <polygon points="1645,490 1637,485 1639,489" fill="var(--fg)"/>
            <line x1="1645" y1="490" x2="1645" y2="505" stroke="var(--line)" stroke-width="1.4"/>

            <!-- Bornes de Conexão C, B, E -->
            <circle cx="1645" cy="445" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <text x="1651" y="448" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--pin-text)">C</text>
            <circle cx="1585" cy="475" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <text x="1581" y="472" text-anchor="end" font-size="4.5" font-weight="700" fill="var(--pin-text)">B</text>
            <circle cx="1645" cy="505" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <text x="1651" y="508" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--pin-text)">E</text>
          </g>"""

# 10. E04 — Módulo Driver MOSFET Canal N com Esquemático Interno
replacements['bloco-e04-pg'] = """          <g id="bloco-e04-pg">
            <!-- E04 — Módulo Driver MOSFET de Potência D4184 -->
            <rect x="1830" y="485" width="120" height="175" rx="3" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.4"/>
            <text x="1890" y="499" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E04 — MOSFET D4184</text>
            <text x="1890" y="509" text-anchor="middle" font-size="4.8" fill="var(--dim)">DRIVER N-CH PWM / ON-OFF</text>

            <!-- Barramento Positivo Direto (Pass-Through: VIN+ -> VOUT+) -->
            <line x1="1830" y1="520" x2="1950" y2="520" stroke="var(--line)" stroke-width="1.6"/>
            <text x="1890" y="516" text-anchor="middle" font-size="4" font-weight="700" fill="var(--fg)">BARRAMENTO +6V DIRETO</text>

            <!-- Símbolo Esquemático Interno do MOSFET Canal N (D4184) -->
            <!-- Linha de Gate (Pino SIG 1830, 640 -> Gate) -->
            <line x1="1830" y1="640" x2="1868" y2="640" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1868" y1="640" x2="1868" y2="585" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1868" y1="585" x2="1878" y2="585" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Placa de Gate isolada -->
            <line x1="1878" y1="573" x2="1878" y2="597" stroke="var(--line)" stroke-width="1.8" stroke-linecap="round"/>

            <!-- Canal N: 3 segmentos (Dreno, Substrato com seta, Fonte) -->
            <line x1="1884" y1="571" x2="1884" y2="577" stroke="var(--line)" stroke-width="2"/>
            <line x1="1884" y1="582" x2="1884" y2="588" stroke="var(--line)" stroke-width="2"/>
            <line x1="1884" y1="593" x2="1884" y2="599" stroke="var(--line)" stroke-width="2"/>

            <!-- Terminal de Dreno (D): sai de (1884, 574) até VOUT- (1950, 580) -->
            <line x1="1884" y1="574" x2="1904" y2="574" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="1904" y1="574" x2="1904" y2="580" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="1904" y1="580" x2="1950" y2="580" stroke="var(--line)" stroke-width="1.4"/>
            <text x="1898" y="570" text-anchor="middle" font-size="4.2" font-weight="700" fill="var(--fg)">D</text>

            <!-- Terminal de Substrato e Fonte (S): de (1884, 585) e (1884, 596) -->
            <!-- Seta do Canal N (aponta para dentro em direção ao canal) -->
            <line x1="1884" y1="585" x2="1904" y2="585" stroke="var(--line)" stroke-width="1.2"/>
            <polygon points="1884,585 1892,582 1892,588" fill="var(--fg)"/>
            <line x1="1884" y1="596" x2="1904" y2="596" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="1904" y1="585" x2="1904" y2="605" stroke="var(--line)" stroke-width="1.4"/>
            <text x="1898" y="605" text-anchor="middle" font-size="4.2" font-weight="700" fill="var(--fg)">S</text>

            <!-- Conexão Fonte ao VIN- (1830, 550) e GND (1830, 610) -->
            <line x1="1904" y1="605" x2="1855" y2="605" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1855" y1="550" x2="1855" y2="610" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1855" y1="550" x2="1830" y2="550" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1855" y1="610" x2="1830" y2="610" stroke="var(--line)" stroke-width="1.2"/>

            <!-- Terminal VCC (1830, 580) - Pull-up / optoacoplador interno -->
            <line x1="1830" y1="580" x2="1848" y2="580" stroke="var(--line)" stroke-width="1.2"/>
            <rect x="1848" y="575" width="10" height="10" rx="0.5" fill="var(--bg)" stroke="var(--line)" stroke-width="0.8"/>
            <text x="1853" y="582" text-anchor="middle" font-size="3" fill="var(--dim)">OPTO</text>

            <!-- Diodo de Corpo Interno do MOSFET (Body Diode entre D e S) -->
            <line x1="1916" y1="574" x2="1916" y2="596" stroke="var(--line)" stroke-width="0.8"/>
            <polygon points="1912,590 1920,590 1916,580" fill="none" stroke="var(--line)" stroke-width="0.8"/>
            <line x1="1912" y1="580" x2="1920" y2="580" stroke="var(--line)" stroke-width="1"/>

            <!-- Círculo envolvente do encapsulamento do transistor -->
            <circle cx="1895" cy="585" r="22" fill="none" stroke="var(--line)" stroke-width="0.8" stroke-dasharray="2,2"/>

            <!-- Bornes de Conexão com anéis CAD -->
            <circle cx="1830" cy="520" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1830" cy="520" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1837" y="522" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">VIN+</text>

            <circle cx="1830" cy="550" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1830" cy="550" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1837" y="552" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">VIN-</text>

            <circle cx="1830" cy="580" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1830" cy="580" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1837" y="582" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">VCC</text>

            <circle cx="1830" cy="610" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1830" cy="610" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1837" y="612" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">GND</text>

            <circle cx="1830" cy="640" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1830" cy="640" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1837" y="642" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">SIG</text>

            <circle cx="1950" cy="520" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1950" cy="520" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1943" y="522" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">VOUT+</text>

            <circle cx="1950" cy="580" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1950" cy="580" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1943" y="582" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">VOUT-</text>
          </g>"""

# 11. M13 — Motor TT DC 3-6V IEC
replacements['bloco-m13-pg'] = """          <g id="bloco-m13-pg">
            <!-- M13 — Motor TT DC com Redução -->
            <!-- Fundo circular suave -->
            <circle cx="2055" cy="550" r="32" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.6"/>
            <!-- Letra M central e símbolo DC '=' -->
            <text x="2055" y="551" text-anchor="middle" font-size="18" font-weight="800" font-family="sans-serif" fill="var(--fg)">M</text>
            <text x="2055" y="565" text-anchor="middle" font-size="8.5" font-weight="700" font-family="monospace" fill="var(--dim)">= DC</text>
            <!-- Escovas de contato do rotor (Brushes) -->
            <rect x="2020" y="516" width="6" height="8" rx="1" fill="var(--fg)" stroke="var(--line)" stroke-width="0.8"/>
            <rect x="2020" y="576" width="6" height="8" rx="1" fill="var(--fg)" stroke="var(--line)" stroke-width="0.8"/>
            <!-- Linhas de derivação até os bornes externos -->
            <line x1="2015" y1="520" x2="2020" y2="520" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="2015" y1="580" x2="2020" y2="580" stroke="var(--line)" stroke-width="1.4"/>
            <!-- Bornes de conexão M+ e M- -->
            <circle cx="2015" cy="520" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="2015" cy="520" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="2008" y="517" text-anchor="end" font-size="5.5" font-weight="700" fill="var(--pin-text)">M+</text>
            <circle cx="2015" cy="580" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="2015" cy="580" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="2008" y="585" text-anchor="end" font-size="5.5" font-weight="700" fill="var(--pin-text)">M-</text>
            <!-- Títulos e Especificações Industriais -->
            <text x="2055" y="508" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">M13 — MOTOR TT</text>
            <text x="2055" y="595" text-anchor="middle" font-size="5" font-weight="600" fill="var(--dim)">DC 3–6V (AMARELO)</text>
            <text x="2055" y="605" text-anchor="middle" font-size="4.5" fill="var(--dim)">REDUÇÃO 1:48 @ 6V</text>
          </g>"""

# 12. E05 — Diodo Flyback Schottky 1N5822 para Motor TT
replacements['bloco-e05-pg'] = """          <g id="bloco-e05-pg">
            <!-- Diodo Flyback Schottky E05 (1N5822) -->
            <!-- Terminais de conexão -->
            <line x1="1995" y1="670" x2="1986" y2="670" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="1974" y1="670" x2="1965" y2="670" stroke="var(--line)" stroke-width="1.4"/>
            <!-- Triângulo do Diodo (aponta p/ esquerda: A -> K) -->
            <polygon points="1986,662 1986,678 1974,670" fill="var(--fg)" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Barra de Cátodo tipo Schottky (com abas características) -->
            <polyline points="1971,664 1974,662 1974,678 1977,676" fill="none" stroke="var(--line)" stroke-width="1.6" stroke-linecap="square"/>
            <!-- Pontos de borne / conexão -->
            <circle cx="1965" cy="670" r="2.5" fill="var(--line)"/>
            <circle cx="1995" cy="670" r="2.5" fill="var(--line)"/>
            <!-- Textos e Identificação -->
            <text x="1980" y="655" text-anchor="middle" font-size="6" font-weight="700" fill="var(--fg)">E05</text>
            <text x="1980" y="688" text-anchor="middle" font-size="4.8" font-weight="700" fill="var(--dim)">1N5822</text>
            <text x="1963" y="663" text-anchor="end" font-size="4.5" font-weight="700" fill="var(--pin-text)">K</text>
            <text x="1997" y="663" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--pin-text)">A</text>
          </g>"""

# 13. H05 — Painel de LEDs com Resistores e Símbolos Oficiais
replacements['bloco-h05-pg'] = """          <g id="bloco-h05-pg">
            <!-- Painel H05 — Indicadores Luminosos LED com Resistores -->
            <!-- Moldura de delimitação do conjunto H05 -->
            <rect x="2120" y="248" width="138" height="118" rx="3" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="4,3"/>
            <text x="2189" y="259" text-anchor="middle" font-size="6" font-weight="700" fill="var(--fg)">H05 — PAINEL DE LEDS</text>

            <!-- CANAL 1: LED VERMELHO (y = 270) -->
            <circle cx="2130" cy="270" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <text x="2126" y="267" text-anchor="end" font-size="4.5" font-weight="700" fill="var(--pin-text)">R+</text>
            <!-- Resistor 330Ω IEC -->
            <line x1="2130" y1="270" x2="2142" y2="270" stroke="var(--line)" stroke-width="1.2"/>
            <rect x="2142" y="266" width="18" height="8" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <text x="2151" y="272" text-anchor="middle" font-size="4" font-weight="600" fill="var(--dim)">330Ω</text>
            <line x1="2160" y1="270" x2="2172" y2="270" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Símbolo LED Vermelho -->
            <polygon points="2172,263 2172,277 2184,270" fill="#ef4444" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="2184" y1="263" x2="2184" y2="277" stroke="var(--line)" stroke-width="1.6"/>
            <!-- Setas de Emissão Luminosa -->
            <line x1="2179" y1="262" x2="2185" y2="256" stroke="var(--line)" stroke-width="1"/>
            <polygon points="2185,256 2182,258 2186,259" fill="var(--line)"/>
            <line x1="2183" y1="264" x2="2189" y2="258" stroke="var(--line)" stroke-width="1"/>
            <polygon points="2189,258 2186,260 2190,261" fill="var(--line)"/>
            <!-- Saída até borne R- -->
            <line x1="2184" y1="270" x2="2250" y2="270" stroke="var(--line)" stroke-width="1.2"/>
            <circle cx="2250" cy="270" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <text x="2255" y="267" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--pin-text)">R-</text>
            <text x="2195" y="272" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--fg)">VERM (FALHA)</text>

            <!-- CANAL 2: LED VERDE (y = 310) -->
            <circle cx="2130" cy="310" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <text x="2126" y="307" text-anchor="end" font-size="4.5" font-weight="700" fill="var(--pin-text)">G+</text>
            <!-- Resistor 330Ω IEC -->
            <line x1="2130" y1="310" x2="2142" y2="310" stroke="var(--line)" stroke-width="1.2"/>
            <rect x="2142" y="306" width="18" height="8" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <text x="2151" y="312" text-anchor="middle" font-size="4" font-weight="600" fill="var(--dim)">330Ω</text>
            <line x1="2160" y1="310" x2="2172" y2="310" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Símbolo LED Verde -->
            <polygon points="2172,303 2172,317 2184,310" fill="#22c55e" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="2184" y1="303" x2="2184" y2="317" stroke="var(--line)" stroke-width="1.6"/>
            <!-- Setas de Emissão Luminosa -->
            <line x1="2179" y1="302" x2="2185" y2="296" stroke="var(--line)" stroke-width="1"/>
            <polygon points="2185,296 2182,298 2186,299" fill="var(--line)"/>
            <line x1="2183" y1="304" x2="2189" y2="298" stroke="var(--line)" stroke-width="1"/>
            <polygon points="2189,298 2186,300 2190,301" fill="var(--line)"/>
            <!-- Saída até borne G- -->
            <line x1="2184" y1="310" x2="2250" y2="310" stroke="var(--line)" stroke-width="1.2"/>
            <circle cx="2250" cy="310" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <text x="2255" y="307" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--pin-text)">G-</text>
            <text x="2195" y="312" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--fg)">VERD (RUN)</text>

            <!-- CANAL 3: LED AMARELO (y = 350) -->
            <circle cx="2130" cy="350" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <text x="2126" y="347" text-anchor="end" font-size="4.5" font-weight="700" fill="var(--pin-text)">Y+</text>
            <!-- Resistor 330Ω IEC -->
            <line x1="2130" y1="350" x2="2142" y2="350" stroke="var(--line)" stroke-width="1.2"/>
            <rect x="2142" y="346" width="18" height="8" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <text x="2151" y="352" text-anchor="middle" font-size="4" font-weight="600" fill="var(--dim)">330Ω</text>
            <line x1="2160" y1="350" x2="2172" y2="350" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Símbolo LED Amarelo -->
            <polygon points="2172,343 2172,357 2184,350" fill="#eab308" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="2184" y1="343" x2="2184" y2="357" stroke="var(--line)" stroke-width="1.6"/>
            <!-- Setas de Emissão Luminosa -->
            <line x1="2179" y1="342" x2="2185" y2="336" stroke="var(--line)" stroke-width="1"/>
            <polygon points="2185,336 2182,338 2186,339" fill="var(--line)"/>
            <line x1="2183" y1="344" x2="2189" y2="338" stroke="var(--line)" stroke-width="1"/>
            <polygon points="2189,338 2186,340 2190,341" fill="var(--line)"/>
            <!-- Saída até borne Y- -->
            <line x1="2184" y1="350" x2="2250" y2="350" stroke="var(--line)" stroke-width="1.2"/>
            <circle cx="2250" cy="350" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <text x="2255" y="347" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--pin-text)">Y-</text>
            <text x="2195" y="352" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--fg)">AMAR (REJEIÇÃO)</text>
          </g>"""

# 14. E25 — Avisador Sonoro Piezoelétrico (Buzzer 5V)
replacements['bloco-e25-pg'] = """          <g id="bloco-e25-pg">
            <!-- E25 — Avisador Sonoro Piezoelétrico (Buzzer 5V) -->
            <rect x="2120" y="448" width="80" height="68" rx="3" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="3,2"/>
            <text x="2160" y="460" text-anchor="middle" font-size="6.8" font-weight="700" fill="var(--fg)">E25 — BUZZER</text>
            <text x="2160" y="469" text-anchor="middle" font-size="4.5" fill="var(--dim)">PIEZO 5V (NR-12)</text>

            <!-- Símbolo Acústico IEC do Buzzer -->
            <!-- Corpo acústico do avisador -->
            <path d="M 2150,476 L 2162,476 L 2170,470 L 2170,496 L 2162,490 L 2150,490 Z" fill="var(--bg)" stroke="var(--line)" stroke-width="1.4"/>
            <!-- Ondas sonoras emitidas -->
            <path d="M 2174,475 Q 2178,483 2174,491" fill="none" stroke="var(--line)" stroke-width="1.2" stroke-linecap="round"/>
            <path d="M 2178,471 Q 2184,483 2178,495" fill="none" stroke="var(--line)" stroke-width="1.2" stroke-linecap="round"/>

            <!-- Linhas de alimentação até os bornes -->
            <line x1="2130" y1="480" x2="2150" y2="480" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="2160" y1="490" x2="2160" y2="510" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="2160" y1="510" x2="2190" y2="510" stroke="var(--line)" stroke-width="1.2"/>

            <!-- Bornes de Conexão +5V e - -->
            <circle cx="2130" cy="480" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="2130" cy="480" r="1.4" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="2136" y="476" text-anchor="start" font-size="4.8" font-weight="700" fill="var(--pin-text)">+5V</text>

            <circle cx="2190" cy="510" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="2190" cy="510" r="1.4" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="2190" y="503" text-anchor="middle" font-size="5" font-weight="700" fill="var(--pin-text)">-</text>
          </g>"""

# 15. Q1 — Transistor Driver NPN BC337-40 para Buzzer E25
replacements['bloco-q1-pg'] = """          <g id="bloco-q1-pg">
            <!-- Transistor Driver Q1 (NPN BC337-40) para Buzzer E25 -->
            <rect x="2120" y="550" width="105" height="70" rx="3" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="3,2"/>
            <text x="2173" y="561" text-anchor="middle" font-size="5.5" font-weight="700" fill="var(--fg)">Q1 — BC337-40 (NPN)</text>

            <!-- Resistor de Base E11 (1kΩ) -->
            <line x1="2130" y1="585" x2="2140" y2="585" stroke="var(--line)" stroke-width="1.2"/>
            <rect x="2140" y="581" width="16" height="8" rx="0.8" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <text x="2148" y="587" text-anchor="middle" font-size="3.8" font-weight="600" fill="var(--dim)">1kΩ</text>
            <line x1="2156" y1="585" x2="2169" y2="585" stroke="var(--line)" stroke-width="1.2"/>

            <!-- Resistor Pull-Down R_PD1 (10kΩ) da base ao GND -->
            <line x1="2163" y1="585" x2="2163" y2="602" stroke="var(--line)" stroke-width="1"/>
            <rect x="2159" y="602" width="8" height="10" rx="0.6" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <text x="2163" y="609" text-anchor="middle" font-size="3" fill="var(--dim)">10k</text>
            <line x1="2163" y1="612" x2="2163" y2="615" stroke="var(--line)" stroke-width="1"/>
            <line x1="2163" y1="615" x2="2190" y2="615" stroke="var(--line)" stroke-width="1"/>

            <!-- Símbolo Transistor NPN (Círculo + Barra Base + Coletor + Emissor com flecha) -->
            <circle cx="2181" cy="585" r="14" fill="none" stroke="var(--line)" stroke-width="1"/>
            <!-- Barra de Base vertical -->
            <line x1="2171" y1="576" x2="2171" y2="594" stroke="var(--line)" stroke-width="2" stroke-linecap="round"/>
            <!-- Ligação Base interna -->
            <line x1="2169" y1="585" x2="2171" y2="585" stroke="var(--line)" stroke-width="1.4"/>
            <!-- Terminal Coletor: parte da base (2171, 579) diagonal até (2190, 570) e sobe até (2190, 555) -->
            <line x1="2171" y1="579" x2="2190" y2="570" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="2190" y1="570" x2="2190" y2="555" stroke="var(--line)" stroke-width="1.4"/>
            <!-- Terminal Emissor: parte da base (2171, 591) diagonal até (2190, 600) com SETA NPN e desce até (2190, 615) -->
            <line x1="2171" y1="591" x2="2190" y2="600" stroke="var(--line)" stroke-width="1.4"/>
            <polygon points="2190,600 2182,595 2184,599" fill="var(--fg)"/>
            <line x1="2190" y1="600" x2="2190" y2="615" stroke="var(--line)" stroke-width="1.4"/>

            <!-- Bornes de Conexão C, B, E -->
            <circle cx="2190" cy="555" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <text x="2196" y="558" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--pin-text)">C</text>
            <circle cx="2130" cy="585" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <text x="2126" y="582" text-anchor="end" font-size="4.5" font-weight="700" fill="var(--pin-text)">B</text>
            <circle cx="2190" cy="615" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <text x="2196" y="618" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--pin-text)">E</text>
          </g>"""

# Also update Revision block note in Aba 3 title block:
# Mention REV. E (09/11/2026): Simbologia esquemática IEC 60617 / IEEE 315 aplicada aos componentes discretos
old_rev = 'REV. D (09/11/2026): M13 GA37 12V → Motor TT amarelo 3–6V. W050 sai do rail +6V_SV (E02, pós-K1): o E-STOP continua cortando o motor. E03 = LM2596. NUNCA ligar o motor TT em 12V.'
new_rev = 'REV. E (09/11/2026): Simbologia esquemática IEC 60617/IEEE 315 completa (diodos flyback Schottky/retificadores, LEDs com emissão luminosa, fusíveis IEC 60127, transistores NPN, relé com bobina/contato, botão E-STOP cogumelo, buzzer e motor DC com escovas).'

# Perform block replacements
new_content = content
for block_id, new_block_svg in replacements.items():
    pattern = rf'[ \t]*<g id="{block_id}">[\s\S]*?</g>'
    match = re.search(pattern, new_content)
    if not match:
        print(f"ERROR: Could not find block {block_id}")
        sys.exit(1)
    new_content = new_content[:match.start()] + new_block_svg + new_content[match.end():]
    print(f"Replaced: {block_id}")

if old_rev in new_content:
    new_content = new_content.replace(old_rev, new_rev)
    print("Updated Revision text to REV. E!")
else:
    print("Warning: old_rev text not found for exact replacement")

# Validate the new Planta Geral SVG section using minidom
planta_start = new_content.find('<svg id="planta-geral"')
if planta_start == -1:
    planta_start = new_content.find('id="planta-geral"')
    # find '<svg' backwards
    planta_start = new_content.rfind('<svg', 0, planta_start)

planta_end = new_content.find('</svg>', planta_start) + len('</svg>')
planta_svg = new_content[planta_start:planta_end]

try:
    xml.dom.minidom.parseString(planta_svg)
    print("Planta Geral SVG parsed successfully with xml.dom.minidom! 100% Valid XML.")
except Exception as e:
    print(f"XML Validation Error in Planta Geral: {e}")
    sys.exit(1)

# Write out the updated file
with open(r'desenho-eletrico\esp32.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("SUCCESS: esp32.html successfully updated with authentic electronic schematic symbology!")
