# TOOLS.md - Local Notes
version: 4.0 | last_updated: 2026-04-09

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
- docs/：`/opt/wechat/ai/workspace-wechat-shared/docs/`（tech-html-acceptance-standards-1.md），**本Agent仅有只读权限**
- topics/ article/ images/：本Agent可读写
- 注意：不得读写其他 Agent 的个人 workspace（`~/.openclaw/workspace-wechat-XXX/`）

## 模型使用
- 文字创作：**MiniMax-M2**（默认模型）
- 图片生成：**curl直接调用新API**（不用OpenClaw内置image_generate工具）

---

## 图片生成（v4.0：必须用新API）

### 为什么废弃 OpenClaw 内置工具
OpenClaw内置 `image_generate` 工具调用的是旧API endpoint，不遵守 `aspect_ratio` 参数，
实际生成1024x1024正方形而非16:9。

### 新API（正确的）
**Endpoint**：`POST https://api.minimax.io/v1/image_generation`

**curl命令示例**：
```bash
curl -s --request POST \
  --url https://api.minimax.io/v1/image_generation \
  --header "Authorization: Bearer $MINIMAX_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "model": "image-01",
  "prompt": "<英文prompt>",
  "aspect_ratio": "16:9",
  "response_format": "url",
  "n": 1
}'
```

**返回JSON**：
```json
{
  "id": "...",
  "data": {"image_urls": ["http://hailuo-image-algeng-data-us.oss-..."]},
  "base_resp": {"status_code": 0, "status_msg": "success"}
}
```

### 完整处理流程
1. 执行curl调用新API → 获取外部图片URL
2. curl下载图片：`curl -s "<URL>" -o /tmp/<output>.jpg`
3. 校验尺寸：`file /tmp/<output>.jpg`（确认1280x720即16:9）
4. 复制到images目录
5. upload_material.py上传微信CDN → 获取mmbiz.qpic.cn链接
6. mmbiz链接嵌入Markdown

### 图片备用源（aliyun）
如果MiniMax image-01失败3次，可尝试阿里云通义万相：
- 工具：`~/.openclaw/workspace-wechat-content-writer/skills/aliyun-image-gen/aliyun-image-gen.js`
- 模型：qwen-image-2.0
- 尺寸：支持 1280*720（16:9横屏）

### 环境变量
- `MINIMAX_API_KEY`：已配置在env中，直接使用即可

---

## 排版Skill体系（v4.0）

### 主力：wechat-article-typeset（生成预览链接）

**工具**：`~/.openclaw/workspace-wechat-content-writer/skills/wechat-article-typeset/wechat-copy.js`

**调用方式**：
```bash
node ~/.openclaw/workspace-wechat-content-writer/skills/wechat-article-typeset/wechat-copy.js \
  --preset "<预设名>" \
  <markdown文件路径>
```

**输出**：
- `article.preset.html` — 预设主题渲染HTML
- `wechat-preview-url.txt` — 预览链接

**预览链接**：`https://edit.shiker.tech/copy.html?id=xxx`
- 用户打开 → 点击「复制到剪贴板」→ 直接粘贴公众号后台
- **预览链接以 wechat-preview-url.txt 中的内容为准，勿AI转述**

**可用预设（--preset）**：
```
智慧蓝左边线  → smartblue + leftline（热度第1名默认）
深色护眼      → dark-calm + card（热度第2名默认）
青绿左边线    → teal-fresh + leftline（工具教程类）
墨色下划线    → ink-seri + underline（观点评论类）
橙心          → yanqi-coral（热点轻娱乐类）
暖色色块      → coral-warm + block
琥珀色块      → amber-paper + block
紫调渐变      → purple-elegant + gradient
极简黑白      → minimal-bw + minimal
```

查看全部预设：
```bash
node ~/.openclaw/workspace-wechat-content-writer/skills/wechat-article-typeset/wechat-html.js --list-presets
```

### 降级：wechat-article-typeset（仅生成HTML）

**工具**：`~/.openclaw/workspace-wechat-content-writer/skills/wechat-article-typeset/wechat-html.js`

```bash
node ~/.openclaw/workspace-wechat-content-writer/skills/wechat-article-typeset/wechat-html.js \
  --preset "<预设名>" \
  <markdown文件路径> > <输出html路径>
```

### 兜底：zhy-markdown2wechat

**工具**：`~/.openclaw/workspace-wechat-content-writer/skills/zhy-markdown2wechat/scripts/convert.js`

**调用方式**：
```bash
node ~/.openclaw/workspace-wechat-content-writer/skills/zhy-markdown2wechat/scripts/convert.js \
  <markdown文件路径> \
  <主题css路径> \
  <输出html路径>
```

**主题**：
- `resources/themes/default.css` — 经典紫色编辑风格
- `resources/themes/dark.css` — 深色护眼
- `resources/themes/blue.css` / `green.css` / `notion.css` / `vibrant.css` / `apple.css`

---

## CDN上传校验规范（强制）

### 上传前校验
- 文件格式：PNG / JPG / JPEG
- 文件大小：单张≤10MB

### 上传后校验
- 返回URL必须以 `mmbiz.qpic.cn` 开头
- URL可访问性：HEAD请求，返回 200/301/302 为通过

### 校验失败处理
- 必须重新上传
- 禁止携带无效/空链接继续执行
- 重试3次仍失败，报错并终止当前任务
