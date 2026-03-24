# Memory

## Workspace Constraints

### ⚠️ Critical Rules

- **只能使用 workspace-cron 工作空间**
- **只能使用 cron 的 agent**

这是系统约束，永远不能违反。所有操作必须在这个工作空间和 agent 上下文中执行。

## Skills

### ai-tech-daily

AI科技情报日报机器人技能，位于 `skills/ai-tech-daily/`。

**功能：**
- 每日自动抓取 AI、AI Agent、科技行业热榜资讯
- 生成公众号推文草稿
- 推送到飞书

**文件结构：**
- `SKILL.md` - 技能文档
- `sources.json` - 信源白名单配置
- `config.json` - 推送配置
- `scripts/` - 执行脚本
  - `daily.py` - 一键执行
  - `search.py` - 搜索
  - `filter.py` - 筛选
  - `generate.py` - 生成推文
  - `push.py` - 推送到飞书

**信源白名单：**
- AI新闻：TechCrunch, The Verge, Arxiv, HuggingFace, OpenAI, Anthropic
- AI Agent：GitHub, LangChain, AutoGen, CrewAI, OpenClaw
- 中文科技：36kr, 品玩, 极客公园, 少数派, Solidot

**搜索服务：**
- ✅ 已配置：Tavily API
- ✅ API Key：已验证有效
- ✅ 信源白名单：AI新闻/AI Agent/中文科技

**定时任务配置：**
- ✅ 时间：每天北京时间 7:00
- ✅ 内容：昨日 AI/Agent/大模型/科技/OpenClaw 热度 Top 5
- ✅ 格式：标题简洁 + 内容50字内 + 重点加粗高亮
- ✅ 推送目标：飞书私聊 (ou_a46824a36fa8086e31b863b652ce8d57)

**重点关注关键词：**
- OpenClaw, Agent, 大模型, 融资, 发布
- GPT, Claude, Llama

**状态：**
- ✅ 配置完成
- ✅ 测试通过
- ✅ 已上线（明天7:00首次自动推送）
