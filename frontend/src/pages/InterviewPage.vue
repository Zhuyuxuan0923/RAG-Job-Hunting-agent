<template>
  <div class="interview-page">
    <div v-if="!started" class="interview-start">
      <div class="start-card">
        <div class="start-icon">
          <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
            <line x1="12" y1="19" x2="12" y2="23"/>
            <line x1="8" y1="23" x2="16" y2="23"/>
          </svg>
        </div>
        <h1>模拟面试</h1>
        <p>AI 面试官将基于 JD 要求和你的简历缺口出题，模拟真实面试场景。</p>
        <div class="start-form">
          <label for="task-id">输入 Match Task ID 开始面试</label>
          <input id="task-id" v-model="taskIdInput" placeholder="例如：a1b2c3d4" class="task-input" />
        </div>
        <button class="btn-primary" type="button" :disabled="loading || !taskIdInput" @click="start">
          {{ loading ? '正在准备面试题...' : '开始面试' }}
        </button>
      </div>
    </div>

    <div v-else class="interview-active">
      <div class="interview-header">
        <span class="interview-badge">AI 面试进行中</span>
        <span class="interview-progress">
          {{ messages.filter(m => m.feedback).length }} / {{ totalQuestions || '...' }}
        </span>
      </div>

      <div class="chat-area">
        <div v-for="(msg, i) in messages" :key="i">
          <ChatBubble :role="msg.role">
            <template v-if="msg.role === 'interviewer' && msg.question">
              <QuestionCard :question="msg.question" />
            </template>
            <template v-else>
              {{ msg.content }}
            </template>
          </ChatBubble>
          <FeedbackCard v-if="msg.feedback" :feedback="msg.feedback" />
        </div>

        <div v-if="waiting" class="typing-indicator" aria-label="AI 正在思考">
          <span></span><span></span><span></span>
        </div>
      </div>

      <AnswerInput
        v-if="!finished"
        :disabled="waiting"
        @submit="submitAnswer"
        @skip="submitAnswer('')"
      />

      <div v-if="finished" class="interview-done">
        <div class="done-card">
          <div class="done-icon">✓</div>
          <h2>面试完成</h2>
          <p>所有问题已回答完毕，可以查看详细面试报告。</p>
          <button class="btn-primary" type="button" @click="viewReport">查看面试报告</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ChatBubble from '../components/ChatBubble.vue'
import QuestionCard from '../components/QuestionCard.vue'
import AnswerInput from '../components/AnswerInput.vue'
import FeedbackCard from '../components/FeedbackCard.vue'
import { api } from '../api/client'
import type { InterviewQuestion, InterviewFeedback } from '../types'

const route = useRoute()
const router = useRouter()

const started = ref(false)
const loading = ref(false)
const waiting = ref(false)
const finished = ref(false)
const sessionId = ref('')
const totalQuestions = ref(0)
const taskIdInput = ref(route.params.sessionId as string || '')

interface Message {
  role: 'interviewer' | 'candidate'
  content: string
  question?: InterviewQuestion
  feedback?: InterviewFeedback
}
const messages = ref<Message[]>([])

async function start() {
  loading.value = true
  try {
    const matchReport = await api.getMatchReport(taskIdInput.value)
    const resumeId = matchReport.resume_id || matchReport.task_id
    const jdId = matchReport.jd_id || matchReport.task_id
    const res = await api.startInterview(resumeId, jdId)
    sessionId.value = res.session_id
    totalQuestions.value = res.total_questions
    if (res.first_question) {
      messages.value.push({ role: 'interviewer', content: '', question: res.first_question })
    }
    started.value = true
    loading.value = false
  } catch {
    loading.value = false
  }
}

