/* 《精忠·丰碑》排练时间轴 Word 文档生成脚本（docx-js）
 * 运行：NODE_PATH=$(npm root -g) node 生成排练时间轴docx.js
 */
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, PageNumber, NumberFormat, AlignmentType, HeadingLevel,
  WidthType, BorderStyle, ShadingType, SectionType, TableLayoutType,
} = require("docx");
const fs = require("fs");

/* ── 调色板（与演出方案PPT同源：深红+金） ── */
const PAL = {
  bg: "2B1214", accent: "C9A227",
  cover: { titleColor: "FFFFFF", subtitleColor: "E2C25C", metaColor: "9A8B8B", footerColor: "8A7A7A" },
  table: { headerBg: "A61B29", headerText: "FFFFFF", accentLine: "A61B29", innerLine: "E0D0D0", surface: "FBF7F7" },
  headingColor: "A61B29", ink: "000000", muted: "808080",
};

const NB = { style: BorderStyle.NONE, size: 0, color: "auto" };
const allNoBorders = { top: NB, bottom: NB, left: NB, right: NB, insideHorizontal: NB, insideVertical: NB };
const noBorders = { top: NB, bottom: NB, left: NB, right: NB };
const emptyPara = () => new Paragraph({ children: [] });

/* ── design-system.md 标题布局函数 ── */
function splitTitleLines(title, charsPerLine) {
  if (title.length <= charsPerLine) return [title];
  const breakAfter = new Set([..."\uFF0C\u3002\u3001\uFF1B\uFF1A\uFF01\uFF1F", ..."\u7684\u4E0E\u548C\u53CA\u4E4B\u5728\u4E8E\u4E3A", ..."-_\u2014\u2013\u00B7/", ..." \t"]);
  const lines = [];
  let remaining = title;
  while (remaining.length > charsPerLine) {
    let breakAt = -1;
    for (let i = charsPerLine; i >= Math.floor(charsPerLine * 0.6); i--) {
      if (i < remaining.length && breakAfter.has(remaining[i - 1])) { breakAt = i; break; }
    }
    if (breakAt === -1) {
      const limit = Math.min(remaining.length, Math.ceil(charsPerLine * 1.3));
      for (let i = charsPerLine + 1; i < limit; i++) {
        if (breakAfter.has(remaining[i - 1])) { breakAt = i; break; }
      }
    }
    if (breakAt === -1) {
      breakAt = charsPerLine;
      const prevChar = remaining[breakAt - 1], nextChar = remaining[breakAt];
      if (prevChar && nextChar && !breakAfter.has(prevChar) && !breakAfter.has(nextChar) &&
          /[\u4e00-\u9fff]/.test(prevChar) && /[\u4e00-\u9fff]/.test(nextChar)) breakAt -= 1;
    }
    lines.push(remaining.slice(0, breakAt).trim());
    remaining = remaining.slice(breakAt).trim();
  }
  if (remaining) lines.push(remaining);
  if (lines.length > 1 && lines[lines.length - 1].length <= 2) {
    const last = lines.pop();
    lines[lines.length - 1] += last;
  }
  return lines;
}
function calcTitleLayout(title, maxWidthTwips, preferredPt = 40, minPt = 24) {
  const charWidth = (pt) => pt * 20;
  const charsPerLine = (pt) => Math.floor(maxWidthTwips / charWidth(pt));
  let titlePt = preferredPt, lines;
  while (titlePt >= minPt) {
    const cpl = charsPerLine(titlePt);
    if (cpl < 2) { titlePt -= 2; continue; }
    lines = splitTitleLines(title, cpl);
    if (lines.length <= 3) break;
    titlePt -= 2;
  }
  if (!lines || lines.length > 3) {
    lines = splitTitleLines(title, charsPerLine(minPt));
    titlePt = minPt;
  }
  return { titlePt, titleLines: lines };
}

/* ── R4 封面（Top Color Block）── */
function buildCoverR4(config) {
  const P = config.palette;
  const padL = 1200, padR = 800;
  const availableWidth = 11906 - padL - padR;
  const { titlePt, titleLines } = calcTitleLayout(config.title, availableWidth, 40, 26);
  const titleSize = titlePt * 2;
  const titleBlockHeight = titleLines.length * (titlePt * 23 + 200);
  const englishLabelH = config.englishLabel ? (9 * 23 + 500) : 0;
  const subtitleH = config.subtitle ? (12 * 23 + 200) : 0;
  const UPPER_MIN = 7500;
  const UPPER_H = Math.max(UPPER_MIN, englishLabelH + titleBlockHeight + subtitleH + 1500 + 800);
  const DIVIDER_H = 60;
  const contentEstimate = englishLabelH + titleBlockHeight + subtitleH;
  const spacerIntrinsic = 280;
  const topSpacing = Math.max(UPPER_H - contentEstimate - spacerIntrinsic - 800, 400);

  const upperBlock = new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    layout: TableLayoutType.FIXED,
    borders: allNoBorders,
    rows: [new TableRow({
      height: { value: UPPER_H, rule: "exact" },
      children: [new TableCell({
        shading: { fill: P.bg }, borders: noBorders,
        verticalAlign: "top",
        margins: { left: padL, right: padR },
        children: [
          new Paragraph({ spacing: { before: topSpacing } }),
          config.englishLabel ? new Paragraph({
            spacing: { after: 500 },
            children: [new TextRun({ text: config.englishLabel.split("").join(" "),
              size: 18, color: P.accent, font: { ascii: "Calibri" }, characterSpacing: 60 })],
          }) : null,
          ...titleLines.map((line, i) => new Paragraph({
            spacing: { after: i < titleLines.length - 1 ? 100 : 200, line: Math.ceil(titlePt * 23), lineRule: "atLeast" },
            children: [new TextRun({ text: line, size: titleSize, bold: true,
              color: P.cover.titleColor, font: { eastAsia: "SimHei", ascii: "Arial" } })],
          })),
          config.subtitle ? new Paragraph({
            spacing: { after: 100 },
            children: [new TextRun({ text: config.subtitle, size: 24, color: P.cover.subtitleColor,
              font: { eastAsia: "Microsoft YaHei", ascii: "Arial" } })],
          }) : null,
        ].filter(Boolean),
      })],
    })],
  });

  const divider = new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: allNoBorders,
    rows: [new TableRow({
      height: { value: DIVIDER_H, rule: "exact" },
      children: [new TableCell({ borders: noBorders,
        shading: { fill: P.accent }, children: [emptyPara()] })],
    })],
  });

  const lowerContent = [
    new Paragraph({ spacing: { before: 800 } }),
    ...(config.metaLines || []).map(line => new Paragraph({
      indent: { left: padL }, spacing: { after: 100 },
      children: [new TextRun({ text: line, size: 28, color: P.cover.metaColor,
        font: { eastAsia: "Microsoft YaHei", ascii: "Arial" } })],
    })),
    new Paragraph({ spacing: { before: 2000 } }),
    new Paragraph({
      indent: { left: padL },
      children: [
        new TextRun({ text: config.footerLeft || "", size: 22, color: P.cover.footerColor }),
        new TextRun({ text: "          " }),
        new TextRun({ text: config.footerRight || "", size: 22, color: P.cover.footerColor }),
      ],
    }),
  ];

  return [new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    layout: TableLayoutType.FIXED,
    borders: allNoBorders,
    rows: [new TableRow({
      height: { value: 16838, rule: "exact" },
      children: [new TableCell({
        shading: { fill: "FFFFFF" }, borders: noBorders,
        verticalAlign: "top",
        children: [upperBlock, divider, ...lowerContent],
      })],
    })],
  })];
}

