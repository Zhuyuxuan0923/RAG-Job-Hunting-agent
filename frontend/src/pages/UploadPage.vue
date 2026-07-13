<template>
  <div
    class="upload-page"
    :style="{ '--pointer-x': `${pointerX}px`, '--pointer-y': `${pointerY}px` }"
    @pointermove="handlePointerMove"
  >
    <div class="sunlight-dust" aria-hidden="true">
      <span v-for="i in 26" :key="i"></span>
    </div>

    <section class="page-hero">
      <div>
        <h1 class="page-title">找到你的<span>光明未来</span></h1>
        <p class="page-desc">智能匹配职位机会，发现更适合你的职业道路。</p>
      </div>
    </section>

    <section class="assistant-card" aria-label="求职助手上传与匹配">
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
              <p>支持 PDF / DOCX / DOC，大小不超过 10MB。</p>
            </div>
            <span v-if="resumeUploaded" class="column-badge done">已完成</span>
          </div>

          <template v-if="!resumeUploaded">
            <FileDropZone label="简历上传" @file="handleResumeFile" />
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
              <p>上传 JD 文件，越详细匹配越精准。</p>
            </div>
            <span v-if="jdUploaded" class="column-badge done">已完成</span>
          </div>

          <template v-if="!jdUploaded">
            <FileDropZone label="上传 JD 文件" @file="handleJDFile" />
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
          <span class="btn-spark" aria-hidden="true">✧</span>
          立即匹配
        </button>
        <p class="actions-hint">{{ canProceed ? 'AI 将为你深度分析匹配度与机会' : '请先上传简历和 JD 后再开始分析' }}</p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import FileDropZone from '../components/FileDropZone.vue'
import { api } from '../api/client'

const router = useRouter()
const resumeId = ref('')
const jdId = ref('')
const resumeFilename = ref('')
const jdFilename = ref('')
const resumeUploaded = ref(false)
const jdUploaded = ref(false)
const resumePreview = ref('')
const jdPreview = ref('')
const pointerX = ref(0)
const pointerY = ref(0)

const canProceed = computed(() => {
  return Boolean(resumeId.value && jdId.value)
})

function previewText(text: string, maxLen = 200): string {
  return text.length > maxLen ? text.slice(0, maxLen) + '...' : text
}

function resetResume() {
  resumeId.value = ''
  resumeFilename.value = ''
  resumeUploaded.value = false
  resumePreview.value = ''
}

function resetJD() {
  jdId.value = ''
  jdFilename.value = ''
  jdUploaded.value = false
  jdPreview.value = ''
}

function handlePointerMove(e: PointerEvent) {
  const { innerWidth, innerHeight } = window
  pointerX.value = Number(((e.clientX / innerWidth - 0.5) * 14).toFixed(2))
  pointerY.value = Number(((e.clientY / innerHeight - 0.5) * 10).toFixed(2))
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
  const match = await api.startMatch(resumeId.value, jdId.value)
  router.push(`/match/${match.task_id}`)
}
</script>

<style scoped>
.upload-page {
  --pointer-x: 0px;
  --pointer-y: 0px;
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  padding: 96px 24px 70px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.1), rgba(255, 250, 239, 0.58)),
    url('../assets/sunlit-job-room.png') center / cover no-repeat;
}

.upload-page::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(circle at 52% 48%, rgba(255, 255, 255, 0.46), transparent 26rem),
    linear-gradient(105deg, rgba(255, 255, 255, 0.12), rgba(255, 244, 220, 0.46));
}

.upload-page::after {
  content: '';
  position: absolute;
  left: -8%;
  right: -8%;
  bottom: -12%;
  height: 34%;
  pointer-events: none;
  background: radial-gradient(ellipse at center, rgba(255, 255, 255, 0.68), transparent 64%);
  filter: blur(8px);
}

.sunlight-dust {
  position: absolute;
  inset: 0 0 auto;
  z-index: 1;
  height: 210px;
  pointer-events: none;
  transform: translate(calc(var(--pointer-x) * -0.28), calc(var(--pointer-y) * -0.24));
}

.sunlight-dust::before,
.sunlight-dust::after {
  content: '';
  position: absolute;
  left: 13%;
  right: 9%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 203, 96, 0.34), rgba(255, 255, 255, 0.84), rgba(255, 194, 68, 0.28), transparent);
  box-shadow: 0 0 16px rgba(255, 191, 73, 0.32);
  transform-origin: center;
}

.sunlight-dust::before {
  top: 48px;
  transform: rotate(4deg);
}

.sunlight-dust::after {
  top: 84px;
  transform: rotate(-2deg);
}

