import sys

with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

target_ids = [
    'bloco-e01-pg',
    'bloco-x1-pg',
    'bloco-h04-pg'
]

lines = text.splitlines()

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
