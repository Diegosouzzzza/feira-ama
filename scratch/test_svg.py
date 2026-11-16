import sys
with open(r'desenho-eletrico\esp32.html', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[12228:], start=12229):
    if 'W075' in l or 'W076' in l:
        sys.stdout.buffer.write(f"{i}: {l.strip()}\n".encode('utf-8'))
