# VoicePix 代码审查报告

**文件：** `voicepix.html`
**审查日期：** 2026-03-28
**审查范围：** 🔒 安全 / ⚡ 性能 / 🐛 Bug / 📝 代码质量

---

## 严重程度：高

### 1. API Key 存储在 localStorage — 存在 XSS 被盗风险

**位置：** `loadAK()` → `localStorage.getItem("vp_ak")` / `saveKey()` → `localStorage.setItem`

**问题描述：**
`GID` 和 `KEY` 直接明文存储在浏览器的 `localStorage` 中，键名为 `vp_ak`，无任何加密或签名保护。

攻击场景：
- 站点存在任何 XSS 漏洞（DOM 注入、第三方脚本劫持等），攻击者可一行 JS 窃取：`localStorage.getItem('vp_ak')`
- 用户在公共/共享电脑上使用，Key 被永久留存
- 恶意浏览器插件可读取 localStorage

**风险评估：** 若 Key 被盗，攻击者可以冒用用户身份调用 MiniMax API，造成经济损失（语音合成按调用量计费）。

**建议修复：**
- 短期：在 UI 上增加"请勿在公共电脑上使用"的警告提示
- 中期：改用 `sessionStorage` 替代 `localStorage`，会话结束自动清除
- 长期：考虑后端代理模式，前端不直接暴露 API Key

---

### 2. 音频预览（prevVoice）内存泄漏 — blob URL 未释放

**位置：** `prevVoice()` 函数

```javascript
async function prevVoice(voiceId, btn) {
  // ...
  var url = URL.createObjectURL(blob);
  var a = new Audio(url);
  a.addEventListener("ended", function () {
    btn.textContent = "▶";
    URL.revokeObjectURL(url); // ✅ 只在 ended 时释放
  });
  a.addEventListener("error", function () {
    btn.textContent = "▶";
    // ❌ error 时没有 revoke
  });
  a.play();
  // ❌ 如果用户快速连续点击多个声音，url 和 Audio 对象全部泄漏
}
```

**问题描述：**
- 快速连续点击多个声音预览按钮时，每次创建的 blob URL 都不会被 `revokeObjectURL` 释放
- `Audio` 对象本身也未被 `pause()` 就可能被丢弃
- 对于较长的预览音频，用户多次点击后会造成大量 blob URL 残留

**建议修复：**
```javascript
// 在创建新 URL 前 revoke 旧的
if (window._prevAudio) {
  window._prevAudio.pause();
  if (window._prevUrl) URL.revokeObjectURL(window._prevUrl);
}
window._prevUrl = url;
window._prevAudio = a;
```

---

### 3. 克隆结果区域不清除 — 重复克隆时界面残留旧数据

**位置：** `doClone()` 函数

```javascript
} catch(e) {
  document.getElementById("cloneRes").style.display = "block";
  document.getElementById("cres").innerHTML = "<span class=\"err\">❌ " + ...;
}
```

**问题描述：**
- 克隆成功后再次尝试克隆（失败或尚未上传新文件），旧的"✅ 克隆成功"消息仍会显示，不会被清除
- `r.style.display = "block"` 只在 `try` 块中设置，失败时显示错误，但之前成功的内容也还在 HTML 里

**建议修复：** 在 `doClone()` 开头先清除结果区域：
```javascript
document.getElementById("cloneRes").style.display = "none";
document.getElementById("cres").innerHTML = "";
```

---

### 4. 生成语音后旧 Audio 对象未暂停

**位置：** `genSpeech()` 函数

```javascript
if (audioEl) { audioEl.pause(); }
audioEl = new Audio(auUrl);
```

**问题描述：**
- 如果用户在播放语音时再次点击"生成语音"，旧 `audioEl` 会被 `pause()`，逻辑正确
- 但 `auUrl`（上一个 blob URL）在创建新 URL 前未被 `URL.revokeObjectURL()` 释放
- 与问题 #2 类似，属于 blob URL 累积泄漏

**建议修复：** 每次生成前释放旧 URL：
```javascript
if (auUrl) URL.revokeObjectURL(auUrl);
auUrl = URL.createObjectURL(auBlob);
```

