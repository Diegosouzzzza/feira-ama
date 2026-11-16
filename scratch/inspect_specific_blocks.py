import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="planta-geral"')
svg_tag_start = text.rfind('<svg', 0, idx)
svg_tag_end = text.find('</svg>', idx)
planta = text[svg_tag_start:svg_tag_end]

def print_block(bid):
    m = re.search(rf'<g id="{bid}">([\s\S]*?)</g>', planta)
    if m:
        sys.stdout.buffer.write(f"\n=================== {bid} ===================\n".encode('utf-8'))
        sys.stdout.buffer.write(m.group(0).encode('utf-8'))
        sys.stdout.buffer.write(b"\n")

for bid in ['bloco-e08-pg', 'bloco-e16-pg', 'bloco-clamp-s1-pg', 'bloco-h02-pg', 'bloco-e04-pg', 'bloco-m13-pg']:
    print_block(bid)
