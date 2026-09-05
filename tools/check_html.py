# -*- coding: utf-8 -*-
"""Self-check for generated courseware HTML."""
import re, json, sys

path = sys.argv[1] if len(sys.argv) > 1 else r"D:\App\Apps\caoguilunzhan.html"
src = open(path, encoding="utf-8").read()

print("=== Structure ===")
checks = {
    ":root{--fs:1}": ":root{--fs:1}" in src,
    "btnAll": 'id="btnAll"' in src,
    "btnRecite": 'id="btnRecite"' in src,
    "btnPrint": 'id="btnPrint"' in src,
    "verseList": 'id="verseList"' in src,
    "fulltext": 'id="fulltext"' in src and 'class="poem"' in src,
    "main wrap": '<main class="wrap">' in src,
    "nav nav-in": '<nav class="nav">' in src and '<div class="nav-in">' in src,
    "part-head h3 line-height": "line-height:1" in src,
    "https player": "https://player.bilibili.com/player.html?bvid=" in src,
}
for k, v in checks.items():
    print(f"  {'OK' if v else 'FAIL'}: {k}")

# Check for //player specifically in iframe src
iframe_srcs = re.findall(r'<iframe[^>]*src="([^"]*)"', src)
print(f"\n  iframe srcs:")
for s in iframe_srcs:
    print(f"    {s[:80]}")
    if s.startswith("//"):
        print(f"    FAIL: protocol-relative URL!")

print("\n=== English quotes ===")
ascii_q_in_text = len(re.findall(r'[\u4e00-\u9fff]"[\u4e00-\u9fff]', src))
print(f"  ASCII quotes between Chinese chars: {ascii_q_in_text}")

print("\n=== Question bank ===")
# Find DICT_WORDS assignment more precisely
m = re.search(r'var DICT_WORDS = (\[.*?\]);\s*\n', src, re.S)
if m:
    words = json.loads(m.group(1))
    print(f"  DICT_WORDS: {len(words)} entries")
    leak = [x for x in words if any(c in x['q'] for c in x['w'])]
    nbox = [x for x in words if x['q'].count('\u25a1') != len(x['w'])]
    npy = [x for x in words if len(x['py'].split()) != len(x['w']) and len(x['py'].split()) != 1]
    ntip = [x for x in words if not x.get('tip') or x['tip'] == x['w']]
    print(f"  leak: {len(leak)}, nbox: {len(nbox)}, npy: {len(npy)}, ntip: {len(ntip)}")
    if leak: print(f"    LEAK: {[(x['w'],x['q']) for x in leak[:3]]}")
    if nbox: print(f"    NBOX: {[(x['w'],x['q']) for x in nbox[:3]]}")
    if npy: print(f"    NPY: {[(x['w'],x['py']) for x in npy[:3]]}")
    if ntip: print(f"    NTIP: {[(x['w'],x['tip']) for x in ntip[:3]]}")
else:
    print("  FAIL: DICT_WORDS not found")

m = re.search(r'var DICT_NOTES = (\[.*?\]);\s*\n', src, re.S)
if m:
    notes = json.loads(m.group(1))
    print(f"  DICT_NOTES: {len(notes)} entries")
else:
    print("  FAIL: DICT_NOTES not found")

print("\n=== Videos ===")
bvids = re.findall(r'bvid=([A-Za-z0-9]+)', src)
print(f"  BVIDs: {bvids}")

print("\n=== localStorage key ===")
fs_keys = re.findall(r"getItem\('(\w+_fs)'\)", src)
print(f"  fs keys: {fs_keys}")

print("\n=== Verse count ===")
verses = re.findall(r'class="verse" id="l(\d+)"', src)
print(f"  verses: {len(verses)}")

print("\n=== Annotation count ===")
annos = re.findall(r'class="anno-word"', src)
print(f"  anno-word spans: {len(annos)}")

print("\n=== Empty annotations check ===")
# Check for annotations where note equals word (空转)
anno_pairs = re.findall(r'data-note="([^"]*)">([^<]+)</span>', src)
empty = [(w,n) for w,n in anno_pairs if n == w or n.strip() == w.strip()]
print(f"  empty/self-referential annotations: {len(empty)}")
if empty: print(f"    {empty[:5]}")

print("\nDone.")
