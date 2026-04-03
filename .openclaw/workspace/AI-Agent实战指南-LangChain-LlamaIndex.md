# AI Agent 实战指南：LangChain + LlamaIndex

> 目标：能够跑通 Agent + RAG 的最小可用 Demo，理解每个环节的代码逻辑。

---

## 一、环境准备

### 1.1 依赖安装

```bash
# Python 3.10+
python --version

# 创建虚拟环境
python -m venv agent-env
source agent-env/bin/activate  # Mac/Linux
# agent-env\Scripts\activate  # Windows

# 安装核心依赖（注意版本，避免兼容性）
pip install \
  langchain langchain-core langchain-community \
  langchain-openai \
  llama-index llama-index-core llama-index-llms-openai \
  chromadb \
  openai \
  python-dotenv \
  tiktoken  # token计数
```

### 1.2 环境变量配置

创建 `.env` 文件：

```bash
# .env
OPENAI_API_KEY=sk-xxxxx  # 你的 API Key
OPENAI_BASE_URL=https://api.openai.com/v1  # 默认，可选国内代理
```

> ⚠️ 如果用国内模型（如硅基流动），修改 `OPENAI_BASE_URL` 为对应地址。

---

## 二、最小 RAG Demo（LlamaIndex 写法）

> 用 LlamaIndex 的原因是它比 LangChain 更专注 RAG 场景，API 更简洁。

### 2.1 完整代码

```python
# 01_minimal_rag.py
import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.openai import OpenAI

# 加载环境变量
load_dotenv()

# Step 1: 加载文档（支持 txt/pdf/docx）
documents = SimpleDirectoryReader("./knowledge").load_data()

# Step 2: 构建索引
index = VectorStoreIndex.from_documents(documents)

# Step 3: 获取检索器和查询引擎
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=3  # 召回 Top-3
)
query_engine = RetrieverQueryEngine.from_args(
    retriever=retriever,
    llm=OpenAI(model="gpt-3.5-turbo")
)

# Step 4: 提问
response = query_engine.query("这份文档讲了什么？")
print(response)
```

### 2.2 目录结构

```
project/
├── .env
├── 01_minimal_rag.py
└── knowledge/          # 放你的文档
    ├── 文档1.txt
    └── 文档2.pdf
```

### 2.3 运行

```bash
# 先创建测试文档
mkdir -p knowledge
echo "AI Agent 是大模型 + 工具 + 记忆 + 循环的结合体。" > knowledge/test.txt

# 运行
python 01_minimal_rag.py
```

---

## 三、分步骤解析 RAG 流程

### 3.1 文档加载（Loading）

```python
from llama_index.core import SimpleDirectoryReader

# 支持多种格式
documents = SimpleDirectoryReader(
    "./knowledge",
    recursive=True,  # 递归遍历子目录
    exclude_hidden=True,  # 排除隐藏文件
).load_data()

print(f"加载了 {len(documents)} 个文档")
```

**LlamaIndex 支持的格式：**

| 格式 | 是否支持 | 需要额外库 |
|-----|---------|-----------|
| TXT | ✅ 原生 | - |
| PDF | ✅ 原生 | - |
| DOCX | ✅ | python-docx |
| Markdown | ✅ | - |
| CSV | ✅ | pandas |
| Web | ✅ | playwright |

### 3.2 文档分块（Chunking / Splitting）

```python
from llama_index.core.node_parser import SentenceSplitter

# 按句子分块，效果比固定长度好
node_parser = SentenceSplitter(
    chunk_size=500,      # 每块 token 数
    chunk_overlap=50,     # 块之间重叠，防止语义断裂
)

# 把文档分成节点
nodes = node_parser.get_nodes_from_documents(documents)

print(f"分成了 {len(nodes)} 个块")
```

**分块策略对比：**

```python
# 固定长度（不推荐）
from llama_index.core.node_parser import TokenTextSplitter
splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=50)

# 按句子（推荐）
from llama_index.core.node_parser import SentenceSplitter
splitter = SentenceSplitter(chunk_size=500, chunk_overlap=50)

# 递归字符分割（最通用）
from llama_index.core.node_parser import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "！", "？", " "],
    chunk_size=500,
    chunk_overlap=50
)
```

### 3.3 Embedding 和存储（Embedding + Indexing）

