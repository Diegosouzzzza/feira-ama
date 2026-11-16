import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for i in range(13950, 14050):
    sys.stdout.buffer.write(f"Line {i}: {lines[i]}\n".encode('utf-8'))
