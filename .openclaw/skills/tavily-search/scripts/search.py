#!/usr/bin/env python3
"""
Tavily AI 搜索引擎

支持功能：
- 高质量网络搜索
- AI 自动生成答案
- 深度搜索模式
- 多源信息整合
"""

import os
import sys
import json
import requests
from pathlib import Path


def load_config():
    """加载配置文件"""
    config = {}
    skill_dir = Path(__file__).parent.parent
    env_file = skill_dir / '.env'
    
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    
    return config


def get_api_key():
    """获取 Tavily API Key"""
    # 优先从环境变量获取
    api_key = os.environ.get('TAVILY_API_KEY')
    
    # 其次从配置文件获取
    if not api_key:
        config = load_config()
        api_key = config.get('TAVILY_API_KEY')
    
    return api_key


def tavily_search(
    query: str,
    search_depth: str = "basic",
    include_answer: bool = True,
    max_results: int = 5,
    include_domains: list = None,
    exclude_domains: list = None,
    include_images: bool = False
) -> dict:
    """
    使用 Tavily 进行 AI 搜索
    
    Args:
        query: 搜索查询词
        search_depth: 搜索深度 (basic/advanced)
        include_answer: 是否包含 AI 生成的答案
        max_results: 最大结果数 (1-20)
        include_domains: 指定包含的域名列表
        exclude_domains: 指定排除的域名列表
        include_images: 是否包含图片
    
    Returns:
        dict: 搜索结果
    """
    api_key = get_api_key()
    
    if not api_key:
        raise ValueError("缺少 Tavily API Key，请设置 TAVILY_API_KEY 环境变量或在 .env 文件中配置")
    
    url = "https://api.tavily.com/search"
    
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": search_depth,
        "include_answer": include_answer,
        "max_results": max_results,
        "include_images": include_images
    }
    
    # 可选参数
    if include_domains:
        payload["include_domains"] = include_domains
    if exclude_domains:
        payload["exclude_domains"] = exclude_domains
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        
        # 添加查询信息
        result['query'] = query
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"请求失败: {str(e)}",
            "query": query,
            "results": []
        }


def format_results(result: dict, verbose: bool = False) -> str:
    """格式化搜索结果为可读文本"""
    
    if result.get('error'):
        return f"❌ 错误: {result['error']}"
    
    output = []
    output.append("=" * 60)
    output.append(f"🔍 搜索: {result.get('query', 'Unknown')}")
    output.append("=" * 60)
    
    # AI 生成的答案
    if result.get('answer'):
        output.append("\n🤖 AI 回答:")
        output.append("-" * 60)
        output.append(result['answer'])
        output.append("")
    
    # 搜索结果
    results = result.get('results', [])
    if results:
        output.append(f"\n📚 找到 {len(results)} 个相关结果:")
        output.append("-" * 60)
        
        for i, item in enumerate(results, 1):
            title = item.get('title', '无标题')
            url = item.get('url', '')
            content = item.get('content', '')[:200]  # 限制摘要长度
            score = item.get('score', 0)
            
            output.append(f"\n{i}. {title}")
            output.append(f"   🔗 {url}")
            output.append(f"   📄 {content}...")
            if verbose:
                output.append(f"   ⭐ 相关度: {score:.2f}")
    
    output.append("\n" + "=" * 60)
    return "\n".join(output)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Tavily AI 搜索引擎')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--depth', choices=['basic', 'advanced'], default='basic',
                       help='搜索深度 (默认: basic)')
    parser.add_argument('--no-answer', action='store_true',
                       help='不包含 AI 生成的答案')
    parser.add_argument('--max-results', type=int, default=5,
                       help='最大结果数 (默认: 5)')
    parser.add_argument('--images', action='store_true',
                       help='包含图片')
    parser.add_argument('--json', action='store_true',
                       help='输出 JSON 格式')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='显示详细信息')
    
    args = parser.parse_args()
    
    # 执行搜索
    result = tavily_search(
        query=args.query,
        search_depth=args.depth,
        include_answer=not args.no_answer,
        max_results=args.max_results,
        include_images=args.images
    )
    
    # 输出结果
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_results(result, verbose=args.verbose))


if __name__ == '__main__':
    main()
