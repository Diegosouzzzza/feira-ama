import xml.dom.minidom

unboxed_symbols = {}

# -------------------------------------------------------------------------
# 1. E15 — Disjuntor Bipolar 2P (SEM NENHUMA CAIXA)
# -------------------------------------------------------------------------
unboxed_symbols['bloco-e15-pg'] = """          <g id="bloco-e15-pg">
            <!-- E15 — Disjuntor Bipolar Termomagnético 2P (IEC 60898) — Totalmente Aberto -->
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
            <text x="179" y="295" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">IN_L</text>

            <circle cx="185" cy="335" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="185" cy="335" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="179" y="330" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">IN_N</text>

            <circle cx="265" cy="300" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="265" cy="300" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="271" y="295" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">OUT_L</text>

            <circle cx="265" cy="335" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="265" cy="335" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="271" y="330" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">OUT_N</text>
          </g>"""

# -------------------------------------------------------------------------
# 2. E01 — Fonte 12V 10A (SEM NENHUMA CAIXA)
# -------------------------------------------------------------------------
unboxed_symbols['bloco-e01-pg'] = """          <g id="bloco-e01-pg">
            <!-- E01 — Fonte Chaveada Industrial 12V 10A (Conversor AC/DC SMPS) — Totalmente Aberto -->
            <text x="362" y="278" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E01 — FONTE 12V</text>
            <text x="362" y="287" text-anchor="middle" font-size="5" fill="var(--dim)">SMPS AC/DC (12V 10A — 120W)</text>

            <!-- Linha divisória diagonal normativa IEC entre entrada AC e saída DC -->
            <line x1="345" y1="365" x2="385" y2="295" stroke="var(--line)" stroke-width="0.8" stroke-dasharray="2,2"/>

            <!-- Símbolo Entrada AC '~' -->
            <path d="M 345,320 Q 349,312 353,320 T 361,320" fill="none" stroke="var(--line)" stroke-width="1.6" stroke-linecap="round"/>
            <text x="353" y="330" text-anchor="middle" font-size="4.5" font-weight="700" fill="var(--dim)">AC IN</text>

            <!-- Símbolo Saída DC '=' -->
            <line x1="368" y1="334" x2="384" y2="334" stroke="var(--line)" stroke-width="1.6"/>
            <line x1="368" y1="338" x2="384" y2="338" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="2.5,2"/>
            <text x="376" y="347" text-anchor="middle" font-size="4.5" font-weight="700" fill="var(--fg)">DC OUT</text>

            <!-- Aterramento PE -->
            <line x1="310" y1="370" x2="332" y2="370" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="332" y1="364" x2="332" y2="376" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="335" y1="366" x2="335" y2="374" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="338" y1="368" x2="338" y2="372" stroke="var(--line)" stroke-width="1"/>

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

# -------------------------------------------------------------------------
# 3. H04 (S1) e E07 (S2) — Sensores Ópticos Reflexivos (SEM CAIXAS PONTILHADAS)
# Ajustado também o posicionamento dos textos para eliminar qualquer sobreposição!
# -------------------------------------------------------------------------
unboxed_symbols['bloco-h04-pg'] = """          <g id="bloco-h04-pg">
            <!-- H04 — Sensor Óptico Reflexivo S1 (Entrada) — Totalmente Aberto -->
            <text x="725" y="260" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">H04 — SENSOR S1</text>
            <text x="725" y="270" text-anchor="middle" font-size="4.8" fill="var(--dim)">ÓPTICO IR 5V (ENTRADA)</text>

            <!-- Símbolo Esquemático Interno IEC do Sensor Fotoelétrico -->
            <!-- Diodo Emissor Infravermelho (LED IR) -->
            <line x1="680" y1="280" x2="700" y2="280" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="700" y1="280" x2="700" y2="300" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="695" y1="300" x2="705" y2="300" stroke="var(--line)" stroke-width="1.2"/>
            <polygon points="705,296 705,304 712,300" fill="var(--fg)" stroke="var(--line)" stroke-width="0.8"/>
            <line x1="712" y1="296" x2="712" y2="304" stroke="var(--line)" stroke-width="1.4"/>
            <!-- Flechas de Luz IR Emitidas -->
            <line x1="714" y1="297" x2="720" y2="294" stroke="var(--line)" stroke-width="0.8"/>
            <polygon points="720,294 717,296 719,298" fill="var(--line)"/>
            <line x1="714" y1="302" x2="720" y2="299" stroke="var(--line)" stroke-width="0.8"/>
            <polygon points="720,299 717,301 719,303" fill="var(--line)"/>

            <!-- Fototransistor Receptor -->
            <circle cx="738" cy="300" r="9" fill="none" stroke="var(--line)" stroke-width="1"/>
            <line x1="733" y1="294" x2="733" y2="306" stroke="var(--line)" stroke-width="1.6"/>
            <line x1="733" y1="297" x2="742" y2="293" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="733" y1="303" x2="742" y2="307" stroke="var(--line)" stroke-width="1.2"/>
            <polygon points="742,307 737,304 739,306" fill="var(--fg)"/>
            <!-- Flechas de Luz Refletida Entrando -->
            <line x1="727" y1="293" x2="732" y2="296" stroke="var(--line)" stroke-width="0.8"/>
            <polygon points="732,296 728,296 730,294" fill="var(--line)"/>

            <!-- Linhas de conexão aos bornes de saída -->
            <line x1="742" y1="293" x2="748" y2="293" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="748" y1="293" x2="748" y2="305" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="748" y1="305" x2="765" y2="305" stroke="var(--line)" stroke-width="1.2"/>

            <line x1="742" y1="307" x2="748" y2="307" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="748" y1="307" x2="748" y2="330" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="748" y1="330" x2="765" y2="330" stroke="var(--line)" stroke-width="1.2"/>

            <!-- Bornes e Rótulos sem sobreposição -->
            <circle cx="680" cy="280" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="680" cy="280" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="674" y="276" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">VCC</text>

            <circle cx="765" cy="305" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="765" cy="305" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="758" y="301" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">OUT</text>

            <circle cx="765" cy="330" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="765" cy="330" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="758" y="326" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">GND</text>
          </g>"""

unboxed_symbols['bloco-e07-pg'] = """          <g id="bloco-e07-pg">
            <!-- E07 — Sensor Óptico Reflexivo S2 (Saída) — Totalmente Aberto (SEM CAIXA PONTILHADA) -->
            <text x="725" y="432" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E07 — SENSOR S2</text>
            <text x="725" y="442" text-anchor="middle" font-size="4.8" fill="var(--dim)">ÓPTICO IR 5V (SAÍDA)</text>

            <!-- Símbolo Esquemático Interno IEC do Sensor Fotoelétrico -->
            <!-- Diodo Emissor Infravermelho (LED IR) -->
            <line x1="680" y1="450" x2="700" y2="450" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="700" y1="450" x2="700" y2="470" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="695" y1="470" x2="705" y2="470" stroke="var(--line)" stroke-width="1.2"/>
            <polygon points="705,466 705,474 712,470" fill="var(--fg)" stroke="var(--line)" stroke-width="0.8"/>
            <line x1="712" y1="466" x2="712" y2="474" stroke="var(--line)" stroke-width="1.4"/>
            <!-- Flechas de Luz IR Emitidas -->
            <line x1="714" y1="467" x2="720" y2="464" stroke="var(--line)" stroke-width="0.8"/>
            <polygon points="720,464 717,466 719,468" fill="var(--line)"/>
            <line x1="714" y1="472" x2="720" y2="469" stroke="var(--line)" stroke-width="0.8"/>
            <polygon points="720,469 717,471 719,473" fill="var(--line)"/>

            <!-- Fototransistor Receptor -->
            <circle cx="738" cy="470" r="9" fill="none" stroke="var(--line)" stroke-width="1"/>
            <line x1="733" y1="464" x2="733" y2="476" stroke="var(--line)" stroke-width="1.6"/>
            <line x1="733" y1="467" x2="742" y2="463" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="733" y1="473" x2="742" y2="477" stroke="var(--line)" stroke-width="1.2"/>
            <polygon points="742,477 737,474 739,476" fill="var(--fg)"/>
            <!-- Flechas de Luz Refletida Entrando -->
            <line x1="727" y1="463" x2="732" y2="466" stroke="var(--line)" stroke-width="0.8"/>
            <polygon points="732,466 728,466 730,464" fill="var(--line)"/>

            <!-- Linhas de conexão aos bornes de saída -->
            <line x1="742" y1="463" x2="748" y2="463" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="748" y1="463" x2="748" y2="475" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="748" y1="475" x2="765" y2="475" stroke="var(--line)" stroke-width="1.2"/>

            <line x1="742" y1="477" x2="748" y2="477" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="748" y1="477" x2="748" y2="500" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="748" y1="500" x2="765" y2="500" stroke="var(--line)" stroke-width="1.2"/>

            <!-- Bornes e Rótulos sem colisão -->
            <circle cx="680" cy="450" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="680" cy="450" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="674" y="446" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">VCC</text>

            <circle cx="765" cy="475" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="765" cy="475" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="758" y="471" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">OUT</text>

            <circle cx="765" cy="500" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="765" cy="500" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="758" y="496" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">GND</text>
          </g>"""

# -------------------------------------------------------------------------
# 4. E16 — Fusíveis (SEM CAIXA PONTILHADA)
# -------------------------------------------------------------------------
unboxed_symbols['bloco-e16-pg'] = """          <g id="bloco-e16-pg">
            <!-- E16 — Módulo de Fusíveis DIN (Norma IEC 60127) — Totalmente Aberto -->
            <text x="490" y="278" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E16 — FUSÍVEIS</text>
            <text x="490" y="287" text-anchor="middle" font-size="4.8" fill="var(--dim)">TRILHO DIN (IEC 60127)</text>

            <!-- F1: FUSÍVEL GERAL 10A (Símbolo IEC longitudinal) -->
            <line x1="450" y1="300" x2="530" y2="300" stroke="var(--line)" stroke-width="1.4"/>
            <rect x="470" y="294" width="40" height="12" rx="1" fill="var(--bg)" stroke="var(--line)" stroke-width="1.4"/>
            <text x="490" y="302" text-anchor="middle" font-size="4.5" font-weight="700" fill="var(--fg)">F1 10A</text>
            <text x="490" y="311" text-anchor="middle" font-size="3.5" fill="var(--dim)">GERAL (W006→W007)</text>

            <!-- Fusíveis Derivados Setoriais -->
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

            <!-- Bornes IN e OUT -->
            <circle cx="450" cy="300" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="450" cy="300" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="444" y="295" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">IN</text>

            <circle cx="530" cy="300" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="530" cy="300" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="536" y="295" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">OUT</text>
          </g>"""

# -------------------------------------------------------------------------
# 5. E08 — Relé K1 (SEM CAIXA PONTILHADA)
# -------------------------------------------------------------------------
unboxed_symbols['bloco-e08-pg'] = """          <g id="bloco-e08-pg">
            <!-- E08 — Relé de Segurança K1 (12V 40A / NR-12) — Totalmente Aberto -->
            <text x="1647" y="278" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E08 — RELÉ K1</text>
            <text x="1647" y="288" text-anchor="middle" font-size="4.8" fill="var(--dim)">12V 40A (NR-12)</text>

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
            <text x="1593" y="286" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">85</text>

            <circle cx="1645" cy="400" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1645" cy="400" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1645" y="393" text-anchor="middle" font-size="5" font-weight="700" fill="var(--pin-text)">86</text>

            <circle cx="1600" cy="375" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1600" cy="375" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1593" y="371" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">30</text>

            <circle cx="1695" cy="375" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1695" cy="375" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1701" y="371" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">87</text>
          </g>"""

# -------------------------------------------------------------------------
# 6. H02 — Servo MG996R (SEM CAIXA PONTILHADA)
# -------------------------------------------------------------------------
unboxed_symbols['bloco-h02-pg'] = """          <g id="bloco-h02-pg">
            <!-- H02 — Servomotor de Rejeição MG996R — Totalmente Aberto -->
            <text x="1890" y="260" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">H02 — SERVO MG996R</text>
            <text x="1890" y="270" text-anchor="middle" font-size="4.6" fill="var(--dim)">ATUADOR ANGULAR (0°–180°)</text>

            <!-- Símbolo IEC de Servomotor -->
            <circle cx="1898" cy="305" r="22" fill="none" stroke="var(--line)" stroke-width="1.4"/>
            <text x="1898" y="310" text-anchor="middle" font-size="12" font-weight="800" fill="var(--fg)">M</text>
            <text x="1898" y="320" text-anchor="middle" font-size="5" font-weight="700" fill="var(--dim)">SERVO</text>
            <path d="M 1884,288 A 18 18 0 0 1 1912,288" fill="none" stroke="var(--line)" stroke-width="1.2"/>
            <polygon points="1912,288 1908,284 1913,283" fill="var(--fg)"/>

            <!-- Linhas internas -->
            <line x1="1830" y1="275" x2="1876" y2="275" stroke="var(--line)" stroke-width="1.2"/>
            <polyline points="1855,272 1860,272 1860,278 1865,278 1865,272 1870,272" fill="none" stroke="var(--line)" stroke-width="1"/>
            <line x1="1876" y1="275" x2="1876" y2="305" stroke="var(--line)" stroke-width="1.2"/>

            <line x1="1830" y1="305" x2="1876" y2="305" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1830" y1="335" x2="1876" y2="335" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1876" y1="335" x2="1876" y2="305" stroke="var(--line)" stroke-width="1.2"/>

            <!-- Bornes de Conexão: PWM, VCC, GND -->
            <circle cx="1830" cy="275" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1830" cy="275" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1824" y="271" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">PWM</text>

            <circle cx="1830" cy="305" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1830" cy="305" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1824" y="301" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">+6V</text>

            <circle cx="1830" cy="335" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1830" cy="335" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1824" y="331" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">GND</text>
          </g>"""

# -------------------------------------------------------------------------
# 7. E04 — Driver MOSFET D4184 (SEM CAIXA PONTILHADA)
# -------------------------------------------------------------------------
unboxed_symbols['bloco-e04-pg'] = """          <g id="bloco-e04-pg">
            <!-- E04 — Módulo Driver MOSFET de Potência D4184 — Totalmente Aberto -->
            <text x="1890" y="499" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E04 — MOSFET D4184</text>
            <text x="1890" y="509" text-anchor="middle" font-size="4.8" fill="var(--dim)">DRIVER N-CH PWM / ON-OFF</text>

            <!-- Barramento Positivo Direto (Pass-Through: VIN+ -> VOUT+) -->
            <line x1="1830" y1="520" x2="1950" y2="520" stroke="var(--line)" stroke-width="1.6"/>
            <text x="1890" y="516" text-anchor="middle" font-size="4" font-weight="700" fill="var(--fg)">BARRAMENTO +6V DIRETO</text>

            <!-- Símbolo Esquemático Interno do MOSFET Canal N (D4184) -->
            <line x1="1830" y1="640" x2="1868" y2="640" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1868" y1="640" x2="1868" y2="585" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="1868" y1="585" x2="1878" y2="585" stroke="var(--line)" stroke-width="1.2"/>
            <!-- Placa de Gate isolada -->
            <line x1="1878" y1="573" x2="1878" y2="597" stroke="var(--line)" stroke-width="1.8" stroke-linecap="round"/>

            <!-- Canal N: 3 segmentos -->
            <line x1="1884" y1="571" x2="1884" y2="577" stroke="var(--line)" stroke-width="2"/>
            <line x1="1884" y1="582" x2="1884" y2="588" stroke="var(--line)" stroke-width="2"/>
            <line x1="1884" y1="593" x2="1884" y2="599" stroke="var(--line)" stroke-width="2"/>

            <!-- Terminal de Dreno (D) -->
            <line x1="1884" y1="574" x2="1904" y2="574" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="1904" y1="574" x2="1904" y2="580" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="1904" y1="580" x2="1950" y2="580" stroke="var(--line)" stroke-width="1.4"/>
            <text x="1898" y="570" text-anchor="middle" font-size="4.2" font-weight="700" fill="var(--fg)">D</text>

            <!-- Terminal de Substrato e Fonte (S) -->
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

            <!-- Terminal VCC (1830, 580) -->
            <line x1="1830" y1="580" x2="1848" y2="580" stroke="var(--line)" stroke-width="1.2"/>
            <rect x="1848" y="575" width="10" height="10" rx="0.5" fill="var(--bg)" stroke="var(--line)" stroke-width="0.8"/>
            <text x="1853" y="582" text-anchor="middle" font-size="3" fill="var(--dim)">OPTO</text>

            <!-- Diodo de Corpo Interno do MOSFET -->
            <line x1="1916" y1="574" x2="1916" y2="596" stroke="var(--line)" stroke-width="0.8"/>
            <polygon points="1912,590 1920,590 1916,580" fill="none" stroke="var(--line)" stroke-width="0.8"/>
            <line x1="1912" y1="580" x2="1920" y2="580" stroke="var(--line)" stroke-width="1"/>

            <!-- Círculo envolvente do transistor -->
            <circle cx="1895" cy="585" r="22" fill="none" stroke="var(--line)" stroke-width="0.8" stroke-dasharray="2,2"/>

            <!-- Bornes de Conexão -->
            <circle cx="1830" cy="520" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1830" cy="520" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1824" y="516" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">VIN+</text>

            <circle cx="1830" cy="550" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1830" cy="550" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1824" y="546" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">VIN-</text>

            <circle cx="1830" cy="580" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1830" cy="580" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1824" y="576" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">VCC</text>

            <circle cx="1830" cy="610" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1830" cy="610" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1824" y="606" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">GND</text>

            <circle cx="1830" cy="640" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1830" cy="640" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1824" y="636" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">SIG</text>

            <circle cx="1950" cy="520" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1950" cy="520" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1956" y="516" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">VOUT+</text>

            <circle cx="1950" cy="580" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="1950" cy="580" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="1956" y="576" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">VOUT-</text>
          </g>"""

# -------------------------------------------------------------------------
# 8. E13 — Ring Light (SEM CAIXA PONTILHADA)
# -------------------------------------------------------------------------
unboxed_symbols['bloco-e13-pg'] = """          <g id="bloco-e13-pg">
            <!-- E13 — Anel de Iluminação Ring Light LED 12V 6000K — Totalmente Aberto -->
            <text x="2190" y="844" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E13 — RING LIGHT</text>
            <text x="2190" y="854" text-anchor="middle" font-size="4.8" fill="var(--dim)">LED 12V 6000K CÚPULA</text>

            <!-- Símbolo de Iluminação LED -->
            <circle cx="2165" cy="868" r="10" fill="none" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="2158" y1="861" x2="2172" y2="875" stroke="var(--line)" stroke-width="1"/>
            <line x1="2172" y1="861" x2="2158" y2="875" stroke="var(--line)" stroke-width="1"/>
            <line x1="2177" y1="863" x2="2183" y2="859" stroke="var(--line)" stroke-width="0.8"/>
            <line x1="2178" y1="868" x2="2185" y2="868" stroke="var(--line)" stroke-width="0.8"/>
            <line x1="2177" y1="873" x2="2183" y2="877" stroke="var(--line)" stroke-width="0.8"/>

            <line x1="2130" y1="860" x2="2155" y2="860" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="2165" y1="878" x2="2165" y2="890" stroke="var(--line)" stroke-width="1.2"/>
            <line x1="2165" y1="890" x2="2190" y2="890" stroke="var(--line)" stroke-width="1.2"/>

            <circle cx="2130" cy="860" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="2130" cy="860" r="1.4" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="2124" y="856" text-anchor="end" font-size="4.8" font-weight="700" fill="var(--pin-text)">+12V</text>

            <circle cx="2190" cy="890" r="3.5" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="2190" cy="890" r="1.4" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="2190" y="884" text-anchor="middle" font-size="4.8" font-weight="700" fill="var(--pin-text)">GND</text>
          </g>"""

# -------------------------------------------------------------------------
# 9. E19 e E27 (SEM CAIXAS PONTILHADAS)
# -------------------------------------------------------------------------
unboxed_symbols['bloco-e19-pg'] = """          <g id="bloco-e19-pg">
            <!-- E19 — Conector de Entrada AC (Plugue NBR 14136 2P+T 10A) — Totalmente Aberto -->
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

