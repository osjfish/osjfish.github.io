/* 《精忠·丰碑》六分钟节目设计方案 PPT 生成脚本
 * 运行：NODE_PATH=$(npm root -g) node 生成PPT.js
 */
const pptxgen = require("pptxgenjs");
const P = new pptxgen();
P.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
P.author = "节目筹备组";
P.title = "《精忠·丰碑》六分钟节目设计方案";

const W = 13.33, M = 0.5;
const C = {
  dark: "2B1214", dark2: "3A1D20",
  red: "A61B29", redDeep: "7C1420",
  gold: "C9A227", goldSoft: "E2C25C",
  ink: "262626", muted: "8C8C8C",
  tint: "F8F0F0", tint2: "FBF7F7", line: "E5D8D8",
  white: "FFFFFF", dim: "D9C4C4",
};
const F = "微软雅黑";

const T = (s, t, o) => s.addText(t, Object.assign({ fontFace: F }, o));
const star = (s, x, y, w, h, color) => s.addShape("star5", { x, y, w, h, fill: { color } });
const rect = (s, o) => s.addShape("rect", o);
const rrect = (s, o) => s.addShape("roundRect", o);
const hline = (s, x, y, w, color, wd, dash) =>
  s.addShape("line", { x, y, w, h: 0, line: { color, width: wd || 1, dashType: dash || "solid" } });

let pageNum = 0;
const TOTAL = 13;
function footer(s) {
  pageNum++;
  if (pageNum === 1 || pageNum === TOTAL) return;
  T(s, String(pageNum).padStart(2, "0") + " / " + TOTAL,
    { x: 11.9, y: 7.02, w: 0.95, h: 0.32, fontSize: 12, color: C.muted, align: "right" });
}
function header(s, kick, title) {
  s.background = { color: C.white };
  star(s, M, 0.56, 0.27, 0.27, C.gold);
  T(s, kick, { x: 0.92, y: 0.5, w: 9.5, h: 0.38, fontSize: 13, bold: true, color: C.gold, charSpacing: 2 });
  T(s, title, { x: M, y: 0.92, w: 12.33, h: 0.72, fontSize: 36, bold: true, color: C.ink });
}

/* ---------- 表格单元格样式 ---------- */
const hd = t => ({ text: t, options: { fill: { color: C.red }, color: C.white, bold: true, fontSize: 12.5, align: "center", valign: "middle" } });
const role = t => ({ text: t, options: { color: t === "音效" ? C.muted : C.red, bold: true, fontSize: 12, align: "center", valign: "middle" } });
const say = t => ({ text: t, options: { color: C.ink, fontSize: 12.5, align: "left", valign: "middle" } });
const tip = t => ({ text: t, options: { color: C.muted, fontSize: 12, align: "left", valign: "middle" } });
const tbOpt = (x, y, colW, rowH) => ({ x, y, w: colW.reduce((a, b) => a + b), colW, rowH, border: { pt: 0.5, color: C.line }, fontFace: F, margin: 0.06, valign: "middle" });

/* ================= S1 封面 ================= */
(() => {
  const s = P.addSlide();
  s.background = { color: C.dark };
  star(s, 8.7, 1.3, 4.7, 4.7, C.dark2);
  star(s, 0.55, 1.42, 0.36, 0.36, C.gold);
  T(s, "班级合唱比赛 · 六分钟节目设计方案", { x: 0.55, y: 2.0, w: 9, h: 0.4, fontSize: 16, bold: true, color: C.gold, charSpacing: 2 });
  T(s, "《精忠·丰碑》", { x: 0.5, y: 2.42, w: 11.5, h: 1.35, fontSize: 60, bold: true, color: C.white });
  T(s, "情景朗诵《丰碑》 × 合唱《精忠报国》", { x: 0.55, y: 3.95, w: 11, h: 0.55, fontSize: 22, bold: true, color: C.goldSoft });
  T(s, "朗诵与合唱有机融合 · 至少一个部分与长征有关 · 全程 6 分钟以内", { x: 0.55, y: 4.62, w: 11.5, h: 0.45, fontSize: 15, color: C.dim });
  T(s, "4 排合唱队形　　　4 支话筒　　　可预录音轨对口型", { x: 0.55, y: 6.35, w: 8.5, h: 0.4, fontSize: 13, color: C.dim });
  T(s, "节目筹备组 · 2026 年 9 月", { x: 8.9, y: 6.35, w: 3.9, h: 0.4, fontSize: 13, color: C.dim, align: "right" });
  s.addNotes("封面。节目名把两个作品各取一字：《丰碑》的“丰碑”与《精忠报国》的“精忠”。");
  footer(s);
})();

