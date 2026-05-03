# AI Agent 理论速背教程

> 目标：快速掌握 AI Agent 核心概念，2-3 天背完，直接上手写代码。

---

## 一、LLM 本质（三句话）

> - 大模型 = 超级强大的"文字接龙"机器
> - 输入一段文字，输出最可能接下来出现的文字
> - 训练方式：海量文本 + 预测下一个词 + 人工反馈微调（RLHF）

---

## 二、Token 是什么

> - Token = 模型处理的最小单位
> - 1个中文词 ≈ 1.5-2 个 token
> - API 按 token 计费，不是按字数

---

## 三、Embedding 向量（必须背）

> - 任何文字 → 一串数字（向量）
> - **核心规律**：意思相近的文字 → 向量也相近
> - 向量距离近 = 语义相似
> - RAG 的根基就在这里

---

## 四、Prompt 工程三个黄金法则

1. **说清楚要什么** — 角色 + 任务 + 格式
2. **给例子** — Few-shot example 效果远超空说
3. **拆步骤** — 复杂任务拆成多步，比一步到位效果好

---

## 五、Agent 是什么（最核心的一句）

> **Agent = LLM + 工具 + 记忆 + 循环**
> - LLM 做大脑
> - 工具让 LLM 能操作世界（搜索、计算、读写文件）
> - 记忆让 LLM 记住之前的事
> - 循环让 Agent 能反复思考直到完成任务

---

## 六、Agent 四种核心能力

1. **感知** — 接收用户输入/环境信息
2. **推理** — 基于已有知识做判断（ReAct 模式：思考→行动→观察）
3. **行动** — 调用工具（搜索、API、代码执行）
4. **记忆** — 短期（对话历史）+ 长期（向量数据库）

---

## 七、RAG 是什么（面试必背）

> **RAG = 检索 + 增强生成**
> - 用户提问 → 从文档库检索相关段落 → 把段落 + 问题一起发给 LLM
> - 目的：让 LLM 能回答私有/最新数据的问题
> - 三步：切分 → Embedding → 检索 → 生成

---

## 八、向量数据库工作流

> **存**：文档 → 分块（chunk）→ Embedding → 存入向量库
> **查**：用户问题 → Embedding → 向量相似度搜索 → 返回 top-K 块
> **用**：把 K 个块 + 用户问题 → LLM → 生成回答

---

## 九、分块策略（Chunking）

> - 固定长度分块：简单但效果一般
> - 按段落/句子分块：效果更好
> - 块大小：一般 500-1000 token
> - 重叠：相邻块重叠 10-20%，防上下文断裂

---

## 十、多 Agent 协作模式

> - **层级模式**：一个 Agent 做调度，其他执行
> - **协作模式**：多个 Agent 各司其职，结果汇总
> - **对抗模式**：多个 Agent 互相审查、纠错

---

## 十一、ReAct 模式（Agent 推理核心）

> - **Re**ason：思考下一步该做什么
> - **Act**：执行某个工具
> - **Ob**serve：观察结果
> - 循环直到任务完成

---

## 十二、记忆的三层架构

> - **感官记忆**：当前对话的原始输入
> - **短期记忆**：最近 N 轮对话历史（一个滑动窗口）
> - **长期记忆**：向量数据库里持久化的内容

---

## 十三、Fine-tuning vs RAG（面试高频）

| | Fine-tuning | RAG |
|--|-----------|-----|
| 用途 | 改变模型行为/风格 | 让模型知道新知识 |
| 成本 | 高（重新训练） | 低（只改检索） |
| 实时性 | 低（知识固化在模型里） | 高（随时更新文档） |
| 选谁 | 想让模型"更像某个角色" | 想让模型"知道某些事" |

---

## 十四、评估 RAG 效果四个指标

1. **召回率** — 相关文档是否都被检索到了
2. **精确率** — 检索结果里有多少是真正相关的
3. **答案质量** — LLM 生成的回答是否准确
4. **上下文相关性** — 检索到的块是否恰好够回答问题

---

## 十五、LLM 推理优化常用方法

> - **量化**：FP16 → INT8 → INT4（用更少位数表示权重）
> - **Batching**：批量处理请求，提高 GPU 利用率
> - **KV Cache**：缓存已计算的 Key/Value，避免重复计算
> - **Streaming**：逐 token 返回，用户体验更好

---

## 十六、高频面试八股（速背）

### Q: Agent 和普通 LLM 调用的区别是什么？
> Agent 能通过工具与环境交互，能做多轮推理，能记住上下文。普通 LLM 只能根据当次输入生成输出。

### Q: RAG 效果不好怎么排查？
> - 检索不到相关内容 → 检查 Embedding 模型、chunk 大小
> - 检索到了但生成答非所问 → 检查 Prompt、上下文长度
> - 答案有遗漏 → 调高 top-K 数量

### Q: 什么时候用 RAG，什么时候用 Fine-tuning？
> 要让模型知道新知识 → RAG；要改变模型说话风格/行为 → Fine-tuning；两者也可以结合用。

### Q: 为什么需要向量数据库，直接用关键词搜索不行吗？
> 关键词搜索无法理解语义。比如"电脑死机了"和"计算机宕机"关键词不同但语义相同，向量检索能捕捉到这种相似性。

---

