#!/usr/bin/env python3
"""
搜索模块 - 使用 Tavily API 搜索资讯
"""
import json
import os
import requests
from pathlib import Path
from datetime import datetime, timedelta

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent

TAVILY_API_URL = "https://api.tavily.com/search"

def get_api_key():
    """获取 Tavily API Key"""
    # 优先从环境变量获取，其次从配置文件
    return os.environ.get('TAVILY_API_KEY', '')

def load_sources():
    """加载信源配置"""
    sources_path = SKILL_DIR / "sources.json"
    with open(sources_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def search_tavily(query, num_results=10, include_domains=None, days=1):
    """
    使用 Tavily API 搜索
    
    Args:
        query: 搜索关键词
        num_results: 返回结果数量 (max 20)
        include_domains: 限定域名白名单
        days: 搜索最近几天内的内容
    
    Returns:
        list: 搜索结果列表
    """
    api_key = get_api_key()
    if not api_key:
        print("❌ 未设置 TAVILY_API_KEY")
        return []
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "api_key": api_key,
        "query": query,
        "max_results": min(num_results, 20),
        "search_depth": "advanced",
        "include_answer": False,
        "include_raw_content": False
    }
    
    if include_domains:
        payload["include_domains"] = include_domains
    
    if days == 1:
        payload["time_range"] = "day"
    elif days == 7:
        payload["time_range"] = "week"
    elif days == 30:
        payload["time_range"] = "month"
    elif days == 365:
        payload["time_range"] = "year"
    
    try:
        response = requests.post(TAVILY_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"❌ Tavily API 请求失败: {e}")
        if hasattr(e.response, 'text'):
            print(f"   响应: {e.response.text}")
        return []

def search_category(category="ai_news", days=1, num_results=10):
    """
    搜索指定类别的资讯
    
    Args:
        category: 类别 (ai_news, ai_agent, tech)
        days: 时间范围（天）
        num_results: 返回结果数量
    
    Returns:
        list: 搜索结果列表
    """
    sources = load_sources()
    config = sources.get(category, {})
    domains = config.get("domains", [])
    keywords = config.get("keywords", [])
    
    print(f"🔍 搜索 {category}")
    print(f"   关键词: {keywords}")
    print(f"   信源: {domains}")
    print(f"   时间: 最近 {days} 天")
    
    all_results = []
    
    # 对每个关键词进行搜索
    for keyword in keywords[:2]:  # 限制关键词数量，避免过多请求
        query = f"{keyword} news"
        results = search_tavily(
            query=query,
            num_results=num_results,
            include_domains=domains,
            days=days
        )
        
        # 格式化结果
        for r in results:
            all_results.append({
                'title': r.get('title', '无标题'),
                'url': r.get('url', ''),
                'source': r.get('source', '未知'),
                'published': r.get('published_date', ''),
                'content': r.get('content', '')[:150] + '...' if r.get('content') else '',
                'score': r.get('score', 0)
            })
    
    # 按分数排序并去重
    all_results.sort(key=lambda x: x.get('score', 0), reverse=True)
    
    seen = set()
    unique_results = []
    for r in all_results:
        key = r['title'][:40]
        if key not in seen:
            seen.add(key)
            unique_results.append(r)
    
    print(f"   找到 {len(unique_results)} 条结果")
    return unique_results[:num_results]

def search_all(days=1):
    """搜索所有类别"""
    all_results = {}
    sources = load_sources()
    
    for category in sources.keys():
        results = search_category(category, days, num_results=5)
        all_results[category] = results
    
    return all_results

def verify_api_key():
    """验证 API Key 是否有效"""
    print("🔑 验证 Tavily API Key...")
    results = search_tavily("AI news", num_results=1)
    if results:
        print("✅ API Key 有效！")
        print(f"   测试搜索返回: {len(results)} 条结果")
        if results:
            print(f"   示例: {results[0].get('title', 'N/A')}")
        return True
    else:
        print("❌ API Key 验证失败")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", default="ai_news", help="搜索类别")
    parser.add_argument("--days", type=int, default=1, help="时间范围（天）")
    parser.add_argument("--num", type=int, default=10, help="结果数量")
    parser.add_argument("--verify", action="store_true", help="验证 API Key")
    args = parser.parse_args()
    
    if args.verify:
        verify_api_key()
    else:
        results = search_category(args.category, args.days, args.num)
        
        # 输出结果
        print("\n" + "="*50)
        for i, r in enumerate(results[:5], 1):
            print(f"\n{i}. {r['title']}")
            print(f"   来源: {r['source']}")
            print(f"   分数: {r.get('score', 'N/A')}")
            print(f"   链接: {r['url']}")
