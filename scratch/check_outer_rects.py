import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

p_start = text.find('id="planta-geral"')
p_end = text.find('</svg>', p_start)
planta = text[p_start:p_end]

blocks = re.findall(r'<g id="(bloco-[^"]+)">([\s\S]*?)</g>', planta)

for bid, bcontent in blocks:
    # check if first element after comment is a rect enclosing the block
    rects = re.findall(r'<rect\s+([^>]+)>', bcontent)
    outer = []
    for r in rects:
        # check width/height
        wm = re.search(r'width="([^"]+)"', r)
        hm = re.search(r'height="([^"]+)"', r)
        if wm and hm:
            w = float(wm.group(1))
            h = float(hm.group(1))
            if w >= 40 and h >= 40:
                outer.append((w, h, r))
    if outer:
        sys.stdout.buffer.write(f"\n{bid}:\n".encode('utf-8'))
        for w, h, r in outer:
            sys.stdout.buffer.write(f"   w={w}, h={h}: <rect {r[:80]}...>\n".encode('utf-8'))
