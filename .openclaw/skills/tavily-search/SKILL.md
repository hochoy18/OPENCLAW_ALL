---
name: tavily-search
description: Tavily AI 搜索引擎，支持深度搜索、新闻搜索、问答搜索。Use when user needs to search the web, find recent information, research topics, or get AI-powered search results with sources.
---

# Tavily 智能搜索

使用 Tavily AI 搜索引擎进行高质量网络搜索。

## 功能特性

- **深度搜索**: 获取详细、准确的搜索结果
- **AI 问答**: 自动生成带引用来源的答案
- **新闻搜索**: 获取最新资讯
- **多源整合**: 从多个可靠来源获取信息

## 使用方法

### 命令行搜索

```bash
# 基础搜索
python3 scripts/search.py "人工智能最新发展趋势"

# 深度搜索
python3 scripts/search.py "量子计算原理" --depth advanced

# 获取带答案的搜索结果
python3 scripts/search.py "什么是大语言模型" --include-answer

# 限制结果数量
python3 scripts/search.py "Python 教程" --max-results 10
```

### Python API

```python
from scripts.search import tavily_search

# 基础搜索
results = tavily_search("人工智能最新发展趋势")

# 高级搜索
results = tavily_search(
    query="量子计算",
    search_depth="advanced",
    include_answer=True,
    max_results=10
)

print(results['answer'])  # AI 生成的答案
print(results['results'])  # 搜索结果列表
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query | string | 必填 | 搜索关键词 |
| search_depth | string | basic | 搜索深度: basic / advanced |
| include_answer | bool | true | 是否包含 AI 生成的答案 |
| max_results | int | 5 | 返回结果数量 (1-20) |
| include_domains | list | None | 指定搜索域名 |
| exclude_domains | list | None | 排除搜索域名 |

## 响应格式

```json
{
  "answer": "AI 生成的综合答案",
  "query": "原始搜索词",
  "results": [
    {
      "title": "结果标题",
      "url": "链接地址",
      "content": "内容摘要",
      "score": 0.95
    }
  ],
  "response_time": 2.34
}
```

## 配置

API Key 已配置在 `.env` 文件中：
- `TAVILY_API_KEY` - Tavily API 密钥

## 使用示例

### 示例 1：快速搜索
```python
from scripts.search import tavily_search

result = tavily_search("2024年 AI 发展趋势")
print(result['answer'])
```

### 示例 2：深度研究
```python
result = tavily_search(
    query="新能源汽车市场前景分析",
    search_depth="advanced",
    max_results=10
)

for item in result['results']:
    print(f"- {item['title']}: {item['url']}")
```

### 示例 3：新闻搜索
```python
result = tavily_search(
    query="最新科技新闻",
    search_depth="advanced",
    include_answer=True
)
```