/* ── 正文组件 ── */
const h1 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  keepNext: true,
  spacing: { before: 360, after: 160, line: 380, lineRule: "atLeast" },
  children: [new TextRun({ text, bold: true, size: 32, color: PAL.headingColor, font: { ascii: "Times New Roman", eastAsia: "SimHei" } })],
});
const h2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  keepNext: true,
  spacing: { before: 240, after: 120, line: 340, lineRule: "atLeast" },
  children: [new TextRun({ text, bold: true, size: 28, color: PAL.headingColor, font: { ascii: "Times New Roman", eastAsia: "SimHei" } })],
});
const body = (text, opts = {}) => new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  indent: { firstLine: 480 },
  spacing: { line: 312, after: opts.after || 80 },
  children: [new TextRun({ text, size: 24, color: PAL.ink, font: { ascii: "Times New Roman", eastAsia: "SimSun" } })],
});
const tableTitle = (text) => new Paragraph({
  keepNext: true,
  spacing: { before: 160, after: 80 },
  children: [new TextRun({ text, bold: true, size: 21, color: PAL.ink, font: { ascii: "Times New Roman", eastAsia: "SimHei" } })],
});
const cellP = (text, opts = {}) => new Paragraph({
  alignment: opts.align || AlignmentType.LEFT,
  keepNext: !!opts.keepNext,
  spacing: { line: 276 },
  children: [new TextRun({
    text, size: opts.size || 21, bold: !!opts.bold,
    color: opts.color || PAL.ink,
    font: { ascii: "Times New Roman", eastAsia: opts.hei ? "SimHei" : "SimSun" },
  })],
});
const cellLines = (lines) => lines.map((t, i) => new Paragraph({
  alignment: AlignmentType.LEFT,
  spacing: { line: 276, after: i < lines.length - 1 ? 40 : 0 },
  children: [new TextRun({ text: t, size: 21, color: PAL.ink, font: { ascii: "Times New Roman", eastAsia: "SimSun" } })],
}));
function mkTable(headers, widths, rows, opts = {}) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: PAL.table.accentLine },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: PAL.table.accentLine },
      left: NB, right: NB,
      insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: PAL.table.innerLine },
      insideVertical: { style: BorderStyle.SINGLE, size: 1, color: PAL.table.innerLine },
    },
    rows: [
      new TableRow({
        tableHeader: true, cantSplit: true,
        children: headers.map((t, i) => new TableCell({
          children: [cellP(t, { bold: true, color: PAL.table.headerText, align: AlignmentType.CENTER, hei: true, keepNext: true })],
          shading: { type: ShadingType.CLEAR, fill: PAL.table.headerBg },
          margins: { top: 70, bottom: 70, left: 110, right: 110 },
          width: { size: widths[i], type: WidthType.PERCENTAGE },
        })),
      }),
      ...rows.map((r, ri) => new TableRow({
        cantSplit: true,
        children: r.map((cell, ci) => new TableCell({
          children: Array.isArray(cell) ? cellLines(cell) : [cellP(cell, { align: opts.centerCols && opts.centerCols.includes(ci) ? AlignmentType.CENTER : AlignmentType.LEFT })],
          shading: (opts.zebra && ri % 2 === 1) ? { type: ShadingType.CLEAR, fill: PAL.table.surface } : undefined,
          margins: { top: 60, bottom: 60, left: 110, right: 110 },
          width: { size: widths[ci], type: WidthType.PERCENTAGE },
        })),
      })),
    ],
  });
}

/* ── 封面配置 ── */
const coverConfig = {
  title: "\u300A\u7CBE\u5FE0\u00B7\u4E30\u7891\u300B\u6392\u7EC3\u65F6\u95F4\u8F74",
  subtitle: "\u60C5\u666F\u6717\u8BF5\u300A\u4E30\u7891\u300B\u00D7 \u5408\u5531\u300A\u7CBE\u5FE0\u62A5\u56FD\u300B \u00B7 \u56DB\u5468\u51B2\u523A\u65B9\u6848",
  englishLabel: "REHEARSAL TIMELINE",
  metaLines: [
    "\u8282\u76EE\u603B\u957F\uFF1A5\u203215\u2033\uFF08\u4E0A\u9650 5\u203230\u2033\uFF09",
    "\u6392\u7EC3\u5468\u671F\uFF1A2026\u5E749\u67087\u65E5 \u2014 10\u67084\u65E5\uFF08\u56DB\u5468 13 \u6B21\uFF09",
    "\u9A8C\u6536\u6807\u51C6\uFF1A\u5168\u7A0B\u6390\u8868 5\u203215\u2033\u00B110\u2033",
    "\u7F16\u5236\uFF1A\u8282\u76EE\u7B79\u5907\u7EC4 \u00B7 2026\u5E749\u6708",
  ],
  footerLeft: "\u300A\u7CBE\u5FE0\u00B7\u4E30\u7891\u300B\u8282\u76EE\u7EC4",
  footerRight: "2026.09",
  palette: PAL,
};

/* ── 正文内容 ── */
const bodyChildren = [];

