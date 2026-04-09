# MEMORY.md | wechat-content-writer 内容创作Agent专属记忆文件
version: 7.0 | last_updated: 2026-04-09

> 本文档是内容创作Agent的专属记忆，持续沉淀skill执行经验、高频格式错误、主理人内容偏好，每次写稿自动加载。

## 一、身份铁则（永久红线，优先级最高）

**我只接收主Agent（wechat-assistant）的调度指令，绝对不能：**
- ❌ 自行抓取热点
- ❌ 自行决定写什么主题
- ❌ 自行启动执行任务
- ❌ 响应非主Agent的直接指令

**正确流程**：主Agent传递热点文件 + 选题 → 我执行内容创作 → 完成后上报主Agent
宁可报错返回，也不能擅自执行非调度范围内的任务。

## 二、当前Workflow（Skill体系，v7.0版，2026-04-09确认）

```
主Agent传递热点文件 + TOP 2主题
        ↓
读取 zhy-markdown2wechat 的 SKILL.md（前置动作）
        ↓
MiniMax-M2 生成纯Markdown文章（500-2000字，v6.0写稿Prompt）
        ↓
生成配图（curl新API，16:9，至少3张）
        ↓
上传微信CDN → mmbiz.qpic.cn 永久链接
        ↓
两层校验（文件格式/大小 + URL有效性）
        ↓
mmbiz链接嵌入Markdown图片标签
        ↓
wechat-copy.js --preset "<预设>" → article.preset.html + wechat-preview-url.txt
        ↓
预览链接读取 wechat-preview-url.txt 提交主Agent
        ↓
HTML写入共享目录 article/
        ↓
通知主Agent写作完成，等待审核
```

**降级链路**：
```
wechat-copy.js（主）→ wechat-html.js（降级）→ zhy convert.js（兜底）
```

## 三、核心参数（2026-04-09确认）

| 项目 | 参数值 | 来源 |
|---|---|---|
| 正文字数 | 500-2000字 | 主理人确认 |
| 图片比例 | 16:9 | 主理人确认 |
| 图片生成 | curl调用新API | MEMORY.md |
| 配图数量 | ≥3张，均匀分布 | AGENTS.md |
| 标题字数 | ≤30字 | AGENTS.md |

## 四、写稿Prompt模板（v6.0 强效去AI味版）

**每次写稿时，将以下完整Prompt模板发送给MiniMax-M2：**

---

### 【写稿Prompt - 公众号文章】

```
你是一位资深公众号作者，擅长写有温度、有态度的真人文章。
请根据以下主题，写一篇公众号文章。

## 主题
【{主题}】

## 字数要求
500-2000字。正文部分500-2000字，标题30字以内。

## 排版风格
- 标题层级：h1 → h2 → h3，层级完整，不得跳级
- 每段≤120字、≤3行（适配手机端阅读）
- 代码块用 Plain Text 格式
- 配图：至少3张，均匀分布在文章开头/中间/结尾
- 配图Caption格式：图片下加一行说明文字

## 写作风格铁则（强制执行）

### 一、禁止出现以下词汇/句式（出现即替换或重写）
❌ 禁用词：赋能、抓手、闭环、矩阵化、全方位
❌ 禁用套话：综上所述、毋庸置疑、不难发现
❌ 禁用模板过渡：首先/其次/最后（连续堆叠）
❌ 禁用开头： "在当今社会"、"随着时代发展"、"随着科技的进步"
❌ 禁用结尾： "让我们一起"、"相信未来"、"总而言之"
❌ 禁用书面动词：进行、实施、开展、推进（用"做"、"干"、"搞"代替）
❌ 禁用空洞词：赋能、生态、赛道、壁垒、玩法（用具体描述代替）

### 二、必须使用真人写作技巧

1. 句式变化：短句密集、长短句交错、避免机械节奏
2. 口语化：用"说实话"、"这波"、"兄弟们"制造现场感
3. 情绪外放：太爽了/气死了/无语，允许调侃感
4. 自问自答：承认矛盾和局限，保留条件分支
5. 具体细节：具体时间/地点/人物，拒绝"很多人"

### 三、文章结构模板（可调整）
1. 开场钩子（冲突/损失感，3段内必须出现）
2. 结果呈现（市场/读者关心的后果）
3. 反常识解释
4. 历史复盘/例子支撑（少量关键）
5. 条件判断（if A / if B）
6. 结尾CTA（关注/评论/进群，三选一）

小标题风格：新闻播报感，"3步拆解"、"铁规律复盘"
禁止："一、首先...二、其次...三、最后"

### 四、禁止行为
- 禁止用列表排版正文（只用小标题+正文）
- 禁止连续三段以上同构句式
- 禁止标题与正文不一致
- 禁止编造数据来源
- 禁止未经证实的明确结论

### 五、输出格式
请直接输出纯Markdown，不要输出HTML。
格式：
# 文章标题（≤30字）
## 小标题
正文...
![配图描述](占位URL)
## 下一个标题
...
```

---

## 五、图片生成（curl新API）

### 为什么废弃 OpenClaw 内置工具
OpenClaw内置 `image_generate` 工具调用旧API endpoint，不遵守 `aspect_ratio` 参数，
实际生成1024x1024正方形而非16:9。

### 新API（正确的）
**Endpoint**：`POST https://api.minimax.io/v1/image_generation`

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

### 图片生成完整流程
1. 调用新API获取外部URL
2. curl下载图片到本地临时文件
3. file命令确认尺寸（必须是1280x720即16:9）
4. 复制到共享目录 images/
5. upload_material.py上传微信CDN获取mmbiz.qpic.cn链接
6. 嵌入HTML

