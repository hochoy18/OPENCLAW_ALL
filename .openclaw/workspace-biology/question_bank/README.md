# 高中生物试题库

一个简洁高效的自用高中生物试题管理系统，支持题目导入、分类管理、智能搜索和组卷导出。

## 功能特性

- ✅ **多格式导入**：支持 Excel、Word (.docx)、JSON 格式批量导入题目
- ✅ **多维分类**：按难度、知识点、来源、题型分类管理
- ✅ **智能搜索**：支持关键词搜索和 AI 语义相似度搜索
- ✅ **灵活组卷**：按条件筛选题目，自由组成试卷
- ✅ **一键导出**：导出为 Word 试卷或 Excel 表格

## 安装

```bash
cd question_bank
pip install -r requirements.txt
```

## 快速开始

### 1. 启动应用

```bash
cd question_bank
streamlit run app.py
```

浏览器会自动打开 http://localhost:8501

### 2. 导入题目

**方式一：通过界面上传**
- 点击左侧菜单「📥 导入题目」
- 上传 Excel/Word/JSON 文件

**方式二：放置文件自动导入**
- 将文件放入 `data/uploads/` 目录

**Excel 格式要求**：

| 列 | 内容 | 说明 |
|---|---|---|
| A | 题干 | 必填 |
| B | 答案 | 选填 |
| C | 难度 | 1-5，选填，默认3 |
| D | 来源 | 选填 |
| E | 知识点 | 选填 |
| F | 关键词 | 选填 |
| G | 题型 | 选填 |

### 3. 搜索和筛选

- **题库浏览**：按难度、知识点、来源、题型筛选
- **关键词搜索**：搜索题目、知识点、关键词
- **语义搜索**：用自然语言描述，AI 找到相关题目

### 4. 组卷导出

1. 在「题库浏览」或「题目搜索」中勾选题目
2. 左侧显示已选题目数量
3. 进入「📤 导出试卷」设置试卷标题并导出

## 项目结构

```
question_bank/
├── app.py              # Streamlit 主应用
├── database.py         # SQLite 数据库操作
├── vector_store.py     # ChromaDB 向量存储
├── importer.py         # Excel/Word 导入器
├── exporter.py         # Word 导出器
├── requirements.txt    # Python 依赖
├── README.md           # 说明文档
└── data/
    ├── questions.db    # SQLite 数据库（自动创建）
    ├── chroma_db/      # 向量数据库（自动创建）
    ├── uploads/        # 上传文件目录
    └── exports/        # 导出文件目录
```

## 数据字段说明

| 字段 | 类型 | 说明 | 示例 |
|---|---|---|---|
| id | INTEGER | 题目唯一ID | 1 |
| title | TEXT | 题干 | 关于细胞呼吸的题目... |
| answer | TEXT | 答案 | B |
| difficulty | INTEGER | 难度1-5 | 3 |
| source | TEXT | 来源 | 学科网 |
| knowledge_point | TEXT | 知识点 | 光合作用 |
| keywords | TEXT | 关键词 | ATP,细胞呼吸 |
| question_type | TEXT | 题型 | 选择题/填空题/解答题 |
| created_at | TIMESTAMP | 创建时间 | 2024-01-01 10:00:00 |

## 使用示例

### 导入 Excel 题目

```python
import importer
import database
import vector_store

# 导入Excel
questions = importer.import_from_excel("sample_questions.xlsx")

# 存入数据库和向量库
for q in questions:
    q["text"] = q["title"] + " " + q.get("knowledge_point", "") + " " + q.get("keywords", "")
    qid = database.insert_question(**q)
    vector_store.add_question(qid, q["text"], q)
```

### 语义搜索

```python
results = vector_store.search_similar("关于光合作用和呼吸作用的综合题", top_k=5)
for r in results:
    print(r["question_id"], r["distance"])
```

### 导出试卷

```python
questions = [database.get_question_by_id(1), database.get_question_by_id(3)]
exporter.export_to_word(questions, "test_paper.docx", "第一章测试")
```

## 技术栈

- **数据库**：SQLite（轻量级，无需配置）
- **向量搜索**：ChromaDB（本地向量数据库）
- **前端**：Streamlit（Python Web 框架，无需前端知识）
- **文档处理**：python-docx、openpyxl

## 注意事项

1. 首次运行会自动创建数据库
2. 题目会同时存入 SQLite 和 ChromaDB
3. 语义搜索功能需要下载 sentence-transformers 模型（约 400MB）
4. 建议使用 Google Chrome 或 Microsoft Edge 浏览器

## 常见问题

**Q: 导入时提示"未找到题目"？**
A: 检查 Excel 文件是否有正确的表头，第一列应为"题干"

**Q: 语义搜索很慢？**
A: 首次使用需要下载模型，后续会缓存加速

**Q: 如何备份数据？**
A: 复制 `data/questions.db` 和 `data/chroma_db/` 目录即可