/* ================= S2 节目概览 ================= */
(() => {
  const s = P.addSlide();
  header(s, "一座丰碑 × 一曲报国", "节目概览");
  const stats = [
    ["6′00″", "总时长（上限）", true],
    ["1 + 1", "朗诵 × 合唱", false],
    ["4 + 2", "领诵 + 领唱（人）", false],
    ["4 × 13", "合唱队形（以52人计）", false],
    ["4", "话筒（支）", false],
  ];
  const cw = 12.33 / 5;
  stats.forEach((st, i) => {
    const x = M + i * cw;
    T(s, st[0], { x, y: 1.86, w: cw, h: 0.8, fontSize: 40, bold: true, color: st[2] ? C.gold : C.red, align: "center" });
    T(s, st[1], { x, y: 2.72, w: cw, h: 0.34, fontSize: 13, color: C.muted, align: "center" });
    if (i) s.addShape("line", { x, y: 2.0, w: 0, h: 0.95, line: { color: C.line, width: 0.75 } });
  });
  rect(s, { x: 0, y: 3.4, w: W, h: 1.06, fill: { color: C.tint } });
  T(s, "立意：以长征雪山上军需处长的牺牲讲“忠”，以《精忠报国》的歌声答“魂”——一座晶莹的丰碑，一曲嘹亮的报国。",
    { x: 0.7, y: 3.4, w: 11.93, h: 1.06, fontSize: 18, bold: true, color: C.ink, valign: "middle" });
  const reqs = [
    ["命题要求 ①", "至少一个部分与长征有关", "朗诵《丰碑》——红军翻越雪山、军需处长冻亡的真实故事，课文级红色经典。"],
    ["命题要求 ②", "包含合唱与朗诵，有机融合", "前奏齐诵转场接唱；间奏齐诵《过雪山草地》二次点题；尾声敬礼定格同台收束。"],
    ["命题要求 ③", "从上场到下场不超过 6 分钟", "朗诵 1′45″ ＋ 合唱 3′28″ ＋ 暗场/转场/定格 42″ ＝ 5′55″，留安全余量。"],
  ];
  reqs.forEach((r, i) => {
    const x = M + i * 4.22;
    rrect(s, { x, y: 4.85, w: 3.89, h: 1.75, rectRadius: 0.06, fill: { color: C.white }, line: { color: C.line, width: 1 } });
    T(s, r[0] + "　" + r[1], { x: x + 0.24, y: 5.02, w: 3.45, h: 0.62, fontSize: 14, bold: true, color: C.red });
    T(s, r[2], { x: x + 0.24, y: 5.62, w: 3.45, h: 0.9, fontSize: 12.5, color: C.ink });
  });
  footer(s);
})();

/* ================= S3 创意阐述 ================= */
(() => {
  const s = P.addSlide();
  header(s, "选题逻辑", "创意阐述");
  // 左右来源
  const box = (x, title, l1, l2, hit) => {
    rrect(s, { x, y: 2.05, w: 3.62, h: 1.95, rectRadius: 0.06, fill: { color: C.white }, line: { color: C.red, width: 1.25 } });
    T(s, title, { x: x + 0.25, y: 2.25, w: 3.15, h: 0.45, fontSize: 17, bold: true, color: C.red });
    T(s, l1, { x: x + 0.25, y: 2.75, w: 3.15, h: 0.34, fontSize: 12.5, color: C.ink });
    T(s, l2, { x: x + 0.25, y: 3.09, w: 3.15, h: 0.34, fontSize: 12.5, color: C.ink });
    T(s, hit, { x: x + 0.25, y: 3.5, w: 3.15, h: 0.34, fontSize: 12.5, bold: true, color: C.gold });
  };
  box(0.7, "《丰碑》· 情景朗诵", "长征 · 雪山 · 军需处长", "过雪山真实故事，课文级经典", "命中命题：与长征有关");
  box(9.01, "《精忠报国》· 合唱", "豪情 · 忠魂 · 报国志", "全民传唱的主旋律军歌风", "命中命题：主旋律 · 正能量");
  // 中心圆 + 箭头
  s.addShape("ellipse", { x: 5.71, y: 2.07, w: 1.92, h: 1.92, fill: { color: C.red }, line: { color: C.gold, width: 2 } });
  T(s, "精忠\n丰碑", { x: 5.71, y: 2.07, w: 1.92, h: 1.92, fontSize: 19, bold: true, color: C.white, align: "center", valign: "middle" });
  s.addShape("line", { x: 4.44, y: 3.03, w: 1.15, h: 0, line: { color: C.red, width: 2, endArrowType: "triangle" } });
  s.addShape("line", { x: 7.74, y: 3.03, w: 1.15, h: 0, line: { color: C.red, width: 2, beginArrowType: "triangle" } });
  // 三个融合机制
  const mech = [
    ["01", "前奏齐诵转场", "“红军不怕远征难”压着鼓点起，朗诵无缝接唱，避免报幕式割裂。"],
    ["02", "间奏二次点题", "20″间奏齐诵“红军都是钢铁汉”，长征题材再点一次，呼应最严命题。"],
    ["03", "尾声敬礼定格", "尾句渐慢收拍，全体注目礼定格5″，朗诵者与合唱队同台收束。"],
  ];
  mech.forEach((m, i) => {
    const x = M + i * 4.22;
    T(s, m[0], { x, y: 4.45, w: 1.2, h: 0.55, fontSize: 28, bold: true, color: C.gold });
    T(s, m[1], { x, y: 5.05, w: 3.8, h: 0.38, fontSize: 15, bold: true, color: C.ink });
    T(s, m[2], { x, y: 5.45, w: 3.8, h: 0.75, fontSize: 12.5, color: C.muted });
  });
  hline(s, M, 6.5, 12.33, C.line, 0.75);
  T(s, "时长账：朗诵 1′45″ ＋ 合唱 3′28″ ＋ 暗场/转场/定格 42″ ＝ 5′55″，与第 4 页时间轴一致。", { x: M, y: 6.62, w: 12.33, h: 0.35, fontSize: 12.5, color: C.muted });
  footer(s);
})();

