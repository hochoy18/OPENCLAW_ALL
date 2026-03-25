# 第二部分：OpenClaw 系统深度解析（2-3周）

> ⭐ **本部分是整个学习体系的核心。** OpenClaw 既是你学习的平台，也是你学习的对象。本部分将深入剖析一个生产级 AI Agent 系统的内部实现。

---

## 2.1 OpenClaw 整体架构

### 1.1 核心设计理念

OpenClaw 是一个**生产级的 AI Agent 编排平台**，不是简单的 Chatbot 框架。它的设计哲学是：

> **简单比复杂更重要，可控比强大更重要。**

与 LangChain（研究框架）、AutoGPT（实验性）不同，OpenClaw 从一开始就是为**生产环境**设计的。

---

### 1.2 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                         Gateway                                │
│  (WebSocket Server, 端口 18789, 单一长连接)                    │
│                                                              │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ Gateway  │  │ Protocol │  │  Hook   │  │   Canvas    │  │
│  │ Daemon   │  │ Validator│  │ System  │  │   Server    │  │
│  └─────────┘  └──────────┘  └──────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
           │                │                │
           ▼                ▼                ▼
    ┌──────────────────────────────────────────────────┐
    │              Provider Connections                  │
    │  WhatsApp │ Telegram │ Discord │ Feishu │ ...    │
    └──────────────────────────────────────────────────┘
           │
           ▼
    ┌──────────────────────────────────────────────────┐
    │                   Agent(s)                      │
    │  ┌────────┐  ┌────────┐  ┌────────┐           │
    │  │ Agent  │  │ Agent  │  │ Agent  │  ...     │
    │  │ (main) │  │ (work) │  │ (code) │           │
    │  └────────┘  └────────┘  └────────┘           │
    │       │           │           │                  │
    │       ▼           ▼           ▼                  │
    │  ┌─────────────────────────────────────────┐    │
    │  │           Skills + Memory +             │    │
    │  │       Session Manager + Model            │    │
    │  └─────────────────────────────────────────┘    │
    └──────────────────────────────────────────────────┘
```

---

### 1.3 核心组件详解

#### Gateway（网关）

**职责**：所有消息的单一入口点

- 维护所有 Provider 连接（WhatsApp、Telegram、Discord、飞书等）
- 暴露 WebSocket API（请求、响应、服务端推送事件）
- 验证入站帧是否符合 JSON Schema
- 发出事件：`agent`、`chat`、`presence`、`health`、`heartbeat`、`cron`

**关键特性**：
- 单主机只有一个 Gateway 实例
- 使用 WebSocket 维持长连接
- 本地连接（loopback）自动批准，远端需要显式配对

#### Agent（智能体）

**职责**：核心推理引擎

每个 Agent 是完全隔离的"大脑"，拥有自己的：
- **Workspace**：工作空间文件（AGENTS.md、SOUL.md、USER.md 等）
- **State Directory**：认证配置、模型注册表
- **Session Store**：聊天历史和路由状态

**Auth Profiles 是每个 Agent 独立的**——主 Agent 的凭证不会自动共享给其他 Agent。

#### Skills（技能系统）

**职责**：Agent 的工具集

- Skill = SKILL.md 定义 + 执行脚本
- 支持**Per-Agent Skills**（每个 Workspace 独立）和**共享 Skills**（全局）
- Skill 执行流程：`SKILL.md` 定义 → Agent 决定调用 → 执行脚本 → 返回结果

#### Memory（记忆系统）

**职责**：长期知识存储

- **两层记忆架构**：短期（Session）+ 长期（Memory 文件）
- 支持**向量搜索**（语义相似度）
- 自动内存刷新（pre-compaction ping）

---

## 2.2 Agent Loop：Agent 如何处理一条消息（核心机制）

> ⭐ **这是整个 OpenClaw 最重要的概念。** Agent Loop 决定了 Agent 如何将一条消息转化为行动和回复。

---

### 2.1 完整生命周期

```
┌─────────────────────────────────────────────────────────────┐
│                      消息接收                                │
│                 Gateway RPC: agent / agent.wait               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ ① Session 解析与队列化                                      │
│    - 验证参数，解析 sessionKey/sessionId                     │
│    - Per-session 队列序列化（防止并发破坏上下文）              │
│    - 可选全局队列                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ ② Workspace + Skills 准备                                   │
│    - 解析并创建 Workspace                                   │
│    - 加载 Skills 快照                                      │
│    - 解析 Bootstrap/上下文文件                              │
│    - 获取 Session 写锁，打开 SessionManager                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ ③ Prompt 构建 + System Prompt 组装                          │
│    - 构建 System Prompt（OpenClaw base + Skills + Bootstrap） │
│    - 模型特定限制和 Compaction 预留 Token                    │
│    - 执行 agent:bootstrap Hook                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ ④ 模型推理（流式输出）                                       │
│    - Thinking 流 → 工具调用 → 最终回复                       │
│    - Assistant deltas 流式发出                              │
│    - 推理过程可选流式输出                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ ⑤ 工具执行                                                 │
│    - before_tool_call Hook                                │
│    - 执行工具，返回结果                                     │
│    - after_tool_call Hook                                │
│    - tool_result_persist Hook                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ ⑥ 回复整形 + 发送                                          │
│    - 组装最终 payload                                      │
│    - 过滤 NO_REPLY                                        │
│    - 重复消息工具去重                                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ ⑦ Compaction + 重试                                        │
│    - 自动 Compaction 发出 compaction 事件                   │
│    - 重试时重置内存缓冲区和工具摘要                         │
└─────────────────────────────────────────────────────────────┘
```

---

### 2.2 队列化与并发控制

**为什么需要队列化？**

```
问题：如果两个请求同时到达同一个 Session
     → 如果不序列化，可能导致上下文顺序混乱
     → 工具执行结果可能写入错误的历史位置
