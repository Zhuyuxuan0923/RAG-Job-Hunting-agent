<template>
  <div class="study-plan">
    <h3>复习计划</h3>
    <div class="plan-list">
      <div v-for="item in plan" :key="item.topic" class="plan-card">
        <div class="plan-header">
          <div class="plan-left">
            <span class="plan-topic">{{ item.topic }}</span>
            <span class="plan-timeline">{{ item.timeline }}</span>
          </div>
          <span class="plan-priority" :class="item.priority">{{ priorityLabel(item.priority) }}</span>
        </div>
        <div class="plan-resources">
          <h4>推荐资源</h4>
          <ul>
            <li v-for="r in item.resources" :key="r">{{ r }}</li>
          </ul>
        </div>
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
.study-plan { margin: 28px 0; }
.study-plan h3 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 16px;
}
.plan-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.plan-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 18px 22px;
  box-shadow: var(--shadow-xs);
  transition: box-shadow 0.2s;
}
.plan-card:hover {
  box-shadow: var(--shadow-sm);
}
.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 14px;
}
.plan-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.plan-topic { font-weight: 700; font-size: 15px; }
.plan-timeline { font-size: 13px; color: var(--color-text-secondary); }
.plan-priority {
  font-size: 12px;
  padding: 4px 14px;
  border-radius: 14px;
  font-weight: 700;
  flex-shrink: 0;
}
.plan-priority.high { background: var(--color-error-light); color: var(--color-error); }
.plan-priority.medium { background: var(--color-warning-light); color: #d97706; }
.plan-priority.low { background: var(--color-primary-light); color: var(--color-primary); }
.plan-resources {
  padding: 12px 14px;
  background: #fafafc;
  border-radius: var(--radius-sm);
}
.plan-resources h4 {
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--color-text-secondary);
}
.plan-resources ul { padding-left: 18px; }
.plan-resources li {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: 3px 0;
  line-height: 1.5;
}
</style>
