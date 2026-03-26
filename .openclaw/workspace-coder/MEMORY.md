# MEMORY.md

## 系统约束配置

### 工作空间限制
- **只允许工作空间**: `workspace-coder`
- **只允许使用 Agent**: `coder`

### 执行策略
如果执行任务时超出上述范围（非 workspace-coder 工作空间或非 coder agent），**直接报错返回**，不允许执行。

---

## 每日自动记忆

每天 23:00 自动执行：
1. 读取当日（00:00 - 23:00）当前 agent 的 session 历史
2. 提取关键内容：做了什么、产出什么、决策了什么
3. 追加写入 `[workspace]/memory/YYYY-MM-DD.md`
4. 格式参考 `memory/2026-03-25.md`

---

## 其他记忆
_(未来添加)_
