const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:/Users/vanfis/AppData/Local/ms-playwright/chromium-1208/chrome-win64/chrome.exe',
    headless: true
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
  page.on('console', msg => { if (msg.type() === 'error') errors.push('CONSOLE: ' + msg.text()); });

  const file = 'file://' + path.resolve('D:/App/Apps/yanshi/taikongyiri-yangliwei.html').replace(/\\/g, '/');
  await page.goto(file, { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);

  // Check DOM order: first section inside main should be #bg
  const firstSection = await page.evaluate(() => {
    const main = document.querySelector('main.wrap');
    const sec = main.querySelector('section[id]');
    return sec ? sec.id : null;
  });

  // btnShowAll should be hidden initially
  const btnShowAllDisplay = await page.evaluate(() => {
    const b = document.getElementById('btnShowAll');
    return b ? getComputedStyle(b).display : 'missing';
  });

  // Click recite and check toggle
  await page.click('#btnRecite');
  await page.waitForTimeout(200);
  const reciteState = await page.evaluate(() => {
    const ft = document.getElementById('fulltext');
    const vl = document.getElementById('verseList');
    const b = document.getElementById('btnRecite');
    const sa = document.getElementById('btnShowAll');
    return {
      btnText: b ? b.textContent : null,
      ftDisplay: ft ? getComputedStyle(ft).display : null,
      vlDisplay: vl ? getComputedStyle(vl).display : null,
      showAllDisplay: sa ? getComputedStyle(sa).display : null
    };
  });

  console.log(JSON.stringify({
    firstSection,
    btnShowAllDisplay,
    reciteState,
    errors
  }, null, 2));

  await browser.close();
})();
