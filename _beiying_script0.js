
(function(){
  'use strict';

  /* ---------- 导航高亮 ---------- */
  var secs = document.querySelectorAll('main section[id]');
  var navA = document.querySelectorAll('.nav a[href^="#"]');
  function setActive(id){
    navA.forEach(function(a){ a.classList.toggle('on', a.getAttribute('href') === '#' + id); });
  }
  if ('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){ if (e.isIntersecting) setActive(e.target.id); });
    }, {rootMargin:'-30% 0px -60% 0px'});
    secs.forEach(function(s){ io.observe(s); });
  }
  window.addEventListener('scroll', function(){
    var top = document.getElementById('topBtn');
    top.style.opacity = (window.scrollY > 500) ? '1' : '0';
  }, {passive:true});
  document.getElementById('topBtn').addEventListener('click', function(){ window.scrollTo({top:0, behavior:'smooth'}); });

  /* ---------- 背诵模式 ---------- */
  var btnRecite = document.getElementById('btnRecite');
  var btnShowAll = document.getElementById('btnShowAll');
  var reciting = false;
  var ft = document.getElementById('fulltext');
  var lines = ft.querySelectorAll('.pl');
  lines.forEach(function(line){
    line.dataset.orig = line.innerHTML;
    line.dataset.full = line.textContent.trim();
    line.addEventListener('click', function(){
      if (!reciting) return;
      if (line.dataset.shown === '1'){
        renderReciteLine(line);
      } else {
        var full = line.dataset.full;
        var firstIdx = 0;
        while (firstIdx < full.length && /[\s\u3000-\u303f\uff00-\uffef\u0020-\u002f\u003a-\u0040\u005b-\u0060\u007b-\u007e]/.test(full.charAt(firstIdx))) {
          firstIdx++;
        }
        line.innerHTML = '<span class="rh">' + full.substring(0, firstIdx + 1) + '</span>' +
          '<span class="rb">' + full.slice(firstIdx + 1) + '</span>';
        line.dataset.shown = '1';
      }
    });
  });
  function renderReciteLine(line){
    var full = line.dataset.full;
    // 跳过开头标点，找到第一个汉字
    var firstIdx = 0;
    while (firstIdx < full.length && /[\s\u3000-\u303f\uff00-\uffef\u0020-\u002f\u003a-\u0040\u005b-\u0060\u007b-\u007e]/.test(full.charAt(firstIdx))) {
      firstIdx++;
    }
    var hintChar = firstIdx < full.length ? full.charAt(firstIdx) : full.charAt(0);
    var prefix = full.substring(0, firstIdx);
    line.innerHTML = '<span class="rh">' + prefix + hintChar + '</span>' +
      '<span class="rb">' + new Array(full.length - firstIdx).join('＿') + '＿</span>';
    line.dataset.shown = '0';
  }
  btnRecite.addEventListener('click', function(){
    reciting = !reciting;
    btnRecite.textContent = reciting ? '原文' : '背诵';
    btnRecite.classList.toggle('off', !reciting);
    btnShowAll.style.display = reciting ? '' : 'none';
    var ft = document.getElementById('fulltext');
    var vl = document.getElementById('verseList');
    if (reciting){
      ft.style.display = '';
      vl.style.display = 'none';
      lines.forEach(function(l){ l.classList.add('reciteline'); renderReciteLine(l); });
    } else {
      ft.style.display = 'none';
      vl.style.display = '';
      lines.forEach(function(l){ l.classList.remove('reciteline'); l.innerHTML = l.dataset.orig; });
    }
  });
  btnShowAll.addEventListener('click', function(){
    var allShown = lines[0] && lines[0].dataset.shown === '1';
    lines.forEach(function(l){
      if (allShown){ renderReciteLine(l); }
      else { l.innerHTML = '<span class="rh">' + l.dataset.full.charAt(0) + '</span>' +
        '<span class="rb">' + l.dataset.full.slice(1) + '</span>';
        l.dataset.shown = '1'; }
    });
    btnShowAll.textContent = allShown ? '显示全部' : '隐藏全部';
  });

  /* ---------- 正文字体大小 ---------- */
  var fsSel = document.getElementById('fsSel');
  var curFs = localStorage.getItem('beiying_fs') || '100';
  fsSel.value = curFs;
  document.body.setAttribute('data-fs', curFs);
  fsSel.addEventListener('change', function(){
    document.body.setAttribute('data-fs', this.value);
    try { localStorage.setItem('beiying_fs', this.value); } catch(e){}
  });

  /* ---------- 一键展开/收起 ---------- */
  var btnAll = document.getElementById('btnAll');
  var allOpen = false;
  btnAll.addEventListener('click', function(){
    allOpen = !allOpen;
    document.querySelectorAll('.verse .v-more').forEach(function(d){ d.open = allOpen; });
    btnAll.textContent = allOpen ? '收起' : '展开';
  });

  /* ---------- 视频伪全屏 ---------- */
  document.querySelectorAll('.fsbtn').forEach(function(btn){
    btn.addEventListener('click', function(){
      var f = document.getElementById(btn.dataset.target);
      if (!f) return;
      var overlay = document.createElement('div');
      overlay.className = 'video-fs-overlay active';
      var closeBtn = document.createElement('button');
      closeBtn.className = 'video-fs-close';
      closeBtn.textContent = '退出全屏 (Esc)';
      overlay.appendChild(closeBtn);
      var parent = f.parentNode;
      var placeholder = document.createElement('span');
      placeholder.style.display = 'none';
      placeholder.id = f.id + '_ph';
      parent.insertBefore(placeholder, f);
      overlay.appendChild(f);
      document.body.appendChild(overlay);
      document.body.style.overflow = 'hidden';
      function closeFs(){
        parent.insertBefore(f, placeholder);
        parent.removeChild(placeholder);
        if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
        document.body.style.overflow = '';
        document.removeEventListener('keydown', escHandler);
      }
      function escHandler(e){ if(e.key === 'Escape') closeFs(); }
      closeBtn.addEventListener('click', closeFs);
      document.addEventListener('keydown', escHandler);
    });
  });

  /* ---------- 原文注释点击弹窗 ---------- */
  var annoPopup = document.getElementById('annoPopup');
  var annoW = document.getElementById('annoW');
  var annoN = document.getElementById('annoN');
  var activeAnno = null;
  document.addEventListener('click', function(e){
    var word = e.target.closest('.anno-word');
    if(word){
      e.stopPropagation();
      if(activeAnno) activeAnno.classList.remove('active');
      activeAnno = word;
      word.classList.add('active');
      annoW.textContent = word.textContent;
      annoN.textContent = word.dataset.note;
      annoPopup.style.display = 'block';
      var rect = word.getBoundingClientRect();
      var top = rect.bottom + 10;
      var left = rect.left;
      var pw = annoPopup.offsetWidth || 300;
      if(left + pw > window.innerWidth - 12) left = window.innerWidth - pw - 12;
      if(left < 12) left = 12;
      if(top + annoPopup.offsetHeight > window.innerHeight - 12){
        top = rect.top - annoPopup.offsetHeight - 10;
      }
      annoPopup.style.top = top + 'px';
      annoPopup.style.left = left + 'px';
    } else if(!e.target.closest('#annoPopup')){
      annoPopup.style.display = 'none';
      if(activeAnno){ activeAnno.classList.remove('active'); activeAnno = null; }
    }
  });
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape' && annoPopup.style.display === 'block'){
      annoPopup.style.display = 'none';
      if(activeAnno){ activeAnno.classList.remove('active'); activeAnno = null; }
    }
  });
  window.addEventListener('scroll', function(){
    if(annoPopup.style.display === 'block' && activeAnno){
      var rect = activeAnno.getBoundingClientRect();
      var top = rect.bottom + 10;
      var left = rect.left;
      var pw = annoPopup.offsetWidth || 300;
      if(left + pw > window.innerWidth - 12) left = window.innerWidth - pw - 12;
      if(left < 12) left = 12;
      annoPopup.style.top = top + 'px';
      annoPopup.style.left = left + 'px';
    }
  }, {passive:true});

  /* ---------- 听写题库 ---------- */
  /* ---------- 听写模式 ---------- */
  var dictate = document.getElementById('dictate');
  var dictMode = document.getElementById('dictMode');
  var dictProgress = document.getElementById('dictProgress');
  var dictPy = document.getElementById('dictPy');
  var dictLine = document.getElementById('dictLine');
  var dictHint = document.getElementById('dictHint');
  var dictAnsBox = document.getElementById('dictAnsBox');
  var dictWord = document.getElementById('dictWord');
  var dictTip = document.getElementById('dictTip');
  var dictShow = document.getElementById('dictShow');
  var dictNext = document.getElementById('dictNext');
  var dictPrev = document.getElementById('dictPrev');
  var dictExit = document.getElementById('dictExit');
  var dictFsMinus = document.getElementById('dictFsMinus');
  var dictFsPlus = document.getElementById('dictFsPlus');
  var dictScale = parseFloat(localStorage.getItem('dict_ds')) || 1.25;
  dictate.style.setProperty('--ds', dictScale);
  dictFsMinus.addEventListener('click', function(){ dictScale = Math.max(0.8, dictScale - 0.1); dictate.style.setProperty('--ds', dictScale); try{localStorage.setItem('dict_ds', dictScale);}catch(e){} });
  dictFsPlus.addEventListener('click', function(){ dictScale = Math.min(1.8, dictScale + 0.1); dictate.style.setProperty('--ds', dictScale); try{localStorage.setItem('dict_ds', dictScale);}catch(e){} });
  var dictState = null;

  function dictShuffle(a){ var b = a.slice(); for (var i = b.length - 1; i > 0; i--){ var j = Math.floor(Math.random() * (i + 1)); var t = b[i]; b[i] = b[j]; b[j] = t; } return b; }

  document.querySelectorAll('#practice .ptools button').forEach(function(btn){
    btn.addEventListener('click', function(){
      var src = (btn.dataset.mode === 'word') ? DICT_WORDS : DICT_NOTES;
      var list = btn.dataset.rand ? dictShuffle(src).slice(0, 5) : src.slice();
      dictState = { mode: btn.dataset.mode, list: list, i: 0 };
      dictate.hidden = false;
      var p = document.documentElement.requestFullscreen();
      if (p && p.catch) p.catch(function(){});
      dictRender();
    });
  });

  function dictRender(){
    var s = dictState, it = s.list[s.i];
    dictMode.textContent = (s.mode === 'word') ? '字形听写' : '注释听写';
    dictProgress.textContent = '第 ' + (s.i + 1) + ' / ' + s.list.length + ' 题';
    if (s.mode === 'word'){
      dictPy.textContent = it.py;
      dictLine.textContent = it.q;
      dictHint.textContent = '—— 默写空格中的字 ——';
      dictWord.textContent = it.w;
      dictTip.textContent = '易错：' + it.tip;
    } else {
      dictPy.textContent = it.w;
      dictLine.textContent = it.q;
      dictHint.textContent = '—— 默写释义 ——';
      dictWord.textContent = it.a;
      dictTip.textContent = '';
    }
    dictAnsBox.hidden = true;
    dictShow.textContent = '显示答案';
    dictNext.textContent = (s.i === s.list.length - 1) ? '完成' : '下一题';
    dictPrev.disabled = (s.i === 0);
    dictPrev.style.opacity = (s.i === 0) ? '0.4' : '1';
  }

  dictShow.addEventListener('click', function(){
    if (!dictState) return;
    if (dictAnsBox.hidden){ dictAnsBox.hidden = false; dictShow.textContent = '隐藏答案'; }
    else { dictAnsBox.hidden = true; dictShow.textContent = '显示答案'; }
  });
  dictNext.addEventListener('click', function(){
    if (!dictState) return;
    if (dictState.i >= dictState.list.length - 1){ dictClose(); return; }
    dictState.i++; dictRender();
  });
  dictPrev.addEventListener('click', function(){
    if (!dictState) return;
    if (dictState.i <= 0) return;
    dictState.i--; dictRender();
  });
  dictExit.addEventListener('click', dictClose);
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && dictate && !dictate.hidden) dictClose(); });
  function dictClose(){
    dictate.hidden = true; dictState = null;
    var p = document.exitFullscreen();
    if (p && p.catch) p.catch(function(){});
  }

  /* ---------- 打印 ---------- */
  var saved = [];
  window.addEventListener('beforeprint', function(){
    saved = [];
    document.querySelectorAll('.verse details').forEach(function(d){ saved.push([d, d.open]); d.open = true; });
  });
  window.addEventListener('afterprint', function(){
    saved.forEach(function(p){ p[0].open = p[1]; }); saved = [];
  });
  document.getElementById('btnPrint').addEventListener('click', function(){ window.print(); });
})();
