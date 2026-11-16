# -*- coding: utf-8 -*-
"""
Builder script that generates the complete Manual_Montagem_Esteira_70cm.html
"""
import sys, json

with open('cad_data_preserved.json', 'r', encoding='utf-8') as f:
    cad_json = f.read()

print("CAD JSON read, length:", len(cad_json))
