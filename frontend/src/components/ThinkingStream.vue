<template>
  <div class="thinking-stream">
    <div class="stream-header">
      <span class="pulse"></span>
      Agent 思考过程
    </div>
    <div class="stream-body" ref="bodyRef">
      <div v-for="(item, i) in items" :key="i" class="think-item">
        <span class="think-action">{{ item.action }}</span>
        <span class="think-detail">{{ item.detail }}</span>
        <span v-if="item.search_round" class="think-round">第 {{ item.search_round }} 轮</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { watch, ref } from 'vue'

const props = defineProps<{ items: Array<{ action: string; detail: string; search_round: number }> }>()
const bodyRef = ref<HTMLElement>()

watch(() => props.items.length, () => {
  if (bodyRef.value) {
    bodyRef.value.scrollTop = bodyRef.value.scrollHeight
  }
})
</script>

<style scoped>
.thinking-stream {
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  background: #fafafa;
  margin: 16px 0;
}
.stream-header {
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 600;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  gap: 8px;
}
.pulse {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-success);
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}
.stream-body {
  max-height: 300px;
  overflow-y: auto;
  padding: 12px 16px;
  font-size: 13px;
}
.think-item {
  padding: 6px 0;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  gap: 8px;
  align-items: center;
}
.think-action {
  background: var(--color-primary);
  color: #fff;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  white-space: nowrap;
}
.think-detail {
  color: var(--color-text-secondary);
  flex: 1;
}
.think-round {
  font-size: 11px;
  color: var(--color-text-secondary);
}
</style>
