<template>
  <div class="thinking-stream">
    <div class="stream-header">
      <span class="pulse"></span>
      Agent 思考过程
    </div>
    <div class="stream-body" ref="bodyRef">
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
  fuse: '正在去重和整合检索结果...',
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
