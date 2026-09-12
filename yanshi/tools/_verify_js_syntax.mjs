// -*- coding: utf-8 -*-
// 按真实 JS 语法校验每篇课件的 <script> 块（new Function 仅编译不执行，可捕获浏览器 SyntaxError）。
import fs from 'fs';
import path from 'path';
import os from 'os';

const ROOT = 'D:\\App\\Apps\\yanshi';
const SKIP = new Set(['zixinli.html']);
const SCRIPT = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;

const files = fs.readdirSync(ROOT).filter(f => f.endsWith('.html') && !SKIP.has(f)).sort();
const bad = [];
for (const fn of files) {
  const src = fs.readFileSync(path.join(ROOT, fn), 'utf-8');
  let m, idx = 0;
  SCRIPT.lastIndex = 0;
  while ((m = SCRIPT.exec(src))) {
    const code = m[1];
    idx++;
    if (!code.trim()) continue;
    try {
      // 仅做语法编译，不执行（不触发 DOM 引用）
      new Function(code);
    } catch (e) {
      bad.push(`${fn} (script#${idx}): ${e.message.split('\n')[0]}`);
    }
  }
}
console.log('文件数:', files.length);
if (bad.length === 0) {
  console.log('全部 <script> 语法合法，0 问题');
} else {
  console.log(`【语法错误】 ${bad.length} 篇`);
  for (const b of bad) console.log('   ', b);
}
