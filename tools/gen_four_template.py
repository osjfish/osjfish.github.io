# -*- coding: utf-8 -*-
"""生成4篇统编版七年级上册童话/寓言/神话交互式教学课件"""
import json, os, re

OUT_DIR = r"D:\App\Apps\yanshi"

# ============ CSS 模板（来自beiying标杆） ============
CSS = r'''
  :root{
    --paper:#f6f0e0; --paper-deep:#efe6ce; --card:#fbf7ec;
    --ink:#332c22; --ink2:#5d5443; --ink3:#8d826c; --line:#e2d7bd;
    --red:#8c2f2b; --red-deep:#6f211e; --teal:#3d5766; --teal-deep:#2e4552;
    --gold:#a8874f;
    --fs:1;
    --font-kai:"Kaiti SC","STKaiti","KaiTi","楷体","FangSong","仿宋",serif;
    --font-song:"Songti SC","SimSun","Noto Serif SC",serif;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{
    font-family:var(--font-song); color:var(--ink); line-height:1.9;
    overflow-x:clip;
    background-color:var(--paper);
    background-image:
      radial-gradient(ellipse 900px 420px at 85% -60px, rgba(61,87,102,.055), transparent 65%),
      radial-gradient(ellipse 700px 380px at 8% 120%, rgba(140,47,43,.04), transparent 60%),
      repeating-linear-gradient(0deg, rgba(60,50,30,.016) 0 1px, transparent 1px 4px);
  }
  ::selection{background:rgba(168,135,79,.35)}
  .kai{font-family:var(--font-kai)}
  a{color:var(--teal)}
  button{font-family:inherit}

  /* ========== 卷首 ========== */
  .hero{
    position:relative; overflow:hidden; color:#f1e9d4;
    background:
      radial-gradient(ellipse 90% 130% at 50% -12%, rgba(240,231,206,.06), transparent 55%),
      linear-gradient(170deg,#233241 0%, #1a2635 55%, #141d29 100%);
    padding:54px 20px 46px; text-align:center;
  }
  .hero::after{
    content:""; position:absolute; left:50%; bottom:0; transform:translateX(-50%);
    width:min(420px,72%); height:2px;
    background:linear-gradient(90deg, transparent, rgba(203,171,112,.55), transparent);
  }
  .hero-inner{position:relative; z-index:2}
  .hero-side{
    display:flex; align-items:center; justify-content:center; gap:16px;
    font-family:var(--font-kai); font-size:clamp(14px,1.7vw,18px);
    letter-spacing:.32em; text-indent:.32em; color:#cbbd9c; line-height:1.4;
  }
  .hero-side::before,.hero-side::after{
    content:""; flex:0 0 auto; width:56px; height:1px;
    background:linear-gradient(90deg, transparent, rgba(203,171,112,.65));
  }
  .hero-side::after{transform:scaleX(-1)}
  .hero-title{
    font-family:var(--font-kai); font-size:clamp(34px,5.8vw,64px);
    letter-spacing:.16em; text-indent:.16em; line-height:1.3;
    color:#f4edd8; text-shadow:0 3px 22px rgba(0,0,0,.45); margin:0;
  }
  @media(max-width:560px){
    .hero{padding:40px 14px 34px}
    .hero-side{gap:10px; letter-spacing:.22em; text-indent:.22em}
    .hero-side::before,.hero-side::after{width:26px}
  }

  /* ========== 导航 ========== */
  .nav{
    position:sticky; top:0; z-index:99; background:rgba(246,240,224,.96); backdrop-filter:blur(6px);
    border-bottom:1px solid var(--line); box-shadow:0 2px 10px rgba(51,44,34,.06);
  }
  .nav-in{max-width:1000px; margin:0 auto; display:flex; align-items:center; gap:4px; padding:8px 14px; overflow-x:auto; scrollbar-width:none}
  .nav-in::-webkit-scrollbar{display:none}
  .nav a{
    flex:0 0 auto; text-decoration:none; color:var(--ink2); font-size:14px; letter-spacing:1px;
    padding:6px 12px; border-radius:8px; white-space:nowrap; transition:.2s;
  }
  .nav a:hover{background:rgba(168,135,79,.12); color:var(--ink)}
  .nav a.on{background:linear-gradient(180deg,#efe0ba,#e6d2a4); color:var(--red-deep); font-weight:700}
  .nav .tool{flex:0 0 auto; margin-left:auto; display:flex; gap:5px; flex-wrap:nowrap}
  .nav .tool button{
    border:1px solid var(--line); background:#fdfaf3; color:var(--ink2); font-size:12.5px;
    border-radius:8px; padding:5px 9px; cursor:pointer; transition:.2s; white-space:nowrap;
  }
  .nav .tool button:hover{border-color:var(--teal); color:var(--teal)}
  .nav .tool .fs-sel{
    border:1px solid var(--line); background:#fdfaf3; color:var(--ink2); font-size:12.5px;
    border-radius:8px; padding:5px 6px; cursor:pointer; outline:none; white-space:nowrap;
  }
  .nav .tool .fs-sel:hover{border-color:var(--teal)}

  /* ========== 主体 ========== */
  .wrap{max-width:960px; margin:0 auto; padding:0 18px}
  section{padding:34px 0 10px; scroll-margin-top:64px}
  .sec-head{display:flex; align-items:baseline; gap:14px; margin:0 0 8px}
  .sec-head::before{content:""; width:6px; height:30px; background:linear-gradient(180deg,var(--red),var(--red-deep)); border-radius:3px; transform:translateY(6px)}
  .sec-head h2{font-family:var(--font-kai); font-size:30px; letter-spacing:6px; font-weight:700; color:var(--ink); flex:0 0 auto}
  .sec-head .no{font-size:12px; color:var(--ink3); letter-spacing:2px}
  .sec-sub{color:var(--ink2); font-size:15.5px; margin:0 0 20px; padding-left:20px}
  .divider{height:1px; background:linear-gradient(90deg,transparent,var(--line) 18%,var(--line) 82%,transparent); margin:34px 0 8px}
  .kai-lg{font-family:var(--font-kai)}

  .lead{
    font-family:var(--font-kai); font-size:17.5px; line-height:2.25; color:var(--ink);
    background:linear-gradient(180deg,#fbf7ec,#f7f0dd); border:1px solid var(--line);
    border-left:4px solid var(--gold); border-radius:10px; padding:22px 26px; margin:0 0 24px;
    letter-spacing:.06em; overflow:hidden;
  }
  .box{
    background:var(--card); border:1px solid var(--line); border-radius:12px; padding:20px 24px; margin:0 0 18px; overflow:hidden;
  }
  .box h3{font-family:var(--font-kai); font-size:19px; color:var(--teal-deep); letter-spacing:2px; margin:0 0 10px}
  .box h3::before{content:"\u25c6 "; color:var(--gold); font-size:14px}
  .box p{font-size:15.5px; margin:16px 0}
  .lead p{margin:14px 0}
  .box .note{font-size:13.5px; color:var(--ink2)}

  /* 原文 */
  .texttools{display:flex; flex-wrap:wrap; gap:8px; margin:0 0 16px; padding-left:20px}
  .texttools button{
    border:1px solid var(--teal); color:var(--teal); background:rgba(61,87,102,.06);
    border-radius:8px; padding:6px 16px; cursor:pointer; font-size:14px; transition:.2s;
  }
  .texttools button:hover{background:var(--teal); color:#fff}
  .texttools button.off{opacity:.5}
  .media-box{padding:16px 20px}
  .media-grid{display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:14px; margin:4px 0 6px}
  .media{background:#fbf7ec; border:1px solid var(--line); border-radius:12px; padding:12px 14px; overflow:hidden}
  .media h4{font-family:var(--font-kai); font-size:16.5px; letter-spacing:2px; color:var(--teal-deep); margin:0 0 8px}
  .media iframe{width:100%; aspect-ratio:16/9; border:0; border-radius:8px; background:#111; display:block}
  .media a{display:inline-block; font-size:13px; margin-top:8px; color:var(--teal); text-decoration:none; border-bottom:1px dashed rgba(61,87,102,.5)}
  .media a:hover{color:var(--red)}
  .fsbtn{
    display:inline-block; margin:8px 0 0 10px; border:1px solid var(--teal); color:var(--teal);
    background:rgba(61,87,102,.06); border-radius:8px; padding:4px 12px; cursor:pointer;
    font-size:12.5px; transition:.2s; vertical-align:middle;
  }
  .fsbtn:hover{background:var(--teal); color:#fff}
  .fulltext{columns:2; column-gap:34px; column-rule:1px dashed var(--line); margin:10px 0 8px}
  .pl{break-inside:avoid; margin:0 0 10px; font-size:17px}
  .pl .no{color:var(--red); font-size:12px; vertical-align:super; margin-right:5px; font-family:var(--font-kai); letter-spacing:0}
  .xu-block b{color:var(--red-deep)}
  .pl.reciteline{cursor:pointer; transition:.15s; border-radius:6px}
  .pl.reciteline:hover{background:rgba(168,135,79,.1)}
  .pl .rh{color:var(--red-deep); font-weight:700; font-size:inherit; vertical-align:baseline}
  .pl .rb{letter-spacing:.14em; color:rgba(61,87,102,.55); font-size:inherit; vertical-align:baseline}
  .tip{font-size:13px; color:var(--ink3); margin-bottom:6px}

  /* 逐句卡片 */
  .part-head{
    display:flex; align-items:center; justify-content:center; gap:14px; margin:30px 0 6px; flex-wrap:wrap;
  }
  .part-head .p-num{
    font-family:var(--font-kai); font-size:15px; color:#fff; background:linear-gradient(160deg,var(--teal),var(--teal-deep));
    border-radius:8px; padding:4px 12px; letter-spacing:2px; flex:0 0 auto;
  }
  .part-head h3{font-family:var(--font-kai); font-size:23px; letter-spacing:3px; color:var(--ink); line-height:1; margin:0}
  .part-head .range{font-size:12.5px; color:var(--ink3); letter-spacing:1px}
  .part-overview{
    font-size:14.8px; color:var(--ink2); background:rgba(168,135,79,.08);
    border:1px solid rgba(168,135,79,.25); border-radius:10px; padding:12px 18px; margin:6px 0 16px;
  }
  .verse{
    background:var(--card); border:1px solid var(--line); border-radius:12px;
    margin:0 0 16px; padding:16px 20px 14px; box-shadow:0 1px 3px rgba(51,44,34,.04); overflow:hidden;
  }
  .v-top{display:flex; align-items:center; gap:12px}
  .v-no{
    flex:0 0 auto; font-family:var(--font-kai); font-size:13px; color:var(--red-deep);
    border:1.5px solid rgba(140,47,43,.5); border-radius:50%; width:32px; height:32px;
    display:flex; align-items:center; justify-content:center;
  }
  .v-line{font-family:var(--font-kai); font-size:clamp(19px,3.4vw,23px); letter-spacing:2px; color:var(--ink); flex:1; min-width:0; word-break:break-word}
  .v-line b{color:var(--red-deep); font-weight:700}
  .v-trans{
    font-size:15.2px; color:var(--ink2); background:rgba(61,87,102,.055);
    border-left:3px solid var(--teal); border-radius:0 8px 8px 0; padding:7px 12px; margin:9px 0;
    overflow:hidden;
  }
  .v-trans b{color:var(--teal-deep); font-weight:400}
  details{font-size:14.5px}
  details summary{
    cursor:pointer; list-style:none; font-family:var(--font-kai); letter-spacing:2px;
    color:var(--teal-deep); font-weight:700; font-size:15px; margin:4px 0 2px; display:inline-flex; align-items:center; gap:6px;
  }
  details summary::-webkit-details-marker{display:none}
  details summary::before{content:"\u25b8 "; font-size:12px; color:var(--gold); transition:.2s}
  details[open] summary::before{transform:rotate(90deg)}
  details .d-body{padding:2px 2px 6px 16px; color:var(--ink2); font-size:14.6px; min-width:0}
  .v-more{margin-top:8px}
  .v-more summary{font-size:14px; letter-spacing:1px}
  .v-sec{margin:10px 0 12px}
  .v-sec .v-label{font-family:var(--font-kai); color:var(--teal-deep); font-weight:700; font-size:15px; letter-spacing:3px; display:block; margin:0 0 4px}
  .term{color:var(--teal-deep); font-weight:700; margin-right:3px}
  .tags{display:flex; flex-wrap:wrap; gap:6px; margin-top:8px}
  .tags span{
    font-size:12px; color:var(--red-deep); background:rgba(140,47,43,.07);
    border:1px solid rgba(140,47,43,.22); border-radius:12px; padding:2px 10px; letter-spacing:1px;
  }

  /* 练习 · 听写 */
  .ptools{display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:12px; margin:0 0 6px}
  .ptools button{
    border:1px solid var(--teal); color:var(--teal); background:rgba(61,87,102,.06);
    border-radius:10px; padding:13px 8px; cursor:pointer; font-size:15px; letter-spacing:1px; transition:.2s;
  }
  .ptools button:hover{background:var(--teal); color:#fff}

  /* 听写全屏 */
  .dictate{--ds:1.25; position:fixed; inset:0; z-index:9999; display:flex; flex-direction:column;
    background:radial-gradient(ellipse 90% 120% at 50% -10%, rgba(240,231,206,.08), transparent 55%),
    linear-gradient(160deg,#1e2a39 0%, #151f2b 60%, #0f1722 100%);
    color:#f4edd8; padding:26px 6vw 20px; font-family:var(--font-kai)}
  .dictate[hidden]{display:none}
  .dictate-top{display:flex; justify-content:space-between; align-items:center; margin-bottom:4vh}
  .dictate-mode{font-size:calc(15px * var(--ds)); letter-spacing:4px; color:#cbbd9c}
  .dictate-progress{font-size:calc(15px * var(--ds)); color:#8fa0ae; letter-spacing:1px}
  .dictate-exit{border:1px solid rgba(203,189,156,.5); color:#cbbd9c; background:transparent; border-radius:8px; padding:6px 18px; cursor:pointer; font-size:calc(14px * var(--ds)); font-family:var(--font-kai); letter-spacing:2px; transition:.2s}
  .dictate-exit:hover{background:rgba(203,189,156,.15)}
  .dictate-fs{border:1px solid rgba(203,189,156,.5); color:#cbbd9c; background:transparent; border-radius:8px; padding:6px 10px; cursor:pointer; font-size:calc(14px * var(--ds)); font-family:var(--font-kai); letter-spacing:1px; transition:.2s; margin-left:6px}
  .dictate-fs:hover{background:rgba(203,189,156,.15)}
  .dictate-card{flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; min-height:0}
  .dictate-py{font-size:calc(clamp(34px,5.2vw,56px) * var(--ds)); color:#cbbd9c; letter-spacing:6px; margin-bottom:26px; line-height:1.3}
  .dictate-line{font-size:calc(clamp(19px,2.6vw,28px) * var(--ds)); color:#f4edd8; opacity:.94; margin-bottom:14px; letter-spacing:1px}
  .dictate-hint{font-size:calc(15px * var(--ds)); color:#8fa0ae; letter-spacing:3px}
  .dictate-ans{margin-top:32px; padding:18px 36px; border:1px solid rgba(203,189,156,.38); border-radius:14px; background:rgba(203,189,156,.09); animation:fadeIn .25s ease}
  .dictate-word{font-size:calc(clamp(30px,4.8vw,48px) * var(--ds)); color:#f0d9a8; letter-spacing:5px; margin-bottom:8px}
  .dictate-tip{font-size:calc(15px * var(--ds)); color:#a8b6c2; letter-spacing:1px}
  .dictate-actions{display:flex; justify-content:center; gap:14px; padding-top:2vh}
  .dictate-actions button{border:1px solid #cbbd9c; color:#f4edd8; background:transparent; border-radius:10px; padding:10px 32px; font-size:calc(16px * var(--ds)); cursor:pointer; letter-spacing:3px; font-family:var(--font-kai); transition:.2s}
  .dictate-actions button:hover{background:rgba(203,189,156,.18)}
  .dictate-actions .primary{background:linear-gradient(180deg,#efe0ba,#e6d2a4); color:#7a3326; border-color:transparent; font-weight:700}
  .dictate-actions .primary:hover{background:linear-gradient(180deg,#f4e8c8,#ecdbb2)}
  @keyframes fadeIn{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}

  /* 名句 */
  .fame{display:grid; grid-template-columns:1fr; gap:14px; margin-top:10px}
  .fame-card{
    background:var(--card); color:var(--ink); border-radius:12px;
    padding:18px 22px; position:relative; border:1px solid var(--line);
    box-shadow:0 2px 8px rgba(0,0,0,.04);
  }
  .fame-card .f-line{font-family:var(--font-kai); font-size:clamp(18px,3.2vw,22px); letter-spacing:2px; color:var(--teal-deep); margin-bottom:8px; border-left:3px solid var(--gold); padding-left:12px}
  .fame-card .f-line b{color:var(--red-deep)}
  .fame-card p{font-size:14.8px; color:var(--ink2); margin:4px 0; line-height:1.9}

  /* 表格 */
  .tw{overflow-x:auto; -webkit-overflow-scrolling:touch; max-width:100%; margin:0}
  table{width:100%; border-collapse:collapse; font-size:14.4px; background:var(--card); border-radius:10px; overflow:hidden; margin:8px 0 16px; min-width:520px}
  th,td{border:1px solid var(--line); padding:8px 12px; text-align:left; vertical-align:top; word-break:break-word}
  th{font-family:var(--font-kai); background:#efe6ce; color:var(--teal-deep); letter-spacing:1px}
  td .kai{font-size:16px}
  tr:nth-child(even) td{background:rgba(246,240,224,.6)}

  /* 积累 */
  .glossary{display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:12px}
  .g-item{background:var(--card); border:1px solid var(--line); border-radius:10px; padding:12px 16px; font-size:14.6px}
  .g-item dt{font-family:var(--font-kai); color:var(--red-deep); font-size:17px; letter-spacing:2px}
  .g-item dd{color:var(--ink2)}

  .acc-cat{margin-bottom:28px}
  .acc-cat h3{font-family:var(--font-kai); font-size:calc(20px*var(--fs)); color:var(--red-deep); border-left:4px solid var(--gold); padding-left:12px; margin-bottom:14px}
  .acc-item{display:flex; gap:14px; padding:8px 0; border-bottom:1px dashed var(--line); font-size:calc(15.5px*var(--fs)); line-height:1.8}
  .acc-w{font-family:var(--font-kai); color:var(--teal-deep); font-weight:700; min-width:200px; flex-shrink:0}
  .acc-d{color:var(--ink2); flex:1}
  .acc-sub{font-family:var(--font-kai); font-weight:700; border-left:3px solid #b8934a; padding-left:8px; color:var(--teal-deep); margin:14px 0 6px; font-size:calc(16px*var(--fs))}
  @media(max-width:640px){.acc-item{flex-direction:column; gap:2px}.acc-w{min-width:0}}

  footer{
    margin-top:44px; border-top:1px solid var(--line); padding:24px 0 40px;
    text-align:center; color:var(--ink3); font-size:13px; line-height:2.2; overflow:hidden;
  }
  footer .kai{font-size:15px; color:var(--ink2)}

  .top-btn{
    position:fixed; right:18px; bottom:22px; z-index:90; border:1px solid var(--line);
    background:#fdfaf3; color:var(--ink2); border-radius:50%; width:42px; height:42px;
    font-size:17px; cursor:pointer; box-shadow:0 3px 10px rgba(51,44,34,.15); transition:.2s;
  }
  .top-btn:hover{color:var(--red); border-color:var(--red)}

  /* 打印 */
  @media print{
    .nav,.tool,.top-btn,.tags{display:none!important}
    .hero{display:none!important}
    .texttools{display:none}
    .media-box{display:none}
    body{background:#fff!important; color:#000!important; line-height:1.5}
    .wrap{max-width:100%}
    section{padding:8px 0}
    .divider{display:none}
    .sec-head h2{font-size:20px; letter-spacing:2px}
    .sec-head{background:none}
    .lead,.box,.verse,.fame-card,.lane,.converge{
      background:#fff!important; border:1px solid #999!important; box-shadow:none!important;
      color:#000!important; border-radius:0; page-break-inside:avoid;
    }
    .lead{padding:8px 10px; font-size:12.5px; line-height:1.7}
    .box{padding:8px 10px; margin-bottom:8px}
    .box h3{color:#000!important}
    .box p,.box .note{color:#000!important}
    .fame-card .f-line,.fame-card p{color:#000!important}
    .v-line,.xu-src{color:#000!important}
    .xu-trans,.v-trans{background:#fff!important; border-left:2px solid #000!important; color:#000!important}
    details .d-body{color:#000!important}
    .v-label{color:#000!important}
    details{display:block}
    details .d-body{padding-left:10px}
    table{min-width:0!important; font-size:11.5px}
    th{background:#eee!important; color:#000!important}
    th,td{border:1px solid #000!important; color:#000!important; padding:3px 6px}
    .xu-block{columns:1!important}
    footer{border:none; color:#000!important; padding:10px 0 20px}
  }

  @media(max-width:680px){
    .fulltext{columns:1}
    section{padding:24px 0 6px}
    .sec-head{flex-wrap:wrap}
    .sec-head h2{font-size:24px; letter-spacing:3px}
    .verse{padding:13px 14px 11px}
    .v-line{letter-spacing:1px}
    table{min-width:440px}
  }
  @media(max-width:420px){
    table{min-width:0}
    .box{padding:14px}
    .lead{padding:16px 18px}
  }
  /* 正文字体缩放 */
  :root{--fs:1}
  body[data-fs="150"]{--fs:1.5}
  body[data-fs="200"]{--fs:2}
  body[data-fs="250"]{--fs:2.5}
  body[data-fs="300"]{--fs:3}
  .lead{font-size:calc(17.5px*var(--fs))}
  .sec-sub{font-size:calc(15.5px*var(--fs))}
  .part-overview{font-size:calc(14.8px*var(--fs))}
  .box p{font-size:calc(15.5px*var(--fs))}
  .box .note{font-size:calc(13.5px*var(--fs))}
  .pl{font-size:calc(17px*var(--fs))}
  .v-line{font-size:calc(clamp(19px,3.4vw,23px)*var(--fs))}
  .v-trans{font-size:calc(15.2px*var(--fs))}
  details .d-body{font-size:calc(14.6px*var(--fs))}
  .fame-card .f-line{font-size:calc(clamp(20px,3.6vw,26px)*var(--fs))}
  .fame-card p{font-size:calc(14.8px*var(--fs))}
  table{font-size:calc(14.4px*var(--fs))}
  td .kai{font-size:calc(16px*var(--fs))}
  th,td{line-height:calc(1.9*var(--fs))}
  .g-item{font-size:calc(14.6px*var(--fs))}
  .g-item dt{font-size:calc(17px*var(--fs))}
  .sec-head h2{font-size:calc(30px*var(--fs))}
  .sec-head .no{font-size:calc(12px*var(--fs))}
  .box h3{font-size:calc(19px*var(--fs))}
  .v-sec .v-label{font-size:calc(15px*var(--fs))}
  .v-more summary{font-size:calc(14px*var(--fs))}
  footer{font-size:calc(13px*var(--fs))}
  .media h4{font-size:calc(15px*var(--fs))}
  .media a,.media .fsbtn{font-size:calc(13px*var(--fs))}

  /* 原文可点击注释词 */
  .anno-word{color:var(--teal-deep); border-bottom:1px dashed var(--teal); cursor:pointer; transition:.15s; padding:0 1px; border-radius:2px}
  .anno-word:hover{background:rgba(42,107,102,.12)}
  .anno-word.active{background:rgba(42,107,102,.2)}
  /* 注释弹窗 */
  .anno-popup{position:fixed; z-index:10000; background:#fffdf7; border:1px solid var(--gold); border-radius:10px; box-shadow:0 6px 24px rgba(51,44,34,.18); padding:12px 16px; max-width:340px; display:none; line-height:1.75}
  .anno-popup .aw{font-family:var(--font-kai); font-weight:700; color:var(--red-deep); font-size:calc(17px*var(--fs)); margin-bottom:4px}
  .anno-popup .an{color:var(--ink); font-size:calc(14.5px*var(--fs))}
  .anno-popup::after{content:''; position:absolute; top:-7px; left:20px; border-left:7px solid transparent; border-right:7px solid transparent; border-bottom:7px solid var(--gold)}

  /* 视频伪全屏 */
  .video-fs-overlay{position:fixed; top:0; left:0; width:100vw; height:100vh; background:#000; z-index:9999; display:none; align-items:center; justify-content:center}
  .video-fs-overlay.active{display:flex}
  .video-fs-overlay iframe{width:100%; height:100%; max-width:100%; max-height:100%; border:0}
  .video-fs-close{position:absolute; top:16px; right:16px; z-index:10000; background:rgba(0,0,0,.65); color:#fff; border:1px solid rgba(255,255,255,.3); border-radius:8px; padding:8px 18px; cursor:pointer; font-size:14px; letter-spacing:1px; transition:.2s}
  .video-fs-close:hover{background:rgba(0,0,0,.85)}
'''

