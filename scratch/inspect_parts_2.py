import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("Manual_Montagem_Esteira_70cm.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

def print_range(start, end, header=""):
    print(f"=== {header} ({start} to {end}) ===")
    for idx in range(start - 1, min(end, len(lines))):
        print(f"{idx+1}: {lines[idx]}", end="")
    print("\n")

print_range(2330, 2410, "PINS")
print_range(2565, 2620, "UPDATE PIN POSITIONS")
print_range(2715, 2770, "SET VIEW MODE")
print_range(2915, 2948, "RESTORE FULL ASSEMBLY VIEW")
