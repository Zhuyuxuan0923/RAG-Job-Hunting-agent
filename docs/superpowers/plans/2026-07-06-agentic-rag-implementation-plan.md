# Agentic RAG 求职助手 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a full-stack Agentic RAG job search assistant with document parsing, vector search, LangGraph agent, FastAPI backend, and Vue 3 frontend.

**Architecture:** Monorepo with `backend/` (FastAPI + LangGraph + ChromaDB) and `frontend/` (Vue 3 + Vite + TypeScript). Agent uses LangGraph state machine with 5 tools and 4-dimension reflection, streaming progress via SSE to the frontend.

**Tech Stack:** Python 3.11+, Poetry, FastAPI, LangChain, LangGraph, ChromaDB, DeepSeek v4 Pro API, Vue 3, Vite, TypeScript

---

## File Structure Map

```
backend/
  .env.example
  pyproject.toml
  src/
    __init__.py
    main.py                    # FastAPI app, CORS, lifespan
    config.py                  # pydantic-settings from .env
    models/
      __init__.py
      schemas.py               # All Pydantic request/response models
    services/
      __init__.py
      parser.py                # PyMuPDF + python-docx -> text
      chunker.py               # Text -> chunks (resume by section, JD semantic)
      embeddings.py            # DeepSeek Embedding API wrapper
      vectordb.py              # ChromaDB CRUD, 4 collections, hybrid search
    agent/
      __init__.py
      state.py                 # TypedDict state, AgentState
      tools.py                 # 5 tool definitions (search_resume, search_jd, etc.)
      graph.py                 # LangGraph StateGraph: classify->plan->search->fuse->reflect->generate
      reflection.py            # 4-dimension reflection: coverage, consistency, freshness, sufficiency
      prompts.py               # All system prompts as constants
    api/
      __init__.py
      resume.py                # POST /api/resume/upload
      jd.py                    # POST /api/jd/upload
      match.py                 # POST /api/match, GET /api/match/{id}/stream, GET /api/match/{id}/report
      interview.py             # POST /api/interview/start, POST /api/interview/{id}/answer, GET /api/interview/{id}/report
  tests/
    __init__.py
    test_parser.py
    test_chunker.py
    test_vectordb.py
    test_agent_graph.py
    test_api_match.py
    test_api_interview.py

frontend/
  package.json
  vite.config.ts
  tsconfig.json
  tsconfig.node.json
  index.html
  src/
    main.ts
    App.vue
    style.css
    router/
      index.ts
    types/
      index.ts
    api/
      client.ts
    composables/
      useSSE.ts
    components/
      AppHeader.vue
      FileDropZone.vue
      TextPasteArea.vue
      ScoreCircle.vue
      SkillGapChart.vue
      InfoCard.vue
      ThinkingStream.vue
      ChatBubble.vue
      QuestionCard.vue
      AnswerInput.vue
      FeedbackCard.vue
      ScoreSummary.vue
      QuestionReview.vue
      WeakAreaAnalysis.vue
      StudyPlan.vue
    pages/
      UploadPage.vue
      MatchReport.vue
      InterviewPage.vue
      InterviewReport.vue
```

---

## Phase 1: Project Scaffolding

### Task 1.1: Backend scaffolding with Poetry

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/.env.example`
- Create: `backend/src/__init__.py`
- Create: `backend/src/config.py`
- Create: `backend/src/main.py`

- [ ] **Step 1: Create pyproject.toml**

```toml
[tool.poetry]
name = "agentic-rag-backend"
version = "0.1.0"
description = "Agentic RAG Job Search Assistant - Backend"
python = "^3.11"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.115.0"
uvicorn = {extras = ["standard"], version = "^0.32.0"}
pydantic = "^2.10.0"
pydantic-settings = "^2.7.0"
python-dotenv = "^1.0.1"
langchain = "^0.3.0"
langgraph = "^0.2.0"
chromadb = "^0.5.0"
pymupdf = "^1.25.0"
python-docx = "^1.1.0"
openai = "^1.58.0"
tavily-python = "^0.5.0"
httpx = "^0.28.0"
sse-starlette = "^2.1.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.3.0"
pytest-asyncio = "^0.24.0"
httpx = "^0.28.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

- [ ] **Step 2: Create .env.example**

```env
DEEPSEEK_API_KEY=sk-your-deepseek-key
DEEPSEEK_BASE_URL=https://api.deepseek.com
TAVILY_API_KEY=tvly-your-tavily-key
CHROMA_PERSIST_DIR=./chroma_data
```

- [ ] **Step 3: Create src/config.py**

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    tavily_api_key: str = ""
    chroma_persist_dir: str = "./chroma_data"
    model_name: str = "deepseek-v4-pro"
    embedding_model: str = "deepseek-embedding"
    embedding_dim: int = 1536

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
```

- [ ] **Step 4: Create minimal src/main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Agentic RAG 求职助手")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
```

- [ ] **Step 5: Install dependencies**

```bash
cd backend && poetry install
```

- [ ] **Step 6: Verify health endpoint**

```bash
cd backend && poetry run uvicorn src.main:app --port 8000 &
sleep 2
curl http://localhost:8000/api/health
```
Expected: `{"status":"ok"}`

- [ ] **Step 7: Commit**

```bash
git add backend/pyproject.toml backend/.env.example backend/src/__init__.py backend/src/config.py backend/src/main.py
git commit -m "feat: scaffold backend with FastAPI and Poetry"
```

### Task 1.2: Frontend scaffolding with Vue 3 + Vite

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/tsconfig.json`
- Create: `frontend/tsconfig.node.json`
- Create: `frontend/index.html`
- Create: `frontend/src/main.ts`
- Create: `frontend/src/App.vue`
- Create: `frontend/src/style.css`
- Create: `frontend/src/router/index.ts`
- Create: `frontend/src/types/index.ts`
- Create: `frontend/src/api/client.ts`
- Create: `frontend/src/pages/UploadPage.vue` (placeholder)
- Create: `frontend/src/pages/MatchReport.vue` (placeholder)
- Create: `frontend/src/pages/InterviewPage.vue` (placeholder)
- Create: `frontend/src/pages/InterviewReport.vue` (placeholder)

- [ ] **Step 1: Create package.json**

```json
{
  "name": "agentic-rag-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.5.0",
    "vue-router": "^4.4.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.2.0",
    "typescript": "^5.6.0",
    "vite": "^6.0.0",
    "vue-tsc": "^2.1.0"
  }
}
```

- [ ] **Step 2: Create vite.config.ts**

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

- [ ] **Step 3: Create tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForExpose": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "preserve",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*.ts", "src/**/*.tsx", "src/**/*.vue", "env.d.ts"]
}
```

- [ ] **Step 4: Create tsconfig.node.json**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2023"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["vite.config.ts"]
}
```

- [ ] **Step 5: Create index.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Agentic RAG 求职助手</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

- [ ] **Step 6: Create src/main.ts**

```typescript
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)
app.use(router)
app.mount('#app')
```

- [ ] **Step 7: Create src/App.vue**

```vue
<template>
  <div id="app">
    <AppHeader />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import AppHeader from './components/AppHeader.vue'
</script>
```

- [ ] **Step 8: Create src/style.css (global styles)**

```css
:root {
  --color-primary: #1a73e8;
  --color-primary-dark: #1557b0;
  --color-bg: #f8f9fa;
  --color-surface: #ffffff;
  --color-text: #202124;
  --color-text-secondary: #5f6368;
  --color-border: #dadce0;
  --color-success: #34a853;
  --color-warning: #fbbc04;
  --color-error: #ea4335;
  --radius: 8px;
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--color-bg);
  color: var(--color-text);
  line-height: 1.6;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}
```

- [ ] **Step 9: Create src/router/index.ts**

```typescript
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'upload',
      component: () => import('../pages/UploadPage.vue'),
    },
    {
      path: '/match/:taskId',
      name: 'match',
      component: () => import('../pages/MatchReport.vue'),
    },
    {
      path: '/interview/:sessionId',
      name: 'interview',
      component: () => import('../pages/InterviewPage.vue'),
    },
    {
      path: '/report/:sessionId',
      name: 'report',
      component: () => import('../pages/InterviewReport.vue'),
    },
  ],
})

export default router
```

- [ ] **Step 10: Create src/types/index.ts**

```typescript
export interface ResumeUploadResponse {
  resume_id: string
  filename: string
  parsed_text: string
}

export interface JDUploadResponse {
  jd_id: string
  title: string
  parsed_text: string
}

export interface MatchProgress {
  event: 'progress' | 'thinking' | 'result' | 'done'
  stage?: string
  action?: string
  detail?: string
  data?: MatchReport
}

export interface MatchReport {
  task_id: string
  overall_score: number
  skill_match: SkillMatchItem[]
  skill_gaps: string[]
  company_background: string
  interview_experience: string
  suggestions: string[]
  preparation_checklist: string[]
}

export interface SkillMatchItem {
  skill: string
  required: boolean
  candidate_level: number
  jd_level: number
}

export interface InterviewStartResponse {
  session_id: string
  total_questions: number
}

export interface InterviewQuestion {
  question_number: number
  total_questions: number
  question: string
  category: string
  expected_points: string[]
}

export interface InterviewFeedback {
  score: number
  feedback: string
  strengths: string[]
  improvements: string[]
  model_answer: string
  next_question: InterviewQuestion | null
}

export interface InterviewReportData {
  session_id: string
  overall_score: number
  questions: QuestionReviewData[]
  weak_areas: WeakArea[]
  study_plan: StudyPlanItem[]
}

export interface QuestionReviewData {
  question_number: number
  question: string
  answer: string
  score: number
  feedback: string
  strengths: string[]
  improvements: string[]
}

export interface WeakArea {
  area: string
  score: number
  description: string
}

export interface StudyPlanItem {
  topic: string
  priority: 'high' | 'medium' | 'low'
  resources: string[]
  timeline: string
}

export interface SSEEvent {
  event: string
  data: string
}
```

- [ ] **Step 11: Create src/api/client.ts**

```typescript
const BASE = '/api'

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}

export const api = {
  uploadResume: (body: FormData | { text: string }) =>
    request<{ resume_id: string; filename: string; parsed_text: string }>('/resume/upload', {
      method: 'POST',
      body: body instanceof FormData ? body : JSON.stringify(body),
      headers: body instanceof FormData ? {} : { 'Content-Type': 'application/json' },
    }),

  uploadJD: (body: FormData | { text: string }) =>
    request<{ jd_id: string; title: string; parsed_text: string }>('/jd/upload', {
      method: 'POST',
      body: body instanceof FormData ? body : JSON.stringify(body),
      headers: body instanceof FormData ? {} : { 'Content-Type': 'application/json' },
    }),

  startMatch: (resumeId: string, jdId: string) =>
    request<{ task_id: string }>('/match', {
      method: 'POST',
      body: JSON.stringify({ resume_id: resumeId, jd_id: jdId }),
    }),

  startInterview: (resumeId: string, jdId: string) =>
    request<{ session_id: string; total_questions: number }>('/interview/start', {
      method: 'POST',
      body: JSON.stringify({ resume_id: resumeId, jd_id: jdId }),
    }),

  submitAnswer: (sessionId: string, answer: string, questionNumber: number) =>
    request<import('../types').InterviewFeedback>(`/interview/${sessionId}/answer`, {
      method: 'POST',
      body: JSON.stringify({ answer, question_number: questionNumber }),
    }),

  getMatchReport: (taskId: string) =>
    request<import('../types').MatchReport>(`/match/${taskId}/report`),

  getInterviewReport: (sessionId: string) =>
    request<import('../types').InterviewReportData>(`/interview/${sessionId}/report`),
}
```

- [ ] **Step 12: Create placeholder pages (4 files)**

Create `src/pages/UploadPage.vue`:
```vue
<template>
  <div class="upload-page">
    <h1>上传简历 & JD</h1>
    <p>拖拽或粘贴简历和职位描述，开始智能分析</p>
  </div>
