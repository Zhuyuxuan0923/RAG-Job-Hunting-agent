# Agentic RAG 求职助手

基于 **LangGraph Agent 编排** 与 **RAG 检索增强生成** 的 AI 求职助手。系统支持简历/JD 上传解析、岗位匹配度分析、SSE 实时进度反馈、AI 模拟面试和面试报告生成，帮助求职者更高效地判断岗位匹配度并准备面试。

![项目首页截图](docs/assets/upload-page-desktop.png)

## 核心功能

- **简历/JD 上传解析**：支持 PDF、DOCX、DOC 等文件上传，自动解析文本并进行语义分块。
- **岗位匹配分析**：基于简历、职位描述、向量检索和网络搜索，生成匹配评分、技能缺口和准备建议。
- **Agent 反思迭代**：通过 LangGraph 编排意图分类、检索规划、多源检索、融合去重、反思补查和报告生成。
- **SSE 实时反馈**：分析过程通过 `progress`、`thinking`、`result`、`done` 等事件流式返回。
- **AI 模拟面试**：根据简历和 JD 生成面试题，评估用户回答，并输出面试报告与学习计划。

## 技术栈

| 模块 | 技术 |
| --- | --- |
| 前端 | Vue 3、Vite、TypeScript、Vue Router |
| 后端 | Python 3.11+、FastAPI、Uvicorn、Pydantic |
| Agent | LangGraph、LangChain Tools |
| RAG | ChromaDB、SiliconFlow Qwen3-Embedding-0.6B |
| LLM | DeepSeek V4 Pro（OpenAI SDK 兼容调用） |
| 搜索 | Tavily Search API |
| 文档解析 | PyMuPDF、python-docx |
| 通信 | REST API、Server-Sent Events |
| 部署 | Docker、Docker Compose |

## 快速开始

### 1. 安装依赖

```bash
# 后端
cd backend
poetry install

# 前端
cd ../frontend
npm install
```

### 2. 配置环境变量

在 `backend/.env` 中配置：

```env
DEEPSEEK_API_KEY=你的 DeepSeek API Key
DEEPSEEK_BASE_URL=https://api.deepseek.com
TAVILY_API_KEY=你的 Tavily API Key
EMBEDDING_API_KEY=你的 SiliconFlow API Key
EMBEDDING_BASE_URL=https://api.siliconflow.cn/v1
```

### 3. 启动服务

```bash
# 后端，端口 8000
cd backend
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 前端，端口 5173
cd frontend
npm run dev
```

访问：

- 前端页面：`http://localhost:5173`
- 后端接口文档：`http://localhost:8000/docs`
- 健康检查：`http://localhost:8000/api/health`

也可以直接运行项目根目录下的快速启动脚本：

```bash
start.bat
```

## Docker 部署

```bash
docker compose up -d
```

常用命令：

```bash
docker compose logs -f
docker compose restart
docker compose down
docker compose build --no-cache
```

## 项目结构

```text
├── backend/                 # FastAPI 后端与 Agent/RAG 逻辑
├── frontend/                # Vue 3 前端
├── docs/                    # 项目文档与截图资源
├── docker-compose.yml
├── docker-compose.dev.yml
├── start.bat
├── start.sh
└── README.md
```

## API 概览

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `GET` | `/api/health` | 健康检查 |
| `POST` | `/api/resume/upload` | 上传简历 |
| `POST` | `/api/jd/upload` | 上传 JD |
| `POST` | `/api/match` | 创建匹配任务 |
| `GET` | `/api/match/{task_id}/stream` | SSE 获取分析进度与结果 |
| `GET` | `/api/match/{task_id}/report` | 获取匹配报告 |
| `POST` | `/api/interview/start` | 开始模拟面试 |
| `POST` | `/api/interview/{session_id}/answer` | 提交面试回答 |
| `GET` | `/api/interview/{session_id}/report` | 获取面试报告 |

## 验证

```bash
# 前端构建
cd frontend
npm run build

# 后端测试
cd backend
poetry run pytest
```

## License

MIT