/* 一、总则 */
bodyChildren.push(h1("\u4E00\u3001\u603B\u5219\u4E0E\u76EE\u6807"));
bodyChildren.push(body("\u672C\u8868\u9002\u7528\u4E8E\u73ED\u7EA7\u5408\u5531\u6BD4\u8D5B\u8282\u76EE\u300A\u7CBE\u5FE0\u00B7\u4E30\u7891\u300B\uFF08\u60C5\u666F\u6717\u8BF5\u300A\u4E30\u7891\u300B\u00D7\u5408\u5531\u300A\u7CBE\u5FE0\u62A5\u56FD\u300B\uFF09\u3002\u8282\u76EE\u603B\u957F 5\u203215\u2033\uFF0C\u5176\u4E2D\u6717\u8BF5 1\u203245\u2033\u3001\u5408\u5531 2\u203253\u2033\u3001\u7ED3\u5C3E\u8BED\u5F55\u70B9\u9898 22\u2033\uFF1B\u5F69\u6392\u9A8C\u6536\u6807\u51C6\u4E3A\u5168\u7A0B\u6390\u8868 5\u203215\u2033\u00B110\u2033\uFF0C\u4E0D\u5F97\u8D85\u8FC7 5\u203230\u2033\u3002"));
bodyChildren.push(body("\u6392\u7EC3\u5468\u671F\u5171\u56DB\u5468 13 \u6B21\uFF0C\u81EA 2026 \u5E74 9 \u6708 7 \u65E5\uFF08\u5468\u4E00\uFF09\u8D77\u7B97\uFF1A\u5468\u4E2D\u4E24\u6B21\uFF08\u5468\u4E00\u3001\u5468\u4E09 17:00\u201318:30\uFF09\uFF0C\u5468\u516D\u4E00\u6B21\uFF089:30\u201311:30\uFF09\u3002\u5982\u6BD4\u8D5B\u65E5\u53E6\u6709\u5B89\u6392\uFF0C\u53EF\u5C06\u6574\u8868\u5E73\u79FB\uFF0C\u5468\u6B21\u76F8\u5BF9\u5173\u7CFB\u4E0D\u53D8\uFF1B\u8D70\u53F0\u56FA\u5B9A\u5B89\u6392\u5728\u8D5B\u524D\u4E00\u65E5\u3002"));
bodyChildren.push(body("\u6BCF\u6B21\u6392\u7EC3\u8BF7\u63D0\u524D 10 \u5206\u949F\u5230\u573A\u7B7E\u5230\uFF1B\u9886\u8BF5\u3001\u9886\u5531\u5982\u9700\u8BF7\u5047\uFF0C\u987B\u63D0\u524D\u4E00\u5929\u62A5\u603B\u5BFC\u6F14\u5E76\u5B89\u6392\u66FF\u8865\u8DDF\u6392\u3002\u6BCF\u6B21\u6392\u7EC3\u7684\u6390\u8868\u6570\u636E\u8BB0\u5F55\u5728\u6848\uFF0C\u4F9B\u5468\u672B\u590D\u76D8\u3002"));
bodyChildren.push(tableTitle("\u8868 1  \u5C97\u4F4D\u5206\u5DE5"));
bodyChildren.push(mkTable(
  ["\u5C97\u4F4D", "\u4EBA\u6570", "\u804C\u8D23", "\u4EBA\u9009"],
  [16, 12, 50, 22],
  [
    ["\u603B\u5BFC\u6F14", "1", "\u603B\u4F53\u7EDF\u7B79\u3001\u8FDB\u5EA6\u4E0E\u7EAA\u5F8B\u3001\u6390\u8868\u590D\u76D8", "\u3010\u59D3\u540D\u3011"],
    ["\u6717\u8BF5\u6307\u5BFC", "1", "\u9886\u8BF5\u5904\u7406\u4E0E\u7FA4\u8BF5\u7EC4\u7EC7\uFF08\u5EFA\u8BAE\u8BED\u6587\u8001\u5E08\u6216\u64AD\u97F3\u7279\u957F\u751F\u62C5\u4EFB\uFF09", "\u3010\u59D3\u540D\u3011"],
    ["\u9886\u8BF5", "4\uFF08\u75372\u59732\uFF09", "\u6717\u8BF5\u6BB5\u4E0E\u70B9\u9898\u6BB5\u9886\u8BF5\uFF1B\u4F7F\u7528\u9EA61\u3001\u9EA62", "\u30104\u4EBA\u540D\u5355\u3011"],
    ["\u9886\u5531", "2", "\u4E3B\u6B4C\u72EC\u5531\u4E0E\u526F\u6B4C\u5E26\u5531\uFF1B\u4F7F\u7528\u9EA63\u3001\u9EA64", "\u30102\u4EBA\u540D\u5355\u3011"],
    ["\u6307\u6325\uFF08\u53EF\u9009\uFF09", "1", "\u5408\u5531\u6307\u6325\uFF0C\u7AD9\u5DE6\u524D\u89D2\u4FA7\u8EAB\u9762\u5BF9\u5408\u5531\u961F", "\u3010\u59D3\u540D\u3011"],
    ["\u97F3\u63A7", "1", "\u9884\u5F55\u97F3\u8F68\u64AD\u653E\u3001LED\u89E6\u53D1\u3001\u53CC\u5907\u4EFD\u5207\u6362", "\u3010\u59D3\u540D\u3011"],
    ["\u670D\u88C5\u9053\u5177", "1", "\u7EA2\u56F4\u5DFE\u3001\u767D\u624B\u5957\u7BA1\u7406\uFF0C\u4E0A\u4E0B\u573A\u5F15\u5BFC", "\u3010\u59D3\u540D\u3011"],
    ["\u6444\u5F71\u8BB0\u5F55", "1", "\u5F69\u6392\u6444\u50CF\u3001\u56DE\u770B\u7D20\u6750\u6574\u7406", "\u3010\u59D3\u540D\u3011"],
  ],
  { zebra: true, centerCols: [1] }
));

