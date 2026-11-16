import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for i, l in enumerate(lines):
    if '1812' in l or '1794' in l or 'W048' in l or 'W050' in l:
        if any(k in l for k in ['wire-tag', 'wire-label', 'wire-spec', 'path d=']):
            sys.stdout.buffer.write(f"Line {i}: {l.strip()}\n".encode('utf-8'))
