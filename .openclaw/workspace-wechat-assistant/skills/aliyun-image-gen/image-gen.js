const SKILL_CONFIG = {
  API_KEY: process.env.ALIYUN_IMAGE_API_KEY || 'sk-ff15c72de8f1487088912988a97e13c7',
  MODEL: process.env.ALIYUN_IMAGE_MODEL || 'qwen-image-2.0',
  API_URL: 'https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation'
};

/**
 * 生成图片
 * @param {Object} params - 生成参数
 * @param {string} params.prompt - 提示词
 * @param {string[]} params.reference_images - 参考图片 URL 数组
 * @param {number} params.n - 生成数量
 * @param {string} params.negative_prompt - 负面提示词
 * @param {boolean} params.watermark - 是否加水印
 * @param {string} params.size - 图片尺寸
 * @param {number} params.seed - 随机种子
 */
async function generateImage(params) {
  const {
    prompt,
    reference_images = [],
    n = 1,
    negative_prompt = '',
    watermark = false,
    size,
    seed
  } = params;

  // 构建 content 数组
  const content = [];
  
  // 添加参考图片
  for (const imageUrl of reference_images) {
    content.push({ image: imageUrl });
  }
  
  // 添加文本提示
  content.push({ text: prompt });

  const requestBody = {
    model: SKILL_CONFIG.MODEL,
    input: {
      messages: [
        {
          role: 'user',
          content: content
        }
      ]
    },
    parameters: {
      n: Math.min(Math.max(1, n), 4), // 限制 1-4
      negative_prompt: negative_prompt || '',
      watermark: !!watermark
    }
  };

  // 可选参数
  if (size) {
    requestBody.parameters.size = size;
  }
  if (seed !== undefined) {
    requestBody.parameters.seed = seed;
  }

  try {
    const response = await fetch(SKILL_CONFIG.API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${SKILL_CONFIG.API_KEY}`
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`API 请求失败: ${response.status} - ${error}`);
    }

    const data = await response.json();
    
    // 解析返回的图片 URL
    const images = [];
    if (data.output && data.output.results) {
      for (const result of data.output.results) {
        if (result.url) {
          images.push(result.url);
        }
      }
    }

    return {
      success: images.length > 0,
      images,
      raw_response: data,
      usage: data.usage || {}
    };
  } catch (error) {
    return {
      success: false,
      error: error.message,
      images: []
    };
  }
}

module.exports = {
  generateImage,
  SKILL_CONFIG
};
