#!/bin/bash
# 微信公众号文章发布完整流程

cd /home/hochoy/.openclaw/workspace-wechat-assistant/skills/wechat-article-publisher/scripts

# 1. 生成封面图片
echo "🎨 生成封面图片..."
cover_result=$(python3 generate_cover.py --prompt "未来科技办公室，AI智能助手与人类协作，蓝色科技风格，现代简洁设计，工作效率提升概念，16:9横屏构图" --provider qwen --output /tmp/cover_ai_productivity.jpg 2>&1)
echo "$cover_result"

# 提取图片URL
cover_url=$(echo "$cover_result" | grep -o '"image_url": "[^"]*"' | sed 's/"image_url": "//;s/"$//')
echo "封面URL: $cover_url"

# 2. 上传封面到微信
echo "📤 上传封面到微信素材库..."
source ../.env
upload_result=$(python3 upload_material.py --app_id "$WECHAT_APP_ID" --app_secret "$WECHAT_APP_SECRET" --image_path /tmp/cover_ai_productivity.jpg 2>&1)
echo "$upload_result"

# 提取 thumb_media_id
thumb_media_id=$(echo "$upload_result" | python3 -c "import sys,json; print(json.load(sys.stdin)['thumb_media_id'])")
echo "封面 Media ID: $thumb_media_id"

# 输出结果到文件
echo "$thumb_media_id" > /tmp/thumb_media_id.txt
echo "$cover_url" > /tmp/cover_url.txt
