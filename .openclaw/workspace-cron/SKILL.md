## 技能1：全网资讯精准抓取与筛选
1. 每日执行时，使用 Tavily Search API 抓取**近24小时内**全网发布的AI、AI Agent、科技行业相关的最新资讯
2. 调用 Tavily API 进行多维度搜索（使用环境变量 TAVILY_API_KEY）：
   ```bash
   curl -s "https://api.tavily.com/search" \
     -H "Content-Type: application/json" \
     -d '{
       "api_key": "'"$TAVILY_API_KEY"'",
       "query": "AI artificial intelligence latest news today",
       "search_depth": "advanced",
       "include_answer": true,
       "max_results": 10
     }'
   ```
3. 搜索关键词轮换：
   - "AI artificial intelligence latest news today"
   - "AI Agent autonomous agents 2024 2025"
   - "OpenAI Google Gemini Claude latest updates"
   - "科技行业热点 technology breaking news"
   - "AI startup funding investment news"
4. 筛选维度：优先选择行业头部媒体发布、全网热度高、有行业影响力的内容，剔除广告、水文、重复、过时的信息
5. 内容分类固定为4个板块：
   - AI大模型最新动态
   - AI Agent/智能体技术与应用进展
   - 全球科技行业热点
   - 重要产品发布与行业投融资

## 技能2：公众号推文草稿标准化生成
1. 为每日内容生成1个吸引人、符合公众号传播调性的标题，标题需包含当日核心亮点
2. 正文开头配一段简短的导语，概括当日资讯的核心看点
3. 每个资讯条目配「核心事件+简短解读」，语言正式流畅、适合公众号发布，每条内容标注信息来源
4. 全文排版清晰，分段合理，使用公众号兼容的排版格式，无特殊符号，输出的内容可直接复制粘贴到公众号后台草稿箱，无需二次调整
5. 结尾配固定的引导话术：「以上是今日AI科技日报精选内容，关注我们不迷路，明日再见！」

## 技能3：飞书定时推送交付
1. 每日定时任务触发后，完整执行上述资讯抓取、推文生成全流程
2. 生成完成后，将完整的公众号推文草稿，以固定格式推送到飞书群
3. 推送内容开头标注当日日期，标题醒目，正文完整，无多余的执行说明内容
4. 飞书群目标ID: oc_d24f04fe60514d5b59fda960532fa269
