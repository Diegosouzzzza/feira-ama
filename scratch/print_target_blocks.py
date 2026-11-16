import sys

with open(r'scratch\planta_blocks.txt', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

target_ids = [
    'bloco-e16-pg',
    'bloco-e06-pg',
    'bloco-e12a-pg',
    'bloco-clamp-s1-pg',
    'bloco-clamp-s2-pg',
    'bloco-e12b-pg',
    'bloco-e09-pg',
    'bloco-q2-pg',
    'bloco-m13-pg',
    'bloco-e05-pg',
    'bloco-h05-pg',
    'bloco-e25-pg',
    'bloco-q1-pg',
]

for target in target_ids:
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
