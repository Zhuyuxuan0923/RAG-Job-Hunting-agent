import json
from langchain_core.tools import tool
from src.services.vectordb import VectorStore
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
    """对比简历技能和JD要求技能，输出结构化的差异分析。"""
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
    """基于技能缺口生成面试题目。category: technical/behavioral/project, difficulty: easy/medium/hard"""
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
