# 定时任务配置
## 任务标识
- 任务名称：wechat-daily
- 所属Agent：wechat-assistant
- 目标群：oc_eca0989d92d6638ff952496754eee106

## 触发规则
- 触发类型：Cron定时触发
- Cron表达式：`0 20 * * *`（每日北京时间 4:00 = UTC 前一天 20:00）
- 执行周期：每日一次，无节假日限制

## 触发后执行指令
请立即执行微信公众号每日热点文章生产任务，严格按照以下流程完成：

1. 调度 wechat-hot-collector 抓取今日TOP 7 AI领域热点
2. 从TOP 7中自动选取TOP 3，选取标准：热度优先 + 领域多样性 + 公众号受众适配
3. 按以下风格同时创作3篇文章：
   - 热度第1名 → default.css（默认风格）
   - 热度第2名 → dark.css（深色风格）
   - 热度第3名 → apple.css（苹果风格）
4. 3篇文章同时进入 wechat-quality-auditor 审核
5. 审核通过后，3篇文章同时推送到微信公众号草稿箱
6. 推送完成后，在群里汇报：3篇草稿的标题、ID、草稿箱链接

## 共享目录路径
- 热点存储：`/opt/wechat/ai/workspace-wechat-shared/{date}/hot/`
- 文章存储：`/opt/wechat/ai/workspace-wechat-shared/{date}/article/`
- 配图存储：`/opt/wechat/ai/workspace-wechat-shared/{date}/images/`
- 审核报告：`/opt/wechat/ai/workspace-wechat-shared/{date}/audit/`
- 推送日志：`/opt/wechat/ai/workspace-wechat-shared/{date}/push/`

## 时间要求
- 开始时间：4:00 北京时间
- 最晚完成：7:00 北京时间之前
- 预估总耗时：30-50分钟

## 异常通知
- 任意单篇失败：完成其他2篇后通知主理人
- 全部失败：立即通知主理人，说明原因
