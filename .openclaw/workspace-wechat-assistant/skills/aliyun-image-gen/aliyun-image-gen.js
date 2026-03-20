const ALIYUN_IMAGE_API_URL = 'https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation';
const DEFAULT_MODEL = 'qwen-image-2.0';
const DEFAULT_API_KEY = 'sk-ff15c72de8f1487088912988a97e13c7';

/**
 * 阿里云图片生成
 * @param {Object} options - 配置选项
 * @param {string} options.prompt - 图片描述
 * @param {string[]} options.referenceImages - 参考图片 URL 列表
 * @param {number} options.n - 生成数量
 * @param {string} options.negativePrompt - 负面提示词
 * @param {boolean} options.watermark - 是否加水印
 * @param {string} options.model - 模型版本
 * @param {string} apiKey - API 密钥（可选，默认使用内置 key）
 */
async function generateImage(options, apiKey) {
  // 优先使用传入的 apiKey，其次环境变量，最后使用默认 key
  const key = apiKey || 
    (typeof process !== 'undefined' && process.env && process.env.ALIYUN_IMAGE_API_KEY) || 
    DEFAULT_API_KEY;
  
  if (!key) {
    throw new Error('Missing API key. Set ALIYUN_IMAGE_API_KEY env var or configure in openclaw.json');
  }

  const {
    prompt,
    referenceImages = [],
    n = 1,
    negativePrompt = '',
    watermark = false,
    model = DEFAULT_MODEL
  } = options;

  if (!prompt) {
    throw new Error('Prompt is required');
  }

  // 构建消息内容
  const content = [];
  
  // 添加参考图片
  for (const imageUrl of referenceImages) {
    content.push({ image: imageUrl });
  }
  
  // 添加文本提示
  content.push({ text: prompt });

  const requestBody = {
    model,
    input: {
      messages: [
        {
          role: 'user',
          content
        }
      ]
    },
    parameters: {
      n: Math.min(Math.max(n, 1), 4),
      negative_prompt: negativePrompt,
      watermark
    }
  };

  const response = await fetch(ALIYUN_IMAGE_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${key}`
    },
    body: JSON.stringify(requestBody)
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API request failed: ${response.status} - ${errorText}`);
  }

  const data = await response.json();
  
  // 解析响应
  const images = [];
  if (data.output && data.output.choices) {
    for (const choice of data.output.choices) {
      if (choice.message && choice.message.content) {
        for (const item of choice.message.content) {
          if (item.image_url) {
            images.push(item.image_url);
          }
        }
      }
    }
  }

  return { images };
}

// 工具导出
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { generateImage };
}
