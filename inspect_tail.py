import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Manual_Montagem_Esteira_70cm.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1720, len(lines)):
    print(f"{i+1:4d}: {lines[i]}", end='')
