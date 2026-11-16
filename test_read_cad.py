# Script to generate Manual_Montagem_Esteira_70cm.html
# with 100% preservation of cad_data_preserved.json
import json

with open('cad_data_preserved.json', 'r', encoding='utf-8') as f:
    cad_json_str = f.read()

print("CAD JSON read successfully, bytes:", len(cad_json_str))
