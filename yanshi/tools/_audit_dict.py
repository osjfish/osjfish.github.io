# -*- coding: utf-8 -*-
"""按 SKILL §4.2/§4.3 审计全库 DICT_WORDS / DICT_NOTES。
兼容两种数据形态：
  A) 单行 JSON：var DICT_WORDS = [{"w":"..","py":"..","q":"..","tip":".."}, ...];
  B) 逐行单引号：var DICT_WORDS = [\n  {w:'..', py:'..', q:'..', tip:'..'},\n ...];
规则：不泄题 / □数=字数 / 音节数=字数或1 / tip 有区分度 / 注释题显示所在句。
"""
import os, re, io, sys, json, collections

ROOT = r'D:\App\Apps\yanshi'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PAIR = re.compile(r"(\w+):\s*'([^']*)'")


def parse_array(src, name):
    """返回 (list[dict], fmt) ；解析失败返回 ([], None)"""
    m = re.search(r'var\s+' + name + r'\s*=\s*(\[.*?\])\s*;', src, re.S)
    if not m:
        return [], None
    raw = m.group(1).strip()
    if '"w"' in raw or '{"w"' in raw:
        # A) JSON 单行
        try:
            return json.loads(raw), 'json'
        except Exception:
            fixed = re.sub(r',\s*\]', ']', raw)
            try:
                return json.loads(fixed), 'json'
            except Exception as e:
                return [], 'json-err'
    # B) 逐行单引号
    items = []
    for line in raw.splitlines():
        line = line.strip().rstrip(',')
        if not line.startswith('{'):
            continue
        d = dict(PAIR.findall(line))
        if 'w' in d:
            items.append(d)
    return items, 'sq'


files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html'))
leak, blankmis, sylmis, tipweak, notes_bad, dup = [], [], [], [], [], []
fmtcnt = collections.Counter()
cw = cn = 0
per_file = {}

for f in files:
    src = open(os.path.join(ROOT, f), encoding='utf-8').read()
    W, fw = parse_array(src, 'DICT_WORDS')
    N, fn = parse_array(src, 'DICT_NOTES')
    fmtcnt[('W', fw)] += 1
    fmtcnt[('N', fn)] += 1
    cw += len(W)
    cn += len(N)
    per_file[f] = (len(W), len(N))
    seen = set()
    probs = 0
    for it in W:
        w = it.get('w', ''); py = it.get('py', ''); q = it.get('q', ''); tip = it.get('tip', '')
        nblank = q.count('□')
        q_nb = q.replace('□', '')
        hit = [c for c in w if c and c in q_nb]
        if hit:
            leak.append((f, w, py, q, tip, ''.join(hit))); probs += 1
        if nblank != len(w):
            blankmis.append((f, w, py, q, tip, '%d≠%d' % (nblank, len(w)))); probs += 1
        nsyl = len([s for s in re.split(r'\s+', py.strip()) if s])
        if nsyl not in (len(w), 1) and len(w) > 0:
            sylmis.append((f, w, py, q, tip, '%d≠%d' % (nsyl, len(w)))); probs += 1
        bare = re.sub(r'[「」《》（）()\s，。、；：]', '', tip)
        if not bare or bare == w or set(bare) <= set(w):
            tipweak.append((f, w, py, q, tip, '无区分度')); probs += 1
        key = (w, q)
        if key in seen:
            dup.append((f, w, q, tip, '', '重复')); probs += 1
        seen.add(key)
    for it in N:
        w = it.get('w', ''); q = it.get('q', ''); a = it.get('a', '')
        wbase = re.sub(r'\(.*?\)', '', w)
        if not q.strip() or not a.strip():
            notes_bad.append((f, w, q, a, '', '空 q/a')); probs += 1
        elif wbase and wbase not in q:
            notes_bad.append((f, w, q, a, '', '被考词未在句中(q 可能是章节名)')); probs += 1

print('格式分布:', dict(fmtcnt))
print('DICT_WORDS 条目 =', cw, ' DICT_NOTES 条目 =', cn, ' 文件数 =', len(files))
print()
print('【1】泄题（答案字出现在题句里）:', len(leak))
for x in leak:
    print('   %-40s w=%-6s q=%-26s 泄露=%s' % (x[0], x[1], x[3], x[5]))
print()
print('【2】□数≠字数:', len(blankmis))
for x in blankmis[:30]:
    print('   %-40s w=%-6s q=%-26s %s' % (x[0], x[1], x[3], x[5]))
print()
print('【3】音节数≠字数且≠1:', len(sylmis))
for x in sylmis[:30]:
    print('   %-40s w=%-6s py=%-16s %s' % (x[0], x[1], x[2], x[5]))
print()
print('【4】tip 无区分度:', len(tipweak))
for x in tipweak[:30]:
    print('   %-40s w=%-6s tip=%s' % (x[0], x[1], x[4]))
print()
print('【5】重复条目:', len(dup))
for x in dup[:15]:
    print('   %-40s w=%-6s q=%s' % (x[0], x[1], x[2]))
print()
print('【6】注释题异常（空/被考词未出现）:', len(notes_bad))
byf = collections.Counter(x[0] for x in notes_bad)
for f_, c in byf.most_common(12):
    print('   %-40s %d 条' % (f_, c))

json.dump({'leak': leak, 'blankmis': blankmis, 'sylmis': sylmis,
           'tipweak': tipweak, 'dup': dup, 'notes': notes_bad, 'per_file': per_file},
          open(os.path.join(ROOT, 'tools', '_dict_audit.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
