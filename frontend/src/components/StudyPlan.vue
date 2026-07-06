<template>
  <div class="study-plan">
    <h3>复习计划</h3>
    <div v-for="item in plan" :key="item.topic" class="plan-item">
      <div class="plan-header">
        <span class="plan-topic">{{ item.topic }}</span>
        <span class="priority" :class="item.priority">{{ priorityLabel(item.priority) }}</span>
      </div>
      <p class="plan-timeline">建议时间：{{ item.timeline }}</p>
      <div class="plan-resources">
        <h4>推荐资源</h4>
        <ul>
          <li v-for="r in item.resources" :key="r">{{ r }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { StudyPlanItem } from '../types'

defineProps<{ plan: StudyPlanItem[] }>()

function priorityLabel(p: string) {
  const map: Record<string, string> = { high: '高优先级', medium: '中优先级', low: '低优先级' }
  return map[p] || p
}
</script>

<style scoped>
.study-plan { margin: 24px 0; }
.study-plan h3 { margin-bottom: 16px; }
.plan-item {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 16px;
  margin: 12px 0;
}
.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.plan-topic { font-weight: 600; font-size: 15px; }
.priority {
  font-size: 12px;
  padding: 2px 10px;
  border-radius: 12px;
  font-weight: 600;
}
.priority.high { background: #fce8e6; color: var(--color-error); }
.priority.medium { background: #fef7e0; color: #e37400; }
.priority.low { background: #e8f0fe; color: var(--color-primary); }
.plan-timeline { font-size: 13px; color: var(--color-text-secondary); margin: 8px 0; }
.plan-resources h4 { font-size: 13px; font-weight: 600; margin: 8px 0 4px; }
.plan-resources ul { padding-left: 20px; }
.plan-resources li { font-size: 13px; color: var(--color-text-secondary); margin: 2px 0; }
</style>
