"""
vector_store.py - ChromaDB 向量存储模块
"""

import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "data", "chroma_db")

# 全局客户端
_client = None
_collection = None


def get_client():
    """获取ChromaDB客户端"""
    global _client
    if _client is None:
        os.makedirs(CHROMA_PATH, exist_ok=True)
        _client = chromadb.PersistentClient(path=CHROMA_PATH)
    return _client


def get_collection():
    """获取题目集合"""
    global _collection
    if _collection is None:
        client = get_client()
        _collection = client.get_or_create_collection(
            name="questions",
            metadata={"description": "高中生物试题向量库"}
        )
    return _collection


def add_question(question_id: int, text: str, metadata: Dict = None):
    """添加题目到向量库"""
    collection = get_collection()
    
    # 构建元数据
    meta = metadata or {}
    meta["question_id"] = str(question_id)
    
    collection.add(
        ids=[str(question_id)],
        documents=[text],
        metadatas=[meta]
    )


def add_questions_batch(questions: List[Dict]):
    """批量添加题目到向量库"""
    collection = get_collection()
    
    ids = [str(q["id"]) for q in questions]
    texts = [q["text"] for q in questions]
    metadatas = []
    
    for q in questions:
        meta = {
            "question_id": str(q["id"]),
            "title": q.get("title", "")[:500],
            "difficulty": q.get("difficulty", 3),
            "knowledge_point": q.get("knowledge_point", ""),
            "source": q.get("source", ""),
            "question_type": q.get("question_type", ""),
        }
        metadatas.append(meta)
    
    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas
    )


def search_similar(query: str, top_k: int = 5, filters: Dict = None) -> List[Dict]:
    """语义搜索相似题目"""
    collection = get_collection()
    
    # 构建查询条件
    where_filter = None
    if filters:
        where_filter = {}
        if filters.get("difficulty") is not None:
            where_filter["difficulty"] = filters["difficulty"]
        if filters.get("knowledge_point"):
            where_filter["knowledge_point"] = {"$contains": filters["knowledge_point"]}
        if filters.get("question_type"):
            where_filter["question_type"] = filters["question_type"]
    
    try:
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
            where=where_filter if where_filter else None,
            include=["documents", "metadatas", "distances"]
        )
        
        similar = []
        if results["ids"] and len(results["ids"]) > 0:
            for i, qid in enumerate(results["ids"][0]):
                similar.append({
                    "question_id": int(qid),
                    "distance": results["distances"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "document": results["documents"][0][i]
                })
        
        return similar
    except Exception as e:
        print(f"搜索出错: {e}")
        return []


def delete_question(question_id: int):
    """从向量库删除题目"""
    collection = get_collection()
    try:
        collection.delete(ids=[str(question_id)])
    except Exception as e:
        print(f"删除向量出错: {e}")


def get_vector_count() -> int:
    """获取向量库中的题目数量"""
    collection = get_collection()
    return collection.count()


def rebuild_index():
    """重建向量索引（从数据库同步）"""
    global _collection
    _collection = None
    
    # 删除旧集合
    client = get_client()
    try:
        client.delete_collection("questions")
    except:
        pass
    
    # 重新创建
    get_collection()
