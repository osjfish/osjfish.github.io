// 构建脚本: 将 chat.src.html (含 JSX 源码) 编译为 chat.html (纯 JS, 无 Babel/Tailwind/lucide)
import { readFileSync, writeFileSync } from 'fs';
import { transformSync } from '@babel/core';
import presetReact from '@babel/preset-react';
import presetEnv from '@babel/preset-env';

const src = readFileSync(new URL('./chat.src.html', import.meta.url), 'utf8');

const scriptRe = /<script type="text\/babel">([\s\S]*?)<\/script>/;
const m = src.match(scriptRe);
if (!m) { console.error('未找到 babel script 块'); process.exit(1); }

const jsxCode = m[1];
const compiled = transformSync(jsxCode, {
    presets: [
        [presetEnv, { targets: 'defaults' }],
        [presetReact, { runtime: 'classic' }]
    ],
    comments: false,
    compact: false
}).code;

const out = src.replace(scriptRe, () => `<script>\n${compiled}\n    </script>`);
writeFileSync(new URL('./chat.html', import.meta.url), out);
console.log('构建完成 -> chat.html (' + out.length + ' bytes)');
