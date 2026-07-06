<template>
  <div
    class="drop-zone"
    :class="{ 'drag-over': dragging }"
    @dragover.prevent="dragging = true"
    @dragleave.prevent="dragging = false"
    @drop.prevent="handleDrop"
  >
    <div class="drop-content">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M12 16V4m0 0L8 8m4-4l4 4M4 20h16"/>
      </svg>
      <p class="drop-text">{{ label }}</p>
      <p class="drop-hint">支持 PDF / DOCX 格式</p>
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
  border: 2px dashed var(--color-border);
  border-radius: var(--radius);
  padding: 32px;
  text-align: center;
  transition: border-color 0.2s, background 0.2s;
  cursor: pointer;
  background: var(--color-surface);
}
.drop-zone.drag-over {
  border-color: var(--color-primary);
  background: #e8f0fe;
}
.drop-text {
  font-size: 16px;
  font-weight: 600;
  margin-top: 12px;
}
.drop-hint {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-top: 4px;
}
.btn-select {
  margin-top: 16px;
  padding: 8px 20px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 14px;
  cursor: pointer;
}
.btn-select:hover {
  background: var(--color-primary-dark);
}
</style>
