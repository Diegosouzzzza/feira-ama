import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

p_start = text.find('id="planta-geral"')
p_start = text.rfind('<svg', 0, p_start)
p_end = text.find('</svg>', p_start) + len('</svg>')
planta = text[p_start:p_end]

# 1. Extract all wire tags Wxxx
wires = re.findall(r'W\d{3}', planta)
wires_unique = sorted(list(set(wires)))
sys.stdout.buffer.write(f"Total unique wires found: {len(wires_unique)}\n".encode('utf-8'))
sys.stdout.buffer.write(f"Wires list: {wires_unique}\n\n".encode('utf-8'))

# 2. Extract all blocks
blocks = re.findall(r'<g id="(bloco-[^"]+)">([\s\S]*?)</g>', planta)
sys.stdout.buffer.write(f"Total blocks in Aba 3: {len(blocks)}\n".encode('utf-8'))
for bid, bcode in blocks:
    pins = re.findall(r'<circle[^>]+>', bcode)
    texts = re.findall(r'<text[^>]+>([^<]+)</text>', bcode)
    sys.stdout.buffer.write(f"Block: {bid} | Pins: {len(pins)} | Labels: {texts[:4]}\n".encode('utf-8'))

# 3. Check for any overlapping or potential wiring discrepancies
# Look at wire definitions and polyline/path/line in the schematic
lines = re.findall(r'<(line|polyline|path)[^>]+>', planta)
sys.stdout.buffer.write(f"\nTotal wire segments (line/polyline/path): {len(lines)}\n".encode('utf-8'))
