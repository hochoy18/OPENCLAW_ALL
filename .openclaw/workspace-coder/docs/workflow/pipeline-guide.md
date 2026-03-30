# VoicePix 开发自动化流程

> 目标：用户说一句需求 → 自动走完 需求分析 → PRD → 开发 → 安全审查 → 测试 → 上线 的完整闭环。

---

## 触发方式

| 用户说 | 触发 |
|--------|------|
| `做需求` / `新功能` / `加个功能` | 启动完整 Pipeline |
| `review 代码` / `审查代码` | 只跑代码审查阶段 |
| `写测试` / `加测试用例` | 只跑测试阶段 |
| `上线` | 只跑部署阶段 |
| `帮我分析这个需求` | 只跑需求分析阶段 |

---

## Pipeline 阶段定义

```
需求提出
   ↓
① 需求分析    ← requirements-analysis
   ↓
② PRD 撰写    ← prd-writer-pro
   ↓
③ PRD 评审    ← prd-review（逻辑闭环 + 设计要点）
   ↓
④ 开发       ← code-review-cycle-skill（A→B 循环）
   ↓
⑤ 安全审查   ← code-review-assistant（--security-only）
   ↓
⑥ API 测试   ← openclaw-api-tester
   ↓
⑦ E2E 测试   ← e2e-testing-patterns
   ↓
⑧ 部署上线   ← Cloudflare Tunnel / pm2
   ↓
⑨ 汇报总结
```

---

## 各阶段职责与产出

### ① 需求分析（requirements-analysis）

**入口**：用户描述一句话需求
**执行**：多轮对话提取（5W1H、用户故事、EPIC 分解）
**产出**：`docs/requirements/{feature}-requirements.md`

**对话问题模板**：
```
1. 这个功能解决什么问题？
2. 谁是用户？（内容创作者/企业/教育/个人）
3. 核心操作流程是什么？
4. 成功指标是什么？
5. 有没有时间节点？
```

---

### ② PRD 撰写（prd-writer-pro）

**入口**：需求分析产出
**执行**：基于分析结果生成完整 PRD
**产出**：`docs/prd/{feature}-prd.md`

**文档结构**：
```
1. 文档信息（版本/日期/状态）
2. 背景与目标
3. 用户场景（用户故事）
4. 功能需求详情（优先级/交互/异常/埋点）
5. 非功能需求（性能/安全/兼容性）
6. 接口说明
7. 风险评估
8. 项目计划
```

---

### ③ PRD 评审（prd-review）

**入口**：PRD 文档
**执行**：逻辑准确性 + 闭环性审查 → 设计要点提取 → 优先级划分
**产出**：`docs/prd/{feature}-prd-review.md`

**审查维度**：
- 逻辑准确性（目标 vs 背景是否匹配）
- 闭环性（异常场景：网络失败/权限/付费）
- 设计要点（界面/交互/视觉/状态）
- 优先级（高/中/低 + 工时预估）

---

### ④ 开发（code-review-cycle-skill）

**入口**：评审通过的 PRD
**执行**：`/cr --rounds 2 <功能描述>` → A 写代码 → B Review → 决策
**产出**：修改后的代码文件

**规则**：
- A 使用 `claude-code`（写代码能力最强）
- B 只读不写，提严重问题/建议/结论
- 每轮结束暂停，等我决策
- 不满意可手动调整

---

### ⑤ 安全审查（code-review-assistant）

**入口**：开发完成的代码
**执行**：`code-review-assistant review {file} --language javascript --security-only`
**产出**：`docs/security/{feature}-review.md`

**审查项**：
- API Key 泄露
- XSS / Injection
- 敏感数据暴露
- CORS 配置
- 输入校验

---

### ⑥ API 测试（openclaw-api-tester）

**入口**：代码中对 API 的调用
**执行**：基于调用记录生成 YAML 测试用例 → 自动执行
**产出**：`api-tests/{feature}-*.yaml` + 测试报告

---

### ⑦ E2E 测试（e2e-testing-patterns）

**入口**：完整功能
**执行**：Playwright 测试框架 → 关键路径测试
**产出**：`e2e/tests/{feature}-*.spec.ts` + HTML 报告

**测试优先级**：
```
P0：核心功能（生成语音/下载）
P1：常见路径（音色切换/格式切换）
P2：边界情况（空文字/超大文件）
P3：异常处理（无 Key/网络错误）
```

---

### ⑧ 部署上线

**入口**：测试通过的代码
**执行**：
1. 备份当前版本
2. 更新 HTML 文件
3. 重启 Node 服务器（环境变量注入 Key）
4. 创建 Cloudflare Tunnel
5. 验证可访问

**产物**：新的公开 URL

---

## 自动化状态追踪

每次 Pipeline 启动时，创建状态文件：`memory/pipeline/{date}-{feature}.json`

```json
{
  "feature": "录音转文字",
  "started": "2026-03-28T08:00:00Z",
  "current_stage": "④开发",
  "stages": {
    "①需求分析": { "status": "done", "output": "docs/requirements/..." },
    "②PRD撰写": { "status": "done", "output": "docs/prd/..." },
    "③PRD评审": { "status": "in_progress", "output": null },
    "④开发": { "status": "pending", "output": null },
    "⑤安全审查": { "status": "pending", "output": null },
    "⑥API测试": { "status": "pending", "output": null },
    "⑦E2E测试": { "status": "pending", "output": null },
    "⑧部署上线": { "status": "pending", "output": null }
  },
  "issues": []
}
```

---

## 命令速查

| 功能 | 命令 |
|------|------|
| 启动完整 Pipeline | `做需求：{描述}` |
| 快速代码审查 | `review {文件}` |
| 快速安全扫描 | `安全审查 {文件}` |
| 生成测试用例 | `写测试 {功能}` |
| API 层验证 | `测 API {接口}` |
| 一键部署 | `上线` |
| 查看 Pipeline 状态 | `pipeline 状态` |
| 跳过某阶段 | `跳过 ⑤` |

---

## 修改日志

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-03-28 | v1.0 | 初始版本 |
