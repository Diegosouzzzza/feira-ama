import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="planta-geral"')
svg_tag_start = text.rfind('<svg', 0, idx)
svg_tag_end = text.find('</svg>', idx)
planta = text[svg_tag_start:svg_tag_end]

lines = planta.splitlines()
for i, l in enumerate(lines):
    if 'S3' in l or 'RESET' in l:
        sys.stdout.buffer.write(f"Line {i}: {l.strip()[:140]}\n".encode('utf-8'))
