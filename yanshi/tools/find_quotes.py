# -*- coding: utf-8 -*-
"""查找HTML中可见文本区域的英文直引号"""
f = open(r'D:\App\Apps\yanshi\huangdindexinzhuang-antusheng.html', encoding='utf-8').read()
lines = f.split('\n')
count = 0
for i, l in enumerate(lines):
    # Skip CSS, JS, HTML attribute lines
    if l.strip().startswith(('var ', '//', '/*', '*', '.', '#', ':', '@media')):
        continue
    if '<script' in l or '</script>' in l or '<style' in l or '</style>' in l:
        continue
    # Look for lines with visible text content and straight quotes
    if '"' in l and any(tag in l for tag in ['<p', 'v-trans', 'f-line', 'acc-d', 'acc-w', 'v-line', 'lead', 'pl>', 'd-body', 'fame-card', 'sec-sub', 'part-overview', 'box h3', 'media h4']):
        # Extract text between tags
        import re
        texts = re.findall(r'>([^<]+)<', l)
        for t in texts:
            if '"' in t:
                count += 1
                if count <= 20:
                    print(f'L{i+1}: {t.strip()[:100]}')
print(f'Total visible text lines with straight quotes: {count}')
