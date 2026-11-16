import json

with open('cad_data_preserved.json', 'r', encoding='utf-8') as f:
    cad_obj = json.load(f)

v = cad_obj['rampa']['verts']
# Check points near min Y and max Y
bottom_pts = []
top_pts = []
for i in range(0, len(v), 3):
    x, y, z = v[i], v[i+1], v[i+2]
    if y < 10:
        bottom_pts.append((x, y, z))
    elif y > 110:
        top_pts.append((x, y, z))

print(f"Rampa: {len(bottom_pts)} points near Y=0, {len(top_pts)} points near Y=120")
if bottom_pts:
    print("Bottom pts Z range:", min(p[2] for p in bottom_pts), max(p[2] for p in bottom_pts))
if top_pts:
    print("Top pts Z range:", min(p[2] for p in top_pts), max(p[2] for p in top_pts))
