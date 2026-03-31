

### 5.2 全局MEMORY.md

路径：`~/.openclaw/workspace-wechat-assistant/MEMORY.md`

```markdown
# MEMORY.md | 公众号内容生产长期核心记忆

version: 1.0 | last_updated: {{自动更新最新执行日期}}

## 一、公众号基础信息（永久记忆）

- 公众号名称：【待填写】
- 公众号定位：AI/AI Agent/大模型/科技领域垂直专业IP
- 核心受众：AI从业者、技术开发者、产品经理、科技爱好者、AI创业人群
- 更新频率：日更1篇
- 发布规则：仅推送至草稿箱，正式发布需主理人手动确认
- 热点源要求：海外权威信息源为主，国内信息源为辅

## 二、主理人内容偏好（持续更新）

- 标题偏好：【待填写】
- 内容偏好：【待填写】
- 排版偏好：简约科技风，行间距1.75，正文16px，重点内容标红
- 配图偏好：【待填写】
- 禁用内容：【待填写】

## 三、爆款内容方法论（持续迭代）

1. 选题爆款特征：【待沉淀】
2. 标题爆款公式：【待沉淀】
3. 结构爆款逻辑：开头100字点明核心价值，中间分3段讲干货，结尾总结+引导关注
4. 发布最佳时间：工作日早上7:30-8:30

## 四、避坑与合规规则（永久记忆）

1. 微信公众平台内容合规红线，绝对不触碰
2. 技术内容必须可溯源，不编造参数、不夸大技术效果
3. 不发布未经证实的海外行业传闻
4. 未经主理人确认，绝对不执行正式群发发布
5. 所有图片必须使用合规无版权素材
6. 严格遵循独立Workspace隔离规则

## 五、全Agent Workspace索引（永久有效）

| Agent | Workspace路径 |
|-------|--------------|
| 主Agent | ~/.openclaw/workspace-wechat-assistant/ |
| hot-collector | ~/.openclaw/workspace-hot-collector/ |
| topic-selector | ~/.openclaw/workspace-topic-selector/ |
| article-writer | ~/.openclaw/workspace-article-writer/ |
| quality-auditor | ~/.openclaw/workspace-quality-auditor/ |
| draft-publisher | ~/.openclaw/workspace-draft-publisher/ |

## 六、历史发布记录（持续追加）

| 日期 | 主题 | 标题 | 推送结果 | 备注 |
|------|------|------|---------|------|
| | | | | |
```

### 5.3 全局AGENTS.md

路径：`~/.openclaw/workspace-wechat-assistant/AGENTS.md`

```markdown
# AGENTS.md | 全局Agent索引

## Agent列表

| Agent ID | 名称 | Workspace | 核心职责 |
|----------|------|-----------|---------|
| wechat-assistant | 主Agent | workspace-wechat-assistant | 全局调度、用户交互、数据中转 |
| hot-collector | 热点采集Agent | workspace-hot-collector | 海外热点采集 |
| topic-selector | 选题筛选Agent | workspace-topic-selector | 热点二次筛选、价值评估 |
| article-writer | 文章创作Agent | workspace-article-writer | 文章写作、配图生成 |
| quality-auditor | 质量审核Agent | workspace-quality-auditor | 全维度质量审核 |
| draft-publisher | 草稿发布Agent | workspace-draft-publisher | 草稿箱推送 |

## 文件传递路径

```
workspace-hot-collector/output/{{date}}.md
    ↓ 主Agent读取校验
    ↓ 复制到
workspace-topic-selector/input/{{date}}-hots.md
    ↓ topic-selector执行
workspace-topic-selector/output/{{date}}-topics.md
    ↓ 主Agent读取校验，展示给用户
    ↓ 用户选定，主Agent复制到
workspace-article-writer/input/{{date}}-selected-topic.md
    ↓ article-writer执行
workspace-article-writer/output/{{date}}-article.md
+ workspace-article-writer/images/
    ↓ 主Agent读取校验，复制到
