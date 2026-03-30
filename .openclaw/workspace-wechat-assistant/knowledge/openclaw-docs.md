# OpenClaw 官方文档知识库

## 路径约束
- **知识库目录**: `/home/hochoy/.openclaw/workspace-wechat-assistant/knowledge/`

---

## 一、OpenClaw 核心定位

**官网**: https://openclaw.ai
**文档**: https://docs.openclaw.ai
**GitHub**: https://github.com/openclaw/openclaw

OpenClaw 是一个**个人 AI 助手**，运行在你自己的设备上。它在你已经使用的渠道（WhatsApp、Telegram、Slack、Discord 等）上回复你。

> "The Gateway is just the control plane — the product is the assistant."

### 支持的渠道
WhatsApp, Telegram, Slack, Discord, Google Chat, Signal, iMessage, BlueBubbles, IRC, Microsoft Teams, Matrix, Feishu, LINE, Mattermost, Nextcloud Talk, Nostr, Synology Chat, Tlon, Twitch, Zalo, Zalo Personal, WeChat, WebChat

### 支持的平台
- **macOS**: 菜单栏控制、Voice Wake + PTT、Talk Mode overlay、WebChat、调试工具、远程 Gateway 控制
- **iOS**: Canvas、Voice Wake、Talk Mode、相机、屏幕录制、Bonjour + 设备配对
- **Android**: Connect tab、Chat sessions、Voice tab、Canvas、相机/屏幕录制、Android 设备命令（通知/位置/短信/照片/联系人/日历/运动/应用更新）
- **Linux/Windows (WSL2)**: 支持

### 技术要求
- **运行时**: Node 24 (推荐) 或 Node 22.16+
- **安装**: `npm install -g openclaw@latest`

---

## 二、多智能体路由 (Multi-Agent Routing)

### 什么是"一个智能体"？

一个**智能体（Agent）** 是一个完全隔离作用域的"大脑"，拥有自己的：

| 组件 | 说明 |
|------|------|
| **工作区** | 文件、AGENTS.md/SOUL.md/USER.md、本地笔记、人设规则 |
| **状态目录** (`agentDir`) | 认证配置文件、模型注册表、每智能体配置 |
| **会话存储** | 聊天历史 + 路由状态，位于 `~/.openclaw/agents/<agentId>/sessions` |

### 关键路径映射

| 用途 | 路径 |
|------|------|
| 配置 | `~/.openclaw/openclaw.json` (或 `OPENCLAW_CONFIG_PATH`) |
| 状态目录 | `~/.openclaw` (或 `OPENCLAW_STATE_DIR`) |
| 工作区 | `~/.openclaw/workspace` (或 `~/.openclaw/workspace-<agentId>`) |
| 智能体目录 | `~/.openclaw/agents/<agentId>/agent` |
| 会话 | `~/.openclaw/agents/<agentId>/sessions` |
| 认证配置 | `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` |

### 单智能体模式（默认）

- `agentId` 默认为 **`main`**
- 会话键为 `agent:main:<mainKey>`
- 工作区默认为 `~/.openclaw/workspace`

### 多智能体模式

使用多个智能体，每个 `agentId` 成为完全隔离的人格：

- **不同的电话号码/账户**（每渠道 `accountId`）
- **不同的人格**（每智能体工作区文件如 `AGENTS.md` 和 `SOUL.md`）
- **独立的认证 + 会话**（除非明确启用，否则无交叉通信）

### 路由规则（消息如何选择智能体）

绑定是**确定性的**，**最具体的优先**：

1. `peer` 匹配（精确私信/群组/频道 id）
2. `guildId`（Discord）
3. `teamId`（Slack）
4. 渠道的 `accountId` 匹配
5. 渠道级匹配（`accountId: "*"`）
6. 回退到默认智能体

### 核心概念

| 概念 | 说明 |
|------|------|
| `agentId` | 一个"大脑"（工作区、每智能体认证、每智能体会话存储） |
| `accountId` | 一个渠道账户实例（例如 WhatsApp 账户 `"personal"` vs `"biz"`） |
| `binding` | 通过 `(channel, accountId, peer)` 将入站消息路由到 `agentId` |

---

## 三、架构概览

```
WhatsApp / Telegram / Slack / Discord / ... (各渠道)
         │
         ▼
┌───────────────────────────────┐
│         Gateway               │
│     (control plane)          │
│    ws://127.0.0.1:18789      │
└──────────────┬────────────────┘
               │
   ├─ Pi agent (RPC)
   ├─ CLI (openclaw …)
   ├─ WebChat UI
   ├─ macOS app
   └─ iOS / Android nodes
```

