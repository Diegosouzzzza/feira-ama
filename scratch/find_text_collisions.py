import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="planta-geral"')
svg_tag_start = text.rfind('<svg', 0, idx)
svg_tag_end = text.find('</svg>', idx)
planta = text[svg_tag_start:svg_tag_end]

# Extract all text elements with their x, y, anchor, font-size, content
text_matches = re.findall(r'<text\s+([^>]+)>([^<]+)</text>', planta)
sys.stdout.buffer.write(f"Total text elements found: {len(text_matches)}\n".encode('utf-8'))

parsed_texts = []
for attrs, content in text_matches:
    xm = re.search(r'x="([^"]+)"', attrs)
    ym = re.search(r'y="([^"]+)"', attrs)
    fsm = re.search(r'font-size="([^"]+)"', attrs)
    anc = re.search(r'text-anchor="([^"]+)"', attrs)
    if xm and ym:
        x = float(xm.group(1))
        y = float(ym.group(1))
        fs = float(fsm.group(1)) if fsm else 5.0
        anchor = anc.group(1) if anc else 'start'
        parsed_texts.append({'x': x, 'y': y, 'fs': fs, 'anchor': anchor, 'text': content.strip(), 'attrs': attrs})

# Let's find pairs of texts that are very close (e.g. abs(y1 - y2) < 6 and abs(x1 - x2) < 40)
collisions = []
for i in range(len(parsed_texts)):
    for j in range(i + 1, len(parsed_texts)):
        t1 = parsed_texts[i]
        t2 = parsed_texts[j]
        # Ignore if both are inside the notas block (y > 1300) unless identical y
        if t1['y'] > 1320 and t2['y'] > 1320:
            continue
        dy = abs(t1['y'] - t2['y'])
        dx = abs(t1['x'] - t2['x'])
        if dy < 5.5 and dx < 35:
            collisions.append((t1, t2, dx, dy))

sys.stdout.buffer.write(f"Potential text collisions detected: {len(collisions)}\n".encode('utf-8'))
for t1, t2, dx, dy in collisions:
    sys.stdout.buffer.write(f"  dx={dx:.1f}, dy={dy:.1f} | '{t1['text']}' (x={t1['x']}, y={t1['y']}) vs '{t2['text']}' (x={t2['x']}, y={t2['y']})\n".encode('utf-8'))
