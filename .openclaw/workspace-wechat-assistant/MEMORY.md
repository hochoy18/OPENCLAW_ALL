# MEMORY.md | wechat-assistant 主Agent专属记忆文件
version: 3.0 | last_updated: 2026-04-01
> 本文档是主Agent的专属记忆，持续沉淀全流程执行经验、主理人偏好、流程优化记录，每次会话自动加载。

---

## 一、主理人核心偏好（固定不变）

- **选题偏好**：AI Agent落地、海外大模型更新、开源AI项目类主题
- **内容偏好**：侧重实操干货、技术解读，拒绝纯行业八卦、无营养水文
- **操作习惯**：每天早上确认选题，下午审核，晚上确认推送
- **禁用内容**：网络热梗、焦虑式营销、未经证实的传闻

---

## 二、发稿标准文档（强制使用，每次必读）

| 文档 | 路径 | 用途 |
|------|------|------|
| **HTML模板** | `/opt/wechat/ai/workspace-wechat-shared/docs/tech-html-template-1.md` | 写文章时必须完整套用此模板结构 |
| **验收标准** | `/opt/wechat/ai/workspace-wechat-shared/docs/tech-html-acceptance-standards-1.md` | 审核时必须逐阶段对照检查 |

**警告**：tech-html-template-1.md的模板结构必须完整遵守，不得擅自删减章节或改变模块格式。

---

## 三、我自己的严重问题（永久禁止再犯）

**今日核心教训（2026-04-01，全天累积）：**

1. **"派发了"≠"完成了"** — 最大问题。派发任务后必须通读全文、验证格式，才能进入下一步。
2. **校验走形式** — 只检查"文件存在"，没检查内容质量、排版格式、配图可用性。
3. **审核形同虚设** — 审核打了9.1分但文章格式完全不能用。
4. **输出Markdown而非HTML** — 微信公众号不解析Markdown，这是一个低级错误。
5. **配图链接用外部失效链接** — 必须上传微信CDN获取永久链接。
6. **字数超标** — 标准要求600-800字，我写了1250字。
7. **配图全部堆在文末** — 必须均匀分布在开头/中间/结尾。
8. **代码块用了blockquote** — 模板要求是 `Plain Text` 代码块。
9. **报喜不报忧** — 问题出现先解释，不先承认。
10. **第一次催促才认真做** — 主理人多次强调"认真点"才执行到位。

**永久整改承诺：**
- 每步必须通读全文，预览HTML效果
- 严格对照 tech-html-acceptance-standards-1.md 逐阶段检查
- 配图必须上传微信CDN才能嵌入HTML
- 发现问题第一时间承认，不解释
- 主理人说一遍就认真做，不要等反复催促

11. **workspace 混入业务文件**：2026-04-01 发现 output/ 目录内存放22个业务文件（文章HTML、推送日志、审核报告、热点素材等），严重违规。正确路径应在 /opt/wechat/ai/workspace-wechat-shared/{date}/ 的对应子目录。output/ 目录已删除，并确保 SOUL.md 禁止条款已生效。

---

## 四、全流程执行记录

| 日期 | 主题 | 推送状态 | 问题记录 |
|------|------|---------|---------|
| 2026-04-01 AM | Claude Code源码泄露 | 推送成功（v2） | ①~⑩全部问题都犯了，被主理人严重批评 |
| 2026-04-01 PM | oh-my-claudecode团队协作 | 推送成功（v4） | 无，全流程严格按标准执行，14项核查全部通过 |

---

## 五、经验沉淀

### 技术要点（固定规则）
- **sessions_spawn 工具不可用**，无法启动新subagent；关键步骤我自己执行
- **token有效期2小时**，每次推送需重新获取
- **配图上传流程**：生成图片 → 查文件路径 → 上传CDN → 替换HTML占位符 → 推送
- **文章输出路径**：`/opt/wechat/ai/workspace-wechat-shared/{date}/article/{date}-article-v{N}.html`
- **推送日志路径**：`/opt/wechat/ai/workspace-wechat-shared/{date}/push/{date}-push-log.md`
- **搜索工具**：使用 Tavily（`skills/tavily-search/scripts/search.py`），不使用 web_search（Brave API Key 不需要配置）

### 共享目录机制（2026-04-01 新增）
- 共享根目录：`/opt/wechat/ai/workspace-wechat-shared/`
- 所有 5 个 Agent 均直接读写共享目录，无须 cp
- SOUL.md 中各自限定了可读写的子目录范围
- 日期分区：每个日期一个独立目录，结构为 {date}/{hot,topics,article,images,audit,push}
- 目录权限：hot/=hot-collector写, topics/=content-writer写, article/=共写, images/=共写, audit/=quality-auditor写, push/=draft-publisher写

### 文章结构规则（tech-html-template-1.md）
```
标题（14-26字）
作者 | 来源
导语（1-2段，每段≤3行）
  ↓
一、二级标题
  1. 三级标题
    正文（每段≤120字，≤3行）
    pre代码块（ Plain Text格式，不是blockquote）
    图片（mmbiz.qpic.cn永久链接）
    引用块/列表
  ↓
二、二级标题（可有表格）
三、总结 + 引导语 + 版权footer
```

### 验收标准（tech-html-acceptance-standards-1.md）
必须逐阶段核查，5个阶段全部通过才能推送：
- 阶段1：热点采集（信息可溯源、无事实错误、无违规）
- 阶段2：选题（贴合热点、结构清晰、有实用性）
- 阶段3：写文（字数≥800、结构完整、命令准确、无错别字）
- 阶段4：审核（0错别字、0事实错误、0合规风险、配图CDN、代码块格式正确）
- 阶段5：发布（草稿创建成功）

---

## 六、子Agent运行状态记录

| Agent名称 | 运行状态 | 最近一次执行时间 | 异常记录 | 优化建议 |
|-----------|----------|------------------|----------|----------|
| wechat-hot-collector | 待观察 | 2026-04-01 | workspace路径混用 | 需主理人协助修复 |
| wechat-content-writer | 待观察 | 2026-04-01 | workspace隔离导致无法正常调用 | 需主理人协助修复 |
| wechat-quality-auditor | 待观察 | 2026-04-01 | 审核形同虚设（我的问题） | 需主理人协助修复 |
| wechat-draft-publisher | 待观察 | 2026-04-01 | 同上 | 需主理人协助修复 |

---

## 七、全局异常处理经验库

| 异常类型 | 出现场景 | 解决方案 | 状态 |
|----------|----------|----------|------|
| 热点抓取失败 | 海外源访问超时 | 切换备用国内源重试 | 已解决 |
| sessions_spawn不可用 | 需要启动新subagent时 | 关键步骤我自己执行 | 已解决 |
| 配图链接失效 | 使用外部链接 | 必须上传微信CDN | 已解决 |
| Markdown格式推文 | 输出纯Markdown | 必须输出HTML+内联样式 | 已解决 |