- **Gateway**: 本地优先的单控制平面，用于会话、渠道、工具和事件
- **Pi agent runtime**: RPC 模式，支持工具流和块流
- **Session model**: 主会话用于直接聊天，群组隔离，激活模式，队列模式，回复机制

---

## 四、Skills 系统

### 三种 Skills 类型

| 类型 | 位置 | 说明 |
|------|------|------|
| **Bundled** | `~/.openclaw/skills/` | 内置技能 |
| **Managed** | `~/.openclaw/skills/` (通过 ClawHub 管理) | 可从 ClawHub 安装 |
| **Workspace** | `~/.openclaw/workspace/skills/` | 每个智能体独立 |

### ClawHub

ClawHub (https://clawhub.com) 是一个极简技能注册表。启用后，智能体可以自动搜索技能并按需拉取。

---

## 五、沙箱与安全

### 每智能体沙箱配置

从 v2026.1.6 开始，每个智能体可以有自己的沙箱和工具限制：

```json
{
  "agents": {
    "list": [
      {
        "id": "personal",
        "sandbox": { "mode": "off" }  // 无沙箱
      },
      {
        "id": "family",
        "sandbox": {
          "mode": "all",
          "scope": "agent",
          "docker": {
            "setupCommand": "apt-get update && apt-get install -y git curl"
          }
        },
        "tools": {
          "allow": ["read"],
          "deny": ["exec", "write", "edit", "apply_patch"]
        }
      }
    ]
  }
}
```

### 安全说明

- **DM 配对**: 默认 Telegram/WhatsApp/Signal 等渠道对新发送者使用配对码机制
- **公开 DM**: 需要设置 `dmPolicy="open"` 并在 allowlist 中包含 `"*"`
- 工具 `elevated` 是**全局的**且基于发送者，不能按智能体配置

---

## 六、Voice 和 Canvas

### Voice Wake + Talk Mode

- **macOS/iOS**: Wake words + 语音触发转发
- **Android**: 连续语音模式（ElevenLabs + 系统 TTS 后备）

### Live Canvas

- Agent 驱动的可视化工作区
- 支持 A2UI push/reset、eval、snapshot

---

## 七、配置示例

### 两个 WhatsApp → 两个智能体

```json
{
  "agents": {
    "list": [
      { "id": "home", "default": true, "workspace": "~/.openclaw/workspace-home" },
      { "id": "work", "workspace": "~/.openclaw/workspace-work" }
    ]
  },
  "bindings": [
    { "agentId": "home", "match": { "channel": "whatsapp", "accountId": "personal" } },
    { "agentId": "work", "match": { "channel": "whatsapp", "accountId": "biz" } }
  ],
  "channels": {
    "whatsapp": {
      "accounts": {
        "personal": {},
        "biz": {}
      }
    }
  }
}
```

### WhatsApp 日常聊天 + Telegram 深度工作

```json
{
  "agents": {
    "list": [
      { "id": "chat", "model": "anthropic/claude-sonnet-4-5", "workspace": "~/.openclaw/workspace-chat" },
      { "id": "opus", "model": "anthropic/claude-opus-4-5", "workspace": "~/.openclaw/workspace-opus" }
    ]
  },
  "bindings": [
    { "agentId": "chat", "match": { "channel": "whatsapp" } },
    { "agentId": "opus", "match": { "channel": "telegram" } }
  ]
}
```

---

## 八、飞书 (Feishu) 渠道

飞书是支持的渠道之一。配置示例：

```json
{
  "channels": {
    "feishu": {
      // 飞书相关配置
    }
  }
}
```

---

## 九、最近更新 (2026.03.29)

### GitHub Release v2026.3.28 正式版 (2026-03-29) 🆕

> ⚠️ 原 v2026.3.28-beta.1 已转为正式版，标签/标记更新。

**Breaking Changes:**
- **Qwen Provider**: 移除 portal.qwen.ai 废弃的 OAuth 集成，需迁移至 Model Studio（`--auth-choice modelstudio-api-key`）
- **Config/Doctor**: 取消超过两个月的自动配置迁移，旧版配置键将直接报错而非自动重写

**核心新特性:**

1. **xAI 重大升级**: 迁移至 Responses API，新增 `x_search` 一级支持，自动启用 xAI 插件（原有 Grok 配置无需手动）

2. **MiniMax 生图正式上线**: 新增 `image-01` 模型支持文生图和图生图，支持长宽比控制（注：M2.7 以上专用）

3. **插件 Approval 钩子**: `before_tool_call` 钩子支持异步 `requireApproval`，可通过 exec overlay、Telegram 按钮、Discord 交互或各渠道 `/approve` 命令暂停工具执行

4. **ACP Binds 扩展**: Discord、BlueBubbles、iMessage 支持当前对话 ACP binds，可实现 `/acp spawn codex --bind here` 无需创建子线程

5. **apply_patch 默认启用**: OpenAI 和 OpenAI Codex 模型默认开启 apply_patch

6. **CLI Backends 统一化**: Claude CLI、Codex CLI、Gemini CLI 推理迁移至统一插件层，新增 Gemini CLI 后端支持

7. **Slack 文件上传**: 新增显式 `upload-file` action，支持 filename/title/comment 覆盖

8. **跨平台文件发送统一**: Microsoft Teams、Google Chat、BlueBubbles 均通过 `upload-file` 统一暴露

9. **Matrix TTS**: 自动 TTS 回复改为原生 Matrix 语音气泡而非音频附件

10. **Config Schema CLI**: `openclaw config schema` 输出 JSON schema

11. **TTS 配置迁移**: 旧版 speech config 自动迁移（运行时不再回退旧版）

12. **Memory 插件重构**: 内存压缩 flush plan 移至插件合约层

13. **Plugin heartbeat**: 新增 `runHeartbeatOnce` API，插件可触发单次心跳并指定投递目标

14. **Agents/compaction 改进**: 压缩后保留 AGENTS 刷新，改进取消原因展示

15. **Tavily 流量标识**: 请求头新增 `X-Client-Source: openclaw` 便于流量归因

**Model Catalog 变更:**
- MiniMax 精简至仅保留 M2.7，移除 M2/M2.1/M2.5/VL-01

**Bug Fixes:**
- 修复敏感内容导致 Agent 崩溃问题（Anthropic provider）
- 修复 Gemini 3.1 flash-lite 前缀排序问题
- 修复 OpenAI Codex 图像理解工具注册问题
- 修复 WhatsApp 私信自聊天回声循环问题
- 修复 Telegram 文件发送等问题

---

### v2026.03.25 主要新特性

1. **Gateway/OpenAI 兼容性增强**
   - 新增 `/v1/models` 和 `/v1/embeddings` 端点
   - `/v1/chat/completions` 和 `/v1/responses` 支持显式 model override
   - 兼容更广泛的客户端和 RAG 集成

2. **Agents/Tools 改进**
   - `/tools` 现在只显示当前智能体实际可用的工具
   - 新增紧凑默认视图 + 可选详细模式
   - Control UI 新增 "Available Right Now" 实时区域

3. **Microsoft Teams 重大升级**
   - 迁移至官方 Teams SDK
   - 新增 AI-agent UX 最佳实践：流式 1:1 回复、欢迎卡片+提示启动器、反馈/反思、状态更新、输入指示器、原生 AI 标注
   - 支持消息编辑和删除（含 in-thread 回退）

4. **Skills 一键安装**
   - 首批支持一键安装的 bunded skills：`coding-agent`, `gh-issues`, `openai-whisper-api`, `session-logs`, `tmux`, `trello`, `weather`
   - CLI 和 Control UI 可在依赖缺失时自动引导安装

5. **Control UI / Skills 界面重构**
   - 新增状态过滤标签页（All / Ready / Needs Setup / Disabled）+ 计数
   - 点击技能卡片弹出详情对话框，展示 requirements、toggle 开关、安装按钮、API Key 录入、源码信息、主页链接

6. **Slack 改进**
   - 恢复 direct deliveries 丰富回复能力
   - 自动将简单的 `Options:` 行渲染为 buttons/selects
   - 改进 Slack interactive setup 默认值

7. **CLI/Containers**
   - 新增 `--container` 和 `OPENCLAW_CONTAINER` 支持容器内运行 openclaw 命令

---

## 十、常用命令

```bash
# 安装
npm install -g openclaw@latest

# 引导设置
openclaw onboard --install-daemon

# 启动 Gateway
openclaw gateway --port 18789 --verbose

# 发送消息
openclaw message send --to +1234567890 --message "Hello"

# 与助手对话
openclaw agent --message "Ship checklist" --thinking high

# 更新
openclaw update --channel stable|beta|dev

# 健康检查
openclaw doctor
```

---

## 十一、参考资料

- 完整配置参考: https://docs.openclaw.ai/gateway/configuration
- 架构概览: https://docs.openclaw.ai/concepts/architecture
- 安全指南: https://docs.openclaw.ai/gateway/security
- 故障排除: https://docs.openclaw.ai/channels/troubleshooting
