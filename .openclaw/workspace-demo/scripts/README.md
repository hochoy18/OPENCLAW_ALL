# OpenClaw 文档更新检查工具

此工具集用于自动检查OpenClaw官方文档的更新，并生成更新摘要通知。

## 文件说明

1. **check_openclaw_docs.sh**
   - 主要的文档检查shell脚本
   - 负责从官方源获取最新文档并检测变化
   - 生成差异摘要并保存到临时目录

2. **docs_update_agent.js**
   - 原始的更新通知脚本
   - 执行shell脚本并解析结果

3. **send_docs_update.js**
   - 简化版的更新通知脚本
   - 直接读取最新的日志和摘要文件
   - 格式化通知消息

4. **docs_update_summary.js**
   - 改进版的更新分析脚本
   - 过滤掉HTML元数据变更
   - 仅保留有实质性内容的更新
   - 提供更加清晰的更新摘要

## 使用方法

1. 首次运行，初始化知识库：
   ```
   bash /home/hochoy/.openclaw/workspace-demo/scripts/check_openclaw_docs.sh
   ```

2. 定期检查更新：
   ```
   bash /home/hochoy/.openclaw/workspace-demo/scripts/check_openclaw_docs.sh
   ```

3. 生成格式化通知：
   ```
   node /home/hochoy/.openclaw/workspace-demo/scripts/docs_update_summary.js
   ```

## 文件目录结构

- **/home/hochoy/.openclaw/workspace-demo/**
  - **scripts/** - 脚本目录
    - check_openclaw_docs.sh
    - docs_update_agent.js
    - send_docs_update.js
    - docs_update_summary.js
  - **knowledge/** - 文档知识库
    - openclaw-multi-agent.md
    - openclaw-overview.md
  - **logs/** - 日志文件
    - docs_check_YYYY-MM-DD_HH-MM-SS.log
  - **temp/** - 临时文件
    - update_summary.txt

## 自动化建议

可以通过cron job定期运行检查脚本，并在检测到更新时发送通知：

```bash
# 每天早上9点检查OpenClaw文档更新
0 9 * * * bash /home/hochoy/.openclaw/workspace-demo/scripts/check_openclaw_docs.sh && node /home/hochoy/.openclaw/workspace-demo/scripts/docs_update_summary.js
```