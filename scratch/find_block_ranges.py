import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

blocks_to_find = [
    'bloco-e16-pg',
    'bloco-e06-pg',
    'bloco-e12a-pg',
    'bloco-clamp-s1-pg',
    'bloco-clamp-s2-pg',
    'bloco-e12b-pg',
    'bloco-e08-pg',
    'bloco-e09-pg',
    'bloco-q2-pg',
    'bloco-e04-pg',
    'bloco-m13-pg',
    'bloco-e05-pg',
    'bloco-h05-pg',
    'bloco-e25-pg',
    'bloco-q1-pg'
]

ranges = {}
for name in blocks_to_find:
    start_idx = None
    end_idx = None
    depth = 0
    for i, line in enumerate(lines):
        if f'id="{name}"' in line:
            start_idx = i
            depth = 0
        if start_idx is not None and i >= start_idx:
            depth += line.count('<g')
            depth -= line.count('</g>')
            if depth <= 0:
                end_idx = i
                break
    ranges[name] = (start_idx, end_idx)
    sys.stdout.buffer.write(f"{name}: lines {start_idx+1} to {end_idx+1} (count {end_idx - start_idx + 1})\n".encode('utf-8'))
