import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'id="bloco-' in line:
        sys.stdout.buffer.write(f"{i+1}: {line.strip()[:100]}\n".encode('utf-8'))
