// 全库实测各层级元素计算字号，输出每个选择器的取值分布 + 异常文件
const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');

const DIR = 'D:\\App\\Apps\\yanshi';
const files = fs.readdirSync(DIR).filter(f => f.endsWith('.html')).sort();

const TARGETS = [
  ['hero h1', '.hero-title'],
  ['板块 h2', '.sec-head h2'],
  ['板块副标', '.sec-sub'],
  ['卡片 h3', '.box > h3'],
  ['积累 h3', '.acc-cat > h3'],
  ['媒体 h4', '.media h4'],
  ['人物 h4', '.lane h4'],
  ['积累小标', '.acc-sub'],
  ['原文 .pl', '.pl'],
  ['解读原句', '.v-line'],
  ['译文 .v-trans', '.v-trans'],
  ['注释 d-body', '.d-body p'],
  ['名句 f-line', '.f-line'],
  ['名句释 p', '.fame-card p'],
  ['box 正文 p', '.box p'],
  ['积累条目', '.acc-item'],
  ['人物 lane p', '.lane p'],
  ['题解 lead', '.lead, .lead p'],
];

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:/Users/vanfis/AppData/Local/ms-playwright/chromium-1208/chrome-win64/chrome.exe',
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const rows = [];
  for (const f of files) {
    await page.goto('file:///' + path.join(DIR, f).replace(/\\/g, '/'), { waitUntil: 'load' });
    const r = await page.evaluate((TARGETS) => {
      const res = {};
      for (const [name, sel] of TARGETS) {
        const el = document.querySelector(sel);
        res[name] = el ? getComputedStyle(el).fontSize : null;
      }
      return res;
    }, TARGETS);
    rows.push({ file: f, ...r });
  }
  await browser.close();
  fs.writeFileSync(path.join(DIR, 'tools', '_fs_measure_all.json'), JSON.stringify(rows, null, 1));

  console.log('测量文件数', rows.length);
  console.log('层级'.padEnd(16) + '出现文件  取值分布');
  for (const [name] of TARGETS) {
    const vals = {};
    for (const r of rows) if (r[name]) vals[r[name]] = (vals[r[name]] || []).concat(r.file);
    const keys = Object.keys(vals);
    const dist = keys.map(k => `${k}×${vals[k].length}`).join('  ');
    const flag = keys.length > 1 ? '   <<< 不一致' : '';
    console.log(String(name).padEnd(16) + String(keys.reduce((a, k) => a + vals[k].length, 0)).padEnd(10) + dist + flag);
    if (keys.length > 1) {
      keys.sort((a, b) => vals[b].length - vals[a].length);
      const major = keys[0];
      const others = keys.slice(1);
      for (const k of others) {
        console.log('      异常 ' + k + ': ' + vals[k].slice(0, 6).join(', ') + (vals[k].length > 6 ? ' …' : ''));
      }
    }
  }
})();
