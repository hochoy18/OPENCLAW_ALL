# TOOLS.md - Local Notes

## 共享目录（2026-04-01 新增）
- 共享根目录：`/opt/wechat/ai/workspace-wechat-shared/`
- 日期分区：`{{date}}/`（每日独立子目录）
- 目录结构：
  - `hot/` — wechat-hot-collector 输出
  - `topics/` — wechat-content-writer 选题清单（仅本Agent可写）
  - `article/` — 各版本文章草稿及终稿HTML（本Agent可读写）
  - `images/` — AI生成的配图原始文件（本Agent可读写）
  - `audit/` — wechat-quality-auditor 审核报告
  - `push/` — wechat-draft-publisher 推送日志
- docs/：`/opt/wechat/ai/workspace-wechat-shared/docs/`（tech-html-template-1.md、tech-html-acceptance-standards-1.md），**本Agent仅有只读权限**
- topics/ article/ images/：本Agent可读写
- 注意：不得读写其他 Agent 的个人 workspace（`~/.openclaw/workspace-wechat-XXX/`）

## 模型使用
- 文字创作：`kimi-coding/k2p5`
- 图片生成：`image_generate`（MiniMax image-01）

## 图片生成工具 (image_generate) 正确调用规范

### 必填参数
- `prompt`: 图像描述（必填），英文提示词效果更好

### 可选参数
- `model`: "image-01" 或 "image-01-live"（**不要加 "minimax/" 前缀**）
- `aspect_ratio`: "16:9" / "4:3" / "1:1" 等（可选，默认 "1:1"）

### 禁止使用的参数
- `size` - 不是有效参数
- 单独的 `width` 或 `height`（如需自定义尺寸，必须同时设置 width 和 height，且仅用于 image-01）

### 正确示例
```json
{
  "prompt": "A futuristic tech illustration...",
  "model": "image-01",
  "aspect_ratio": "16:9"
}
```

### 错误示例
```json
{
  "prompt": "...",
  "model": "minimax/image-01",
  "size": "1024x1024"
}
```
