#!/bin/bash
# 今日 AI 选题素材搜索脚本

cd /home/hochoy/.openclaw/workspace-wechat-assistant/skills/tavily-search

echo "🔍 正在搜索选题 1: AI 视频生成工具对比..."
python3 scripts/search.py "AI视频生成工具对比 2024 即梦 可灵 Runway 教程" \
  --depth advanced --max-results 5 --verbose > /tmp/topic1_video.txt

echo "🔍 正在搜索选题 2: AI 办公提效工具..."
python3 scripts/search.py "AI办公工具推荐 2024 Kimi 通义千问 效率提升 实测" \
  --depth advanced --max-results 5 --verbose > /tmp/topic2_office.txt

echo "🔍 正在搜索选题 3: AI 副业变现..."
python3 scripts/search.py "AI副业赚钱 2024 普通人 闲鱼 小红书 AI绘画接单" \
  --depth advanced --max-results 5 --verbose > /tmp/topic3_sidejob.txt

echo "🔍 正在搜索选题 4: AI 教育辅导..."
python3 scripts/search.py "AI辅导孩子学习 家长实测 作业帮 AI家教 效果对比" \
  --depth advanced --max-results 5 --verbose > /tmp/topic4_education.txt

echo "🔍 正在搜索选题 5: AI 工具评测..."
python3 scripts/search.py "AI工具评测 2024 ChatGPT Claude 通义千问 对比 避坑" \
  --depth advanced --max-results 5 --verbose > /tmp/topic5_review.txt

echo "✅ 搜索完成！结果保存在 /tmp/topic*.txt"
