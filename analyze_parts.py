import json

with open('cad_data_preserved.json', 'r', encoding='utf-8') as f:
    cad_obj = json.load(f)

for name, part in cad_obj.items():
    v = part['verts']
    xs = v[0::3]
    ys = v[1::3]
    zs = v[2::3]
    print(f"=== {name} ===")
    print(f"  X: [{min(xs):.2f}, {max(xs):.2f}], range: {max(xs)-min(xs):.2f}, center: {(max(xs)+min(xs))/2:.2f}")
    print(f"  Y: [{min(ys):.2f}, {max(ys):.2f}], range: {max(ys)-min(ys):.2f}, center: {(max(ys)+min(ys))/2:.2f}")
    print(f"  Z: [{min(zs):.2f}, {max(zs):.2f}], range: {max(zs)-min(zs):.2f}, center: {(max(zs)+min(zs))/2:.2f}")
