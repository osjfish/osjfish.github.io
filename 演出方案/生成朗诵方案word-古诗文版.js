/* 《精忠·丰碑》朗诵方案（古诗文版）纯文本 Word 生成脚本
 * 结构：诗① → 歌上半首 → 诗②（间奏） → 歌下半首 → 诗③收尾（语录）
 * 运行：NODE_PATH=$(npm root -g) node 生成朗诵方案word-古诗文版.js
 */
const { Document, Packer, Paragraph, TextRun, Footer, PageNumber,
        AlignmentType, HeadingLevel, NumberFormat } = require("docx");
const fs = require("fs");

const INK = "000000", MUTED = "7A7A7A";
const F = { ascii: "Times New Roman", eastAsia: "SimSun" };
const FH = { ascii: "Times New Roman", eastAsia: "SimHei" };

const para = (text, opts = {}) => new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  indent: { firstLine: 480 },
  spacing: { line: 312, after: opts.after == null ? 80 : opts.after },
  children: [new TextRun({ text, size: 24, color: INK, font: F })],
});
const line = (role, text, note) => new Paragraph({
  spacing: { line: 312, after: 60 },
  children: [
    new TextRun({ text: role + "：", size: 24, bold: true, color: INK, font: F }),
    new TextRun({ text: text, size: 24, color: INK, font: F }),
    ...(note ? [new TextRun({ text: "（" + note + "）", size: 21, color: MUTED, font: F })] : []),
  ],
});
const sub = (text) => new Paragraph({
  keepNext: true,
  spacing: { before: 200, after: 80 },
  children: [new TextRun({ text, bold: true, size: 24, color: INK, font: FH })],
});
const h = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  keepNext: true,
  spacing: { before: 280, after: 120, line: 340, lineRule: "atLeast" },
  children: [new TextRun({ text, bold: true, size: 26, color: INK, font: FH })],
});

const children = [];

children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 60, line: 380, lineRule: "atLeast" },
  children: [new TextRun({ text: "《精忠·丰碑》朗诵方案（古诗文版）", size: 32, bold: true, color: INK, font: FH })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 160 },
  children: [new TextRun({ text: "5 分钟版 · 诗书同台 · 念诗—唱半首—念诗—唱半首—诗收尾 · 2 男 2 女领诵 + 全班群诵", size: 21, color: MUTED, font: F })],
}));

/* 一、时间账 */
children.push(h("一、时间账：5 分钟怎么装"));
children.push(para("全程约 4′21″ ≈ 开场风雪声 3″ + 诗①33″ + 歌上半首 90″ + 诗②20″ + 歌下半首 63″ + 诗③收尾 52″（注目礼定格含在内）。歌曲剪去主歌二：上半首＝前奏＋主歌一＋副歌一（约 90″）；下半首＝间奏之后直接副歌二＋尾句（约 63″）。若实测伴奏紧凑且想唱满，可加回主歌二（约 4′56″，贴 5 分钟极限，不建议）。具体以手上伴奏实测为准。"));
children.push(para("最关键的咬合点在诗②：副歌一结束、间奏起，诗②三句骑在间奏上念，收字必须落在下半首第一拍。预录音轨时把间奏剪成诗②的实测长度（约 20″），录完音先对这一处。"));

/* 二、朗诵分工稿 */
children.push(h("二、朗诵分工稿（三段）"));

children.push(sub("诗①（开头，约 33″）——什么是长征？四部经典告诉我们"));
children.push(line("女领①", "什么是长征？", "设问，全场静一拍再往下走"));
children.push(line("男领①", "论语告诉我们：士不可以不弘毅，任重而道远。", "沉缓起步；“道远”二字就是长征最古老的写法"));
children.push(line("女领②", "诗经告诉我们：岂曰无衣？与子同袍。王于兴师，修我甲兵，与子偕行！", "铿锵加快；末句用“与子偕行”——一起出征行军，更贴长征行军意象"));
children.push(line("男领②", "唐诗告诉我们：黄沙百战穿金甲，不破楼兰终不还！", "激越；百战不还，是誓言——出自王昌龄《从军行》"));
children.push(line("女领①", "岳飞告诉我们：三十功名尘与土，八千里路云和月！", "苍劲收束；八千里路直通两万五千里"));
children.push(line("女领①（或四人齐）", "这条路，从诗里出发，一走就是两千年——", "收束句压住排比；收字即战鼓前奏进，唱上半首"));

