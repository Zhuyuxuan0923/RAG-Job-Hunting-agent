<template>
  <div
    class="drop-zone"
    :class="{ 'drag-over': dragging }"
    @dragover.prevent="dragging = true"
    @dragleave.prevent="dragging = false"
    @drop.prevent="handleDrop"
  >
    <div class="drop-content">
      <div class="drop-icon">
        <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="17 8 12 3 7 8"/>
          <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
      </div>
      <p class="drop-text">{{ label }}</p>
      <p class="drop-hint">支持 PDF / DOCX 格式，最大 10MB</p>
      <input ref="fileInput" type="file" accept=".pdf,.docx,.doc" @change="onFileSelect" hidden />
      <button class="btn-select" @click="fileInput?.click()">选择文件</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{ label: string }>()
const emit = defineEmits<{ file: [file: File] }>()

const dragging = ref(false)
const fileInput = ref<HTMLInputElement>()

function handleDrop(e: DragEvent) {
  dragging.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) emit('file', file)
}

function onFileSelect(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) emit('file', file)
}
</script>

<style scoped>
.drop-zone {
  border: 2px dashed #d0d0d8;
  border-radius: var(--radius);
  padding: 36px 24px;
  text-align: center;
  transition: all 0.2s;
  cursor: pointer;
  background: #fafafc;
}
.drop-zone:hover {
  border-color: var(--color-primary);
  background: var(--color-primary-light);
}
.drop-zone.drag-over {
  border-color: var(--color-primary);
  background: var(--color-primary-light);
  transform: scale(1.01);
}
.drop-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--color-primary-light);
  color: var(--color-primary);
  margin-bottom: 14px;
  transition: transform 0.2s;
}
.drag-over .drop-icon {
  transform: translateY(-4px);
}
.drop-text {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
}
.drop-hint {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-top: 4px;
}
.btn-select {
  margin-top: 16px;
  padding: 8px 22px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-select:hover {
  background: var(--color-primary-dark);
  transform: translateY(-1px);
}
</style>
