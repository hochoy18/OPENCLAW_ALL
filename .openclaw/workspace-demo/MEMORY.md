# MEMORY.md - 长期记忆

## 核心配置限制 (Critical Constraints)

### 工作空间限制
- **允许的工作空间**: 仅限 `workspace-demo`
- **禁止**: 任何在 `workspace-demo` 范围外的文件操作或执行

### Agent 限制
- **允许的 Agent**: 仅限 `demo`
- **禁止**: 使用其他 agent 执行操作

### 执行策略
如果用户请求的操作超出以上范围：
1. **直接报错返回** - 不执行操作
2. **说明限制** - 告知用户当前仅支持 workspace-demo 和 demo agent

---

## 其他记忆
_(随着使用逐步添加)_
