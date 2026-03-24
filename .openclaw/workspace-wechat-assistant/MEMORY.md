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

