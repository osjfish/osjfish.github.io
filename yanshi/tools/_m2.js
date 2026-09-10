const { chromium } = require('playwright-core');
const path = require('path');
(async () => {
  const b = await chromium.launch({ headless: true, executablePath: 'C:/Users/vanfis/AppData/Local/ms-playwright/chromium-1208/chrome-win64/chrome.exe' });
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  for (const f of ['jinianbaiqiuen-maozedong.html', 'qieduji-linhaiyin.html', 'taikongyiri-yangliwei.html', 'ailianshuo-zhoudunyi.html', 'pipaxing-baijuyi.html']) {
    await p.goto('file:///' + path.join('D:\\App\\Apps\\yanshi', f).replace(/\\/g, '/'), { waitUntil: 'load' });
    const r = await p.evaluate(() => {
      const g = s => { const e = document.querySelector(s); return e ? getComputedStyle(e).fontSize : null; };
      const all = [...document.querySelectorAll('.box > p')].map(e => getComputedStyle(e).fontSize);
      return { 'box>p直系': [...new Set(all)].join(','), 'd-body p': g('.d-body p'), 'vs-body p': g('.vs-body p'), 'verse-text': g('.verse-text'), 'video-label': g('.video-label'), 'part-desc': g('.part-desc'), 'acc-word': g('.acc-word') };
    });
    console.log(f, JSON.stringify(r));
  }
  await b.close();
})();
