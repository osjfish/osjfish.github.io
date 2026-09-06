import re, os
os.chdir(r'D:\App\Apps')
with open('beiying-zhuziqing.html','r',encoding='utf-8') as f:
    html=f.read()

# Find iframe
ifs = re.findall(r'<iframe[^>]*>', html)
for f in ifs:
    print(f)
print()
# Find media section HTML (not CSS)
idx = html.find('<div class="box media-box">')
print(html[idx:idx+800])
