import xml.dom.minidom

all_symbols = {}

# 1. E15 — DISJUNTOR BIPOLAR 2P (IEC 60898)
all_symbols['bloco-e15-pg'] = """          <g id="bloco-e15-pg">
            <!-- E15 — Disjuntor Bipolar Termomagnético 2P (Norma IEC 60898 / IEC 60947-2) -->
            <rect x="185" y="265" width="80" height="100" rx="3" fill="none" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="3,2"/>
            <text x="225" y="278" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E15 — DISJ. 2P</text>
            <text x="225" y="287" text-anchor="middle" font-size="4.8" fill="var(--dim)">10A CURVA C (IEC 60898)</text>

            <!-- POLO 1: FASE L (y = 300) -->
            <line x1="185" y1="300" x2="208" y2="300" stroke="var(--line)" stroke-width="1.4"/>
            <circle cx="208" cy="300" r="2.2" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="208" y1="300" x2="228" y2="291" stroke="var(--line)" stroke-width="1.8" stroke-linecap="round"/>
            <circle cx="232" cy="300" r="2.2" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Disparo Térmico Bimetálico -->
            <polyline points="232,300 240,300 240,296 248,296 248,300 252,300" fill="none" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Disparo Magnético -->
            <line x1="243" y1="293" x2="245" y2="295" stroke="var(--line)" stroke-width="1"/>
            <line x1="245" y1="293" x2="243" y2="295" stroke="var(--line)" stroke-width="1"/>
            <line x1="252" y1="300" x2="265" y2="300" stroke="var(--line)" stroke-width="1.4"/>

            <!-- POLO 2: NEUTRO N (y = 335) -->
            <line x1="185" y1="335" x2="208" y2="335" stroke="var(--line)" stroke-width="1.4"/>
            <circle cx="208" cy="335" r="2.2" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="208" y1="335" x2="228" y2="326" stroke="var(--line)" stroke-width="1.8" stroke-linecap="round"/>
            <circle cx="232" cy="335" r="2.2" fill="var(--bg)" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Disparo Térmico Bimetálico -->
            <polyline points="232,335 240,335 240,331 248,331 248,335 252,335" fill="none" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Disparo Magnético -->
            <line x1="243" y1="328" x2="245" y2="330" stroke="var(--line)" stroke-width="1"/>
            <line x1="245" y1="328" x2="243" y2="330" stroke="var(--line)" stroke-width="1"/>
            <line x1="252" y1="335" x2="265" y2="335" stroke="var(--line)" stroke-width="1.4"/>

            <!-- Acoplamento Mecânico Bipolar -->
            <line x1="220" y1="294" x2="220" y2="330" stroke="var(--line)" stroke-width="1" stroke-dasharray="2,2"/>
            <line x1="216" y1="312" x2="224" y2="312" stroke="var(--line)" stroke-width="2" stroke-linecap="round"/>

            <!-- Bornes IN_L, IN_N, OUT_L, OUT_N -->
            <circle cx="185" cy="300" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="185" cy="300" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="191" y="295" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">IN_L</text>

            <circle cx="185" cy="335" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="185" cy="335" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="191" y="330" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">IN_N</text>

            <circle cx="265" cy="300" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="265" cy="300" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="259" y="295" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">OUT_L</text>

            <circle cx="265" cy="335" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="265" cy="335" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="259" y="330" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">OUT_N</text>
          </g>"""

