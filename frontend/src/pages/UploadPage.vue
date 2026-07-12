<template>
  <div class="upload-page">
    <section class="page-hero">
      <div>
        <h1 class="page-title">智能求职准备工作台</h1>
        <p class="page-desc">上传简历和职位描述，AI 将生成岗位匹配分析，并继续引导模拟面试。</p>
      </div>
      <div class="hero-meta">
        <span>RAG 分析</span>
        <span>面试追问</span>
        <span>复习计划</span>
      </div>
    </section>

    <div class="steps-indicator">
      <div class="step active">
        <div class="step-num">1</div>
        <span>上传资料</span>
      </div>
      <div class="step-divider"></div>
      <div class="step">
        <div class="step-num">2</div>
        <span>匹配分析</span>
      </div>
      <div class="step-divider"></div>
      <div class="step">
        <div class="step-num">3</div>
        <span>模拟面试</span>
      </div>
    </div>

    <div class="upload-grid">
      <div class="upload-column" :class="{ uploaded: resumeUploaded }">
        <div class="column-header">
          <span class="column-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
            </svg>
          </span>
          <div>
            <h2>个人简历</h2>
            <p>上传文件或粘贴文本，生成候选人能力画像。</p>
          </div>
          <span v-if="resumeUploaded" class="column-badge done">已完成</span>
        </div>

        <template v-if="!resumeUploaded">
          <FileDropZone label="点击或拖拽上传简历文件" @file="handleResumeFile" />
          <div class="divider"><span>或直接粘贴</span></div>
          <TextPasteArea v-model="resumeText" placeholder="在此粘贴简历文本内容..." />
        </template>

        <div v-else class="upload-card">
          <div class="upload-card-icon">✓</div>
          <div class="upload-card-title">简历解析完成</div>
          <div class="upload-card-filename">{{ resumeFilename }}</div>
          <div v-if="resumePreview" class="upload-card-preview">{{ resumePreview }}</div>
          <button class="btn-reset" type="button" @click="resetResume">重新上传</button>
        </div>
      </div>

      <div class="upload-column" :class="{ uploaded: jdUploaded }">
        <div class="column-header">
          <span class="column-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
              <line x1="8" y1="21" x2="16" y2="21"/>
              <line x1="12" y1="17" x2="12" y2="21"/>
            </svg>
          </span>
          <div>
            <h2>职位描述</h2>
            <p>提供 JD，让 Agent 对齐岗位要求和考察重点。</p>
          </div>
          <span v-if="jdUploaded" class="column-badge done">已完成</span>
        </div>

        <template v-if="!jdUploaded">
          <FileDropZone label="点击或拖拽上传 JD 文件" @file="handleJDFile" />
          <div class="divider"><span>或直接粘贴</span></div>
          <TextPasteArea v-model="jdText" placeholder="在此粘贴 JD 文本内容..." />
        </template>

        <div v-else class="upload-card">
          <div class="upload-card-icon">✓</div>
          <div class="upload-card-title">JD 解析完成</div>
          <div class="upload-card-filename">{{ jdFilename }}</div>
          <div v-if="jdPreview" class="upload-card-preview">{{ jdPreview }}</div>
          <button class="btn-reset" type="button" @click="resetJD">重新上传</button>
        </div>
      </div>
    </div>

    <div class="actions">
      <button class="btn-primary" type="button" :disabled="!canProceed" @click="startAnalysis">
        <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <polygon points="5 3 19 12 5 21 5 3"/>
        </svg>
        开始匹配度分析
      </button>
      <p v-if="!canProceed" class="actions-hint">请先上传简历和 JD 后再开始分析</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import FileDropZone from '../components/FileDropZone.vue'
import TextPasteArea from '../components/TextPasteArea.vue'
import { api } from '../api/client'

const router = useRouter()
const resumeText = ref('')
const jdText = ref('')
const resumeId = ref('')
const jdId = ref('')
const resumeFilename = ref('')
const jdFilename = ref('')
const resumeUploaded = ref(false)
const jdUploaded = ref(false)
const resumePreview = ref('')
const jdPreview = ref('')

const canProceed = computed(() => {
  const hasResume = Boolean(resumeId.value || resumeText.value.trim())
  const hasJD = Boolean(jdId.value || jdText.value.trim())
  return hasResume && hasJD
})

function previewText(text: string, maxLen = 200): string {
  return text.length > maxLen ? text.slice(0, maxLen) + '...' : text
}

function resetResume() {
  resumeId.value = ''
  resumeFilename.value = ''
  resumeUploaded.value = false
  resumePreview.value = ''
  resumeText.value = ''
}

function resetJD() {
  jdId.value = ''
  jdFilename.value = ''
  jdUploaded.value = false
  jdPreview.value = ''
  jdText.value = ''
}

async function handleResumeFile(file: File) {
  const form = new FormData()
  form.append('file', file)
  const res = await api.uploadResume(form)
  resumeId.value = res.resume_id
  resumeFilename.value = res.filename
  resumePreview.value = previewText(res.parsed_text)
  resumeUploaded.value = true
}

async function handleJDFile(file: File) {
  const form = new FormData()
  form.append('file', file)
  const res = await api.uploadJD(form)
  jdId.value = res.jd_id
  jdFilename.value = res.title
  jdPreview.value = previewText(res.parsed_text)
  jdUploaded.value = true
}

