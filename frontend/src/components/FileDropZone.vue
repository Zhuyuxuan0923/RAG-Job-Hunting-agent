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
  border: 1.5px dashed rgba(244, 123, 18, 0.28);
  border-radius: var(--radius-lg);
  padding: 30px 24px;
  text-align: center;
  transition: border-color 0.18s, background 0.18s, transform 0.18s, box-shadow 0.18s;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.56);
}

.drop-zone:hover,
.drop-zone.drag-over {
  border-color: var(--color-primary);
  background: rgba(255, 248, 234, 0.82);
  box-shadow: 0 0 0 3px rgba(244, 123, 18, 0.12), 0 14px 30px rgba(244, 123, 18, 0.13);
}

.drop-zone.drag-over {
  transform: translateY(-2px);
}

.drop-icon {
  width: 58px;
  height: 58px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 14px;
  color: var(--color-primary);
  background: rgba(255, 241, 216, 0.86);
  border: 1px solid rgba(244, 123, 18, 0.16);
  border-radius: 17px;
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
  background: linear-gradient(180deg, #ff9d28 0%, #f27409 100%);
  border: 1px solid rgba(212, 102, 9, 0.7);
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 9px 20px rgba(244, 123, 18, 0.2);
  transition: background 0.15s, border-color 0.15s, transform 0.15s, box-shadow 0.15s;
}

.btn-select:hover {
  background: linear-gradient(180deg, #ffaa3b 0%, #e86506 100%);
  border-color: var(--color-primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 11px 26px rgba(244, 123, 18, 0.28);
}
</style>
