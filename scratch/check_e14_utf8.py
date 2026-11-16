import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="bloco-e14-pg"')
end_idx = text.find('</g>', idx) + 4
sys.stdout.buffer.write(text[idx:end_idx].encode('utf-8'))
