# -*- coding: utf-8 -*-
"""
全库字号/样式统一：
1. 以 pipaxing 的 style 为基准，补入积累区 acc-* 与解读区 v-orig 规范；
2. 重写「正文字体缩放」段为全库统一清单；
3. 把每个文件的 <style> 块替换为规范 CSS（2 个漏写 <style> 标签的文件一并补上）；
4. 清除正文里的行内 font-size 覆盖。
"""
import os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_FILE = 'pipaxing-baijuyi.html'
BASE_SNAPSHOT = os.path.join(ROOT, 'tools', '_base_css.txt')  # 修改前的原始基准 CSS
STYLE_RE = re.compile(r'<style[^>]*>(.*?)</style>', re.S)
SCALE_START = '  /* 正文字体缩放（仅作用于正文文字，界面不变） */'
SCALE_END = '  /* 视频伪全屏 */'
MARK_TAIL = '.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em'

SCALE_BLOCK = '''  /* 正文字体缩放（全库统一 · 仅作用于正文文字，界面不变） */
  :root{--fs:1}
  body[data-fs="150"]{--fs:1.5}
  body[data-fs="200"]{--fs:2}
  body[data-fs="250"]{--fs:2.5}
  body[data-fs="300"]{--fs:3}
  .fs-sel{
    border:1px solid var(--line); background:#fdfaf3; color:var(--ink2);
    font-size:12.5px; border-radius:8px; padding:5px 6px; cursor:pointer; outline:none;
  }
  .fs-sel:hover{border-color:var(--teal); color:var(--teal)}
  /* 一级：板块大标题 */
  .sec-head h2{font-size:calc(30px*var(--fs))}
  .sec-head .no{font-size:calc(12px*var(--fs))}
  .part-head .p-num{font-size:calc(15px*var(--fs))}
  .part-head h3{font-size:calc(23px*var(--fs))}
  .part-head .range{font-size:calc(12.5px*var(--fs))}
  /* 二级之上：赏析区分点组的归属标题（管辖一、二、三、四） */
  .app-group{font-size:calc(21px*var(--fs))}
  /* 二级：卡片标题（赏析 h3 / 积累 acc-cat h3 / 媒体 h4 / 人物 lane h4） */
  .sec-sub{font-size:calc(15.5px*var(--fs))}
  .box h3{font-size:calc(19px*var(--fs))}
  .acc-cat h3{font-size:calc(19px*var(--fs))}
  .media h4{font-size:calc(16.5px*var(--fs))}
  .lane h4{font-size:calc(17px*var(--fs))}
  /* 三级：卡片内小标题 */
  .acc-sub{font-size:calc(16px*var(--fs))}
  .v-sec .v-label{font-size:calc(15px*var(--fs))}
  /* 正文 */
  .lead{font-size:calc(17.5px*var(--fs))}
  .part-overview{font-size:calc(14.8px*var(--fs))}
  .box p{font-size:calc(15.5px*var(--fs))}
  .box .note{font-size:calc(13.5px*var(--fs))}
  .acc-item{font-size:calc(15.5px*var(--fs))}
  .g-item{font-size:calc(14.6px*var(--fs))}
  .g-item dt{font-size:calc(17px*var(--fs))}
  .pl{font-size:calc(17px*var(--fs))}
  .v-line{font-size:calc(clamp(19px,3.4vw,23px)*var(--fs))}
  .v-orig{font-size:calc(16px*var(--fs))}
  .v-trans{font-size:calc(15.2px*var(--fs))}
  .v-more summary{font-size:calc(14px*var(--fs))}
  details .d-body{font-size:calc(14.6px*var(--fs))}
  .fame-card .f-line{font-size:calc(clamp(20px,3.6vw,26px)*var(--fs))}
  .fame-card p{font-size:calc(14.8px*var(--fs))}
  .step{font-size:calc(14.2px*var(--fs))}
  .xu-src{font-size:calc(19px*var(--fs))}
  .xu-sub{font-size:calc(14.8px*var(--fs))}
  .xu-trans{font-size:calc(15px*var(--fs))}
  table{font-size:calc(14.4px*var(--fs))}
  td .kai{font-size:calc(16px*var(--fs))}
  th,td{line-height:calc(1.9*var(--fs))}
  .anno-popup .aw{font-size:calc(17px*var(--fs))}
  .anno-popup .an{font-size:calc(14.5px*var(--fs))}
  footer{font-size:calc(13px*var(--fs))}
  /* 操作文字（随正文同步缩放） */
  .texttools button{font-size:calc(14px*var(--fs))}
  .ptools button{font-size:calc(15px*var(--fs))}
  .media a,.media .fsbtn{font-size:calc(13px*var(--fs))}

'''

