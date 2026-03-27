# 每日热点公众号 - Prompt 模板
# 由 OpenClaw Cron 触发，Agent 执行完整工作流

## 工作流步骤

你今天要执行"每日热点公众号"工作流：

### Step 1: 热点搜索

使用 tavily-search 搜索今日热点：

**AI 工具方向（70%概率）：**
- "AI tools trending this week"
- "new AI tool release"
- "ChatGPT Claude Gemini comparison"
- "AI productivity tools 2024"

**职场方向（30%概率）：**
- "职场 热议 今天"
- "打工人 热点"
- "职场成长 干货"

### Step 2: 选题

根据搜索结果，选择一个有话题性、有创作空间的选题。

规则：
- AI 方向优先
- 选你能写出独特观点的题目
- 不要选太泛或太窄的

### Step 3: 写作（crayon 风格）

使用 wechat-article-crayon skill 的规范写作：
- 口语化，像和朋友聊天
- 情绪外放，敢下判断
- 禁止"首先/其次/综上所述"
- 开头要有钩子
- 字数 1200-1500
- 标题要有吸引力

### Step 4: 生成封面图

使用 MiniMax image-01 生成封面：
```bash
python3 /home/hochoy/.openclaw/workspace-wechat-assistant/skills/wechat-article-publisher/scripts/generate_cover.py \
  --prompt "文章封面：{标题}。风格：简洁现代、高质量插画、16:9" \
  --provider minimax \
  --aspect-ratio "16:9" \
  --output /tmp/cover.jpg
```

### Step 5: 发布到草稿箱

使用 mp-draft-push 或 wechat-article-publisher 发布：

```bash
cd /home/hochoy/.openclaw/workspace-wechat-assistant/skills/mp-draft-push
set -a
source .env
set +a
source scripts.sh

# 上传封面
TOKEN=$(get_wechat_token)
MEDIA_RESPONSE=$(upload_wechat_image "$TOKEN" "/tmp/cover.jpg")
THUMB_MEDIA_ID=$(echo "$MEDIA_RESPONSE" | jq -r '.media_id')

# 创建草稿
# 需要把文章内容转成 HTML 格式
```

### Step 6: 通知用户

完成后，发送消息通知用户：
- 今天写的什么方向
- 标题是什么
- 已推送到草稿箱，请审稿后发布

---

## 注意事项

1. **实测为主**：写 AI 工具测评时，优先用你自己的体验
2. **积极向上**：职场方向不要负能量
3. **封面必要**：必须生成封面图才能发布
4. **先推草稿箱**：不要直接发布，由用户确认
