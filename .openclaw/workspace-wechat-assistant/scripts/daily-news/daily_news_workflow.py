#!/usr/bin/env python3
"""
每日热点公众号自动创作 - 主工作流 v2

功能：
1. 读取当天 hots/YYYY-MM-DD.md 热点
2. 选题（从热点中选取）
3. crayon 风格写文章
4. 生成封面图 + 内容配图
5. 发布到草稿箱
6. 发送通知

Usage:
    python3 scripts/daily-news/daily_news_workflow.py
    python3 scripts/daily-news/daily_news_workflow.py --topic 1  # 选第1个话题
"""

import os
import sys
import json
import random
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/home/hochoy/.openclaw/workspace-wechat-assistant")
SKILL_DIR = WORKSPACE / "skills"
HOTS_DIR = WORKSPACE / "hots"

# 添加 skills 路径
sys.path.insert(0, str(SKILL_DIR / "wechat-article-publisher" / "scripts"))

# 加载配置
try:
    from config import load_config, get_wechat_config
    config = load_config()
    wechat_config = get_wechat_config()
except Exception as e:
    print(f"配置加载失败: {e}")
    sys.exit(1)


def read_daily_hots(date_str: str = None) -> list:
    """读取当天热点文件"""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    md_file = HOTS_DIR / f"{date_str}.md"
    
    if not md_file.exists():
        print(f"热点文件不存在: {md_file}")
        return []
    
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 解析 md 文件，提取热点
    hots = []
    lines = content.split("\n")
    current_title = None
    
    for line in lines:
        if line.startswith("## "):
            current_title = line[3:].strip()
            hots.append({"title": current_title, "content": ""})
        elif line.startswith("**来源**:"):
            if hots:
                hots[-1]["query"] = line.split(":**")[1].strip() if ":**" in line else ""
        elif line.startswith("**链接**:"):
            if hots:
                hots[-1]["url"] = line.split(":**")[1].strip() if ":**" in line else ""
        elif line.startswith("**摘要**:"):
            if hots:
                hots[-1]["content"] = line.replace("**摘要**:", "").replace("...", "").strip()
    
    return hots


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


def create_draft(title: str, content: str, digest: str, thumb_media_id: str = None) -> dict:
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
        return {}
    
    try:
        return json.loads(result.stdout)
    except:
        return {}


def main():
    parser = argparse.ArgumentParser(description='每日热点公众号工作流')
    parser.add_argument('--topic', type=int, default=None, help='选择第几个话题 (1-5)')
    parser.add_argument('--date', type=str, default=None, help='指定日期 YYYY-MM-DD')
    args = parser.parse_args()
    
    date_str = args.date or datetime.now().strftime('%Y-%m-%d')
    
    print("=" * 60)
    print(f"每日热点公众号工作流 - {date_str}")
    print("=" * 60)
    
    # Step 1: 读取当天热点
    print(f"\n[1/5] 读取热点...")
    hots = read_daily_hots(date_str)
    
    if not hots:
        print("  没有找到热点，请先运行热点收集脚本")
        print(f"  python3 {WORKSPACE}/scripts/daily-hot-collect.py")
        sys.exit(1)
    
    print(f"  找到 {len(hots)} 个热点话题:")
    for i, h in enumerate(hots, 1):
        print(f"    {i}. {h['title']}")
    
    # Step 2: 选题
    print(f"\n[2/5] 选题...")
    if args.topic:
        idx = args.topic - 1
        if idx < 0 or idx >= len(hots):
            print(f"  无效的话题编号: {args.topic}")
            sys.exit(1)
        selected = hots[idx]
        print(f"  指定话题: {selected['title']}")
    else:
        # 默认选第1个（最热的）
        selected = hots[0]
        print(f"  自动选择: {selected['title']}")
    
    # 输出写作上下文
    print(f"\n[3/5] 文章写作 (crayon 风格)")
    print(f"  标题: 请控制在20字以内")
    print(f"  话题: {selected['title']}")
    print(f"  内容摘要: {selected.get('content', '')[:100]}...")
    print(f"  参考链接: {selected.get('url', '无')}")
    print(f"\n  -> 请使用 crayon skill 写作，完成后继续")
    
    print(f"\n[4/5] 配图生成")
    print(f"  -> 封面图 + 3张内容配图，均匀分布")
    
    print(f"\n[5/5] 发布草稿箱")
    print(f"  -> 使用 mp-draft-push 推送")
    
    print("\n" + "=" * 60)
    print("工作流准备完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
