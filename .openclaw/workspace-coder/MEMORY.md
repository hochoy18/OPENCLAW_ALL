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
## 服务器文件路径约束
- **可以读写/tmp/, /temp/** 下的所有文件
- **知识库相关的文件以后都放在/home/hochoy/.openclaw/workspace-coder/knowledge/ 下**

---
## 发送图片规范
- **不要发路径文字**，直接发送图片文件到聊天框
- **发图片正确方式**：先调用 Feishu 上传图片 API 获取 image_key，再发送为 inline image（msg_type=image）
  - 上传：POST https://open.feishu.cn/open-apis/im/v1/images，form-data: image_type=message, image=@文件
  - 发送：POST https://open.feishu.cn/open-apis/im/v1/messages，body: {"receive_id": "群id", "msg_type": "image", "content": "{\"image_key\":\"刚才获取的key\"}"}
- 这是固定规范，必须遵守


## 其他记忆

### 工作范围限制
- **`.openclaw` 目录**：该目录下的任何修改、git/github 相关操作，我都不管、不问、不提交
- 这是一个明确的工作范围边界，避免我浪费精力在不相关的事务上

### 授权与工作目录
1. 授权读写 `/opt/projects` 目录下所有内容
2. 以后创建的项目都放在 `/opt/projects/` 下，每个项目独立目录和 repo
3. 每个项目可以在 GitHub 上创建对应 repo，我可以提交代码

### VoicePix 项目位置
- 项目路径：`/opt/projects/voicepix`

## VoicePix 项目标准开发流程

### 安装的 Skills（位置：workspace-coder/skills/）
- `requirements-analysis` — 需求分析（5W1H/EPIC/MoSCoW）
- `prd-writer-pro` — PRD 文档撰写
- `prd-review` — PRD 审查 + 设计要点梳理
- `code-review-cycle-skill` — 代码 Review 循环（/cr 触发）
- `code-review-assistant` — 安全/质量代码审查
- `e2e-testing-patterns` — Playwright 端到端测试
- `openclaw-api-tester` — API 层验证
- `gitlab-code-review` — GitLab 定时审查

### Pipeline 流程（8 阶段）
需求 → ①需求分析 → ②PRD撰写 → ③PRD评审 → ④开发(/cr) → ⑤安全审查 → ⑥API测试 → ⑦E2E测试 → ⑧部署上线

详细定义：`docs/workflow/pipeline-guide.md`
状态追踪：`docs/workflow/pipeline-state.md`

### VoicePix 最新版本
- 文件：`voicepix.html`（服务端注入 API Key，__MINIMAX_API_KEY__ 占位符）
- 启动：`MINIMAX_API_KEY=xxx node server.js`（监听 8765）
- API 模型：`speech-2.8-hd`（非 speech-02）
- 响应格式：`output_format=hex`，需 hex→binary 解码
- sample_rate：仅支持 32000（不支持 48000）
- Authorization：Bearer `${API_KEY}`（不需要 Group ID）
- 默认英文，默认音色：`English_CalmWoman`

### MiniMax Speech API 关键信息
- 文档：https://platform.minimax.io/docs/guides/speech-t2a-http
- T2A 端点：POST https://api.minimax.io/v1/t2a_v2
- Clone 端点：POST https://api.minimax.io/v1/voice_clone
- 认证：Bearer API_KEY（不需要 Group ID）
- 模型：speech-2.8-hd
- 响应：JSON 内含 hex 音频，需解码
- sample_rate：仅支持 32000
- 可用音色：Chinese (Mandarin)_Warm_Girl, English_expressive_narrator（注意大小写）

