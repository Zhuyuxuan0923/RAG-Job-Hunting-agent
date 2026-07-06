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
