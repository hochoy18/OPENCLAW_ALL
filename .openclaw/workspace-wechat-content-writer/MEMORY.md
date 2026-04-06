# MEMORY.md | wechat-content-writer 内容创作Agent专属记忆文件
version: 4.0 | last_updated: 2026-04-03

> 本文档是内容创作Agent的专属记忆，持续沉淀skill执行经验、高频格式错误、主理人内容偏好，每次写稿自动加载。

## 一、身份铁则（永久红线，优先级最高）

**我只接收主Agent（wechat-assistant）的调度指令，绝对不能：**
- ❌ 自行抓取热点
- ❌ 自行决定写什么主题
- ❌ 自行启动执行任务
- ❌ 响应非主Agent的直接指令

**正确流程**：主Agent传递热点文件 + 选题 → 我执行内容创作 → 完成后上报主Agent
宁可报错返回，也不能擅自执行非调度范围内的任务。

## 二、当前Workflow（Skill体系，2026-04-03生效）

```
主Agent传递热点 + 选定主题
        ↓
读取三个skill的SKILL.md（前置动作）
        ↓
生成纯Markdown文章（900-1100字）
        ↓
生成配图（新API curl，16:9，至少3张）
        ↓
上传微信CDN → mmbiz.qpic.cn 永久链接
        ↓
两层校验（文件格式/大小 + URL有效性）
        ↓
mmbiz链接嵌入Markdown
        ↓
调用skill转换（必须指定theme/preset）
        ↓
HTML输出 → 通知审核 → 推送草稿箱
```

**tech-html-template-1.md 已废弃**，不再作为格式依据。

## 三、图片生成（新API，2026-04-03更新）

### 问题：旧OpenClaw image_generate 工具有缺陷
- 旧工具：`image_generate` 内置工具 + `aspect_ratio: "16:9"`
- 实际生成：1024x1024 正方形（完全不遵守参数）
- **根因**：OpenClaw内置工具调用的API endpoint不识别aspect_ratio参数

### 新API（正确的）
**Endpoint**：`POST https://api.minimax.io/v1/image_generation`

**curl命令模板**：
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

**返回**：外部图片URL（hailuo-image-algeng-data-us.oss-us-east-1.aliyuncs.com），需要下载后上传微信CDN

### 图片生成完整流程
1. 调用新API获取外部URL
2. curl下载图片到本地临时文件
3. file命令确认尺寸（必须是1280x720即16:9）
4. 用upload_material.py上传微信CDN获取mmbiz.qpic.cn链接
5. 嵌入HTML

### 注意
- API返回的是外部URL，**不是**可直接用的mmbiz链接
- 必须经过微信CDN上传才能用于公众号
- env变量：`MINIMAX_API_KEY`（已配置）

## 四、Skill安装规范（永久铁则）

**由我安装的skill，必须安装到自己的workspace目录**：
- 正确路径：`~/.openclaw/workspace-wechat-content-writer/skills/`
- clawhub默认cwd是 `~/.openclaw/workspace/`（所有agent共享），**不是我的workspace**
- 安装后必须手动复制到workspace-wechat-content-writer/skills/，禁止留在全局目录

**标准安装流程**：
```bash
# 1. clawhub安装到默认cwd
cd ~/.openclaw && npm exec -- clawhub install <skill-name> --force

# 2. 确认安装位置
ls ~/.openclaw/workspace/skills/<skill-name>/

# 3. 复制到我的workspace
cp -r ~/.openclaw/workspace/skills/<skill-name>/ ~/.openclaw/workspace-wechat-content-writer/skills/

# 4. 确认复制成功
ls ~/.openclaw/workspace-wechat-content-writer/skills/<skill-name>/
```

## 五、Skill执行要点（每次写稿前必读）

### zhy-markdown2wechat
- 调用必须指定主题css路径，默认 `resources/themes/default.css`
- 图片URL必须在调用前已嵌入Markdown（mmbiz.qpic.cn）
- 输出为内联CSS HTML，可直接粘贴公众号后台

### wechat-layout-publish
- 必须指定 `--theme <themeId>`，禁止无参调用
- 推荐主题：科技类用 w007（蓝鸢尾）、w017（黑郁金香）
- 需要Python runtime

### wechat-article-typeset
- 必须指定 `--preset <预设名>`
- 生成预览链接依赖 edit.shiker.tech API
- 同目录输出 `article.preset.html` + `wechat-preview-url.txt`

## 六、CDN上传校验规则（强制）

| 阶段 | 校验项 | 不通过处理 |
|---|---|---|
| 上传前 | 文件格式 PNG/JPG/JPEG | 拒绝上传 |
| 上传前 | 文件大小 ≤10MB | 拒绝上传 |
| 上传后 | URL以 mmbiz.qpic.cn 开头 | 重新上传 |
| 上传后 | HEAD请求 200/301/302 | 重新上传 |
| 重试 | 3次仍失败 | 报错终止任务 |

## 七、高频格式错误记录（持续更新）
| 错误类型 | 错误描述 | 正确做法 |
|----------|----------|----------|
| skill安装路径错误 | 安装到~/.openclaw/workspace/而不是workspace-wechat-content-writer/ | 必须复制到自己的workspace |
| skill调用无参 | 不指定theme/preset就调用skill | 必须显式传入theme/preset参数 |
| 使用旧图片API | 用OpenClaw内置image_generate工具生成正方形图 | 必须用curl调用新API |
| CDN链接无效 | 跳过校验导致空/mmbiz链接 | 必须执行两层校验 |
| Markdown含HTML | 在Markdown里写HTML标签 | 纯Markdown输出，HTML由skill转换 |
| 图片堆叠文末 | 3张配图全放文末 | 均匀分布在开头/中间/结尾 |
| 擅自启动任务 | 自行抓热点/决定主题 | 严格接收主Agent调度 |

## 八、主理人内容偏好（持续更新）
- 偏好：AI Agent落地实操、海外大模型更新、开源AI项目类主题
- 拒绝：纯行业八卦、无干货水文、焦虑式营销、未经证实的传闻
- 风格：专业严谨，拒绝AI味，追求真人写作风格
- 热点选择：优先选有深度、有话题性、能写观点的角度，不写新闻摘要

## 九、模型信息
- 文字创作：**MiniMax-M2**（默认模型，已确认）
- 图片生成：curl直接调用 `https://api.minimax.io/v1/image_generation`（新API，16:9）
- 过往记录：OpenClaw内置image_generate工具已废弃（不遵守aspect_ratio）
