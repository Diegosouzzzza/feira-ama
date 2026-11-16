import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

planta_start = text.find('id="planta-geral"')
planta_end = text.find('</svg>', planta_start)
planta_text = text[planta_start:planta_end]

for line in planta_text.splitlines():
    if any(k in line for k in ['clamp-s1', 'clamp-s2', 'E10', 'E11', 'BAT54S', '965', '1041', '1052']):
        sys.stdout.buffer.write((line.strip() + "\n").encode('utf-8'))
