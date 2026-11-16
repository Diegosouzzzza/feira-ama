import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="planta-geral"')
svg_tag_start = text.rfind('<svg', 0, idx)
svg_tag_end = text.find('</svg>', idx)
planta = text[svg_tag_start:svg_tag_end]

def print_section(tag_id):
    pattern = rf'<g id="{tag_id}">([\s\S]*?)</g>'
    m = re.search(pattern, planta)
    if m:
        sys.stdout.buffer.write(f"\n=================== {tag_id} ===================\n".encode('utf-8'))
        lines = m.group(1).strip().splitlines()
        for l in lines[:30]:
            sys.stdout.buffer.write((l + '\n').encode('utf-8'))
        if len(lines) > 30:
            sys.stdout.buffer.write(f"... ({len(lines)} total lines)\n".encode('utf-8'))

for gid in ['barramentos-pg', 'bloco-e26-bornes-pg', 'fios-pg', 'notas-pg', 'carimbo-pg']:
    print_section(gid)
