export interface ResumeUploadResponse {
  resume_id: string
  filename: string
  parsed_text: string
}

export interface JDUploadResponse {
  jd_id: string
  title: string
  parsed_text: string
}

export interface MatchProgress {
  event: 'progress' | 'thinking' | 'result' | 'done'
  stage?: string
  action?: string
  detail?: string
  data?: MatchReport
}

export interface MatchReport {
  task_id: string
  overall_score: number
  skill_match: SkillMatchItem[]
  skill_gaps: string[]
  company_background: string
  interview_experience: string
  suggestions: string[]
  preparation_checklist: string[]
}

export interface SkillMatchItem {
  skill: string
  required: boolean
  candidate_level: number
  jd_level: number
}

export interface InterviewStartResponse {
  session_id: string
  total_questions: number
  first_question: InterviewQuestion | null
}

export interface InterviewQuestion {
  question_number: number
  total_questions: number
  question: string
  category: string
  expected_points: string[]
}

export interface InterviewFeedback {
  score: number
  feedback: string
  strengths: string[]
  improvements: string[]
  model_answer: string
  next_question: InterviewQuestion | null
}

export interface InterviewReportData {
  session_id: string
  overall_score: number
  questions: QuestionReviewData[]
  weak_areas: WeakArea[]
  study_plan: StudyPlanItem[]
}

export interface QuestionReviewData {
  question_number: number
  question: string
  answer: string
  score: number
  feedback: string
  strengths: string[]
  improvements: string[]
}

export interface WeakArea {
  area: string
  score: number
  description: string
}

export interface StudyPlanItem {
  topic: string
  priority: 'high' | 'medium' | 'low'
  resources: string[]
  timeline: string
}
