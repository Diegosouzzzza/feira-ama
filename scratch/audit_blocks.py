import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

p_start = text.find('id="planta-geral"')
p_end = text.find('</svg>', p_start)
planta = text[p_start:p_end]

blocks = re.findall(r'<g id="(bloco-[^"]+)">([\s\S]*?)</g>', planta)
sys.stdout.buffer.write(f"Total blocks found: {len(blocks)}\n".encode('utf-8'))

for bid, bcontent in blocks:
    rects = re.findall(r'<rect[^>]+>', bcontent)
    dashed = [r for r in rects if 'dasharray' in r or 'stroke-dasharray' in r]
    # filter out wire tags and small terminal/component elements
    sys.stdout.buffer.write(f"{bid}: {len(rects)} rects ({len(dashed)} dashed)\n".encode('utf-8'))
    for d in dashed:
        sys.stdout.buffer.write(f"   DASHED: {d[:120]}\n".encode('utf-8'))