# 2. E01 — FONTE 12V 10A (SMPS AC/DC)
all_symbols['bloco-e01-pg'] = """          <g id="bloco-e01-pg">
            <!-- E01 — Fonte Chaveada Industrial 12V 10A (Conversor AC/DC SMPS) -->
            <rect x="310" y="265" width="105" height="125" rx="3" fill="none" stroke="var(--line)" stroke-width="1.4"/>
            <text x="362" y="279" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E01 — FONTE 12V</text>
            <text x="362" y="288" text-anchor="middle" font-size="5" fill="var(--dim)">SMPS AC/DC (12V 10A — 120W)</text>

            <!-- Linha divisória diagonal normativa IEC entre entrada AC e saída DC -->
            <line x1="335" y1="365" x2="390" y2="295" stroke="var(--line)" stroke-width="0.8" stroke-dasharray="2,2"/>

            <!-- Símbolo Entrada AC '~' -->
            <path d="M 342,320 Q 346,312 350,320 T 358,320" fill="none" stroke="var(--line)" stroke-width="1.6" stroke-linecap="round"/>
            <text x="350" y="330" text-anchor="middle" font-size="4.5" font-weight="700" fill="var(--dim)">AC IN</text>

            <!-- Símbolo Saída DC '=' -->
            <line x1="368" y1="334" x2="384" y2="334" stroke="var(--line)" stroke-width="1.6"/>
            <line x1="368" y1="338" x2="384" y2="338" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="2.5,2"/>
            <text x="376" y="347" text-anchor="middle" font-size="4.5" font-weight="700" fill="var(--fg)">DC OUT</text>

            <!-- Aterramento PE -->
            <line x1="310" y1="370" x2="328" y2="370" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="328" y1="364" x2="328" y2="376" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="331" y1="366" x2="331" y2="374" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="334" y1="368" x2="334" y2="372" stroke="var(--line)" stroke-width="1"/>

            <text x="362" y="380" text-anchor="middle" font-size="4.4" font-weight="700" fill="var(--fg)">CONFERIR CHAVE 115/230V!</text>

            <!-- Bornes: AC_L, AC_N, PE, +12V, GND -->
            <circle cx="310" cy="300" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="310" cy="300" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="317" y="295" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">AC_L</text>

            <circle cx="310" cy="335" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="310" cy="335" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="317" y="330" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">AC_N</text>

            <circle cx="310" cy="370" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="310" cy="370" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="317" y="365" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">PE ⏚</text>

            <circle cx="415" cy="300" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="415" cy="300" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="408" y="295" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">+12V</text>

            <circle cx="415" cy="355" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="415" cy="355" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="408" y="350" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">GND</text>
          </g>"""

# 3. H04 (S1) e E07 (S2) — Sensores Ópticos Reflexivos Infravermelhos 5V
all_symbols['bloco-h04-pg'] = """          <g id="bloco-h04-pg">
            <!-- H04 — Sensor Óptico Reflexivo S1 (Entrada da Esteira / Detecção de Castanha) -->
            <rect x="680" y="255" width="85" height="90" rx="3" fill="none" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="3,2"/>
            <text x="722" y="268" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">H04 — SENSOR S1</text>
            <text x="722" y="276" text-anchor="middle" font-size="4.6" fill="var(--dim)">ÓPTICO IR 5V (ENTRADA)</text>

            <!-- Símbolo Esquemático Interno IEC do Sensor Fotoelétrico -->
            <line x1="695" y1="300" x2="705" y2="300" stroke="var(--line)" stroke-width="1"/>
            <polygon points="705,296 705,304 712,300" fill="var(--fg)" stroke="var(--line)" stroke-width="0.8"/>
            <line x1="712" y1="296" x2="712" y2="304" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Flechas de Luz IR Emitidas -->
            <line x1="714" y1="297" x2="720" y2="294" stroke="var(--line)" stroke-width="0.8"/>
            <polygon points="720,294 717,296 719,298" fill="var(--line)"/>
            <line x1="714" y1="302" x2="720" y2="299" stroke="var(--line)" stroke-width="0.8"/>
            <polygon points="720,299 717,301 719,303" fill="var(--line)"/>

            <!-- Fototransistor Receptor -->
            <circle cx="738" cy="300" r="9" fill="none" stroke="var(--line)" stroke-width="0.8"/>
            <line x1="733" y1="294" x2="733" y2="306" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="733" y1="297" x2="742" y2="293" stroke="var(--line)" stroke-width="1"/>
            <line x1="733" y1="303" x2="742" y2="307" stroke="var(--line)" stroke-width="1"/>
            <polygon points="742,307 737,304 739,306" fill="var(--fg)"/>
            <line x1="727" y1="293" x2="732" y2="296" stroke="var(--line)" stroke-width="0.8"/>
            <polygon points="732,296 728,296 730,294" fill="var(--line)"/>

            <line x1="680" y1="280" x2="700" y2="280" stroke="var(--line)" stroke-width="1"/>
            <line x1="700" y1="280" x2="700" y2="300" stroke="var(--line)" stroke-width="1"/>
            <line x1="742" y1="293" x2="748" y2="293" stroke="var(--line)" stroke-width="1"/>
            <line x1="748" y1="293" x2="748" y2="305" stroke="var(--line)" stroke-width="1"/>
            <line x1="748" y1="305" x2="765" y2="305" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="742" y1="307" x2="748" y2="307" stroke="var(--line)" stroke-width="1"/>
            <line x1="748" y1="307" x2="748" y2="330" stroke="var(--line)" stroke-width="1"/>
            <line x1="748" y1="330" x2="765" y2="330" stroke="var(--line)" stroke-width="1.2"/>

            <!-- Bornes: VCC, OUT, GND -->
            <circle cx="680" cy="280" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="680" cy="280" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="687" y="276" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">VCC</text>

            <circle cx="765" cy="305" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="765" cy="305" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="758" y="301" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">OUT</text>

            <circle cx="765" cy="330" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="765" cy="330" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="758" y="326" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">GND</text>
          </g>"""