/* ================= S4 六分钟时间轴 ================= */
(() => {
  const s = P.addSlide();
  header(s, "全流程 5′55″", "六分钟时间轴");
  const segs = [ // [秒, 名称, 颜色, 文字色]
    [15, "暗场", C.dark2, C.white],
    [105, "朗诵《丰碑》", C.red, C.white],
    [10, "转场", C.gold, C.ink],
    [208, "合唱《精忠报国》（含间奏齐诵）", C.redDeep, C.white],
    [17, "定格", "5A2A2E", C.white],
  ];
  const total = segs.reduce((a, b) => a + b[0], 0); // 355
  const x0 = M, scale = 12.33 / total;
  let cx = x0;
  segs.forEach((g, i) => {
    const w = g[0] * scale;
    rect(s, { x: cx, y: 2.1, w, h: 0.85, fill: { color: g[2] } });
    if (w > 1.6) T(s, g[1], { x: cx + 0.12, y: 2.1, w: w - 0.24, h: 0.85, fontSize: 13.5, bold: true, color: g[3], valign: "middle" });
    cx += w;
  });
  // 小段名称放条上方
  T(s, "暗场 15″", { x: 0.5, y: 1.62, w: 1.6, h: 0.34, fontSize: 13, bold: true, color: C.ink });
  s.addShape("line", { x: 0.76, y: 1.96, w: 0, h: 0.14, line: { color: C.muted, width: 0.75 } });
  T(s, "齐诵转场 10″", { x: 4.3, y: 1.62, w: 1.9, h: 0.34, fontSize: 13, bold: true, color: C.ink, align: "center" });
  s.addShape("line", { x: 5.195, y: 1.96, w: 0, h: 0.14, line: { color: C.muted, width: 0.75 } });
  T(s, "定格 17″", { x: 11.68, y: 1.62, w: 1.7, h: 0.34, fontSize: 13, bold: true, color: C.ink, align: "center" });
  s.addShape("line", { x: 12.53, y: 1.96, w: 0, h: 0.14, line: { color: C.muted, width: 0.75 } });
  // 时间刻度（0:15/2:10 与相邻刻度仅差10秒，错一行避免重叠）
  const ticks = [["0:00", 0.5, "left"], ["2:00", 4.67, "left"], ["5:55", 12.83, "right"]];
  ticks.forEach(tk => T(s, tk[0], { x: tk[1] - 0.5, y: 3.0, w: 1.0, h: 0.3, fontSize: 12, color: C.muted, align: tk[2] }));
  [["0:15", 1.02], ["2:10", 5.02]].forEach(tk => {
    s.addShape("line", { x: tk[1], y: 2.97, w: 0, h: 0.34, line: { color: C.muted, width: 0.75 } });
    T(s, tk[0], { x: tk[1] - 0.35, y: 3.31, w: 1.0, h: 0.3, fontSize: 12, color: C.muted });
  });
  // 五列说明
  const cols = [
    ["① 暗场 0:00–0:15", "风雪声渐起，LED雪山剪影亮起，暗场起光。"],
    ["② 朗诵 0:15–2:00", "领诵4人讲述军需处长故事，群诵三次插入。"],
    ["③ 转场 2:00–2:10", "“红军不怕远征难”压鼓点，全体起唱。"],
    ["④ 合唱 2:10–5:38", "主歌→副歌→间奏齐诵20″→主歌→副歌。"],
    ["⑤ 定格 5:38–5:55", "尾句渐慢，全体注目礼定格5″，音乐收。"],
  ];
  cols.forEach((c, i) => {
    const x = M + i * 2.466;
    T(s, c[0], { x, y: 3.55, w: 2.32, h: 0.36, fontSize: 13, bold: true, color: C.ink });
    T(s, c[1], { x, y: 3.93, w: 2.32, h: 0.85, fontSize: 12, color: C.muted });
  });
  // 验收标准
  star(s, 5.0, 6.32, 0.3, 0.3, C.gold);
  T(s, "彩排验收：全程掐表 5′45″ ± 15″", { x: 5.45, y: 6.24, w: 5.2, h: 0.45, fontSize: 20, bold: true, color: C.red });
  s.addNotes("时间轴按秒对齐预录音轨：风雪声15″、朗诵105″、转场10″、合唱208″（原曲3′28″）、定格17″。");
  footer(s);
})();

