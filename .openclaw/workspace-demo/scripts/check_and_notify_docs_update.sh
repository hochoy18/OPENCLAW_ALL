#!/bin/bash

# OpenClaw文档更新检查和通知脚本
# 此脚本完成以下任务：
# 1. 运行文档检查脚本
# 2. 如果有更新，则运行分析脚本并输出通知消息

# 工作目录
WORKSPACE="/home/hochoy/.openclaw/workspace-demo"
SCRIPTS_DIR="${WORKSPACE}/scripts"
LOGS_DIR="${WORKSPACE}/logs"

# 时间戳
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOG_FILE="${LOGS_DIR}/update_check_${TIMESTAMP}.log"

# 确保日志目录存在
mkdir -p "${LOGS_DIR}"

# 执行文档检查脚本
echo "开始检查OpenClaw文档更新..."
bash "${SCRIPTS_DIR}/check_openclaw_docs.sh"
CHECK_EXIT_CODE=$?

if [ ${CHECK_EXIT_CODE} -eq 0 ]; then
  echo "没有检测到文档更新."
  echo "OpenClaw文档没有更新。" > "${LOG_FILE}"
  cat "${LOG_FILE}"
  exit 0
fi

# 如果退出代码为0，表示没有更新
# 如果退出代码为非0，可能是检测到更新或是出错

# 分析更新并生成通知
echo "检测到更新，分析更新内容..."
node "${SCRIPTS_DIR}/docs_update_summary.js" | tee "${LOG_FILE}"

echo "更新检查完成。日志保存在: ${LOG_FILE}"
exit ${CHECK_EXIT_CODE}