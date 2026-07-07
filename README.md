# Agentic RAG 求职助手

基于 **LangGraph 多智能体协作** + **RAG 检索增强生成**的 AI 求职助手。支持简历/JD 智能解析、岗位匹配度分析、AI 模拟面试，全链路 SSE 实时反馈。

## 架构概览

```
用户 → Vue 3 前端 → FastAPI 后端 → LangGraph Agent 编排
                                      ├─ Classify（意图分类）
                                      ├─ Plan（检索规划）
                                      ├─ Search（多工具检索）
                                      ├─ Fuse（结果去重融合）
                                      ├─ Reflect（4维度反思）← 循环最多3轮
                                      └─ Generate（生成报告）
                       ↓
              ChromaDB（向量检索）
              Tavily（网络搜索）
              DeepSeek V4 Pro（LLM）
              SiliconFlow Embedding（向量化）
```

## 功能

- **简历/JD 解析入库**：支持 PDF/DOCX/TXT，语义分块后向量化存入 ChromaDB
- **岗位匹配分析**：Agent 自主检索 + 反思迭代，输出评分、技能对比、技能缺口、改进建议、面试准备清单
- **AI 模拟面试**：多维度面试题生成 + 实时回答评估 + 面试报告（薄弱环节 & 学习计划）
- **SSE 实时进度**：4 种事件类型（progress/thinking/result/done），Agent 思考过程可视化

## 技术栈

| 层级 | 技术 |
|------|------|
| **Agent 框架** | LangGraph StateGraph（6 节点 + 条件边） |
| **后端** | Python 3.14 + FastAPI + SSE |
| **前端** | Vue 3 + Vite + TypeScript |
| **向量数据库** | ChromaDB（4 个 Collection） |
| **LLM** | DeepSeek V4 Pro |
| **Embedding** | SiliconFlow Qwen3-Embedding-0.6B（1024维） |
| **搜索引擎** | Tavily Search API |
| **文档解析** | PyMuPDF（PDF）+ python-docx（DOCX） |

## 快速开始

### 1. 安装依赖

```bash
# 后端
cd backend
poetry install

# 前端
cd frontend
npm install
```

### 2. 配置环境变量

在 `backend/.env` 中填入 API Key：

```env
DEEPSEEK_API_KEY=你的DeepSeek_API_Key
DEEPSEEK_BASE_URL=https://api.deepseek.com
TAVILY_API_KEY=你的Tavily_API_Key
EMBEDDING_API_KEY=你的SiliconFlow_API_Key
EMBEDDING_BASE_URL=https://api.siliconflow.cn/v1
```

### 3. 启动服务

```bash
# 启动后端（端口 8000）
cd backend
poetry run uvicorn src.main:app --port 8000 --reload

# 启动前端（端口 5173）
cd frontend
npm run dev
```

打开 http://localhost:5173 使用。

## 项目结构

```
├── backend/
│   ├── src/
│   │   ├── agent/          # LangGraph Agent 编排
│   │   │   ├── graph.py    # 6节点 StateGraph
│   │   │   ├── state.py    # Agent 状态定义
│   │   │   ├── tools.py    # 5个 Agent 工具
│   │   │   ├── reflection.py  # 4维度反思
│   │   │   └── prompts.py  # Prompt 模板
│   │   ├── api/            # FastAPI 路由
│   │   │   ├── match.py    # 匹配分析 + SSE 流
│   │   │   ├── interview.py # 模拟面试
│   │   │   ├── resume.py   # 简历上传
│   │   │   └── jd.py       # JD 上传
│   │   ├── services/       # 核心服务
│   │   │   ├── vectordb.py # ChromaDB 向量存储
│   │   │   ├── embeddings.py # 向量化
│   │   │   ├── parser.py   # 文档解析
│   │   │   └── chunker.py  # 语义分块
│   │   ├── models/         # Pydantic 数据模型
│   │   └── config.py       # 配置管理
│   └── tests/              # 测试
├── frontend/
│   └── src/
│       ├── components/     # 12个Vue组件
│       ├── pages/          # 4个页面路由
│       ├── composables/    # SSE流式消费Hook
│       └── api/            # API 客户端
└── README.md
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/resume/upload` | 上传简历 |
| POST | `/api/jd/upload` | 上传 JD |
| POST | `/api/match` | 创建匹配任务 |
| GET | `/api/match/{id}/stream` | SSE 流式获取匹配结果 |
| GET | `/api/match/{id}/report` | 获取匹配报告 |
| POST | `/api/interview/start` | 开始模拟面试 |
| POST | `/api/interview/{id}/answer` | 提交面试回答 |
| GET | `/api/interview/{id}/report` | 获取面试报告 |

## License

MIT
