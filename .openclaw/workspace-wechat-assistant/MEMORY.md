# MEMORY.md - Long-Term Memory

## 用户信息

- **用户:** 霍去病 (ou_7f442bef1a102e6c203ad4e2d1a86e69)
- **时区:** Asia/Shanghai

---

## 核心定位 🚀

**主要工作：自媒体公众号（订阅号）全栈运营**

包括：
- 公众号文章创作（选题、标题、正文、润色）
- 文章发布（草稿箱、正式发布）
- 配图生成（封面图、正文配图）
- 内容改写（去AI味、口语化）
- 文章提取与转载
- 素材管理
- 后续可能扩展：其他自媒体平台

---

## 微信公众号配置 ✅ 已确认

- **AppID:** `wx7ce09b0230364ce1`
- **AppSecret:** `659fb396a1362ab79454c3a576e9db60`
- **认证状态:** 已认证订阅号 ✅
- **IP白名单:** 已设置 ✅
- **接口权限:** 已启用 ✅

---

## 图片生成配置

### MiniMax (当前默认)
- **API Key:** `sk-cp-dEJDwSZI46V_ys9hSxmyH3MT3kjnYJAkMGQK6fz38Imta8l5FmHU9stkSc8lqrT_xpeglsSQypkntDpu0xuJAYVxmkx_cpo3wEHseh_5pCi_HX_qX9X66-Y`
- **Base URL:** `https://api.minimax.io/v1/image_generation`
- **模型:** `image-01`
- **支持的宽高比:** `1:1`, `16:9`, `4:3`, `3:2`, `2:3`, `3:4`, `9:16`

### 阿里云通义万相 (备用)
- **API Key:** `sk-ff15c72de8f1487088912988a97e13c7`
- **Base URL:** `https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
- **模型:** `qwen-image-2.0`

---

## 搜索配置

### Tavily Search
- **API Key:** `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`

---

## Skill 配置位置

所有微信公众号相关 Skill 配置都在：
`/home/hochoy/.openclaw/workspace-wechat-assistant/skills/`

### 各 Skill 的 .env 位置

| Skill | 用途 | .env 路径 |
|-------|------|-----------|
| wechat-article-publisher | 公众号大全套 | skills/wechat-article-publisher/.env |
| wechat-article-writer | 公众号写作 | skills/wechat-article-writer/.env |
| wechat-multi-publisher | Markdown发布 | skills/wechat-multi-publisher/.env |
| mp-draft-push | 纯发布工具 | skills/mp-draft-push/.env |
| tavily-search | 网络搜索 | skills/tavily-search/.env |

### generate_cover.py 已支持 MiniMax

已修改 `wechat-article-publisher/scripts/generate_cover.py`，添加 MiniMax provider：
```bash
# 默认使用 MiniMax
python3 generate_cover.py --prompt "封面描述"

# 指定 provider
python3 generate_cover.py --prompt "封面描述" --provider minimax
python3 generate_cover.py --prompt "封面描述" --provider qwen
```

---

## 工作空间约束

**硬性约束，必须永远遵守：**

- **工作空间:** 只能在 `workspace-wechat-assistant` 目录下工作
- **Agent:** 只能使用 `wechat-assistant` agent
- **行为:** 如果任何操作超出上述范围，必须直接报错返回，拒绝执行

> ⚠️ 这是一条红线规则。无论任何请求，都必须先检查是否在允许的范围内。如果不在，立即报错，不要执行。

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
- **知识库相关的文件以后都放在/home/hochoy/.openclaw/workspace-wechat-assistant/knowledge/ 下**

---

## 发送图片规范

- **不要发路径文字**，直接发送图片文件到聊天框
- **发图片正确方式**：先调用 Feishu 上传图片 API 获取 image_key，再发送为 inline image（msg_type=image）
  - 上传：POST https://open.feishu.cn/open-apis/im/v1/images，form-data: image_type=message, image=@文件
  - 发送：POST https://open.feishu.cn/open-apis/im/v1/messages，body: {"receive_id": "用户open_id", "msg_type": "image", "content": "{\"image_key\":\"刚才获取的key\"}"}
- 这是固定规范，必须遵守

---

## 已安装的 Skills 列表

```
workspace-wechat-assistant/skills/
├── aliyun-image-gen          # 阿里云通义万相生图
├── find-skills-skill         # 搜索安装新 Skill
├── mp-draft-push            # 纯发布到草稿箱
├── tavily-search             # Tavily 搜索
├── wechat-article-crayon     # 公众号写作风格优化
├── wechat-article-publisher  # 公众号大全套
├── wechat-article-writer     # 公众号写作流程
├── wechat-mp-writer-skill-mxx # AI去味润色
└── wechat-multi-publisher   # Markdown批量发布
```

---

## OpenClaw 文档知识库

已学习并保存在 `knowledge/openclaw-docs.md`：
- OpenClaw 核心定位
- 多智能体路由架构
- Skills 系统
- 沙箱与安全
- 飞书渠道配置
