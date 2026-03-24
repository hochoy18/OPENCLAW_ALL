# MEMORY.md

## 系统约束配置

### 工作空间限制
- **只允许工作空间**: `workspace-coder`
- **只允许使用 Agent**: `coder`

### 执行策略
如果执行任务时超出上述范围（非 workspace-coder 工作空间或非 coder agent），**直接报错返回**，不允许执行。

---

## 其他记忆
_(未来添加)_
