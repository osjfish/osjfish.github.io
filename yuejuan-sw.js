/* 智能阅卷 · Service Worker
   设计要点：
   1) 只接管本应用静态资源（yuejuan.html / lib/*），其余请求一律放行；
   2) 导航请求只做「网络优先 + 离线回退预缓存」，不在导航流上写缓存——
      在导航响应上做 Response.clone()/缓存写入，一旦 CacheStorage 写入变慢会拖住页面流（表现为刷新后卡在 loading）；
   3) 预缓存清单在 install 阶段写入，因此**每次发布都要把 VER 加一**，否则用户拿到的仍是旧页面。 */
const VER='yj-2026-09-11';
const CACHE='yuejuan-'+VER;
const SHELL=[
  './yuejuan.html',
  './lib/jspdf.umd.min.js',
  './lib/qrcode.js',
  './lib/jsQR.js',
  './lib/pdf.min.js',
  './lib/pdf.worker.min.js',
  './lib/xlsx.full.min.js',
  './lib/jszip.min.js'
];
const inScope=function(u){
  const p=u.pathname;
  return /\/yuejuan\.html$/.test(p)||/\/yuejuan-sw\.js$/.test(p)
    ||/\/lib\/[A-Za-z0-9._-]+\.(js|css)$/.test(p);
};
/* 先完整读入内存，再分别构造「给页面的响应」与「缓存副本」，两者不共享底层流 */
function splitResponse(r){
  return r.arrayBuffer().then(function(buf){
    const headers={};
    r.headers.forEach(function(v,k){headers[k]=v});
    const mk=function(body){return new Response(body,{status:r.status,statusText:r.statusText,headers:headers})};
    return {forPage:mk(buf.slice(0)),forCache:mk(buf)};
  });
}
self.addEventListener('install',function(e){
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(SHELL).catch(function(){})}));
});
self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(ks){
    return Promise.all(ks.filter(function(k){return k!==CACHE}).map(function(k){return caches.delete(k)}));
  }).then(function(){return self.clients.claim()}));
});
self.addEventListener('fetch',function(e){
  const req=e.request;
  if(req.method!=='GET')return;
  let url;
  try{url=new URL(req.url)}catch(err){return}
  if(url.origin!==self.location.origin)return;
  if(!inScope(url))return;
  if(req.mode==='navigate'||/\/yuejuan\.html$/.test(url.pathname)){
    /* 页面：优先用预缓存秒开（导航不依赖网络），后台顺带刷新缓存；未命中再走网络 */
    e.respondWith(caches.match('./yuejuan.html').then(function(hit){
      if(hit){
        e.waitUntil(fetch(req).then(function(r){
          if(r&&r.ok)return caches.open(CACHE).then(function(c){return c.put('./yuejuan.html',r)});
        }).catch(function(){}));
        return hit;
      }
      return fetch(req);
    }));
    return;
  }
  /* 静态资源：缓存优先，未命中再联网（读取后拆分，避免流分叉） */
  e.respondWith(caches.match(req).then(function(hit){
    if(hit)return hit;
    return fetch(req).then(function(r){
      if(!r||!r.ok)return r;
      return splitResponse(r).then(function(pair){
        e.waitUntil(caches.open(CACHE).then(function(c){return c.put(req,pair.forCache)}).catch(function(){}));
        return pair.forPage;
      });
    });
  }));
});