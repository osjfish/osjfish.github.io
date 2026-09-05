# -*- coding: utf-8 -*-
import re
src = open(r'D:\App\Apps\hongmenyan-shiji.html', encoding='utf-8').read()
# Find practice buttons
m = re.search(r'<section id="practice".*?</section>', src, re.S)
print(m.group()[:1500] if m else 'not found')
print('---BUTTONS---')
for m in re.finditer(r'data-mode="(note|word)"[^>]*>([^<]+)<', src):
    print(m.group(1), '|', m.group(2))
print('---LOCALSTORAGE---')
for m in re.finditer(r'localStorage[^;]+', src):
    print(m.group()[:80])
