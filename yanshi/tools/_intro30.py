# -*- coding: utf-8 -*-
"""最近30篇：背景区作者简介首句 + kai块 + 卷首侧栏，供人工核对张冠李戴"""
import re, subprocess

FILES = """manjianghong-qiujin.html puliurenjia-liushaotang.html zaoer-sunhong.html
tongyi-nieluda.html haiyan-gaoerji.html tianxiadiyilou-hejiping.html tandushu-peigen.html
buqiushenjie-manancun.html shanshuihuadeyijing-likeran.html wuyanzhimei-zhuguangqian.html
quqianwomendexiangxiang-yetaotao.html fengyuyin-ludi.html duanzhang-bianzhilin.html
quyuan-guomoruo.html taikongyiri-yangliwei.html taijie-lisenxiang.html
zaichangjiangyuantougeladandong-malihua.html dengbolangfeng-maketuweng.html
weixuanzedelu-fuluosite.html jiarushenghuoqipianleni-puxijin.html huiyanan-hejingzhi.html
shuohezuo-zangkejia.html lie futuoersitai-ciweige.html weidadebeiju-ciweige.html
liefutuoersitai-ciweige.html meilideyanse-aifujuli.html tianxiadiyilou-hejiping.html
zuihouyicijiangyan-wenyiduo.html yingyougewuzhizhijingshen-dingzhaozhong.html
woyishengzhongdezhongyaojueze-wangxuan.html woweishimeerhuozhe-luosu.html""".split()

seen = set()
for f in FILES:
    if f in seen or not f.endswith('.html'):
        continue
    seen.add(f)
    try:
        s = open(f, 'rb').read().decode('utf-8', errors='ignore')
    except FileNotFoundError:
        print('%-48s !! 文件不存在' % f)
        continue
    mk = re.search(r'<div class="kai">([^<]{1,30})</div>\s*<div>([^<]{1,70})</div>', s, re.S)
    kai = (mk.group(1).strip() + '｜' + mk.group(2).strip()) if mk else '?'
    mbg = re.search(r'<section[^>]*id="bg"[^>]*>(.*?)(?=<section)', s, re.S)
    intro = ''
    if mbg:
        p = re.search(r'<h3>作者简介</h3>\s*<p>(.*?)</p>', mbg.group(1), re.S)
        if p:
            intro = re.sub(r'<[^>]+>', '', p.group(1)).strip()[:55]
    mh = re.search(r'<div class="hero-side[^"]*"[^>]*>\s*<div>([^<]{1,24})</div>', s, re.S)
    side = mh.group(1).strip() if mh else '?'
    print('%-44s\n   侧栏: %-16s kai: %s\n   简介: %s' % (f[:44], side, kai[:64], intro))
