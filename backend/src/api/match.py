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
        state.update(node_data)
        yield f"event: thinking\ndata: {json.dumps({'action': node_name, 'detail': str(node_data.get('next_action', '')), 'search_round': node_data.get('search_round', 0)}, ensure_ascii=False)}\n\n"

    try:
        raw = state.get("final_answer", "{}")
        result = json.loads(raw)
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
