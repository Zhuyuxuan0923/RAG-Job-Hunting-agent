<template>
  <div class="interview-page">
    <div v-if="!started" class="interview-start">
      <h1>模拟面试</h1>
      <p>AI 面试官将基于 JD 要求和你的简历缺口出题，模拟真实面试场景</p>
      <div class="start-form">
        <label>输入 Task ID 开始面试</label>
        <input v-model="taskIdInput" placeholder="例如：a1b2c3d4" class="task-input" />
      </div>
      <button class="btn-primary" :disabled="loading || !taskIdInput" @click="start">
        {{ loading ? '正在准备面试题...' : '开始面试' }}
      </button>
    </div>

    <div v-else class="interview-active">
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
      </div>

      <AnswerInput
        v-if="!finished"
        :disabled="waiting"
        @submit="submitAnswer"
        @skip="submitAnswer('')"
      />

      <div v-if="finished" class="interview-done">
        <h2>面试完成</h2>
        <button class="btn-primary" @click="viewReport">查看面试报告</button>
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
.interview-start { text-align: center; padding: 80px 20px; }
.interview-start h1 { font-size: 28px; }
.interview-start p { margin: 16px 0 32px; color: var(--color-text-secondary); }
.start-form { margin: 16px 0; }
.start-form label { display: block; margin-bottom: 8px; font-size: 14px; color: var(--color-text-secondary); }
.task-input {
  padding: 10px 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  font-size: 14px;
  width: 240px;
  text-align: center;
  outline: none;
}
.task-input:focus { border-color: var(--color-primary); }
.interview-done { text-align: center; margin: 40px 0; }
.interview-done h2 { margin-bottom: 16px; }
.btn-primary {
  padding: 14px 40px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-primary:not(:disabled):hover { background: var(--color-primary-dark); }
.chat-area { margin: 20px 0; }
</style>
