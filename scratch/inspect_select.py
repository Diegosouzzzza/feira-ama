import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("Manual_Montagem_Esteira_70cm.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

def print_range(start, end, header=""):
    print(f"=== {header} ({start} to {end}) ===")
    for idx in range(start - 1, min(end, len(lines))):
        print(f"{idx+1}: {lines[idx]}", end="")
    print("\n")

print_range(2670, 2720, "SELECT COMPONENT")
