#!/bin/bash

# 测试阿里云图片生成 API

API_KEY="sk-ff15c72de8f1487088912988a97e13c7"
API_URL="https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"

# 文生图测试
echo "=== 测试 1: 文生图 ==="
curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "qwen-image-2.0",
    "input": {
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "text": "一只可爱的柴犬在樱花树下，高清写实风格"
            }
          ]
        }
      ]
    },
    "parameters": {
      "n": 1,
      "negative_prompt": "",
      "watermark": false
    }
  }' | tee /tmp/aliyun_test_response.json | jq '.'

echo ""
echo "=== 原始响应 ==="
cat /tmp/aliyun_test_response.json
