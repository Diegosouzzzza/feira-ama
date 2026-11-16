import sys

with open(r'scratch\planta_blocks.txt', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

specific_targets = [
    'bloco-e05-pg',
    'bloco-e09-pg',
    'bloco-m13-pg',
    'bloco-q2-pg',
    'bloco-clamp-s1-pg',
    'bloco-clamp-s2-pg',
    'bloco-e12b-pg',
    'bloco-e04-pg',
    'bloco-e08-pg'
]

for target in specific_targets:
    sys.stdout.buffer.write(f"\n==================== {target} ====================\n".encode('utf-8'))
    recording = False
    depth = 0
    for l in lines:
        if f'id="{target}"' in l:
            recording = True
        if recording:
            sys.stdout.buffer.write((l + "\n").encode('utf-8'))
            if '<g' in l:
                depth += l.count('<g')
            if '</g>' in l:
                depth -= l.count('</g>')
                if depth <= 0:
                    break
