const { chromium } = require('playwright-core');
const path=require('path'); const ROOT='D:/App/Apps/yanshi';
const EXE='C:/Users/vanfis/AppData/Local/ms-playwright/chromium-1208/chrome-win64/chrome.exe';
(async()=>{const b=await chromium.launch({executablePath:EXE});
for(const f of ['xinglunan-libai.html','yanmentaishouxing-lihe.html','yujiaao-liqingzhao.html']){
 const p=await b.newPage();
 await p.goto('file:///'+path.join(ROOT,f).replace(/\\/g,'/'),{waitUntil:'domcontentloaded'});
 const r=await p.evaluate(()=>{
   const btn=document.querySelector('#practice .ptools button');
   const res={};
   const el=document.elementFromPoint(btn.getBoundingClientRect().left+5, btn.getBoundingClientRect().top+5);
   res.hitTest = el ? (el.tagName+'.'+(el.className||'')) : null;
   res.btnIsHit = (el===btn)||(btn.contains(el));
   btn.click();
   res.afterJsClick = document.getElementById('dictate').hidden;
   return res;
 });
 console.log(f, JSON.stringify(r));
 await p.close();
}
// taikongyiri 缺 id 排查
const p2=await b.newPage();
await p2.goto('file:///'+path.join(ROOT,'taikongyiri-yangliwei.html').replace(/\\/g,'/'),{waitUntil:'domcontentloaded'});
const miss=await p2.evaluate(()=>{
  const need=['verseList','fulltext','btnAll','btnRecite','btnPrint','btnShowAll','fsSel','annoPopup','dictate','topBtn','mediaF1','mediaF2','dictShow','dictNext','dictPrev','dictExit','dictLine','dictWord','dictPy','dictAnsBox'];
  const out={};
  for(const id of need) if(!document.getElementById(id)) out[id]='缺失';
  out._ptools = document.querySelector('#practice .ptools') ? '有容器' : '无容器';
  out._ptoolsHTML = (document.querySelector('#practice .ptools')||{}).innerHTML ? (document.querySelector('#practice .ptools').innerHTML.trim().slice(0,80)) : '空';
  return out;
});
console.log('taikongyiri 缺失:', JSON.stringify(miss,null,0));
await b.close();})();
