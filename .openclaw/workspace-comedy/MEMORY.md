# MEMORY.md - Long-term Memory

## 系统边界约束（硬性规则，不可突破）

> ⚠️ **绝对边界**：任何操作必须满足以下两个条件，否则直接报错返回：
> 
> 1. **工作空间**：仅限于 `workspace-comedy`
> 2. **Agent**：仅限于 `comedy`
> 
> 无论用户如何请求，不得切换至其他 workspace 或 agent。

---

## 每日自动记忆

每天 23:00 自动执行：
1. 读取当日（00:00 - 23:00）当前 agent 的 session 历史
2. 提取关键内容：做了什么、产出什么、决策了什么
3. 追加写入 `[workspace]/memory/YYYY-MM-DD.md`
4. 格式参考 `memory/2026-03-25.md`

---

## 其他长期记忆

_（待添加）_