workspace-quality-auditor/input/{{date}}-article.md
    ↓ quality-auditor执行
workspace-quality-auditor/output/{{date}}-audit-report.md
    ↓ 主Agent读取校验，展示给用户
    ↓ 用户确认，主Agent复制到
workspace-draft-publisher/input/{{date}}-final-article.md
    ↓ draft-publisher执行
workspace-draft-publisher/output/{{date}}-publish-log.md
    ↓ 主Agent读取校验，通知用户
```

## Skill绑定

| Agent | Skill | 用途 |
|-------|-------|------|
| hot-collector | tavily-search | 搜索热点 |
| article-writer | wechat-article-crayon | 文章写作 |
| article-writer | generate_cover.py | 生成封面图 |
| article-writer | upload_material.py | 上传配图到公众号 |
| draft-publisher | mp-draft-push | 推送草稿箱 |
```

---

## 六、定时任务配置

### 6.1 定时任务清单

| 任务名称 | Agent | 执行时间 | Cron表达式 | 用途 |
|---------|-------|---------|-----------|------|
| 每日热点采集 | hot-collector | 每天07:00 | `0 7 * * *` | 抓取前一天热点 |
| 每日选题通知 | wechat-assistant | 每天07:30 | `0 7 * * *` | 通知用户选主题 |

### 6.2 不设置定时任务的Agent

以下Agent不设置定时任务，由主Agent根据流程和用户指令调度：
- topic-selector：等用户选完主题后触发
- article-writer：用户选定主题后触发
- quality-auditor：文章创作完成后触发
- draft-publisher：用户确认审核报告后触发

### 6.3 定时任务配置示例

```bash
# 定时任务1：每日热点采集
openclaw cron add \
  --name "daily-hot-collect" \
  --cron "0 7 * * *" \
  --tz "Asia/Shanghai" \
  --message "执行热点采集：从海外信息源抓取前一天00:00-23:59的AI领域热点，写入 workspace-hot-collector/output/{{date}}.md" \
  --session isolated \
  --timeout-seconds 300

# 定时任务2：每日选题提醒
openclaw cron add \
  --name "daily-topic-reminder" \
  --cron "0 7 * * *" \
  --tz "Asia/Shanghai" \
  --message "检查今日热点是否已采集完毕。如已完成，向用户展示待选主题列表，等待用户选定。" \
  --session main \
  --timeout-seconds 60
```

---

## 七、Skill安装清单

| Agent | Skill名称 | 安装位置 | 用途 |
|-------|----------|---------|------|
| hot-collector | tavily-search | workspace-wechat-assistant/skills/tavily-search | 搜索热点 |
| article-writer | wechat-article-crayon | workspace-wechat-assistant/skills/wechat-article-crayon | 文章写作风格 |
| article-writer | generate_cover.py | workspace-wechat-assistant/skills/wechat-article-publisher/scripts/generate_cover.py | 生成封面图 |
| article-writer | upload_material.py | workspace-wechat-assistant/skills/wechat-article-publisher/scripts/upload_material.py | 上传配图 |
| draft-publisher | mp-draft-push | workspace-wechat-assistant/skills/mp-draft-push | 推送草稿箱 |

---

## 八、环境搭建清单

### 8.1 目录创建

```bash
# 创建各Agent独立Workspace根目录
mkdir -p ~/.openclaw/workspace-hot-collector/{output,memory,logs}
mkdir -p ~/.openclaw/workspace-topic-selector/{input,output,memory,logs}
mkdir -p ~/.openclaw/workspace-article-writer/{input,output,images,memory,logs}
mkdir -p ~/.openclaw/workspace-quality-auditor/{input,output,memory,logs}
mkdir -p ~/.openclaw/workspace-draft-publisher/{input,output,memory,logs}

# 创建主Agent全局目录
mkdir -p ~/.openclaw/workspace-wechat-assistant/{agents,global/transfer}
```

### 8.2 配置文件写入

各Agent的SOUL.md和MEMORY.md需要在初始化时写入对应目录。

