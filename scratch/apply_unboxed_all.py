import re
import sys
import xml.dom.minidom
from test_unboxed_all_bucks import unboxed_symbols

# Add unboxed X1 and X2
unboxed_symbols['bloco-x1-pg'] = """          <g id="bloco-x1-pg">
            <!-- X1 — Régua de Bornes de Potência DIN (SAK 6 Vias) — Totalmente Aberto -->
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

unboxed_symbols['bloco-x2-pg'] = """          <g id="bloco-x2-pg">
            <!-- X2 — Régua de Bornes de Sinais DIN (SAK 7 Vias) — Totalmente Aberto -->
            <text x="867" y="400" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">X2 — E17</text>
            <text x="867" y="410" text-anchor="middle" font-size="4.8" fill="var(--dim)">7 VIAS CAMPO</text>

            <line x1="867" y1="416" x2="867" y2="625" stroke="var(--line)" stroke-width="0.8" stroke-dasharray="2,2"/>

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

# Read original
with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make backup first
with open(r'desenho-eletrico\esp32_backup_pre_unboxed_all.html', 'w', encoding='utf-8') as f:
    f.write(content)

new_content = content
for block_id, new_block_svg in unboxed_symbols.items():
    pattern = rf'[ \t]*<g id="{block_id}">[\s\S]*?</g>'
    match = re.search(pattern, new_content)
    if not match:
        sys.stdout.buffer.write(f"ERROR: Could not find block {block_id}\n".encode('utf-8'))
        sys.exit(1)
    new_content = new_content[:match.start()] + new_block_svg + new_content[match.end():]
    sys.stdout.buffer.write(f"Replaced with unboxed symbol: {block_id}\n".encode('utf-8'))

# In bloco-h01-pg, remove the dashed border around firmware note
old_dashed_note = '<rect x="1135" y="645" width="160" height="55" rx="2" fill="none" stroke="var(--line-thin)" stroke-dasharray="2,2" stroke-width="0.8"/>'
if old_dashed_note in new_content:
    new_content = new_content.replace(old_dashed_note, '<!-- Firmware notes unboxed -->')
    sys.stdout.buffer.write(b"Removed inner dashed note box in ESP32 block!\n")

# Validate full Planta Geral SVG
planta_start = new_content.find('id="planta-geral"')
planta_start = new_content.rfind('<svg', 0, planta_start)
planta_end = new_content.find('</svg>', planta_start) + len('</svg>')
planta_svg = new_content[planta_start:planta_end]

try:
    xml.dom.minidom.parseString(planta_svg)
    sys.stdout.buffer.write(b"Planta Geral SVG parsed successfully with xml.dom.minidom! 100% Valid XML.\n")
except Exception as e:
    sys.stdout.buffer.write(f"XML Validation Error in Planta Geral: {e}\n".encode('utf-8'))
    sys.exit(1)

with open(r'desenho-eletrico\esp32.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

sys.stdout.buffer.write(b"SUCCESS: esp32.html successfully updated with ALL 16 unboxed schematic components!\n")
