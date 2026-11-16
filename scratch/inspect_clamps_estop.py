import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="planta-geral"')
svg_tag_start = text.rfind('<svg', 0, idx)
svg_tag_end = text.find('</svg>', idx)
planta = text[svg_tag_start:svg_tag_end]

for bid in ['bloco-clamp-s1-pg', 'bloco-clamp-s2-pg', 'bloco-e12a-pg', 'bloco-e12b-pg']:
    m = re.search(rf'<g id="{bid}">([\s\S]*?)</g>', planta)
    if m:
        sys.stdout.buffer.write(f"\n=================== {bid} ===================\n".encode('utf-8'))
        sys.stdout.buffer.write(m.group(0).encode('utf-8'))