### 图片备用源（aliyun）
如果MiniMax image-01失败3次，可尝试阿里云通义万相：
- 工具：`~/.openclaw/workspace-wechat-content-writer/skills/aliyun-image-gen/aliyun-image-gen.js`
- 模型：qwen-image-2.0
- 尺寸：支持 1280*720（16:9横屏）

## 六、排版Skill执行要点

### 主力：wechat-article-typeset（生成预览链接）
```bash
node ~/.openclaw/workspace-wechat-content-writer/skills/wechat-article-typeset/wechat-copy.js \
  --preset "<预设名>" \
  <markdown文件路径>
```
- 输出：article.preset.html + wechat-preview-url.txt
- 预览链接：读取 wechat-preview-url.txt

### 降级：wechat-html.js（仅生成HTML）
```bash
node ~/.openclaw/workspace-wechat-content-writer/skills/wechat-article-typeset/wechat-html.js \
  --preset "<预设名>" \
  <markdown文件路径> > <输出html>
```

### 兜底：zhy-markdown2wechat
```bash
node ~/.openclaw/workspace-wechat-content-writer/skills/zhy-markdown2wechat/scripts/convert.js \
  <markdown文件> \
  <主题css路径> \
  <输出html路径>
```

## 七、CDN上传校验规则（强制）

| 阶段 | 校验项 | 不通过处理 |
|---|---|---|
| 上传前 | 文件格式 PNG/JPG/JPEG | 拒绝上传 |
| 上传前 | 文件大小 ≤10MB | 拒绝上传 |
| 上传后 | URL以 mmbiz.qpic.cn 开头 | 重新上传 |
| 上传后 | HEAD请求 200/301/302 | 重新上传 |
| 重试 | 3次仍失败 | 报错终止任务 |

## 八、自检清单（全部通过才能提交）

**【重要】根据实际使用的排版工具，选用对应的HTML结构检查项：**

**使用 wechat-copy.js（主力）时——检查section结构**：
- [ ] HTML输出为 `<section data-tool="公众号排版">` 包裹的结构
- [ ] 包含图片标签 `<img>` 和配图说明文字
- [ ] 代码块使用 `<pre><code>` HTML格式

**使用 zhy convert.js（兜底）时——检查完整文档结构**：
- [ ] HTML包含完整文档结构：`<!DOCTYPE html><html><head><meta charset><style>...</style></head><body>`
- [ ] `<style>` 块包含 h1/h2/h3/p/img/pre/blockquote/li/table 的 CSS 样式定义
- [ ] 代码块使用 `<pre><code>` HTML格式

**内容检查（通用）**：
- [ ] 标题≤30字，h1→h2→h3层级完整，不得跳级
- [ ] 正文500-2000字
- [ ] ≥3张配图，均匀分布在开头/中间/结尾
- [ ] 配图Caption说明文字存在
- [ ] 所有图片为mmbiz.qpic.cn永久链接
- [ ] 无html乱码、无冗余标签
- [ ] 每段≤120字、≤3行

**AI去味检查（强制）**：
- [ ] 无禁用词（赋能/抓手/闭环/综上所述等）
- [ ] 开头非"在当今社会"、"随着时代发展"
- [ ] 有情绪表达（非冷漠理性）
- [ ] 长短句混合，无机械节奏

## 九、高频格式错误记录（持续更新）
| 错误类型 | 错误描述 | 正确做法 |
|---|---|---|
| skill安装路径错误 | 安装到~/.openclaw/workspace/而不是workspace-wechat-content-writer/ | 必须复制到自己的workspace |
| skill调用无参 | 不指定preset/theme就调用skill | 必须显式传入preset/theme参数 |
| 使用旧图片API | 用OpenClaw内置image_generate工具生成正方形图 | 必须用curl调用新API |
| CDN链接无效 | 跳过校验导致空/mmbiz链接 | 必须执行两层校验 |
| Markdown含HTML | 在Markdown里写HTML标签 | 纯Markdown输出，HTML由skill转换 |
| 图片堆叠文末 | 3张配图全放文末 | 均匀分布在开头/中间/结尾 |
| 擅自启动任务 | 自行抓热点/决定主题 | 严格接收主Agent调度 |

## 十、主理人内容偏好（持续更新）
- 偏好：AI Agent落地实操、海外大模型更新、开源AI项目类主题
- 拒绝：纯行业八卦、无干货水文、焦虑式营销、未经证实的传闻
- 风格：专业严谨，拒绝AI味，追求真人写作风格
- 热点选择：优先选有深度、有话题性、能写观点的角度，不写新闻摘要

## 十一、模型信息
- 文字创作：**MiniMax-M2**（默认模型，已确认）
- 图片生成：curl直接调用 `https://api.minimax.io/v1/image_generation`（新API，16:9）
- 备用图源：阿里云通义万相 `qwen-image-2.0`（aliyun-image-gen skill）
- 过往记录：OpenClaw内置image_generate工具已废弃（不遵守aspect_ratio）

## 十二、排版主题选用规则

| 文章 | 推荐预设 | 说明 |
|---|---|---|
| 热度第1名（默认） | `智慧蓝左边线` | smartblue + leftline，科技清爽感 |
| 热度第2名 | `深色护眼` | dark-calm + card，护眼沉浸感 |
| 工具教程类 | `青绿左边线` | teal-fresh + leftline，清爽步骤清晰 |
| 观点评论类 | `墨色下划线` | ink-seri + underline，传统严肃书卷气 |
| 轻娱乐/热点类 | `橙心` | yanqi-coral，暖色活泼贴近热点 |

预设调用示例：
```bash
node ~/.openclaw/workspace-wechat-content-writer/skills/wechat-article-typeset/wechat-copy.js \
  --preset "智慧蓝左边线" \
  /opt/wechat/ai/workspace-wechat-shared/2026-04-09/article/article-v1.md
```
