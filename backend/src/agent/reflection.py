import json
from typing import Dict, Any, List
from src.agent.llm_client import call_with_tool, TOOL_REFLECTION


def reflect(search_results: List[Dict], sub_queries: List[str], intent: str) -> Dict[str, Any]:
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
4. **充分性(sufficiency)**: 现有信息足够高质量回答吗？"""

    return call_with_tool(
        messages=[{"role": "user", "content": prompt}],
        tools=[TOOL_REFLECTION],
        tool_choice={"type": "function", "function": {"name": "output_reflection"}},
        temperature=0.3,
        default={
            "coverage": {"pass": True, "reason": ""},
            "consistency": {"pass": True, "reason": ""},
            "freshness": {"pass": True, "reason": ""},
            "sufficiency": {"pass": True, "reason": ""},
            "overall_pass": True,
            "missing_queries": [],
        },
    )


def should_continue(reflection_result: Dict[str, Any], max_rounds: int, current_round: int) -> bool:
    if current_round >= max_rounds:
        return False
    if reflection_result.get("overall_pass", False):
        return False
    return True