/* ================= S5 朗诵分工稿（上） ================= */
(() => {
  const s = P.addSlide();
  header(s, "李本深《丰碑》改编", "朗诵分工稿（上）：风雪山林");
  const rows = [
    ["音效", "风雪声渐起 5 秒；LED 亮出雪山剪影，全场暗场起光。", "音乐先行，压住安静"],
    ["女领①", "1935 年冬，云中山，大雪封山。", "声音清冷，字字落地"],
    ["男领①", "红军队伍在冰天雪地里艰难地前进。狂风呼啸，大雪纷飞，似乎要吞掉这支装备很差的队伍。", "沉缓厚重，压过风声"],
    ["女领②", "将军把马让给了重伤员。他率领战士们向前挺进，在冰雪中为后续部队开辟通路。", "平稳叙述，渐入情境"],
    ["男领②", "这支队伍能不能经受住这样严峻的考验呢？将军思索着——", "自问留白，放慢半拍"],
    ["群诵", "风，更狂了。雪，更大了。", "四排低声，由弱渐起"],
    ["女领①", "队伍忽然放慢了速度——前面有人冻死了！", "骤然揪起，语速加快"],
    ["男领①", "一个冻僵的老战士，依靠光秃秃的树干坐着。他一动不动，好似一尊塑像，身上落满了雪。", "最慢一段，逐字描摹"],
    ["女领②", "单薄破旧的衣服，紧紧地贴在他的身上。他的神态，十分镇定，十分安详。", "轻声细数，带着心疼"],
  ];
  const data = [[hd("角色"), hd("台词"), hd("表演处理")]];
  rows.forEach(r => data.push([role(r[0]), say(r[1]), tip(r[2])]));
  s.addTable(data, tbOpt(M, 1.72, [1.35, 7.6, 3.38], [0.36, 0.44, 0.44, 0.64, 0.44, 0.44, 0.44, 0.44, 0.6, 0.44]));
  T(s, "改编自李本深《丰碑》（统编教材课文，又名《军需处长》），为控时略作删减；领诵站位见第 8 页队形图。", { x: M, y: 6.6, w: 12.33, h: 0.35, fontSize: 12, color: C.muted });
  s.addNotes("群诵=合唱四排齐声。三次群诵分别是：“风更狂了”“没有人回答”“晶莹的丰碑”。");
  footer(s);
})();

/* ================= S6 朗诵分工稿（下） ================= */
(() => {
  const s = P.addSlide();
  header(s, "李本深《丰碑》改编", "朗诵分工稿（下）：晶莹的丰碑");
  const rows = [
    ["男领②", "把军需处长给我叫来！为什么不给他发棉衣？！", "怒音放开，全篇最响之一"],
    ["群诵", "呼啸的狂风淹没了将军的话音。没有人回答，也没有人走开。", "低而齐，风声衬人声"],
    ["女领①", "有人小声告诉将军——", "欲言又止，吊住全场"],
    ["男领①", "……他就是军需处长。", "极轻极慢，静场两秒"],
    ["男领②", "将军愣住了，久久地站在雪地里。他深深吸了一口气，缓缓举起右手——向军需处长敬了一个军礼！", "随句敬礼，全体注目"],
    ["女领②", "风更狂了，雪更大了。大雪很快覆盖了他——他，成了一座晶莹的丰碑！", "“晶莹的丰碑”一字一顿"],
    ["群诵", "晶莹的——丰碑——", "回声式，由弱到强"],
    ["男领①", "那无数沉重而坚定的脚步声，似乎在告诉人们：如果胜利不属于这样的队伍，还会属于谁呢？！", "层层推高，问句砸实"],
    ["全体", "红军不怕远征难，万水千山只等闲！", "最强音；《精忠报国》鼓点从此句压进"],
  ];
  const data = [[hd("角色"), hd("台词"), hd("表演处理")]];
  rows.forEach(r => data.push([role(r[0]), say(r[1]), tip(r[2])]));
  s.addTable(data, tbOpt(M, 1.72, [1.35, 7.6, 3.38], [0.36, 0.44, 0.44, 0.44, 0.44, 0.64, 0.6, 0.44, 0.62, 0.5]));
  T(s, "末句“红军不怕远征难”出自毛泽东《七律·长征》，与《精忠报国》前奏战鼓重叠，完成朗诵→合唱的无缝转场。", { x: M, y: 6.7, w: 12.33, h: 0.35, fontSize: 12, color: C.muted });
  s.addNotes("“他就是军需处长”之后必须留足2秒静场，这是全篇最大的泪点，不要抢。");
  footer(s);
})();

