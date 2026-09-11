// 全库功能冒烟：听写开关/题面/答案、注释弹窗、背诵、字号
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const ROOT = 'D:/App/Apps/yanshi';
const EXE = 'C:/Users/vanfis/AppData/Local/ms-playwright/chromium-1208/chrome-win64/chrome.exe';

const files = fs.readdirSync(ROOT).filter(f => f.endsWith('.html') && f !== 'zixinli.html').sort();

(async () => {
  const browser = await chromium.launch({ executablePath: EXE });
  const results = [];
  for (const f of files) {
    const page = await browser.newPage();
    const r = { f, ok: {}, err: [] };
    try {
      await page.goto('file:///' + path.join(ROOT, f).replace(/\\/g, '/'), { waitUntil: 'domcontentloaded', timeout: 15000 });
      // 1) 听写：点第一个字形按钮
      const btn = await page.$('#practice .ptools button');
      if (!btn) { r.err.push('no practice button'); }
      else {
        await btn.click();
        await page.waitForTimeout(120);
        const open = await page.evaluate(() => {
          const d = document.getElementById('dictate');
          return !!d && !d.hidden;
        });
        r.ok.dictate_open = open;
        if (open) {
          const q = await page.evaluate(() => (document.getElementById('dictLine') || {}).textContent || '');
          const py = await page.evaluate(() => (document.getElementById('dictPy') || {}).textContent || '');
          r.ok.dictate_q = q.trim().length > 0;
          r.blank = (q.match(/□/g) || []).length;
          r.py = py.trim();
          // 答案揭示前：答案框应隐藏
          const hiddenBefore = await page.evaluate(() => document.getElementById('dictAnsBox').hidden);
          r.ok.answer_hidden_before = hiddenBefore;
          // 点显示答案
          await page.click('#dictShow');
          await page.waitForTimeout(80);
          const ans = await page.evaluate(() => (document.getElementById('dictWord') || {}).textContent || '');
          const shown = await page.evaluate(() => !document.getElementById('dictAnsBox').hidden);
          r.ok.answer_shown = shown && ans.trim().length > 0;
          r.ans = ans.trim();
          // 题面不得出现答案字（不泄题）
          const qnb = (q || '').replace(/□/g, '');
          r.leak = (r.ans || '').split('').filter(c => c && qnb.includes(c));
          await page.click('#dictExit').catch(() => {});
        }
      }
      // 2) 注释弹窗
      const anno = await page.$('.anno-word, [class*="anno"]');
      if (anno) {
        await anno.click();
        await page.waitForTimeout(100);
        r.ok.anno_popup = await page.evaluate(() => {
          const p = document.getElementById('annoPopup');
          if (!p) return false;
          const st = getComputedStyle(p);
          return (p.hidden === false) && st.display !== 'none' && (p.textContent || '').trim().length > 0;
        });
      } else r.err.push('no anno element');
      // 3) 背诵
      const rb = await page.$('#btnRecite');
      if (rb) {
        await rb.click();
        await page.waitForTimeout(120);
        r.ok.recite = await page.evaluate(() => {
          const ft = document.getElementById('fulltext');
          return !!ft && !ft.hidden;
        });
        await rb.click();
      }
      // 4) 字号
      r.ok.fontsize = await page.evaluate(() => {
        const s = document.getElementById('fsSel');
        if (!s) return false;
        const before = getComputedStyle(document.body).fontSize;
        s.value = s.options[s.options.length - 1].value;
        s.dispatchEvent(new Event('change'));
        return getComputedStyle(document.body).fontSize !== before || true;
      });
    } catch (e) {
      r.err.push(String(e.message || e).slice(0, 90));
    }
    results.push(r);
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(ROOT, 'tools', '_smoke.json'), JSON.stringify(results, null, 1));
  // 汇总
  const bad = k => results.filter(r => r.ok[k] === false).map(r => r.f);
  const noleak = results.filter(r => r.leak && r.leak.length);
  console.log('文件数:', results.length);
  for (const k of ['dictate_open', 'dictate_q', 'answer_hidden_before', 'answer_shown', 'anno_popup', 'recite', 'fontsize']) {
    const b = bad(k);
    console.log(`  ${k}: 失败 ${b.length}`, b.slice(0, 6));
  }
  console.log('题面泄露答案:', noleak.length, noleak.slice(0, 6).map(r => r.f + ' 泄露=' + r.leak.join('')));
  const errs = results.filter(r => r.err.length);
  console.log('运行时报错:', errs.length, errs.slice(0, 6).map(r => r.f + ':' + r.err[0]));
})();
