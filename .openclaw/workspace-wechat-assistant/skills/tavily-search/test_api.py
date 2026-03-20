#!/usr/bin/env python3
"""测试 Tavily API 连接"""

import sys
sys.path.insert(0, '/home/hochoy/.openclaw/workspace-wechat-assistant/skills/tavily-search/scripts')

from search import tavily_search, get_api_key

print("🔑 检查 API Key...")
api_key = get_api_key()
if api_key:
    print(f"✅ API Key 已配置: {api_key[:20]}...")
else:
    print("❌ API Key 未配置")
    sys.exit(1)

print("\n🔍 测试搜索...")
result = tavily_search("OpenClaw AI agent", max_results=3)

if result.get('error'):
    print(f"❌ 搜索失败: {result['error']}")
    sys.exit(1)

print("✅ 搜索成功!")
print(f"\n查询: {result['query']}")
print(f"结果数: {len(result.get('results', []))}")

if result.get('answer'):
    print(f"\n🤖 AI 答案:\n{result['answer'][:200]}...")

print("\n📚 搜索结果:")
for i, item in enumerate(result.get('results', [])[:3], 1):
    print(f"{i}. {item.get('title')} - {item.get('url')[:50]}...")