all_symbols['bloco-e07-pg'] = """          <g id="bloco-e07-pg">
            <!-- E07 — Sensor Óptico Reflexivo S2 (Saída / Pós-Classificação) -->
            <rect x="680" y="425" width="85" height="90" rx="3" fill="none" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="3,2"/>
            <text x="722" y="438" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E07 — SENSOR S2</text>
            <text x="722" y="446" text-anchor="middle" font-size="4.6" fill="var(--dim)">ÓPTICO IR 5V (SAÍDA)</text>

            <!-- Símbolo Esquemático Interno IEC do Sensor Fotoelétrico -->
            <line x1="695" y1="470" x2="705" y2="470" stroke="var(--line)" stroke-width="1"/>
            <polygon points="705,466 705,474 712,470" fill="var(--fg)" stroke="var(--line)" stroke-width="0.8"/>
            <line x1="712" y1="466" x2="712" y2="474" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Flechas de Luz IR Emitidas -->
            <line x1="714" y1="467" x2="720" y2="464" stroke="var(--line)" stroke-width="0.8"/>
            <polygon points="720,464 717,466 719,468" fill="var(--line)"/>
            <line x1="714" y1="472" x2="720" y2="469" stroke="var(--line)" stroke-width="0.8"/>
            <polygon points="720,469 717,471 719,473" fill="var(--line)"/>

            <!-- Fototransistor Receptor -->
            <circle cx="738" cy="470" r="9" fill="none" stroke="var(--line)" stroke-width="0.8"/>
            <line x1="733" y1="464" x2="733" y2="476" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="733" y1="467" x2="742" y2="463" stroke="var(--line)" stroke-width="1"/>
            <line x1="733" y1="473" x2="742" y2="477" stroke="var(--line)" stroke-width="1"/>
            <polygon points="742,477 737,474 739,476" fill="var(--fg)"/>
            <line x1="727" y1="463" x2="732" y2="466" stroke="var(--line)" stroke-width="0.8"/>
            <polygon points="732,466 728,466 730,464" fill="var(--line)"/>

            <line x1="680" y1="450" x2="700" y2="450" stroke="var(--line)" stroke-width="1"/>
            <line x1="700" y1="450" x2="700" y2="470" stroke="var(--line)" stroke-width="1"/>
            <line x1="742" y1="463" x2="748" y2="463" stroke="var(--line)" stroke-width="1"/>
            <line x1="748" y1="463" x2="748" y2="475" stroke="var(--line)" stroke-width="1"/>
            <line x1="748" y1="475" x2="765" y2="475" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="742" y1="477" x2="748" y2="477" stroke="var(--line)" stroke-width="1"/>
            <line x1="748" y1="477" x2="748" y2="500" stroke="var(--line)" stroke-width="1"/>
            <line x1="748" y1="500" x2="765" y2="500" stroke="var(--line)" stroke-width="1.2"/>

            <!-- Bornes: VCC, OUT, GND -->
            <circle cx="680" cy="450" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="680" cy="450" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="687" y="446" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">VCC</text>

            <circle cx="765" cy="475" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="765" cy="475" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="758" y="471" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">OUT</text>

            <circle cx="765" cy="500" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="765" cy="500" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="758" y="496" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">GND</text>
          </g>"""

