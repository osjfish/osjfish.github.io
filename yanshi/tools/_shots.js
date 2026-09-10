// 对指定课件截图（整页 + 解读区局部），用于人工核对版式
const { chromium } = require('playwright-core');
const path = require('path');

const DIR = 'D:\\App\\Apps\\yanshi';
const files = process.argv.slice(2);

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:/Users/vanfis/AppData/Local/ms-playwright/chromium-1208/chrome-win64/chrome.exe',
  });
  const page = await browser.newPage({ viewport: { width: 1180, height: 1000 }, deviceScaleFactor: 1 });
  for (const f of files) {
    const url = 'file:///' + path.join(DIR, f).replace(/\\/g, '/');
    await page.goto(url, { waitUntil: 'load' });
    await page.waitForTimeout(1200);
    const name = f.replace('.html', '');
    await page.screenshot({ path: path.join(DIR, 'tools', '_shot_' + name + '_top.png'), clip: { x: 0, y: 0, width: 1180, height: 1000 } });
    const el = await page.$('#jielu');
    if (el) {
      await el.scrollIntoViewIfNeeded();
      await page.waitForTimeout(300);
      await page.screenshot({ path: path.join(DIR, 'tools', '_shot_' + name + '_jielu.png'), clip: { x: 0, y: 0, width: 1180, height: 1000 } });
    }
    console.log('shot', f);
  }
  await browser.close();
})();
