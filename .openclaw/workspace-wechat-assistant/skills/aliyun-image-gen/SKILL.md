# aliyun-image-gen

使用阿里云通义万相（Qwen-Image-2.0）生成图片。

## 默认配置

| 配置项 | 值 |
|--------|-----|
| **API Key** | `sk-ff15c72de8f1487088912988a97e13c7` |
| **默认模型** | `qwen-image-2.0` |

## 快速测试

```bash
# 文生图测试（使用默认 API Key）
curl -X POST 'https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer sk-ff15c72de8f1487088912988a97e13c7' \
  -d '{
    "model": "qwen-image-2.0",
    "input": {
      "messages": [
        {
          "role": "user",
          "content": [{ "text": "一只可爱的柴犬在樱花树下" }]
        }
      ]
    },
    "parameters": { "n": 1, "watermark": false }
  }'
```

## 环境变量覆盖

如需使用其他 API Key，可设置环境变量：

```bash
export ALIYUN_IMAGE_API_KEY="your-api-key"
```

## 使用

### 文生图

```json
{
  "prompt": "一只可爱的柴犬在樱花树下",
  "n": 2
}
```

### 图生图 / 多图参考

```json
{
  "prompt": "图1中的女生穿着图2中的黑色裙子按图3的姿势坐下",
  "referenceImages": [
    "https://example.com/image1.png",
    "https://example.com/image2.png",
    "https://example.com/image3.png"
  ],
  "n": 2
}
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `prompt` | string | - | 图片描述（必需）|
| `referenceImages` | string[] | - | 参考图片 URL 列表 |
| `n` | number | 1 | 生成图片数量（1-4）|
| `negativePrompt` | string | "" | 负面提示词 |
| `watermark` | boolean | false | 是否添加水印 |
| `model` | string | "qwen-image-2.0" | 模型版本 |

## 响应格式

```json
{
  "output": {
    "choices": [
      {
        "message": {
          "content": [
            { "image_url": "https://.../output1.png" }
          ]
        }
      }
    ]
  }
}
```

## 示例

### 简单文生图

> "用阿里云画一只宇航员猫咪在月球上"

### 带参考图

> "用阿里云生成图片：参考图 https://a.com/person.jpg 中的人物穿着 https://b.com/dress.jpg 中的红裙子"
