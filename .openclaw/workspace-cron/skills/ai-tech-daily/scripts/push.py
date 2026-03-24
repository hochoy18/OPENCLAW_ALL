#!/usr/bin/env python3
"""
推送模块 - 将生成的内容推送到飞书
"""
import json
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent

def load_config():
    """加载配置"""
    config_path = SKILL_DIR / "config.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def push_to_feishu(content, chat_id=None):
    """
    推送内容到飞书
    
    Args:
        content: 要推送的文本内容（Markdown）
        chat_id: 飞书群ID，默认使用配置中的
    
    Returns:
        bool: 是否成功
    """
    config = load_config()
    
    if chat_id is None:
        chat_id = config.get('feishu', {}).get('chat_id')
    
    if not chat_id:
        print("❌ 未配置飞书 chat_id")
        return False
    
    print(f"📤 推送到飞书群: {chat_id}")
    
    # TODO: 调用飞书 API 发送消息
    # 使用 message tool 或 Feishu API
    
    return True

def push_file(file_path, chat_id=None):
    """推送文件到飞书"""
    content = Path(file_path).read_text(encoding='utf-8')
    return push_to_feishu(content, chat_id)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--content", help="要推送的内容")
    parser.add_argument("--file", help="要推送的文件路径")
    parser.add_argument("--chat-id", help="飞书群ID")
    args = parser.parse_args()
    
    if args.file:
        push_file(args.file, args.chat_id)
    elif args.content:
        push_to_feishu(args.content, args.chat_id)
    else:
        print("请提供 --content 或 --file")
