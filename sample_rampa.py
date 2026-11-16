import json

with open('cad_data_preserved.json', 'r', encoding='utf-8') as f:
    cad_obj = json.load(f)

v = cad_obj['rampa']['verts']
# Sample vertices
for i in range(0, min(60, len(v)), 3):
    print(f"({v[i]:.1f}, {v[i+1]:.1f}, {v[i+2]:.1f})")