# 4. X1 e X2 — Réguas de Bornes DIN (Terminal Blocks)
all_symbols['bloco-x1-pg'] = """          <g id="bloco-x1-pg">
            <!-- X1 — Régua de Bornes de Potência DIN (SAK 6 Vias) -->
            <rect x="450" y="455" width="80" height="185" rx="3" fill="none" stroke="var(--line)" stroke-width="1.4"/>
            <text x="490" y="470" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">X1 — BORNE E17</text>
            <text x="490" y="479" text-anchor="middle" font-size="4.8" fill="var(--dim)">RÉGUA SAK (POTÊNCIA / 12V)</text>

            <line x1="490" y1="486" x2="490" y2="635" stroke="var(--line)" stroke-width="0.8" stroke-dasharray="2,2"/>

            <!-- VIA 1: +12V_GERAL (y = 490) -->
            <line x1="450" y1="490" x2="530" y2="490" stroke="var(--line)" stroke-width="1.4"/>
            <rect x="482" y="484" width="16" height="12" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <text x="490" y="493" text-anchor="middle" font-size="5" font-weight="700" fill="var(--fg)">1</text>

            <!-- VIA 2: +12V_LÓGICA (y = 515) -->
            <line x1="490" y1="515" x2="530" y2="515" stroke="var(--line)" stroke-width="1.4"/>
            <rect x="482" y="509" width="16" height="12" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <text x="490" y="518" text-anchor="middle" font-size="5" font-weight="700" fill="var(--fg)">2</text>
            <line x1="486" y1="496" x2="486" y2="509" stroke="var(--fg)" stroke-width="1.4"/>

            <!-- VIA 3: +12V_ATUADORES (y = 540) -->
            <line x1="490" y1="540" x2="530" y2="540" stroke="var(--line)" stroke-width="1.4"/>
            <rect x="482" y="534" width="16" height="12" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <text x="490" y="543" text-anchor="middle" font-size="5" font-weight="700" fill="var(--fg)">3</text>

            <!-- VIA 4: RESERVA (y = 565) -->
            <rect x="482" y="559" width="16" height="12" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="0.8" stroke-dasharray="1.5,1.5"/>
            <text x="490" y="568" text-anchor="middle" font-size="4.5" fill="var(--dim)">4</text>
            <text x="502" y="568" text-anchor="start" font-size="4" fill="var(--dim)">RESERVA</text>

            <!-- VIA 5: GND_FONTE (y = 590) -->
            <line x1="450" y1="590" x2="530" y2="590" stroke="var(--line)" stroke-width="1.4"/>
            <rect x="482" y="584" width="16" height="12" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <text x="490" y="593" text-anchor="middle" font-size="5" font-weight="700" fill="var(--fg)">5</text>

            <!-- VIA 6: GND_DISTRIBUIÇÃO (y = 615) -->
            <line x1="490" y1="615" x2="530" y2="615" stroke="var(--line)" stroke-width="1.4"/>
            <rect x="482" y="609" width="16" height="12" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <text x="490" y="618" text-anchor="middle" font-size="5" font-weight="700" fill="var(--fg)">6</text>
            <line x1="486" y1="596" x2="486" y2="609" stroke="var(--fg)" stroke-width="1.4"/>

            <!-- Bornes -->
            <circle cx="450" cy="490" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="450" cy="490" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="457" y="486" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">1:+12V_G</text>

            <circle cx="530" cy="490" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="530" cy="490" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>

            <circle cx="530" cy="515" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="530" cy="515" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="523" y="511" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">2:+12V_L</text>

            <circle cx="530" cy="540" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="530" cy="540" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="523" y="536" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">3:+12V_AT</text>

            <circle cx="450" cy="590" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="450" cy="590" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="457" y="586" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">5:GND_F</text>

            <circle cx="530" cy="590" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="530" cy="590" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>

            <circle cx="530" cy="615" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="530" cy="615" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="523" y="611" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">6:GND_D</text>
          </g>"""

