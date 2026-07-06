from pydantic import BaseModel, Field
from typing import List, Optional


class TextUpload(BaseModel):
    text: str


class ResumeUploadResponse(BaseModel):
    resume_id: str
    filename: str
    parsed_text: str


class JDUploadResponse(BaseModel):
    jd_id: str
    title: str
    parsed_text: str


class MatchRequest(BaseModel):
    resume_id: str
    jd_id: str


class MatchTaskResponse(BaseModel):
    task_id: str


class SkillMatchItem(BaseModel):
    skill: str
    required: bool
    candidate_level: int = Field(default=0)
    jd_level: int = Field(default=0)


class MatchReportResponse(BaseModel):
    task_id: str
    overall_score: int
    skill_match: List[SkillMatchItem]
    skill_gaps: List[str]
    company_background: str
    interview_experience: str
    suggestions: List[str]
    preparation_checklist: List[str]


class InterviewStartRequest(BaseModel):
    resume_id: str
    jd_id: str


class InterviewStartResponse(BaseModel):
    session_id: str
    total_questions: int


class AnswerRequest(BaseModel):
    answer: str
    question_number: int


class InterviewQuestion(BaseModel):
    question_number: int
    total_questions: int
    question: str
    category: str
    expected_points: List[str]


class InterviewFeedback(BaseModel):
    score: int
    feedback: str
    strengths: List[str]
    improvements: List[str]
    model_answer: str
    next_question: Optional[InterviewQuestion] = None


class QuestionReview(BaseModel):
    question_number: int
    question: str
    answer: str
    score: int
    feedback: str
    strengths: List[str]
    improvements: List[str]


class WeakArea(BaseModel):
    area: str
    score: int
    description: str


class StudyPlanItem(BaseModel):
    topic: str
    priority: str
    resources: List[str]
    timeline: str


class InterviewReportResponse(BaseModel):
    session_id: str
    overall_score: int
    questions: List[QuestionReview]
    weak_areas: List[WeakArea]
    study_plan: List[StudyPlanItem]
