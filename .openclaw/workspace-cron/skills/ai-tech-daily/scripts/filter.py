#!/usr/bin/env python3
"""
筛选模块 - 过滤和排序搜索结果
"""
import json
from datetime import datetime
from pathlib import Path

def filter_by_time(results, hours=24):
    """按时间筛选"""
    cutoff = datetime.now() - timedelta(hours=hours)
    return [r for r in results if r.get('published', datetime.now()) > cutoff]

def filter_by_quality(results, min_score=50):
    """按质量评分筛选"""
    return [r for r in results if r.get('score', 0) >= min_score]

def remove_duplicates(results):
    """去重 - 基于标题相似度"""
    seen = set()
    unique = []
    for r in results:
        title = r.get('title', '')
        # 简单的标题相似度检查
        key = title[:30].lower()
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique

def rank_by_importance(results):
    """按重要性排序"""
    # 综合评分：热度 + 时效 + 来源权威性
    return sorted(results, key=lambda x: x.get('score', 0), reverse=True)

def filter_all(raw_results, max_items=10):
    """
    执行完整筛选流程
    
    Returns:
        list: 筛选后的结果
    """
    results = raw_results
    results = filter_by_time(results)
    results = remove_duplicates(results)
    results = filter_by_quality(results)
    results = rank_by_importance(results)
    return results[:max_items]

if __name__ == "__main__":
    # 测试筛选逻辑
    test_data = [
        {"title": "Test 1", "score": 80},
        {"title": "Test 2", "score": 60},
        {"title": "Test 3", "score": 90},
    ]
    filtered = filter_all(test_data, max_items=2)
    print(f"筛选后: {len(filtered)} 条")
    for item in filtered:
        print(f"  - {item['title']} (score: {item['score']})")
