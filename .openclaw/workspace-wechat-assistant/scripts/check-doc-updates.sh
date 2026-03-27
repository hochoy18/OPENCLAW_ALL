#!/bin/bash
# OpenClaw 文档更新检查脚本
# 每天早上 8 点执行，检查官方文档是否有更新

WORKSPACE="/home/hochoy/.openclaw/workspace-wechat-assistant"
KNOWLEDGE_DIR="$WORKSPACE/knowledge"
LOG_FILE="$WORKSPACE/logs/doc-check.log"
STATE_FILE="$WORKSPACE/.doc-check-state"

# 创建必要的目录
mkdir -p "$KNOWLEDGE_DIR" "$WORKSPACE/logs"

# 记录日志
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "========== 开始检查文档更新 =========="

# 检查的文档 URLs
DOC_URLS=(
    "https://docs.OpenClaw.ai/zh-CN/concepts/multi-agent"
    "https://github.com/OpenClaw/OpenClaw/"
)

# 获取当前时间戳
CHECK_TIME=$(date '+%Y-%m-%d %H:%M:%S')

# 需要发送更新的标志
UPDATE_NEEDED=false
SUMMARY=""

for url in "${DOC_URLS[@]}"; do
    log "检查: $url"
    
    # 生成 URL 的 hash 作为状态文件名
    url_hash=$(echo "$url" | md5sum | cut -d' ' -f1)
    state_file="$STATE_FILE.$url_hash"
    
    # 获取当前内容
    current_content=$(curl -sL --max-time 30 "$url" 2>/dev/null)
    
    if [ -z "$current_content" ]; then
        log "获取内容失败: $url"
        continue
    fi
    
    # 计算当前内容的 hash
    current_hash=$(echo "$current_content" | md5sum | cut -d' ' -f1)
    
    # 读取上次的状态
    if [ -f "$state_file" ]; then
        last_hash=$(cat "$state_file")
        last_check=$(cat "$state_file.timestamp" 2>/dev/null || echo "未知")
        
        if [ "$current_hash" != "$last_hash" ]; then
            log "检测到更新: $url"
            UPDATE_NEEDED=true
            
            # 提取文档名称
            doc_name=$(echo "$url" | grep -oP '(multi-agent|OpenClaw)')
            [ -z "$doc_name" ] && doc_name="$url"
            
            SUMMARY="${SUMMARY}📝 文档更新: ${doc_name}\n"
            SUMMARY="${SUMMARY}   链接: ${url}\n"
            SUMMARY="${SUMMARY}   上次检查: ${last_check}\n\n"
            
            # 更新本地知识库
            if [[ "$url" == *"multi-agent"* ]]; then
                echo "$current_content" > "$KNOWLEDGE_DIR/openclaw-multi-agent-latest.md"
                log "已更新知识库: openclaw-multi-agent-latest.md"
            elif [[ "$url" == *"github"* ]]; then
                echo "$current_content" > "$KNOWLEDGE_DIR/openclaw-github-latest.md"
                log "已更新知识库: openclaw-github-latest.md"
            fi
        else
            log "无更新: $url"
        fi
    else
        log "首次检查，创建状态文件: $url"
    fi
    
    # 保存当前状态
    echo "$current_hash" > "$state_file"
    echo "$CHECK_TIME" > "$state_file.timestamp"
done

# 如果有更新，发送通知到飞书
if [ "$UPDATE_NEEDED" = true ]; then
    log "发送更新通知到飞书"
    
    # 构建通知消息
    notify_msg="🤖 OpenClaw 文档更新提醒\n\n"
    notify_msg="${notify_msg}${SUMMARY}"
    notify_msg="${notify_msg}---\n"
    notify_msg="${notify_msg}检查时间: ${CHECK_TIME}\n"
    notify_msg="${notify_msg}请查看知识库获取最新内容"
    
    # 发送到飞书 (使用 openclaw CLI)
    openclaw message send --channel feishu --message "$notify_msg" 2>> "$LOG_FILE"
    
    log "飞书通知已发送"
else
    log "无更新，跳过通知"
fi

log "========== 检查完成 =========="