/* ================= S7 合唱编排 ================= */
(() => {
  const s = P.addSlide();
  header(s, "萧华《长征组歌》点题", "合唱编排：《精忠报国》");
  const flow = [
    ["① 前奏 · 齐诵压鼓点", "15″"],
    ["② 主歌一 · 男领唱", "35″"],
    ["③ 副歌一 · 全体合唱", "40″"],
    ["④ 间奏 · 插入齐诵", "20″"],
    ["⑤ 主歌二 · 可删控时", "40″"],
    ["⑥ 副歌二＋尾句 · 定格", "58″"],
  ];
  flow.forEach((f, i) => {
    const y = 1.85 + i * 0.82;
    rrect(s, { x: M, y, w: 4.7, h: 0.7, rectRadius: 0.05, fill: { color: i === 5 ? C.tint : C.tint2 }, line: { color: C.line, width: 0.75 } });
    T(s, f[0], { x: 0.72, y: y + 0.05, w: 3.35, h: 0.6, fontSize: 14, bold: true, color: i === 5 ? C.red : C.ink, valign: "middle" });
    T(s, f[1], { x: 4.05, y: y + 0.05, w: 1.0, h: 0.6, fontSize: 12.5, bold: true, color: C.gold, align: "right", valign: "middle" });
  });
  // 右：间奏齐诵卡
  rect(s, { x: 5.6, y: 1.85, w: 7.23, h: 2.0, fill: { color: C.tint } });
  T(s, "间奏齐诵（二次点题长征）——《长征组歌·过雪山草地》萧华词", { x: 5.85, y: 2.0, w: 6.75, h: 0.36, fontSize: 14, bold: true, color: C.red });
  T(s, "雪皑皑，野茫茫，高原寒，炊断粮。红军都是钢铁汉，千锤百炼不怕难！", { x: 5.85, y: 2.42, w: 6.75, h: 0.85, fontSize: 18, bold: true, color: C.ink });
  T(s, "四排齐声，音量盖过间奏旋律；两句在 20″ 间奏内完成，收字正好落在副歌前。", { x: 5.85, y: 3.32, w: 6.75, h: 0.4, fontSize: 12, color: C.muted });
  // 右：控时与删减
  T(s, "控时与删减", { x: 5.6, y: 4.12, w: 4, h: 0.4, fontSize: 15, bold: true, color: C.red });
  s.addText([
    { text: "全曲约 3′28″：彩排若超时，删主歌二，可省约 40″；", options: { bullet: { code: "25B8", indent: 12 }, breakLine: true } },
    { text: "尾句“堂堂中国要让四方来贺”渐慢渐强，收拍全体行注目礼定格 5″；", options: { bullet: { code: "25B8", indent: 12 }, breakLine: true } },
    { text: "合唱队形全程不动，只有领诵在朗诵段进入前区。", options: { bullet: { code: "25B8", indent: 12 } } },
  ], { x: 5.6, y: 4.52, w: 7.23, h: 1.35, fontFace: F, fontSize: 13, color: C.ink, paraSpaceAfter: 6, margin: 0 });
  // 右：领唱与声部
  T(s, "领唱与声部", { x: 5.6, y: 5.95, w: 4, h: 0.4, fontSize: 15, bold: true, color: C.red });
  s.addText([
    { text: "主歌一：男领唱独唱（麦3）；主歌二：男＋女对唱（如保留）；", options: { bullet: { code: "25B8", indent: 12 }, breakLine: true } },
    { text: "副歌：领唱带唱，四排合唱铺底；女声部二声部视排练水平加花。", options: { bullet: { code: "25B8", indent: 12 } } },
  ], { x: 5.6, y: 6.35, w: 7.23, h: 0.9, fontFace: F, fontSize: 13, color: C.ink, paraSpaceAfter: 6, margin: 0 });
  s.addNotes("合唱若用简谱版调性偏低，男领唱可降八度处理；间奏齐诵务必卡在20秒内收字。");
  footer(s);
})();

