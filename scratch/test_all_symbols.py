# Test and validate all schematic symbols for Aba 3 (Planta Geral)
import xml.dom.minidom

symbols = {}

# -------------------------------------------------------------------------
# 1. E05 — Diodo Flyback Motor TT (1N5822 Schottky)
# Connects W057 (+6V / VOUT+) at (1965, 670) and W058 (Drain / VOUT-) at (1995, 670)
# Schottky Diode pointing LEFT (Anode at right 1995, Cathode at left 1965)
# -------------------------------------------------------------------------
symbols['bloco-e05-pg'] = """          <g id="bloco-e05-pg">
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

# -------------------------------------------------------------------------
# 2. E09 — Diodo Flyback Bobina do Relé K1 (1N4007)
# Connects W073 (+12V / pino 85) at (1730, 295) and W074 (Q2 Coletor / pino 86) at (1730, 345)
# Rectifier Diode pointing UP (Anode at bottom 345, Cathode at top 295)
# -------------------------------------------------------------------------
symbols['bloco-e09-pg'] = """          <g id="bloco-e09-pg">
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

# -------------------------------------------------------------------------
# 3. M13 — Motor TT DC (3–6V)
# Terminais M+ em (2015, 520) e M- em (2015, 580)
# Símbolo oficial IEC / IEEE de Máquina DC (círculo com 'M' e '=')
# -------------------------------------------------------------------------
symbols['bloco-m13-pg'] = """          <g id="bloco-m13-pg">
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

# -------------------------------------------------------------------------
# 4. E06 — Capacitor Eletrolítico 1000µF / 16V
# Terminais: + em (460, 720) e (510, 720); - em (460, 750) e (510, 750)
# Símbolo oficial IEC / IEEE de capacitor eletrolítico polarizado
# -------------------------------------------------------------------------
symbols['bloco-e06-pg'] = """          <g id="bloco-e06-pg">
            <!-- E06 — Capacitor Eletrolítico de Filtragem 1000µF -->
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
            <!-- Bornes de entrada / saída -->
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

# -------------------------------------------------------------------------
# 5. H05 — Painel de LEDs Indicadores (Vermelho, Verde, Amarelo)
# Terminais de entrada em (2130, 270), (2130, 310), (2130, 350)
# Terminais de saída (retorno GND W060, W062, W064) em (2250, 270), (2250, 310), (2250, 350)
# Cada canal: Resistor limitador IEC (330Ω) em série com Símbolo de LED oficial (triângulo + barra de cátodo + 2 flechas de emissão luminosa)
# -------------------------------------------------------------------------
symbols['bloco-h05-pg'] = """          <g id="bloco-h05-pg">
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
            <line x1="2179" y1="262" x2="2185" y2="256" stroke="var(--line)" stroke-width="1" marker-end="none"/>
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

# -------------------------------------------------------------------------
# 6. E16 — Porta-Fusíveis DIN com Símbolos Oficiais IEC 60127
# Terminais: IN em (450, 300), OUT em (530, 300)
# Desenho técnico: Símbolo oficial IEC (retângulo atravessado pelo condutor central)
# Mostrando F1 10A Geral em série no W006->W007 + matriz de distribuição F2/F3/F4
# -------------------------------------------------------------------------
symbols['bloco-e16-pg'] = """          <g id="bloco-e16-pg">
            <!-- E16 — Módulo de Fusíveis DIN (Norma IEC 60127) -->
            <rect x="448" y="265" width="84" height="125" rx="3" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.4"/>
            <text x="490" y="278" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E16 — FUSÍVEIS</text>
            <text x="490" y="287" text-anchor="middle" font-size="4.8" fill="var(--dim)">TRILHO DIN (IEC 60127)</text>

            <!-- F1: FUSÍVEL GERAL 10A (Símbolo IEC: condutor atravessa o retângulo) -->
            <line x1="450" y1="305" x2="530" y2="305" stroke="var(--line)" stroke-width="1.4"/>
            <rect x="470" y="299" width="40" height="12" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="1.4"/>
            <text x="490" y="303" text-anchor="middle" font-size="4.2" font-weight="700" fill="var(--fg)">F1 10A</text>
            <text x="490" y="309" text-anchor="middle" font-size="3.5" fill="var(--dim)">GERAL</text>

            <!-- Fusíveis Derivados de Proteção Setorial (Símbolos IEC) -->
            <!-- F2: 3A Motor TT (W050) -->
            <rect x="460" y="322" width="26" height="8" rx="0.8" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <line x1="456" y1="326" x2="490" y2="326" stroke="var(--line)" stroke-width="0.8"/>
            <text x="494" y="328" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--fg)">F2: 3A MOTOR</text>
            <text x="526" y="328" text-anchor="end" font-size="4" fill="var(--dim)">(W050)</text>

            <!-- F3: 3A Servo MG996R (W011) -->
            <rect x="460" y="342" width="26" height="8" rx="0.8" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <line x1="456" y1="346" x2="490" y2="346" stroke="var(--line)" stroke-width="0.8"/>
            <text x="494" y="348" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--fg)">F3: 3A SERVO</text>
            <text x="526" y="348" text-anchor="end" font-size="4" fill="var(--dim)">(W011)</text>

            <!-- F4: 1A Lógica ESP32/Sensores (W015) -->
            <rect x="460" y="362" width="26" height="8" rx="0.8" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <line x1="456" y1="366" x2="490" y2="366" stroke="var(--line)" stroke-width="0.8"/>
            <text x="494" y="368" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--fg)">F4: 1A LÓGICA</text>
            <text x="526" y="368" text-anchor="end" font-size="4" fill="var(--dim)">(W015)</text>

            <!-- Bornes de Conexão IN e OUT do Barramento Geral -->
            <circle cx="450" cy="305" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="450" cy="305" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="456" y="299" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">IN</text>

            <circle cx="530" cy="305" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="530" cy="305" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="524" y="299" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">OUT</text>
          </g>"""

# -------------------------------------------------------------------------
# 7. Q1 & Q2 — Transistores BJT NPN (BC337-40 / 2N2222A)
# Q2 comanda Relé K1: Coletor em (1645, 445), Base em (1585, 475), Emissor em (1645, 505)
# Símbolo oficial IEEE / IEC: Barra de Base + Coletor + Emissor com Seta NPN
# -------------------------------------------------------------------------
symbols['bloco-q2-pg'] = """          <g id="bloco-q2-pg">
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