```

**OpenClaw 的解决方案**：

- **Per-Session 队列**：同一 Session 的请求串行执行
- **可选全局队列**：跨 Session 的全局序列化
- 消息渠道可以选择队列模式（collect/steer/followup）

---

### 2.3 Hook 系统（拦截点）

OpenClaw 有**两套 Hook 系统**：

#### A. 内部 Hook（Gateway Hooks）

| Hook 名称 | 触发时机 | 用途 |
|-----------|----------|------|
| `agent:bootstrap` | 构建 Bootstrap 文件时 | 添加/删除 Bootstrap 上下文文件 |
| Command Hooks | `/new`、`/reset`、`/stop` 等命令 | 拦截命令事件 |

#### B. 插件 Hook（Agent + Gateway 生命周期）

| Hook 名称 | 触发时机 | 用途 |
|-----------|----------|------|
| `before_model_resolve` | Session 前（无 messages） | 在模型解析前覆盖 provider/model |
| `before_prompt_build` | Session 加载后（有 messages） | 注入 prependContext 或修改 systemPrompt |
| `before_agent_start` | Agent 启动前 | 兼容性 Hook |
| `agent_end` | 完成 后 | 检查最终消息列表和运行元数据 |
| `before_compaction` | Compaction 前 | 观察或注解 Compaction 周期 |
| `after_compaction` | Compaction 后 | 观察或注解 Compaction 周期 |
| `before_tool_call` | 工具调用 前 | 拦截工具参数 |
| `after_tool_call` | 工具调用 后 | 拦截工具结果 |
| `tool_result_persist` | 工具结果持久化时 | 同步转换工具结果 |
| `message_received` | 消息接收时 | 入站消息 Hook |
| `message_sending` | 消息发送前 | 出站消息 Hook |
| `message_sent` | 消息发送后 | 出站消息 Hook |
| `session_start` | Session 启动时 | Session 生命周期边界 |
| `session_end` | Session 结束时 | Session 生命周期边界 |
| `gateway_start` | Gateway 启动时 | Gateway 生命周期事件 |
| `gateway_stop` | Gateway 停止时 | Gateway 生命周期事件 |

---

## 2.3 Workspace 与安全模型

### 3.1 Workspace 架构

```
~/.openclaw/
├── workspace-main/          # Agent "main" 的工作空间
│   ├── AGENTS.md          # Agent 行为定义
│   ├── SOUL.md            # Agent 人格定义
│   ├── USER.md            # 用户信息
│   ├── TOOLS.md           # 工具配置
│   ├── IDENTITY.md        # Agent 身份
│   ├── HEARTBEAT.md       # 心跳配置
│   ├── MEMORY.md          # 长期记忆
│   └── memory/            # 每日日志
│       └── YYYY-MM-DD.md
├── workspace-work/         # Agent "work" 的工作空间（隔离）
│   └── ...
├── agents/                # Agent 状态目录
│   ├── main/
│   │   ├── agent/         # Agent 配置
│   │   └── sessions/     # Session 历史
│   └── work/
└── skills/               # 共享 Skills（全局）
```

**关键点**：
- Workspace 是默认的**工作目录**，不是硬沙箱
- 每个 Agent 的 Workspace 完全隔离
- 相对路径在 Workspace 内解析，但绝对路径可以到达其他位置

---

### 3.2 安全模型

#### Sandbox 模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `off` | 无沙箱 | 信任的 Agent |
| `read-only` | 只读文件系统 | 只读任务 |
| `all` | 完全沙箱 | 不信任的 Agent |

#### Tool Policy

```json
{
  "tools": {
    "allow": ["exec", "read", "sessions_list"],
    "deny": ["write", "edit", "browser", "canvas"]
  }
}
```

- **allow list**：只有列出的工具可用
- **deny list**：列出的工具不可用
- 默认为空（所有工具可用）

#### Per-Agent 沙箱（v2026.1.6+）

```json
{
  "agents": {
    "list": [
      {
        "id": "personal",
        "sandbox": { "mode": "off" }
      },
      {
        "id": "family",
        "sandbox": { "mode": "all", "scope": "agent" },
        "tools": {
          "allow": ["read"],
          "deny": ["exec", "write", "edit"]
        }
      }
    ]
  }
}
```

---

## 2.4 Memory 系统深度解析

### 4.1 两层记忆架构

```
短期记忆（Session）
    │
    │ 自动压缩（Compaction）
    ▼
