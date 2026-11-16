import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="planta-geral"')
svg_tag_start = text.rfind('<svg', 0, idx)
svg_tag_end = text.find('</svg>', idx)
planta = text[svg_tag_start:svg_tag_end]

# Only look in schematic groups:
schematic_groups = [
    'barramentos-pg', 'bloco-e19-pg', 'bloco-e27-pe-pg', 'bloco-e15-pg',
    'bloco-e01-pg', 'bloco-e16-pg', 'bloco-x1-pg', 'bloco-e02-pg',
    'bloco-e06-pg', 'bloco-e03-pg', 'bloco-h04-pg', 'bloco-e07-pg',
    'bloco-e12a-pg', 'bloco-x2-pg', 'bloco-e26-bornes-pg', 'bloco-clamp-s1-pg',
    'bloco-clamp-s2-pg', 'bloco-h01-pg', 'bloco-e14-pg', 'bloco-e12b-pg',
    'bloco-e08-pg', 'bloco-e09-pg', 'bloco-q2-pg', 'bloco-h02-pg',
    'bloco-e04-pg', 'bloco-m13-pg', 'bloco-e05-pg', 'bloco-h05-pg',
    'bloco-e25-pg', 'bloco-q1-pg', 'bloco-e13-pg', 'fios-pg'
]

parsed_texts = []
for gid in schematic_groups:
    m = re.search(rf'<g id="{gid}">([\s\S]*?)</g>', planta)
    if m:
        t_matches = re.findall(r'<text\s+([^>]+)>([^<]+)</text>', m.group(1))
        for attrs, content in t_matches:
            xm = re.search(r'x="([^"]+)"', attrs)
            ym = re.search(r'y="([^"]+)"', attrs)
            fsm = re.search(r'font-size="([^"]+)"', attrs)
            anc = re.search(r'text-anchor="([^"]+)"', attrs)
            if xm and ym:
                x = float(xm.group(1))
                y = float(ym.group(1))
                fs = float(fsm.group(1)) if fsm else 5.0
                anchor = anc.group(1) if anc else 'start'
                parsed_texts.append({'gid': gid, 'x': x, 'y': y, 'fs': fs, 'anchor': anchor, 'text': content.strip(), 'attrs': attrs})

sys.stdout.buffer.write(f"Total schematic text elements: {len(parsed_texts)}\n".encode('utf-8'))

# Check real overlap: dy < 6 and dx < text_len * fs * 0.4
collisions = []
for i in range(len(parsed_texts)):
    for j in range(i + 1, len(parsed_texts)):
        t1 = parsed_texts[i]
        t2 = parsed_texts[j]
        dy = abs(t1['y'] - t2['y'])
        dx = abs(t1['x'] - t2['x'])
        # check if they really overlap based on anchors and lengths
        if dy < 6:
            # estimate width
            w1 = len(t1['text']) * t1['fs'] * 0.6
            w2 = len(t2['text']) * t2['fs'] * 0.6
            # check distance
            if dx < (w1 + w2) / 2:
                collisions.append((t1, t2, dx, dy))

sys.stdout.buffer.write(f"Detected {len(collisions)} schematic collisions:\n".encode('utf-8'))
for t1, t2, dx, dy in collisions:
    sys.stdout.buffer.write(f"[{t1['gid']}] '{t1['text']}' @ ({t1['x']}, {t1['y']}) <--> [{t2['gid']}] '{t2['text']}' @ ({t2['x']}, {t2['y']}) (dx={dx:.1f}, dy={dy:.1f})\n".encode('utf-8'))