async function submitAnswer(answer: string) {
  const qNum = messages.value.filter(m => m.feedback).length + 1
  messages.value.push({ role: 'candidate', content: answer || '(跳过)' })
  waiting.value = true
  try {
    const fb = await api.submitAnswer(sessionId.value, answer || '(跳过)', qNum)
    const lastMsg = messages.value[messages.value.length - 1]
    lastMsg.feedback = fb
    if (fb.next_question) {
      messages.value.push({ role: 'interviewer', content: '', question: fb.next_question })
    } else {
      finished.value = true
    }
  } finally {
    waiting.value = false
  }
}

function viewReport() {
  router.push(`/report/${sessionId.value}`)
}
</script>

<style scoped>
.interview-page {
  max-width: 860px;
  margin: 0 auto;
}

.interview-start {
  padding: 34px 0;
}

.start-card {
  max-width: 680px;
  margin: 0 auto;
  padding: 42px 38px;
  text-align: center;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
}

.start-icon {
  width: 78px;
  height: 78px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 18px;
  color: var(--color-primary);
  background: var(--color-primary-light);
  border-radius: 22px;
}

.start-card h1 {
  margin-bottom: 10px;
  color: var(--color-text);
  font-size: 28px;
  font-weight: 850;
  line-height: 1.25;
}

.start-card p {
  max-width: 520px;
  margin: 0 auto 26px;
  color: var(--color-text-secondary);
  font-size: 15px;
  line-height: 1.75;
}

.start-form {
  margin: 18px 0;
}

.start-form label {
  display: block;
  margin-bottom: 8px;
  color: var(--color-text-secondary);
  font-size: 14px;
  font-weight: 650;
}

.task-input {
  width: min(100%, 320px);
  padding: 12px 16px;
  color: var(--color-text);
  background: #fff;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  font-family: var(--font-mono);
  font-size: 15px;
  letter-spacing: 0;
  text-align: center;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.task-input:focus {
  border-color: var(--color-primary);
  box-shadow: var(--focus-ring);
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 46px;
  padding: 12px 32px;
  color: #fff;
  background: var(--color-primary);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius);
  box-shadow: 0 12px 24px rgba(37, 99, 235, 0.2);
  cursor: pointer;
  font-size: 15px;
  font-weight: 800;
  transition: background 0.15s, border-color 0.15s, transform 0.15s, box-shadow 0.15s;
}

.btn-primary:disabled {
  opacity: 0.45;
  box-shadow: none;
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-primary-dark);
  border-color: var(--color-primary-dark);
  transform: translateY(-1px);
}

.interview-active {
  padding-bottom: 20px;
}

.interview-header {
  position: sticky;
  top: 72px;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
  padding: 12px 0;
  background: rgba(246, 248, 251, 0.86);
  backdrop-filter: blur(10px);
}

.interview-badge {
  padding: 6px 12px;
  color: var(--color-primary);
  background: var(--color-primary-light);
  border: 1px solid #bfdbfe;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 800;
}

.interview-progress {
  color: var(--color-text-secondary);
  font-size: 14px;
  font-weight: 750;
}

.chat-area {
  margin: 12px 0;
}

.typing-indicator {
  display: flex;
  width: fit-content;
  gap: 5px;
  margin: 12px 0;
  padding: 13px 16px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xs);
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: var(--color-text-secondary);
  border-radius: 999px;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
  0%, 60%, 100% { opacity: 0.3; transform: translateY(0); }
  30% { opacity: 1; transform: translateY(-4px); }
}

.interview-done {
  margin: 36px 0;
}

.done-card {
  padding: 42px 34px;
  text-align: center;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.done-icon {
  width: 62px;
  height: 62px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  color: #fff;
  background: var(--color-success);
  border-radius: 18px;
  font-size: 28px;
  font-weight: 900;
}

.done-card h2 {
  margin-bottom: 8px;
  color: var(--color-text);
  font-size: 24px;
  font-weight: 850;
}

.done-card p {
  margin-bottom: 22px;
  color: var(--color-text-secondary);
}

@media (max-width: 640px) {
  .interview-start {
    padding: 12px 0;
  }

  .start-card {
    padding: 32px 22px;
  }

  .interview-header {
    top: 62px;
  }
}
</style>