长期记忆（Memory 文件）
    │
    │ 语义搜索（memory_search）
    ▼
向量数据库（可选）
```

---

### 4.2 记忆文件组织

#### Daily Log（每日日志）

```markdown
# memory/2026-03-25.md

## 今日工作
- 研究了 OpenClaw Agent Loop 机制
- 理解了 Hook 系统的工作原理

## 待办
- [ ] 继续研究 Memory 向量搜索
- [ ] 实践 Skill 编写
```

**规则**：
- 自动读取今天 + 昨天的日志
- Session 启动时加载
- 可通过 `memory_get` 手动访问

#### MEMORY.md（长期记忆）

**规则**：
- **仅在主会话（私人 DM）加载**
- **永远不在群聊中加载**
- 用于：重要决策、用户偏好、长期目标

**写入时机**：
- 重要决策时
- 用户明确说"记住这个"时
- 每周回顾时

---

### 4.3 向量搜索原理

#### 工作流程

```
Markdown 文件
      │
      ▼ 分块（~400 tokens，80 token 重叠）
向量块
      │
      ▼ 向量化（Embedding Model）
SQLite 向量库（~/.openclaw/memory/<agentId>.sqlite）
      │
      │ 用户查询
      ▼
查询向量化 → 余弦相似度搜索 → 返回最相关片段
```

#### 支持的 Embedding 提供者

| 提供者 | 配置键 | 说明 |
|--------|--------|------|
| OpenAI | `openai` | text-embedding-3-small |
| Gemini | `gemini` | gemini-embedding-001 / 2-preview |
| Voyage | `voyage` | voyage-3 |
| Mistral | `mistral` | mistral-embed |
| Ollama | `ollama` | 本地模型 |
| Local | `local` | node-llama-cpp + GGUF |

#### 高级特性

**1. Hybrid Search（混合搜索）**

```json
{
  "memorySearch": {
    "query": {
      "hybrid": {
        "enabled": true,
        "vectorWeight": 0.7,
        "textWeight": 0.3
      }
    }
  }
}
```

- **向量搜索**：语义相似（"Mac Studio" ≈ "运行 gateway 的机器"）
- **BM25 搜索**：精确关键词（ID、代码符号、错误字符串）

**2. MMR Reranking（多样性重排）**

解决：搜索"家庭网络设置"返回 5 个几乎相同的路由器配置片段。

```json
{
  "query": {
    "hybrid": {
      "mmr": {
        "enabled": true,
        "lambda": 0.7
      }
    }
  }
}
```

- `lambda = 1.0`：纯相关性
- `lambda = 0.0`：最大多样性
- 默认 `0.7`（平衡）

**3. Temporal Decay（时间衰减）**

解决：6 个月前的笔记可能比昨天的更新排名更高。

```json
{
  "query": {
    "hybrid": {
      "temporalDecay": {
        "enabled": true,
        "halfLifeDays": 30
      }
    }
  }
}
```

| 时间 | 得分保留 |
|------|----------|
| 今天 | 100% |
| 7 天前 | 84% |
| 30 天前 | 50% |
| 90 天前 | 12.5% |

**MEMORY.md 和非日期文件不受衰减影响**——它们是永久参考信息。

---

### 4.4 自动内存刷新（Pre-compaction Ping）

当 Session 接近自动压缩时：

```
Session 接近 Compaction
      │
      ▼
