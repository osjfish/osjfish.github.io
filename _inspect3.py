import re, os
os.chdir(r'D:\App\Apps')
with open('beiying-zhuziqing.html','r',encoding='utf-8') as f:
    html=f.read()

# fulltext
ft_start = html.find('<div id="fulltext"')
ft_end = html.find('</div>', ft_start+100)
# find the actual closing
idx = ft_start
depth = 0
while idx < len(html):
    if html[idx:idx+5] == '<div ':
        depth += 1
    elif html[idx:idx+6] == '</div>':
        depth -= 1
        if depth == 0:
            ft_end = idx+6
            break
    idx += 1
print('=== FULLTEXT (first 2000) ===')
print(html[ft_start:ft_start+2000])
print('\n=== FULLTEXT last 500 ===')
print(html[ft_end-500:ft_end])

# Now find sections after jielu
for sec_id in ['app','acc','practice']:
    s = html.find(f'<section id="{sec_id}"')
    e = html.find('<section id=', s+10)
    if e == -1: e = html.find('</main>', s)
    print(f'\n=== SECTION #{sec_id} (first 1500) ===')
    print(html[s:s+1500])
