import xml.dom.minidom

e08_svg = """          <g id="bloco-e08-pg">
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

wrapped = f"<svg xmlns='http://www.w3.org/2000/svg'>{e08_svg}</svg>"
xml.dom.minidom.parseString(wrapped)
print("E08 SVG is valid XML!")
