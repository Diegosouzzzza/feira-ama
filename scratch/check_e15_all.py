import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="bloco-e15-pg"')
end_idx = text.find('</g>', idx)
sys.stdout.buffer.write(text[idx:end_idx+4].encode('utf-8'))