---

### 5. 音频拖拽/上传仅校验扩展名，未校验 MIME type 和文件内容

**位置：** `handleF()` 函数

```javascript
if (!f.name.match(/\.(mp3|m4a|wav)$/i)) { toast(...); return; }
// ❌ 没有校验 f.type (MIME)
// ❌ 没有文件大小校验（UI 显示最大 20MB，代码无限制）
```

**问题描述：**
- 文件扩展名可通过重命名绕过
- `accept=".mp3,.m4a,.wav"` 属性仅作 UI 提示，可被绕过
- 无文件大小限制，用户可上传超大文件导致网络超时浪费 API 调用

**建议修复：**
```javascript
var allowedTypes = ["audio/mpeg", "audio/mp4", "audio/wav", "audio/x-m4a"];
var maxSize = 20 * 1024 * 1024; // 20MB
if (!allowedTypes.includes(f.type)) { toast("不支持的文件类型"); return; }
if (f.size > maxSize) { toast("文件超过20MB限制"); return; }
```

---

## 严重程度：中

### 6. 无防抖/节流 — 语音预览按钮可被快速重复触发

**位置：** `prevVoice()` 函数（每个声音预览按钮绑定独立事件）

**问题描述：**
用户快速连续点击同一个或多个声音预览按钮时，会同时发起多个 T2A API 请求，每次都是真实计费调用。在网络较慢时用户还可能认为请求失败而多次点击，造成额外扣费。

**建议修复：** 添加请求中状态锁或 debounce：
```javascript
var _previewing = false;
async function prevVoice(voiceId, btn) {
  if (_previewing) return;
  _previewing = true;
  // ... 请求完成后
  _previewing = false;
}
```

---

### 7. API 429（限流）未专门处理

**位置：** `callT2A()` / `doClone()`

```javascript
if (!res.ok) {
  var err = await res.text();
  throw new Error(err); // 429 也走这里，错误信息不友好
}
```

**问题描述：**
- 429 Too Many Requests 未被识别，无法给用户有意义的提示（如"请求过于频繁，请稍后再试"）
- 没有读取 `Retry-After` 响应头做自动重试

**建议修复：**
```javascript
if (res.status === 429) {
  var retryAfter = res.headers.get("Retry-After") || 5;
  throw new Error(L === "zh" ? `请求过于频繁，请在 ${retryAfter} 秒后重试` : `Rate limited. Retry after ${retryAfter}s`);
}
```

---

### 8. `genSpeech()` 无字数上限拦截

**位置：** `genSpeech()` 开头

```javascript
if (!text) { toast(...); return; }
// ❌ 只校验空文字，未校验长度
// UI 显示 10,000 字上限但无强制限制
```

**问题描述：**
- 用户可输入超过 10,000 字，超出 API 限制会导致请求失败
- 大量文本传输浪费带宽，且可能触发 API 端字数限制报错

**建议修复：**
```javascript
var MAX_TEXT = 10000;
if (text.length > MAX_TEXT) {
  toast(L === "zh" ? `文字不能超过 ${MAX_TEXT} 字` : `Text cannot exceed ${MAX_TEXT} characters`, "err");
  return;
}
```

---

### 9. 克隆成功判断使用宽松比较（Loose Equality）

**位置：** `doClone()` 函数

```javascript
if (j.base_resp && j.base_resp.status_code === 0 || j.voice_id) {
```

**问题描述：**
- 缺少括号，运算符优先级不清晰（`&&` 优先级高于 `||`），逻辑易误读
- `j.voice_id` 为 `""` 时也视为成功（truthy check）
- 应使用 `===` 严格比较 `status_code`

**建议修复：**
```javascript
if ((j.base_resp && j.base_resp.status_code === 0) || (j.voice_id && j.voice_id.length > 0)) {
```

---

### 10. 音频进度条点击无防护 NaN

**位置：** 匿名事件监听器

```javascript
audioEl.addEventListener("timeupdate", function () {
  if (!audioEl.duration) return; // ✅ 有检查
  // ...
});
document.getElementById("pbar").addEventListener("click", function (e) {
  if (!audioEl || !audioEl.duration) return; // ✅ 有检查
  // ...
});
```