all_symbols['bloco-x2-pg'] = """          <g id="bloco-x2-pg">
            <!-- X2 — Régua de Bornes de Campo DIN (E17 — 7 Vias Sensores/E-STOP) -->
            <rect x="835" y="385" width="65" height="235" rx="3" fill="none" stroke="var(--line)" stroke-width="1.4"/>
            <text x="867" y="400" text-anchor="middle" font-size="7" font-weight="700" fill="var(--fg)">X2 — E17</text>
            <text x="867" y="409" text-anchor="middle" font-size="4.5" fill="var(--dim)">7 VIAS CAMPO</text>

            <line x1="867" y1="416" x2="867" y2="615" stroke="var(--line)" stroke-width="0.8" stroke-dasharray="2,2"/>

            <!-- VIA 1: SINAL S1 (y = 420) -->
            <line x1="835" y1="420" x2="900" y2="420" stroke="var(--line)" stroke-width="1.2"/>
            <rect x="860" y="415" width="14" height="10" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <text x="867" y="422" text-anchor="middle" font-size="4.8" font-weight="700" fill="var(--fg)">1</text>
            <circle cx="835" cy="420" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="835" cy="420" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="842" y="415" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--pin-text)">1:S1</text>
            <circle cx="900" cy="420" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="900" cy="420" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>

            <!-- VIA 2: SINAL S2 (y = 450) -->
            <line x1="835" y1="450" x2="900" y2="450" stroke="var(--line)" stroke-width="1.2"/>
            <rect x="860" y="445" width="14" height="10" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <text x="867" y="452" text-anchor="middle" font-size="4.8" font-weight="700" fill="var(--fg)">2</text>
            <circle cx="835" cy="450" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="835" cy="450" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="842" y="445" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--pin-text)">2:S2</text>
            <circle cx="900" cy="450" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="900" cy="450" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>

            <!-- VIA 3: GND S1 (y = 480) -->
            <line x1="835" y1="480" x2="900" y2="480" stroke="var(--line)" stroke-width="1.2"/>
            <rect x="860" y="475" width="14" height="10" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <text x="867" y="482" text-anchor="middle" font-size="4.8" font-weight="700" fill="var(--fg)">3</text>
            <circle cx="835" cy="480" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="835" cy="480" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="842" y="475" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--pin-text)">3:G_S1</text>
            <circle cx="900" cy="480" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="900" cy="480" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>

            <!-- VIA 4: GND S2 (y = 510) -->
            <line x1="835" y1="510" x2="900" y2="510" stroke="var(--line)" stroke-width="1.2"/>
            <rect x="860" y="505" width="14" height="10" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <text x="867" y="512" text-anchor="middle" font-size="4.8" font-weight="700" fill="var(--fg)">4</text>
            <circle cx="835" cy="510" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="835" cy="510" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="842" y="505" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--pin-text)">4:G_S2</text>
            <circle cx="900" cy="510" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="900" cy="510" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>

            <!-- VIA 5: COM E-STOP (y = 540) -->
            <line x1="835" y1="540" x2="900" y2="540" stroke="var(--line)" stroke-width="1.2"/>
            <rect x="860" y="535" width="14" height="10" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <text x="867" y="542" text-anchor="middle" font-size="4.8" font-weight="700" fill="var(--fg)">5</text>
            <circle cx="835" cy="540" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="835" cy="540" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="842" y="535" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--pin-text)">5:COM</text>
            <circle cx="900" cy="540" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="900" cy="540" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>

            <!-- VIA 6: NC E-STOP (y = 570) -->
            <line x1="835" y1="570" x2="900" y2="570" stroke="var(--line)" stroke-width="1.2"/>
            <rect x="860" y="565" width="14" height="10" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="1"/>
            <text x="867" y="572" text-anchor="middle" font-size="4.8" font-weight="700" fill="var(--fg)">6</text>
            <circle cx="835" cy="570" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="835" cy="570" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="842" y="565" text-anchor="start" font-size="4.5" font-weight="700" fill="var(--pin-text)">6:NC</text>
            <circle cx="900" cy="570" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="900" cy="570" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>

            <!-- VIA 7: RESERVA (y = 600) -->
            <rect x="860" y="595" width="14" height="10" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="0.8" stroke-dasharray="1.5,1.5"/>
            <text x="867" y="602" text-anchor="middle" font-size="4.5" fill="var(--dim)">7</text>
            <text x="867" y="612" text-anchor="middle" font-size="4" fill="var(--dim)">RESERVA</text>
          </g>"""