children.push(sub("诗②（中间，约 20″，骑在间奏上）——红军接过这条路"));
children.push(line("女领①", "一九三五年，红军接过这条路——脚下是雪山草地，身后是万里河山！", "间奏一起就开口"));
children.push(line("全班", "红军不怕远征难，万水千山只等闲！", "中段点火；出处《七律·长征》，不念"));
children.push(line("男领②", "雄关漫道真如铁，而今迈步从头越！", "收字即进下半首；出处《忆秦娥·娄山关》，不念"));

children.push(sub("诗③（收尾，约 52″，尾奏不停接着念）——我们的长征，回到语录"));
children.push(line("女领①", "雪山草地走过去了，而长征，从来没有结束——国家的长征，是复兴；民族的长征，是自强；", "排比递进"));
children.push(line("男领②", "我们这一代人的长征，在书山学海，在每一天不服输的坚持里。", "落到个人，放慢"));
children.push(line("女领②", "八千里路云和月，两万五千里风和雪——今天，轮到我们出发！", "全篇金句：岳飞对红军，焊死“从古到今”"));
children.push(line("男领①", "少年中国说告诉我们：红日初升，其道大光；河出伏流，一泻汪洋！", "第二处古文；点“少年”即“我们”"));
children.push(line("女领①", "什么是长征？——长征，永远在路上。一个不记得来路的民族，是没有出路的民族。", "开头之问在此作答；沉下来"));
children.push(line("女领②", "每一代人有每一代人的长征路——", "扬起"));
children.push(line("全班", "每一代人，都要走好自己的长征路！", "最强音；收字即全体注目礼定格，全篇终"));

/* 三、接口 */
children.push(h("三、朗诵和歌的三个咬合点"));
children.push(para("进上半首：诗①末句“一走就是两千年——”收字，战鼓前奏直接进，主歌一由男领唱开嗓。"));
children.push(para("诗②与间奏：副歌一结束、间奏起，诗②三句骑在间奏上念，收字落在下半首第一拍；预录音轨按诗②实测长度剪间奏。"));
children.push(para("接诗③：尾句“堂堂中国要让四方来贺”唱毕，尾奏不停，女领①紧接着开口，不留空拍。"));

/* 四、要点 */
children.push(h("四、几条要点"));
children.push(para("响点只有三个：全班“红军不怕远征难”、诗③“轮到我们出发”、末句“走好自己的长征路”；古诗文句都往回收——念而不吟，别上戏腔，文言自带顿挫，语速可比白话快半拍。"));
children.push(para("两个静点：开头“什么是长征？”之后静一拍；诗③末句之前的“轮到我们出发”稍停半拍再起——安静是给最强音让路。"));
children.push(para("全班三次上场：诗②“七律”、副歌两遍、末句语录，每分钟都有事做；群诵口型整齐、只动下巴。"));
children.push(para("角色分量：女领①戏最重（设问、岳飞句、收束句、语录引入），选最稳的声音；男领②管唐诗、娄山关，要气势；女领②的“八千里路对两万五千里”是全篇金句，给声线最好的女生；男领①的《论语》《少年中国说》两处古文要念得像说话，不像背书。"));
children.push(para("语录出处：习近平《在纪念红军长征胜利 80 周年大会上的讲话》（2016 年 10 月 21 日，新华社受权发布），报幕词可直接引用。", { after: 0 }));

/* 组装 */
const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: F, size: 24, color: INK },
        paragraph: { spacing: { line: 312 } },
      },
      heading1: {
        run: { font: FH, size: 26, bold: true, color: INK },
        paragraph: { spacing: { before: 280, after: 120, line: 340 } },
      },
    },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 },
        pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL },
      },
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: MUTED })],
        })],
      }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  const out = process.argv[2] || "精忠丰碑-朗诵方案-古诗文版-纯文本.docx";
  fs.writeFileSync(out, buf);
  console.log("written:", out);
});
