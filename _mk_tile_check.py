# -*- coding: utf-8 -*-
# 从 mahjong.html 抽取牌面渲染函数，生成自检预览页 _tile_check.html
src = open('mahjong.html', encoding='utf-8').read()
start = src.index('/* ---- 牌面')
end = src.index('function renderAll')
block = src[start:end]

codes = [s + str(n) for s in 'mtd' for n in range(1, 10)] + ['df', 'nf', 'xf', 'bf', 'hz', 'fc', 'bb']

tpl = """<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8"><title>tiles check</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&display=swap');
body{background:#dfe8ee;padding:16px;font-family:sans-serif}
.row{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}
.tile{width:60px;height:81px;border-radius:8px;background:linear-gradient(168deg,#fffef8 0%,#faf4e2 45%,#eee5cc 100%);box-shadow:0 2px 5px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.85),inset 0 -3px 0 rgba(180,160,110,.28);display:flex;align-items:center;justify-content:center;border:1px solid rgba(160,140,90,.3)}
.tile svg{display:block}
.tile svg text{font-family:"Noto Serif SC","STKaiti","KaiTi","Kaiti SC","STSong","SimSun",serif}
.small .tile{width:36px;height:49px}
.lbl{font-size:12px;margin:6px 0}
</style></head><body>
<div class="lbl">标准尺寸（60px）</div><div class="row" id="r1"></div>
<div class="lbl">副露小尺寸（36px）</div><div class="row small" id="r2"></div>
<script>
var G=null;
var WIND_CHAR={df:'东',nf:'南',xf:'西',bf:'北'};
__BLOCK__
var codes=__CODES__;
['r1','r2'].forEach(function(id){var el=document.getElementById(id);
codes.forEach(function(c){var w=document.createElement('div');w.innerHTML=tileHTML(c);el.appendChild(w.firstChild);});});
</script></body></html>"""

html = tpl.replace('__BLOCK__', block).replace('__CODES__', repr(codes))
open('_tile_check.html', 'w', encoding='utf-8').write(html)
print('ok', len(html))
