import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("Manual_Montagem_Esteira_70cm.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx in range(3720, 3745):
    print(f"{idx+1}: {lines[idx]}", end="")