/* 二、四周总览 */
bodyChildren.push(h1("\u4E8C\u3001\u56DB\u5468\u603B\u89C8"));
bodyChildren.push(tableTitle("\u8868 2  \u9636\u6BB5\u5212\u5206\u4E0E\u4EA4\u4ED8"));
bodyChildren.push(mkTable(
  ["\u5468\u6B21", "\u65E5\u671F", "\u9636\u6BB5", "\u672C\u5468\u4EA4\u4ED8"],
  [12, 20, 16, 52],
  [
    ["\u7B2C1\u5468", "9\u67087\u65E5\u201312\u65E5", "\u5B9A\u7A3F\u00B7\u6A21\u4EFF", "\u89D2\u8272\u3001\u58F0\u90E8\u3001\u8BDD\u7B52\u5206\u914D\u5B9A\u7A3F\uFF1B\u6717\u8BF5\u7EBF\u9996\u6B21\u901A\u8BFB\uFF1B\u5408\u5531\u5206\u58F0\u90E8\u5B66\u8C31"],
    ["\u7B2C2\u5468", "9\u670814\u65E5\u201319\u65E5", "\u5206\u7EBF\u5408\u6392", "\u6717\u8BF5\u7EBF\u6390\u8868\u22641\u203250\u2033\uFF1B\u5408\u5531\u5168\u66F2\u8FDE\u8D2F\uFF08\u526A\u4E3B\u6B4C\u4E8C\uFF09\uFF1B\u961F\u5F62\u843D\u4F4D\u8D70\u4F4D"],
    ["\u7B2C3\u5468", "9\u670821\u65E5\u201326\u65E5", "\u5408\u6210\u00B7\u5F55\u97F3", "\u6717\u8BF5\u00D7\u5408\u5531\u62FC\u63A5\u22645\u203230\u2033\uFF1B\u9884\u5F55\u97F3\u8F68\u5355\u6761\u4EA4\u4ED8\uFF085\u203215\u2033\uFF09"],
    ["\u7B2C4\u5468", "9\u670828\u65E5\u201310\u67083\u65E5", "\u5E26\u9EA6\u5F69\u6392", "\u5E26\u9EA6\u5168\u6D41\u7A0B\u00D73\u8FBE\u6807\uFF085\u203215\u2033\u00B110\u2033\uFF09\uFF1B\u5E94\u6025\u9884\u6848\u6F14\u7EC3\uFF1B\u7740\u88C5\u5F69\u6392"],
    ["\u673A\u52A8", "\u8D5B\u524D\u4E00\u65E5", "\u8D70\u53F0", "\u4E0A\u4E0B\u573A\u8DEF\u7EBF\u3001\u8BDD\u7B52\u3001LED\u4E0E\u97F3\u8F68\u5B9E\u6D4B\uFF0C\u573A\u5730\u5DEE\u5F02\u786E\u8BA4"],
  ],
  { zebra: true, centerCols: [0, 1, 2] }
));

/* 三、逐次安排 */
bodyChildren.push(h1("\u4E09\u3001\u9010\u6B21\u6392\u7EC3\u5B89\u6392\uFF0813 \u6B21\uFF09"));
bodyChildren.push(body("\u4E0B\u8868\u4E2D\u65F6\u6BB5\u4E3A\u5EFA\u8BAE\u503C\uFF0C\u53EF\u6309\u5B9E\u9645\u8BFE\u8868\u5FAE\u8C03\uFF1B\u201C\u5F53\u65E5\u9A8C\u6536\u201D\u662F\u6BCF\u6B21\u6392\u7EC3\u7ED3\u675F\u524D\u5FC5\u987B\u8FBE\u5230\u7684\u786C\u6307\u6807\uFF0C\u672A\u8FBE\u6807\u9879\u76EE\u987A\u5EF6\u81F3\u4E0B\u6B21\u4F18\u5148\u5B8C\u6210\u3002", { after: 120 }));

bodyChildren.push(h2("\u7B2C 1 \u5468\uFF089/7\u20139/12\uFF09\uFF1A\u5B9A\u7A3F\u00B7\u6A21\u4EFF"));
bodyChildren.push(mkTable(
  ["\u6B21", "\u65E5\u671F\u00B7\u65F6\u6BB5", "\u53C2\u52A0", "\u6392\u7EC3\u5185\u5BB9\uFF08\u5206\u949F\u7EA7\uFF09", "\u5F53\u65E5\u9A8C\u6536"],
  [6, 17, 12, 45, 20],
  [
    ["1", "9/7\u5468\u4E00\n17:00\u201318:30", "\u5168\u4F53", [
      "00\u201310 \u96C6\u5408\uFF1B\u6295\u5C4F\u8BB2\u89E3\u65B9\u6848PPT\uFF08\u7ED3\u6784\u3001\u65F6\u95F4\u8F74\u3001\u961F\u5F62\uFF09",
      "10\u201335 \u5B9A\u89D2\u8272\uFF1A4\u9886\u8BF5\u8BD5\u97F3\uFF08\u5404\u5FF5\u201C\u2026\u2026\u4ED6\u5C31\u662F\u519B\u9700\u5904\u957F\u3002\u201D\uFF09\uFF0C\u5B9A2\u9886\u5531\uFF1B\u516C\u5E034\u652F\u8BDD\u7B52\u5206\u914D",
      "35\u201360 \u5408\u5531\u58F0\u90E8\u5206\u914D\uFF08\u9AD8/\u4F4E\uFF09\uFF0C\u53D1\u5408\u5531\u8C31\u4E0E\u6717\u8BF5\u5206\u5DE5\u7A3F",
      "60\u201385 \u5168\u7EC4\u540C\u770B\u9F50\u8D8A\u8282\u300A\u4E30\u7891\u300B\u89C6\u9891\uFF0C\u8BB2\u89E3\u5904\u7406\u601D\u8DEF",
      "85\u201390 \u5E03\u7F6E\u4EFB\u52A1\uFF1A\u9886\u8BF5\u80CC\u7A3F\u3001\u5168\u5458\u8DDF\u4F34\u594F\u54FC\u5531",
    ], "\u89D2\u8272/\u58F0\u90E8/\u8BDD\u7B52\u540D\u5355\u516C\u793A\uFF1B\u4EBA\u4EBA\u660E\u786E\u81EA\u5DF1\u7684\u8BDD\u7B52\u4E0E\u7AD9\u4F4D"],
    ["2", "9/9\u5468\u4E09\n17:00\u201318:30", "\u5206\u7EC4", [
      "00\u201310 \u5F00\u55D3\u70ED\u58F0\uFF08\u54FC\u9E23\u3001\u97F3\u9636\uFF09",
      "10\u201345 \u6717\u8BF5\u7EC4\uFF1A\u9010\u53E5\u8DDF\u8BFB\u9F50\u8D8A\u8282\u89C6\u9891\uFF0C\u6807\u6362\u6C14/\u91CD\u97F3\uFF1B\u7CBE\u7B80\u7A3F\u901A\u8BFB2\u904D",
      "\u540C\u65F6\u6BB5 \u5408\u5531\u7EC4\uFF1A\u5B66\u4E3B\u6B4C\u4E00+\u526F\u6B4C\u4E00\u65CB\u5F8B\uFF0C\u5206\u58F0\u90E8\u8FC7\u8C31",
      "45\u201380 \u4E24\u7EC4\u4EA4\u6362\u573A\u5730\u7EE7\u7EED",
      "80\u201390 \u9886\u8BF5\u5408\u4F53\u8FC7\u7CBE\u7B80\u7A3F\u4E00\u904D\uFF08\u4E0D\u6390\u8868\uFF09",
    ], "\u9886\u8BF5\u8131\u7A3F50%\u4EE5\u4E0A\uFF1B\u4E3B\u6B4C\u4E00\u97F3\u51C6\u8282\u594F\u8FC7\u5173"],
    ["3", "9/12\u5468\u516D\n9:30\u201311:30", "\u5168\u4F53", [
      "00\u201315 \u5F00\u55D3\uFF1B\u9F50\u8BF5\u201C\u7EA2\u519B\u4E0D\u6015\u8FDC\u5F81\u96BE\u201D\u5B9A\u8C03",
      "15\u201345 \u5B66\u95F4\u594F\u9F50\u8BF5\u300A\u8FC7\u96EA\u5C71\u8349\u5730\u300B\u4E24\u53E5\uFF08\u5361 20\u2033 \u8282\u594F\uFF09",
      "45\u201375 \u5408\u5531\u5168\u66F2\u8DDF\u4F34\u594F\u5531\u4E00\u904D\uFF0C\u6807\u5220\u51CF\u5904\uFF08\u4E3B\u6B4C\u4E8C\u8DF3\u8FC7\uFF09",
      "75\u2013105 \u8F6C\u573A\u4E13\u9879\uFF1A\u201C\u4E07\u6C34\u5343\u5C71\u53EA\u7B49\u95F2\u201D\u538B\u9F13\u70B9\u8D77\u5531\u00D75\u904D",
      "105\u2013120 \u6717\u8BF5\u7EBF\u9996\u6390\u8868\uFF08\u76EE\u6807\u22642\u203200\u2033\uFF0C\u5148\u6C42\u901A\u987A\uFF09",
    ], "\u5168\u8282\u76EE\u80FD\u4ECE\u5934\u4E32\u5230\u5C3E\u4E0D\u65AD\u7247"],
  ],
  { zebra: true, centerCols: [0] }
));