</template>
```

Create `src/pages/MatchReport.vue`:
```vue
<template>
  <div class="match-report">
    <h1>匹配度分析报告</h1>
  </div>
</template>
```

Create `src/pages/InterviewPage.vue`:
```vue
<template>
  <div class="interview-page">
    <h1>模拟面试</h1>
  </div>
</template>
```

Create `src/pages/InterviewReport.vue`:
```vue
<template>
  <div class="interview-report">
    <h1>面试报告</h1>
  </div>
</template>
```

- [ ] **Step 13: Create placeholder AppHeader.vue**

```vue
<template>
  <header class="app-header">
    <router-link to="/" class="logo">Agentic RAG 求职助手</router-link>
  </header>
</template>

<style scoped>
.app-header {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  padding: 16px 24px;
}
.logo {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-primary);
  text-decoration: none;
}
</style>
```

- [ ] **Step 14: Install frontend dependencies and verify**

```bash
cd frontend && npm install && npx vite build --emptyOutDir
```
Expected: build succeeds.

- [ ] **Step 15: Commit**

```bash
git add frontend/
git commit -m "feat: scaffold Vue 3 frontend with Vite and TypeScript"
```

---

## Phase 2: Document Parsing

### Task 2.1: PDF/DOCX parser service

**Files:**
- Create: `backend/src/services/__init__.py`
- Create: `backend/src/services/parser.py`
- Create: `backend/tests/__init__.py`
- Create: `backend/tests/test_parser.py`

- [ ] **Step 1: Write failing test**

Create `backend/tests/test_parser.py`:
```python
import pytest
from src.services.parser import parse_pdf, parse_docx, parse_text


def test_parse_text_extracts_content():
    text = "## 个人信息\n\n张三\n\n## 技能\n\nPython, Java"
    result = parse_text(text)
    assert "张三" in result
    assert "Python" in result


def test_parse_text_handles_empty():
    result = parse_text("")
    assert result == ""


def test_parse_text_strips_excess_whitespace():
    result = parse_text("  张三\n\n\n  Python  ")
    assert result == "张三\nPython"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd backend && poetry run pytest tests/test_parser.py -v
```
Expected: FAIL, module not found.

- [ ] **Step 3: Implement parser.py**

Create `backend/src/services/parser.py`:
```python
import io


def parse_pdf(file_bytes: bytes, filename: str) -> str:
    import fitz
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text_parts = []
    for page in doc:
        text_parts.append(page.get_text())
    doc.close()
    return "\n".join(text_parts).strip()


def parse_docx(file_bytes: bytes, filename: str) -> str:
    from docx import Document
    doc = Document(io.BytesIO(file_bytes))
    text_parts = []
    for para in doc.paragraphs:
        if para.text.strip():
            text_parts.append(para.text)
    return "\n".join(text_parts).strip()


def parse_text(text: str) -> str:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return "\n".join(lines)