触发 Silent Agent Turn
      │
      ▼
提醒模型写入持久记忆
      │
      ▼
回复 NO_REPLY（用户看不到）
```

**配置**：

```json
{
  "compaction": {
    "reserveTokensFloor": 20000,
    "memoryFlush": {
      "enabled": true,
      "softThresholdTokens": 4000,
      "systemPrompt": "Session 即将压缩，请存储持久记忆。",
      "prompt": "如有必要，写入 memory/YYYY-MM-DD.md。无需回复请用 NO_REPLY。"
    }
  }
}
```

---

## 2.5 Skills 系统：Agent 的工具箱

### 5.1 Skill 结构

```
~/.openclaw/skills/weather/
├── SKILL.md        # Skill 定义（必须）
└── script.py       # 执行脚本（可选）
```

**SKILL.md 格式**：

```markdown
# SKILL.md

## 描述
获取指定城市的天气预报。

## 触发词
"天气"、"weather"、"预报"

## 参数
- city: 城市名称（必填）

## 返回
JSON 格式的天气信息
```

---

### 5.2 Skill 查找顺序

```
Agent 需要工具
      │
      ▼
搜索 Per-Agent Skills（workspace/skills/）
      │
      ▼ 未找到
搜索全局 Skills（~/.openclaw/skills/）
      │
      ▼ 未找到
搜索内置 Skills（bundled）
```

---

### 5.3 内置 Skills

| Skill | 功能 |
|-------|------|
| `weather` | 获取天气预报 |
| `coding-agent` | Codex 集成 |
| `feishu-doc` | 飞书文档操作 |
| `clawhub` | 技能市场 |

---

## 2.6 多 Agent 路由与绑定系统

### 6.1 绑定规则（Bindings）

**路由优先级（从上到下，匹配即停止）**：

1. `peer` 匹配（精确 DM/群组/频道 ID）
2. `parentPeer` 匹配（线程继承）
3. `guildId + roles`（Discord 角色路由）
4. `guildId`（Discord）
5. `teamId`（Slack）
6. `accountId` 匹配（频道账号）
7. channel 级匹配（`accountId: "*"`）
8. 回退到默认 Agent

---

### 6.2 Session Key 构成

```
agent:<agentId>:<channel>:<peer>
        │         │        │
        │         │        └── 对方标识（DM ID / 群组 ID / 频道 ID）
        │         │
        │         └── 渠道类型（whatsapp / telegram / discord / feishu）
        │
        └── Agent ID（main / work / coding 等）
```

**示例**：
- `agent:main:feishu:ou_123456` → 主 Agent 的某个飞书用户 DM
- `agent:coding:discord:guild_789:channel_456` → Coding Agent 的某个 Discord 频道

---

### 6.3 多账号支持

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "personal": { "appId": "...", "appSecret": "..." },
        "work": { "appId": "...", "appSecret": "..." }
      }
    }
  },
  "bindings": [
    { "agentId": "main", "match": { "channel": "feishu", "accountId": "personal" } },
    { "agentId": "work", "match": { "channel": "feishu", "accountId": "work" } }
  ]
}
```

---

## 2.7 配置体系

### 7.1 核心配置文件

**位置**：`~/.openclaw/openclaw.json`

**主要配置项**：

```json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback"
  },
  "agents": {
    "defaults": {
      "workspace": "~/.openclaw/workspace",
      "timeoutSeconds": 600,
      "compaction": { ... },
      "memorySearch": { ... }
    },
    "list": [
      {
        "id": "main",
        "default": true,
        "model": "minimax/MiniMax-M2.7"
      }
    ]
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "accounts": { ... }
    }
  },
  "bindings": [ ... ]
}
```

