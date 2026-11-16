import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

for b in ['bloco-e02-pg', 'bloco-e03-pg', 'bloco-e13-pg']:
    idx = text.find(f'id="{b}"')
    end_idx = text.find('</g>', idx) + 4
    print(f"=== {b} ===")
    print(text[idx:end_idx])
