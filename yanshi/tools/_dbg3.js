const { chromium } = require('playwright-core');
const path=require('path'); const ROOT='D:/App/Apps/yanshi';
const EXE='C:/Users/vanfis/AppData/Local/ms-playwright/chromium-1208/chrome-win64/chrome.exe';
(async()=>{const b=await chromium.launch({executablePath:EXE});
const p=await b.newPage();
p.on('pageerror',e=>{ console.log('PAGEERROR:',e.message); console.log('STACK:',String(e.stack).split('\n').slice(0,5).join(' | ')); });
await p.goto('file:///'+path.join(ROOT,'taikongyiri-yangliwei.html').replace(/\\/g,'/'),{waitUntil:'domcontentloaded'});
await p.waitForTimeout(300);
const r=await p.evaluate(()=>{
  const need=['dictMode','dictProgress','dictPy','dictLine','dictHint','dictAnsBox','dictWord','dictTip','dictShow','dictNext','dictPrev','dictExit','dictFsMinus','dictFsPlus','dictate','annoPopup','btnPrint','btnRecite','btnShowAll','fsSel','fulltext','verseList','topBtn','mediaF1','mediaF2'];
  const miss=need.filter(id=>!document.getElementById(id));
  return {miss};
});
console.log('缺失 id:',JSON.stringify(r.miss));
await b.close();})();
