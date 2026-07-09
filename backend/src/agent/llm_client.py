"""
Centralized LLM client and structured-output helpers.

All LLM calls that need structured JSON output should use call_with_tool()
so that the model emits valid JSON via function-calling / tool-use, with a
fallback to plain prompt-based JSON parsing.
"""

import json
import logging
from typing import Any
from openai import OpenAI
from src.config import settings

logging.basicConfig(level=logging.INFO, format="[%(name)s] %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

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


def _parse_json_from_content(content: str) -> Any:
    """Try to extract and parse JSON from raw LLM text output."""
    if not content:
        raise json.JSONDecodeError("empty content", "", 0)
    cleaned = content
    if "```" in cleaned:
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()
    return json.loads(cleaned)


def call_with_tool(
    *,
    messages: list[dict],
    tools: list[dict],
    tool_choice: dict | str = "auto",
    temperature: float = 0.7,
    default: Any = None,
) -> Any:
    """Call the LLM with tool-use for structured JSON output.

    Tries, in order:
      1. Parse tool_call arguments (primary path)
      2. Parse message content as JSON (fallback 1 – same request)
      3. Retry WITHOUT tools, parsing content as JSON (fallback 2)
      4. Return `default`
    """
    client = get_client()
    tool_name = tools[0]["function"]["name"] if tools else "unknown"

    # ── Phase 1: try with tools ──────────────────────────────
    try:
        resp = client.chat.completions.create(
            model=settings.model_name,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            temperature=temperature,
            extra_body=THINKING_DISABLED,
        )
        msg = resp.choices[0].message

        # Path 1 – tool call
        if msg.tool_calls:
            try:
                result = json.loads(msg.tool_calls[0].function.arguments)
                logger.info(f"[{tool_name}] tool call OK, {len(msg.tool_calls[0].function.arguments)} bytes")
                return result
            except (json.JSONDecodeError, AttributeError, IndexError) as e:
                logger.warning(f"[{tool_name}] tool call args parse failed: {e} | raw={msg.tool_calls[0].function.arguments[:200] if msg.tool_calls else 'N/A'}")

        # Path 2 – content fallback (same response)
        content = msg.content or ""
        try:
            result = _parse_json_from_content(content)
            logger.info(f"[{tool_name}] content parse OK (from tool request)")
            return result
        except json.JSONDecodeError:
            logger.warning(f"[{tool_name}] content parse failed | preview={content[:300]}")

    except Exception as e:
        logger.error(f"[{tool_name}] API call failed: {e}")

    # ── Phase 2: retry without tools ─────────────────────────
    logger.info(f"[{tool_name}] retrying without tools (plain prompt mode)...")
    try:
        resp = client.chat.completions.create(
            model=settings.model_name,
            messages=messages,
            temperature=temperature,
            extra_body=THINKING_DISABLED,
        )
        content = resp.choices[0].message.content or ""
        try:
            result = _parse_json_from_content(content)
            logger.info(f"[{tool_name}] plain prompt retry OK")
            return result
        except json.JSONDecodeError:
            logger.warning(f"[{tool_name}] plain prompt retry parse failed | preview={content[:300]}")
    except Exception as e:
        logger.error(f"[{tool_name}] plain prompt retry API error: {e}")

    # ── Phase 3: return default ──────────────────────────────
    logger.warning(f"[{tool_name}] all paths failed, returning default")
    if default is not None:
        return default
    raise RuntimeError(f"[{tool_name}] all structured-output paths failed")


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
