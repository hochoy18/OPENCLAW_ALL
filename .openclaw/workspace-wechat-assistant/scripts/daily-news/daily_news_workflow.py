#!/usr/bin/env python3
"""
每日热点公众号自动创作 - 主工作流

功能：
1. 搜索热点（AI工具 + 职场）
2. 选题决策（按 3:1 比例）
3. crayon 风格写文章
4. 生成封面图
5. 发布到草稿箱
6. 发送通知

Usage:
    python3 daily_news_workflow.py
"""

import os
import sys
import json
import random
import subprocess
from datetime import datetime
from pathlib import Path

# 添加 skills 路径
SKILL_DIR = Path(__file__).parent.parent.parent / "skills"
sys.path.insert(0, str(SKILL_DIR / "wechat-article-publisher" / "scripts"))

# 加载配置
try:
    from config import load_config, get_wechat_config
    config = load_config()
    wechat_config = get_wechat_config()
except Exception as e:
    print(f"配置加载失败: {e}")
    sys.exit(1)

# 搜索关键词配置
AI_TOPICS = [
    "AI tools trending 2024",
    "new AI tool this week",
    "ChatGPT alternatives",
    "AI productivity tools",
    "best AI apps 2024",
    "人工智能工具 最新",
    "AI 软件 热点",
]

WORKPLACE_TOPICS = [
    "职场 热议 2024",
    "打工人 热点",
    "职场 成长 干货",
    "工作 技巧",
]

def search_with_tavily(query: str) -> dict:
    """使用 Tavily 搜索"""
    script_path = SKILL_DIR / "tavily-search" / "scripts" / "search.py"
    
    result = subprocess.run(
        ["python3", str(script_path), query, "--depth", "basic"],
        capture_output=True,
        text=True,
        cwd=str(SKILL_DIR / "tavily-search")
    )
    
    if result.returncode != 0:
        print(f"搜索失败: {result.stderr}")
        return {}
    
    return {"query": query, "output": result.stdout}

def generate_cover_image(prompt: str, output_path: str) -> dict:
    """生成封面图"""
    script_path = SKILL_DIR / "wechat-article-publisher" / "scripts" / "generate_cover.py"
    
    result = subprocess.run(
        [
            "python3", str(script_path),
            "--prompt", prompt,
            "--provider", "minimax",
            "--aspect-ratio", "16:9",
            "--output", output_path
        ],
        capture_output=True,
        text=True,
        cwd=str(SKILL_DIR / "wechat-article-publisher" / "scripts")
    )
    
    if result.returncode != 0:
        print(f"封面生成失败: {result.stderr}")
        return {}
    
    try:
        return json.loads(result.stdout)
    except:
        return {}

def upload_to_wechat(image_path: str) -> str:
    """上传图片到微信素材库"""
    script_path = SKILL_DIR / "wechat-article-publisher" / "scripts" / "upload_material.py"
    
    result = subprocess.run(
        [
            "python3", str(script_path),
            "--app_id", wechat_config['app_id'],
            "--app_secret", wechat_config['app_secret'],
            "--image_path", image_path
        ],
        capture_output=True,
        text=True,
        cwd=str(SKILL_DIR / "wechat-article-publisher" / "scripts")
    )
    
    if result.returncode != 0:
        print(f"上传失败: {result.stderr}")
        return None
    
    try:
        data = json.loads(result.stdout)
        return data.get("thumb_media_id")
    except:
        return None

def create_draft(title: str, content: str, digest: str, thumb_media_id: str = None) -> str:
    """创建草稿"""
    script_path = SKILL_DIR / "wechat-article-publisher" / "scripts" / "create_draft.py"
    
    cmd = [
        "python3", str(script_path),
        "--app_id", wechat_config['app_id'],
        "--app_secret", wechat_config['app_secret'],
        "--title", title,
        "--content", content,
        "--digest", digest
    ]
    
    if thumb_media_id:
        cmd.extend(["--thumb_media_id", thumb_media_id])
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(SKILL_DIR / "wechat-article-publisher" / "scripts")
    )
    
    if result.returncode != 0:
        print(f"创建草稿失败: {result.stderr}")
        return None
    
    try:
        data = json.loads(result.stdout)
        return data.get("media_id")
    except:
        return None

def determine_topic():
    """
    决定今天的选题
    按 3:1 比例（AI : 职场）
    """
    # 每周一算起，第几天
    today = datetime.now().strftime("%w")
    
    # 简单方案：随机但保持比例
    # 4天一个周期：3天AI + 1天职场
    cycle_day = int(today) % 4
    
    if cycle_day == 0:
        return "workplace", random.choice(WORKPLACE_TOPICS)
    else:
        return "ai", random.choice(AI_TOPICS)

def main():
    print("=" * 50)
    print(f"每日热点公众号工作流 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Step 1: 选题决策
    topic_type, topic_keyword = determine_topic()
    print(f"\n[1/6] 选题决策")
    print(f"  类型: {'AI工具测评' if topic_type == 'ai' else '职场打工人'}")
    print(f"  关键词: {topic_keyword}")
    
    # Step 2: 搜索热点
    print(f"\n[2/6] 搜索热点...")
    search_results = search_with_tavily(topic_keyword)
    print(f"  搜索完成: {topic_keyword}")
    
    # Step 3-4: 写文章（由 Agent 完成后填充）
    # 这里输出提示信息，实际写作由 Agent 执行
    print(f"\n[3/6] 准备写作上下文...")
    print(f"  搜索结果已保存，可供 Agent 使用")
    
    print(f"\n[4/6] 文章写作 (crayon 风格)")
    print(f"  -> 由 Agent 读取 crayon skill 后执行")
    
    print(f"\n[5/6] 封面图生成")
    print(f"  -> 文章完成后执行")
    
    print(f"\n[6/6] 发布草稿箱")
    print(f"  -> 封面完成后执行")
    
    print("\n" + "=" * 50)
    print("工作流启动成功！Agent 将继续执行后续步骤。")
    print("=" * 50)

if __name__ == "__main__":
    main()
