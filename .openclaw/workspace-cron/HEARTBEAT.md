# HEARTBEAT.md - AI科技情报日报

## 任务：每日 AI 情报推送

每天早上北京时间 7:00 左右检查并推送昨日 AI、AI Agent、大模型、科技、OpenClaw 方面热度 Top 5 资讯。

## 执行逻辑

1. 检查当前时间是否为北京时间 7:00-7:30 之间
2. 检查今日是否已推送（避免重复）
3. 如未推送，执行日报生成并推送到飞书

## 执行命令

```python
python3 skills/ai-tech-daily/scripts/daily.py
```

## 输出格式

- 标题：简洁精炼
- 内容：不超过50字
- 重点内容（含 OpenClaw/Agent/大模型/融资/发布/GPT/Claude/Llama）自动加粗高亮 ⭐

## 推送目标

飞书私聊：ou_a46824a36fa8086e31b863b652ce8d57

## 状态记录

- 上次推送时间：记录到 `output/last_push.txt`
- 推送历史：保存于 `output/YYYY-MM-DD/draft.md`
