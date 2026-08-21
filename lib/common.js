// Apps 公共工具库：HTML 转义与安全存储
// 用法：<script src="./lib/common.js"></script> 后使用 window.AppUtils
(function () {
  'use strict';

  // HTML 转义：所有用户输入拼进 innerHTML 前必须经过此函数
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (m) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m];
    });
  }

  // 转义用于 onclick="fn('...')" 单引号参数场景（先 HTML 转义再转单引号已含于上）
  // 推荐：改用 data-* 属性 + addEventListener，见 bindDelegated

  // 事件委托辅助：容器内点击匹配 selector 的元素时回调（元素需带 data-value）
  function bindDelegated(container, selector, fn) {
    container.addEventListener('click', function (e) {
      const el = e.target.closest(selector);
      if (el && container.contains(el)) fn(el.dataset.value, el, e);
    });
  }

  // 安全 JSON 解析：脏数据返回 fallback 而不是抛错
  function loadJSON(key, fallback) {
    try {
      const v = JSON.parse(localStorage.getItem(key));
      return v == null ? fallback : v;
    } catch (e) { return fallback; }
  }

  // 安全写入：超限时返回 false，调用方可提示用户
  function saveJSON(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); return true; }
    catch (e) { return false; }
  }

  window.AppUtils = { esc: esc, bindDelegated: bindDelegated, loadJSON: loadJSON, saveJSON: saveJSON };
})();
