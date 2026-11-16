import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("Manual_Montagem_Esteira_70cm.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

keywords = [
    "tab-btn", "setViewMode", "makeSketchMesh", "pinAnchors",
    "updatePinPositions", "applyExplosion", "runFullCycle",
    "triggerPusherTest", "toggleBeltMotor", "setTheme",
    "conveyorRoot", "cards", "card-title", "restoreFullAssemblyView"
]

for i, line in enumerate(lines):
    for k in keywords:
        if k in line:
            print(f"{i+1}: {line.strip()[:110]}")
            break