```python
from llama_index.core import VectorStoreIndex
from llama_index.core.storage import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

# 方式1：用内存向量库（简单，快速，但重启丢数据）
index = VectorStoreIndex.from_documents(documents)

# 方式2：用 Chroma 向量库（持久化存储）
chroma_client = chromadb.PersistentClient(path="./chroma_db")
vector_store = ChromaVectorStore(chroma_client=chroma_client, collection_name="my_kb")

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    show_progress=True  # 显示进度条
)

# 保存索引（方便下次直接加载）
index.storage_context.persist("./index_store")
```

### 3.4 检索（Retrieval）

```python
from llama_index.core.retrievers import VectorIndexRetriever

# 配置检索器
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=3,      # 召回 Top-K
    # 可选：过滤条件
    # filters=MetadataFilters(...),
)

# 测试检索
results = retriever.retrieve("AI Agent 是什么？")
for i, node in enumerate(results):
    print(f"结果 {i+1}，相似度得分：{results[i].get('score', 'N/A')}")
    print(f"内容：{node.text[:100]}...")
```

### 3.5 生成（Generation）

```python
from llama_index.core import QueryBundle
from llama_index.core.query_engine import RetrieverQueryEngine

# 构建查询引擎（检索+生成）
query_engine = RetrieverQueryEngine.from_args(
    retriever=retriever,
    llm=OpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,  # 创造性 0-1
        max_tokens=500,    # 最大生成 token 数
    ),
    # 可选：生成参数
    # response_mode="compact",  # compact 把检索结果压缩再生成
    # response_mode="refine",   # refine 迭代优化答案
)

# 提问
response = query_engine.query("AI Agent 的核心是什么？")
print(response)
```

---

## 四、最小 Agent Demo（LangChain 写法）

> LangChain 的优势是 Agent 生态更成熟，工具集成更丰富。

### 4.1 完整代码

```python
# 02_minimal_agent.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.tools import DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper

load_dotenv()

# 初始化 LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
)

# 定义工具
tools = [
    Tool(
        name="搜索",
        func=DuckDuckGoSearchRun().run,
        description="当你需要搜索最新信息时使用，输入搜索关键词，返回搜索结果。"
    ),
    Tool(
        name="维基百科",
        func=WikipediaAPIWrapper().run,
        description="当你需要查询百科知识时使用，输入问题，返回简要答案。"
    ),
]

# 初始化 Agent（ReAct 模式）
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # ReAct 模式
    verbose=True,  # 显示推理过程
    handle_parsing_errors=True,  # 解析错误自动处理
)

# 让 Agent 完成任务
result = agent.invoke("搜索今天北京的天气，然后结合维基百科解释为什么北京冬季干燥。")
print(result)
```

### 4.2 运行

```bash
# 安装额外依赖
pip install wikipedia-api

python 02_minimal_agent.py
```

### 4.3 输出示例

```
> Entering new AgentExecutor chain...
 I need to find out the current weather in Beijing today.
Action: 搜索
Action Input: 北京今天天气
Observation: 今天北京晴，12-18℃，空气质量良。
 I now know the current weather in Beijing today.
 I need to find information about why Beijing is dry in winter.
Action: 维基百科
Action Input: 北京冬季干燥原因
Observation: 北京属于温带季风气候，冬季受西伯利亚高压影响...
 I now know why Beijing is dry in winter.
Finish: 北京今天天气晴朗...
```

---

## 五、自定义工具开发

### 5.1 基础工具模板

```python
from langchain.tools import tool
from langchain_core.tools import StructuredTool

# 方式1：简单工具（无参数）
@tool
def get_current_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 方式2：带参数的工具（Pydantic 格式）
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    city: str = Field(description="城市名称")

@tool(args_schema=WeatherInput)
def get_weather(city: str) -> str:
    """查询城市天气"""
    # 这里可以是真实 API 调用
    return f"{city}今天晴，15-22℃"

# 方式3：StructuredTool（更灵活）
def calculate(expression: str) -> str:
    """执行数学计算"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"计算错误: {e}"

calculator = StructuredTool.from_function(
    name="计算器",
    func=calculate,
    description="用于数学计算，支持加减乘除和括号",
)
```

### 5.2 完整 Agent 示例（带多个自定义工具）