# ============ JS 模板 ============
def make_js(fs_key):
    return r'''
<script>
(function(){
  'use strict';

  /* ---------- 导航高亮 ---------- */
  var secs = document.querySelectorAll('main section[id]');
  var navA = document.querySelectorAll('.nav a[href^="#"]');
  function setActive(id){
    navA.forEach(function(a){ a.classList.toggle('on', a.getAttribute('href') === '#' + id); });
  }
  if ('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){ if (e.isIntersecting) setActive(e.target.id); });
    }, {rootMargin:'-30% 0px -60% 0px'});
    secs.forEach(function(s){ io.observe(s); });
  }
  window.addEventListener('scroll', function(){
    var top = document.getElementById('topBtn');
    top.style.opacity = (window.scrollY > 500) ? '1' : '0';
  }, {passive:true});
  document.getElementById('topBtn').addEventListener('click', function(){ window.scrollTo({top:0, behavior:'smooth'}); });

  /* ---------- 背诵模式 ---------- */
  var btnRecite = document.getElementById('btnRecite');
  var btnShowAll = document.getElementById('btnShowAll');
  var reciting = false;
  var ft = document.getElementById('fulltext');
  var lines = ft.querySelectorAll('.pl');
  lines.forEach(function(line){
    line.dataset.orig = line.innerHTML;
    line.dataset.full = line.textContent.trim();
    line.addEventListener('click', function(){
      if (!reciting) return;
      if (line.dataset.shown === '1'){
        renderReciteLine(line);
      } else {
        var full = line.dataset.full;
        var firstIdx = 0;
        while (firstIdx < full.length && /[\s\u3000-\u303f\uff00-\uffef\u0020-\u002f\u003a-\u0040\u005b-\u0060\u007b-\u007e]/.test(full.charAt(firstIdx))) {
          firstIdx++;
        }
        line.innerHTML = '<span class="rh">' + full.substring(0, firstIdx + 1) + '</span>' +
          '<span class="rb">' + full.slice(firstIdx + 1) + '</span>';
        line.dataset.shown = '1';
      }
    });
  });
  function renderReciteLine(line){
    var full = line.dataset.full;
    var firstIdx = 0;
    while (firstIdx < full.length && /[\s\u3000-\u303f\uff00-\uffef\u0020-\u002f\u003a-\u0040\u005b-\u0060\u007b-\u007e]/.test(full.charAt(firstIdx))) {
      firstIdx++;
    }
    var hintChar = firstIdx < full.length ? full.charAt(firstIdx) : full.charAt(0);
    var prefix = full.substring(0, firstIdx);
    line.innerHTML = '<span class="rh">' + prefix + hintChar + '</span>' +
      '<span class="rb">' + new Array(full.length - firstIdx).join('\uff3f') + '\uff3f</span>';
    line.dataset.shown = '0';
  }
  btnRecite.addEventListener('click', function(){
    reciting = !reciting;
    btnRecite.textContent = reciting ? '\u539f\u6587' : '\u80cc\u8bf5';
    btnRecite.classList.toggle('off', !reciting);
    btnShowAll.style.display = reciting ? '' : 'none';
    var ft = document.getElementById('fulltext');
    var vl = document.getElementById('verseList');
    if (reciting){
      ft.style.display = '';
      vl.style.display = 'none';
      lines.forEach(function(l){ l.classList.add('reciteline'); renderReciteLine(l); });
    } else {
      ft.style.display = 'none';
      vl.style.display = '';
      lines.forEach(function(l){ l.classList.remove('reciteline'); l.innerHTML = l.dataset.orig; });
    }
  });
  btnShowAll.addEventListener('click', function(){
    var allShown = lines[0] && lines[0].dataset.shown === '1';
    lines.forEach(function(l){
      if (allShown){ renderReciteLine(l); }
      else { l.innerHTML = '<span class="rh">' + l.dataset.full.charAt(0) + '</span>' +
        '<span class="rb">' + l.dataset.full.slice(1) + '</span>';
        l.dataset.shown = '1'; }
    });
    btnShowAll.textContent = allShown ? '\u663e\u793a\u5168\u90e8' : '\u9690\u85cf\u5168\u90e8';
  });

  /* ---------- 正文字体大小 ---------- */
  var fsSel = document.getElementById('fsSel');
  var curFs = localStorage.getItem('''' + fs_key + r''') || '100';
  fsSel.value = curFs;
  document.body.setAttribute('data-fs', curFs);
  fsSel.addEventListener('change', function(){
    document.body.setAttribute('data-fs', this.value);
    try { localStorage.setItem('''' + fs_key + r''', this.value); } catch(e){}
  });

  /* ---------- 一键展开/收起 ---------- */
  var btnAll = document.getElementById('btnAll');
  var allOpen = false;
  btnAll.addEventListener('click', function(){
    allOpen = !allOpen;
    document.querySelectorAll('.verse .v-more').forEach(function(d){ d.open = allOpen; });
    btnAll.textContent = allOpen ? '\u6536\u8d77' : '\u5c55\u5f00';
  });

  /* ---------- 视频伪全屏 ---------- */
  document.querySelectorAll('.fsbtn').forEach(function(btn){
    btn.addEventListener('click', function(){
      var f = document.getElementById(btn.dataset.target);
      if (!f) return;
      var overlay = document.createElement('div');
      overlay.className = 'video-fs-overlay active';
      var closeBtn = document.createElement('button');
      closeBtn.className = 'video-fs-close';
      closeBtn.textContent = '\u9000\u51fa\u5168\u5c4f (Esc)';
      overlay.appendChild(closeBtn);
      var parent = f.parentNode;
      var placeholder = document.createElement('span');
      placeholder.style.display = 'none';
      placeholder.id = f.id + '_ph';
      parent.insertBefore(placeholder, f);
      overlay.appendChild(f);
      document.body.appendChild(overlay);
      document.body.style.overflow = 'hidden';
      function closeFs(){
        parent.insertBefore(f, placeholder);
        parent.removeChild(placeholder);
        if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
        document.body.style.overflow = '';
        document.removeEventListener('keydown', escHandler);
      }
      function escHandler(e){ if(e.key === 'Escape') closeFs(); }
      closeBtn.addEventListener('click', closeFs);
      document.addEventListener('keydown', escHandler);
    });
  });

  /* ---------- 原文注释点击弹窗 ---------- */
  var annoPopup = document.getElementById('annoPopup');
  var annoW = document.getElementById('annoW');
  var annoN = document.getElementById('annoN');
  var activeAnno = null;
  document.addEventListener('click', function(e){
    var word = e.target.closest('.anno-word');
    if(word){
      e.stopPropagation();
      if(activeAnno) activeAnno.classList.remove('active');
      activeAnno = word;
      word.classList.add('active');
      annoW.textContent = word.textContent;
      annoN.textContent = word.dataset.note;
      annoPopup.style.display = 'block';
      var rect = word.getBoundingClientRect();
      var top = rect.bottom + 10;
      var left = rect.left;
      var pw = annoPopup.offsetWidth || 300;
      if(left + pw > window.innerWidth - 12) left = window.innerWidth - pw - 12;
      if(left < 12) left = 12;
      if(top + annoPopup.offsetHeight > window.innerHeight - 12){
        top = rect.top - annoPopup.offsetHeight - 10;
      }
      annoPopup.style.top = top + 'px';
      annoPopup.style.left = left + 'px';
    } else if(!e.target.closest('#annoPopup')){
      annoPopup.style.display = 'none';
      if(activeAnno){ activeAnno.classList.remove('active'); activeAnno = null; }
    }
  });
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape' && annoPopup.style.display === 'block'){
      annoPopup.style.display = 'none';
      if(activeAnno){ activeAnno.classList.remove('active'); activeAnno = null; }
    }
  });
  window.addEventListener('scroll', function(){
    if(annoPopup.style.display === 'block' && activeAnno){
      var rect = activeAnno.getBoundingClientRect();
      var top = rect.bottom + 10;
      var left = rect.left;
      var pw = annoPopup.offsetWidth || 300;
      if(left + pw > window.innerWidth - 12) left = window.innerWidth - pw - 12;
      if(left < 12) left = 12;
      annoPopup.style.top = top + 'px';
      annoPopup.style.left = left + 'px';
    }
  }, {passive:true});

  /* ---------- 听写模式 ---------- */
  var dictate = document.getElementById('dictate');
  var dictMode = document.getElementById('dictMode');
  var dictProgress = document.getElementById('dictProgress');
  var dictPy = document.getElementById('dictPy');
  var dictLine = document.getElementById('dictLine');
  var dictHint = document.getElementById('dictHint');
  var dictAnsBox = document.getElementById('dictAnsBox');
  var dictWord = document.getElementById('dictWord');
  var dictTip = document.getElementById('dictTip');
  var dictShow = document.getElementById('dictShow');
  var dictNext = document.getElementById('dictNext');
  var dictPrev = document.getElementById('dictPrev');
  var dictExit = document.getElementById('dictExit');
  var dictFsMinus = document.getElementById('dictFsMinus');
  var dictFsPlus = document.getElementById('dictFsPlus');
  var dictScale = parseFloat(localStorage.getItem('dict_ds')) || 1.25;
  dictate.style.setProperty('--ds', dictScale);
  dictFsMinus.addEventListener('click', function(){ dictScale = Math.max(0.8, dictScale - 0.1); dictate.style.setProperty('--ds', dictScale); try{localStorage.setItem('dict_ds', dictScale);}catch(e){} });
  dictFsPlus.addEventListener('click', function(){ dictScale = Math.min(1.8, dictScale + 0.1); dictate.style.setProperty('--ds', dictScale); try{localStorage.setItem('dict_ds', dictScale);}catch(e){} });
  var dictState = null;

  function dictShuffle(a){ var b = a.slice(); for (var i = b.length - 1; i > 0; i--){ var j = Math.floor(Math.random() * (i + 1)); var t = b[i]; b[i] = b[j]; b[j] = t; } return b; }

  document.querySelectorAll('#practice .ptools button').forEach(function(btn){
    btn.addEventListener('click', function(){
      var src = (btn.dataset.mode === 'word') ? DICT_WORDS : DICT_NOTES;
      var list = btn.dataset.rand ? dictShuffle(src).slice(0, 5) : src.slice();
      dictState = { mode: btn.dataset.mode, list: list, i: 0 };
      dictate.hidden = false;
      var p = document.documentElement.requestFullscreen();
      if (p && p.catch) p.catch(function(){});
      dictRender();
    });
  });

  function dictRender(){
    var s = dictState, it = s.list[s.i];
    dictMode.textContent = (s.mode === 'word') ? '\u5b57\u5f62\u542c\u5199' : '\u6ce8\u91ca\u542c\u5199';
    dictProgress.textContent = '\u7b2c ' + (s.i + 1) + ' / ' + s.list.length + ' \u9898';
    if (s.mode === 'word'){
      dictPy.textContent = it.py;
      dictLine.textContent = it.q;
      dictHint.textContent = '\u2014\u2014 \u9ed8\u5199\u7a7a\u683c\u4e2d\u7684\u5b57 \u2014\u2014';
      dictWord.textContent = it.w;
      dictTip.textContent = '\u6613\u9519\uff1a' + it.tip;
    } else {
      dictPy.textContent = it.w;
      dictLine.textContent = it.q;
      dictHint.textContent = '\u2014\u2014 \u9ed8\u5199\u91ca\u4e49 \u2014\u2014';
      dictWord.textContent = it.a;
      dictTip.textContent = '';
    }
    dictAnsBox.hidden = true;
    dictShow.textContent = '\u663e\u793a\u7b54\u6848';
    dictNext.textContent = (s.i === s.list.length - 1) ? '\u5b8c\u6210' : '\u4e0b\u4e00\u9898';
    dictPrev.disabled = (s.i === 0);
    dictPrev.style.opacity = (s.i === 0) ? '0.4' : '1';
  }

  dictShow.addEventListener('click', function(){
    if (!dictState) return;
    if (dictAnsBox.hidden){ dictAnsBox.hidden = false; dictShow.textContent = '\u9690\u85cf\u7b54\u6848'; }
    else { dictAnsBox.hidden = true; dictShow.textContent = '\u663e\u793a\u7b54\u6848'; }
  });
  dictNext.addEventListener('click', function(){
    if (!dictState) return;
    if (dictState.i >= dictState.list.length - 1){ dictClose(); return; }
    dictState.i++; dictRender();
  });
  dictPrev.addEventListener('click', function(){
    if (!dictState) return;
    if (dictState.i <= 0) return;
    dictState.i--; dictRender();
  });
  dictExit.addEventListener('click', dictClose);
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && dictate && !dictate.hidden) dictClose(); });
  function dictClose(){
    dictate.hidden = true; dictState = null;
    var p = document.exitFullscreen();
    if (p && p.catch) p.catch(function(){});
  }

  /* ---------- 打印 ---------- */
  var saved = [];
  window.addEventListener('beforeprint', function(){
    saved = [];
    document.querySelectorAll('.verse details').forEach(function(d){ saved.push([d, d.open]); d.open = true; });
  });
  window.addEventListener('afterprint', function(){
    saved.forEach(function(p){ p[0].open = p[1]; }); saved = [];
  });
  document.getElementById('btnPrint').addEventListener('click', function(){ window.print(); });
})();
</script>
'''

# ============ 辅助函数 ============
def annotate(sentence, notes):
    """给句子加注释span。notes: [(词, 注释), ...]，按词长降序匹配"""
    result = sentence
    # 按词长降序，避免短词先匹配
    sorted_notes = sorted(notes, key=lambda x: len(x[0]), reverse=True)
    used = set()
    for word, note in sorted_notes:
        if word in used:
            continue
        # 检查是否已被span包裹
        idx = result.find(word)
        while idx != -1:
            # 检查前后是否在span标签内
            before = result[:idx]
            if before.rfind('<span') > before.rfind('</span>'):
                idx = result.find(word, idx + 1)
                continue
            span = '<span class="anno-word" data-note="' + note.replace('"', '&quot;') + '">' + word + '</span>'
            result = result[:idx] + span + result[idx + len(word):]
            break
    return result

def make_verse(idx, sentence, notes, content, technique):
    """生成一个解读卡片"""
    annotated = annotate(sentence, notes)
    return f'''      <div class="verse" id="l{idx}" data-i="{idx-1}">
        <div class="v-top"><span class="v-no">{idx}</span><div class="v-line">{annotated}</div></div>
        <details class="v-more">
          <summary>内容 · 手法</summary>
          <div class="d-body">
            <div class="v-sec"><b class="v-label">内容概括</b>
              <div class="v-trans">{content}</div>
            </div>
            <div class="v-sec"><b class="v-label">手法分析</b>
              <div class="d-body"><p>{technique}</p></div>
            </div>
          </div>
        </details>
      </div>'''

def make_part_head(num, title, rng):
    return f'''      <div class="part-head"><span class="p-num">{num}</span><h3>{title}</h3><span class="range">{rng}</span></div>'''

def make_part_overview(text):
    return f'''      <div class="part-overview">{text}</div>'''

def make_fulltext(paragraphs):
    """生成背诵区全文"""
    items = []
    for p in paragraphs:
        items.append(f'    <div class="pl">{p}</div>')
    return '\n'.join(items)

def make_video(bv, title, fid):
    return f'''        <div class="media">
          <h4>{title}</h4>
          <iframe id="{fid}" src="https://player.bilibili.com/player.html?bvid={bv}&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="{title}"></iframe>
          <a href="https://www.bilibili.com/video/{bv}" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="{fid}">全屏播放</button>
        </div>'''

def make_acc_item(w, d):
    return f'''        <div class="acc-item"><div class="acc-w">{w}</div><div class="acc-d">{d}</div></div>'''

def make_acc_cat(title, items, sub=None):
    """items: list of (w, d) or acc-sub string"""
    html = f'''      <div class="acc-cat">
        <h3>{title}</h3>
'''
    if sub:
        html += f'        <div class="acc-sub">{sub}</div>\n'
    for w, d in items:
        html += make_acc_item(w, d) + '\n'
    html += '      </div>'
    return html

print("模板加载完成")
