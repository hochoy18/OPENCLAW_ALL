# 系统配置限制

## 工作空间限制
- **只能使用**: `workspace-task-manager` 工作空间
- **Agent 限制**: 只能使用 `task-manager` agent

## 执行规则
- 如果执行请求超出上述范围，直接报错返回
- 不执行任何不在 workspace-task-manager 范围内的操作

---
_记录时间: 2026-03-24_
