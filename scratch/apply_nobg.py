import re
import xml.dom.minidom
import sys
from validate_nobg import new_blocks

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_content = content
for block_id, new_block_svg in new_blocks.items():
    pattern = rf'[ \t]*<g id="{block_id}">[\s\S]*?</g>'
    match = re.search(pattern, new_content)
    if not match:
        print(f"ERROR: Could not find block {block_id}")
        sys.exit(1)
    new_content = new_content[:match.start()] + new_block_svg + new_content[match.end():]
    print(f"Replaced: {block_id}")

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

print("SUCCESS: esp32.html successfully updated with transparent background schematic symbols!")
