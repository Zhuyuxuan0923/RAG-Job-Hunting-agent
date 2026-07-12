<template>
  <div v-if="items.length" class="thinking-stream">
    <div class="stream-header">
      <span class="pulse"></span>
      <span>Agent 思考过程</span>
    </div>
    <div ref="bodyRef" class="stream-body">
      <div v-for="(item, i) in items" :key="i" class="think-item">
        <span class="think-action">{{ labelOf(item.action) }}</span>
        <span class="think-detail">{{ detailOf(item.action) }}</span>
        <span v-if="item.search_round" class="think-round">第 {{ item.search_round }} 轮</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { watch, ref } from 'vue'

const props = defineProps<{ items: Array<{ action: string; detail: string; search_round: number }> }>()
const bodyRef = ref<HTMLElement>()

const LABELS: Record<string, string> = {
  classify: '意图识别',
  plan: '检索规划',
  search: '信息检索',
  fuse: '结果融合',
  reflect: '质量反思',
  generate: '生成报告',
}

const DETAILS: Record<string, string> = {
  classify: '正在分析用户意图...',
  plan: '正在拆解检索子问题...',
  search: '正在搜索简历、JD 和网络信息...',
  fuse: '正在去重并整合检索结果...',
  reflect: '正在评估检索质量，必要时补充搜索...',
  generate: '正在生成岗位匹配度分析报告...',
}

function labelOf(action: string): string {
  return LABELS[action] || action
}

function detailOf(action: string): string {
  return DETAILS[action] || ''
}

watch(() => props.items.length, () => {
  if (bodyRef.value) {
    bodyRef.value.scrollTop = bodyRef.value.scrollHeight
  }
})
</script>

<style scoped>
.thinking-stream {
  overflow: hidden;
  margin: 0 0 20px;
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xs);
}

.stream-header {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 12px 16px;
  color: var(--color-text);
  background: var(--color-surface-soft);
  border-bottom: 1px solid var(--color-border);
  font-size: 14px;
  font-weight: 750;
}

.pulse {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: var(--color-success);
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.45; transform: scale(0.82); }
}

.stream-body {
  max-height: 260px;
  overflow-y: auto;
  padding: 10px 14px;
  font-size: 13px;
}

.think-item {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 8px 0;
  border-bottom: 1px solid #eef2f7;
}

.think-item:last-child {
  border-bottom: none;
}

.think-action {
  flex-shrink: 0;
  min-width: 72px;
  padding: 3px 8px;
  color: var(--color-primary);
  background: var(--color-primary-light);
  border-radius: 999px;
  font-size: 12px;
  font-weight: 750;
  text-align: center;
}

.think-detail {
  flex: 1;
  color: var(--color-text-secondary);
}

.think-round {
  flex-shrink: 0;
  color: var(--color-text-secondary);
  font-size: 12px;
}

@media (max-width: 640px) {
  .think-item {
    align-items: flex-start;
    flex-direction: column;
    gap: 5px;
  }
}
</style>
