"""
Centralized LLM client and structured-output helpers.

All LLM calls that need structured JSON output should use call_with_tool()
so that the model is forced to emit valid JSON via function-calling / tool-use.
"""

import json
from typing import Any
from openai import OpenAI
from src.config import settings

THINKING_DISABLED = {"thinking": {"type": "disabled"}}

_client: OpenAI | None = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
        )
    return _client


def call_with_tool(
    *,
    messages: list[dict],
    tools: list[dict],
    tool_choice: dict | str = "auto",
    temperature: float = 0.7,
    default: Any = None,
) -> Any:
    """Call the LLM with tool-use for guaranteed structured JSON output.

    The primary path is to read the arguments from the forced tool call.
    If that fails (e.g. the provider doesn't support tool_choice="function"),
    falls back to parsing the message content as JSON (with markdown-fence
    stripping).  On total failure returns `default`.
    """
    client = get_client()
    resp = client.chat.completions.create(
        model=settings.model_name,
        messages=messages,
        tools=tools,
        tool_choice=tool_choice,
        temperature=temperature,
        extra_body=THINKING_DISABLED,
    )

    msg = resp.choices[0].message

    # Path 1 – the expected tool call
    if msg.tool_calls:
        try:
            return json.loads(msg.tool_calls[0].function.arguments)
        except (json.JSONDecodeError, AttributeError, IndexError):
            pass

    # Path 2 – fallback: parse content as JSON
    content = msg.content or ""
    if "```" in content:
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        if default is not None:
            return default
        raise


# ── Tool schemas ──────────────────────────────────────────────

TOOL_MATCH_REPORT = {
    "type": "function",
    "function": {
        "name": "output_match_report",
        "description": "输出职位匹配分析报告",
        "parameters": {
            "type": "object",
            "properties": {
                "overall_score": {
                    "type": "integer",
                    "description": "综合匹配度评分 0-100",
                },
                "skill_match": {
                    "type": "array",
                    "description": "逐项技能对比",
                    "items": {
                        "type": "object",
                        "properties": {
                            "skill": {"type": "string", "description": "技能名称"},
                            "required": {"type": "boolean", "description": "是否为JD硬性要求"},
                            "candidate_level": {"type": "integer", "description": "候选人掌握程度 1-10"},
                            "jd_level": {"type": "integer", "description": "JD要求程度 1-10"},
                        },
                        "required": ["skill", "required", "candidate_level", "jd_level"],
                    },
                },
                "skill_gaps": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "技能缺口列表",
                },
                "company_background": {
                    "type": "string",
                    "description": "公司背景和业务介绍",
                },
                "interview_experience": {
                    "type": "string",
                    "description": "面试经验和常见面试流程",
                },
                "suggestions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "具体改进建议",
                },
                "preparation_checklist": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "面试准备清单",
                },
            },
            "required": [
                "overall_score",
                "skill_match",
                "skill_gaps",
                "company_background",
                "interview_experience",
                "suggestions",
                "preparation_checklist",
            ],
        },
    },
}

TOOL_REFLECTION = {
    "type": "function",
    "function": {
        "name": "output_reflection",
        "description": "输出检索质量评估结果",
        "parameters": {
            "type": "object",
            "properties": {
                "coverage": {
                    "type": "object",
                    "properties": {
                        "pass": {"type": "boolean"},
                        "reason": {"type": "string"},
                    },
                    "required": ["pass", "reason"],
                },
                "consistency": {
                    "type": "object",
                    "properties": {
                        "pass": {"type": "boolean"},
                        "reason": {"type": "string"},
                    },
                    "required": ["pass", "reason"],
                },
                "freshness": {
                    "type": "object",
                    "properties": {
                        "pass": {"type": "boolean"},
                        "reason": {"type": "string"},
                    },
                    "required": ["pass", "reason"],
                },
                "sufficiency": {
                    "type": "object",
                    "properties": {
                        "pass": {"type": "boolean"},
                        "reason": {"type": "string"},
                    },
                    "required": ["pass", "reason"],
                },
                "overall_pass": {"type": "boolean"},
                "missing_queries": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "required": [
                "coverage",
                "consistency",
                "freshness",
                "sufficiency",
                "overall_pass",
                "missing_queries",
            ],
        },
    },
}

TOOL_INTERVIEW_QUESTIONS = {
    "type": "function",
    "function": {
        "name": "output_interview_questions",
        "description": "生成面试题目列表",
        "parameters": {
            "type": "object",
            "properties": {
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string", "description": "面试题内容"},
                            "category": {"type": "string", "description": "题目类别(技术能力/项目经验/行为面试/系统设计/解决问题)"},
                            "expected_points": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "期望回答要点",
                            },
                        },
                        "required": ["question", "category", "expected_points"],
                    },
                    "description": "面试题目列表",
                },
            },
            "required": ["questions"],
        },
    },
}

TOOL_ANSWER_EVALUATION = {
    "type": "function",
    "function": {
        "name": "output_answer_evaluation",
        "description": "输出面试回答评估",
        "parameters": {
            "type": "object",
            "properties": {
                "score": {"type": "integer", "description": "评分 0-10"},
                "feedback": {"type": "string", "description": "整体评价"},
                "strengths": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "优点列表",
                },
                "improvements": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "改进建议列表",
                },
                "model_answer": {"type": "string", "description": "参考答案"},
            },
            "required": ["score", "feedback", "strengths", "improvements", "model_answer"],
        },
    },
}

TOOL_INTERVIEW_REPORT = {
    "type": "function",
    "function": {
        "name": "output_interview_report",
        "description": "输出面试综合报告",
        "parameters": {
            "type": "object",
            "properties": {
                "weak_areas": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "area": {"type": "string", "description": "薄弱领域"},
                            "score": {"type": "integer", "description": "该领域评分 0-10"},
                            "description": {"type": "string", "description": "具体描述"},
                        },
                        "required": ["area", "score", "description"],
                    },
                },
                "study_plan": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "topic": {"type": "string", "description": "学习主题"},
                            "priority": {"type": "string", "description": "优先级 high/medium/low"},
                            "resources": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "学习资源",
                            },
                            "timeline": {"type": "string", "description": "建议时间线"},
                        },
                        "required": ["topic", "priority", "resources", "timeline"],
                    },
                },
            },
            "required": ["weak_areas", "study_plan"],
        },
    },
}
