import fs from 'node:fs';
const src = fs.readFileSync('D:/App/Apps/yuejuan.html', 'utf8');

// 收集所有 data-act / data-on 引用（HTML 模板字符串里的双引号）
const usedActs = new Set(), usedOns = new Set();
for (const m of src.matchAll(/data-act="([a-z0-9-]+)"/g)) usedActs.add(m[1]);
for (const m of src.matchAll(/data-on="([a-z0-9-]+)"/g)) usedOns.add(m[1]);

// 收集 ACTS 定义（'key':function / "key":function 两种引号）
const defActs = new Set();
for (const m of src.matchAll(/['"]([a-z0-9-]+)['"]\s*:\s*(?:async\s+)?function/g)) defActs.add(m[1]);

// data-on 的处理器也可能走 addEventListener / 专用 change 分发，列出后人工判断
const missing = [...usedActs].filter(a => !defActs.has(a) && a !== 'nav');
const unused = [...defActs].filter(a => !usedActs.has(a));

console.log('== 引用了但 ACTS 无定义（疑似死按钮） ==');
console.log(missing.length ? missing.join('\n') : '（无）');
console.log('\n== ACTS 有定义但 HTML 未引用（候选死代码） ==');
console.log(unused.length ? unused.join('\n') : '（无）');
console.log('\n== data-on 引用（检查各自处理是否存在） ==');
for (const o of usedOns) {
  const has = defActs.has(o) || src.includes("dataset.on==='" + o + "'") || src.includes('dataset.on==="' + o + '"') || new RegExp("on\\s*===\\s*['\"]" + o + "['\"]").test(src);
  console.log(' ', o, has ? 'OK' : '!! 处理器未找到');
}