.sunlight-dust span {
  position: absolute;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: rgba(255, 204, 83, 0.82);
  box-shadow: 0 0 10px rgba(255, 204, 83, 0.72);
  animation: floatDust 8s ease-in-out infinite;
}

.sunlight-dust span:nth-child(3n) {
  width: 2px;
  height: 2px;
  background: rgba(255, 255, 255, 0.88);
}

.sunlight-dust span:nth-child(1) { left: 18%; top: 46px; animation-delay: -0.2s; }
.sunlight-dust span:nth-child(2) { left: 23%; top: 70px; animation-delay: -1.5s; }
.sunlight-dust span:nth-child(3) { left: 29%; top: 36px; animation-delay: -2.6s; }
.sunlight-dust span:nth-child(4) { left: 35%; top: 92px; animation-delay: -3.3s; }
.sunlight-dust span:nth-child(5) { left: 41%; top: 58px; animation-delay: -0.9s; }
.sunlight-dust span:nth-child(6) { left: 46%; top: 31px; animation-delay: -4.8s; }
.sunlight-dust span:nth-child(7) { left: 50%; top: 79px; animation-delay: -1.2s; }
.sunlight-dust span:nth-child(8) { left: 55%; top: 52px; animation-delay: -5.1s; }
.sunlight-dust span:nth-child(9) { left: 61%; top: 88px; animation-delay: -2.1s; }
.sunlight-dust span:nth-child(10) { left: 66%; top: 39px; animation-delay: -3.8s; }
.sunlight-dust span:nth-child(11) { left: 70%; top: 72px; animation-delay: -0.4s; }
.sunlight-dust span:nth-child(12) { left: 76%; top: 55px; animation-delay: -4.4s; }
.sunlight-dust span:nth-child(13) { left: 82%; top: 97px; animation-delay: -2.8s; }
.sunlight-dust span:nth-child(14) { left: 88%; top: 42px; animation-delay: -6.1s; }
.sunlight-dust span:nth-child(15) { left: 20%; top: 108px; animation-delay: -4.9s; }
.sunlight-dust span:nth-child(16) { left: 31%; top: 114px; animation-delay: -5.8s; }
.sunlight-dust span:nth-child(17) { left: 44%; top: 126px; animation-delay: -2.2s; }
.sunlight-dust span:nth-child(18) { left: 58%; top: 119px; animation-delay: -1.1s; }
.sunlight-dust span:nth-child(19) { left: 72%; top: 128px; animation-delay: -3.1s; }
.sunlight-dust span:nth-child(20) { left: 84%; top: 112px; animation-delay: -0.7s; }
.sunlight-dust span:nth-child(n+21) { opacity: 0.52; top: 145px; }
.sunlight-dust span:nth-child(21) { left: 27%; animation-delay: -4.2s; }
.sunlight-dust span:nth-child(22) { left: 39%; animation-delay: -2.9s; }
.sunlight-dust span:nth-child(23) { left: 52%; animation-delay: -6.2s; }
.sunlight-dust span:nth-child(24) { left: 65%; animation-delay: -3.6s; }
.sunlight-dust span:nth-child(25) { left: 78%; animation-delay: -1.8s; }
.sunlight-dust span:nth-child(26) { left: 91%; animation-delay: -5.3s; }

.page-hero {
  position: relative;
  z-index: 2;
  max-width: 1040px;
  margin: 0 auto 24px;
  text-align: center;
  animation: riseIn 0.8s ease both;
}

.page-title {
  color: var(--color-text);
  font-size: clamp(40px, 5.2vw, 66px);
  font-weight: 280;
  line-height: 1.08;
  letter-spacing: 0;
}

.page-title span {
  color: #e89719;
  font-weight: 320;
}

.page-desc {
  max-width: 650px;
  margin: 14px auto 0;
  color: var(--color-text-secondary);
  font-size: 16px;
  line-height: 1.7;
}

.assistant-card {
  position: relative;
  z-index: 2;
  max-width: 980px;
  margin: 0 auto;
  padding: 34px 54px 38px;
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.64));
  border: 1px solid rgba(226, 179, 101, 0.72);
  border-radius: 26px;
  box-shadow: var(--shadow-lg), inset 0 1px 0 rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(22px) saturate(126%);
  transform: translate(calc(var(--pointer-x) * 0.18), calc(var(--pointer-y) * 0.14));
  animation: riseIn 0.9s 0.08s ease both;
}

.assistant-card::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  border-radius: inherit;
  background: radial-gradient(circle at 50% 91%, rgba(255, 180, 50, 0.16), transparent 15rem);
}

.steps-indicator {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 26px;
  padding: 0 0 4px;
  background: transparent;
  border: 0;
  box-shadow: none;
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
  background: rgba(255, 255, 255, 0.76);
  border: 1px solid var(--color-border);
  border-radius: 999px;
  font-size: 13px;
  font-weight: 850;
}

