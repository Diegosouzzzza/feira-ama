import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for i, l in enumerate(lines):
    if 'W084' in l or 'SELO' in l:
        sys.stdout.buffer.write(f"Line {i}: {l.strip()[:140]}\n".encode('utf-8'))