# 5. E19 e E27
all_symbols['bloco-e19-pg'] = """          <g id="bloco-e19-pg">
            <!-- E19 — Conector de Entrada AC (Plugue NBR 14136 2P+T 10A) -->
            <rect x="45" y="265" width="85" height="130" rx="3" fill="none" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="3,2"/>
            <text x="87" y="279" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E19 — PLUGUE AC</text>
            <text x="87" y="288" text-anchor="middle" font-size="5" fill="var(--dim)">NBR 14136 (2P+T 10A)</text>
            <text x="87" y="386" text-anchor="middle" font-size="4.8" fill="var(--dim)">127/220V~ + PG13.5</text>

            <line x1="85" y1="300" x2="130" y2="300" stroke="var(--line)" stroke-width="1.4"/>
            <rect x="88" y="297" width="12" height="6" rx="1" fill="var(--fg)"/>

            <line x1="85" y1="335" x2="130" y2="335" stroke="var(--line)" stroke-width="1.4"/>
            <rect x="88" y="332" width="12" height="6" rx="1" fill="var(--fg)"/>

            <line x1="85" y1="370" x2="130" y2="370" stroke="var(--line)" stroke-width="1.4"/>
            <rect x="88" y="367" width="12" height="6" rx="1" fill="var(--fg)"/>

            <circle cx="130" cy="300" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="130" cy="300" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="123" y="295" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">L</text>

            <circle cx="130" cy="335" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="130" cy="335" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="123" y="330" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">N</text>

            <circle cx="130" cy="370" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="130" cy="370" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="123" y="365" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">PE</text>
          </g>"""

all_symbols['bloco-e27-pe-pg'] = """          <g id="bloco-e27-pe-pg">
            <!-- E27 — Barramento de Terra de Proteção PE / Chassi (Norma IEC 60417-5019) -->
            <rect x="45" y="440" width="85" height="65" rx="3" fill="none" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="3,2"/>
            <text x="87" y="454" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">PE / CHASSI</text>
            <text x="87" y="463" text-anchor="middle" font-size="4.8" fill="var(--dim)">TERRA PROTEÇÃO (E27)</text>

            <line x1="130" y1="470" x2="87" y2="470" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="87" y1="470" x2="87" y2="476" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="75" y1="476" x2="99" y2="476" stroke="var(--line)" stroke-width="2"/>
            <line x1="79" y1="480" x2="95" y2="480" stroke="var(--line)" stroke-width="1.6"/>
            <line x1="83" y1="484" x2="91" y2="484" stroke="var(--line)" stroke-width="1.2"/>

            <text x="87" y="496" text-anchor="middle" font-size="4.5" fill="var(--dim)">CARCAÇA / ESTRUTURA</text>

            <circle cx="130" cy="470" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="130" cy="470" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="123" y="465" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">PE</text>
          </g>"""

# 6. E02 e E03 — Conversores DC-DC Buck Step-Down
all_symbols['bloco-e02-pg'] = """          <g id="bloco-e02-pg">
            <!-- E02 — Módulo Step-Down XL4015 6V (Conversor DC/DC) -->
            <rect x="310" y="685" width="100" height="85" rx="3" fill="none" stroke="var(--line)" stroke-width="1.4"/>
            <text x="360" y="699" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E02 — BUCK 6V</text>
            <text x="360" y="709" text-anchor="middle" font-size="4.8" fill="var(--dim)">XL4015 5A (SERVO+MOTOR)</text>

            <!-- Linha divisória DC/DC -->
            <line x1="335" y1="760" x2="385" y2="710" stroke="var(--line)" stroke-width="0.8" stroke-dasharray="2,2"/>
            <!-- Símbolo '=' Entrada DC -->
            <line x1="338" y1="733" x2="350" y2="733" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="338" y1="737" x2="350" y2="737" stroke="var(--line)" stroke-width="1" stroke-dasharray="2,1.5"/>
            <text x="344" y="746" text-anchor="middle" font-size="4" font-weight="700" fill="var(--dim)">12V</text>

            <!-- Símbolo '=' Saída DC com seta de regulação -->
            <line x1="370" y1="733" x2="382" y2="733" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="370" y1="737" x2="382" y2="737" stroke="var(--line)" stroke-width="1" stroke-dasharray="2,1.5"/>
            <text x="376" y="746" text-anchor="middle" font-size="4" font-weight="700" fill="var(--fg)">+6V</text>

            <!-- Bornes: IN+, IN-, OUT+, OUT- -->
            <circle cx="310" cy="720" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="310" cy="720" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="317" y="715" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">IN+</text>

            <circle cx="310" cy="750" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="310" cy="750" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="317" y="745" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">IN-</text>

            <circle cx="410" cy="720" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="410" cy="720" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="403" y="715" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">OUT+</text>

            <circle cx="410" cy="750" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="410" cy="750" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="403" y="745" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">OUT-</text>
          </g>"""

