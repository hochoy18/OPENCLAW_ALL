# OpenClaw 文档更新自动检查与通知系统

## 系统概述

这个系统负责定期检查OpenClaw官方文档的更新，并在检测到更新时生成摘要通知。系统主要由以下组件组成：

1. **文档检查脚本** (check_openclaw_docs.sh)
   - 从官方文档源获取最新内容
   - 与本地知识库版本比对，检测变化
   - 生成更新差异摘要

2. **更新分析脚本** (docs_update_summary.js)
   - 分析检测到的变更
   - 过滤掉HTML元数据等非实质性变更
   - 生成格式化的更新通知

3. **整合脚本** (check_and_notify_docs_update.sh)
   - 整合检查和通知功能
   - 保存执行日志
   - 提供简单的使用接口

## 如何使用

### 手动检查文档更新

运行以下命令检查文档是否有更新，并在检测到更新时生成通知：

```bash
bash /home/hochoy/.openclaw/workspace-demo/scripts/check_and_notify_docs_update.sh
```

### 设置自动检查

可以通过cron作业定期自动检查文档更新：

1. 编辑cron配置：
   ```bash
   crontab -e
   ```

2. 添加以下配置（每天上午9点检查）：
   ```
   0 9 * * * /home/hochoy/.openclaw/workspace-demo/scripts/check_and_notify_docs_update.sh > /home/hochoy/.openclaw/workspace-demo/logs/cron_update_$(date +\%Y-\%m-\%d).log 2>&1
   ```

## 系统文件

- **主要脚本**
  - `/home/hochoy/.openclaw/workspace-demo/scripts/check_openclaw_docs.sh` - 文档检查脚本
  - `/home/hochoy/.openclaw/workspace-demo/scripts/docs_update_summary.js` - 更新分析脚本
  - `/home/hochoy/.openclaw/workspace-demo/scripts/check_and_notify_docs_update.sh` - 整合脚本

- **知识库目录**
  - `/home/hochoy/.openclaw/workspace-demo/knowledge/` - 存放最新文档
  
- **日志目录**
  - `/home/hochoy/.openclaw/workspace-demo/logs/` - 存放执行日志
  
- **临时文件**
  - `/home/hochoy/.openclaw/workspace-demo/temp/` - 存放临时文件和更新摘要

## 注意事项

1. 首次运行会初始化知识库，不会报告更新
2. 系统会自动过滤HTML元数据变更，只关注实质性内容变化
3. 所有文档版本都会保留备份，格式为`文件名.bak.时间戳`

## 故障排除

如果系统无法正常工作，请检查以下几点：

1. 确保所有脚本有执行权限：
   ```bash
   chmod +x /home/hochoy/.openclaw/workspace-demo/scripts/*.sh
   ```

2. 检查日志文件了解详细错误信息：
   ```bash
   ls -l /home/hochoy/.openclaw/workspace-demo/logs/
   ```

3. 确保目录结构完整：
   ```bash
   mkdir -p /home/hochoy/.openclaw/workspace-demo/{scripts,knowledge,logs,temp}
   ```