```python
# 03_custom_tools_agent.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.tools import tool
from pydantic import BaseModel, Field

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 工具1：天气查询
@tool
def get_weather(city: str) -> str:
    """查询城市天气"""
    weathers = {"北京": "晴 15-22℃", "上海": "雨 18-25℃", "深圳": "多云 25-30℃"}
    return weathers.get(city, f"{city}天气未知")

# 工具2：计算器
@tool
def calculate(expression: str) -> str:
    """执行数学计算"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"错误: {e}"

# 工具3：记事本
notes = {}

@tool
def save_note(key: str, value: str) -> str:
    """保存笔记"""
    notes[key] = value
    return f"已保存: {key} = {value}"

@tool
def get_note(key: str) -> str:
    """读取笔记"""
    return notes.get(key, f"未找到: {key}")

# 组合工具
tools = [get_weather, calculate, save_note, get_note]

# 初始化 Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# 测试
if __name__ == "__main__":
    # 测试1：查天气
    print("=== 测试1：查天气 ===")
    agent.invoke("北京今天天气怎么样？")

    # 测试2：计算
    print("\n=== 测试2：计算 ===")
    agent.invoke("计算 (100 + 200) * 3 / 10 等于多少？")

    # 测试3：记事
    print("\n=== 测试3：记事 ===")
    agent.invoke("帮我记一下：项目代号是 Alpha")
    agent.invoke("读取刚才记的内容")
```

---

## 六、RAG + Agent 结合（高级版）

> 让 Agent 在回答问题时，先检索知识库，再生成。

### 6.1 架构图

```
用户问题
    ↓
Agent 规划
    ↓
调用 RAG 检索工具 → 知识库（向量库）
    ↓
返回相关文档
    ↓
Agent 结合文档生成回答
```

### 6.2 完整代码

```python
# 04_rag_agent.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, Tool
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.retrievers import VectorIndexRetriever

load_dotenv()

# ===== 准备知识库 =====
documents = SimpleDirectoryReader("./knowledge").load_data()
index = VectorStoreIndex.from_documents(documents)
retriever = VectorIndexRetriever(index=index, similarity_top_k=3)

# ===== 自定义 RAG 检索工具 =====
def rag_search(query: str) -> str:
    """从知识库检索相关信息"""
    results = retriever.retrieve(query)
    if not results:
        return "知识库中没有找到相关信息"
    
    context = "\n\n".join([f"【文档{i+1}】{r.text}" for i, r in enumerate(results)])
    return f"检索到 {len(results)} 条相关信息：\n\n{context}"

# ===== 初始化 LLM 和 Agent =====
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

tools = [
    Tool(
        name="知识库检索",
        func=rag_search,
        description="当你需要回答关于知识库内容的问题时使用，输入是搜索查询。"
    ),
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# ===== 测试 =====
if __name__ == "__main__":
    print("=== RAG + Agent 测试 ===")
    agent.invoke("你们公司的产品有哪些？")
```

### 6.3 目录结构

```
project/
├── .env
├── 04_rag_agent.py
└── knowledge/          # 你的知识库文档
    └── 产品介绍.txt     # "我们的产品包括：AI助手、智能客服、数据分析平台..."
```

---

## 七、多 Agent 协作（CrewAI）

### 7.1 安装

```bash
pip install crewai crewai-tools
```

### 7.2 完整代码

```python
# 05_multi_agent.py
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

load_dotenv()

# ===== 定义 Agent =====

researcher = Agent(
    role="研究员",
    goal="从可靠来源搜集准确信息",
    backstory="你是一个专业的研究员，擅长搜索和整理信息",
    verbose=True,
    allow_delegation=False,  # 不委托给其他人
)

writer = Agent(
    role="作家",
    goal="把信息写成易读的总结",
    backstory="你是一个专业的作家，擅长用简洁有趣的语言写作",
    verbose=True,
    allow_delegation=False,
)

reviewer = Agent(
    role="审核员",
    goal="检查文章是否准确、完整、易读",
    backstory="你是一个严格的编辑，专注于质量和准确性",
    verbose=True,
    allow_delegation=False,
)

# ===== 定义 Task =====

task1 = Task(
    description="研究 AI Agent 的最新发展趋势，输出 200 字的研究报告",
    agent=researcher,
    expected_output="包含3-5个要点的研究报告",
)

task2 = Task(
    description="把研究报告扩展成一篇 500 字的文章",
    agent=writer,
    expected_output="结构清晰、语言流畅的文章",
    context=[task1],  # 依赖 task1 的输出
)

task3 = Task(
    description="审核文章，检查准确性和可读性，给出修改建议",
    agent=reviewer,
    expected_output="修改建议列表",
    context=[task2],  # 依赖 task2 的输出
)

# ===== 启动 Crew =====
crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[task1, task2, task3],
    process="sequential",  # 顺序执行（还有 hierarchical）
    verbose=True,
)

result = crew.kickoff()
print("\n=== 最终输出 ===")
print(result)
```

