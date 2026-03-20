#!/usr/bin/env node
/**
 * Feishu Group Welcome Handler
 * Sends welcome messages when new members join a group
 */

const fs = require('fs');
const path = require('path');

// Load configuration
const CONFIG_FILE = path.join(__dirname, '..', 'config.json');

function loadConfig() {
  try {
    return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
  } catch (e) {
    return {};
  }
}

function getWelcomeMessage(chatId, userId, userName) {
  const config = loadConfig();
  const chatConfig = config[chatId];
  
  if (!chatConfig || !chatConfig.enabled) {
    return null;
  }
  
  let message = chatConfig.welcome_message || '欢迎 @新成员 加入群聊！🎉';
  
  if (chatConfig.mention_new_member && userId) {
    message = message.replace('@新成员', `\u003cat user_id="${userId}"\u003e${userName || '新成员'}\u003c/at\u003e`);
  }
  
  return message;
}

// Main handler
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args[0] === 'get-message') {
    const chatId = args[1];
    const userId = args[2];
    const userName = args[3];
    
    const message = getWelcomeMessage(chatId, userId, userName);
    if (message) {
      console.log(message);
      process.exit(0);
    } else {
      process.exit(1);
    }
  }
  
  if (args[0] === 'list-config') {
    console.log(JSON.stringify(loadConfig(), null, 2));
    process.exit(0);
  }
}

module.exports = { getWelcomeMessage, loadConfig };