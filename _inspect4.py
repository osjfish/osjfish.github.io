import re, os
os.chdir(r'D:\App\Apps')
with open('beiying-zhuziqing.html','r',encoding='utf-8') as f:
    html=f.read()

# media section
ms = html.find('media-box')
print('=== MEDIA BOX ===')
print(html[ms-200:ms+1200])

# dictate actions
da = html.find('dictate-actions')
print('\n=== DICTATE ACTIONS + END ===')
print(html[da:da+800])

# Check CSS for acc-sub
print('\n=== acc-sub in CSS? ===', '.acc-sub' in html)
print('=== part-head h3 CSS ===')
ph = html.find('.part-head h3')
print(html[ph:ph+200] if ph>=0 else 'not found')

# Check data-fs CSS
dfs = html.find('body[data-fs')
print('\n=== data-fs rules ===')
while dfs >= 0:
    print(html[dfs:dfs+80])
    dfs = html.find('body[data-fs', dfs+1)
