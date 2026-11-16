import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("Manual_Montagem_Esteira_70cm.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ["function init3D", "const conveyorRoot", "let conveyorRoot", "var conveyorRoot", "function setViewMode"]):
        print(f"{i+1}: {l.strip()}")
