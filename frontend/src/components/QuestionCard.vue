<template>
  <div class="question-card">
    <div class="q-header">
      <span class="q-number">第 {{ question.question_number }} / {{ question.total_questions }} 题</span>
      <span class="q-category">{{ categoryLabel }}</span>
    </div>
    <p class="q-text">{{ question.question }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { InterviewQuestion } from '../types'

const props = defineProps<{ question: InterviewQuestion }>()

const categoryLabel = computed(() => {
  const map: Record<string, string> = {
    technical: '技术能力',
    behavioral: '行为面试',
    project: '项目经验',
    system_design: '系统设计',
    problem_solving: '解决问题',
  }
  return map[props.question.category] || props.question.category
})
</script>

<style scoped>
.question-card {
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
  border: 1px solid var(--color-border);
  border-left: 4px solid var(--color-primary);
  border-radius: var(--radius-lg);
  padding: 18px 20px;
  box-shadow: var(--shadow-xs);
}

.q-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.q-number {
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 800;
}

.q-category {
  flex-shrink: 0;
  padding: 4px 11px;
  color: var(--color-accent);
  background: var(--color-accent-light);
  border-radius: 999px;
  font-size: 12px;
  font-weight: 750;
}

.q-text {
  color: var(--color-text);
  font-size: 16px;
  line-height: 1.75;
}

@media (max-width: 520px) {
  .q-header {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
