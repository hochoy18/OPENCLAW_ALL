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
_(未来添加)_
