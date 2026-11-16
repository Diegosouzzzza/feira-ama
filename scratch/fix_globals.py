import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open("Manual_Montagem_Esteira_70cm.html", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add global variable declaration
old_decl = 'let dimensionsGroup, ghostBoxGroup, fruitMesh, ringLightMesh;'
new_decl = 'let dimensionsGroup, ghostBoxGroup, fruitMesh, ringLightMesh;\n    let bancaFeiraGroup, fairFloorMesh, conveyorApplesGroup, s0Cap;'
assert old_decl in text, "old_decl not found!"
text = text.replace(old_decl, new_decl, 1)

# 2. Inside fair 3D code, use the global variables instead of const
text = text.replace('const bancaFeiraGroup = new THREE.Group();', 'bancaFeiraGroup = new THREE.Group();', 1)
text = text.replace('const fairFloorMesh = makeSketchMesh(fairFloorGeo, 0xcbd5e1);', 'fairFloorMesh = makeSketchMesh(fairFloorGeo, 0xcbd5e1);', 1)
text = text.replace('const conveyorApplesGroup = new THREE.Group();', 'conveyorApplesGroup = new THREE.Group();', 1)
text = text.replace('const s0Cap = makeSketchMesh(new THREE.CylinderGeometry(22, 18, 18, 20), 0xdc2626);', 's0Cap = makeSketchMesh(new THREE.CylinderGeometry(22, 18, 18, 20), 0xdc2626);', 1)

with open("Manual_Montagem_Esteira_70cm.html", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated Manual_Montagem_Esteira_70cm.html with global declarations!")
