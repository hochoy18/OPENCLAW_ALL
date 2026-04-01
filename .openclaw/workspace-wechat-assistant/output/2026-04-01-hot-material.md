# 热点素材包 | 2026-04-01

> 主题：GitHub AI Agent 项目 · 多Agent协同编程

## 核心项目：oh-my-claudecode

**GitHub**: https://github.com/Yeachan-Heo/oh-my-claudecode
**Stars**: 19k+
**定位**: Teams-first Multi-agent orchestration for Claude Code
**语言**: TypeScript (npm包名: oh-my-claude-sisyphus)

### 核心功能
- **一条指令团队作战**: `/autopilot: build a REST API` 即可自动拆解任务、分配给不同Agent执行
- **团队流水线**: team-plan → team-prd → team-exec → team-verify → team-fix（循环）
- **多Worker并行**: 支持同时运行 N 个 Claude Code / Codex / Gemini 实例
- **Marketplace安装**: `/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claude` 一键安装
- **Socratic访谈**: `/deep-interview` 功能，用苏格拉底式提问澄清需求再执行

### 技术原理
- 基于 Claude Code 内置的 `agent_teams` 实验功能
- 通过 tmux 启动多个独立 Agent 工作区
- 每个 Worker 独立运行，完成后汇总结果

### 适用场景
- 复杂多模块项目（前端+后端+测试+部署）
- 大型代码重构
- 安全审计（多Agent分工检查不同模块）
- PR Review 分工

---

## 辅助参考项目

### hermes-agent (NousResearch)
- Stars: 20k+
- 定位: "The agent that grows with you"，自托管+自我进化
- 支持 MiniMax/Kimi 等国产模型

### CopilotKit
- 定位: 前端Agent框架 + AG-UI协议
- 让React/Angular应用接入AI Agent

---

## 信息来源
- GitHub Topics/ai-agent (https://github.com/topics/ai-agent)
- oh-my-claudecode README (https://github.com/Yeachan-Heo/oh-my-claudecode)
- Hacke News AI/Coding 热门讨论
