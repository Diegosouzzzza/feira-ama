import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/test_manual.html", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'<nav class="tab-bar">(.*?)</nav>', text, re.DOTALL)
if m:
    print(m.group(0))
