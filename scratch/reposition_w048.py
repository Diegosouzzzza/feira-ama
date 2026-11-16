import re
import sys
import xml.dom.minidom

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update W048 tag to y=655
old_w048 = """        <rect x="1801.0" y="475.5" width="22" height="8" rx="1.5" class="wire-tag"/>
        <text x="1812" y="481.5" text-anchor="middle" class="wire-label" font-size="5">W048</text>
        <text x="1812" y="490.5" text-anchor="middle" class="wire-spec" font-size="4.5">22AWG → W3</text>"""

new_w048 = """        <rect x="1801.0" y="650.5" width="22" height="8" rx="1.5" class="wire-tag"/>
        <text x="1812" y="656.5" text-anchor="middle" class="wire-label" font-size="5">W048</text>
        <text x="1812" y="665.5" text-anchor="middle" class="wire-spec" font-size="4.5">22AWG → W3</text>"""

if old_w048 in content:
    content = content.replace(old_w048, new_w048)
    print("Repositioned W048 tag to clear F2 3A area!")
else:
    print("Could not find old_w048")

with open(r'desenho-eletrico\esp32.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