ADD_BLOCK = '''  /* ========== 积累区（全库统一） ========== */
  .acc-cat{margin-bottom:28px}
  .acc-cat h3{font-family:var(--font-kai); font-size:19px; color:var(--red-deep); border-left:4px solid var(--gold); padding-left:12px; margin-bottom:14px}
  .acc-sub{font-family:var(--font-kai,serif); font-weight:700; font-size:16px; color:var(--teal-deep); margin:14px 0 6px; padding-left:10px; border-left:3px solid #b8934a}
  .acc-item{display:flex; gap:14px; padding:8px 0; border-bottom:1px dashed var(--line); font-size:15.5px; line-height:1.8}
  .acc-w{font-family:var(--font-kai); color:var(--teal-deep); font-weight:700; min-width:200px; flex-shrink:0}
  .acc-d{color:var(--ink2); flex:1}
  @media(max-width:640px){
    .acc-item{flex-direction:column; gap:2px}
    .acc-w{min-width:0}
  }
  /* 解读区原文段落 */
  .v-orig{font-family:var(--font-kai); font-size:16px; color:var(--ink); line-height:2.1; margin:2px 0; text-indent:2em}
  /* 赏析区组标题：比卡片 h3 高一级，用于管辖「一、二、三、四」分点 box */
  .app-group{
    font-family:var(--font-kai); font-size:21px; letter-spacing:4px; color:var(--ink);
    margin:26px 0 14px; padding-left:14px; border-left:5px solid var(--red); line-height:1.4;
  }
  /* 折叠正文内的段落统一继承 .d-body 字号（避免落在 .box 内时被 .box p 放大） */
  details .d-body p{font-size:inherit; margin:4px 0}

  /* ========== 兼容：早期模板类名（与标准类名同一层级、同一字号） ========== */
  .verse-text{font-family:var(--font-kai); font-size:calc(clamp(19px,3.4vw,23px)*var(--fs)); letter-spacing:2px; color:var(--ink); line-height:1.9; word-break:break-word}
  .vs-label{font-family:var(--font-kai); color:var(--teal-deep); font-weight:700; font-size:calc(15px*var(--fs)); letter-spacing:3px}
  .vs-body{color:var(--ink2); font-size:calc(14.6px*var(--fs)); padding:2px 2px 6px 16px; overflow:hidden}
  .vs-body p{font-size:inherit; margin:4px 0}
  .video-box{background:#fbf7ec; border:1px solid var(--line); border-radius:12px; padding:12px 14px; overflow:hidden; margin:4px 0}
  .video-label{font-family:var(--font-kai); font-size:calc(16.5px*var(--fs)); letter-spacing:2px; color:var(--teal-deep); margin:0 0 8px}
  .part-desc{font-size:calc(14.8px*var(--fs)); color:var(--ink2); background:rgba(168,135,79,.08); border:1px solid rgba(168,135,79,.25); border-radius:10px; padding:12px 18px; margin:6px 0 16px}
  .acc-word{font-family:var(--font-kai); color:var(--teal-deep); font-weight:700; font-size:inherit; min-width:200px; flex-shrink:0}
  .acc-exp{color:var(--ink2); font-size:inherit; flex:1}
  .hero-sub{font-family:var(--font-kai); font-size:15px; letter-spacing:3px; color:#cbbd9c; margin-top:10px}

'''


def build_canon():
    if os.path.exists(BASE_SNAPSHOT):
        css = open(BASE_SNAPSHOT, encoding='utf-8').read()
    else:
        src = open(os.path.join(ROOT, BASE_FILE), encoding='utf-8').read()
        css = STYLE_RE.search(src).group(1)
    # 1) 去掉重复的 .lead p
    css = re.sub(r'(\.lead p\{margin:14px 0\}\s*)+', '.lead p{margin:14px 0}\n  ', css)
    # 2) 去掉尾部残留的 1.05em 版 .acc-sub
    if MARK_TAIL in css:
        i = css.index(MARK_TAIL)
        css = css[:i]
    # 3) 打印样式：补 .fulltext 与 .app-group
    css = css.replace('.xu-block{columns:1!important}', '.xu-block,.fulltext{columns:1!important}')
    css = css.replace('.sec-head{background:none}',
                      '.sec-head{background:none}\n    .app-group{color:#000!important; border-left-color:#000!important; margin:14px 0 8px}')
    # 4) 替换缩放段
    a = css.index(SCALE_START)
    b = css.index(SCALE_END)
    css = css[:a] + ADD_BLOCK + SCALE_BLOCK + css[b:]
    return css.rstrip() + '\n'


INLINE_FS = re.compile(r'(<[^>]+?)\sstyle="([^"]*)"')


def strip_inline_fs(body):
    """删除正文里行内的 font-size 声明；若 style 只剩空白或仅余 line-height，则整段去掉。"""
    n = 0

    def rep(m):
        nonlocal n
        tag, st = m.group(1), m.group(2)
        parts = [p.strip() for p in st.split(';') if p.strip()]
        keep = [p for p in parts if not p.replace(' ', '').startswith('font-size:')]
        if not keep:
            n += 1
            return tag
        if keep == ['line-height:2']:
            n += 1
            return tag
        new = ';'.join(keep)
        if new != st:
            n += 1
        return '%s style="%s"' % (tag, new)

    return INLINE_FS.sub(rep, body), n


def main(apply=True):
    canon = build_canon()
    open(os.path.join(ROOT, 'tools', '_canon.css'), 'w', encoding='utf-8').write(canon)
    files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html'))
    stat = collections.Counter()
    for f in files:
        p = os.path.join(ROOT, f)
        src = open(p, encoding='utf-8').read()
        m = STYLE_RE.search(src)
        if m:
            head, tail = src[:m.start()], src[m.end():]
            new = head + '<style>' + canon + '</style>' + tail
            stat['ok'] += 1
        else:
            # 裸 CSS：head 内 </title> 之后到 </head> 之前
            i = src.index('</title>') + len('</title>')
            j = src.index('</head>')
            new = src[:i] + '\n<style>' + canon + '</style>\n' + src[j:]
            stat['wrapped'] += 1
        # 清行内 font-size（只动 style 块之后的正文）
        sm = STYLE_RE.search(new)
        a = sm.end()
        rest, n = strip_inline_fs(new[a:])
        if n:
            stat['inline'] += 1
            stat['inline_n'] += n
            new = new[:a] + rest
        if new != src:
            stat['changed'] += 1
            if apply:
                open(p, 'w', encoding='utf-8').write(new)
    print(dict(stat), '总文件', len(files))


if __name__ == '__main__':
    main(apply='--apply' in sys.argv)
