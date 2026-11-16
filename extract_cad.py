import json

with open('Manual_Montagem_Esteira_70cm.html', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = 'const CAD_DATA = '
idx_start = text.find(prefix)
if idx_start == -1:
    print("ERROR: CAD_DATA not found")
    exit(1)

idx_json_start = idx_start + len(prefix)
idx_end = text.find(';\n', idx_json_start)
if idx_end == -1:
    idx_end = text.find(';', idx_json_start)

cad_json_str = text[idx_json_start:idx_end].strip()
print(f"Extracted CAD_DATA length: {len(cad_json_str)}")

cad_obj = json.loads(cad_json_str)
print("Keys:", list(cad_obj.keys()))
for k in cad_obj:
    print(f"{k}: verts={len(cad_obj[k]['verts'])}, indices={len(cad_obj[k]['indices'])}")

# Save to a dedicated file for 100% preservation
with open('cad_data_preserved.json', 'w', encoding='utf-8') as f:
    f.write(cad_json_str)
print("Successfully saved cad_data_preserved.json")