# 第二部分：快速上手指南

## 环境准备（半天搞定）

```bash
# Python 3.10+
python --version

# 创建虚拟环境
python -m venv agent-env
source agent-env/bin/activate  # Mac/Linux
# agent-env\Scripts\activate  # Windows

# 安装核心依赖
pip install langchain langchain-openai langchain-community
pip install chromadb  # 向量数据库
pip install crewai    # 多 Agent 框架
pip install fastapi uvicorn  # API 服务
pip install python-dotenv  # 环境变量管理
```

---

## 最小 RAG Demo（一天搞定）

```python
# 1. 准备知识库文件
# 创建 knowledge 目录，放入你的 .txt / .pdf / .docx 文件

# 2. 基础 RAG 流程代码
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# Step 1: 加载文档
loader = TextLoader("knowledge/你的文档.txt")
documents = loader.load()

# Step 2: 分块
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)

# Step 3: 转成向量存进 Chroma
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="db")

# Step 4: 构建检索+生成链
llm = ChatOpenAI(model="gpt-3.5-turbo")
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

# Step 5: 提问
question = "这份文档讲了什么？"
answer = qa_chain.run(question)
print(answer)
```

---

## 最小 Agent Demo（一天搞定）

```python
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_openai import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun

# 定义工具
search = DuckDuckGoSearchRun()

def calculator(expression: str) -> str:
    """执行简单计算"""
    return str(eval(expression))

tools = [
    Tool(name="搜索", func=search.run, description="用于搜索最新信息"),
    Tool(name="计算器", func=calculator, description="用于数学计算")
]

# 初始化 Agent
llm = ChatOpenAI(model="gpt-3.5-turbo")
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# 让 Agent 完成任务
agent.run("帮我查一下今天北京的天气，然后计算一下过去一周的平均气温是多少？")
```

---

## 最小多 Agent Demo（一天搞定）

```python
from crewai import Agent, Task, Crew

# 定义两个 Agent
researcher = Agent(
    role="研究员",
    goal="搜集准确的信息",
    backstory="你是一个专业的研究员，善于搜索和整理信息",
    verbose=True
)

writer = Agent(
    role="作家",
    goal="把信息写成易读的总结",
    backstory="你是一个专业的作家，擅长用简洁的语言写作",
    verbose=True
)

# 定义任务
task1 = Task(
    description="搜索并整理 AI Agent 的最新发展趋势",
    agent=researcher
)

task2 = Task(
    description="把研究员的发现写成一段 200 字的总结",
    agent=writer
)

# 启动 Crew（多 Agent 协作）
crew = Crew(agents=[researcher, writer], tasks=[task1, task2])
result = crew.kickoff()
print(result)
```

---

# 第三部分：整体学习路径

## 速成版（约 6-8 周，每天 6 小时）

```
📅 第1周：理论速背 + 搭环境
├─ 背完第一部分的 16 个核心概念
├─ 搭好 Python 环境 + 安装依赖
└─ 跑通上面的三个最小 Demo

📅 第2-3周：RAG 深度 + 知识库
├─ 深入 Chromadb / Milvus / Pinecone
├─ 高级 RAG：Query 改写、混合检索、重排序
├─ 多格式文档处理：PDF、Word、飞书文档
├─ 项目：给 OpenClaw 加上 RAG 知识库能力
└─ 输出：私有知识库问答 Agent

📅 第4周：Agent 记忆 + 工具
├─ 对话历史管理（短期记忆）
├─ 向量数据库持久化（长期记忆）
├─ 自定义工具开发
├─ 项目：给 Agent 加上"记忆所有对话"能力
└─ 输出：能记住用户偏好的个人助手

📅 第5-6周：多 Agent 协作
├─ CrewAI / AutoGen 深入
├─ 多 Agent 通信机制
├─ Agent 角色设计与任务分工
├─ 项目：多 Agent 客服系统
└─ 输出：能协作处理复杂问题的 Agent 团队

📅 第7-8周：工程化 + 部署
├─ FastAPI 封装 Agent 为服务
├─ Docker 镜像构建
├─ K8s 部署（结合你的 DevOps 优势）
├─ 监控与日志
└─ 输出：可生产部署的 Agent 服务
```

---

## 里程碑检查点

| 周数 | 应该达到的状态 |
|------|---------------|
| 第1周结束 | 能解释清楚 RAG 原理，跑通最小 Demo |
| 第2-3周结束 | 能独立搭 RAG 知识库，接入实际文档 |
| 第4周结束 | Agent 有记忆能力，不丢上下文 |
| 第5-6周结束 | 能做多 Agent 协作项目 |
| 第7-8周结束 | 能部署到 K8s，有实际项目可展示 |

---

## 推荐资源

### 视频课程
- B站：搜索 "LangChain 教程"、"RAG 实战"
- YouTube：CodingJon、James Briggs（LangChain 官方讲师）

### 文档
- LangChain 官方文档：https://python.langchain.com/docs/
- CrewAI 官方文档：https://docs.crewai.com/
- Chromadb 官方文档：https://docs.trychroma.com/

### 书籍
- 《Building AI Agents》— 目前最系统的 Agent 实战书
- 《Hands-On RAG》— RAG 专项实战

---

*背完理论、跑通 Demo，就是干！理论是骨架，实践是血肉。*
