const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const ROOT = 'D:/App/Apps/yanshi';
const EXE = 'C:/Users/vanfis/AppData/Local/ms-playwright/chromium-1208/chrome-win64/chrome.exe';

const files = fs.readdirSync(ROOT).filter(f => f.endsWith('.html') && f !== 'zixinli.html').sort();

(async () => {
  const browser = await chromium.launch({ executablePath: EXE });
  const out = [];
  for (const f of files) {
    const page = await browser.newPage({ viewport: { width: 900, height: 700 } });
    const r = { file: f, errors: [] };
    page.on('pageerror', e => r.errors.push('PAGEERROR: ' + e.message));
    page.on('console', m => { if (m.type() === 'error') r.errors.push('CONSOLE: ' + m.text()); });
    try {
      await page.goto('file:///' + path.join(ROOT, f).replace(/\\/g, '/'), { waitUntil: 'domcontentloaded', timeout: 15000 });
      await page.waitForTimeout(80);
      const dom = await page.evaluate(() => {
        const br = document.getElementById('btnRecite');
        const ft = document.getElementById('fulltext');
        return {
          btnRecite_exists: !!br,
          btnRecite_onclick: br ? br.getAttribute('onclick') : null,
          toggleRecite_global: typeof window.toggleRecite !== 'undefined',
          has_addEventListener: !!document.querySelector('script'),
          fulltext_exists: !!ft,
          fulltext_display: ft ? getComputedStyle(ft).display : null,
          fulltext_p: ft ? ft.querySelectorAll(':scope > p').length : 0,
          fulltext_pl: ft ? ft.querySelectorAll('.pl').length : 0,
        };
      });
      Object.assign(r, dom);
      // classify
      r.issues = [];
      if (r.btnRecite_exists && r.btnRecite_onclick && !r.toggleRecite_global) {
        r.issues.push('dead-inline-onclick');
      }
      if (r.btnRecite_exists && !r.btnRecite_onclick && r.fulltext_exists && r.fulltext_pl === 0 && r.fulltext_p > 0) {
        r.issues.push('fulltext-p-no-pl');
      }
      if (r.btnRecite_exists && !r.btnRecite_onclick && r.fulltext_exists && r.fulltext_pl === 0 && r.fulltext_p === 0) {
        r.issues.push('fulltext-empty');
      }
    } catch(e) {
      r.errors.push('LOADERR: ' + e.message);
    }
    out.push(r);
    await page.close();
  }
  await browser.close();

  // summary
  const bad = out.filter(o => o.issues.length || o.errors.length);
  console.log('files scanned: ' + out.length);
  console.log('files with issues: ' + bad.length);
  console.log('---');
  for (const o of bad) {
    console.log([o.file, o.issues.join(','), 'p=' + o.fulltext_p, 'pl=' + o.fulltext_pl, 'onclick=' + (o.btnRecite_onclick || 'NONE'), 'err=' + o.errors.length].join(' | '));
  }
  fs.writeFileSync(path.join(ROOT, 'tools', '_recite_browser_audit.json'), JSON.stringify(out, null, 2), 'utf-8');
  fs.writeFileSync(path.join(ROOT, 'tools', '_recite_browser_audit_bad.json'), JSON.stringify(bad, null, 2), 'utf-8');
})();