### 7.3 运行

```bash
python 05_multi_agent.py
```

---

## 八、生产环境注意事项

### 8.1 常见错误与排查

| 错误 | 原因 | 解决 |
|-----|------|------|
| `AuthenticationError` | API Key 错误/过期 | 检查 `.env` 和 API Key 有效性 |
| `RateLimitError` | 请求太快，被限流 | 加 `tiktoken` 计费，加 `time.sleep` 限速 |
| `IndexError: list index out of range` | 检索不到结果 | 检查文档是否加载成功，调整 `similarity_top_k` |
| `json.decoder.JSONDecodeError` | LangChain 输出解析失败 | 开启 `handle_parsing_errors=True` |

### 8.2 成本控制

```python
# 方案1：加 Token 计数
import tiktoken

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

# 方案2：加限速
import time
def rate_limited_call(func, *args, delay=1.0, **kwargs):
    time.sleep(delay)
    return func(*args, **kwargs)
```

### 8.3 上下文长度管理

```python
# 检查 token 数，避免超过模型上限
MAX_TOKENS = 6000  # GPT-3.5 约 4K 输出上限

def truncate_text(text: str, max_tokens: int = MAX_TOKENS) -> str:
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = enc.encode(text)
    if len(tokens) > max_tokens:
        return enc.decode(tokens[:max_tokens])
    return text
```

### 8.4 持久化索引（避免重复构建）

```python
import os
from llama_index.core import load_index_from_storage, StorageContext

INDEX_PATH = "./index_store"

def get_index():
    """获取索引，不存在则创建"""
    if os.path.exists(f"{INDEX_PATH}/default__vector_store.json"):
        # 从磁盘加载
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_PATH)
        return load_index_from_storage(storage_context)
    else:
        # 创建新索引
        documents = SimpleDirectoryReader("./knowledge").load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(INDEX_PATH)
        return index
```

---

## 九、完整项目模板

```
project/
├── .env                        # API Key
├── requirements.txt            # 依赖列表
├── knowledge/                  # 知识库文档
│   ├── 公司介绍.txt
│   └── 产品手册.pdf
├── index_store/                # 持久化的向量索引
├── chroma_db/                  # Chroma 向量库
├── 01_minimal_rag.py          # 最小 RAG Demo
├── 02_minimal_agent.py        # 最小 Agent Demo
├── 03_custom_tools_agent.py   # 自定义工具 Agent
├── 04_rag_agent.py            # RAG + Agent
├── 05_multi_agent.py          # 多 Agent 协作
└── utils.py                   # 工具函数
```

### `requirements.txt`

```
langchain>=0.1.0
langchain-openai>=0.0.5
langchain-community>=0.0.10
llama-index>=0.9.0
llama-index-core>=0.9.0
llama-index-llms-openai>=0.1.0
chromadb>=0.4.0
openai>=1.0.0
python-dotenv>=1.0.0
tiktoken>=0.5.0
crewai>=0.1.0
crewai-tools>=0.1.0
wikipedia-api>=0.6.0
```

---

## 十、学习路线建议

```
📅 第1天：跑通最小 Demo
├─ 搭好环境（Python 3.10+、虚拟环境、API Key）
├─ 跑通 01_minimal_rag.py
└─ 跑通 02_minimal_agent.py

📅 第2-3天：深入 RAG 流程
├─ 理解分块策略（固定长度 vs 句子 vs 递归）
├─ 尝试不同 Embedding 模型
├─ 学会持久化索引
└─ 跑通 04_rag_agent.py

📅 第4-5天：Agent 进阶
├─ 自定义工具开发
├─ 多工具组合
├─ 理解 ReAct 模式（看 verbose 输出）
└─ 多 Agent 协作（CrewAI）

📅 第6-7天：生产环境
├─ 加错误处理
├─ 加 Token 计费
├─ 学会排查常见错误
└─ 部署到服务器
```

---

*跑通 Demo 是第一步，理解每个环节"为什么这样做"才是关键。*