/* ================= S8 舞台队形 ================= */
(() => {
  const s = P.addSlide();
  header(s, "4 排合唱 × 前区领诵", "舞台队形与调度");
  // 舞台
  rect(s, { x: 0.7, y: 1.6, w: 11.93, h: 4.5, fill: { color: C.tint2 }, line: { color: C.line, width: 1 } });
  hline(s, 0.7, 5.78, 11.93, C.muted, 1, "dash");
  T(s, "台口 · 观众席方向", { x: 4.63, y: 5.84, w: 4, h: 0.3, fontSize: 12, color: C.muted, align: "center" });
  // 图例（舞台内上沿）
  s.addShape("ellipse", { x: 1.05, y: 1.78, w: 0.2, h: 0.2, fill: { color: C.red } });
  T(s, "合唱队员", { x: 1.32, y: 1.72, w: 1.3, h: 0.32, fontSize: 12.5, color: C.ink });
  rect(s, { x: 2.75, y: 1.78, w: 0.2, h: 0.2, fill: { color: C.redDeep } });
  T(s, "领诵 / 领唱", { x: 3.02, y: 1.72, w: 1.5, h: 0.32, fontSize: 12.5, color: C.ink });
  s.addShape("ellipse", { x: 4.65, y: 1.78, w: 0.2, h: 0.2, fill: { color: C.gold } });
  T(s, "话筒", { x: 4.92, y: 1.72, w: 0.9, h: 0.32, fontSize: 12.5, color: C.ink });
  T(s, "朗诵段：领诵 4 人上前区；歌曲段：退回一排两翼", { x: 7.0, y: 1.72, w: 5.4, h: 0.32, fontSize: 12.5, color: C.muted, align: "right" });
  // 四排合唱（下=前）
  const rowColor = ["A61B29", "BE5B63", "D39297", "E5C4C6"];
  const rowName = ["一排（前）", "二排", "三排", "四排（后）"];
  for (let r = 0; r < 4; r++) {
    const y = 4.62 - r * 0.62; // 一排 y=4.62 … 四排 y=2.76
    const x0 = 2.92;
    T(s, rowName[r], { x: 0.9, y: y - 0.02, w: 1.9, h: 0.34, fontSize: 12.5, color: C.muted, align: "right" });
    for (let i = 0; i < 13; i++) {
      s.addShape("ellipse", { x: x0 + i * 0.6, y, w: 0.3, h: 0.3, fill: { color: rowColor[r] } });
    }
  }
  // 前区：领诵（左）领唱（右）
  const leaders = [["女领①", 1.1], ["男领①", 2.8], ["男领唱", 9.2], ["女领唱", 10.9]];
  leaders.forEach((L, i) => {
    rrect(s, { x: L[1], y: 5.05, w: 1.5, h: 0.56, rectRadius: 0.05, fill: { color: i < 2 ? C.red : C.redDeep } });
    T(s, L[0], { x: L[1], y: 5.05, w: 1.5, h: 0.56, fontSize: 12.5, bold: true, color: C.white, align: "center", valign: "middle" });
  });
  const mics = [["麦1", 1.62], ["麦2", 3.32], ["麦3", 9.72], ["麦4", 11.42]];
  mics.forEach(mc => {
    s.addShape("ellipse", { x: mc[1], y: 5.42, w: 0.46, h: 0.46, fill: { color: C.gold } });
    T(s, mc[0], { x: mc[1], y: 5.42, w: 0.46, h: 0.46, fontSize: 12, bold: true, color: C.ink, align: "center", valign: "middle" });
  });
  T(s, "以 52 人为例（4排×13，按实际人数增减）；排面呈微弧形，前排强、后排高；若设指挥，站左前角侧身面对合唱队。",
    { x: M, y: 6.35, w: 12.33, h: 0.35, fontSize: 12.5, color: C.muted });
  s.addNotes("话筒全为立式架：麦1/麦2给领诵，麦3/麦4给领唱。朗诵段领诵从两侧口上前区，避免穿越队形。");
  footer(s);
})();

