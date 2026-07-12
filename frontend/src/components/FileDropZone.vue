<template>
  <div
    class="drop-zone"
    :class="{ 'drag-over': dragging }"
    @click="fileInput?.click()"
    @dragover.prevent="dragging = true"
    @dragleave.prevent="dragging = false"
    @drop.prevent="handleDrop"
  >
    <div class="drop-content">
      <div class="drop-icon">
        <svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="17 8 12 3 7 8"/>
          <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
      </div>
      <p class="drop-text">{{ label }}</p>
      <p class="drop-hint">支持 PDF / DOCX / DOC，最大 10MB</p>
      <input ref="fileInput" type="file" accept=".pdf,.docx,.doc" @change="onFileSelect" hidden />
      <button class="btn-select" type="button" @click.stop="fileInput?.click()">选择文件</button>
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
  border: 1.5px dashed #cbd5e1;
  border-radius: var(--radius-lg);
  padding: 34px 24px;
  text-align: center;
  transition: border-color 0.18s, background 0.18s, transform 0.18s, box-shadow 0.18s;
  cursor: pointer;
  background: linear-gradient(180deg, #ffffff 0%, var(--color-surface-soft) 100%);
}

.drop-zone:hover,
.drop-zone.drag-over {
  border-color: var(--color-primary);
  background: #f8fbff;
  box-shadow: var(--focus-ring);
}

.drop-zone.drag-over {
  transform: translateY(-2px);
}

.drop-icon {
  width: 62px;
  height: 62px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 14px;
  color: var(--color-primary);
  background: var(--color-primary-light);
  border-radius: 18px;
}

.drop-text {
  font-size: 15px;
  font-weight: 700;
  color: var(--color-text);
}

.drop-hint {
  margin-top: 4px;
  font-size: 13px;
  color: var(--color-text-secondary);
}

.btn-select {
  margin-top: 16px;
  padding: 8px 18px;
  color: #fff;
  background: var(--color-primary);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s, transform 0.15s;
}

.btn-select:hover {
  background: var(--color-primary-dark);
  border-color: var(--color-primary-dark);
  transform: translateY(-1px);
}
</style>
