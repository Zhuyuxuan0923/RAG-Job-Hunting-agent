from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.services.vectordb import VectorStore
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


@app.get("/api/health")
async def health():
    return {"status": "ok"}
