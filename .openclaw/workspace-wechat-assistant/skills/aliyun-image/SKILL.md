# Aliyun Image Generation

Generate images using Alibaba Cloud DashScope (Qwen Image 2.0) API.

## Usage

```json
{
  "prompt": "A cat wearing a hat",
  "n": 1,
  "negative_prompt": "",
  "watermark": false
}
```

### Parameters

- `prompt` (string, required): The text description of the image to generate
- `n` (number, optional): Number of images to generate (default: 1)
- `negative_prompt` (string, optional): Things to avoid in the image
- `watermark` (boolean, optional): Whether to add watermark (default: false)
- `reference_images` (array, optional): URLs of reference images to use

## Example

```json
{
  "prompt": "图1中的女生穿着图2中的黑色裙子按图3的姿势坐下",
  "reference_images": [
    "https://example.com/image1.png",
    "https://example.com/image2.png",
    "https://example.com/image3.png"
  ],
  "n": 2
}
```

## API Reference

- Endpoint: `https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
- Model: `qwen-image-2.0`
- Documentation: https://www.alibabacloud.com/help/en/model-studio/developer-reference/qwen-image-2.0

## Configuration

Set your API key in `config.json`:

```json
{
  "api_key": "your-dashscope-api-key"
}
```
