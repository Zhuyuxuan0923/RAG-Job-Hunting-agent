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

THINKING_DISABLED = {"thinking": {"type": "disabled"}}

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
返回 JSON 数组：
[
  {{"question": "...", "category": "...", "expected_points": ["..."]}}
]"""}],
        temperature=0.8,
        extra_body=THINKING_DISABLED,
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
        extra_body=THINKING_DISABLED,
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
        extra_body=THINKING_DISABLED,
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
