<template>
  <div class="upload-page">
    <h1 class="page-title">上传简历 & 职位描述</h1>
    <p class="page-desc">开始智能岗位匹配分析和模拟面试</p>

    <div class="upload-grid">
      <div class="upload-column">
        <h2>简历</h2>
        <FileDropZone label="上传简历文件" @file="handleResumeFile" />
        <div class="divider"><span>或</span></div>
        <TextPasteArea v-model="resumeText" placeholder="粘贴简历文本..." />
        <div v-if="resumeUploaded" class="upload-success">已解析 {{ resumeFilename }}</div>
      </div>

      <div class="upload-column">
        <h2>职位描述 (JD)</h2>
        <FileDropZone label="上传 JD 文件" @file="handleJDFile" />
        <div class="divider"><span>或</span></div>
        <TextPasteArea v-model="jdText" placeholder="粘贴 JD 文本..." />
        <div v-if="jdUploaded" class="upload-success">已解析 {{ jdFilename }}</div>
      </div>
    </div>

    <div class="actions">
      <button class="btn-primary" :disabled="!canProceed" @click="startAnalysis">
        开始匹配度分析
      </button>
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

const canProceed = computed(() => resumeId.value && jdId.value)

async function handleResumeFile(file: File) {
  const form = new FormData()
  form.append('file', file)
  const res = await api.uploadResume(form)
  resumeId.value = res.resume_id
  resumeFilename.value = res.filename
  resumeUploaded.value = true
}

async function handleJDFile(file: File) {
  const form = new FormData()
  form.append('file', file)
  const res = await api.uploadJD(form)
  jdId.value = res.jd_id
  jdFilename.value = res.title
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
.page-title { font-size: 28px; font-weight: 700; }
.page-desc { color: var(--color-text-secondary); margin: 8px 0 32px; }
.upload-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}
.upload-column h2 { font-size: 18px; margin-bottom: 16px; }
.divider {
  text-align: center;
  margin: 16px 0;
  color: var(--color-text-secondary);
  font-size: 13px;
}
.upload-success {
  margin-top: 12px;
  padding: 10px 16px;
  background: #e6f4ea;
  border-radius: var(--radius);
  color: var(--color-success);
  font-size: 14px;
}
.actions {
  text-align: center;
  margin-top: 40px;
}
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
.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.btn-primary:not(:disabled):hover {
  background: var(--color-primary-dark);
}
</style>
