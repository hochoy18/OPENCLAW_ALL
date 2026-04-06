# TOOLS.md - Local Notes
version: 3.0 | last_updated: 2026-04-03

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
- 图片生成：**curl直接调用新API**（不用OpenClaw内置image_generate工具）

---

## 图片生成（2026-04-03更新：必须用新API）

### 为什么废弃OpenClaw内置工具
OpenClaw内置 `image_generate` 工具调用的是旧API endpoint，不遵守 `aspect_ratio` 参数，
实际生成1024x1024正方形而非16:9。

### 新API调用方式（必须用）

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
6. 嵌入HTML

### 环境变量
- `MINIMAX_API_KEY`：已配置在env中，直接使用即可

---

## 新Skill体系（2026-04-03生效）

### Skill 1: zhy-markdown2wechat
路径：`~/.openclaw/workspace-wechat-content-writer/skills/zhy-markdown2wechat/`

**调用方式**：
```bash
node ~/.openclaw/workspace-wechat-content-writer/skills/zhy-markdown2wechat/scripts/convert.js \
  <markdown文件路径> \
  <主题css路径> \
  <输出html路径>
```

**主题**（必须指定）：
- `resources/themes/default.css` — 经典紫色编辑风格（默认）
- `resources/themes/blue.css` / `green.css` / `dark.css` / `notion.css` / `vibrant.css` / `apple.css`

---

### Skill 2: wechat-layout-publish
路径：`~/.openclaw/workspace-wechat-content-writer/skills/wechat-layout-publish/`

**调用方式**（需Python runtime）：
```bash
python3 ~/.openclaw/workspace-wechat-content-writer/skills/wechat-layout-publish/scripts/render_wechat_html.py \
  --theme <themeId> \
  --input <markdown路径> \
  --output <输出html路径>
```

**主题catalog**（必须指定）：
- Formal报告：`w001`玉兰、`w006`白百合、`w010`铃兰、`w011`白茶
- 文艺生活：`w002`牡丹、`w013`梅花、`w014`勿忘我、`w022`月见草、`w023`樱花
- 科技产品：`w003`雏菊、`w007`蓝鸢尾、`w017`黑郁金香、`w021`朱槿
- 强视觉：`w004`向日葵、`w005`罂粟、`w018`金盏花、`w019`山茶

---

### Skill 3: wechat-article-typeset
路径：`~/.openclaw/workspace-wechat-content-writer/skills/wechat-article-typeset/`

**调用方式**：
```bash
node ~/.openclaw/workspace-wechat-content-writer/skills/wechat-article-typeset/wechat-copy.js <input.md>
```

**常用预设**（必须指定）：
- 暖色系：`暖色色块`、`金秋渐变`、`琥珀色块`
- 冷色/商务：`墨色极简`、`青绿左边线`、`蓝鸢尾`
- 极简黑白：`极简黑白`、`极简色块`
- 特色：`雁栖湖`、`深色护眼`、`樱粉色块`

---

## CDN上传校验规范（强制）

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
