#!/bin/bash

# 设置工作目录和临时目录
WORKSPACE="/home/hochoy/.openclaw/workspace-demo"
KNOWLEDGE_DIR="${WORKSPACE}/knowledge"
TEMP_DIR="${WORKSPACE}/temp"
LOG_DIR="${WORKSPACE}/logs"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
MAX_DIFF_LINES=50 # 限制差异输出行数，避免过大的摘要

# 确保目录存在
mkdir -p "${TEMP_DIR}"
mkdir -p "${LOG_DIR}"
mkdir -p "${KNOWLEDGE_DIR}"

# 日志文件
LOG_FILE="${LOG_DIR}/docs_check_${TIMESTAMP}.log"

# 输出到日志文件
exec > "${LOG_FILE}" 2>&1

echo "==== OpenClaw文档更新检查 - $(date) ===="

# 创建一个函数来提取文档内容
extract_content() {
    local input_file="$1"
    local output_file="$2"
    
    # 尝试提取Markdown内容，去除HTML标记
    if grep -q "<!DOCTYPE html>" "${input_file}"; then
        # 这是一个HTML文件，尝试提取正文内容
        echo "检测到HTML内容，尝试提取有用的Markdown部分..."
        
        # 尝试提取Markdown部分
        if grep -q "# 多智能体路由" "${input_file}"; then
            echo "提取多智能体路由内容..."
            sed -n '/# 多智能体路由/,/Built with/p' "${input_file}" | 
                grep -v "Built with" | 
                grep -v "<<<END_EXTERNAL_UNTRUSTED_CONTENT" > "${output_file}"
        elif grep -q "OpenClaw is a personal AI assistant" "${input_file}"; then
            echo "提取GitHub仓库内容..."
            sed -n '/OpenClaw is a personal AI assistant/,/openclaw\/openclaw/p' "${input_file}" | 
                grep -v "<<<END_EXTERNAL_UNTRUSTED_CONTENT" > "${output_file}"
        else
            # 如果找不到特定的Markdown部分，则转换HTML为纯文本
            echo "未找到特定Markdown部分，提取可读文本..."
            grep -v "^<" "${input_file}" | 
                grep -v "SECURITY NOTICE" | 
                grep -v "<<<EXTERNAL_UNTRUSTED_CONTENT" |
                grep -v "<<<END_EXTERNAL_UNTRUSTED_CONTENT" > "${output_file}"
        fi
    else
        # 不是HTML，直接使用原内容
        cat "${input_file}" > "${output_file}"
    fi
    
    # 检查提取后的内容
    local line_count=$(wc -l < "${output_file}")
    if [ ${line_count} -lt 10 ]; then
        echo "警告：提取后的内容过少（${line_count}行），可能提取失败"
        echo "使用原始内容的部分行..."
        head -100 "${input_file}" > "${output_file}"
    fi
}

# 创建一个函数来获取文档并检测变化
fetch_and_check() {
    local url="$1"
    local file_name="$2"
    local temp_file="${TEMP_DIR}/${file_name}.md.raw"
    local processed_file="${TEMP_DIR}/${file_name}.md.processed"
    local target_file="${KNOWLEDGE_DIR}/${file_name}.md"
    local changes_file="${TEMP_DIR}/${file_name}_changes.txt"
    local is_new=0
    
    echo "正在检查 ${url} 的更新..."
    
    # 使用curl获取文档内容
    if curl -s "${url}" > "${temp_file}"; then
        # 处理获取的内容
        extract_content "${temp_file}" "${processed_file}"
        
        # 检查目标文件是否存在
        if [ -f "${target_file}" ]; then
            # 比较文件以检测更改
            if diff -q "${target_file}" "${processed_file}" >/dev/null; then
                echo "✓ ${file_name} 没有变化"
                rm "${temp_file}" "${processed_file}"
                return 0
            else
                echo "! 发现 ${file_name} 有更新"
                # 生成差异摘要
                echo "==== ${file_name} 更新摘要 ====" > "${changes_file}"
                diff -U 1 "${target_file}" "${processed_file}" | 
                    grep -v "^---" | 
                    grep -v "^+++" | 
                    grep "^[+-]" | 
                    head -${MAX_DIFF_LINES} >> "${changes_file}"
                
                # 如果差异行数超过限制，添加说明
                local diff_lines=$(grep -c "^[+-]" "${changes_file}")
                if [ ${diff_lines} -ge ${MAX_DIFF_LINES} ]; then
                    echo "... (更多差异已省略)" >> "${changes_file}"
                fi
                
                # 备份旧文件
                cp "${target_file}" "${target_file}.bak.${TIMESTAMP}"
                
                # 更新文件
                cp "${processed_file}" "${target_file}"
                
                return 1  # 返回非零表示有变化
            fi
        else
            echo "! ${target_file} 不存在，创建新文件"
            cp "${processed_file}" "${target_file}"
            
            echo "==== ${file_name} 首次创建 ====" > "${changes_file}"
            echo "首次创建文件，包含以下内容摘要:" >> "${changes_file}"
            head -20 "${target_file}" >> "${changes_file}"
            if [ $(wc -l < "${target_file}") -gt 20 ]; then
                echo "... (更多内容已省略)" >> "${changes_file}"
            fi
            
            is_new=1
            return 1  # 返回非零表示有变化
        fi
    else
        echo "× 无法获取 ${url}"
        rm -f "${temp_file}" "${processed_file}"
        return 2  # 返回2表示错误
    fi
}

