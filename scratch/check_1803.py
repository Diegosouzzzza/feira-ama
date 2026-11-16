import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for i, l in enumerate(lines):
    if '1803' in l or '1803.5' in l:
        sys.stdout.buffer.write(f"Line {i}: {l.strip()}\n".encode('utf-8'))