bodyChildren.push(h2("\u7B2C 2 \u5468\uFF089/14\u20139/19\uFF09\uFF1A\u5206\u7EBF\u5408\u6392"));
bodyChildren.push(mkTable(
  ["\u6B21", "\u65E5\u671F\u00B7\u65F6\u6BB5", "\u53C2\u52A0", "\u6392\u7EC3\u5185\u5BB9\uFF08\u5206\u949F\u7EA7\uFF09", "\u5F53\u65E5\u9A8C\u6536"],
  [6, 17, 12, 45, 20],
  [
    ["4", "9/14\u5468\u4E00\n17:00\u201318:30", "\u5168\u4F53", [
      "00\u201310 \u5F00\u55D3",
      "10\u201350 \u6717\u8BF5\u9010\u53E5\u62A0\uFF1A\u201C\u2026\u2026\u4ED6\u5C31\u662F\u519B\u9700\u5904\u957F\u3002\u201D\u540E\u9759\u573A2\u79D2\u7EC3 10 \u904D\uFF1B\u201C\u6676\u83B9\u7684\u4E30\u7891\u201D\u4E00\u5B57\u4E00\u987F",
      "50\u201380 \u526F\u6B4C\u5F3A\u5316\uFF1B\u9886\u5531\u8BDD\u7B52\u8BD5\u5531",
      "80\u201390 \u6717\u8BF5\u7EBF\u6390\u8868#2\uFF08\u22641\u203255\u2033\uFF09",
    ], "\u6717\u8BF5\u22641\u203255\u2033\uFF1B\u4E24\u6B21\u7FA4\u8BF5\u5F3A\u5F31\u5C42\u6B21\u5206\u660E"],
    ["5", "9/16\u5468\u4E09\n17:00\u201318:30", "\u5168\u4F53", [
      "00\u201310 \u5F00\u55D3",
      "10\u201345 \u5408\u5531\u5206\u6BB5\u8FC7\uFF1A\u526F\u6B4C\u4E8C\u4E0E\u5C3E\u53E5\u6E10\u6162\u8BAD\u7EC3\uFF1B\u9886\u5531\u72EC\u5531\u6BB5\u5361\u4F34\u594F",
      "45\u201370 \u95F4\u594F\u9F50\u8BF5\u97F3\u91CF\u6D4B\u8BD5\uFF08\u76D6\u8FC7\u95F4\u594F\u65CB\u5F8B\uFF09",
      "70\u201390 \u6717\u8BF5\u7EBF\u6390\u8868#3\uFF08\u22641\u203250\u2033\uFF09+\u5F55\u50CF\u56DE\u770B",
    ], "\u6717\u8BF5\u22641\u203250\u2033\uFF1B\u95F4\u594F\u9F50\u8BF5 20\u2033 \u5185\u6536\u5B57"],
    ["6", "9/19\u5468\u516D\n9:30\u201311:30", "\u5168\u4F53", [
      "00\u201310 \u5230\u573A\u6574\u961F",
      "10\u201340 \u6309\u961F\u5F62\u56FE\u843D\u4F4D\uFF084\u6392\u5F27\u5F62\uFF09\uFF0C\u8D34\u70B9\u4F4D\u6807\u8BB0",
      "40\u201370 \u8C03\u5EA6\u6F14\u7EC3\u00D73\uFF1A\u9886\u8BF5\u4E0A\u524D\u533A\u2192\u9000\u4E24\u7FFC\u2192\u70B9\u9898\u518D\u4E0A\u524D\uFF1B\u4E0A\u4E0B\u573A\u8DEF\u7EBF",
      "70\u2013105 \u6717\u8BF5+\u5408\u5531+\u70B9\u9898\u6574\u6BB5\u4E32\u6392\uFF08\u4E0D\u5E26\u9EA6\u4E0D\u6390\u8868\uFF09",
      "105\u2013120 \u6C47\u603B\u95EE\u9898\u6E05\u5355",
    ], "\u4EBA\u4EBA\u77E5\u9053\u6BCF\u6BB5\u7AD9\u54EA\u3001\u4F55\u65F6\u52A8"],
  ],
  { zebra: true, centerCols: [0] }
));

