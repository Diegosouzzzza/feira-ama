import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="planta-geral"')
svg_tag_start = text.rfind('<svg', 0, idx)
svg_tag_end = text.find('</svg>', idx)

planta = text[svg_tag_start:svg_tag_end]

g_ids = re.findall(r'<g id="([^"]+)"', planta)
sys.stdout.buffer.write(f"Total <g id='...'> in planta-geral: {len(g_ids)}\n".encode('utf-8'))
for gid in g_ids:
    sys.stdout.buffer.write(f"  - {gid}\n".encode('utf-8'))