**说明：** 这两处实际上有 `duration` 检查，暂时无 NaN 问题。但 `duration` 为 0 时（音频未加载完成）点击进度条也会无效，建议增加更明确的用户体验（如下使用说明）。

---

### 11. 全局变量污染严重

**位置：** 全局作用域

```javascript
var L = "zh", GID = "", KEY = "", selVoice = "Chinese (Mandarin)_Warm_Girl", selFmt = "mp3";
// ...
var auUrl = null, auBlob = null, audioEl = null, playing = false, ufile = null;
```

**问题描述：**
- 所有状态变量暴露在全局作用域，容易被页面其他脚本修改或冲突
- `window.L`、`window.GID` 等均可被任意 JS 访问和覆盖

**建议修复：** 使用 IIFE 或 ES Module 封装：
```javascript
(function () {
  const state = { L: "zh", GID: "", KEY: "", selVoice: "...", ... };
  // 通过闭包暴露必要接口
})();
```

---

### 12. 代码重复 — 错误处理逻辑重复

`callT2A()` 和 `doClone()` 中均有类似的 fetch + 错误处理模式，且 `genSpeech()` 中捕获错误后用 `toast` 显示。不同地方对错误的处理方式不统一。

---

## 建议改进

### 13. 克隆后声音未持久化
克隆成功后将 `voice_id` 存入 `VOICES` 数组并重新 `renderVGrid()`，但刷新页面后丢失。用户需要重新克隆才能使用。建议克隆成功后存入 `localStorage` 持久化。

### 14. 语言切换时 DOM 属性残留
`applyLang()` 用 `textContent` 替换文本，但 `data-zh` / `data-en` 属性本身不会被清除，后续再次调用会重复追加。可在切换语言时重置所有 `[data-zh]` / `[data-en]` 属性，或使用更规范的 i18n 方案。

### 15. `tTimer` 未声明 `var`
```javascript
var tTimer; // ✅ 声明了
```
无问题，但建议统一命名风格。

### 16. 拖拽文件时未校验是否真的拖拽了文件
```javascript
z.addEventListener("drop", function (e) {
  e.preventDefault();
  z.classList.remove("drag");
  handleF(e.dataTransfer.files[0]); // 如果 drop 了非文件内容，files[0] 是 undefined
});
```
`handleF` 有 `!f` 检查会走 toast，但提示信息不够明确。

### 17. 缺少网络断开处理
所有 API 调用在网络完全断开时 `fetch` 会抛出 `TypeError`，当前错误处理会显示原始异常信息，不友好。建议增加判断：
```javascript
catch (e) {
  if (e instanceof TypeError) {
    toast(L === "zh" ? "网络连接失败，请检查网络" : "Network error", "err");
  } else {
    toast(..., "err");
  }
}
```

---

## 总结

VoicePix 作为纯前端语音合成工具，整体结构清晰、UI 体验良好，但存在若干需要重视的问题：

**必须修复（上线前）：**
1. **API Key localStorage 泄漏风险** — XSS 可直接盗取 Key，应增加用户警告、迁移至 sessionStorage，并规划后端代理方案
2. **blob URL 内存泄漏** — 音频预览和生成时旧 blob URL 未 revoke，长时间使用会积累大量内存泄漏
3. **文件类型/大小未校验** — 可上传超大文件或绕过类型限制
4. **克隆结果区不刷新** — 重复克隆时旧结果残留导致误导

**建议修复（上线后尽快）：**
5. 预览按钮增加防抖锁，防止重复点击计费
6. 429 限流增加专门提示
7. 文本字数上限增加强制校验
8. 全局变量用 IIFE 封装，减少污染
9. 克隆声音 ID 持久化到 localStorage

**代码质量亮点：**
- 音频播放状态管理（`playing` 变量）正确
- TTS/克隆功能分离清晰
- i18n 多语言支持完整
- 错误处理 try/catch/finally 结构完整

---

*审查工具：静态代码分析（手动审查）*
*报告生成：code-review-assistant skill*