async function startAnalysis() {
  if (resumeText.value && !resumeId.value) {
    const res = await api.uploadResume({ text: resumeText.value })
    resumeId.value = res.resume_id
  }
  if (jdText.value && !jdId.value) {
    const res = await api.uploadJD({ text: jdText.value })
    jdId.value = res.jd_id
  }
  const match = await api.startMatch(resumeId.value, jdId.value)
  router.push(`/match/${match.task_id}`)
}
</script>

<style scoped>
.upload-page {
  max-width: 1040px;
  margin: 0 auto;
}

.page-hero {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 24px;
}

.page-title {
  color: var(--color-text);
  font-size: 34px;
  font-weight: 850;
  line-height: 1.18;
  letter-spacing: 0;
}

.page-desc {
  max-width: 650px;
  margin-top: 10px;
  color: var(--color-text-secondary);
  font-size: 15px;
  line-height: 1.7;
}

.hero-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.hero-meta span {
  padding: 6px 11px;
  color: var(--color-accent);
  background: var(--color-accent-light);
  border: 1px solid #99f6e4;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 750;
}

.steps-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 28px;
  padding: 14px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xs);
}

.step {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--color-text-secondary);
  font-size: 14px;
  font-weight: 650;
  white-space: nowrap;
}

.step.active {
  color: var(--color-primary);
}

.step-num {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-secondary);
  background: #e2e8f0;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 850;
}

.step.active .step-num {
  color: #fff;
  background: var(--color-primary);
}

.step-divider {
  width: 56px;
  height: 1px;
  margin: 0 14px;
  background: var(--color-border);
}

.upload-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 22px;
}

.upload-column {
  padding: 24px;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: border-color 0.18s, box-shadow 0.18s, transform 0.18s;
}

.upload-column:hover {
  border-color: #cbd5e1;
  box-shadow: var(--shadow);
}

.upload-column.uploaded {
  border-color: rgba(5, 150, 105, 0.32);
  background: linear-gradient(180deg, #ffffff 0%, var(--color-success-light) 100%);
}

.column-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 18px;
}

.column-icon {
  width: 40px;
  height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: var(--color-primary);
  background: var(--color-primary-light);
  border-radius: 12px;
}

.column-header h2 {
  color: var(--color-text);
  font-size: 17px;
  font-weight: 800;
  line-height: 1.3;
}

.column-header p {
  margin-top: 3px;
  color: var(--color-text-secondary);
  font-size: 13px;
  line-height: 1.5;
}

.column-badge {
  margin-left: auto;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 800;
  white-space: nowrap;
}

.column-badge.done {
  color: var(--color-success);
  background: var(--color-success-light);
  border: 1px solid #bbf7d0;
}

.divider {
  position: relative;
  margin: 18px 0;
  color: var(--color-text-secondary);
  font-size: 13px;
  text-align: center;
}

.divider::before,
.divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 35%;
  height: 1px;
  background: var(--color-border);
}

.divider::before { left: 0; }
.divider::after { right: 0; }

.divider span {
  position: relative;
  z-index: 1;
  padding: 0 10px;
  background: #fff;
}

.upload-card {
  padding: 8px 0 2px;
  text-align: center;
}

.upload-card-icon {
  width: 54px;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 14px;
  color: #fff;
  background: var(--color-success);
  border-radius: 16px;
  font-size: 24px;
  font-weight: 900;
  box-shadow: 0 10px 20px rgba(5, 150, 105, 0.18);
}

.upload-card-title {
  margin-bottom: 6px;
  color: var(--color-success);
  font-size: 17px;
  font-weight: 800;
}

.upload-card-filename {
  margin-bottom: 14px;
  color: var(--color-text-secondary);
  font-size: 13px;
  word-break: break-all;
}

.upload-card-preview {
  max-height: 128px;
  overflow-y: auto;
  margin-bottom: 14px;
  padding: 12px 14px;
  color: var(--color-text-secondary);
  background: #fff;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  font-size: 13px;
  line-height: 1.65;
  text-align: left;
  white-space: pre-wrap;
  word-break: break-word;
}

.btn-reset {
  padding: 8px 18px;
  color: var(--color-text-secondary);
  background: #fff;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 13px;
  font-weight: 700;
  transition: border-color 0.15s, color 0.15s, background 0.15s;
}

.btn-reset:hover {
  color: var(--color-primary);
  background: #f8fbff;
  border-color: #bfdbfe;
}

.actions {
  margin-top: 32px;
  text-align: center;
}

.actions-hint {
  margin-top: 12px;
  color: var(--color-text-secondary);
  font-size: 13px;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 50px;
  padding: 14px 38px;
  color: #fff;
  background: var(--color-primary);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius);
  box-shadow: 0 12px 24px rgba(37, 99, 235, 0.2);
  cursor: pointer;
  font-size: 16px;
  font-weight: 800;
  transition: background 0.15s, border-color 0.15s, transform 0.15s, box-shadow 0.15s;
}

.btn-primary:disabled {
  opacity: 0.42;
  box-shadow: none;
}

.btn-primary:not(:disabled):hover {
  background: var(--color-primary-dark);
  border-color: var(--color-primary-dark);
  box-shadow: 0 16px 28px rgba(37, 99, 235, 0.24);
  transform: translateY(-1px);
}

@media (max-width: 820px) {
  .page-hero {
    align-items: flex-start;
    flex-direction: column;
  }

  .hero-meta {
    justify-content: flex-start;
  }

  .steps-indicator {
    justify-content: flex-start;
    overflow-x: auto;
  }

  .upload-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 560px) {
  .page-title {
    font-size: 28px;
  }

  .step-divider {
    width: 34px;
    margin: 0 10px;
  }

  .upload-column {
    padding: 20px;
  }
}
</style>