unboxed_symbols['bloco-e27-pe-pg'] = """          <g id="bloco-e27-pe-pg">
            <!-- E27 — Barramento de Terra de Proteção PE / Chassi (Norma IEC 60417-5019) — Totalmente Aberto -->
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

# -------------------------------------------------------------------------
# 10. E14 — WEBCAM 1080p + HOST VISÃO (SEM CAIXA PONTILHADA)
# -------------------------------------------------------------------------
unboxed_symbols['bloco-e14-pg'] = """          <g id="bloco-e14-pg">
            <text x="1215" y="840" text-anchor="middle" font-size="8" font-weight="700" fill="var(--fg)">E14 — WEBCAM 1080p + HOST VISÃO</text>
            <text x="1215" y="854" text-anchor="middle" font-size="5.5" fill="var(--dim)">CÂMERA USB 2.0 (CÚPULA ÓPTICA) → MINI-PC YOLOv8</text>
            <text x="1215" y="870" text-anchor="middle" font-size="5.2" fill="var(--fg)">• Alimentação 5V / Dados via Cabo USB 2.0 Direto no Host</text>
            <text x="1215" y="884" text-anchor="middle" font-size="5.2" fill="var(--dim)">• Host envia comando de classificação ao ESP32 via USB-UART (Pinos 1/3)</text>
            <text x="1215" y="898" text-anchor="middle" font-size="5.0" fill="var(--dim)">• Iluminação constante garantida pelo Ring Light E13 (12V 6000K)</text>
          </g>"""

# Validate all
all_valid = True
for name, svg_code in unboxed_symbols.items():
    try:
        wrapped = f"<svg xmlns='http://www.w3.org/2000/svg'>{svg_code}</svg>"
        xml.dom.minidom.parseString(wrapped)
        print(f"OK: {name}")
    except Exception as e:
        print(f"ERROR in {name}: {e}")
        all_valid = False

print(f"Overall validation: {'PASSED' if all_valid else 'FAILED'}")
