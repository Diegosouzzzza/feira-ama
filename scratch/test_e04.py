import xml.dom.minidom

e04_svg = """          <g id="bloco-e04-pg">
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
            <!-- Gap dielétrico entre gate e canal -->
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

            <!-- Terminal VCC (1830, 580) - Pull-up / acoplador óptico interno -->
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

wrapped = f"<svg xmlns='http://www.w3.org/2000/svg'>{e04_svg}</svg>"
xml.dom.minidom.parseString(wrapped)
print("E04 SVG is valid XML!")