all_symbols['bloco-e03-pg'] = """          <g id="bloco-e03-pg">
            <!-- E03 — Módulo Step-Down LM2596 5V (Conversor DC/DC Lógica) -->
            <rect x="310" y="845" width="100" height="85" rx="3" fill="none" stroke="var(--line)" stroke-width="1.4"/>
            <text x="360" y="859" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E03 — BUCK 5V</text>
            <text x="360" y="869" text-anchor="middle" font-size="4.8" fill="var(--dim)">LM2596 (LÓGICA 5V)</text>

            <!-- Linha divisória DC/DC -->
            <line x1="335" y1="920" x2="385" y2="870" stroke="var(--line)" stroke-width="0.8" stroke-dasharray="2,2"/>
            <!-- Símbolo '=' Entrada DC -->
            <line x1="338" y1="893" x2="350" y2="893" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="338" y1="897" x2="350" y2="897" stroke="var(--line)" stroke-width="1" stroke-dasharray="2,1.5"/>
            <text x="344" y="906" text-anchor="middle" font-size="4" font-weight="700" fill="var(--dim)">12V</text>

            <!-- Símbolo '=' Saída DC -->
            <line x1="370" y1="893" x2="382" y2="893" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="370" y1="897" x2="382" y2="897" stroke="var(--line)" stroke-width="1" stroke-dasharray="2,1.5"/>
            <text x="376" y="906" text-anchor="middle" font-size="4" font-weight="700" fill="var(--fg)">+5V</text>

            <!-- Bornes: IN+, IN-, OUT+, OUT- -->
            <circle cx="310" cy="880" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="310" cy="880" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="317" y="875" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">IN+</text>

            <circle cx="310" cy="910" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="310" cy="910" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="317" y="905" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">IN-</text>

            <circle cx="410" cy="880" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="410" cy="880" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="403" y="875" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">OUT+</text>

            <circle cx="410" cy="910" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="410" cy="910" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="403" y="905" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">OUT-</text>
          </g>"""

# 7. H02 — SERVO MG996R (Símbolo de Servomotor IEC)
all_symbols['bloco-h02-pg'] = """          <g id="bloco-h02-pg">
            <!-- H02 — Servomotor de Rejeição MG996R (Norma IEC / IEEE) -->
            <rect x="1830" y="250" width="120" height="105" rx="3" fill="none" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="3,2"/>
            <text x="1890" y="263" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">H02 — SERVO MG996R</text>
            <text x="1890" y="348" text-anchor="middle" font-size="4.6" fill="var(--dim)">ATUADOR ANGULAR (0°–180°)</text>

            <!-- Símbolo IEC de Servomotor (Círculo de Motor com engrenagem/seta de posição) -->
            <circle cx="1898" cy="305" r="22" fill="none" stroke="var(--line)" stroke-width="1.4"/>
            <text x="1898" y="310" text-anchor="middle" font-size="12" font-weight="800" fill="var(--fg)">M</text>
            <text x="1898" y="320" text-anchor="middle" font-size="5" font-weight="700" fill="var(--dim)">SERVO</text>
            <!-- Arco de rotação angular com seta -->
            <path d="M 1884,288 A 18 18 0 0 1 1912,288" fill="none" stroke="var(--line)" stroke-width="1.2"/>
            <polygon points="1912,288 1908,284 1913,283" fill="var(--fg)"/>

            <!-- Linhas internas de controle e alimentação -->
            <line x1="1830" y1="275" x2="1876" y2="275" stroke="var(--line)" stroke-width="1.2"/>
            <polyline points="1855,272 1860,272 1860,278 1865,278 1865,272 1870,272" fill="none" stroke="var(--line)" stroke-width="1"/>
            <line x1="1876" y1="275" x2="1876" y2="305" stroke="var(--line)" stroke-width="1"/>

            <line x1="1830" y1="305" x2="1876" y2="305" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1830" y1="335" x2="1876" y2="335" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1876" y1="335" x2="1876" y2="305" stroke="var(--line)" stroke-width="1"/>

            <!-- Bornes de Conexão: PWM, VCC, GND -->
            <circle cx="1830" cy="275" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1830" cy="275" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1837" y="271" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">PWM (50Hz)</text>

            <circle cx="1830" cy="305" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1830" cy="305" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1837" y="301" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">VCC (+6V)</text>

            <circle cx="1830" cy="335" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1830" cy="335" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1837" y="331" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">GND</text>
          </g>"""

