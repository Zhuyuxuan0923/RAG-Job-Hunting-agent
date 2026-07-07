<template>
  <div class="upload-page">
    <div class="page-hero">
      <h1 class="page-title">智能求职助手</h1>
      <p class="page-desc">上传简历和职位描述，AI 将为你生成岗位匹配分析并进行模拟面试</p>
    </div>

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
          <h2>个人简历</h2>
          <span v-if="resumeUploaded" class="column-badge done">已完成</span>
        </div>

        <template v-if="!resumeUploaded">
          <FileDropZone label="点击或拖拽上传简历文件" @file="handleResumeFile" />
          <div class="divider"><span>或直接粘贴</span></div>
          <TextPasteArea v-model="resumeText" placeholder="在此粘贴简历文本内容..." />
        </template>

        <div v-else class="upload-card">
          <div class="upload-card-icon">&#10003;</div>
          <div class="upload-card-title">简历解析完成</div>
          <div class="upload-card-filename">{{ resumeFilename }}</div>
          <div v-if="resumePreview" class="upload-card-preview">{{ resumePreview }}</div>
          <button class="btn-reset" @click="resetResume">重新上传</button>
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
          <h2>职位描述</h2>
          <span v-if="jdUploaded" class="column-badge done">已完成</span>
        </div>

        <template v-if="!jdUploaded">
          <FileDropZone label="点击或拖拽上传 JD 文件" @file="handleJDFile" />
          <div class="divider"><span>或直接粘贴</span></div>
          <TextPasteArea v-model="jdText" placeholder="在此粘贴 JD 文本内容..." />
        </template>

        <div v-else class="upload-card">
          <div class="upload-card-icon">&#10003;</div>
          <div class="upload-card-title">JD 解析完成</div>
          <div class="upload-card-filename">{{ jdFilename }}</div>
          <div v-if="jdPreview" class="upload-card-preview">{{ jdPreview }}</div>
          <button class="btn-reset" @click="resetJD">重新上传</button>
        </div>
      </div>
    </div>

    <div class="actions">
      <button class="btn-primary" :disabled="!canProceed" @click="startAnalysis">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
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

const canProceed = computed(() => resumeId.value && jdId.value)

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
  max-width: 1000px;
  margin: 0 auto;
}
.page-hero {
  text-align: center;
  margin-bottom: 28px;
}
.page-title {
  font-size: 30px;
  font-weight: 800;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, var(--color-primary) 0%, #7c3aed 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.page-desc {
  color: var(--color-text-secondary);
  margin-top: 10px;
  font-size: 15px;
  line-height: 1.6;
}

/* Steps indicator */
.steps-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  margin-bottom: 36px;
}
.step {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--color-text-secondary);
}
.step.active {
  color: var(--color-primary);
  font-weight: 600;
}
.step-num {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-secondary);
}
.step.active .step-num {
  background: var(--color-primary);
  color: #fff;
}
.step-divider {
  width: 48px;
  height: 2px;
  background: var(--color-border);
  margin: 0 12px;
}

/* Upload grid */
.upload-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
}
.upload-column {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 28px;
  transition: all 0.3s;
}
.upload-column.uploaded {
  border-color: var(--color-success);
  background: var(--color-success-light);
}
.column-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}
.column-icon {
  display: flex;
  color: var(--color-primary);
}
.column-header h2 {
  font-size: 17px;
  font-weight: 700;
  flex: 1;
}
.column-badge {
  font-size: 12px;
  padding: 3px 12px;
  border-radius: 20px;
  font-weight: 600;
}
.column-badge.done {
  background: var(--color-success);
  color: #fff;
}

/* Divider */
.divider {
  text-align: center;
  margin: 18px 0;
  color: var(--color-text-secondary);
  font-size: 13px;
  position: relative;
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

/* Upload card */
.upload-card {
  text-align: center;
  padding: 8px 0;
}
.upload-card-icon {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: var(--color-success);
  color: #fff;
  font-size: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 14px;
}
.upload-card-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--color-success);
  margin-bottom: 6px;
}
.upload-card-filename {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-bottom: 14px;
  word-break: break-all;
}
.upload-card-preview {
  text-align: left;
  font-size: 13px;
  color: var(--color-text-secondary);
  background: #fff;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  max-height: 110px;
  overflow-y: auto;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-all;
  margin-bottom: 14px;
}
.btn-reset {
  padding: 7px 22px;
  font-size: 13px;
  color: var(--color-text-secondary);
  background: #fff;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.15s;
  font-weight: 500;
}
.btn-reset:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

/* Actions */
.actions {
  text-align: center;
  margin-top: 40px;
}
.actions-hint {
  margin-top: 12px;
  font-size: 13px;
  color: var(--color-text-secondary);
}
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 15px 44px;
  background: linear-gradient(135deg, var(--color-primary) 0%, #7c3aed 100%);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3);
}
.btn-primary:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  box-shadow: none;
}
.btn-primary:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
}
.btn-primary:not(:disabled):active {
  transform: translateY(0);
}
</style>
