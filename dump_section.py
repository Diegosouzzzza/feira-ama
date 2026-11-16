import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Manual_Montagem_Esteira_70cm.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start = int(sys.argv[1]) if len(sys.argv) > 1 else 600
end = int(sys.argv[2]) if len(sys.argv) > 2 else 945

for i in range(start - 1, min(end, len(lines))):
    print(f"{i+1:4d}: {lines[i]}", end='')
