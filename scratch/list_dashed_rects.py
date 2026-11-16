import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

planta_start = text.find('id="planta-geral"')
planta_end = text.find('</svg>', planta_start)
planta_text = text[planta_start:planta_end]

for line in planta_text.splitlines():
    if '<rect' in line and 'dasharray' in line:
        sys.stdout.buffer.write((line.strip() + "\n").encode('utf-8'))
