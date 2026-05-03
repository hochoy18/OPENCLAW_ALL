#!/usr/bin/env node
/**
 * resolve_css_vars.js
 * 将 HTML 中的 CSS 变量（var(--xxx)）替换为实际颜色值
 * 同时修复 background-color: transparent 问题
 * 用法: node resolve_css_vars.js <html文件>
 */

const fs = require('fs');

if (process.argv.length < 3) {
  console.error('用法: node resolve_css_vars.js <html文件>');
  process.exit(1);
}

const htmlFile = process.argv[2];
if (!fs.existsSync(htmlFile)) {
  console.error(`文件不存在: ${htmlFile}`);
  process.exit(1);
}

let html = fs.readFileSync(htmlFile, 'utf8');

// 从 section#MdWechat 的 style 属性中提取 CSS 变量值
const sectionMatch = html.match(/<section id="MdWechat"([^>]*)>/);
if (!sectionMatch) {
  console.error('未找到 <section id="MdWechat">');
  process.exit(1);
}

const styleAttr = sectionMatch[1];
const varMap = {};

// 从 style 属性中提取所有 --xxx: #yyy; 格式的变量
const varMatches = styleAttr.matchAll(/--([\w-]+)\s*:\s*([^;]+);/g);
for (const match of varMatches) {
  varMap[match[1]] = match[2].trim();
}

console.log('发现的 CSS 变量:');
for (const [key, val] of Object.entries(varMap)) {
  console.log(`  --${key}: ${val}`);
}

// 1. 替换 html 中所有 var(--xxx) 为实际值
let resolvedCount = 0;
html = html.replace(/var\(--([\w-]+)\)/g, (match, varName) => {
  if (varMap[varName] !== undefined) {
    resolvedCount++;
    return varMap[varName];
  }
  return match;
});

// 2. 如果 section 的 background-color 是 transparent，替换为 --background-color 的实际值
if (varMap['background-color']) {
  const bgColor = varMap['background-color'];
  // 替换 section 标签中 style 里的 background-color: transparent
  html = html.replace(
    /(<section id="MdWechat"[^>]*style="[^"]*?)background-color:\s*transparent/i,
    `background-color: ${bgColor}`
  );
  console.log(`\n修复 background-color: transparent → ${bgColor}`);
}

// 3. 确保 section 上的 color 使用实际值
if (varMap['text-color']) {
  const textColor = varMap['text-color'];
  html = html.replace(
    /(<section id="MdWechat"[^>]*style="[^"]*?)color:\s*var\(--text-color\)/i,
    `color: ${textColor}`
  );
  console.log(`修复 section color: var(--text-color) → ${textColor}`);
}

console.log(`\n已替换 ${resolvedCount} 处 CSS 变量`);

// 写回文件
fs.writeFileSync(htmlFile, html);
console.log(`已保存: ${htmlFile}`);