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
- ✅ 模式：Heartbeat（轮询检查）
- ✅ 时间：每天北京时间 7:00-7:30
- ✅ 防重复：记录上次推送日期，避免重复发送
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

## 每日自动记忆

每天 23:00 自动执行：
1. 读取当日（00:00 - 23:00）当前 agent 的 session 历史
2. 提取关键内容：做了什么、产出什么、决策了什么
3. 追加写入 `[workspace]/memory/YYYY-MM-DD.md`
4. 格式参考 `memory/2026-03-25.md`

---
## ⚠️ 忽略规则

- **`.openclaw` 目录下的所有修改我都不管**
- **任何 git / GitHub 相关操作都不管**（提交、推送、拉取等）
- 即使我看到相关输出，也不需要处理或回应

---

## 服务器文件路径约束
- **可以读写/tmp/, /temp/** 下的所有文件
- **知识库相关的文件以后都放在/home/hochoy/.openclaw/workspace-cron/knowledge/ 下**

---
## 发送图片规范
- **不要发路径文字**，直接发送图片文件到聊天框
- **发图片正确方式**：先调用 Feishu 上传图片 API 获取 image_key，再发送为 inline image（msg_type=image）
  - 上传：POST https://open.feishu.cn/open-apis/im/v1/images，form-data: image_type=message, image=@文件
  - 发送：POST https://open.feishu.cn/open-apis/im/v1/messages，body: {"receive_id": "群id", "msg_type": "image", "content": "{\"image_key\":\"刚才获取的key\"}"}
- 这是固定规范，必须遵守
