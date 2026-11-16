with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open(r'scratch\planta_blocks.txt', 'w', encoding='utf-8') as out:
    for i in range(12290, min(len(lines), 12930)):
        out.write(f"{i+1}: {lines[i]}")

print("Dumped lines 12291 to 12930")
