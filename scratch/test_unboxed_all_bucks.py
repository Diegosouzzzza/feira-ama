import xml.dom.minidom
from test_unboxed_all import unboxed_symbols

unboxed_symbols['bloco-e02-pg'] = """          <g id="bloco-e02-pg">
            <!-- E02 — Módulo Step-Down XL4015 6V (Conversor DC/DC) — Totalmente Aberto -->
            <text x="360" y="699" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E02 — BUCK 6V</text>
            <text x="360" y="709" text-anchor="middle" font-size="4.8" fill="var(--dim)">XL4015 5A (SERVO+MOTOR)</text>

            <!-- Linha divisória DC/DC -->
            <line x1="340" y1="755" x2="380" y2="715" stroke="var(--line)" stroke-width="0.8" stroke-dasharray="2,2"/>
            <!-- Símbolo '=' Entrada DC -->
            <line x1="338" y1="733" x2="350" y2="733" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="338" y1="737" x2="350" y2="737" stroke="var(--line)" stroke-width="1" stroke-dasharray="2,1.5"/>
            <text x="344" y="746" text-anchor="middle" font-size="4" font-weight="700" fill="var(--dim)">12V</text>

            <!-- Símbolo '=' Saída DC -->
            <line x1="370" y1="733" x2="382" y2="733" stroke="var(--line)" stroke-width="1.4"/>
            <line x1="370" y1="737" x2="382" y2="737" stroke="var(--line)" stroke-width="1" stroke-dasharray="2,1.5"/>
            <text x="376" y="746" text-anchor="middle" font-size="4" font-weight="700" fill="var(--fg)">+6V</text>

            <!-- Bornes: IN+, IN-, OUT+, OUT- -->
            <circle cx="310" cy="720" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="310" cy="720" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="304" y="715" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">IN+</text>

            <circle cx="310" cy="750" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="310" cy="750" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="304" y="745" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">IN-</text>

            <circle cx="410" cy="720" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="410" cy="720" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="416" y="715" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">OUT+</text>

            <circle cx="410" cy="750" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="410" cy="750" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="416" y="745" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">OUT-</text>
          </g>"""

unboxed_symbols['bloco-e03-pg'] = """          <g id="bloco-e03-pg">
            <!-- E03 — Módulo Step-Down LM2596 5V (Conversor DC/DC) — Totalmente Aberto -->
            <text x="360" y="859" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E03 — BUCK 5V</text>
            <text x="360" y="869" text-anchor="middle" font-size="4.8" fill="var(--dim)">LM2596 (LÓGICA 5V)</text>

            <!-- Linha divisória DC/DC -->
            <line x1="340" y1="915" x2="380" y2="875" stroke="var(--line)" stroke-width="0.8" stroke-dasharray="2,2"/>
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
            <text x="304" y="875" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">IN+</text>

            <circle cx="310" cy="910" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="310" cy="910" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="304" y="905" text-anchor="end" font-size="5" font-weight="700" fill="var(--pin-text)">IN-</text>

            <circle cx="410" cy="880" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="410" cy="880" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="416" y="875" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">OUT+</text>

            <circle cx="410" cy="910" r="4" fill="var(--pad-fill)" stroke="var(--line)" stroke-width="1"/>
            <circle cx="410" cy="910" r="1.6" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
            <text x="416" y="905" text-anchor="start" font-size="5" font-weight="700" fill="var(--pin-text)">OUT-</text>
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
