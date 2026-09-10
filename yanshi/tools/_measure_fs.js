// 实测课件各层级元素的计算字号，找出跨课件的同级不一致
const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');

const DIR = process.argv[2] || 'D:\\App\\Apps\\yanshi';
const files = process.argv.slice(3);

const TARGETS = [
  ['hero', '.hero-title'],
  ['sec-h2', '.sec-head h2'],
  ['box-h3', '.box > h3'],
  ['box-p', '.box p'],
  ['sec-sub', '.sec-sub'],
  ['pl', '.pl'],
  ['v-line', '.v-line'],
  ['d-body-p', '.d-body p'],
  ['f-line', '.f-line'],
  ['fame-p', '.fame-card p'],
  ['acc-cat-h3', '.acc-cat > h3'],
  ['acc-item', '.acc-item'],
  ['acc-sub', '.acc-sub'],
  ['lead-p', '.lead p'],
  ['practice-p', '#practice p'],
];

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:/Users/vanfis/AppData/Local/ms-playwright/chromium-1208/chrome-win64/chrome.exe',
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const out = [];
  for (const f of files) {
    const file = path.join(DIR, f);
    await page.goto('file:///' + file.replace(/\\/g, '/'), { waitUntil: 'load' });
    const r = await page.evaluate((TARGETS) => {
      const res = {};
      for (const [name, sel] of TARGETS) {
        const el = document.querySelector(sel);
        res[name] = el ? getComputedStyle(el).fontSize : null;
      }
      return res;
    }, TARGETS);
    out.push({ file: f, ...r });
  }
  await browser.close();
  fs.writeFileSync('D:\\App\\Apps\\yanshi\\tools\\_fs_measure_out.json', JSON.stringify(out, null, 1));
  const keys = ['file', ...TARGETS.map(t => t[0])];
  const w = keys.map(k => 24);
  console.log(keys.map((k, i) => String(k).padEnd(w[i])).join('|'));
  for (const r of out) console.log(keys.map((k, i) => String(r[k] ?? '-').padEnd(w[i])).join('|'));
})();