.step.active .step-num {
  color: #fff;
  background: var(--color-primary);
  border-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0 6px 14px rgba(244, 123, 18, 0.24);
}

.step-divider {
  width: 56px;
  height: 1px;
  margin: 0 14px;
  background: linear-gradient(90deg, rgba(244, 123, 18, 0.4), rgba(185, 167, 134, 0.2));
}

.upload-grid {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 22px;
}

.upload-grid::before {
  content: '';
  position: absolute;
  top: 4px;
  bottom: 4px;
  left: 50%;
  width: 1px;
  background: linear-gradient(180deg, transparent, rgba(197, 153, 85, 0.32), transparent);
  transform: translateX(-11px);
}

.upload-column {
  position: relative;
  z-index: 1;
  padding: 24px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  box-shadow: var(--shadow-sm);
  transition: border-color 0.18s, box-shadow 0.18s, transform 0.18s;
}

.upload-column:hover {
  border-color: rgba(244, 123, 18, 0.42);
  box-shadow: var(--shadow);
  transform: translateY(-2px);
}

.upload-column.uploaded {
  border-color: rgba(79, 143, 58, 0.34);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.76) 0%, rgba(238, 248, 230, 0.82) 100%);
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
  background: rgba(255, 241, 216, 0.9);
  border: 1px solid rgba(244, 123, 18, 0.14);
  border-radius: 13px;
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
  border: 1px solid rgba(79, 143, 58, 0.24);
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
  background: linear-gradient(135deg, #6da845, #4f8f3a);
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
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 13px;
  font-weight: 700;
  transition: border-color 0.15s, color 0.15s, background 0.15s;
}

.btn-reset:hover {
  color: var(--color-primary);
  background: #fff8ea;
  border-color: rgba(244, 123, 18, 0.3);
}

.actions {
  position: relative;
  z-index: 1;
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
  min-height: 62px;
  min-width: 280px;
  padding: 16px 48px;
  color: #fff;
  background: linear-gradient(180deg, #ff9f2b 0%, #ff7a0b 58%, #ee6506 100%);
  border: 1px solid rgba(255, 233, 184, 0.76);
  border-radius: 999px;
  box-shadow: 0 16px 34px rgba(244, 123, 18, 0.34), 0 0 0 6px rgba(255, 166, 47, 0.08);
  cursor: pointer;
  font-size: 24px;
  font-weight: 760;
  transition: background 0.15s, border-color 0.15s, transform 0.15s, box-shadow 0.15s;
}

.btn-primary:disabled {
  opacity: 0.72;
  filter: grayscale(0.2);
  box-shadow: 0 10px 22px rgba(127, 100, 59, 0.14);
}

.btn-primary:not(:disabled):hover {
  background: linear-gradient(180deg, #ffad3f 0%, #ff7a0b 58%, #dd5a04 100%);
  border-color: var(--color-primary-dark);
  box-shadow: 0 20px 42px rgba(244, 123, 18, 0.42), 0 0 0 12px rgba(255, 166, 47, 0.1);
  transform: translateY(-2px) scale(1.025);
}

.btn-spark {
  font-size: 22px;
  line-height: 1;
}

@keyframes riseIn {
  from {
    opacity: 0;
    translate: 0 22px;
  }

  to {
    opacity: 1;
    translate: 0 0;
  }
}

@keyframes floatDust {
  0%, 100% {
    transform: translate3d(0, 0, 0);
    opacity: 0.42;
  }

  50% {
    transform: translate3d(12px, -10px, 0);
    opacity: 1;
  }
}

@media (prefers-reduced-motion: reduce) {
  .sunlight-dust span,
  .page-hero,
  .assistant-card {
    animation: none;
  }

  .assistant-card,
  .sunlight-dust {
    transform: none;
  }
}

@media (max-width: 820px) {
  .upload-page {
    padding: 38px 18px 52px;
  }

  .assistant-card {
    padding: 26px 22px 32px;
  }

  .steps-indicator {
    justify-content: flex-start;
    overflow-x: auto;
  }

  .upload-grid {
    grid-template-columns: 1fr;
  }

  .upload-grid::before {
    display: none;
  }
}

@media (max-width: 560px) {
  .upload-page {
    min-height: 100vh;
    padding: 82px 14px 42px;
  }

  .page-title {
    font-size: 36px;
  }

  .step-divider {
    width: 34px;
    margin: 0 10px;
  }

  .upload-column {
    padding: 18px;
  }

  .btn-primary {
    min-width: 100%;
    font-size: 21px;
  }
}
</style>
