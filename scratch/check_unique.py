with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

blocks = [
    'bloco-e16-pg', 'bloco-e06-pg', 'bloco-e12a-pg', 'bloco-clamp-s1-pg',
    'bloco-clamp-s2-pg', 'bloco-e12b-pg', 'bloco-e08-pg', 'bloco-e09-pg',
    'bloco-q2-pg', 'bloco-e04-pg', 'bloco-m13-pg', 'bloco-e05-pg',
    'bloco-h05-pg', 'bloco-e25-pg', 'bloco-q1-pg'
]

for b in blocks:
    count = text.count(f'id="{b}"')
    print(f'{b}: {count} occurrence(s)')
