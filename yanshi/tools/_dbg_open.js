// 复现 dictate_open / anno_popup 失败，捕获控制台错误
const { chromium } = require('playwright-core');
const path = require('path');
const ROOT = 'D:/App/Apps/yanshi';
const EXE = 'C:/Users/vanfis/AppData/Local/ms-playwright/chromium-1208/chrome-win64/chrome.exe';
const FILES = process.argv.slice(2);

(async () => {
  const browser = await chromium.launch({ executablePath: EXE });
  for (const f of FILES) {
    const page = await browser.newPage();
    const logs = [];
    page.on('console', m => { if (m.type() === 'error') logs.push(m.text().slice(0, 160)); });
    page.on('pageerror', e => logs.push('PAGEERROR: ' + String(e.message).slice(0, 160)));
    await page.goto('file:///' + path.join(ROOT, f).replace(/\\/g, '/'), { waitUntil: 'domcontentloaded' });
    console.log('==== ' + f);
    // 结构检查
    const info = await page.evaluate(() => {
      const pr = document.querySelectorAll('#practice');
      const btns = document.querySelectorAll('#practice .ptools button');
      const dt = document.querySelectorAll('#dictate');
      return {
        practice_count: pr.length,
        btn_count: btns.length,
        dictate_count: dt.length,
        btn_modes: [...btns].map(b => b.dataset.mode + '/' + (b.dataset.rand || 'all')).join(','),
        btn_text: [...btns].map(b => b.textContent.trim()).join(' | '),
        dictate_hidden: dt[0] ? dt[0].hidden : null,
      };
    });
    console.log('  ', JSON.stringify(info));
    // 点第一个按钮
    try {
      await page.click('#practice .ptools button', { timeout: 5000 });
      await page.waitForTimeout(200);
      const after = await page.evaluate(() => {
        const d = document.getElementById('dictate');
        return { hidden: d.hidden, line: (document.getElementById('dictLine') || {}).textContent };
      });
      console.log('   click后:', JSON.stringify(after));
    } catch (e) {
      console.log('   click失败:', String(e.message).slice(0, 100));
    }
    // 注释
    try {
      const n = await page.evaluate(() => {
        const els = document.querySelectorAll('.anno-word, [class*="anno"]');
        return { count: els.length, first_visible: els[0] ? (els[0].offsetParent !== null) : null };
      });
      console.log('   anno:', JSON.stringify(n));
      await page.evaluate(() => {
        const els = document.querySelectorAll('.anno-word, [class*="anno"]');
        for (const e of els) { if (e.offsetParent !== null) { e.click(); return; } }
        if (els[0]) els[0].click();
      });
      await page.waitForTimeout(200);
      const ap = await page.evaluate(() => {
        const p = document.getElementById('annoPopup');
        return { exists: !!p, hidden: p ? p.hidden : null, display: p ? getComputedStyle(p).display : null, txt: p ? (p.textContent || '').trim().slice(0, 30) : null };
      });
      console.log('   popup:', JSON.stringify(ap));
    } catch (e) { console.log('   anno失败:', String(e.message).slice(0, 80)); }
    if (logs.length) console.log('   控制台错误:', logs.slice(0, 3));
    await page.close();
  }
  await browser.close();
})();
