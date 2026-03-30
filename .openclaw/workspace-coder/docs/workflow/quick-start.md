# VoicePix Pipeline 快速使用指南

## 一句话触发完整流程

```
用户：我想给 VoicePix 加上"录音转文字"功能
```

我自动执行：①需求分析 → ②PRD → ③PRD评审 → ④开发 → ⑤安全审查 → ⑥API测试 → ⑦E2E测试 → ⑧部署上线

---

## 分阶段触发

| 阶段 | 触发词示例 |
|------|-----------|
| ① 需求分析 | "分析这个需求：xxx" |
| ② PRD 撰写 | "写这个功能的 PRD" |
| ③ PRD 评审 | "评审 PRD，提取设计要点" |
| ④ 开发 | "/cr 实现录音转文字" |
| ⑤ 安全审查 | "安全审查 voicepix.html" |
| ⑥ API 测试 | "测试 T2A API" |
| ⑦ E2E 测试 | "写 Playwright 测试" |
| ⑧ 部署上线 | "上线" |

---

## 开发阶段详解

### /cr 命令格式
```
/cr [功能描述]                    # 默认 A=codex, B=claude-code, rounds=0
/cr --rounds 2 [功能描述]          # 自动循环 2 轮
```

### code-review-assistant 命令格式
```
code-review-assistant review <文件路径> --language javascript --security-only
```

### 部署命令
```bash
# 启动服务
MINIMAX_API_KEY=your_key node -e "..." &

# 创建 tunnel
/tmp/cloudflared tunnel --url localhost:8765
```

---

## Skill 速查

| Skill | 核心能力 | 产出文件 |
|-------|---------|---------|
| `requirements-analysis` | 5W1H + EPIC + MoSCoW | `docs/requirements/*.md` |
| `prd-writer-pro` | 完整 PRD 文档 | `docs/prd/*.md` |
| `prd-review` | 逻辑审查 + 设计要点 | `docs/prd/*-review.md` |
| `code-review-cycle-skill` | A→B→决策 循环 | 代码文件更新 |
| `code-review-assistant` | 安全/质量扫描 | `docs/security/*.md` |
| `e2e-testing-patterns` | Playwright 测试 | `e2e/tests/*.spec.ts` |
| `openclaw-api-tester` | API 验证 | `api-tests/*.yaml` |

---

## 重要约束

- **API Key 不写死在代码** — 用 `__MINIMAX_API_KEY__` 占位符
- **所有 API 测试要先跑** — 再上线
- **安全审查是必选项** — 高优先级问题必须修复
- **E2E 测试不依赖 sleep** — 用 waitForSelector
