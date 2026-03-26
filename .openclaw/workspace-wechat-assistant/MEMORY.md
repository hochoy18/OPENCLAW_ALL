# MEMORY.md - Long-Term Memory

## Aliyun Image Generation

- **API Key:** `sk-ff15c72de8f1487088912988a97e13c7`
- **Default Model:** `qwen-image-2.0`

### Skill: aliyun-image-gen

使用此技能时默认使用以上配置。可通过环境变量 `ALIYUN_IMAGE_API_KEY` 覆盖。

## 工作空间约束

**硬性约束，必须永远遵守：**

- **工作空间:** 只能在 `workspace-wechat-assistant` 目录下工作
- **Agent:** 只能使用 `wechat-assistant` agent
- **行为:** 如果任何操作超出上述范围，必须直接报错返回，拒绝执行

> ⚠️ 这是一条红线规则。无论任何请求，都必须先检查是否在允许的范围内。如果不在，立即报错，不要执行。

## 每日自动记忆

每天 23:00 自动执行：
1. 读取当日（00:00 - 23:00）当前 agent 的 session 历史
2. 提取关键内容：做了什么、产出什么、决策了什么
3. 追加写入 `[workspace]/memory/YYYY-MM-DD.md`
4. 格式参考 `memory/2026-03-25.md`


---
## 服务器文件路径约束
- **可以读写/tmp/, /temp/** 下的所有文件
- **知识库相关的文件以后都放在/home/hochoy/.openclaw/workspace-wechat-assistant/knowledge/ 下**

---
## 发送图片规范
- **不要发路径文字**，直接发送图片文件到聊天框
- **发图片正确方式**：先调用 Feishu 上传图片 API 获取 image_key，再发送为 inline image（msg_type=image）
  - 上传：POST https://open.feishu.cn/open-apis/im/v1/images，form-data: image_type=message, image=@文件
  - 发送：POST https://open.feishu.cn/open-apis/im/v1/messages，body: {"receive_id": "群id", "msg_type": "image", "content": "{\"image_key\":\"刚才获取的key\"}"}
- 这是固定规范，必须遵守
