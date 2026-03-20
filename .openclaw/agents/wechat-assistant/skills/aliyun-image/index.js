const https = require('https');
const fs = require('fs');
const path = require('path');

async function generate_image(args) {
  const { prompt, n = 1, negative_prompt = '', watermark = false, reference_images = [] } = args;
  
  // Load API key from config
  const configPath = path.join(__dirname, 'config.json');
  let apiKey = process.env.DASHSCOPE_API_KEY;
  
  if (!apiKey && fs.existsSync(configPath)) {
    try {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      apiKey = config.api_key;
    } catch (e) {
      console.error('Failed to load config:', e.message);
    }
  }
  
  if (!apiKey) {
    throw new Error('API key not found. Set DASHSCOPE_API_KEY environment variable or configure config.json');
  }
  
  // Build content array
  const content = [];
  
  // Add reference images if provided
  if (reference_images && reference_images.length > 0) {
    for (const imgUrl of reference_images) {
      content.push({ image: imgUrl });
    }
  }
  
  // Add text prompt
  content.push({ text: prompt });
  
  const requestBody = {
    model: 'qwen-image-2.0',
    input: {
      messages: [
        {
          role: 'user',
          content: content
        }
      ]
    },
    parameters: {
      n: n,
      negative_prompt: negative_prompt,
      watermark: watermark
    }
  };
  
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(requestBody);
    
    const options = {
      hostname: 'dashscope-intl.aliyuncs.com',
      port: 443,
      path: '/api/v1/services/aigc/multimodal-generation/generation',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'Content-Length': Buffer.byteLength(postData)
      }
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(response);
          } else {
            reject(new Error(`API Error ${res.statusCode}: ${data}`));
          }
        } catch (e) {
          reject(new Error(`Failed to parse response: ${e.message}`));
        }
      });
    });
    
    req.on('error', (e) => {
      reject(new Error(`Request failed: ${e.message}`));
    });
    
    req.write(postData);
    req.end();
  });
}

module.exports = { generate_image };
