import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'<g id="bloco-h01-pg">([\s\S]*?)</g>', text)
if m:
    lines = m.group(0).splitlines()
    for l in lines[:40]:
        sys.stdout.buffer.write((l + '\n').encode('utf-8'))
    sys.stdout.buffer.write(b"...\n")
    for l in lines[-25:]:
        sys.stdout.buffer.write((l + '\n').encode('utf-8'))
