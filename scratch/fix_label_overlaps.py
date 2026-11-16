import re
import sys
import xml.dom.minidom

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. E15 header texts
old_e15_head = """            <text x="225" y="278" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E15 — DISJ. 2P</text>
            <text x="225" y="287" text-anchor="middle" font-size="4.8" fill="var(--dim)">10A CURVA C (IEC 60898)</text>"""

new_e15_head = """            <text x="225" y="272" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--fg)">E15 — DISJ. 2P</text>
            <text x="225" y="280" text-anchor="middle" font-size="4.8" fill="var(--dim)">10A CURVA C (IEC 60898)</text>"""

if old_e15_head in content:
    content = content.replace(old_e15_head, new_e15_head)
    print("Fixed E15 header text overlap!")
else:
    print("Could not find exact old_e15_head")

# 2. W041 tag
old_w041 = """        <rect x="1074.0" y="503.5" width="20" height="8" rx="1.5" class="wire-tag"/>
        <text x="1084" y="509.5" text-anchor="middle" class="wire-label" font-size="5">W041</text>
        <text x="1084" y="518.5" text-anchor="middle" class="wire-spec" font-size="4.5">JMP → W2</text>"""

new_w041 = """        <rect x="1068.0" y="488.5" width="20" height="8" rx="1.5" class="wire-tag"/>
        <text x="1078" y="494.5" text-anchor="middle" class="wire-label" font-size="5">W041</text>
        <text x="1078" y="503.5" text-anchor="middle" class="wire-spec" font-size="4.5">JMP → W2</text>"""

if old_w041 in content:
    content = content.replace(old_w041, new_w041)
    print("Fixed W041 wire tag overlap with GPIO27!")
else:
    print("Could not find exact old_w041")

# 3. W048 tag
old_w048_pattern = r'<rect x="1801\.0" y="435\.5" width="22" height="8" rx="1\.5" class="wire-tag"/>\s*<text x="1812" y="441\.5" text-anchor="middle" class="wire-label" font-size="5">W048</text>\s*<text x="1812" y="450\.5" text-anchor="middle" class="wire-spec" font-size="4\.5">22AWG → W3</text>'
new_w048 = """<rect x="1801.0" y="475.5" width="22" height="8" rx="1.5" class="wire-tag"/>
        <text x="1812" y="481.5" text-anchor="middle" class="wire-label" font-size="5">W048</text>
        <text x="1812" y="490.5" text-anchor="middle" class="wire-spec" font-size="4.5">22AWG → W3</text>"""

if re.search(old_w048_pattern, content):
    content = re.sub(old_w048_pattern, new_w048, content)
    print("Fixed W048 wire tag overlap with W050!")
else:
    print("Could not find exact old_w048")

# 4. K1 Polo 2 Selo text
old_selo = '<text x="1486" y="350" text-anchor="start" font-size="3.6" font-weight="700" fill="var(--fg)">K1 POLO 2 · SELO</text>'
new_selo = '<text x="1512" y="348" text-anchor="start" font-size="3.6" font-weight="700" fill="var(--fg)">K1 POLO 2 · SELO</text>'
if old_selo in content:
    content = content.replace(old_selo, new_selo)
    print("Fixed K1 Polo 2 Selo text placement!")

# Validate XML
planta_start = content.find('id="planta-geral"')
planta_start = content.rfind('<svg', 0, planta_start)
planta_end = content.find('</svg>', planta_start) + len('</svg>')
planta_svg = content[planta_start:planta_end]

try:
    xml.dom.minidom.parseString(planta_svg)
    print("Planta Geral SVG XML is 100% Valid!")
except Exception as e:
    print(f"XML error: {e}")
    sys.exit(1)

with open(r'desenho-eletrico\esp32.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: esp32.html updated and verified!")
