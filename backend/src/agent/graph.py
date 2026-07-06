import json
from langgraph.graph import StateGraph, END
from openai import OpenAI
from src.config import settings
from src.agent.state import AgentState
from src.agent.tools import search_resume, search_jd, web_search, compare_skills
from src.agent.reflection import reflect, should_continue
from src.agent.prompts import (
    CLASSIFY_PROMPT, PLAN_PROMPT, GENERATE_MATCH_PROMPT,
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
