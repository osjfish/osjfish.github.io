import re, os
os.chdir(r'D:\App\Apps')

for fn in ['beiying-zhuziqing.html','zixinli.html']:
    with open(fn,'r',encoding='utf-8') as f:
        html=f.read()
    print(f'\n===== {fn} =====')
    print(f'total length: {len(html)}')
    m=re.search(r'<style>(.*?)</style>',html,re.S)
    print(f'style length: {len(m.group(1)) if m else 0}')
    scripts=re.findall(r'<script[^>]*>(.*?)</script>',html,re.S)
    print(f'scripts count: {len(scripts)}')
    for i,s in enumerate(scripts):
        print(f'  script[{i}] length:{len(s)} src? {"src" in s[:50]}')
    for kid in ['verseList','fulltext','btnAll','btnRecite','btnPrint','btnShowAll','fsSel','annoPopup','dictate','topBtn','mediaF1','mediaF2']:
        print(f'  {kid}: {kid in html}')
    print('  DICT_WORDS:', 'DICT_WORDS' in html)
    print('  DICT_NOTES:', 'DICT_NOTES' in html)
    lsk=re.findall(r"localStorage(?:\.getItem|\[)[\"']?(\w+)", html)
    print('  localStorage keys:', set(lsk))
