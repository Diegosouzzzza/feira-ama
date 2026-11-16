with open(r'desenho-eletrico\esp32.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('class="tab-bar"')
print(text[idx:idx+1500])
