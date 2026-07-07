<template>
  <div class="interview-page">
    <div v-if="!started" class="interview-start">
      <div class="start-card">
        <div class="start-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
            <line x1="12" y1="19" x2="12" y2="23"/>
            <line x1="8" y1="23" x2="16" y2="23"/>
          </svg>
        </div>
        <h1>模拟面试</h1>
        <p>AI 面试官将基于 JD 要求和你的简历缺口出题，模拟真实面试场景</p>
        <div class="start-form">
          <label>输入 Match Task ID 开始面试</label>
          <input v-model="taskIdInput" placeholder="例如：a1b2c3d4" class="task-input" />
        </div>
        <button class="btn-primary" :disabled="loading || !taskIdInput" @click="start">
          {{ loading ? '正在准备面试题...' : '开始面试' }}
        </button>
      </div>
    </div>

    <div v-else class="interview-active">
      <div class="interview-header">
        <span class="interview-badge">AI 面试进行中</span>
        <span class="interview-progress">
          {{ messages.filter(m => m.feedback).length }} / {{ messages.filter(m => m.role === 'interviewer' && m.question).length + messages.filter(m => m.feedback).length || '...' }}
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

        <div v-if="waiting" class="typing-indicator">
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
          <div class="done-icon">&#10003;</div>
          <h2>面试完成</h2>
          <p>所有问题已回答完毕，可以查看详细面试报告</p>
          <button class="btn-primary" @click="viewReport">查看面试报告</button>
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
    const res = await api.startInterview(matchReport.task_id, matchReport.task_id)
    sessionId.value = res.session_id
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
.interview-page { max-width: 800px; margin: 0 auto; }

/* Start */
.interview-start {
  padding: 40px 20px;
}
.start-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: 48px 40px;
  text-align: center;
  box-shadow: var(--shadow);
}
.start-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--color-primary-light);
  color: var(--color-primary);
  margin-bottom: 20px;
}
.start-card h1 {
  font-size: 26px;
  font-weight: 800;
  margin-bottom: 10px;
}
.start-card p {
  color: var(--color-text-secondary);
  font-size: 15px;
  margin-bottom: 28px;
  line-height: 1.6;
}
.start-form { margin: 16px 0; }
.start-form label { display: block; margin-bottom: 8px; font-size: 14px; color: var(--color-text-secondary); }
.task-input {
  padding: 12px 18px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  font-size: 15px;
  width: 260px;
  text-align: center;
  outline: none;
  transition: border-color 0.15s;
  font-family: var(--font-mono);
  letter-spacing: 1px;
}
.task-input:focus { border-color: var(--color-primary); box-shadow: 0 0 0 3px var(--color-primary-light); }

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 38px;
  background: linear-gradient(135deg, var(--color-primary) 0%, #7c3aed 100%);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3);
  margin-top: 8px;
}
.btn-primary:disabled { opacity: 0.4; cursor: not-allowed; box-shadow: none; }
.btn-primary:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
}

/* Active interview header */
.interview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 0;
  margin-bottom: 12px;
}
.interview-badge {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-primary);
  background: var(--color-primary-light);
  padding: 5px 14px;
  border-radius: 20px;
}
.interview-progress {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-secondary);
}

/* Chat area */
.chat-area {
  margin: 16px 0;
}

/* Typing indicator */
.typing-indicator {
  display: flex;
  gap: 5px;
  padding: 14px 18px;
  margin: 12px 0;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  width: fit-content;
}
.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-text-secondary);
  animation: typing 1.4s infinite;
}
.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing {
  0%, 60%, 100% { opacity: 0.3; transform: translateY(0); }
  30% { opacity: 1; transform: translateY(-4px); }
}

/* Done */
.interview-done {
  margin: 40px 0;
}
.done-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: 48px 40px;
  text-align: center;
  box-shadow: var(--shadow);
}
.done-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--color-success);
  color: #fff;
  font-size: 30px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 18px;
}
.done-card h2 {
  font-size: 24px;
  font-weight: 800;
  margin-bottom: 10px;
}
.done-card p {
  color: var(--color-text-secondary);
  margin-bottom: 24px;
}
</style>
