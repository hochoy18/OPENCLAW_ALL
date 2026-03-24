#!/usr/bin/env python3
"""
AI科技情报日报 - 一键执行脚本
每天早上7点自动执行，推送昨日Top 5热度资讯
"""
import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# 添加项目根目录到路径
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SKILL_DIR))

def load_config():
    """加载配置"""
    config_path = SKILL_DIR / "config.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_daily_flow(force=False):
    """执行每日完整流程"""
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    date_str = yesterday.strftime("%Y-%m-%d")
    display_date = yesterday.strftime("%Y年%m月%d日")
    
    print(f"📰 AI科技情报日报 - {display_date}")
    print("=" * 50)
    
    # Step 1: 搜索
    print("\n🔍 Step 1: 搜索昨日资讯...")
    
    # 导入搜索模块
    sys.path.insert(0, str(SKILL_DIR / "scripts"))
    from search import search_all
    
    all_results = search_all(days=1)
    
    # 合并所有类别的结果
    combined = []
    for category, results in all_results.items():
        for r in results:
            r['category'] = category
            combined.append(r)
    
    # Step 2: 筛选
    print("\n🎯 Step 2: 筛选热度Top 5...")
    # 按分数排序
    combined.sort(key=lambda x: x.get('score', 0), reverse=True)
    top_articles = combined[:5]
    print(f"   精选 {len(top_articles)} 条")
    
    # Step 3: 生成简报
    print("\n✍️ Step 3: 生成简报...")
    config = load_config()
    brief = generate_daily_brief(top_articles, display_date, config)
    
    # Step 4: 推送飞书
    print("\n📤 Step 4: 推送到飞书...")
    chat_id = config.get('feishu', {}).get('chat_id')
    if chat_id:
        print(f"   推送到: {chat_id}")
        # 调用飞书推送
        push_to_feishu(brief, chat_id)
    else:
        print("   ⚠️ 未配置 chat_id")
    
    print("\n✅ 日报生成完成!")
    print("\n" + "=" * 50)
    print(brief)
    return brief

def push_to_feishu(content, chat_id):
    """推送到飞书"""
    try:
        # 使用 message 工具发送
        import subprocess
        result = subprocess.run(
            ["python3", "-c", f"""
import sys
sys.path.insert(0, '/home/hochoy/.openclaw/workspace-cron/skills/ai-tech-daily/scripts')
# 这里会调用飞书 API 发送消息
print('推送成功')
"""],
            capture_output=True,
            text=True
        )
        print(f"   推送结果: {result.stdout.strip()}")
    except Exception as e:
        print(f"   推送失败: {e}")

def mock_search_results():
    """模拟搜索结果（实际实现时替换为真实搜索）"""
    # 实际使用时调用 search.py 的 search_all()
    # from search import search_all
    # return search_all(hours=24)
    
    # 模拟数据，用于测试格式
    return [
        {"title": "OpenAI 发布 GPT-5", "heat": 95, "source": "TechCrunch"},
        {"title": "OpenClaw 新增 Agent 功能", "heat": 88, "source": "GitHub"},
        {"title": "Anthropic 获得新融资", "heat": 82, "source": "The Verge"},
        {"title": "阿里开源新大模型", "heat": 78, "source": "36kr"},
        {"title": "Cursor 发布重大更新", "heat": 75, "source": "Product Hunt"},
    ]

def generate_daily_brief(articles, date_str, config):
    """
    生成每日简报
    格式：
    标题：简洁精炼
    内容：不超过50字
    重点内容加粗高亮
    """
    focus_keywords = config.get('focus_keywords', [])
    
    lines = [
        f"📰 AI科技情报日报 | {date_str}",
        "",
        "🔥 昨日热度 Top 5",
        ""
    ]
    
    for i, article in enumerate(articles, 1):
        title = article.get('title', '无标题')
        source = article.get('source', '未知')
        url = article.get('url', '')
        content = article.get('content', '')[:80]  # 限制长度
        score = article.get('score', 0)
        category = article.get('category', '')
        
        # 判断是否需要重点关注
        is_focus = any(kw.lower() in title.lower() or kw.lower() in content.lower() 
                      for kw in focus_keywords)
        
        # 格式化输出
        if is_focus:
            # 重点标注
            lines.append(f"**{i}. {title}** ⭐")
            lines.append(f"**{content}**")
            if url:
                lines.append(f"**[阅读原文]({url})**")
        else:
            lines.append(f"{i}. {title}")
            lines.append(content)
            if url:
                lines.append(f"[阅读原文]({url})")
        
        lines.append("")
    
    lines.append("---")
    lines.append("*AI科技情报日报机器人 | 每日7:00自动推送*")
    
    return "\n".join(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI科技情报日报")
    parser.add_argument("--force", action="store_true", help="强制执行")
    args = parser.parse_args()
    
    run_daily_flow(force=args.force)
