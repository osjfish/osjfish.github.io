# -*- coding: utf-8 -*-
import re, json

for f in ['yuwosuoyuye-mengzi.html', 'songdongyangmashengxu-songlian.html']:
    h = open(f, encoding='utf-8').read()
    print(f"=== {f} ===")
    body = h[h.index('<body'):]
    body_ns = re.sub(r'<script>.*?</script>', '', body, flags=re.S)
    body_ns = re.sub(r'<style>.*?</style>', '', body_ns, flags=re.S)
    straight = body_ns.count('"')
    print(f"  straight double quotes in body (excl scripts): {straight}")

    # pinyin in visible v-line text
    vlines = re.findall(r'<div class="v-line">(.*?)</div>', body_ns, re.S)
    pinyin_in_text = 0
    for vl in vlines:
        clean = re.sub(r'<span[^>]*data-note="[^"]*">([^<]*)</span>', r'\1', vl)
        if re.search(r'[（(][a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]+[）)]', clean):
            pinyin_in_text += 1
            print(f"    PINYIN LEAK: {clean[:60]}")
    print(f"  v-lines with pinyin in visible text: {pinyin_in_text}")

    # required IDs
    for id_ in ['verseList', 'fulltext', 'btnAll', 'btnRecite', 'btnPrint', 'annoPopup', 'dictate']:
        if f'id="{id_}"' not in h:
            print(f"  MISSING id={id_}")
        else:
            pass
    print("  all required IDs present")

    # localStorage key
    key = 'yuwosuoyuye_fs' if 'yuwosuoyuye' in f else 'songdongyang_fs'
    print(f"  localStorage key {key}: {'OK' if key in h else 'MISSING'}")

    # videos
    iframes = re.findall(r'bvid=([A-Za-z0-9]+)', h)
    print(f"  videos: {len(iframes)} -> {iframes}")

    # part-heads
    print(f"  part-heads: {h.count('class=\"part-head\"')}")

    # dictate buttons
    ptools = re.findall(r'data-mode="(word|note)"', h)
    print(f"  dictate buttons: {len(ptools)} -> {ptools}")

    # fulltext purity (no pinyin, no span)
    ft = re.search(r'<div id="fulltext" class="poem"[^>]*>(.*?)</div>', h, re.S)
    if ft:
        ft_text = ft.group(1)
        if 'data-note' in ft_text:
            print("  WARNING: fulltext contains annotation spans!")
        if re.search(r'[（(][a-zāáǎà]+[）)]', ft_text):
            print("  WARNING: fulltext contains pinyin!")
        else:
            print("  fulltext pure (no pinyin, no spans)")

    # word dict self-check
    wm = re.search(r'var DICT_WORDS = (\[.*?\]);', h, re.S)
    if wm:
        words = json.loads(wm.group(1))
        leak = [x for x in words if any(c in x['q'] for c in x['w'])]
        nbox = [x for x in words if x['q'].count('\u25a1') != len(x['w'])]
        npy = [x for x in words if len(x['py'].split()) != len(x['w']) and len(x['py'].split()) != 1]
        ntip = [x for x in words if not x.get('tip') or x['tip'] == x['w']]
        print(f"  word dict: {len(words)} items, leak={len(leak)}, nbox={len(nbox)}, npy={len(npy)}, ntip={len(ntip)}")
        if leak: print(f"    LEAK: {leak}")
        if nbox: print(f"    NBOX: {nbox}")
        if npy: print(f"    NPY: {npy}")
        if ntip: print(f"    NTIP: {ntip}")

    # note dict
    nm = re.search(r'var DICT_NOTES = (\[.*?\]);', h, re.S)
    if nm:
        notes = json.loads(nm.group(1))
        print(f"  note dict: {len(notes)} items")

    print()
