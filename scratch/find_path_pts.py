import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

planta_start = text.find('id="planta-geral"')
planta_end = text.find('</svg>', planta_start)
planta_text = text[planta_start:planta_end]

for line in planta_text.splitlines():
    if any(k in line for k in ['W057', 'W058', 'W073', 'W074', 'W060', 'W062', 'W064', '1965,670', '1995,670', '1730,295', '1730,345']):
        sys.stdout.buffer.write((line.strip() + "\n").encode('utf-8'))
