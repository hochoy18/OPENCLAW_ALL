/**
 * OpenClaw文档更新通知子代理
 * 
 * 此脚本负责：
 * 1. 读取OpenClaw文档更新检查的结果
 * 2. 分析结果
 * 3. 格式化并发送到飞书
 */

// 导入所需模块
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 获取今天的日期
const today = new Date();
const dateStr = today.toISOString().split('T')[0];

// 工作目录
const WORKSPACE = '/home/hochoy/.openclaw/workspace-demo';
const LOGS_DIR = path.join(WORKSPACE, 'logs');
const TEMP_DIR = path.join(WORKSPACE, 'temp');
const KNOWLEDGE_DIR = path.join(WORKSPACE, 'knowledge');

// 格式化飞书消息
function formatMessage(summary) {
  return `# 📢 OpenClaw文档更新通知 (${dateStr})

检测到OpenClaw文档有新的更新！以下是更新摘要：

${summary}

您可以通过以下命令查看完整文档：
\`\`\`
cat ${KNOWLEDGE_DIR}/openclaw-multi-agent.md
cat ${KNOWLEDGE_DIR}/openclaw-overview.md
\`\`\`

或直接查看知识库目录：
\`\`\`
ls -l ${KNOWLEDGE_DIR}/
\`\`\`
`;
}

// 主函数
async function run() {
  console.log(`[${dateStr}] 开始处理OpenClaw文档更新通知...`);
  
  try {
    // 1. 找到最新的日志文件
    const latestLog = execSync(`ls -t ${LOGS_DIR}/docs_check_*.log | head -1`).toString().trim();
    console.log(`找到最新日志文件: ${latestLog}`);
    
    if (!latestLog) {
      console.log("没有找到日志文件，请先运行文档检查脚本");
      return "错误：没有找到日志文件，请先运行文档检查脚本";
    }
    
    // 2. 读取日志内容
    const logContent = fs.readFileSync(latestLog, 'utf8');
    
    // 3. 检查是否是初始化运行
    if (logContent.includes('初始化知识库文件')) {
      console.log("这是初始化运行，不发送更新通知");
      return "OpenClaw文档知识库已初始化完成。将在下次运行时检测真实更新。";
    }
    
    // 4. 检查是否有更新
    if (!logContent.includes('发现文档更新')) {
      console.log("没有检测到文档更新");
      return "OpenClaw文档没有更新。";
    }
    
    // 5. 提取摘要文件路径
    const summaryMatch = logContent.match(/生成的摘要在\s+([^\s]+)/);
    if (!summaryMatch) {
      console.log("无法从日志中找到摘要文件路径");
      return "错误：无法从日志中找到摘要文件路径";
    }
    
    const summaryPath = summaryMatch[1];
    console.log(`找到摘要文件路径: ${summaryPath}`);
    
    // 6. 读取摘要文件
    if (!fs.existsSync(summaryPath)) {
      console.log(`摘要文件不存在: ${summaryPath}`);
      return `错误：摘要文件不存在: ${summaryPath}`;
    }
    
    const summaryContent = fs.readFileSync(summaryPath, 'utf8');
    console.log(`成功读取摘要文件，大小: ${summaryContent.length} 字节`);
    
    // 7. 格式化通知消息
    const message = formatMessage(summaryContent);
    
    return message;
  } catch (error) {
    console.error("处理文档更新通知时出错:", error);
    return `处理OpenClaw文档更新时发生错误: ${error.message}`;
  }
}

// 运行并返回结果
return run();