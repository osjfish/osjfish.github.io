import re, os, json
os.chdir(r'D:\App\Apps')

with open('beiying-zhuziqing.html','r',encoding='utf-8') as f:
    html=f.read()

# Extract style
m=re.search(r'<style>(.*?)</style>',html,re.S)
style=m.group(1)

# Extract scripts
scripts=re.findall(r'<script>(.*?)</script>',html,re.S)
script0=scripts[0]  # main framework + data
script1=scripts[1]  # likely init

# Save for reference
with open(r'D:\App\Apps\_beiying_style.css','w',encoding='utf-8') as f:
    f.write(style)
with open(r'D:\App\Apps\_beiying_script0.js','w',encoding='utf-8') as f:
    f.write(script0)
with open(r'D:\App\Apps\_beiying_script1.js','w',encoding='utf-8') as f:
    f.write(script1)

print('style saved:', len(style))
print('script0 saved:', len(script0))
print('script1 saved:', len(script1))

# Show body structure - find main sections
body_start=html.find('<body')
body=html[body_start:body_start+3000]
print('\n=== BODY START ===')
print(body[:2000])