# 8. E13 — RING LIGHT (Símbolo de Anel Iluminador LED)
all_symbols['bloco-e13-pg'] = """          <g id="bloco-e13-pg">
            <!-- E13 — Anel de Iluminação Ring Light LED 12V 6000K -->
            <rect x="2130" y="830" width="120" height="60" rx="3" fill="none" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="3,2"/>
            <text x="2190" y="844" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E13 — RING LIGHT</text>
            <text x="2190" y="854" text-anchor="middle" font-size="4.8" fill="var(--dim)">LED 12V 6000K CÚPULA</text>

            <!-- Símbolo de Lâmpada / Iluminação LED -->
            <circle cx="2165" cy="868" r="10" fill="none" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="2158" y1="861" x2="2172" y2="875" stroke="var(--line)" stroke-width="1"/>
            <line x1="2172" y1="861" x2="2158" y2="875" stroke="var(--line)" stroke-width="1"/>
            <!-- Raios de luz emitidos -->
            <line x1="2177" y1="863" x2="2183" y2="859" stroke="var(--line)" stroke-width="0.8"/>
            <line x1="2178" y1="868" x2="2185" y2="868" stroke="var(--line)" stroke-width="0.8"/>
            <line x1="2177" y1="873" x2="2183" y2="877" stroke="var(--line)" stroke-width="0.8"/>

            <line x1="2130" y1="860" x2="2155" y2="860" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="2165" y1="878" x2="2165" y2="890" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="2165" y1="890" x2="2190" y2="890" stroke="var(--line)" stroke-width="1.2"/>

            <circle cx="2130" cy="860" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="2130" cy="860" r="1.4" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="2137" y="856" text-anchor="start" font-size="4.8" font-weight="700" fill="var(--pin-text)">+12V</text>

            <circle cx="2190" cy="890" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="2190" cy="890" r="1.4" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="2190" y="884" text-anchor="middle" font-size="4.8" font-weight="700" fill="var(--pin-text)">GND</text>
          </g>"""

# 9. E14 — WEBCAM 1080p + HOST VISÃO (Fundo transparente)
all_symbols['bloco-e14-pg'] = """          <g id="bloco-e14-pg">
            <rect x="1100" y="820" width="230" height="95" rx="3" fill="none" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="3,2"/>
            <text x="1215" y="840" text-anchor="middle" font-size="8" font-weight="700" fill="var(--fg)">E14 — WEBCAM 1080p + HOST VISÃO</text>
            <text x="1215" y="854" text-anchor="middle" font-size="5.5" fill="var(--dim)">CÂMERA USB 2.0 (CÚPULA ÓPTICA) → MINI-PC YOLOv8</text>
            <text x="1215" y="870" text-anchor="middle" font-size="5.2" fill="var(--fg)">• Alimentação 5V / Dados via Cabo USB 2.0 Direto no Host</text>
            <text x="1215" y="884" text-anchor="middle" font-size="5.2" fill="var(--dim)">• Host envia comando de classificação ao ESP32 via USB-UART (Pinos 1/3)</text>
            <text x="1215" y="898" text-anchor="middle" font-size="5.0" fill="var(--dim)">• Iluminação constante garantida pelo Ring Light E13 (12V 6000K)</text>
          </g>"""

# Validate all XML strings
all_valid = True
for name, svg_code in all_symbols.items():
    try:
        wrapped = f"<svg xmlns='http://www.w3.org/2000/svg'>{svg_code}</svg>"
        xml.dom.minidom.parseString(wrapped)
        print(f"OK: {name}")
    except Exception as e:
        print(f"ERROR in {name}: {e}")
        all_valid = False

print(f"Overall validation: {'PASSED' if all_valid else 'FAILED'}")
