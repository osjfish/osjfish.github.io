// 隐藏板块加密维护工具（零依赖，Node 18+）
// 用法：
//   node tools/encrypt_hidden.mjs                用 tools/.secret 里的解锁词加密
//   node tools/encrypt_hidden.mjs <word>         临时指定解锁词
//   node tools/encrypt_hidden.mjs --decrypt      打印当前 _list.json 里加密的隐藏内容（核对用）
//
// 日常增删隐藏应用：
//   1. 编辑 _hidden.local.json（此文件已被 .gitignore 排除，不会上线）
//   2. 运行上面的加密命令，自动把密文写回 _list.json
//   3. git add -A && git commit && git push 部署
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { pbkdf2Sync, createCipheriv, createDecipheriv, randomBytes } from 'crypto';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const LIST = path.join(ROOT, '_list.json');
const HIDDEN_SRC = path.join(ROOT, '_hidden.local.json');
const SECRET = path.join(path.dirname(fileURLToPath(import.meta.url)), '.secret');
const ITER = 100000;

function getWord(args) {
  if (args.length) return args[0];
  if (existsSync(SECRET)) return readFileSync(SECRET, 'utf8').trim();
  throw new Error('未提供解锁词：请用参数传入，或先写入 tools/.secret');
}

function encrypt(list, word) {
  const salt = randomBytes(16), iv = randomBytes(12);
  const key = pbkdf2Sync(word, salt, ITER, 32, 'sha256');
  const c = createCipheriv('aes-256-gcm', key, iv);
  const ct = Buffer.concat([c.update(Buffer.from(JSON.stringify(list), 'utf8')), c.final()]);
  const tag = c.getAuthTag();
  return { iter: ITER, salt: salt.toString('base64'), iv: iv.toString('base64'), data: Buffer.concat([ct, tag]).toString('base64') };
}

function decrypt(payload, word) {
  const salt = Buffer.from(payload.salt, 'base64'), iv = Buffer.from(payload.iv, 'base64');
  const buf = Buffer.from(payload.data, 'base64');
  const key = pbkdf2Sync(word, salt, payload.iter, 32, 'sha256');
  const d = createDecipheriv('aes-256-gcm', key, iv);
  d.setAuthTag(buf.subarray(buf.length - 16));
  return JSON.parse(Buffer.concat([d.update(buf.subarray(0, buf.length - 16)), d.final()]).toString('utf8'));
}

const [mode, ...rest] = process.argv.slice(2);

if (mode === '--decrypt') {
  const list = JSON.parse(readFileSync(LIST, 'utf8'));
  if (!list.hidden) { console.log('_list.json 中无 hidden 字段'); process.exit(0); }
  console.log(JSON.stringify(decrypt(list.hidden, getWord(rest)), null, 2));
  process.exit(0);
}

const hiddenSrc = JSON.parse(readFileSync(HIDDEN_SRC, 'utf8'));
if (!Array.isArray(hiddenSrc) || !hiddenSrc.every(a => a.name && a.path && a.category)) {
  throw new Error('_hidden.local.json 格式错误：应为 [{name,path,category}, ...]');
}
const word = getWord([mode, ...rest].filter(Boolean));
const list = JSON.parse(readFileSync(LIST, 'utf8'));
list.hidden = encrypt(hiddenSrc, word);
writeFileSync(LIST, JSON.stringify(list));
console.log(`已加密 ${hiddenSrc.length} 个隐藏应用并写回 _list.json（分类：${[...new Set(hiddenSrc.map(a => a.category))].join('、')}）`);
