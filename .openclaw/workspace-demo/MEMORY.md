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

## 每日自动记忆

每天 23:00 自动执行：
1. 读取当日（00:00 - 23:00）当前 agent 的 session 历史
2. 提取关键内容：做了什么、产出什么、决策了什么
3. 追加写入 `[workspace]/memory/YYYY-MM-DD.md`
4. 格式参考 `memory/2026-03-25.md`

---

## 文件路径约束

### 工作空间（严格限制）
- **允许路径**: `[workspace]/` 及其子目录
  - `[workspace]` = 当前 agent 的 workspace 根目录（运行时注入）
  - 目前即：`/home/hochoy/.openclaw/workspace-demo/`
- **禁止**: 任何在该目录外的文件操作（临时文件 `/tmp/`、`/temp/` 除外）

### 知识库目录
- **路径**: `[workspace]/knowledge/`
- **用途**: 存放知识库相关文件（教程、笔记、文档等）
- **规则**: 以后所有知识库文件统一放此处

---

## 其他记忆
_(随着使用逐步添加)_