---

### 7.2 Auth Profiles

每个 Agent 有独立的认证配置：

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

主 Agent 的凭证**不会**自动共享给其他 Agent。

---

## 2.8 System Prompt 解析

### 8.1 Prompt 组装顺序

```
OpenClaw Base Prompt
      │
      ▼ + Skills 提示词
Skills 列表（Name + Description + Location）
      │
      ▼ + Bootstrap Context
AGENTS.md + SOUL.md + USER.md + TOOLS.md + IDENTITY.md + HEARTBEAT.md
      │
      ▼ + Runtime Info
Host / OS / Node / Model / Thinking Level
      │
      ▼ + Channel Context
Reply Tags / Heartbeat Config / ...
```

---

### 8.2 Bootstrap 文件注入规则

| 文件 | 注入位置 | 说明 |
|------|----------|------|
| `AGENTS.md` | Project Context | Agent 行为定义 |
| `SOUL.md` | Project Context | Agent 人格 |
| `USER.md` | Project Context | 用户信息 |
| `TOOLS.md` | Project Context | 工具配置 |
| `IDENTITY.md` | Project Context | Agent 身份 |
| `HEARTBEAT.md` | Heartbeat Config | 心跳配置 |
| `MEMORY.md` | 仅主会话 | 长期记忆 |

**Sub-Agent 只注入 `AGENTS.md` 和 `TOOLS.md`**。

---

### 8.3 Prompt 模式

| 模式 | 用途 | 包含内容 |
|------|------|----------|
| `full` | 默认 | 所有 sections |
| `minimal` | Sub-Agent | Tooling + Safety + Workspace + Sandbox + Runtime |
| `none` | 极简 | 仅 base identity |

---

## 2.9 实践练习

### 练习 1：绘制你的 OpenClaw 架构图

查看你的 `openclaw.json`，绘制：
- 有多少个 Agent？
- 每个 Agent 的 Workspace 在哪里？
- 有多少个 Channel 账号？
- 绑定规则是什么？

### 练习 2：追踪一条消息的生命周期

1. 发送一条消息到飞书
2. 观察 Gateway 日志
3. 追踪消息如何路由到正确的 Agent
4. 观察 Session 如何加载
5. 观察 Prompt 如何构建
6. 观察工具如何调用

### 练习 3：配置第二个 Agent

```bash
openclaw agents add coding
```

创建后配置绑定规则，将特定频道路由到新 Agent。

### 练习 4：理解 Compaction

1. 进行一个长对话（50+ 轮）
2. 观察 `/status` 中的 Compaction 计数
3. 手动触发 Compaction：`/compact`
4. 查看 Session JSONL 文件，理解压缩如何工作

---

## 2.10 关键概念速查表

| 概念 | 说明 | 配置位置 |
|------|------|----------|
| **Agent Loop** | 消息 → 推理 → 工具 → 回复的完整生命周期 | 核心机制 |
| **Queueing** | Per-Session 请求序列化 | `agents.defaults` |
| **Compaction** | 压缩历史消息，保留摘要 | `compaction.*` |
| **Hook** | 生命周期拦截点 | `plugins.hooks` |
| **Workspace** | Agent 工作空间（文件） | `agents.list[].workspace` |
| **Sandbox** | 文件系统隔离 | `agents.list[].sandbox` |
| **Tool Policy** | 工具黑白名单 | `agents.list[].tools` |
| **Memory** | 两层记忆（Session + File） | `memory.*` |
| **Hybrid Search** | 向量 + BM25 混合搜索 | `memorySearch.query.hybrid` |
| **MMR** | 多样性重排 | `memorySearch.query.hybrid.mmr` |
| **Temporal Decay** | 时间衰减 | `memorySearch.query.hybrid.temporalDecay` |
| **Binding** | 消息路由规则 | `bindings[]` |
| **Auth Profiles** | Per-Agent 认证 | `agents/<agentId>/agent/` |

---

## 学习资源

- OpenClaw 官方文档：`/usr/local/lib/node_modules/openclaw/docs/`
- Gateway Protocol：`docs/gateway/protocol.md`
- 配置参考：`docs/reference/configuration.md`

---

*本部分由 OpenClaw AI Assistant 整理 | 2026-03-25*
