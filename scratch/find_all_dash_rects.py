import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

planta_start = text.find('id="planta-geral"')
planta_end = text.find('</svg>', planta_start)
planta_text = text[planta_start:planta_end]

lines = planta_text.splitlines()

for i, line in enumerate(lines):
    if '<rect' in line and any(k in line for k in ['dasharray', 'stroke-dasharray', 'rx=']):
        sys.stdout.buffer.write(f"Line in SVG: {line.strip()}\n".encode('utf-8'))
