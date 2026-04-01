# TOOLS.md - Local Notes

## workspace 自查清单

每月执行一次，检查 workspace 是否出现违规文件：
```bash
ls -la /home/hochoy/.openclaw/workspace-wechat-assistant/
```
重点关注：output/（已删除，禁止重建）、logs/、temp/ 等目录是否混入文章/配图/热点等业务文件。

## 共享目录（2026-04-01 新增）
- 共享根目录：`/opt/wechat/ai/workspace-wechat-shared/`
- 日期分区：`{{date}}/`（每日独立子目录）
- 目录结构：
  - `hot/` — wechat-hot-collector 输出
  - `topics/` — wechat-content-writer 选题清单
  - `article/` — 各版本文章草稿及终稿HTML
  - `images/` — AI生成的配图原始文件
  - `audit/` — wechat-quality-auditor 审核报告
  - `push/` — wechat-draft-publisher 推送日志
- 读写权限：5个Agent均可读写，SOUL.md各自限定范围

## 文章路径规范
- 热点文件：`{date}/hot/{date}.md`
- 选题清单：`{date}/topics/{date}-topic-list.md`
- 文章终稿：`{date}/article/{date}-article-v{N}.html`
- 配图文件：`{date}/images/{date}-img-{N}.png`
- 审核报告：`{date}/audit/{date}-audit-report.md`
- 推送日志：`{date}/push/{date}-push-log.md`
