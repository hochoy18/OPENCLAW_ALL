---
name: aliyun-image-gen
description: 使用阿里云 DashScope 通义万相模型生成图片。支持文生图和垫图（参考图生成）。Use when user wants to generate images using Alibaba Cloud DashScope qwen-image model, including text-to-image and image-to-image generation with reference images.
---

# 阿里云图片生成

使用阿里云 DashScope 的通义万相模型生成图片。

## 使用方法

### 文本生成图片

```json
{
  "prompt": "一只可爱的橘猫在沙发上睡觉",
  "n": 2,
  "negative_prompt": "模糊，低质量",
  "watermark": false
}
```

### 参考图生成（垫图）

```json
{
  "prompt": "图1中的女生穿着图2中的黑色裙子按图3的姿势坐下",
  "reference_images": [
    "https://example.com/image1.png",
    "https://example.com/image2.png",
    "https://example.com/image3.png"
  ],
  "n": 2,
  "watermark": false
}
```

## 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | 是 | 图片描述文本 |
| reference_images | string[] | 否 | 参考图片 URL 数组（最多 5 张） |
| n | number | 否 | 生成图片数量，默认 1，最大 4 |
| negative_prompt | string | 否 | 负面提示词 |
| watermark | boolean | 否 | 是否添加水印，默认 false |
| size | string | 否 | 图片尺寸，如 "1024*1024" |
| seed | number | 否 | 随机种子 |

## 配置

通过环境变量配置：

- `ALIYUN_IMAGE_API_KEY` - 阿里云 DashScope API Key（默认使用内存中的 key）
- `ALIYUN_IMAGE_MODEL` - 模型名称（默认 qwen-image-2.0）

## 响应

成功时返回生成的图片 URL 数组：

```json
{
  "success": true,
  "images": [
    "https://example.com/output1.png",
    "https://example.com/output2.png"
  ],
  "usage": {
    "input_tokens": 100,
    "output_tokens": 0
  }
}
```

## 模型说明

- **qwen-image-2.0**: 通义万相 2.0，支持文生图和垫图功能
- 支持中英文提示词
- 支持多图参考（最多 5 张）

## 使用示例

1. **简单文生图**
   > "生成一张夕阳下海滩的图片"

2. **带参考图**
   > "参考这几张图片的风格，生成一张森林中的小屋" + 上传图片

3. **多图融合**
   > "把图1的人物和图2的背景结合" + 上传两张图片
