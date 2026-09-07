# -*- coding: utf-8 -*-
import re, sys
path = sys.argv[1]
html = open(path, encoding='utf-8').read()

# Extract fulltext: between id="fulltext" and <div class="verse-list"
ft_start = html.index('id="fulltext"')
ft_end = html.index('<div class="verse-list"', ft_start)
ft_section = html[ft_start:ft_end]
ft_lines = re.findall(r'<div class="pl">([^<]+)</div>', ft_section)
ft_text = ''.join(ft_lines)
ft_text = re.sub(r'\s+', '', ft_text)

# Extract v-line from verseList
vl_start = html.index('id="verseList"')
vl_end = html.index('</section>', vl_start)
vl_section = html[vl_start:vl_end]
v_lines = re.findall(r'<div class="v-line">(.*?)</div>', vl_section, re.DOTALL)
def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s)
vl_text = ''.join(strip_tags(l) for l in v_lines)
vl_text = re.sub(r'\s+', '', vl_text)

print('MATCH:', vl_text == ft_text)
print('vl len:', len(vl_text), 'ft len:', len(ft_text))
print('ft lines:', len(ft_lines), 'v lines:', len(v_lines))
if vl_text != ft_text:
    for i,(a,b) in enumerate(zip(vl_text, ft_text)):
        if a != b:
            print(f'First diff at {i}')
            print(f'  vl: ...{vl_text[max(0,i-15):i+15]}...')
            print(f'  ft: ...{ft_text[max(0,i-15):i+15]}...')
            break
    if len(vl_text) != len(ft_text):
        print(f'  vl tail: {vl_text[-30:]}')
        print(f'  ft tail: {ft_text[-30:]}')