bodyChildren.push(h2("\u7B2C 3 \u5468\uFF089/21\u20139/26\uFF09\uFF1A\u5408\u6210\u00B7\u5F55\u97F3"));
bodyChildren.push(mkTable(
  ["\u6B21", "\u65E5\u671F\u00B7\u65F6\u6BB5", "\u53C2\u52A0", "\u6392\u7EC3\u5185\u5BB9\uFF08\u5206\u949F\u7EA7\uFF09", "\u5F53\u65E5\u9A8C\u6536"],
  [6, 17, 12, 45, 20],
  [
    ["7", "9/21\u5468\u4E00\n17:00\u201318:30", "\u5168\u4F53", [
      "00\u201310 \u5F00\u55D3",
      "10\u201355 \u5168\u6D41\u7A0B\u8054\u6392#1\uFF08\u542B\u6697\u573A\u97F3\u6548\uFF09\u6390\u8868\u2014\u2014\u76EE\u6807\u22645\u203245\u2033",
      "55\u201385 \u56DE\u770B\u95EE\u9898\u6E05\u5355\u9010\u6761\u89E3\u51B3",
      "85\u201390 \u5E03\u7F6E\u5F55\u97F3\u65E5\u6CE8\u610F\u4E8B\u9879",
    ], "\u5168\u7A0B\u80FD\u8D70\u5B8C\uFF1B\u8BEF\u5DEE\u70B9\u8BB0\u5F55\u6210\u6E05\u5355"],
    ["8", "9/23\u5468\u4E09\n17:00\u201318:30", "\u5168\u4F53", [
      "00\u201310 \u5F00\u55D3",
      "10\u201330 \u8F6C\u573A\u4E09\u5904\u4E13\u9879\uFF1A\u538B\u9F13\u70B9\u9F50\u8BF5 / \u95F4\u594F\u6536\u5B57 / \u70B9\u9898\u63A5\u5B9A\u683C",
      "30\u201360 \u8054\u6392#2\u6390\u8868\u2014\u2014\u76EE\u6807\u22645\u203230\u2033",
      "60\u201390 \u5B9A\u683C\u9020\u578B\u4E0E\u656C\u793C\u52A8\u4F5C\u7EDF\u4E00\uFF08\u9886\u8BF5\u767D\u624B\u5957\u8BD5\u6234\uFF09",
    ], "\u8054\u6392\u22645\u203230\u2033\uFF1B\u4E09\u5904\u8F6C\u573A\u65E0\u7F1D"],
    ["9", "9/26\u5468\u516D\n9:30\u201311:30", "\u5168\u4F53\n+ \u97F3\u63A7", [
      "00\u201315 \u5230\u6F14\u51FA\u573A\u5730\uFF08\u6216\u6700\u63A5\u8FD1\u7684\u793C\u5802\uFF09\uFF0C\u6446\u4F4D\u3001\u8BD5\u8BDD\u7B52",
      "15\u201330 \u6309\u5F55\u97F3\u811A\u672C\u8D70\u4E00\u904D\uFF08\u4E0D\u51FA\u58F0\uFF0C\u5BF9\u70B9\u4F4D\uFF09",
      "30\u201390 \u6B63\u5F0F\u5F55\u97F32\u20133\u6761\uFF1A\u6717\u8BF5+\u9F50\u8BF5+\u5408\u5531+\u4F34\u594F\u6574\u6761\uFF1B\u5F53\u573A\u56DE\u653E\u62E9\u4F18",
      "\u8BFE\u540E\uFF1A\u6DF7\u97F3\u5355\u8F68 5\u203215\u2033\uFF0CU\u76D8+\u624B\u673A\u53CC\u5907\u4EFD\uFF08\u97F3\u63A7\u8D1F\u8D23\uFF09",
    ], "\u97F3\u8F68\u603B\u957F 5\u203215\u2033\u00B13\u2033\uFF1B\u6E05\u6670\u65E0\u7206\u97F3\uFF1B\u53CC\u5907\u4EFD\u4EA4\u603B\u5BFC\u6F14"],
  ],
  { zebra: true, centerCols: [0] }
));