# 检查两个文档
CHANGES_FOUND=0
FIRST_RUN=0

# 第一个文档：多代理概念
fetch_and_check "https://docs.OpenClaw.ai/zh-CN/concepts/multi-agent" "openclaw-multi-agent"
RESULT=$?
if [ ${RESULT} -eq 1 ]; then
    CHANGES_FOUND=1
    if [ ! -f "${KNOWLEDGE_DIR}/openclaw-multi-agent.md.old" ]; then
        FIRST_RUN=1
    fi
fi

# 第二个文档：GitHub仓库
fetch_and_check "https://github.com/OpenClaw/OpenClaw" "openclaw-overview"
RESULT=$?
if [ ${RESULT} -eq 1 ]; then
    CHANGES_FOUND=1
    if [ ! -f "${KNOWLEDGE_DIR}/openclaw-overview.md.old" ]; then
        FIRST_RUN=1
    fi
fi

# 如果是首次运行，不报告更改
if [ ${FIRST_RUN} -eq 1 ]; then
    echo "这是首次运行，初始化知识库文件"
    for file in "${KNOWLEDGE_DIR}"/*.md; do
        touch "${file}.old"
    done
    
    # 提示而不报告变化
    echo "知识库已初始化。下次运行将检测真实更改。"
    exit 0
fi

# 如果发现更改，生成摘要报告
if [ ${CHANGES_FOUND} -eq 1 ]; then
    SUMMARY_FILE="${TEMP_DIR}/update_summary.txt"
    echo "==== OpenClaw文档更新摘要 (${TIMESTAMP}) ====" > "${SUMMARY_FILE}"
    echo "" >> "${SUMMARY_FILE}"
    
    if [ -f "${TEMP_DIR}/openclaw-multi-agent_changes.txt" ]; then
        echo "## 多代理文档更新" >> "${SUMMARY_FILE}"
        cat "${TEMP_DIR}/openclaw-multi-agent_changes.txt" >> "${SUMMARY_FILE}"
        echo "" >> "${SUMMARY_FILE}"
    fi
    
    if [ -f "${TEMP_DIR}/openclaw-overview_changes.txt" ]; then
        echo "## OpenClaw概述更新" >> "${SUMMARY_FILE}"
        cat "${TEMP_DIR}/openclaw-overview_changes.txt" >> "${SUMMARY_FILE}"
        echo "" >> "${SUMMARY_FILE}"
    fi
    
    echo "发现文档更新，生成的摘要在 ${SUMMARY_FILE}"
    
    # 将更新摘要输出到标准输出，用于OpenClaw cron任务读取
    cat "${SUMMARY_FILE}"
    
    # 清理临时文件
    rm -f "${TEMP_DIR}"/*_changes.txt
    exit 1  # 发现更改，返回非零
else
    echo "未发现文档更新"
    exit 0  # 没有更改，返回零
fi