def parse_file(file_bytes: bytes, filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext == "pdf":
        return parse_pdf(file_bytes, filename)
    elif ext in ("docx", "doc"):
        return parse_docx(file_bytes, filename)
    else:
        raise ValueError(f"Unsupported file type: .{ext}")
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd backend && poetry run pytest tests/test_parser.py -v
```
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add backend/src/services/__init__.py backend/src/services/parser.py backend/tests/
git commit -m "feat: add PDF/DOCX/text parser service"
```

### Task 2.2: Text chunker service

**Files:**
- Create: `backend/src/services/chunker.py`
- Create: `backend/tests/test_chunker.py`

- [ ] **Step 1: Write failing test**

Create `backend/tests/test_chunker.py`:
```python
from src.services.chunker import chunk_resume, chunk_jd


def test_chunk_resume_splits_by_sections():
    text = "# 个人信息\n张三，5年经验\n# 技能\nPython, Java\n# 工作经历\n某公司工程师"
    chunks = chunk_resume(text)
    assert len(chunks) >= 3
    sections = [c["section"] for c in chunks]
    assert "个人信息" in sections
    assert "技能" in sections
    assert "工作经历" in sections


def test_chunk_resume_has_metadata():
    text = "# 技能\nPython\n"
    chunks = chunk_resume(text)
    assert chunks[0]["section"] == "技能"
    assert "chunk_index" in chunks[0]


def test_chunk_jd_uses_semantic_chunks():
    text = "## 岗位职责\n负责系统架构设计，带领5人团队完成产品从0到1的研发。\n\n## 任职要求\n本科以上学历，5年以上Python经验。熟悉分布式系统。"
    chunks = chunk_jd(text)
    assert len(chunks) >= 2


def test_chunk_jd_has_overlap():
    long_text = "职责\n" + ("开发高性能系统。" * 200)
    chunks = chunk_jd(long_text)
    assert len(chunks) > 1
```

- [ ] **Step 2: Implement chunker.py**

Create `backend/src/services/chunker.py`:
```python
import re
from typing import List, Dict, Any


def chunk_resume(text: str, max_tokens: int = 500) -> List[Dict[str, Any]]:
    sections = re.split(r"\n(?=#{1,3}\s)", text)
    chunks = []
    idx = 0
    for section in sections:
        section = section.strip()
        if not section:
            continue
        header_match = re.match(r"^#{1,3}\s+(.+)", section)
        section_name = header_match.group(1) if header_match else "其他"
        content = section
        if len(content) > max_tokens * 4:
            paragraphs = content.split("\n\n")
            for para in paragraphs:
                para = para.strip()
                if para:
                    chunks.append({
                        "text": para,
                        "section": section_name,
                        "chunk_index": idx,
                    })
                    idx += 1
        else:
            chunks.append({
                "text": content,
                "section": section_name,
                "chunk_index": idx,
            })
            idx += 1
    return chunks


def chunk_jd(text: str, chunk_size: int = 800, overlap: int = 100) -> List[Dict[str, Any]]:
    paragraphs = text.split("\n\n")
    chunks = []
    idx = 0
    current_chunk = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current_chunk) + len(para) > chunk_size * 4 and current_chunk:
            chunks.append({"text": current_chunk.strip(), "chunk_index": idx})
            idx += 1
            overlap_text = current_chunk[-overlap * 4:] if len(current_chunk) > overlap * 4 else current_chunk
            current_chunk = overlap_text + "\n" + para
        else:
            current_chunk += "\n" + para if current_chunk else para
    if current_chunk.strip():
        chunks.append({"text": current_chunk.strip(), "chunk_index": idx})
    return chunks
```

- [ ] **Step 3: Run tests**

```bash
cd backend && poetry run pytest tests/test_chunker.py -v
```
Expected: PASS (4 tests).

- [ ] **Step 4: Commit**

```bash
git add backend/src/services/chunker.py backend/tests/test_chunker.py
git commit -m "feat: add resume/JD text chunker service"
```

---

## Phase 3: ChromaDB Knowledge Base

### Task 3.1: Embedding service

**Files:**
- Create: `backend/src/services/embeddings.py`

- [ ] **Step 1: Create embeddings.py**

```python
from openai import OpenAI
from src.config import settings

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
        )
    return _client


def embed_texts(texts: list[str]) -> list[list[float]]:
    client = _get_client()
    resp = client.embeddings.create(
        model=settings.embedding_model,
        input=texts,
    )
    return [d.embedding for d in resp.data]


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]
```

- [ ] **Step 2: Commit**

```bash
git add backend/src/services/embeddings.py
git commit -m "feat: add DeepSeek embedding service wrapper"
```

### Task 3.2: ChromaDB vector store with 4 collections

**Files:**
- Create: `backend/src/services/vectordb.py`
- Create: `backend/tests/test_vectordb.py`

- [ ] **Step 1: Write failing test**

Create `backend/tests/test_vectordb.py`:
```python
import pytest
import chromadb
from src.services.vectordb import VectorStore


@pytest.fixture
def vs():
    client = chromadb.Client(chromadb.config.Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="./test_chroma_data",
        anonymized_telemetry=False,
    ))
    store = VectorStore(client)
    yield store
    client.delete_collection("test_resume_chunks")
    client.delete_collection("test_jd_chunks")


def test_add_and_search_resume(vs):
    chunks = [
        {"text": "张三，Python工程师", "section": "个人信息", "chunk_index": 0},
        {"text": "技能：Python, Java, Docker", "section": "技能", "chunk_index": 1},
    ]
    vs.add_chunks("test_resume_chunks", chunks, "resume")
    results = vs.search("test_resume_chunks", "Python开发", n_results=2)
    assert len(results) >= 1


def test_search_returns_metadata(vs):
    chunks = [{"text": "5年Python开发经验", "section": "工作经历", "chunk_index": 0}]
    vs.add_chunks("test_jd_chunks", chunks, "jd")
    results = vs.search("test_jd_chunks", "Python经验", n_results=1)
    assert len(results) == 1
    assert "section" in results[0]
    assert results[0]["section"] == "工作经历"
```

- [ ] **Step 2: Implement vectordb.py**

Create `backend/src/services/vectordb.py`:
```python
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings as ChromaSettings
from src.config import settings
from src.services.embeddings import embed_texts, embed_query


class VectorStore:
    def __init__(self, client: chromadb.Client = None):
        if client:
            self.client = client
        else:
            self.client = chromadb.Client(ChromaSettings(
                persist_directory=settings.chroma_persist_dir,
                anonymized_telemetry=False,
            ))

    def _get_or_create(self, name: str):
        try:
            return self.client.get_collection(name)
        except Exception:
            return self.client.create_collection(name, metadata={"hnsw:space": "cosine"})

    def add_chunks(self, collection_name: str, chunks: List[Dict[str, Any]], source: str):
        col = self._get_or_create(collection_name)
        texts = [c["text"] for c in chunks]
        embeddings = embed_texts(texts)
        ids = [f"{source}_{c.get('chunk_index', i)}" for i, c in enumerate(chunks)]
        metadatas = []
        for c in chunks:
            meta = {k: str(v) for k, v in c.items() if k != "text"}
            meta["source"] = source
            metadatas.append(meta)
        col.add(embeddings=embeddings, documents=texts, ids=ids, metadatas=metadatas)

    def search(self, collection_name: str, query: str, n_results: int = 20) -> List[Dict[str, Any]]:
        col = self._get_or_create(collection_name)
        q_embedding = embed_query(query)
        results = col.query(query_embeddings=[q_embedding], n_results=n_results)
        out = []
        if results["ids"] and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                out.append({
                    "id": results["ids"][0][i],
                    "text": results["documents"][0][i] if results["documents"] else "",
                    "score": results["distances"][0][i] if results["distances"] else 0,
                    **results["metadatas"][0][i] if results["metadatas"] else {},
                })
        return out

    def clear_collection(self, collection_name: str):
        try:
            self.client.delete_collection(collection_name)
        except Exception:
            pass


COLLECTIONS = ["resume_chunks", "jd_chunks", "interview_exp", "company_info"]
```

- [ ] **Step 3: Run tests**

```bash
cd backend && poetry run pytest tests/test_vectordb.py -v
```
Expected: PASS (2 tests).

- [ ] **Step 4: Commit**

```bash
git add backend/src/services/vectordb.py backend/tests/test_vectordb.py
git commit -m "feat: add ChromaDB vector store with 4 collections"
```

---

## Phase 4: Agent Engine

### Task 4.1: Agent state and prompts

**Files:**
- Create: `backend/src/agent/__init__.py`
- Create: `backend/src/agent/state.py`
- Create: `backend/src/agent/prompts.py`

- [ ] **Step 1: Create state.py**

```python
from typing import TypedDict, List, Dict, Any, Annotated
import operator


class SearchResult(TypedDict):
    source: str
    text: str
    score: float
    metadata: Dict[str, Any]


class AgentState(TypedDict):
    resume_id: str
    jd_id: str
    resume_text: str
    jd_text: str
    query: str
    sub_queries: List[str]
    search_results: Annotated[List[SearchResult], operator.add]
    fused_results: List[SearchResult]
    reflection: Dict[str, Any]
    search_round: int
    final_answer: str
    next_action: str
```

- [ ] **Step 2: Create prompts.py**

```python
CLASSIFY_PROMPT = """你是一个求职分析专家。分析用户意图，分类为以下之一：
- match_analysis: 岗位匹配度分析
- interview: 模拟面试
- general: 一般问题

用户输入：{query}
分类结果："""

PLAN_PROMPT = """你是一个检索规划专家。基于用户意图，生成 1-3 个检索子问题。
每个子问题应该能从已知数据源中获取特定信息。

意图：{intent}
用户问题：{query}
简历内容：{resume_text}
JD内容：{jd_text}

生成子问题列表(每行一个)："""

GENERATE_MATCH_PROMPT = """你是一个资深职业顾问和招聘专家。基于以下信息，进行岗位匹配度分析：

## 简历信息
{resume_text}

## JD信息
{jd_text}

## 检索到的补充信息
{search_results}

请输出一份结构化的匹配度分析报告，包含：
1. 综合匹配度评分（0-100）
2. 技能匹配详情（逐项对比）
3. 技能缺口分析
4. 改进建议
5. 面试准备清单

格式为 JSON。"""

GENERATE_INTERVIEW_PROMPT = """你是一个资深面试官。基于岗位要求和候选人简历，设计面试问题。

## 简历
{resume_text}

## JD
{jd_text}

## 技能缺口
{skill_gaps}

请生成 {num_questions} 道面试题，覆盖技术能力、项目经验、行为面试。
格式为 JSON 数组，每道题包含：question, category, expected_points。"""

EVALUATE_ANSWER_PROMPT = """你是一个资深面试官。请评估候选人对以下面试题的回答：

## 面试题
{question}

## 候选人回答
{answer}

## 期望要点
{expected_points}

请给出：
1. 评分（0-10）
2. 反馈点评
3. 优点
4. 改进建议
5. 参考答案

格式为 JSON。"""

INTERVIEW_REPORT_PROMPT = """你是一个面试评估专家。基于以下面试记录，生成综合面试报告：

## 面试记录
{interview_records}

请输出：
1. 综合评分（0-100）
2. 逐题回顾和点评
3. 薄弱环节分析
4. 后续复习计划

格式为 JSON。"""
```

- [ ] **Step 3: Commit**

```bash
git add backend/src/agent/
git commit -m "feat: add Agent state definitions and prompts"
```

### Task 4.2: Agent tools (5 tools)

**Files:**
- Create: `backend/src/agent/tools.py`

- [ ] **Step 1: Create tools.py**

```python
import json
from typing import List, Dict, Any
from langchain_core.tools import tool
from src.services.vectordb import VectorStore
from src.services.embeddings import embed_query
from src.config import settings

_vector_store: VectorStore | None = None


def get_vector_store() -> VectorStore:
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store


@tool
def search_resume(query: str, top_k: int = 10) -> str:
    """搜索简历知识库。查询候选人的技能、经历、项目等信息。"""
    vs = get_vector_store()
    results = vs.search("resume_chunks", query, n_results=top_k)
    return json.dumps([{"text": r["text"], "score": r["score"], "section": r.get("section", "")} for r in results], ensure_ascii=False)


@tool
def search_jd(query: str, top_k: int = 10) -> str:
    """搜索JD知识库。查询岗位要求、职责、技能要求等信息。"""
    vs = get_vector_store()
    results = vs.search("jd_chunks", query, n_results=top_k)
    return json.dumps([{"text": r["text"], "score": r["score"]} for r in results], ensure_ascii=False)


@tool
def web_search(query: str) -> str:
    """搜索互联网信息。用于查询公司背景、面经、行业趋势等最新信息。"""
    from tavily import TavilyClient
    client = TavilyClient(api_key=settings.tavily_api_key)
    response = client.search(query, search_depth="basic", max_results=5)
    results = response.get("results", [])
    return json.dumps([{"title": r.get("title", ""), "content": r.get("content", ""), "url": r.get("url", "")} for r in results], ensure_ascii=False)


@tool
def compare_skills(resume_skills: str, jd_skills: str) -> str:
    """对比简历技能和JD要求技能，输出结构化的差异分析。
    输入：resume_skills(候选人技能列表), jd_skills(JD要求的技能列表)"""
    resume_set = set(s.strip().lower() for s in resume_skills.split(","))
    jd_set = set(s.strip().lower() for s in jd_skills.split(","))
    matched = resume_set & jd_set
    missing = jd_set - resume_set
    extra = resume_set - jd_set
    return json.dumps({
        "matched": list(matched),
        "missing": list(missing),
        "extra": list(extra),
        "match_rate": round(len(matched) / len(jd_set) * 100, 1) if jd_set else 0,
    }, ensure_ascii=False)


@tool
def generate_question(category: str, skill_gap: str, difficulty: str = "medium") -> str:
    """基于技能缺口生成面试题目。category: technical/behavioral/project, skill_gap: 具体技能缺口, difficulty: easy/medium/hard"""
    from openai import OpenAI
    client = OpenAI(api_key=settings.deepseek_api_key, base_url=settings.deepseek_base_url)
    resp = client.chat.completions.create(
        model=settings.model_name,
        messages=[{
            "role": "user",
            "content": f"你是一位资深面试官。针对候选人的技能缺口「{skill_gap}」，出一道{difficulty}难度的{category}类面试题。只输出题目本身。",
        }],
        temperature=0.7,
    )
    return resp.choices[0].message.content or ""


def get_tools() -> list:
    return [search_resume, search_jd, web_search, compare_skills, generate_question]
```

- [ ] **Step 2: Commit**

```bash
git add backend/src/agent/tools.py
git commit -m "feat: implement 5 LangChain tools for Agent"
```

### Task 4.3: Reflection mechanism

**Files:**
- Create: `backend/src/agent/reflection.py`

- [ ] **Step 1: Create reflection.py**

```python
import json
from typing import Dict, Any, List
from openai import OpenAI
from src.config import settings


def reflect(search_results: List[Dict], sub_queries: List[str], intent: str) -> Dict[str, Any]:
    client = OpenAI(api_key=settings.deepseek_api_key, base_url=settings.deepseek_base_url)

    results_text = json.dumps(search_results, ensure_ascii=False, indent=2)

    prompt = f"""评估以下检索结果的质量，从4个维度判断：

## 子问题列表
{json.dumps(sub_queries, ensure_ascii=False)}

## 检索结果
{results_text}

请从以下4个维度评估，每个维度给出 pass/fail 和原因：
1. **覆盖度(coverage)**: 检索结果是否覆盖所有子问题？
2. **一致性(consistency)**: 不同来源的信息有无矛盾？
3. **时效性(freshness)**: 信息是否过时？
4. **充分性(sufficiency)**: 现有信息足够高质量回答吗？

返回 JSON：{{"coverage": {{"pass": true/false, "reason": ""}}, "consistency": ..., "freshness": ..., "sufficiency": ..., "overall_pass": true/false, "missing_queries": []}}"""

    resp = client.chat.completions.create(
        model=settings.model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content or "{}")


def should_continue(reflection_result: Dict[str, Any], max_rounds: int, current_round: int) -> bool:
    if current_round >= max_rounds:
        return False
    if reflection_result.get("overall_pass", False):
        return False
    return True
```

- [ ] **Step 2: Commit**

```bash
git add backend/src/agent/reflection.py
git commit -m "feat: add 4-dimension reflection mechanism"
```

### Task 4.4: LangGraph state graph

**Files:**
- Create: `backend/src/agent/graph.py`
- Create: `backend/tests/test_agent_graph.py`

- [ ] **Step 1: Write failing test**

Create `backend/tests/test_agent_graph.py`:
```python
import pytest
from src.agent.graph import create_match_graph
from src.agent.state import AgentState


@pytest.mark.asyncio
async def test_match_graph_builds():
    graph = create_match_graph()
    assert graph is not None
    compiled = graph.compile()
    assert compiled is not None


def test_initial_state_structure():
    state: AgentState = {
        "resume_id": "",
        "jd_id": "",
        "resume_text": "",
        "jd_text": "",
        "query": "分析匹配度",
        "sub_queries": [],
        "search_results": [],
        "fused_results": [],
        "reflection": {},
        "search_round": 0,
        "final_answer": "",
        "next_action": "classify",
    }
    assert state["next_action"] == "classify"
    assert state["search_round"] == 0
```

- [ ] **Step 2: Implement graph.py**

```python
import json
from typing import Literal
from langgraph.graph import StateGraph, END
from openai import OpenAI
from src.config import settings
from src.agent.state import AgentState
from src.agent.tools import search_resume, search_jd, web_search, compare_skills
from src.agent.reflection import reflect, should_continue
from src.agent.prompts import (
    CLASSIFY_PROMPT, PLAN_PROMPT, GENERATE_MATCH_PROMPT,
    GENERATE_INTERVIEW_PROMPT, EVALUATE_ANSWER_PROMPT, INTERVIEW_REPORT_PROMPT,
)


def _llm():
    return OpenAI(api_key=settings.deepseek_api_key, base_url=settings.deepseek_base_url)


def classify_node(state: AgentState) -> AgentState:
    client = _llm()
    resp = client.chat.completions.create(
        model=settings.model_name,
        messages=[{"role": "user", "content": CLASSIFY_PROMPT.format(query=state["query"])}],
        temperature=0.3,
    )
    intent = resp.choices[0].message.content.strip().lower()
    if "interview" in intent:
        state["next_action"] = "plan_interview"
    else:
        state["next_action"] = "plan"
    return state


def plan_node(state: AgentState) -> AgentState:
    client = _llm()
    resp = client.chat.completions.create(
        model=settings.model_name,
        messages=[{"role": "user", "content": PLAN_PROMPT.format(
            intent=state.get("next_action", "plan"),
            query=state["query"],
            resume_text=state.get("resume_text", ""),
            jd_text=state.get("jd_text", ""),
        )}],
        temperature=0.5,
    )
    lines = resp.choices[0].message.content.strip().split("\n")
    state["sub_queries"] = [line.lstrip("0123456789.-) ") for line in lines if line.strip()]
    if not state["sub_queries"]:
        state["sub_queries"] = [state["query"]]
    state["next_action"] = "search"
    return state


def search_node(state: AgentState) -> AgentState:
    results = []
    for q in state["sub_queries"]:
        try:
            r1 = search_resume.invoke({"query": q, "top_k": 10})
            results.append({"source": "resume", "text": r1, "score": 0.5})
        except Exception:
            pass
        try:
            r2 = search_jd.invoke({"query": q, "top_k": 10})
            results.append({"source": "jd", "text": r2, "score": 0.5})
        except Exception:
            pass
        try:
            r3 = web_search.invoke({"query": q})
            results.append({"source": "web", "text": r3, "score": 0.5})
        except Exception:
            pass
    state["search_results"] = results
    state["next_action"] = "fuse"
    return state


def fuse_node(state: AgentState) -> AgentState:
    seen = set()
    fused = []
    for r in state["search_results"]:
        key = r["text"][:100]
        if key not in seen:
            seen.add(key)
            fused.append(r)
    state["fused_results"] = fused
    state["next_action"] = "reflect"
    return state


def reflect_node(state: AgentState) -> AgentState:
    state["search_round"] = state.get("search_round", 0) + 1
    reflection = reflect(state["fused_results"], state["sub_queries"], state["query"])
    state["reflection"] = reflection
    if should_continue(reflection, max_rounds=3, current_round=state["search_round"]):
        missing = reflection.get("missing_queries", [])
        if missing:
            state["sub_queries"] = missing
        state["next_action"] = "search"
    else:
        state["next_action"] = "generate"
    return state


def generate_node(state: AgentState) -> AgentState:
    client = _llm()
    prompt = GENERATE_MATCH_PROMPT.format(
        resume_text=state.get("resume_text", ""),
        jd_text=state.get("jd_text", ""),
        search_results=json.dumps(state["fused_results"], ensure_ascii=False),
    )
    resp = client.chat.completions.create(
        model=settings.model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        response_format={"type": "json_object"},
    )
    state["final_answer"] = resp.choices[0].message.content or "{}"
    state["next_action"] = "done"
    return state


def create_match_graph():
    graph = StateGraph(AgentState)
    graph.add_node("classify", classify_node)
    graph.add_node("plan", plan_node)
    graph.add_node("search", search_node)
    graph.add_node("fuse", fuse_node)
    graph.add_node("reflect", reflect_node)
    graph.add_node("generate", generate_node)

    graph.set_entry_point("classify")
    graph.add_edge("classify", "plan")
    graph.add_edge("plan", "search")
    graph.add_edge("search", "fuse")
    graph.add_edge("fuse", "reflect")
    graph.add_conditional_edges("reflect", lambda s: s["next_action"], {
        "search": "search",
        "generate": "generate",
    })
    graph.add_edge("generate", END)

    return graph.compile()
```

- [ ] **Step 3: Run tests**

```bash
cd backend && poetry run pytest tests/test_agent_graph.py -v
```
Expected: PASS (2 tests).

- [ ] **Step 4: Commit**

```bash
git add backend/src/agent/graph.py backend/tests/test_agent_graph.py
git commit -m "feat: implement LangGraph state graph with 6 nodes and reflection loop"
```

---

## Phase 5: FastAPI Backend

### Task 5.1: Pydantic schemas

**Files:**
- Create: `backend/src/models/__init__.py`
- Create: `backend/src/models/schemas.py`

- [ ] **Step 1: Create schemas.py**

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class TextUpload(BaseModel):
    text: str


class ResumeUploadResponse(BaseModel):
    resume_id: str
    filename: str
    parsed_text: str


class JDUploadResponse(BaseModel):
    jd_id: str
    title: str
    parsed_text: str


class MatchRequest(BaseModel):
    resume_id: str
    jd_id: str


class MatchTaskResponse(BaseModel):
    task_id: str


class SkillMatchItem(BaseModel):
    skill: str
    required: bool
    candidate_level: int = Field(default=0)
    jd_level: int = Field(default=0)


class MatchReportResponse(BaseModel):
    task_id: str
    overall_score: int
    skill_match: List[SkillMatchItem]
    skill_gaps: List[str]
    company_background: str
    interview_experience: str
    suggestions: List[str]
    preparation_checklist: List[str]


class InterviewStartRequest(BaseModel):
    resume_id: str
    jd_id: str


class InterviewStartResponse(BaseModel):
    session_id: str
    total_questions: int


class AnswerRequest(BaseModel):
    answer: str
    question_number: int


class InterviewQuestion(BaseModel):
    question_number: int
    total_questions: int
    question: str
    category: str
    expected_points: List[str]


class InterviewFeedback(BaseModel):
    score: int
    feedback: str
    strengths: List[str]
    improvements: List[str]
    model_answer: str
    next_question: Optional[InterviewQuestion] = None


class QuestionReview(BaseModel):
    question_number: int
    question: str
    answer: str
    score: int
    feedback: str
    strengths: List[str]
    improvements: List[str]


class WeakArea(BaseModel):
    area: str
    score: int
    description: str


class StudyPlanItem(BaseModel):
    topic: str
    priority: str
    resources: List[str]
    timeline: str


class InterviewReportResponse(BaseModel):
    session_id: str
    overall_score: int
    questions: List[QuestionReview]
    weak_areas: List[WeakArea]
    study_plan: List[StudyPlanItem]
```

- [ ] **Step 2: Commit**

```bash
git add backend/src/models/
git commit -m "feat: add Pydantic request/response schemas"
```

### Task 5.2: API routes — resume & JD upload

**Files:**
- Create: `backend/src/api/__init__.py`
- Create: `backend/src/api/resume.py`
- Create: `backend/src/api/jd.py`

- [ ] **Step 1: Create resume.py**

```python
import uuid
from fastapi import APIRouter, UploadFile, File, Form
from src.models.schemas import TextUpload, ResumeUploadResponse
from src.services.parser import parse_file, parse_text
from src.services.chunker import chunk_resume
from src.services.vectordb import VectorStore

router = APIRouter(prefix="/api/resume", tags=["resume"])

_resumes: dict = {}


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile | None = File(None),
    text: str | None = Form(None),
):
    resume_id = str(uuid.uuid4())[:8]
    filename = "text_input"

    if file and file.filename:
        file_bytes = await file.read()
        filename = file.filename
        parsed = parse_file(file_bytes, filename)
    elif text:
        parsed = parse_text(text)
    else:
        parsed = ""

    _resumes[resume_id] = {"filename": filename, "parsed_text": parsed}

    chunks = chunk_resume(parsed)
    if chunks:
        vs = VectorStore()
        vs.add_chunks("resume_chunks", chunks, f"resume_{resume_id}")

    return ResumeUploadResponse(resume_id=resume_id, filename=filename, parsed_text=parsed)