bodyChildren.push(h2("\u7B2C 4 \u5468\uFF089/28\u201310/3\uFF09\uFF1A\u5E26\u9EA6\u5F69\u6392\uFF08\u542B\u673A\u52A8\u8D70\u53F0\uFF09"));
bodyChildren.push(mkTable(
  ["\u6B21", "\u65E5\u671F\u00B7\u65F6\u6BB5", "\u53C2\u52A0", "\u6392\u7EC3\u5185\u5BB9\uFF08\u5206\u949F\u7EA7\uFF09", "\u5F53\u65E5\u9A8C\u6536"],
  [6, 17, 12, 45, 20],
  [
    ["10", "9/28\u5468\u4E00\n17:00\u201318:30", "\u5168\u4F53", [
      "00\u201310 \u5E03\u7F6E\u8BDD\u7B52\uFF084\u652F\u7ACB\u67B6\u6309\u9EA61\u20134\u5B9A\u4F4D\uFF09",
      "10\u201350 \u5BF9\u53E3\u578B\u4E13\u9879\uFF1A\u9886\u8BF5\u9010\u53E5\u5BF9\u3001\u7FA4\u8BF5\u5C0F\u53E3\u578B",
      "50\u201385 \u5E26\u9EA6\u5168\u6D41\u7A0B#1\uFF08\u653E\u9884\u5F55\u97F3\u8F68\uFF09\u6390\u8868\u2014\u2014 5\u203215\u2033\u00B110\u2033",
      "85\u201390 \u8BB0\u5F55\u95EE\u9898",
    ], "\u53E3\u578B\u4E0E\u97F3\u8F68\u57FA\u672C\u5BF9\u4E0A\uFF1B\u5168\u7A0B 5\u203225\u2033 \u5185"],
    ["11", "9/30\u5468\u4E09\n17:00\u201318:30", "\u5168\u4F53", [
      "00\u201310 \u5F00\u55D3",
      "10\u201320 \u6444\u50CF\u673A\u4F4D\u67B6\u8BBE\uFF08\u624B\u673A\u6A2A\u5C4F\u56FA\u5B9A\u5373\u53EF\uFF09",
      "20\u201360 \u5E26\u9EA6\u5168\u6D41\u7A0B#2 \u6444\u50CF\u2192\u5F53\u573A\u56DE\u770B\u9010\u5E27\u4FEE\uFF08\u53E3\u578B/\u624B\u52BF/\u8868\u60C5/\u6392\u9762\uFF09",
      "60\u201390 \u95EE\u9898\u70B9\u4E13\u9879\u91CD\u7EC3",
    ], "\u5F55\u50CF\u4E2D\u65E0\u51FA\u620F\u70B9\uFF1B\u6392\u9762\u6574\u9F50"],
    ["12", "10/3\u5468\u516D\n9:30\u201311:30", "\u5168\u4F53", [
      "00\u201315 \u7740\u88C5\uFF1A\u6DF1\u8272\u4E0A\u88C5+\u7EA2\u56F4\u5DFE\uFF1B\u9886\u8BF5\u767D\u624B\u5957",
      "15\u201355 \u5E26\u9EA6\u5168\u6D41\u7A0B#3 \u5B8C\u6574\u6390\u8868\u2014\u2014 5\u203215\u2033\u00B110\u2033",
      "55\u201380 \u5E94\u6025\u6F14\u7EC3\uFF1A\u97F3\u8F68\u53CC\u5907\u4EFD\u5207\u6362 / \u8BDD\u7B52\u5931\u7075\u6539\u771F\u58F0 / \u66FF\u8865\u9876\u4F4D",
      "80\u201390 \u5B9A\u5986\u7167\uFF08\u53EF\u4F5C\u73ED\u7EA7\u5BA3\u4F20\uFF09",
    ], "\u4E09\u6B21\u5F69\u6392\u6570\u636E\u8FBE\u6807\uFF1B\u5E94\u6025\u9884\u6848\u4EBA\u4EBA\u77E5\u9053\u81EA\u5DF1\u7684\u5907\u4EFD\u52A8\u4F5C"],
    ["13", "\u8D5B\u524D\u4E00\u65E5\n\u3010____/____\u3011", "\u5168\u4F53", [
      "\u6309\u6BD4\u8D5B\u987A\u5E8F\u8D70\u53F0\u4E00\u6B21\uFF1A\u4E0A\u4E0B\u573A\u8DEF\u7EBF\u3001\u7AD9\u4F4D\u3001\u8BDD\u7B52\u8BD5\u97F3",
      "LED\u89E6\u53D1\u4E0E\u9884\u5F55\u97F3\u8F68\u5B9E\u653E\uFF08\u70B9\u9898\u5927\u5B57\u3001\u98CE\u96EA\u58F0\u3001\u9F13\u70B9\uFF09",
      "\u8BB0\u5F55\u5B9E\u9645\u573A\u5730\u4E0E\u6392\u7EC3\u573A\u5DEE\u5F02\uFF08\u8FDB\u6DF1/\u56DE\u58F0/\u8BDD\u7B52\u9AD8\u5EA6\uFF09",
    ], "\u5168\u4F53\u719F\u6089\u4E0A\u573A\u53E3\u2013\u53F0\u4F4D\u2013\u4E0B\u573A\u53E3\uFF1B\u97F3\u63A7\u786E\u8BA4\u89E6\u53D1\u70B9"],
  ],
  { zebra: true, centerCols: [0] }
));

/* 四、里程碑 */
bodyChildren.push(h1("\u56DB\u3001\u5173\u952E\u91CC\u7A0B\u7891"));
bodyChildren.push(tableTitle("\u8868 3  \u4E94\u4E2A\u5FC5\u987B\u8FBE\u6210\u7684\u8282\u70B9"));
bodyChildren.push(mkTable(
  ["\u91CC\u7A0B\u7891", "\u65E5\u671F", "\u4EA4\u4ED8\u6807\u51C6"],
  [18, 16, 66],
  [
    ["M1 \u5B9A\u7A3F", "9\u67087\u65E5", "\u89D2\u8272/\u58F0\u90E8/\u8BDD\u7B52\u5206\u914D\u8868\u516C\u793A\uFF0C\u4EBA\u624B\u4E00\u4EFD\u5206\u5DE5\u7A3F"],
    ["M2 \u9996\u8054\u6392", "9\u670821\u65E5", "\u5168\u6D41\u7A0B\uFF08\u542B\u97F3\u6548\uFF09\u22645\u203245\u2033\uFF0C\u95EE\u9898\u6E05\u5355\u5F52\u6863"],
    ["M3 \u5F55\u97F3\u4EA4\u4ED8", "9\u670826\u65E5", "\u9884\u5F55\u97F3\u8F68\u5355\u6761 5\u203215\u2033\u00B13\u2033\uFF0CU\u76D8+\u624B\u673A\u53CC\u5907\u4EFD"],
    ["M4 \u5F69\u6392\u8FBE\u6807", "10\u67083\u65E5", "\u8FDE\u7EED\u4E09\u6B21\u5E26\u9EA6\u5168\u6D41\u7A0B 5\u203215\u2033\u00B110\u2033\uFF0C\u5F55\u50CF\u65E0\u51FA\u620F\u70B9"],
    ["M5 \u8D70\u53F0", "\u8D5B\u524D\u4E00\u65E5", "\u573A\u5730\u5DEE\u5F02\u6E05\u5355\u786E\u8BA4\uFF0C\u4E0A\u4E0B\u573A\u8DEF\u7EBF\u5B9A\u578B"],
  ],
  { zebra: true, centerCols: [0, 1] }
));

