import re
import xml.dom.minidom
import sys
from test_complete_symbols import all_symbols

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_content = content
for block_id, new_block_svg in all_symbols.items():
    pattern = rf'[ \t]*<g id="{block_id}">[\s\S]*?</g>'
    match = re.search(pattern, new_content)
    if not match:
        print(f"ERROR: Could not find block {block_id}")
        sys.exit(1)
    new_content = new_content[:match.start()] + new_block_svg + new_content[match.end():]
    print(f"Replaced: {block_id}")

# In bloco-h01-pg, change the firmware box fill="var(--pad-fill)" to fill="none"
old_h01_box = '<rect x="1135" y="645" width="160" height="55" rx="2" fill="var(--pad-fill)" stroke="var(--line-thin)"'
new_h01_box = '<rect x="1135" y="645" width="160" height="55" rx="2" fill="none" stroke="var(--line-thin)" stroke-dasharray="2,2"'
if old_h01_box in new_content:
    new_content = new_content.replace(old_h01_box, new_h01_box)
    print("Updated firmware note box in ESP32 to transparent background!")

# Validate Planta Geral SVG
planta_start = new_content.find('id="planta-geral"')
planta_start = new_content.rfind('<svg', 0, planta_start)
planta_end = new_content.find('</svg>', planta_start) + len('</svg>')
planta_svg = new_content[planta_start:planta_end]

try:
    xml.dom.minidom.parseString(planta_svg)
    print("Planta Geral SVG parsed successfully with xml.dom.minidom! 100% Valid XML.")
except Exception as e:
    print(f"XML Validation Error in Planta Geral: {e}")
    sys.exit(1)

with open(r'desenho-eletrico\esp32.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("SUCCESS: esp32.html successfully updated with ALL schematic symbols and transparent backgrounds!")
