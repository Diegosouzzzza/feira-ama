import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="planta-geral"')
svg_tag_start = text.rfind('<svg', 0, idx)
svg_tag_end = text.find('</svg>', idx)
planta = text[svg_tag_start:svg_tag_end]

# Check bloco-e08-pg
m_e08 = re.search(r'<g id="bloco-e08-pg">([\s\S]*?)</g>', planta)
if m_e08:
    sys.stdout.buffer.write(b"=== bloco-e08-pg found ===\n")
    sys.stdout.buffer.write(m_e08.group(0)[:500].encode('utf-8'))
    sys.stdout.buffer.write(b"\n...\n")
else:
    sys.stdout.buffer.write(b"bloco-e08-pg NOT found!\n")

# Check S3
m_s3 = re.search(r'S3|REARME|RESET', planta)
sys.stdout.buffer.write(f"S3/REARME search: {'Found' if m_s3 else 'Not found'}\n".encode('utf-8'))

# Check W001-W087
wires = re.findall(r'W\d{3}', planta)
wires_unique = sorted(list(set(wires)))
sys.stdout.buffer.write(f"Total unique wires: {len(wires_unique)}, Max wire: {wires_unique[-1] if wires_unique else 'None'}\n".encode('utf-8'))
