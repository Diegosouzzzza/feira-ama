import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

planta_start = text.find('id="planta-geral"')
planta_end = text.find('</svg>', planta_start)
planta_text = text[planta_start:planta_end]

for line in planta_text.splitlines():
    if '<g id="bloco-' in line:
        sys.stdout.buffer.write(f"\n{line.strip()}\n".encode('utf-8'))
    elif '<rect' in line and ('fill="var(--pad-fill)"' in line or 'fill="var(--bg)"' in line):
        sys.stdout.buffer.write(f"   {line.strip()[:100]}\n".encode('utf-8'))
