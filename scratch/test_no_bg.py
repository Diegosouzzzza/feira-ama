# Test removing background boxes from discrete and schematic symbols in esp32.html
import re

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect the exact lines of bloco-h05-pg, bloco-e25-pg, bloco-q1-pg, bloco-q2-pg, bloco-e12a-pg, bloco-e12b-pg, bloco-e16-pg, bloco-e08-pg, bloco-e04-pg
for b in ['bloco-h05-pg', 'bloco-e25-pg', 'bloco-q1-pg', 'bloco-q2-pg', 'bloco-e12a-pg', 'bloco-e12b-pg']:
    idx = text.find(f'id="{b}"')
    end_idx = text.find('</g>', idx) + 4
    print(f"=== {b} ===")
    print(text[idx:idx+400])
