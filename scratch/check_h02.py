import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="bloco-h02-pg"')
end_idx = text.find('</g>', idx) + 4
print(text[idx:end_idx])
