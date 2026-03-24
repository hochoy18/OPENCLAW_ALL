---
name: ai-tech-daily
description: AI科技情报日报机器人 - 每日自动抓取AI/Agent/科技行业热榜资讯，生成公众号推文草稿，推送至飞书。整合搜索+生成+推送全流程。
metadata:
  openclaw:
    emoji: 📰
    category: content
---

# AI科技情报日报机器人

每日自动抓取全网AI、AI Agent、科技行业热榜资讯，生成可直接发布的公众号推文草稿，并推送至飞书。

## 工作流程

```
[定时触发] → [信源搜索] → [内容筛选] → [生成推文] → [飞书推送]
```

## 1. 信源搜索

### 配置信源白名单

编辑 `sources.json` 配置信源：

```json
{
  "ai_news": {
    "domains": [
      "techcrunch.com",
      "theverge.com",
      "venturebeat.com",
      "arxiv.org",
      "huggingface.co",
      "openai.com",
      "anthropic.com"
    ],
    "keywords": ["AI", "artificial intelligence", "LLM", "machine learning"]
  },
  "ai_agent": {
    "domains": [
      "github.com",
      "langchain.com",
      "autogen.ai",
      "crewai.com"
    ],
    "keywords": ["AI Agent", "autonomous agent", "multi-agent"]
  },
  "tech": {
    "domains": [
      "36kr.com",
      "pingwest.com",
      "geekpark.net",
      "solidot.org",
      "ifanr.com"
    ],
    "keywords": ["科技", "startup", "融资", "新产品"]
  }
}
```

### 执行搜索

```bash
# 使用 desearch 搜索（推荐）
cd /home/hochoy/.openclaw/workspace-cron/skills/ai-tech-daily
python3 scripts/search.py --category ai_news --hours 24

# 或手动搜索
mcporter call 'exa.web_search_exa(query: "AI Agent latest news 2025", numResults: 20)'
```

## 2. 内容筛选

### 筛选标准

- **时效性**：24小时内发布
- **热度**：Twitter/X 讨论数、Reddit upvotes、GitHub stars 增长
- **价值**：对从业者有实际参考价值，非标题党
- **去重**：同一事件只保留最权威来源

### 执行筛选

```bash
python3 scripts/filter.py --input raw_results.json --output filtered.json
```

## 3. 生成推文

### 输出格式

```markdown
# AI科技情报日报 | 2025年3月24日

## 🔥 今日热点

### 1. [标题]
**来源**：[来源名] | **时间**：X小时前
**摘要**：一句话核心要点
**链接**：[原文链接]

### 2. [标题]
...

## 🤖 AI Agent 动态

...

## 💡 深度阅读

...

---
*由 AI科技情报日报机器人 自动生成*
```

### 执行生成

```bash
python3 scripts/generate.py --input filtered.json --output draft.md
```

## 4. 飞书推送

### 配置推送目标

编辑 `config.json`：

```json
{
  "feishu": {
    "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx",
    "chat_id": "oc_xxx"
  },
  "schedule": {
    "time": "09:00",
    "timezone": "Asia/Shanghai"
  }
}
```

### 执行推送

```bash
python3 scripts/push.py --content draft.md
```

## 5. 一键执行

```bash
# 完整流程
python3 scripts/daily.py

# 手动触发（不检查时间）
python3 scripts/daily.py --force
```

## 定时配置

在 `HEARTBEAT.md` 或 cron 中配置：

```bash
# 每天早上 9:00 执行
0 9 * * * cd /home/hochoy/.openclaw/workspace-cron && python3 skills/ai-tech-daily/scripts/daily.py
```

## 文件结构

```
skills/ai-tech-daily/
├── SKILL.md              # 本文件
├── config.json           # 推送配置
├── sources.json          # 信源配置
├── scripts/
│   ├── search.py         # 搜索脚本
│   ├── filter.py         # 筛选脚本
│   ├── generate.py       # 生成脚本
│   ├── push.py           # 推送脚本
│   └── daily.py          # 一键执行
└── output/               # 输出目录
    └── YYYY-MM-DD/
        ├── raw.json      # 原始搜索结果
        ├── filtered.json # 筛选后结果
        └── draft.md      # 推文草稿
```

## 依赖

- Python 3.8+
- `requests` - HTTP 请求
- `desearch` - 搜索 API（或 Exa/Brave）
- `jinja2` - 模板渲染

## 注意事项

- 每日执行前检查 `sources.json` 是否需要更新
- 定期review输出质量，调整筛选阈值
- 飞书 webhook 有频率限制，注意控制推送频率
