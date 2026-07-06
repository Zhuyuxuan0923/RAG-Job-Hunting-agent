const BASE = '/api'

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const headers: Record<string, string> = {}
  if (!(options?.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json'
  }
  const res = await fetch(`${BASE}${url}`, { headers, ...options })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}

export const api = {
  uploadResume: (body: FormData | { text: string }) =>
    request<import('../types').ResumeUploadResponse>('/resume/upload', {
      method: 'POST',
      body: body instanceof FormData ? body : JSON.stringify(body),
    }),

  uploadJD: (body: FormData | { text: string }) =>
    request<import('../types').JDUploadResponse>('/jd/upload', {
      method: 'POST',
      body: body instanceof FormData ? body : JSON.stringify(body),
    }),

  startMatch: (resumeId: string, jdId: string) =>
    request<{ task_id: string }>('/match', {
      method: 'POST',
      body: JSON.stringify({ resume_id: resumeId, jd_id: jdId }),
    }),

  startInterview: (resumeId: string, jdId: string) =>
    request<import('../types').InterviewStartResponse>('/interview/start', {
      method: 'POST',
      body: JSON.stringify({ resume_id: resumeId, jd_id: jdId }),
    }),

  submitAnswer: (sessionId: string, answer: string, questionNumber: number) =>
    request<import('../types').InterviewFeedback>(`/interview/${sessionId}/answer`, {
      method: 'POST',
      body: JSON.stringify({ answer, question_number: questionNumber }),
    }),

  getMatchReport: (taskId: string) =>
    request<import('../types').MatchReport>(`/match/${taskId}/report`),

  getInterviewReport: (sessionId: string) =>
    request<import('../types').InterviewReportData>(`/interview/${sessionId}/report`),
}
