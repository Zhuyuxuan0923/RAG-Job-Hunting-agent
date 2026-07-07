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
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-left: 4px solid var(--color-primary);
  border-radius: var(--radius);
  padding: 20px 24px;
  box-shadow: var(--shadow-xs);
}
.q-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}
.q-number {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-primary);
}
.q-category {
  font-size: 12px;
  font-weight: 600;
  background: var(--color-primary-light);
  color: var(--color-primary);
  padding: 3px 12px;
  border-radius: 14px;
}
.q-text {
  font-size: 16px;
  line-height: 1.75;
  color: var(--color-text);
}
</style>