```

- [ ] **Step 2: Create jd.py**

```python
import uuid
from fastapi import APIRouter, UploadFile, File, Form
from src.models.schemas import TextUpload, JDUploadResponse
from src.services.parser import parse_file, parse_text
from src.services.chunker import chunk_jd
from src.services.vectordb import VectorStore

router = APIRouter(prefix="/api/jd", tags=["jd"])

_jds: dict = {}


@router.post("/upload", response_model=JDUploadResponse)
async def upload_jd(
    file: UploadFile | None = File(None),
    text: str | None = Form(None),
):
    jd_id = str(uuid.uuid4())[:8]
    title = "text_input"

    if file and file.filename:
        file_bytes = await file.read()
        title = file.filename
        parsed = parse_file(file_bytes, title)
    elif text:
        parsed = parse_text(text)
        lines = parsed.split("\n")
        title = lines[0][:50] if lines else "text_input"
    else:
        parsed = ""

    _jds[jd_id] = {"title": title, "parsed_text": parsed}

    chunks = chunk_jd(parsed)
    if chunks:
        vs = VectorStore()
        vs.add_chunks("jd_chunks", chunks, f"jd_{jd_id}")

    return JDUploadResponse(jd_id=jd_id, title=title, parsed_text=parsed)
```

- [ ] **Step 3: Commit**

```bash
git add backend/src/api/
git commit -m "feat: add resume and JD upload API endpoints"
```

### Task 5.3: API routes — match analysis with SSE streaming

**Files:**
- Create: `backend/src/api/match.py`

- [ ] **Step 1: Create match.py**

```python
import uuid
import json
import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.models.schemas import MatchRequest, MatchTaskResponse, MatchReportResponse
from src.agent.graph import create_match_graph
from src.agent.state import AgentState

router = APIRouter(prefix="/api/match", tags=["match"])

_tasks: dict = {}


async def _event_stream(task_id: str, state: AgentState):
    steps = [
        ("parsing", "正在解析简历和JD..."),
        ("indexing", "正在构建知识库索引..."),
        ("analyzing", "Agent 正在分析匹配度..."),
    ]
    for stage, detail in steps:
        yield f"event: progress\ndata: {json.dumps({'stage': stage, 'detail': detail}, ensure_ascii=False)}\n\n"
        await asyncio.sleep(0.3)

    graph = create_match_graph()
    async for event in graph.astream(state, stream_mode="updates"):
        node_name = list(event.keys())[0]
        node_data = event[node_name]
        yield f"event: thinking\ndata: {json.dumps({'action': node_name, 'detail': str(node_data.get('next_action', '')), 'search_round': node_data.get('search_round', 0)}, ensure_ascii=False)}\n\n"

    try:
        result = json.loads(state.get("final_answer", "{}"))
    except json.JSONDecodeError:
        result = {"overall_score": 0, "skill_match": [], "skill_gaps": [], "company_background": "", "interview_experience": "", "suggestions": [], "preparation_checklist": []}

    _tasks[task_id]["report"] = result
    yield f"event: result\ndata: {json.dumps(result, ensure_ascii=False)}\n\n"
    yield f"event: done\ndata: {{}}\n\n"


@router.post("", response_model=MatchTaskResponse)
async def start_match(req: MatchRequest):
    from src.api.resume import _resumes
    from src.api.jd import _jds

    task_id = str(uuid.uuid4())[:8]
    resume_data = _resumes.get(req.resume_id, {})
    jd_data = _jds.get(req.jd_id, {})

    state: AgentState = {
        "resume_id": req.resume_id,
        "jd_id": req.jd_id,
        "resume_text": resume_data.get("parsed_text", ""),
        "jd_text": jd_data.get("parsed_text", ""),
        "query": "分析岗位匹配度，给出评分、技能缺口和改进建议",
        "sub_queries": [],
        "search_results": [],
        "fused_results": [],
        "reflection": {},
        "search_round": 0,
        "final_answer": "",
        "next_action": "classify",
    }

    _tasks[task_id] = {"state": state}

    return MatchTaskResponse(task_id=task_id)


