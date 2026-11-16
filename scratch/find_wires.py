import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find wires around E05, E09, M13, E06, H05, E16, Q1, Q2, E12A, E12B, E25
planta_start = text.find('id="planta-geral"')
planta_end = text.find('</svg>', planta_start)
planta_text = text[planta_start:planta_end]

for line in planta_text.splitlines():
    for target in ['E05', 'E09', 'M13', 'W057', 'W058', 'W073', 'W074', 'W075', 'W076', 'W050', 'W051', 'W052']:
        if target in line and ('<path' in line or '<polyline' in line or '<line' in line or 'data-wire' in line or 'wire-id' in line or 'W0' in line):
            sys.stdout.buffer.write((line.strip() + "\n").encode('utf-8'))
            break
