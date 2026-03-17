/**
 * OpenClaw文档更新检查子代理
 * 
 * 此子代理负责：
 * 1. 运行文档检查脚本
 * 2. 分析结果
 * 3. 如果有更新，格式化并发送到飞书
 */

// 导入执行命令需要的模块
const { exec: childExec } = require('child_process');
const util = require('util');
const exec = util.promisify(childExec);
const fs = require('fs').promises;

// 获取今天的日期
const today = new Date();
const dateStr = today.toISOString().split('T')[0];

async function run() {
  // 打印任务开始信息
  console.log(`[${dateStr}] 开始检查OpenClaw文档更新...`);
  
  try {
    // 先检查是否是首次运行
    const knowledgeDir = '/home/hochoy/.openclaw/workspace-demo/knowledge/';
    const multiAgentPath = `${knowledgeDir}openclaw-multi-agent.md.old`;
    const overviewPath = `${knowledgeDir}openclaw-overview.md.old`;
    
    // 检查是否是首次运行
    let isFirstRun = false;
    try {
      await fs.access(multiAgentPath);
      await fs.access(overviewPath);
    } catch (e) {
      isFirstRun = true;
      console.log("检测到首次运行，将创建初始版本标记文件");
      
      // 尝试创建初始版本标记文件
      try {
        const multiAgentContent = await fs.readFile(`${knowledgeDir}openclaw-multi-agent.md`, 'utf8');
        const overviewContent = await fs.readFile(`${knowledgeDir}openclaw-overview.md`, 'utf8');
        
        await fs.writeFile(multiAgentPath, multiAgentContent);
        await fs.writeFile(overviewPath, overviewContent);
      } catch (writeErr) {
        console.log("创建初始版本标记文件失败:", writeErr);
      }
      
      return "OpenClaw文档知识库已初始化完成。将在下次运行时检测真实更新。";
    }
    
    // 运行文档检查脚本
    const scriptPath = '/home/hochoy/.openclaw/workspace-demo/scripts/check_openclaw_docs.sh';
    
    // 确保脚本存在
    try {
      await fs.access(scriptPath);
    } catch (e) {
      return `错误：文档检查脚本不存在，请确认路径: ${scriptPath}`;
    }
    
    // 执行脚本
    console.log("执行文档检查脚本...");
    const result = await exec(`bash ${scriptPath}`, { maxBuffer: 1024 * 1024 * 10 }); // 增大缓冲区
    
    console.log(`脚本执行结果: 退出码=${result.status || result.code || 0}`);
    console.log(`stdout长度: ${result.stdout ? result.stdout.length : 0}`);
    console.log(`stderr长度: ${result.stderr ? result.stderr.length : 0}`);
    
    // 检查脚本输出是否包含初始化信息
    if (result.stdout && result.stdout.includes("初始化知识库文件")) {
      console.log("知识库初始化完成，无需发送更新通知");
      return "OpenClaw文档知识库已初始化完成。将在下次运行时检测真实更新。";
    }
    
    // 检查脚本执行状态
    if ((result.status || result.code || 0) === 0) {
      console.log("文档检查完成：没有发现更新");
      return "OpenClaw文档没有更新。";
    } else {
      console.log("文档检查完成：发现更新！");
      
      // 解析输出以提取更新摘要
      const summaryFile = '/home/hochoy/.openclaw/workspace-demo/temp/update_summary.txt';
      let updateSummary = "检测到文档更新，但无法读取摘要。";
      
      try {
        updateSummary = await fs.readFile(summaryFile, 'utf8');
        // 摘要可能包含HTML内容，尝试提取纯文本
        updateSummary = cleanHtmlContent(updateSummary);
      } catch (readErr) {
        console.error("读取摘要文件失败:", readErr);
        // 尝试从stdout解析
        updateSummary = parseUpdateSummary(result.stdout);
      }
      
      // 格式化飞书消息
      const message = formatMessage(updateSummary);
      
      return message;
    }
  } catch (error) {
    console.error("执行文档检查脚本时出错:", error);
    
    return `OpenClaw文档检查过程中发生错误: ${error.message}`;
  }
}

// 解析更新摘要
function parseUpdateSummary(output) {
  // 提取更新摘要部分
  const summaryMatch = output.match(/==== OpenClaw文档更新摘要[\s\S]*$/);
  if (summaryMatch) {
    return cleanHtmlContent(summaryMatch[0]);
  }
  
  // 检查是否有日志文件信息
  const logMatch = output.match(/生成的摘要在\s+([^\s]+)/);
  if (logMatch) {
    return `检测到更新，详细摘要保存在: ${logMatch[1]}`;
  }
  
  return "检测到文档更新，但无法解析具体内容。请查看日志获取详情。";
}

// 清理HTML内容，提取纯文本
function cleanHtmlContent(html) {
  // 如果包含HTML标签
  if (html.includes('<html') || html.includes('<!DOCTYPE')) {
    // 简单清理HTML标签
    return html
      .replace(/<[^>]*>/g, '') // 移除HTML标签
      .replace(/\s+/g, ' ')    // 规范化空白
      .trim();
  }
  return html;
}

// 格式化飞书消息
function formatMessage(summary) {
  return `# 📢 OpenClaw文档更新通知 (${dateStr})

检测到OpenClaw文档有新的更新！以下是更新摘要：

${summary}

您可以通过以下命令查看完整文档：
\`\`\`
cat /home/hochoy/.openclaw/workspace-demo/knowledge/openclaw-multi-agent.md
cat /home/hochoy/.openclaw/workspace-demo/knowledge/openclaw-overview.md
\`\`\`

或直接查看知识库目录：
\`\`\`
ls -l /home/hochoy/.openclaw/workspace-demo/knowledge/
\`\`\`
`;
}

// 运行并返回结果
return run();