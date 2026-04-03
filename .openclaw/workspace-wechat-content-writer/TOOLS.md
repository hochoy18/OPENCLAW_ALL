# TOOLS.md - Local Notes
version: 2.0 | last_updated: 2026-04-03

## 共享目录
- 共享根目录：`/opt/wechat/ai/workspace-wechat-shared/`
- 日期分区：`{{date}}/`（每日独立子目录）
- 目录结构：
  - `hot/` — wechat-hot-collector 输出
  - `topics/` — wechat-content-writer 选题清单（仅本Agent可写）
  - `article/` — 各版本文章草稿及终稿Markdown/HTML（本Agent可读写）
  - `images/` — AI生成的配图原始文件（本Agent可读写）
  - `audit/` — wechat-quality-auditor 审核报告
  - `push/` — wechat-draft-publisher 推送日志
- docs/：`/opt/wechat/ai/workspace-wechat-shared/docs/`（tech-html-template-1.md、tech-html-acceptance-standards-1.md），**本Agent仅有只读权限**
- topics/ article/ images/：本Agent可读写
- 注意：不得读写其他 Agent 的个人 workspace（`~/.openclaw/workspace-wechat-XXX/`）

## 模型使用
- 文字创作：**MiniMax-M2**（默认模型）
- 图片生成：`image_generate`（MiniMax image-01）

---

## 新Skill体系（2026-04-03生效）

### Skill 1: zhy-markdown2wechat
路径：`~/.openclaw/workspace-wechat-content-writer/skills/zhy-markdown2wechat/`

**功能**：Markdown → 内联CSS HTML转换器，零部署，Node.js即可运行

**调用方式**：
```bash
node ~/.openclaw/workspace-wechat-content-writer/skills/zhy-markdown2wechat/scripts/convert.js \
  <markdown文件路径> \
  <主题css路径> \
  <输出html路径>
```

**主题选择**（必须指定，默认 default.css）：
- `resources/themes/default.css` — 经典紫色编辑风格
- `resources/themes/blue.css`
- `resources/themes/green.css`
- `resources/themes/apple.css`
- `resources/themes/dark.css`
- `resources/themes/notion.css`
- `resources/themes/vibrant.css`

**图片处理**：原样保留 `<img>` 标签，**必须在调用前嵌入 mmbiz.qpic.cn 永久链接**

---

### Skill 2: wechat-layout-publish
路径：`~/.openclaw/workspace-wechat-content-writer/skills/wechat-layout-publish/`

**功能**：Markdown → 主题化HTML，支持选theme，支持推送到公众号草稿（需凭证）

**调用方式**（需Python runtime）：
```bash
# 列出所有可用主题
python ~/.openclaw/workspace-wechat-content-writer/skills/wechat-layout-publish/scripts/list_themes.py

# 渲染HTML（必须指定 --theme）
python ~/.openclaw/workspace-wechat-content-writer/skills/wechat-layout-publish/scripts/render_wechat_html.py \
  --theme <themeId> \
  --input <markdown路径> \
  --output <输出html路径>
```

**主题catalog**（必须指定，禁止使用未列出的themeId）：
- Formal报告：`w001`玉兰、`w006`白百合、`w010`铃兰、`w011`白茶
- 文艺生活：`w002`牡丹、`w013`梅花、`w014`勿忘我、`w022`月见草、`w023`樱花
- 科技产品：`w003`雏菊、`w007`蓝鸢尾、`w017`黑郁金香、`w021`朱槿
- 强视觉：`w004`向日葵、`w005`罂粟、`w018`金盏花、`w019`山茶

---

### Skill 3: wechat-article-typeset
路径：`~/.openclaw/workspace-wechat-content-writer/skills/wechat-article-typeset/`

**功能**：预设主题排版，生成可复制预览链接（edit.shiker.tech）

**调用方式**：
```bash
# 列出所有预设
node ~/.openclaw/workspace-wechat-content-writer/skills/wechat-article-typeset/wechat-html.js --list-presets

# 生成预设主题HTML + 预览链接
node ~/.openclaw/workspace-wechat-content-writer/skills/wechat-article-typeset/wechat-copy.js <input.md>
```

**常用预设**（必须指定）：
- 暖色系：`暖色色块`、`金秋渐变`、`琥珀色块`
- 冷色/商务：`墨色极简`、`青绿左边线`、`蓝鸢尾`
- 极简黑白：`极简黑白`、`极简色块`
- 特色：`雁栖湖`、`深色护眼`、`樱粉色块`

**预览链接**：同目录生成 `article.preset.html` + `wechat-preview-url.txt`

**注意**：图片必须公网可访问，依赖第三方API（edit.shiker.tech）稳定性

---

## 图片生成工具 (image_generate) 正确调用规范

### 必填参数
- `prompt`: 图像描述（必填），英文提示词效果更好

### 可选参数
- `model`: "image-01" 或 "image-01-live"（**不要加 "minimax/" 前缀**）
- `aspect_ratio`: **强制使用 "16:9"**（长方形，禁止默认正方形）

### 禁止使用的参数
- `size` - 不是有效参数
- 单独的 `width` 或 `height`
- 默认正方形（aspect_ratio 不传时默认1:1，**禁止不传**）

### 正确示例
```json
{
  "prompt": "A futuristic tech illustration...",
  "model": "image-01",
  "aspect_ratio": "16:9"
}
```

---

## CDN上传校验规范（强制）

图片上传微信CDN后必须执行两层校验：

### 上传前校验
- 文件格式：PNG / JPG / JPEG
- 文件大小：单张≤10MB

### 上传后校验
- 返回URL必须以 `mmbiz.qpic.cn` 开头
- URL可访问性：HEAD请求，返回 200/301/302 为通过
- 响应为有效JSON

### 校验失败处理
- 必须重新上传
- 禁止携带无效/空链接继续执行
- 重试3次仍失败，报错并终止当前任务
