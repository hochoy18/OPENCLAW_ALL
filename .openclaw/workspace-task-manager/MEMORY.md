# 系统配置限制

## 工作空间限制
- **只能使用**: `workspace-task-manager` 工作空间
- **Agent 限制**: 只能使用 `task-manager` agent

## 执行规则
- 如果执行请求超出上述范围，直接报错返回
- 不执行任何不在 workspace-task-manager 范围内的操作

---

## 每日自动记忆

每天 23:00 自动执行：
1. 读取当日（00:00 - 23:00）当前 agent 的 session 历史
2. 提取关键内容：做了什么、产出什么、决策了什么
3. 追加写入 `[workspace]/memory/YYYY-MM-DD.md`
4. 格式参考 `memory/2026-03-25.md`

---
_记录时间: 2026-03-24_