/* 五、风险与预案 */
bodyChildren.push(h1("\u4E94\u3001\u98CE\u9669\u4E0E\u9884\u6848"));
bodyChildren.push(tableTitle("\u8868 4  \u98CE\u9669\u5BF9\u7167\u8868"));
bodyChildren.push(mkTable(
  ["\u98CE\u9669", "\u9884\u6848"],
  [24, 76],
  [
    ["\u5168\u7A0B\u8D85 5\u203230\u2033", "\u6717\u8BF5\u538B\u81F3 1\u203240\u2033 \u4EE5\u5185\uFF1B\u70B9\u9898\u6BB5\u5220\u5973\u9886\u2461\u7B2C\u4E8C\u53E5\uFF08\u7701\u7EA6 6\u2033\uFF09\uFF1B\u6697\u573A\u97F3\u6548\u538B\u7F29\u5230 3\u2033"],
    ["\u9884\u5F55\u97F3\u8F68\u4E8B\u6545", "U\u76D8+\u624B\u673A\u53CC\u5907\u4EFD\uFF0C\u97F3\u63A7 10 \u79D2\u5185\u5207\u6362\uFF1B\u82E5\u5F7B\u5E95\u65E0\u58F0\uFF0C\u9886\u5531\u8D77\u8C03\u6E05\u5531\u526F\u6B4C\u7A33\u4F4F\u961F\u5F62\uFF0C\u7FA4\u8BF5\u7167\u5E38"],
    ["\u961F\u5458\u7F3A\u52E4", "\u6BCF\u6B21\u7B7E\u5230\uFF1B\u66FF\u8865\u5168\u7A0B\u8DDF\u6392\uFF1B\u6392\u9762\u7F3A\u53E3\u7531\u540C\u6392\u5FAE\u8C03\u8865\u9F50"],
    ["\u8BDD\u7B52\u6545\u969C", "\u9886\u8BF5/\u9886\u5531\u7ACB\u5373\u6539\u771F\u58F0\u5E76\u5411\u524D\u6392\u534A\u6B65\u8865\u4F4D\uFF1B\u7FA4\u8BF5\u4E0E\u5408\u5531\u7531\u9884\u5F55\u97F3\u8F68\u515C\u5E95"],
    ["\u573A\u5730\u65E0 LED", "\u6539\u5E55\u5E03\u6295\u5F71\uFF1B\u6216\u7EAF\u706F\u5149\u6697\u573A\u2013\u8D77\u5149\u65B9\u6848\uFF1B\u70B9\u9898\u5927\u5B57\u6539 KT \u677F\u624B\u4E3E"],
  ],
  { zebra: true }
));

/* 附：常规流程 */
bodyChildren.push(h1("\u9644\uFF1A\u5355\u6B21\u6392\u7EC3\u5E38\u89C4\u6D41\u7A0B\uFF0890 \u5206\u949F\u6A21\u677F\uFF09"));
bodyChildren.push(tableTitle("\u8868 5  \u5468\u4E2D\u6392\u7EC3\u56FA\u5B9A\u6D41\u7A0B"));
bodyChildren.push(mkTable(
  ["\u65F6\u6BB5", "\u5185\u5BB9", "\u4E3B\u6301"],
  [16, 66, 18],
  [
    ["0\u201310 \u5206\u949F", "\u5F00\u55D3\u70ED\u58F0\uFF1A\u54FC\u9E23\u3001\u97F3\u9636\uFF1B\u9F50\u8BF5\u5B9A\u8C03", "\u9886\u5531"],
    ["10\u201345 \u5206\u949F", "\u5206\u7EBF\u8BAD\u7EC3\uFF1A\u6717\u8BF5\u7EC4\u62A0\u53E5 / \u5408\u5531\u7EC4\u5206\u58F0\u90E8\uFF08\u5206\u533A\u540C\u6B65\uFF09", "\u6717\u8BF5\u6307\u5BFC\u00B7\u6307\u6325"],
    ["45\u201375 \u5206\u949F", "\u5408\u6210\u6BB5\u843D\uFF1A\u8F6C\u573A\u4E09\u5904\u3001\u95F4\u594F\u9F50\u8BF5\u3001\u70B9\u9898\u6BB5", "\u603B\u5BFC\u6F14"],
    ["75\u201390 \u5206\u949F", "\u6390\u8868\u8054\u6392+\u5F55\u50CF\u590D\u76D8\uFF0C\u8BB0\u5F55\u95EE\u9898\u6E05\u5355", "\u603B\u5BFC\u6F14"],
  ],
  { zebra: true, centerCols: [0, 2] }
));
bodyChildren.push(body("\u5468\u516D 120 \u5206\u949F\u7248\u672C\uFF1A\u4E2D\u6BB5\u4E24\u6BB5\u5404\u52A0 15 \u5206\u949F\uFF0C\u590D\u76D8\u52A0\u81F3 25 \u5206\u949F\u3002\u672C\u8868\u6267\u884C\u4E2D\u5982\u6709\u8C03\u6574\uFF0C\u4EE5\u603B\u5BFC\u6F14\u901A\u77E5\u4E3A\u51C6\u3002", { after: 0 }));

/* ── 组装文档 ── */
const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: { ascii: "Times New Roman", eastAsia: "SimSun" }, size: 24, color: "000000" },
        paragraph: { spacing: { line: 312 } },
      },
      heading1: {
        run: { font: { ascii: "Times New Roman", eastAsia: "SimHei" }, size: 32, bold: true, color: PAL.headingColor },
        paragraph: { spacing: { before: 360, after: 160, line: 380 } },
      },
      heading2: {
        run: { font: { ascii: "Times New Roman", eastAsia: "SimHei" }, size: 28, bold: true, color: PAL.headingColor },
        paragraph: { spacing: { before: 240, after: 120, line: 340 } },
      },
    },
  },
  sections: [
    {
      properties: {
        page: { size: { width: 11906, height: 16838 }, margin: { top: 0, bottom: 0, left: 0, right: 0 } },
      },
      children: buildCoverR4(coverConfig),
    },
    {
      properties: {
        type: SectionType.NEXT_PAGE,
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 },
          pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL },
        },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: "\u300A\u7CBE\u5FE0\u00B7\u4E30\u7891\u300B\u6392\u7EC3\u65F6\u95F4\u8F74", size: 18, color: "909090", font: { ascii: "Times New Roman", eastAsia: "SimSun" } })],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "909090" })],
          })],
        }),
      },
      children: bodyChildren,
    },
  ],
});

Packer.toBuffer(doc).then(buf => {
  const out = process.argv[2] || "\u7CBE\u5FE0\u4E30\u7891-\u6392\u7EC3\u65F6\u95F4\u8F74.docx";
  fs.writeFileSync(out, buf);
  console.log("written:", out);
});