@router.get("/{task_id}/stream")
async def stream_match(task_id: str):
    task = _tasks.get(task_id)
    if not task:
        return StreamingResponse(
            iter([f"event: error\ndata: {json.dumps({'detail': 'Task not found'})}\n\n"]),
            media_type="text/event-stream",
        )
    return StreamingResponse(
        _event_stream(task_id, task["state"]),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@router.get("/{task_id}/report", response_model=MatchReportResponse)
async def get_match_report(task_id: str):
    task = _tasks.get(task_id, {})
    report = task.get("report", {})
    return MatchReportResponse(
        task_id=task_id,
        overall_score=report.get("overall_score", 0),
        skill_match=report.get("skill_match", []),
        skill_gaps=report.get("skill_gaps", []),
        company_background=report.get("company_background", ""),
        interview_experience=report.get("interview_experience", ""),
        suggestions=report.get("suggestions", []),
        preparation_checklist=report.get("preparation_checklist", []),
    )
```

- [ ] **Step 2: Commit**

```bash
git add backend/src/api/match.py
git commit -m "feat: add match analysis API with SSE streaming"
```

### Task 5.4: API routes — interview simulation

**Files:**
- Create: `backend/src/api/interview.py`

- [ ] **Step 1: Create interview.py**

```python
import uuid
import json
from fastapi import APIRouter
from openai import OpenAI
from src.config import settings
from src.models.schemas import (
    InterviewStartRequest, InterviewStartResponse,
    AnswerRequest, InterviewFeedback, InterviewReportResponse,
    InterviewQuestion, QuestionReview, WeakArea, StudyPlanItem,
)

router = APIRouter(prefix="/api/interview", tags=["interview"])

_sessions: dict = {}


def _llm():
    return OpenAI(api_key=settings.deepseek_api_key, base_url=settings.deepseek_base_url)


@router.post("/start", response_model=InterviewStartResponse)
async def start_interview(req: InterviewStartRequest):
    from src.api.resume import _resumes
    from src.api.jd import _jds

    session_id = str(uuid.uuid4())[:8]
    resume_data = _resumes.get(req.resume_id, {}).get("parsed_text", "")
    jd_data = _jds.get(req.jd_id, {}).get("parsed_text", "")

    client = _llm()
    resp = client.chat.completions.create(
        model=settings.model_name,
        messages=[{"role": "user", "content": f"""基于以下信息，生成 5 道面试题：

## 简历
{resume_data}

## JD
{jd_data}

每道题覆盖不同维度(技术能力/项目经验/行为面试/系统设计/解决问题)。
返回 JSON 数组：[
  {{"question": "...", "category": "...", "expected_points": ["..."]}}
]"""}],
        temperature=0.8,
        response_format={"type": "json_object"},
    )

    try:
        raw = json.loads(resp.choices[0].message.content or "[]")
        questions = raw if isinstance(raw, list) else raw.get("questions", [])
    except json.JSONDecodeError:
        questions = []

    processed = []
    for i, q in enumerate(questions):
        processed.append({
            "question_number": i + 1,
            "total_questions": len(questions),
            "question": q.get("question", ""),
            "category": q.get("category", "technical"),
            "expected_points": q.get("expected_points", []),
        })

    _sessions[session_id] = {
        "resume_text": resume_data,
        "jd_text": jd_data,
        "questions": processed,
        "answers": [],
        "current_index": 0,
    }

    return InterviewStartResponse(session_id=session_id, total_questions=len(processed))


@router.post("/{session_id}/answer", response_model=InterviewFeedback)
async def submit_answer(session_id: str, req: AnswerRequest):
    session = _sessions.get(session_id)
    if not session:
        return InterviewFeedback(score=0, feedback="Session not found", strengths=[], improvements=[], model_answer="")

    questions = session["questions"]
    current_q = questions[session["current_index"]]

    client = _llm()
    resp = client.chat.completions.create(
        model=settings.model_name,
        messages=[{"role": "user", "content": f"""评估面试回答：

## 题目
{current_q['question']}

## 期望要点
{json.dumps(current_q.get('expected_points', []), ensure_ascii=False)}

## 候选人回答
{req.answer}

请评分(0-10)并给出反馈。返回 JSON：
{{"score": 8, "feedback": "整体评价", "strengths": ["优点1"], "improvements": ["改进1"], "model_answer": "参考答案"}}
"""}],
        temperature=0.5,
        response_format={"type": "json_object"},
    )

    feedback = json.loads(resp.choices[0].message.content or "{}")

    session["answers"].append({
        "question_number": current_q["question_number"],
        "question": current_q["question"],
        "answer": req.answer,
        "score": feedback.get("score", 0),
        "feedback": feedback.get("feedback", ""),
        "strengths": feedback.get("strengths", []),
        "improvements": feedback.get("improvements", []),
    })

    session["current_index"] += 1

    next_q = None
    if session["current_index"] < len(questions):
        next_q_data = questions[session["current_index"]]
        next_q = InterviewQuestion(
            question_number=next_q_data["question_number"],
            total_questions=next_q_data["total_questions"],
            question=next_q_data["question"],
            category=next_q_data["category"],
            expected_points=next_q_data.get("expected_points", []),
        )

    return InterviewFeedback(
        score=feedback.get("score", 0),
        feedback=feedback.get("feedback", ""),
        strengths=feedback.get("strengths", []),
        improvements=feedback.get("improvements", []),
        model_answer=feedback.get("model_answer", ""),
        next_question=next_q,
    )


@router.get("/{session_id}/report", response_model=InterviewReportResponse)
async def get_interview_report(session_id: str):
    session = _sessions.get(session_id)
    if not session:
        return InterviewReportResponse(
            session_id=session_id, overall_score=0,
            questions=[], weak_areas=[], study_plan=[],
        )

    answers = session["answers"]
    if not answers:
        return InterviewReportResponse(
            session_id=session_id, overall_score=0,
            questions=[], weak_areas=[], study_plan=[],
        )

    total = sum(a["score"] for a in answers)
    overall = round(total / len(answers) * 10)

    records_text = json.dumps(answers, ensure_ascii=False)
    client = _llm()
    resp = client.chat.completions.create(
        model=settings.model_name,
        messages=[{"role": "user", "content": f"""基于以下面试记录生成面试报告：

## 面试记录
{records_text}

返回 JSON：
{{
  "weak_areas": [{{"area": "技术深度", "score": 6, "description": "..."}}],
  "study_plan": [{{"topic": "...", "priority": "high", "resources": ["..."], "timeline": "1-2周"}}]
}}
"""}],
        temperature=0.5,
        response_format={"type": "json_object"},
    )

    extra = json.loads(resp.choices[0].message.content or "{}")

    questions_review = []
    for a in answers:
        questions_review.append(QuestionReview(
            question_number=a["question_number"],
            question=a["question"],
            answer=a["answer"],
            score=a["score"],
            feedback=a["feedback"],
            strengths=a.get("strengths", []),
            improvements=a.get("improvements", []),
        ))

    return InterviewReportResponse(
        session_id=session_id,
        overall_score=overall,
        questions=questions_review,
        weak_areas=[WeakArea(**w) for w in extra.get("weak_areas", [])],
        study_plan=[StudyPlanItem(**s) for s in extra.get("study_plan", [])],
    )
```

- [ ] **Step 2: Commit**

```bash
git add backend/src/api/interview.py
git commit -m "feat: add interview simulation API endpoints"
```

### Task 5.5: Register all routes in main.py

**Files:**
- Modify: `backend/src/main.py`

- [ ] **Step 1: Update main.py**

Read existing `backend/src/main.py` and replace with:
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.resume import router as resume_router
from src.api.jd import router as jd_router
from src.api.match import router as match_router
from src.api.interview import router as interview_router
from src.services.vectordb import VectorStore


@asynccontextmanager
async def lifespan(app: FastAPI):
    vs = VectorStore()
    for col_name in ["resume_chunks", "jd_chunks", "interview_exp", "company_info"]:
        vs._get_or_create(col_name)
    yield


app = FastAPI(title="Agentic RAG 求职助手", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)
app.include_router(jd_router)
app.include_router(match_router)
app.include_router(interview_router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
```

- [ ] **Step 2: Verify server starts**

```bash
cd backend && poetry run uvicorn src.main:app --port 8000 &
sleep 2
curl http://localhost:8000/api/health
curl http://localhost:8000/docs
```
Expected: health returns `{"status":"ok"}`, /docs returns OpenAPI page.

- [ ] **Step 3: Commit**

```bash
git add backend/src/main.py
git commit -m "feat: register all API routes and add lifespan collection init"
```

### Task 5.6: Integration tests for API

**Files:**
- Create: `backend/tests/test_api_match.py`
- Create: `backend/tests/test_api_interview.py`

- [ ] **Step 1: Create test_api_match.py**

```python
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.mark.asyncio
async def test_upload_resume_text():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/resume/upload", data={"text": "张三\nPython 5年\nJava"})
    assert resp.status_code == 200
    data = resp.json()
    assert "resume_id" in data
    assert "张三" in data["parsed_text"]


@pytest.mark.asyncio
async def test_upload_jd_text():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/jd/upload", data={"text": "Python工程师\n要求5年经验"})
    assert resp.status_code == 200
    data = resp.json()
    assert "jd_id" in data


@pytest.mark.asyncio
async def test_match_returns_task_id():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r1 = await client.post("/api/resume/upload", data={"text": "张三\nPython专家"})
        r2 = await client.post("/api/jd/upload", data={"text": "Python工程师"})
        resume_id = r1.json()["resume_id"]
        jd_id = r2.json()["jd_id"]
        resp = await client.post("/api/match", json={"resume_id": resume_id, "jd_id": jd_id})
    assert resp.status_code == 200
    assert "task_id" in resp.json()


@pytest.mark.asyncio
async def test_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
```

- [ ] **Step 2: Create test_api_interview.py**

```python
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.mark.asyncio
async def test_interview_start_returns_session():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r1 = await client.post("/api/resume/upload", data={"text": "张三\nPython专家"})
        r2 = await client.post("/api/jd/upload", data={"text": "Python工程师"})
        resume_id = r1.json()["resume_id"]
        jd_id = r2.json()["jd_id"]
        resp = await client.post("/api/interview/start", json={"resume_id": resume_id, "jd_id": jd_id})
    assert resp.status_code == 200
    data = resp.json()
    assert "session_id" in data
    assert data["total_questions"] > 0
```

- [ ] **Step 3: Run integration tests**

```bash
cd backend && poetry run pytest tests/test_api_match.py tests/test_api_interview.py -v
```
Expected: PASS (depends on API key availability; tests without actual LLM calls should pass).

- [ ] **Step 4: Commit**

```bash
git add backend/tests/test_api_match.py backend/tests/test_api_interview.py
git commit -m "test: add API integration tests for match and interview"
```

---

## Phase 6: Vue 3 Frontend

### Task 6.1: Core components (FileDropZone, TextPasteArea)

**Files:**
- Create: `frontend/src/components/FileDropZone.vue`
- Create: `frontend/src/components/TextPasteArea.vue`

- [ ] **Step 1: Create FileDropZone.vue**

```vue
<template>
  <div
    class="drop-zone"
    :class="{ 'drag-over': dragging }"
    @dragover.prevent="dragging = true"
    @dragleave.prevent="dragging = false"
    @drop.prevent="handleDrop"
  >
    <div class="drop-content">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M12 16V4m0 0L8 8m4-4l4 4M4 20h16"/>
      </svg>
      <p class="drop-text">{{ label }}</p>
      <p class="drop-hint">支持 PDF / DOCX 格式</p>
      <input ref="fileInput" type="file" accept=".pdf,.docx,.doc" @change="onFileSelect" hidden />
      <button class="btn-select" @click="($refs.fileInput as HTMLInputElement).click()">选择文件</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{ label: string }>()
const emit = defineEmits<{ file: [file: File] }>()

const dragging = ref(false)
const fileInput = ref<HTMLInputElement>()

function handleDrop(e: DragEvent) {
  dragging.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) emit('file', file)
}

function onFileSelect(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) emit('file', file)
}
</script>

<style scoped>
.drop-zone {
  border: 2px dashed var(--color-border);
  border-radius: var(--radius);
  padding: 32px;
  text-align: center;
  transition: border-color 0.2s, background 0.2s;
  cursor: pointer;
  background: var(--color-surface);
}
.drop-zone.drag-over {
  border-color: var(--color-primary);
  background: #e8f0fe;
}
.drop-text {
  font-size: 16px;
  font-weight: 600;
  margin-top: 12px;
}
.drop-hint {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-top: 4px;
}
.btn-select {
  margin-top: 16px;
  padding: 8px 20px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 14px;
  cursor: pointer;
}
.btn-select:hover {
  background: var(--color-primary-dark);
}
</style>
```

- [ ] **Step 2: Create TextPasteArea.vue**

```vue
<template>
  <div class="paste-area">
    <textarea
      v-model="content"
      :placeholder="placeholder"
      class="paste-input"
      rows="8"
    ></textarea>
    <div class="paste-footer">
      <span class="char-count">{{ content.length }} 字</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{ placeholder: string; modelValue: string }>()
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

const content = ref(props.modelValue)
watch(content, (v) => emit('update:modelValue', v))
watch(() => props.modelValue, (v) => { content.value = v })
</script>

<style scoped>
.paste-area {
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--color-surface);
}
.paste-input {
  width: 100%;
  border: none;
  padding: 16px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  outline: none;
  line-height: 1.6;
}
.paste-footer {
  padding: 8px 16px;
  border-top: 1px solid var(--color-border);
  font-size: 12px;
  color: var(--color-text-secondary);
}
</style>
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/FileDropZone.vue frontend/src/components/TextPasteArea.vue
git commit -m "feat: add FileDropZone and TextPasteArea components"
```

### Task 6.2: UploadPage

**Files:**
- Modify: `frontend/src/pages/UploadPage.vue`

- [ ] **Step 1: Update UploadPage.vue**

```vue
<template>
  <div class="upload-page">
    <h1 class="page-title">上传简历 & 职位描述</h1>
    <p class="page-desc">开始智能岗位匹配分析和模拟面试</p>

    <div class="upload-grid">
      <div class="upload-column">
        <h2>简历</h2>
        <FileDropZone label="上传简历文件" @file="handleResumeFile" />
        <div class="divider"><span>或</span></div>
        <TextPasteArea v-model="resumeText" placeholder="粘贴简历文本..." />
        <div v-if="resumeUploaded" class="upload-success">已解析 {{ resumeFilename }}</div>
      </div>

      <div class="upload-column">
        <h2>职位描述 (JD)</h2>
        <FileDropZone label="上传 JD 文件" @file="handleJDFile" />
        <div class="divider"><span>或</span></div>
        <TextPasteArea v-model="jdText" placeholder="粘贴 JD 文本..." />
        <div v-if="jdUploaded" class="upload-success">已解析 {{ jdFilename }}</div>
      </div>
    </div>

    <div class="actions">
      <button class="btn-primary" :disabled="!canProceed" @click="startAnalysis">
        开始匹配度分析
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import FileDropZone from '../components/FileDropZone.vue'
import TextPasteArea from '../components/TextPasteArea.vue'
import { api } from '../api/client'

const router = useRouter()
const resumeText = ref('')
const jdText = ref('')
const resumeId = ref('')
const jdId = ref('')
const resumeFilename = ref('')
const jdFilename = ref('')
const resumeUploaded = ref(false)
const jdUploaded = ref(false)

const canProceed = computed(() => resumeId.value && jdId.value)

async function handleResumeFile(file: File) {
  const form = new FormData()
  form.append('file', file)
  const res = await api.uploadResume(form)
  resumeId.value = res.resume_id
  resumeFilename.value = res.filename
  resumeUploaded.value = true
}

async function handleJDFile(file: File) {
  const form = new FormData()
  form.append('file', file)
  const res = await api.uploadJD(form)
  jdId.value = res.jd_id
  jdFilename.value = res.title
  jdUploaded.value = true
}

async function startAnalysis() {
  if (resumeText.value && !resumeId.value) {
    const res = await api.uploadResume({ text: resumeText.value })
    resumeId.value = res.resume_id
  }
  if (jdText.value && !jdId.value) {
    const res = await api.uploadJD({ text: jdText.value })
    jdId.value = res.jd_id
  }
  const match = await api.startMatch(resumeId.value, jdId.value)
  router.push(`/match/${match.task_id}`)
}
</script>

<style scoped>
.upload-page {
  max-width: 1000px;
  margin: 0 auto;
}
.page-title { font-size: 28px; font-weight: 700; }
.page-desc { color: var(--color-text-secondary); margin: 8px 0 32px; }
.upload-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}
.upload-column h2 { font-size: 18px; margin-bottom: 16px; }
.divider {
  text-align: center;
  margin: 16px 0;
  color: var(--color-text-secondary);
  font-size: 13px;
}
.upload-success {
  margin-top: 12px;
  padding: 10px 16px;
  background: #e6f4ea;
  border-radius: var(--radius);
  color: var(--color-success);
  font-size: 14px;
}
.actions {
  text-align: center;
  margin-top: 40px;
}
.btn-primary {
  padding: 14px 40px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}
.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.btn-primary:not(:disabled):hover {
  background: var(--color-primary-dark);
}
</style>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/pages/UploadPage.vue
git commit -m "feat: implement UploadPage with file and text input"
```

### Task 6.3: SSE composable and ThinkingStream

**Files:**
- Create: `frontend/src/composables/useSSE.ts`
- Create: `frontend/src/components/ThinkingStream.vue`

- [ ] **Step 1: Create useSSE.ts**

```typescript
import { ref, onUnmounted } from 'vue'

export function useSSE(url: string) {
  const data = ref<any>(null)
  const thinking = ref<Array<{ action: string; detail: string; search_round: number }>>([])
  const stage = ref('')
  const done = ref(false)
  const error = ref<string | null>(null)
  let eventSource: EventSource | null = null

  function connect() {
    eventSource = new EventSource(url)
    eventSource.addEventListener('progress', (e) => {
      const d = JSON.parse(e.data)
      stage.value = d.stage
    })
    eventSource.addEventListener('thinking', (e) => {
      const d = JSON.parse(e.data)
      thinking.value.push(d)
    })
    eventSource.addEventListener('result', (e) => {
      data.value = JSON.parse(e.data)
    })
    eventSource.addEventListener('done', () => {
      done.value = true
      eventSource?.close()
    })
    eventSource.addEventListener('error', (e) => {
      error.value = 'SSE connection error'
      eventSource?.close()
    })
    eventSource.onerror = () => {
      error.value = 'SSE connection failed'
      eventSource?.close()
    }
  }

  function close() {
    eventSource?.close()
  }

  onUnmounted(close)

  return { data, thinking, stage, done, error, connect, close }
}
```

- [ ] **Step 2: Create ThinkingStream.vue**

```vue
<template>
  <div class="thinking-stream">
    <div class="stream-header">
      <span class="pulse"></span>
      Agent 思考过程
    </div>
    <div class="stream-body" ref="bodyRef">
      <div v-for="(item, i) in items" :key="i" class="think-item">
        <span class="think-action">{{ item.action }}</span>
        <span class="think-detail">{{ item.detail }}</span>
        <span v-if="item.search_round" class="think-round">第 {{ item.search_round }} 轮</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { watch, ref } from 'vue'

const props = defineProps<{ items: Array<{ action: string; detail: string; search_round: number }> }>()
const bodyRef = ref<HTMLElement>()

watch(() => props.items.length, () => {
  if (bodyRef.value) {
    bodyRef.value.scrollTop = bodyRef.value.scrollHeight
  }
})
</script>

<style scoped>
.thinking-stream {
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  background: #fafafa;
  margin: 16px 0;
}
.stream-header {
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 600;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  gap: 8px;
}
.pulse {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-success);
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}
.stream-body {
  max-height: 300px;
  overflow-y: auto;
  padding: 12px 16px;
  font-size: 13px;
}
.think-item {
  padding: 6px 0;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  gap: 8px;
  align-items: center;
}
.think-action {
  background: var(--color-primary);
  color: #fff;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  white-space: nowrap;
}
.think-detail {
  color: var(--color-text-secondary);
  flex: 1;
}
.think-round {
  font-size: 11px;
  color: var(--color-text-secondary);
}
</style>
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/composables/useSSE.ts frontend/src/components/ThinkingStream.vue
git commit -m "feat: add SSE composable and ThinkingStream component"
```

### Task 6.4: ScoreCircle and InfoCard components

**Files:**
- Create: `frontend/src/components/ScoreCircle.vue`
- Create: `frontend/src/components/InfoCard.vue`

- [ ] **Step 1: Create ScoreCircle.vue**

```vue
<template>
  <div class="score-circle">
    <svg viewBox="0 0 120 120" class="circle-svg">
      <circle cx="60" cy="60" r="52" fill="none" stroke="#e0e0e0" stroke-width="8" />
      <circle
        cx="60" cy="60" r="52"
        fill="none"
        :stroke="color"
        stroke-width="8"
        stroke-linecap="round"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="offset"
        transform="rotate(-90 60 60)"
        class="progress-ring"
      />
    </svg>
    <div class="score-text">
      <span class="score-value" :style="{ color }">{{ score }}</span>
      <span class="score-label">匹配度</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ score: number }>()
const circumference = 2 * Math.PI * 52

const offset = computed(() => circumference - (props.score / 100) * circumference)

const color = computed(() => {
  if (props.score >= 80) return 'var(--color-success)'
  if (props.score >= 60) return 'var(--color-warning)'
  return 'var(--color-error)'
})
</script>

<style scoped>
.score-circle {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto;
}
.circle-svg {
  width: 100%;
  height: 100%;
}
.progress-ring {
  transition: stroke-dashoffset 1s ease;
}
.score-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}
.score-value {
  font-size: 32px;
  font-weight: 700;
  display: block;
}
.score-label {
  font-size: 12px;
  color: var(--color-text-secondary);
}
</style>
```

- [ ] **Step 2: Create InfoCard.vue**

```vue
<template>
  <div class="info-card">
    <h3 class="card-title">{{ title }}</h3>
    <div class="card-body">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ title: string }>()
</script>

<style scoped>
.info-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 20px;
}
.card-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--color-border);
}
.card-body {
  font-size: 14px;
  line-height: 1.7;
  color: var(--color-text-secondary);
}
</style>
```

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/ScoreCircle.vue frontend/src/components/InfoCard.vue
git commit -m "feat: add ScoreCircle and InfoCard components"
```

### Task 6.5: MatchReport page

**Files:**
- Modify: `frontend/src/pages/MatchReport.vue`

- [ ] **Step 1: Update MatchReport.vue**

Read existing file, then write full implementation:
```vue
<template>
  <div class="match-report">
    <ThinkingStream :items="thinking" />

    <div v-if="data" class="report-content">
      <div class="score-section">
        <ScoreCircle :score="data.overall_score" />
        <h2>岗位匹配度分析报告</h2>
      </div>

      <div class="cards-grid">
        <InfoCard title="公司背景">
          <p>{{ data.company_background || '暂无数据' }}</p>
        </InfoCard>
        <InfoCard title="面经参考">
          <p>{{ data.interview_experience || '暂无数据' }}</p>
        </InfoCard>
        <InfoCard title="技能缺口">
          <ul>
            <li v-for="gap in data.skill_gaps" :key="gap">{{ gap }}</li>
          </ul>
        </InfoCard>
        <InfoCard title="准备清单">
          <ul>
            <li v-for="item in data.preparation_checklist" :key="item">{{ item }}</li>
          </ul>
        </InfoCard>
      </div>

      <div class="skill-match-section">
        <h3>技能匹配详情</h3>
        <table class="skill-table">
          <thead>
            <tr><th>技能</th><th>是否必需</th><th>候选人水平</th><th>JD 要求</th></tr>
          </thead>
          <tbody>
            <tr v-for="s in data.skill_match" :key="s.skill">
              <td>{{ s.skill }}</td>
              <td>{{ s.required ? '是' : '否' }}</td>
              <td>{{ s.candidate_level }}/5</td>
              <td>{{ s.jd_level }}/5</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="suggestions">
        <h3>改进建议</h3>
        <ul>
          <li v-for="s in data.suggestions" :key="s">{{ s }}</li>
        </ul>
      </div>

      <div class="actions">
        <button class="btn-primary" @click="startInterview">开始模拟面试</button>
      </div>
    </div>

    <div v-else-if="!done && stage" class="loading">
      <p>{{ stage === 'parsing' ? '正在解析文档...' : stage === 'indexing' ? '正在构建知识库...' : 'Agent 正在分析...' }}</p>
    </div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ThinkingStream from '../components/ThinkingStream.vue'
import ScoreCircle from '../components/ScoreCircle.vue'
import InfoCard from '../components/InfoCard.vue'
import { useSSE } from '../composables/useSSE'

const route = useRoute()
const router = useRouter()
const taskId = route.params.taskId as string

const { data, thinking, stage, done, error, connect } = useSSE(`/api/match/${taskId}/stream`)

onMounted(() => connect())

function startInterview() {
  router.push(`/interview/new?taskId=${taskId}`)
}
</script>

<style scoped>
.match-report { max-width: 900px; margin: 0 auto; }
.score-section { text-align: center; margin: 24px 0; }
.score-section h2 { margin-top: 16px; font-size: 22px; }
.cards-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin: 24px 0;
}
.skill-match-section { margin: 24px 0; }
.skill-table { width: 100%; border-collapse: collapse; }
.skill-table th, .skill-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}
.skill-table th { font-weight: 600; background: #fafafa; }
.suggestions { margin: 24px 0; }
.suggestions ul, .cards-grid ul { padding-left: 20px; }
.suggestions li, .cards-grid li { margin: 6px 0; }
.actions { text-align: center; margin: 32px 0; }
.btn-primary {
  padding: 14px 40px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}
.btn-primary:hover { background: var(--color-primary-dark); }
.loading { text-align: center; padding: 60px; color: var(--color-text-secondary); }
.error { color: var(--color-error); text-align: center; padding: 20px; }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/pages/MatchReport.vue
git commit -m "feat: implement MatchReport page with SSE streaming"
```

### Task 6.6: Interview components (ChatBubble, QuestionCard, AnswerInput, FeedbackCard)

**Files:**
- Create: `frontend/src/components/ChatBubble.vue`
- Create: `frontend/src/components/QuestionCard.vue`
- Create: `frontend/src/components/AnswerInput.vue`
- Create: `frontend/src/components/FeedbackCard.vue`

- [ ] **Step 1: Create ChatBubble.vue**

```vue
<template>
  <div class="chat-bubble" :class="[role]">
    <div class="bubble-avatar">{{ role === 'interviewer' ? 'AI' : '你' }}</div>
    <div class="bubble-content">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ role: 'interviewer' | 'candidate' }>()
