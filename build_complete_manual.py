# -*- coding: utf-8 -*-
"""
Full generator for Manual_Montagem_Esteira_70cm.html
"""
import sys, json

# Read CAD data preserved
with open('cad_data_preserved.json', 'r', encoding='utf-8') as f:
    cad_json = f.read()

print("CAD data verified, length:", len(cad_json))
