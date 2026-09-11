const { chromium } = require('playwright-core');
const path=require('path'); const ROOT='D:/App/Apps/yanshi';
const EXE='C:/Users/vanfis/AppData/Local/ms-playwright/chromium-1208/chrome-win64/chrome.exe';
(async()=>{const b=await chromium.launch({executablePath:EXE});
for(const f of ['taikongyiri-yangliwei.html','ailianshuo-zhoudunyi.html']){
const p=await b.newPage();
p.on('pageerror',e=>console.log(f,'PAGEERROR:',e.message,'||',String(e.stack).split('\n')[1]||''));
await p.goto('file:///'+path.join(ROOT,f).replace(/\\/g,'/'),{waitUntil:'domcontentloaded'});
const r=await p.evaluate(()=>{
  const els=document.querySelectorAll('.anno-word,[class*="anno"]');
  let el=null; for(const e of els){ if(e.offsetParent!==null){el=e;break;} }
  if(!el) el=els[0];
  if(!el) return {no:true};
  let err=null;
  try{ el.click(); }catch(e){ err=String(e.message); }
  const pop=document.getElementById('annoPopup');
  return {cls:el.className, err, popDisplay:getComputedStyle(pop).display, popTxt:(pop.textContent||'').trim().slice(0,40), popHTML:pop.innerHTML.slice(0,80)};
});
console.log(f, JSON.stringify(r));
await p.close();}
await b.close();})();
