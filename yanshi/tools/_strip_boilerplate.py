# -*- coding: utf-8 -*-
"""清除解读区 sec-sub 里的模板句："每句/联/段/章（逐句）含注释（生僻字附读音）、译文与赏析，点击可展开。"
保留同段中的实质内容（全诗X句、分几部分、各联大意等）；整段清空则删除该 sec-sub。"""
import re, glob, subprocess

files = [l for l in subprocess.run(['grep','-l','点击可展开']+glob.glob('yanshi/*.html'),
         capture_output=True, text=True).stdout.splitlines()]
print(len(files), 'files')

BOIL = re.compile(r'[每逐][句联段章节]含(?:<b>[^<]*</b>)?[^<>]*?点击可展开\s*[。；；]?')

def clean_secsub(m):
    inner = m.group(2)
    if '点击可展开' not in inner:
        return m.group(0)
    t = BOIL.sub('', inner)
    t = re.sub(r'^[\s，、；]+', '', t)
    t = re.sub(r'[\s，、；]+$', '', t)
    if not t:
        return ''           # 整段删除
    return m.group(1) + t + m.group(3)

total = 0
for f in files:
    s = open(f, encoding='utf-8').read()
    s, n0 = re.subn(' data-page-node-id="[^"]*"', '', s)
    before = s.count('点击可展开')
    before_bal = s.count('<div') - s.count('</div>')
    before_bpair = s.count('<b') - s.count('</b>')
    s = re.sub(r'(<div class="sec-sub"[^>]*>)(.*?)(</div>)', clean_secsub, s, flags=re.S)
    after = s.count('点击可展开')
    if after != 0:
        print('WARN leftover in', f, after)
    # 校验：div 平衡与 <b> 开合差不变（<b>注释</b> 整对随模板句移除是合法的）
    assert s.count('<div') - s.count('</div>') == before_bal, f
    assert s.count('<b') - s.count('</b>') == before_bpair, f
    open(f, 'w', encoding='utf-8', newline='').write(s)
    total += 1
print('done', total)
