import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

for bid in ['bloco-x1-pg', 'bloco-x2-pg']:
    m = re.search(rf'<g id="{bid}">([\s\S]*?)</g>', text)
    if m:
        sys.stdout.buffer.write(f"\n=== {bid} ===\n".encode('utf-8'))
        sys.stdout.buffer.write(m.group(0).encode('utf-8'))
