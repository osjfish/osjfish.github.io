import shutil, subprocess, os, sys, re
src = r'D:\App\Apps\yanshi\tools\gen_taikongyiri.py'
tmp = r'D:\App\Apps\yanshi\tools\_gen_tk_test.py'
out = r'D:\App\Apps\yanshi\tools\_tk_test.html'
shutil.copy(src, tmp)
s = open(tmp, 'r', encoding='utf-8').read()
s = s.replace(r'OUT = r"D:\App\Apps\yanshi\taikongyiri-yangliwei.html"', r'OUT = r"D:\App\Apps\yanshi\tools\_tk_test.html"')
open(tmp, 'w', encoding='utf-8').write(s)
try:
    r = subprocess.run([sys.executable, tmp], capture_output=True, text=True)
    print('STDOUT:', r.stdout)
    print('STDERR:', r.stderr)
    print('RC:', r.returncode)
    if r.returncode == 0 and os.path.exists(out):
        h = open(out, 'r', encoding='utf-8').read()
        print('OUTPUT EXISTS, bytes=', len(h.encode('utf-8')))
        print('bg before jielu:', h.find('<section id="bg"') < h.find('<section id="jielu"'))
        m = re.search(r'<button id="btnShowAll"[^>]*>', h)
        print('btnShowAll tag:', m.group(0) if m else 'NOT FOUND')
        print('fsSel onchange:', 'onchange=' in h[h.find('<select id="fsSel"'):h.find('</select>', h.find('<select id="fsSel"')) + 10])
        print('annoPopup has annoW:', 'id="annoW"' in h)
        print('ptools exists:', 'class="ptools"' in h)
finally:
    os.remove(tmp)
    if os.path.exists(out):
        os.remove(out)
