# TOOLS.md - Local Notes

## 共享目录（2026-04-01 新增）
- 共享根目录：`/opt/wechat/ai/workspace-wechat-shared/`
- 日期分区：`{{date}}/`（每日独立子目录）
- 目录结构：
  - `hot/` — wechat-hot-collector 输出（仅本Agent可写）
  - `topics/` — wechat-content-writer 选题清单
  - `article/` — 各版本文章草稿及终稿（HTML）
  - `images/` — AI生成的配图原始文件
  - `audit/` — wechat-quality-auditor 审核报告
  - `push/` — wechat-draft-publisher 推送日志
- 读写权限：hot/ 只允许 hot-collector 写，其他Agent可读
- 注意：不得读写其他 Agent 的个人 workspace（`~/.openclaw/workspace-wechat-XXX/`）
