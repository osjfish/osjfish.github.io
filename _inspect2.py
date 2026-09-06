import re, os
os.chdir(r'D:\App\Apps')
with open('beiying-zhuziqing.html','r',encoding='utf-8') as f:
    html=f.read()

# Find verse-list section
vl_start = html.find('<div class="verse-list"')
vl_end = html.find('</div>\n</section>', vl_start)
verse_section = html[vl_start:vl_end+20]
print('=== VERSE LIST (first 4000 chars) ===')
print(verse_section[:4000])
