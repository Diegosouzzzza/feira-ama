with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

# find tabs
for line in text.splitlines()[:500]:
    if 'tab' in line.lower() or 'planta' in line.lower():
        print(line[:120])
