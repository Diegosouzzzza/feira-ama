import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Manual_Montagem_Esteira_70cm.html', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

print(f"Total lines: {len(lines)}")
for i, line in enumerate(lines):
    if i < 945:
        if any(k in line for k in ['<nav', 'class="tab', 'id="tab', '<h1', '<h2', '<h3', '<section', 'class="card']):
            print(f"L{i+1}: {line.strip()[:90]}")
    else:
        if any(k in line for k in ['function ', 'const ', 'let ', 'class ']) and ('CAD_DATA' not in line or 'const CAD_DATA' in line):
            print(f"L{i+1}: {line.strip()[:90]}")