/* ================= S9 话筒与对口型 ================= */
(() => {
  const s = P.addSlide();
  header(s, "4 支话筒 · 预录音轨", "话筒分配与对口型录音");
  const data = [
    [hd("麦位"), hd("使用人"), hd("备注")],
    [role("麦1 左前"), say("女领诵①"), tip("朗诵主麦；歌曲段收回")],
    [role("麦2 左中"), say("男领诵①"), tip("朗诵主麦；歌曲段收回")],
    [role("麦3 右前"), say("男领唱"), tip("主歌一独唱")],
    [role("麦4 右中"), say("女领唱"), tip("主歌二对唱、副歌领唱")],
  ];
  s.addTable(data, tbOpt(M, 1.85, [1.5, 2.1, 2.5], [0.38, 0.46, 0.46, 0.46, 0.46]));
  rect(s, { x: M, y: 4.35, w: 6.1, h: 1.15, fill: { color: C.tint } });
  T(s, "群诵与合唱不依赖话筒：现场扩声以预录音轨为主，4 支真麦只保领诵领唱。麦1/麦2 在歌曲段收走或让给领唱。",
    { x: 0.72, y: 4.35, w: 5.66, h: 1.15, fontSize: 12.5, color: C.ink, valign: "middle" });
  // 右列：五步流程
  T(s, "对口型录音 · 五步流程", { x: 7.0, y: 1.85, w: 5.83, h: 0.4, fontSize: 15, bold: true, color: C.red });
  const steps = [
    ["1", "定稿 · 标注点位", "把音效、齐诵、起唱的准确时间点写进录音脚本。"],
    ["2", "进场实录", "在演出场地用同一套功放话筒录整条：朗诵＋齐诵＋合唱＋伴奏。"],
    ["3", "混音单轨", "总长 5′40″，首尾各留 2″ 静音；U盘＋手机双备份。"],
    ["4", "对口型排练", "领诵逐句对，群诵小口型，动作卡节拍。"],
    ["5", "现场放带", "报幕后起播；领诵另留一支真麦应急。"],
  ];
  steps.forEach((st, i) => {
    const y = 2.35 + i * 0.92;
    s.addShape("ellipse", { x: 7.0, y, w: 0.42, h: 0.42, fill: { color: C.gold } });
    T(s, st[0], { x: 7.0, y, w: 0.42, h: 0.42, fontSize: 14, bold: true, color: C.ink, align: "center", valign: "middle" });
    T(s, st[1], { x: 7.58, y: y - 0.03, w: 5.2, h: 0.34, fontSize: 13.5, bold: true, color: C.ink });
    T(s, st[2], { x: 7.58, y: y + 0.3, w: 5.2, h: 0.55, fontSize: 12, color: C.muted });
  });
  footer(s);
})();

/* ================= S10 舞美 ================= */
(() => {
  const s = P.addSlide();
  header(s, "雪山与红旗的意象", "舞美：服装 · 造型 · LED");
  const cards = [
    ["服装", [
      "全体深色上装＋红围巾（雪山·红旗意象）",
      "领诵 4 人戴白手套，手势清晰可见",
      "领唱同款另佩徽章或绶带区分",
      "鞋深色统一，忌白鞋抢镜",
    ]],
    ["造型与灯光", [
      "朗诵段合唱肃立，“丰碑”句齐抬头",
      "尾句收拍全体注目礼定格 5″",
      "暗场起光→副歌顶光全亮",
      "若无灯光条件，用 LED 明暗替代",
    ]],
    ["LED 与音效", [
      "背景四段：风雪山林→雪山日出→红旗长城→丰碑剪影",
      "音效：风雪声 15″ 渐入＋战鼓",
      "背景素材见第 11 页资源表",
      "免费音效：爱给网 aigei.com",
    ]],
  ];
  cards.forEach((c, i) => {
    const x = M + i * 4.22;
    rrect(s, { x, y: 1.9, w: 3.89, h: 4.3, rectRadius: 0.06, fill: { color: C.white }, line: { color: C.line, width: 1 } });
    T(s, c[0], { x: x + 0.26, y: 2.12, w: 3.3, h: 0.45, fontSize: 16, bold: true, color: C.red });
    c[1].forEach((it, j) => {
      const y = 2.75 + j * 0.82;
      rect(s, { x: x + 0.28, y: y + 0.09, w: 0.09, h: 0.09, fill: { color: C.gold } });
      T(s, it, { x: x + 0.52, y, w: 3.15, h: 0.78, fontSize: 12.5, color: C.ink });
    });
  });
  hline(s, M, 6.45, 12.33, C.line, 0.75);
  T(s, "LED 播放与音效由 1 名同学跟预录音轨一键触发：同一台电脑、同一份音轨，避免二次对拍。", { x: M, y: 6.58, w: 12.33, h: 0.35, fontSize: 12.5, color: C.muted });
  footer(s);
})();

