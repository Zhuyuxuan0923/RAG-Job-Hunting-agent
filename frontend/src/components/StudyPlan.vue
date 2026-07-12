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
.study-plan {
  margin: 28px 0;
}

.study-plan h3 {
  margin-bottom: 16px;
  color: var(--color-text);
  font-size: 18px;
  font-weight: 800;
}

.plan-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.plan-card {
  padding: 18px 20px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xs);
  transition: border-color 0.18s, box-shadow 0.18s;
}

.plan-card:hover {
  border-color: #cbd5e1;
  box-shadow: var(--shadow-sm);
}

.plan-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 14px;
}

.plan-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.plan-topic {
  color: var(--color-text);
  font-size: 15px;
  font-weight: 800;
}

.plan-timeline {
  color: var(--color-text-secondary);
  font-size: 13px;
}

.plan-priority {
  flex-shrink: 0;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 800;
}

.plan-priority.high {
  color: var(--color-error);
  background: var(--color-error-light);
}

.plan-priority.medium {
  color: var(--color-warning);
  background: var(--color-warning-light);
}

.plan-priority.low {
  color: var(--color-primary);
  background: var(--color-primary-light);
}

.plan-resources {
  padding: 13px 14px;
  background: var(--color-surface-soft);
  border-radius: var(--radius);
}

.plan-resources h4 {
  margin-bottom: 7px;
  color: var(--color-text);
  font-size: 12px;
  font-weight: 800;
}

.plan-resources ul {
  padding-left: 18px;
}

.plan-resources li {
  margin: 3px 0;
  color: var(--color-text-secondary);
  font-size: 13px;
  line-height: 1.55;
}

@media (max-width: 560px) {
  .plan-header {
    flex-direction: column;
  }
}
</style>
