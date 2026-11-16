# -*- coding: utf-8 -*-
"""
Generator for Manual_Montagem_Esteira_70cm.html
AmazonVision 4.0 - XXI Feira Tecnologica FUCAPI 2026
"""

import sys, json

with open('cad_data_preserved.json', 'r', encoding='utf-8') as f:
    cad_json_str = f.read()

print("CAD data loaded successfully, size:", len(cad_json_str))
