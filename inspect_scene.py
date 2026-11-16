import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Manual_Montagem_Esteira_70cm.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1045, 1460):
    l = lines[i]
    if any(k in l for k in ['components[', 'new THREE.', 'Group()', 'makeSketchMesh', 'buildCADBufferGeometry', 'position.set', 'rotation.']):
        print(f"{i+1:4d}: {l.strip()[:100]}")
