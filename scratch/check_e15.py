import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="bloco-e15-pg"')
block = text[idx:idx+1500]
sys.stdout.buffer.write(block[:800].encode('utf-8'))
