import re
import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="planta-geral"')
svg_tag_start = text.rfind('<svg', 0, idx)
svg_tag_end = text.find('</svg>', idx)
planta = text[svg_tag_start:svg_tag_end]

m_e08 = re.search(r'<g id="bloco-e08-pg">([\s\S]*?)</g>', planta)
if m_e08:
    sys.stdout.buffer.write(m_e08.group(0).encode('utf-8'))