# Q1 comanda Buzzer E25: Coletor em (2190, 555), Base em (2130, 585), Emissor em (2190, 615)
symbols['bloco-q1-pg'] = """          <g id="bloco-q1-pg">
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

# -------------------------------------------------------------------------
# 8. Clamps de Proteção Schottky S1 e S2 (E11 1kΩ + E10 BAT54S duplo)
# S1: Linha de sinal em y = 350, Resistor x=965..997, BAT54S nó x=1041, topo 3V3 em (1041, 330), base GND em (1041, 370), saída ESP32 em (1052, 350)
# S2: Linha de sinal em y = 460, Resistor x=965..997, BAT54S nó x=1041, topo 3V3 em (1041, 440), base GND em (1041, 480), saída ESP32 em (1052, 460)
# -------------------------------------------------------------------------
symbols['bloco-clamp-s1-pg'] = """          <g id="bloco-clamp-s1-pg">
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

symbols['bloco-clamp-s2-pg'] = """          <g id="bloco-clamp-s2-pg">
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

# -------------------------------------------------------------------------
# 9. E12-A & E12-B — Botão de Emergência E-STOP Cogumelo (Norma NR-12 / IEC 60947-5-5)
# E12-A: NF1 Auxiliar (11-12) em (765, 630) e (765, 660)
# E12-B: NF2 Potência (21-22) em (1470, 290) e (1545, 290)
# -------------------------------------------------------------------------
symbols['bloco-e12a-pg'] = """          <g id="bloco-e12a-pg">
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

symbols['bloco-e12b-pg'] = """          <g id="bloco-e12b-pg">
            <!-- E12-B — Contato NF2 (21-22) de Força do Botão de Emergência E-STOP (Corte Bobina K1) -->
            <rect x="1468" y="265" width="80" height="52" rx="3" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="3,2"/>
            <text x="1508" y="277" text-anchor="middle" font-size="6.8" font-weight="700" fill="var(--fg)">E12-B — E-STOP</text>
            <text x="1508" y="286" text-anchor="middle" font-size="4.5" fill="var(--dim)">NF2 FORÇA (21-22)</text>

            <!-- Atuador Mecânico Cogumelo Vermelho -->
            <path d="M 1500,287 C 1500,281 1514,281 1514,287 Z" fill="#ef4444" stroke="var(--line)" stroke-width="1"/>
            <line x1="1507" y1="287" x2="1507" y2="293" stroke="var(--line)" stroke-width="1" stroke-dasharray="1.5,1.5"/>

            <!-- Contato NF (Normalmente Fechado) horizontal -->
            <line x1="1470" y1="295" x2="1496" y2="295" stroke="var(--line)" stroke-width="1.4"/>
            <circle cx="1496" cy="295" r="2.2" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1545" y1="295" x2="1518" y2="295" stroke="var(--line)" stroke-width="1.4"/>
            <circle cx="1518" cy="295" r="2.2" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Barra de contato NF repousando sobre os bornes -->
            <line x1="1494" y1="293" x2="1520" y2="293" stroke="var(--line)" stroke-width="2" stroke-linecap="round"/>

            <!-- Bornes de Conexão 21 e 22 -->
            <circle cx="1470" cy="290" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1470" cy="290" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1477" y="286" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">21</text>

            <circle cx="1545" cy="290" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1545" cy="290" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1538" y="286" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">22</text>
          </g>"""

# -------------------------------------------------------------------------
# 10. E25 — Buzzer Piezo 5V (Alarme Audível NR-12)
# Terminais: +5V em (2130, 480) e - (GND chaveado por Q1) em (2190, 510)
# Símbolo oficial acústico de avisador sonoro (buzzer)
# -------------------------------------------------------------------------
symbols['bloco-e25-pg'] = """          <g id="bloco-e25-pg">
            <!-- E25 — Avisador Sonoro Piezoelétrico (Buzzer 5V) -->
            <rect x="2120" y="448" width="80" height="68" rx="3" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="3,2"/>
            <text x="2160" y="460" text-anchor="middle" font-size="6.8" font-weight="700" fill="var(--fg)">E25 — BUZZER</text>
            <text x="2160" y="469" text-anchor="middle" font-size="4.5" fill="var(--dim)">PIEZO 5V (NR-12)</text>

            <!-- Símbolo Acústico IEC do Buzzer -->
            <!-- Corpo circular ou cilíndrico do buzzer -->
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

# Validate all XML strings
all_valid = True
for name, svg_code in symbols.items():
    try:
        wrapped = f"<svg xmlns='http://www.w3.org/2000/svg'>{svg_code}</svg>"
        xml.dom.minidom.parseString(wrapped)
        print(f"OK: {name}")
    except Exception as e:
        print(f"ERROR in {name}: {e}")
        all_valid = False

print(f"Overall validation: {'PASSED' if all_valid else 'FAILED'}")
