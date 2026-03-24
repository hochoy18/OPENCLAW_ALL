#!/usr/bin/env python3
"""
生成模块 - 将筛选后的内容生成公众号推文
"""
import json
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent

def format_article(article, index):
    """格式化单篇文章"""
    title = article.get('title', '无标题')
    source = article.get('source', '未知来源')
    url = article.get('url', '#')
    summary = article.get('summary', '暂无摘要')
    
    return f"""### {index}. {title}
**来源**：{source} | **时间**：{article.get('time', '今日')}  
**摘要**：{summary}  
**链接**：[阅读原文]({url})

"""

def generate_draft(articles, date_str=None):
    """
    生成完整推文草稿
    
    Args:
        articles: 文章列表，按类别分组
        date_str: 日期字符串，默认今天
    
    Returns:
        str: Markdown 格式的推文
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y年%m月%d日")
    
    sections = []
    
    # 今日热点
    hot_articles = articles.get('hot', [])
    if hot_articles:
        sections.append("## 🔥 今日热点\n")
        for i, article in enumerate(hot_articles[:5], 1):
            sections.append(format_article(article, i))
    
    # AI Agent 动态
    agent_articles = articles.get('ai_agent', [])
    if agent_articles:
        sections.append("## 🤖 AI Agent 动态\n")
        for i, article in enumerate(agent_articles[:3], 1):
            sections.append(format_article(article, i))
    
    # 深度阅读
    deep_articles = articles.get('deep', [])
    if deep_articles:
        sections.append("## 💡 深度阅读\n")
        for i, article in enumerate(deep_articles[:2], 1):
            sections.append(format_article(article, i))
    
    content = f"""# AI科技情报日报 | {date_str}

{''.join(sections)}
---
*由 AI科技情报日报机器人 自动生成*
"""
    return content

def save_draft(content, date_str=None):
    """保存草稿到文件"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    output_dir = SKILL_DIR / "output" / date_str
    output_dir.mkdir(parents=True, exist_ok=True)
    
    draft_path = output_dir / "draft.md"
    draft_path.write_text(content, encoding='utf-8')
    return draft_path

if __name__ == "__main__":
    # 测试生成
    test_articles = {
        'hot': [
            {'title': 'OpenAI 发布 GPT-5', 'source': 'TechCrunch', 'url': '#', 'summary': '重磅更新...'},
        ],
        'ai_agent': [
            {'title': 'CrewAI 获融资', 'source': '36kr', 'url': '#', 'summary': '多Agent框架...'},
        ]
    }
    draft = generate_draft(test_articles)
    print(draft)
