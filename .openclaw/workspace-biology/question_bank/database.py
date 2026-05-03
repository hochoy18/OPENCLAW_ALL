"""
database.py - SQLite 数据库操作模块
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "questions.db")


def get_connection():
    """获取数据库连接"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库表"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            answer TEXT,
            difficulty INTEGER DEFAULT 3,
            source TEXT,
            knowledge_point TEXT,
            keywords TEXT,
            question_type TEXT DEFAULT '选择题',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def insert_question(
    title: str,
    answer: str = "",
    difficulty: int = 3,
    source: str = "",
    knowledge_point: str = "",
    keywords: str = "",
    question_type: str = "选择题"
) -> int:
    """插入一道题目，返回新题目ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO questions (title, answer, difficulty, source, knowledge_point, keywords, question_type, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (title, answer, difficulty, source, knowledge_point, keywords, question_type, datetime.now())
    )
    conn.commit()
    question_id = cursor.lastrowid
    conn.close()
    return question_id


def insert_questions_batch(questions: List[Dict]) -> int:
    """批量插入题目，返回插入数量"""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    data = [
        (
            q.get("title", ""),
            q.get("answer", ""),
            q.get("difficulty", 3),
            q.get("source", ""),
            q.get("knowledge_point", ""),
            q.get("keywords", ""),
            q.get("question_type", "选择题"),
            now
        )
        for q in questions
    ]
    cursor.executemany(
        """
        INSERT INTO questions (title, answer, difficulty, source, knowledge_point, keywords, question_type, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        data
    )
    conn.commit()
    count = cursor.rowcount
    conn.close()
    return count


def get_all_questions() -> List[Dict]:
    """获取所有题目"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_question_by_id(question_id: int) -> Optional[Dict]:
    """根据ID获取题目"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def search_questions(
    keyword: str = None,
    difficulty: int = None,
    knowledge_point: str = None,
    source: str = None,
    question_type: str = None,
    limit: int = 100
) -> List[Dict]:
    """多条件搜索题目"""
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = "SELECT * FROM questions WHERE 1=1"
    params = []
    
    if keyword:
        sql += " AND (title LIKE ? OR keywords LIKE ? OR knowledge_point LIKE ?)"
        params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
    
    if difficulty is not None:
        sql += " AND difficulty = ?"
        params.append(difficulty)
    
    if knowledge_point:
        sql += " AND knowledge_point LIKE ?"
        params.append(f"%{knowledge_point}%")
    
    if source:
        sql += " AND source LIKE ?"
        params.append(f"%{source}%")
    
    if question_type:
        sql += " AND question_type = ?"
        params.append(question_type)
    
    sql += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_all_knowledge_points() -> List[str]:
    """获取所有知识点（去重）"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT knowledge_point 
        FROM questions 
        WHERE knowledge_point IS NOT NULL AND knowledge_point != ''
        ORDER BY knowledge_point
    """)
    rows = cursor.fetchall()
    conn.close()
    return [row["knowledge_point"] for row in rows]


def get_all_sources() -> List[str]:
    """获取所有来源（去重）"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT source 
        FROM questions 
        WHERE source IS NOT NULL AND source != ''
        ORDER BY source
    """)
    rows = cursor.fetchall()
    conn.close()
    return [row["source"] for row in rows]


def get_all_question_types() -> List[str]:
    """获取所有题型（去重）"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT question_type 
        FROM questions 
        WHERE question_type IS NOT NULL AND question_type != ''
        ORDER BY question_type
    """)
    rows = cursor.fetchall()
    conn.close()
    return [row["question_type"] for row in rows]


def delete_question(question_id: int) -> bool:
    """删除题目"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def update_question(question_id: int, **kwargs) -> bool:
    """更新题目"""
    allowed_fields = ["title", "answer", "difficulty", "source", "knowledge_point", "keywords", "question_type"]
    updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
    
    if not updates:
        return False
    
    conn = get_connection()
    cursor = conn.cursor()
    set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
    sql = f"UPDATE questions SET {set_clause} WHERE id = ?"
    cursor.execute(sql, list(updates.values()) + [question_id])
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def get_statistics() -> Dict:
    """获取统计信息"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM questions")
    total = cursor.fetchone()["total"]
    
    cursor.execute("SELECT COUNT(DISTINCT knowledge_point) as kp_count FROM questions WHERE knowledge_point IS NOT NULL AND knowledge_point != ''")
    kp_count = cursor.fetchone()["kp_count"]
    
    cursor.execute("SELECT COUNT(DISTINCT source) as source_count FROM questions WHERE source IS NOT NULL AND source != ''")
    source_count = cursor.fetchone()["source_count"]
    
    cursor.execute("SELECT question_type, COUNT(*) as count FROM questions GROUP BY question_type")
    type_dist = {row["question_type"]: row["count"] for row in cursor.fetchall()}
    
    conn.close()
    
    return {
        "total": total,
        "knowledge_point_count": kp_count,
        "source_count": source_count,
        "type_distribution": type_dist
    }


# 初始化数据库
init_db()