/* ================= S11 学习资源 ================= */
(() => {
  const s = P.addSlide();
  header(s, "齐越节 · 央视 · B站", "学习资源与模仿对象");
  const rows = [
    ["2021 届齐越节《丰碑》朗诵", "朗诵处理的直接范本", "B站搜索：丰碑 齐越节"],
    ["情景诵演《丰碑》", "舞台调度与情景化", "bilibili.com/video/BV1Dv411H7r1"],
    ["齐越节《我的墓碑》（湘江战役）", "叙事感与停顿", "bilibili.com/video/BV1pe4y1S7gY"],
    ["齐越奖《吹号者》（第21届）", "气势与声音造型", "bilibili.com/video/BV13V411m7xr"],
    ["历届齐越节获奖作品名单", "挑选更多自备稿件", "zhuanlan.zhihu.com/p/386497564"],
    ["国家大剧院《七律·长征》", "专业级技巧对标", "tv.cctv.com 搜索：七律·长征"],
    ["长征组歌·1976 舞台艺术片", "朗诵×合唱融合教科书", "bilibili.com/video/BV1Ex41147be"],
    ["廖昌永《过雪山草地》", "间奏齐诵的出处范本", "bilibili.com/video/BV1Xf4y1i7RR"],
    ["长征朗诵背景视频素材", "LED 大屏背景", "bilibili.com/video/BV15Q4y137ww"],
  ];
  const data = [[hd("作品"), hd("学什么"), hd("在哪看")]];
  rows.forEach(r => data.push([say(r[0]), tip(r[1]), tip(r[2])]));
  s.addTable(data, tbOpt(M, 1.78, [3.5, 3.0, 5.83], [0.36, ...Array(9).fill(0.45)]));
  T(s, "用法：先全组同看《我的墓碑》学停顿，再逐句仿齐越节《丰碑》；排练时投屏跟读。", { x: M, y: 6.55, w: 12.33, h: 0.35, fontSize: 12.5, color: C.muted });
  footer(s);
})();

/* ================= S12 排练计划 ================= */
(() => {
  const s = P.addSlide();
  header(s, "四周冲刺", "排练计划");
  const weeks = [
    ["第 1 周", "定稿 · 模仿", ["定 4 领诵＋2 领唱人选", "逐句仿齐越节《丰碑》", "合唱分声部学谱"]],
    ["第 2 周", "分线合排", ["朗诵线掐表 ≤1′45″", "合唱线连贯成形", "按队形图落位走位"]],
    ["第 3 周", "合成 · 录音", ["朗诵×合唱拼接合乐", "进场录对口型音轨", "全程 5′45″±15″"]],
    ["第 4 周", "带麦彩排", ["带麦全流程彩排×3", "摄像回看逐帧修", "双备份演练（音轨＋麦）"]],
  ];
  weeks.forEach((wk, i) => {
    const x = M + i * 3.13;
    if (i) s.addShape("line", { x: x - 0.12, y: 2.0, w: 0, h: 3.1, line: { color: C.line, width: 0.75 } });
    T(s, wk[0], { x, y: 1.95, w: 2.9, h: 0.34, fontSize: 13, bold: true, color: C.gold });
    T(s, wk[1], { x, y: 2.32, w: 2.9, h: 0.45, fontSize: 17, bold: true, color: C.ink });
    s.addText(wk[2].map((b, j) => ({
      text: b, options: { bullet: { code: "25B8", indent: 10 }, breakLine: j < wk[2].length - 1 }
    })), { x, y: 2.85, w: 2.9, h: 2.2, fontFace: F, fontSize: 12.5, color: C.muted, paraSpaceAfter: 8, margin: 0 });
  });
  T(s, "风险预案", { x: M, y: 5.55, w: 3, h: 0.35, fontSize: 13, bold: true, color: C.gold });
  const chips = ["超时 → 删主歌二（省 40″）", "伴奏事故 → U盘＋手机双备份", "队员缺勤 → 排面替补位预置"];
  chips.forEach((c, i) => {
    const x = M + i * 4.22;
    rrect(s, { x, y: 5.95, w: 3.89, h: 0.6, rectRadius: 0.06, fill: { color: C.tint2 }, line: { color: C.line, width: 1 } });
    T(s, c, { x, y: 5.95, w: 3.89, h: 0.6, fontSize: 13, bold: true, color: C.ink, align: "center", valign: "middle" });
  });
  s.addNotes("每次合排全程掐表并录像；目标5′45″，给上下场留15秒余量。");
  footer(s);
})();

/* ================= S13 结尾 ================= */
(() => {
  const s = P.addSlide();
  s.background = { color: C.dark };
  star(s, 9.0, 1.4, 4.5, 4.5, C.dark2);
  star(s, 1.0, 1.75, 0.34, 0.34, C.gold);
  T(s, "如果胜利不属于这样的队伍，\n还会属于谁呢？", { x: 1.0, y: 2.35, w: 11.3, h: 1.7, fontSize: 34, bold: true, color: C.white });
  T(s, "——《丰碑》", { x: 1.0, y: 4.15, w: 6, h: 0.4, fontSize: 15, color: C.gold });
  T(s, "雪掩忠骨处，歌声即回答。预祝演出成功！", { x: 1.0, y: 4.95, w: 11, h: 0.5, fontSize: 19, bold: true, color: C.goldSoft });
  T(s, "《精忠·丰碑》节目组 · 2026 年 9 月", { x: 1.0, y: 6.45, w: 8, h: 0.4, fontSize: 13, color: C.dim });
  footer(s);
})();

P.writeFile({ fileName: "精忠丰碑-演出设计方案.pptx" }).then(f => console.log("written:", f));