### 8.3 OpenClaw Agent注册

每个子Agent需要在OpenClaw中注册：

```bash
# 注册hot-collector Agent
openclaw agent add --id hot-collector --name "热点采集Agent" --workspace ~/.openclaw/workspace-hot-collector

# 注册topic-selector Agent
openclaw agent add --id topic-selector --name "选题筛选Agent" --workspace ~/.openclaw/workspace-topic-selector

# 注册article-writer Agent
openclaw agent add --id article-writer --name "文章创作Agent" --workspace ~/.openclaw/workspace-article-writer

# 注册quality-auditor Agent
openclaw agent add --id quality-auditor --name "质量审核Agent" --workspace ~/.openclaw/workspace-quality-auditor

# 注册draft-publisher Agent
openclaw agent add --id draft-publisher --name "草稿发布Agent" --workspace ~/.openclaw/workspace-draft-publisher
```

---

## 九、工作流程总结

### 9.1 每日工作流

```
07:00 ┬─ 定时任务：hot-collector 执行热点采集
      │   └─ 输出：workspace-hot-collector/output/{{date}}.md
      │
07:30 ┼─ 定时任务：主Agent通知用户展示待选主题
      │
      │  【用户选定主题，如：选第2个】
      │
      │  主Agent将选定主题复制到：
      │  └─ workspace-article-writer/input/{{date}}-selected-topic.md
      │
      ├─ 主Agent调度 article-writer
      │   └─ 输出：workspace-article-writer/output/{{date}}-article.md
      │         + workspace-article-writer/images/
      │
      │  主Agent将文章复制到：
      │  └─ workspace-quality-auditor/input/{{date}}-article.md
      │
      ├─ 主Agent调度 quality-auditor
      │   └─ 输出：workspace-quality-auditor/output/{{date}}-audit-report.md
      │
      │  【用户审查审核报告，确认发布】
      │
      │  主Agent将终稿复制到：
      │  └─ workspace-draft-publisher/input/{{date}}-final-article.md
      │
      └─ 主Agent调度 draft-publisher
          └─ 输出：workspace-draft-publisher/output/{{date}}-publish-log.md

      【完成：主Agent通知用户草稿已推送】
```

### 9.2 关键文件路径

| 文件 | 路径 |
|-----|------|
| 主Agent全局配置 | ~/.openclaw/workspace-wechat-assistant/ |
| 全局SOUL.md | ~/.openclaw/workspace-wechat-assistant/SOUL.md |
| 全局MEMORY.md | ~/.openclaw/workspace-wechat-assistant/MEMORY.md |
| 今日热点 | ~/.openclaw/workspace-hot-collector/output/{{date}}.md |
| 今日待选主题 | ~/.openclaw/workspace-topic-selector/output/{{date}}-topics.md |
| 今日文章 | ~/.openclaw/workspace-article-writer/output/{{date}}-article.md |
| 今日审核报告 | ~/.openclaw/workspace-quality-auditor/output/{{date}}-audit-report.md |
| 今日推送日志 | ~/.openclaw/workspace-draft-publisher/output/{{date}}-publish-log.md |

---

## 十、异常处理机制

### 10.1 热点采集失败
- 自动重试1次
- 仍失败则记录日志到 workspace-hot-collector/logs/{{date}}.log
- 主Agent向用户反馈，提供「手动选题/更换信息源重试/终止流程」选项

### 10.2 文章不符合要求
- 主Agent立即向用户反馈问题
- 支持「全文重写/局部修改/终止流程」
- 无需重跑前面所有环节

### 10.3 审核不通过
- 主Agent展示审核报告和不通过原因
- 用户修改完成后，可单独重新触发审核
- 无需重跑前面所有环节

### 10.4 推送失败
- 自动重试2次
- 仍失败则记录日志
- 主Agent向用户反馈具体报错（如IP白名单、凭证问题）

### 10.5 定时任务失败
- 自动重试1次
- 仍失败则记录日志
- 次日用户打开会话时第一时间反馈

---

*文档结束*