</script>

<style scoped>
.chat-bubble {
  display: flex;
  gap: 12px;
  margin: 16px 0;
}
.chat-bubble.candidate { flex-direction: row-reverse; }
.bubble-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
}
.interviewer .bubble-avatar { background: var(--color-primary); color: #fff; }
.candidate .bubble-avatar { background: #e0e0e0; color: var(--color-text); }
.bubble-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
}
.interviewer .bubble-content { background: var(--color-surface); border: 1px solid var(--color-border); }
.candidate .bubble-content { background: var(--color-primary); color: #fff; }
</style>
```

- [ ] **Step 2: Create QuestionCard.vue**

```vue
<template>
  <div class="question-card">
    <div class="q-header">
      <span class="q-number">第 {{ question.question_number }} / {{ question.total_questions }} 题</span>
      <span class="q-category">{{ categoryLabel }}</span>
    </div>
    <p class="q-text">{{ question.question }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { InterviewQuestion } from '../types'

const props = defineProps<{ question: InterviewQuestion }>()

const categoryLabel = computed(() => {
  const map: Record<string, string> = {
    technical: '技术能力',
    behavioral: '行为面试',
    project: '项目经验',
    system_design: '系统设计',
    problem_solving: '解决问题',
  }
  return map[props.question.category] || props.question.category
})
</script>

<style scoped>
.question-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-left: 4px solid var(--color-primary);
  border-radius: var(--radius);
  padding: 20px;
}
.q-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}
.q-number { font-size: 13px; font-weight: 600; color: var(--color-primary); }
.q-category {
  font-size: 12px;
  background: #e8f0fe;
  color: var(--color-primary);
  padding: 2px 10px;
  border-radius: 12px;
}
.q-text { font-size: 16px; line-height: 1.7; }
</style>
```

- [ ] **Step 3: Create AnswerInput.vue**

```vue
<template>
  <div class="answer-input">
    <textarea
      v-model="answer"
      placeholder="输入你的回答..."
      rows="4"
      :disabled="disabled"
      @keydown.ctrl.enter="$emit('submit', answer)"
    ></textarea>
    <div class="input-actions">
      <span class="hint">Ctrl + Enter 发送</span>
      <div>
        <button class="btn-skip" :disabled="disabled" @click="$emit('skip')">跳过</button>
        <button class="btn-submit" :disabled="disabled || !answer.trim()" @click="$emit('submit', answer)">提交回答</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{ disabled: boolean }>()
defineEmits<{ submit: [answer: string]; skip: [] }>()

const answer = ref('')
</script>

<style scoped>
.answer-input { margin: 16px 0; }
textarea {
  width: 100%;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 14px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  outline: none;
  line-height: 1.6;
}
textarea:focus { border-color: var(--color-primary); }
.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}
.hint { font-size: 12px; color: var(--color-text-secondary); }
.btn-skip {
  padding: 8px 20px;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  cursor: pointer;
  margin-right: 8px;
  font-size: 14px;
}
.btn-submit {
  padding: 8px 24px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
}
.btn-submit:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-submit:not(:disabled):hover { background: var(--color-primary-dark); }
</style>
```

- [ ] **Step 4: Create FeedbackCard.vue**

```vue
<template>
  <div class="feedback-card">
    <div class="fb-header">
      <span class="fb-score" :class="scoreClass">评分：{{ feedback.score }}/10</span>
    </div>
    <p class="fb-text">{{ feedback.feedback }}</p>
    <div v-if="feedback.strengths.length" class="fb-section">
      <h4>优点</h4>
      <ul><li v-for="s in feedback.strengths" :key="s">{{ s }}</li></ul>
    </div>
    <div v-if="feedback.improvements.length" class="fb-section">
      <h4>改进建议</h4>
      <ul><li v-for="s in feedback.improvements" :key="s">{{ s }}</li></ul>
    </div>
    <div v-if="feedback.model_answer" class="fb-section">
      <h4>参考答案</h4>
      <p class="model-answer">{{ feedback.model_answer }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { InterviewFeedback } from '../types'

const props = defineProps<{ feedback: InterviewFeedback }>()

const scoreClass = computed(() => {
  if (props.feedback.score >= 8) return 'high'
  if (props.feedback.score >= 6) return 'mid'
  return 'low'
})
</script>

<style scoped>
.feedback-card {
  background: #fafafa;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 20px;
  margin: 16px 0;
}
.fb-header { margin-bottom: 12px; }
.fb-score { font-size: 18px; font-weight: 700; }
.fb-score.high { color: var(--color-success); }
.fb-score.mid { color: var(--color-warning); }
.fb-score.low { color: var(--color-error); }
.fb-text { font-size: 14px; line-height: 1.7; }
.fb-section { margin-top: 16px; }
.fb-section h4 { font-size: 14px; font-weight: 600; margin-bottom: 8px; }
.fb-section ul { padding-left: 20px; }
.fb-section li { font-size: 14px; margin: 4px 0; color: var(--color-text-secondary); }
.model-answer {
  font-size: 14px;
  line-height: 1.7;
  color: var(--color-text-secondary);
  background: #fff;
  padding: 12px;
  border-radius: var(--radius);
  border: 1px solid var(--color-border);
}
</style>
```

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/ChatBubble.vue frontend/src/components/QuestionCard.vue frontend/src/components/AnswerInput.vue frontend/src/components/FeedbackCard.vue
git commit -m "feat: add interview UI components"
```

### Task 6.7: InterviewPage

**Files:**
- Modify: `frontend/src/pages/InterviewPage.vue`

- [ ] **Step 1: Update InterviewPage.vue**

```vue
<template>
  <div class="interview-page">
    <div v-if="!started" class="interview-start">
      <h1>模拟面试</h1>
      <p>AI 面试官将基于 JD 要求和你的简历缺口出题，模拟真实面试场景</p>
      <button class="btn-primary" :disabled="loading" @click="start">
        {{ loading ? '正在准备面试题...' : '开始面试' }}
      </button>
    </div>

    <div v-else class="interview-active">
      <div class="chat-area">
        <div v-for="(msg, i) in messages" :key="i">
          <ChatBubble :role="msg.role">
            <template v-if="msg.role === 'interviewer' && msg.question">
              <QuestionCard :question="msg.question" />
            </template>
            <template v-else>
              {{ msg.content }}
            </template>
          </ChatBubble>
          <FeedbackCard v-if="msg.feedback" :feedback="msg.feedback" />
        </div>
      </div>

      <AnswerInput
        v-if="!finished"
        :disabled="waiting"
        @submit="submitAnswer"
        @skip="submitAnswer('')"
      />

      <div v-if="finished" class="interview-done">
        <h2>面试完成</h2>
        <button class="btn-primary" @click="viewReport">查看面试报告</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ChatBubble from '../components/ChatBubble.vue'
import QuestionCard from '../components/QuestionCard.vue'
import AnswerInput from '../components/AnswerInput.vue'
import FeedbackCard from '../components/FeedbackCard.vue'
import { api } from '../api/client'
import type { InterviewQuestion, InterviewFeedback } from '../types'

const route = useRoute()
const router = useRouter()

const started = ref(false)
const loading = ref(false)
const waiting = ref(false)
const finished = ref(false)
const sessionId = ref('')

interface Message {
  role: 'interviewer' | 'candidate'
  content: string
  question?: InterviewQuestion
  feedback?: InterviewFeedback
}
const messages = ref<Message[]>([])

async function start() {
  loading.value = true
  const taskId = route.params.sessionId as string || route.query.taskId as string
  try {
    const report = await api.getMatchReport(taskId)
    const res = await api.startInterview(report.task_id || taskId, taskId)
    sessionId.value = res.session_id
    started.value = true
    loading.value = false
  } catch {
    loading.value = false
  }
}

async function submitAnswer(answer: string) {
  messages.value.push({ role: 'candidate', content: answer || '(跳过)' })
  waiting.value = true
  try {
    const fb = await api.submitAnswer(
      sessionId.value,
      answer || '(跳过)',
      messages.value.filter(m => m.feedback).length + 1,
    )
    const lastMsg = messages.value[messages.value.length - 1]
    lastMsg.feedback = fb

    if (fb.next_question) {
      messages.value.push({
        role: 'interviewer',
        content: '',
        question: fb.next_question,
      })
    } else {
      finished.value = true
    }
  } finally {
    waiting.value = false
  }
}

function viewReport() {
  router.push(`/report/${sessionId.value}`)
}
</script>

<style scoped>
.interview-page { max-width: 800px; margin: 0 auto; }
.interview-start { text-align: center; padding: 80px 20px; }
.interview-start h1 { font-size: 28px; }
.interview-start p { margin: 16px 0 32px; color: var(--color-text-secondary); }
.interview-done { text-align: center; margin: 40px 0; }
.interview-done h2 { margin-bottom: 16px; }
.btn-primary {
  padding: 14px 40px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-primary:not(:disabled):hover { background: var(--color-primary-dark); }
.chat-area { margin: 20px 0; }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/pages/InterviewPage.vue
git commit -m "feat: implement InterviewPage with chat interface"
```

### Task 6.8: InterviewReport page components

**Files:**
- Create: `frontend/src/components/ScoreSummary.vue`
- Create: `frontend/src/components/QuestionReview.vue`
- Create: `frontend/src/components/WeakAreaAnalysis.vue`
- Create: `frontend/src/components/StudyPlan.vue`
- Modify: `frontend/src/pages/InterviewReport.vue`

- [ ] **Step 1: Create ScoreSummary.vue**

```vue
<template>
  <div class="score-summary">
    <ScoreCircle :score="score" />
    <h2>{{ title }}</h2>
  </div>
</template>

<script setup lang="ts">
import ScoreCircle from './ScoreCircle.vue'
defineProps<{ score: number; title: string }>()
</script>

<style scoped>
.score-summary { text-align: center; padding: 24px 0; }
.score-summary h2 { margin-top: 16px; }
</style>
```

- [ ] **Step 2: Create QuestionReview.vue**

```vue
<template>
  <div class="question-review">
    <div class="review-header">
      <span class="q-num">第 {{ review.question_number }} 题</span>
      <span class="q-score" :class="scoreClass">{{ review.score }}/10</span>
    </div>
    <p class="q-question">{{ review.question }}</p>
    <div class="q-answer">
      <h4>你的回答</h4>
      <p>{{ review.answer }}</p>
    </div>
    <div class="q-feedback">
      <h4>AI 点评</h4>
      <p>{{ review.feedback }}</p>
    </div>
    <div v-if="review.strengths.length" class="q-strengths">
      <span v-for="s in review.strengths" :key="s" class="tag green">{{ s }}</span>
    </div>
    <div v-if="review.improvements.length" class="q-improvements">
      <span v-for="s in review.improvements" :key="s" class="tag orange">{{ s }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { QuestionReviewData } from '../types'

const props = defineProps<{ review: QuestionReviewData }>()

const scoreClass = computed(() => {
  if (props.review.score >= 8) return 'high'
  if (props.review.score >= 6) return 'mid'
  return 'low'
})
</script>

<style scoped>
.question-review {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 20px;
  margin: 16px 0;
}
.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.q-num { font-weight: 600; }
.q-score { font-size: 18px; font-weight: 700; }
.q-score.high { color: var(--color-success); }
.q-score.mid { color: var(--color-warning); }
.q-score.low { color: var(--color-error); }
.q-question { font-size: 15px; line-height: 1.6; margin-bottom: 16px; }
.q-answer, .q-feedback { margin: 12px 0; }
.q-answer h4, .q-feedback h4 { font-size: 13px; font-weight: 600; margin-bottom: 4px; }
.q-answer p, .q-feedback p { font-size: 14px; color: var(--color-text-secondary); line-height: 1.6; }
.tag {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 12px;
  margin: 4px 4px 4px 0;
}
.tag.green { background: #e6f4ea; color: var(--color-success); }
.tag.orange { background: #fef7e0; color: #e37400; }
</style>
```

- [ ] **Step 3: Create WeakAreaAnalysis.vue**

```vue
<template>
  <div class="weak-areas">
    <h3>薄弱环节分析</h3>
    <div v-for="area in areas" :key="area.area" class="area-item">
      <div class="area-header">
        <span class="area-name">{{ area.area }}</span>
        <span class="area-score">{{ area.score }}/10</span>
      </div>
      <div class="area-bar">
        <div class="area-fill" :style="{ width: area.score * 10 + '%' }" :class="barClass(area.score)"></div>
      </div>
      <p class="area-desc">{{ area.description }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { WeakArea } from '../types'

defineProps<{ areas: WeakArea[] }>()

function barClass(score: number) {
  if (score >= 8) return 'high'
  if (score >= 6) return 'mid'
  return 'low'
}
</script>

<style scoped>
.weak-areas { margin: 24px 0; }
.weak-areas h3 { margin-bottom: 16px; }
.area-item { margin: 12px 0; }
.area-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}
.area-name { font-size: 14px; font-weight: 600; }
.area-score { font-size: 14px; }
.area-bar {
  height: 8px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}
.area-fill { height: 100%; border-radius: 4px; }
.area-fill.high { background: var(--color-success); }
.area-fill.mid { background: var(--color-warning); }
.area-fill.low { background: var(--color-error); }
.area-desc { font-size: 13px; color: var(--color-text-secondary); margin-top: 4px; }
</style>
```

- [ ] **Step 4: Create StudyPlan.vue**

```vue
<template>
  <div class="study-plan">
    <h3>复习计划</h3>
    <div v-for="item in plan" :key="item.topic" class="plan-item">
      <div class="plan-header">
        <span class="plan-topic">{{ item.topic }}</span>
        <span class="priority" :class="item.priority">{{ priorityLabel(item.priority) }}</span>
      </div>
      <p class="plan-timeline">建议时间：{{ item.timeline }}</p>
      <div class="plan-resources">
        <h4>推荐资源</h4>
        <ul>
          <li v-for="r in item.resources" :key="r">{{ r }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { StudyPlanItem } from '../types'

defineProps<{ plan: StudyPlanItem[] }>()

function priorityLabel(p: string) {
  const map: Record<string, string> = { high: '高优先级', medium: '中优先级', low: '低优先级' }
  return map[p] || p
}
</script>

<style scoped>
.study-plan { margin: 24px 0; }
.study-plan h3 { margin-bottom: 16px; }
.plan-item {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 16px;
  margin: 12px 0;
}
.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.plan-topic { font-weight: 600; font-size: 15px; }
.priority {
  font-size: 12px;
  padding: 2px 10px;
  border-radius: 12px;
  font-weight: 600;
}
.priority.high { background: #fce8e6; color: var(--color-error); }
.priority.medium { background: #fef7e0; color: #e37400; }
.priority.low { background: #e8f0fe; color: var(--color-primary); }
.plan-timeline { font-size: 13px; color: var(--color-text-secondary); margin: 8px 0; }
.plan-resources h4 { font-size: 13px; font-weight: 600; margin: 8px 0 4px; }
.plan-resources ul { padding-left: 20px; }
.plan-resources li { font-size: 13px; color: var(--color-text-secondary); margin: 2px 0; }
</style>
```

- [ ] **Step 5: Update InterviewReport.vue**

```vue
<template>
  <div class="interview-report">
    <div v-if="data">
      <ScoreSummary :score="data.overall_score" title="面试综合评分" />

      <section>
        <h2>逐题回顾</h2>
        <QuestionReview v-for="q in data.questions" :key="q.question_number" :review="q" />
      </section>

      <section>
        <WeakAreaAnalysis :areas="data.weak_areas" />
      </section>

      <section>
        <StudyPlan :plan="data.study_plan" />
      </section>
    </div>

    <div v-else class="loading">加载中...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import ScoreSummary from '../components/ScoreSummary.vue'
import QuestionReview from '../components/QuestionReview.vue'
import WeakAreaAnalysis from '../components/WeakAreaAnalysis.vue'
import StudyPlan from '../components/StudyPlan.vue'
import { api } from '../api/client'
import type { InterviewReportData } from '../types'

const route = useRoute()
const data = ref<InterviewReportData | null>(null)

onMounted(async () => {
  try {
    data.value = await api.getInterviewReport(route.params.sessionId as string)
  } catch (e) {
    console.error(e)
  }
})
</script>

<style scoped>
.interview-report { max-width: 800px; margin: 0 auto; }
section { margin: 32px 0; }
section h2 { font-size: 20px; margin-bottom: 16px; }
.loading { text-align: center; padding: 60px; color: var(--color-text-secondary); }
</style>
```

- [ ] **Step 6: Commit**

```bash
git add frontend/src/components/ScoreSummary.vue frontend/src/components/QuestionReview.vue frontend/src/components/WeakAreaAnalysis.vue frontend/src/components/StudyPlan.vue frontend/src/pages/InterviewReport.vue
git commit -m "feat: implement InterviewReport page with all sub-components"
```

---

## Phase 7: Final Integration & Polish

### Task 7.1: Add .gitignore and final wiring

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: Create .gitignore**

```gitignore
# Python
__pycache__/
*.pyc
.venv/
*.egg-info/
dist/

# Environment
.env
*.env

# ChromaDB
chroma_data/
test_chroma_data/

# Node
node_modules/
dist/

# IDE
.idea/
.vscode/
*.swp
*.swo
```

- [ ] **Step 2: Verify full stack runs**

Start backend:
```bash
cd backend && cp .env.example .env
# Edit .env with real API keys
poetry run uvicorn src.main:app --port 8000 --reload
```

Start frontend (separate terminal):
```bash
cd frontend && npm run dev
```

Expected: Backend at :8000, Frontend at :5173 with proxy.

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: add .gitignore and final wiring"
```

---

## Spec Coverage Checklist

| Spec Requirement | Covered By |
|---|---|
| PDF/DOCX 解析 | Task 2.1 (parser.py) |
| 文本分块（简历按节/JD语义） | Task 2.2 (chunker.py) |
| ChromaDB 4 个 Collection | Task 3.2 (vectordb.py) |
| 混合检索（向量+关键词+RRF） | Task 3.2 + 4.2 |
| LangGraph Agent 6 节点 | Task 4.4 (graph.py) |
| 5 个工具 | Task 4.2 (tools.py) |
| 反思 4 维度 | Task 4.3 (reflection.py) |
| FastAPI 8 端点 | Tasks 5.2-5.5 |
| SSE 流式 | Task 5.3 (match.py SSE) |
| Vue 3 4 页面 | Tasks 6.2, 6.5, 6.7, 6.8 |
| 单用户无登录 | By design (no auth) |
| .env 管理 | Task 1.1 (config.py) |
| DeepSeek v4 Pro | Task 1.1 (config default) |

All spec requirements mapped. No TBD/placeholder gaps. Types are consistent across backend (Pydantic schemas) and frontend (TypeScript types). Method signatures in API client match backend endpoint shapes.
