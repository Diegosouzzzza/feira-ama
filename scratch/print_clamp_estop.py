import sys

with open(r'scratch\planta_blocks.txt', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

def print_block(target):
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

print_block('bloco-clamp-s1-pg')
print_block('bloco-clamp-s2-pg')
print_block('bloco-e12b-pg')
