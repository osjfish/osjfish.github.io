# -*- coding: utf-8 -*-
import io,re,json
p='hetang-yuese-zhuziqing.html'
h=io.open(p,encoding='utf-8').read()
print('size',len(h))
need=['id="fulltext"','id="verseList"','id="btnAll"','id="btnRecite"','id="btnPrint"','id="fsSel"','id="btnShowAll"',
      'id="dictate"','id="annoPopup"','class="wrap"','class="nav-in"','id="topBtn"','id="mediaF1"','id="mediaF2"']
for n in need:
    print(('OK  ' if n in h else 'MISS'),n)
print('leftover [[ :', h.count('[['))
# 英文引号：检查文本节点
texts=re.findall(r'>([^<>]+)<',h)
bad=[t for t in texts if '"' in t]
print('text nodes with straight quote:',len(bad),bad[:5])
# 注释覆盖
verses=re.findall(r'<div class="verse" id="l\d+" data-i="\d+">.*?(?=<div class="verse" |</div>\s*</section>|$)',h,re.S)
print('verse blocks:',len(verses))
empty=[i+1 for i,v in enumerate(verses) if 'anno-word' not in v]
print('verses without annotation:',empty)
print('anno-word count:',h.count('anno-word'))
print('details count:',h.count('class="v-more"'))
print('part-head:',h.count('part-head'),'part-overview:',h.count('part-overview'))
# 题库
w=json.loads(re.search(r'var DICT_WORDS = (\[.*?\]);',h,re.S).group(1))
n=json.loads(re.search(r'var DICT_NOTES = (\[.*?\]);',h,re.S).group(1))
print('words',len(w),'notes',len(n))
# 字形题自检：①答案字不能在例句中出现（泄题）②□数=答案字数 ③拼音音节数=答案字数
leak=[x for x in w if any(c in x['q'] for c in x['w'])]
print('LEAK(答案出现在例句):',[(x['w'],x['q']) for x in leak])
nbox=[x for x in w if x['q'].count('\u25a1')!=len(x['w'])]
print('BOX数不匹配:',[(x['w'],x['q']) for x in nbox])
npy=[x for x in w if len(x['py'].split())!=len(x['w']) and len(x['py'].split())!=1]
print('拼音音节数不匹配:',[(x['w'],x['py']) for x in npy])
print('tip缺失或与答案重复:',[x['w'] for x in w if not x.get('tip') or x['tip']==x['w']])
print('notes missing field:',[x for x in n if not(x.get('w') and x.get('a') and x.get('q'))])
# 背诵全文段数
print('fulltext pl:',h[h.index('id="fulltext"'):h.index('id="verseList"')].count('class="pl"'))
# 中文引号配对
print('left quote',h.count('\u201c'),'right quote',h.count('\u201d'))
