import json
from typing import Dict, Any, List
from openai import OpenAI
from src.config import settings

THINKING_DISABLED = {"thinking": {"type": "disabled"}}


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
        extra_body=THINKING_DISABLED,
    )
    content = resp.choices[0].message.content or "{}"
    if "```" in content:
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()
    return json.loads(content)


def should_continue(reflection_result: Dict[str, Any], max_rounds: int, current_round: int) -> bool:
    if current_round >= max_rounds:
        return False
    if reflection_result.get("overall_pass", False):
        return False
    return True
