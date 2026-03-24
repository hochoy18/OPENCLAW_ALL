#!/usr/bin/env python3
"""
飞书多维表格任务管理工具
"""
import json
import requests
import sys
from datetime import datetime, timedelta

CONFIG_FILE = '/home/hochoy/.openclaw/workspace/feishu_config.json'

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def get_token(config):
    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": config['app_id'], "app_secret": config['app_secret']}
    )
    return resp.json()['tenant_access_token']

def list_tasks():
    config = load_config()
    token = get_token(config)
    headers = {"Authorization": f"Bearer {token}"}
    
    resp = requests.get(
        f"https://open.feishu.cn/open-apis/bitable/v1/apps/{config['bitable_app_token']}/tables/{config['bitable_table_id']}/records?page_size=50",
        headers=headers
    )
    
    result = resp.json()
    if result.get('code') == 0:
        items = result.get('data', {}).get('items', [])
        print(f"📋 任务列表（共 {len(items)} 个）\n")
        print("-" * 60)
        
        for i, item in enumerate(items, 1):
            fields = item.get('fields', {})
            text = fields.get('文本', '')
            if text:
                print(f"{i}. {text}")
        print("-" * 60)
    else:
        print(f"❌ 获取失败: {result.get('msg')}")

def add_task(title):
    config = load_config()
    token = get_token(config)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    data = {"fields": {"文本": title}}
    
    resp = requests.post(
        f"https://open.feishu.cn/open-apis/bitable/v1/apps/{config['bitable_app_token']}/tables/{config['bitable_table_id']}/records",
        headers=headers,
        json=data
    )
    
    result = resp.json()
    if result.get('code') == 0:
        print(f"✅ 任务创建成功: {title}")
    else:
        print(f"❌ 创建失败: {result.get('msg')}")

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 bitable_task.py list       # 列出任务")
        print("  python3 bitable_task.py add '任务名称'  # 添加任务")
        return
    
    cmd = sys.argv[1]
    if cmd == 'list':
        list_tasks()
    elif cmd == 'add' and len(sys.argv) > 2:
        add_task(sys.argv[2])
    else:
        print("未知命令")

if __name__ == '__main__':
    main()
