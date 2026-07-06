<template>
  <div class="feedback-card">
    <div class="fb-header">
      <span class="fb-score" :class="scoreClass">评分：{{ feedback.score }}/10</span>
    </div>
    <p class="fb-text">{{ feedback.feedback }}</p>
    <div v-if="feedback.strengths.length" class="fb-section">
      <h4>优点</h4>
      <ul><li v-for="s in feedback.strengths" :key="s">{{ s }}</li></ul>
    </div>
    <div v-if="feedback.improvements.length" class="fb-section">
      <h4>改进建议</h4>
      <ul><li v-for="s in feedback.improvements" :key="s">{{ s }}</li></ul>
    </div>
    <div v-if="feedback.model_answer" class="fb-section">
      <h4>参考答案</h4>
      <p class="model-answer">{{ feedback.model_answer }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { InterviewFeedback } from '../types'

const props = defineProps<{ feedback: InterviewFeedback }>()

const scoreClass = computed(() => {
  if (props.feedback.score >= 8) return 'high'
  if (props.feedback.score >= 6) return 'mid'
  return 'low'
})
</script>

<style scoped>
.feedback-card {
  background: #fafafa;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 20px;
  margin: 16px 0;
}
.fb-header { margin-bottom: 12px; }
.fb-score { font-size: 18px; font-weight: 700; }
.fb-score.high { color: var(--color-success); }
.fb-score.mid { color: var(--color-warning); }
.fb-score.low { color: var(--color-error); }
.fb-text { font-size: 14px; line-height: 1.7; }
.fb-section { margin-top: 16px; }
.fb-section h4 { font-size: 14px; font-weight: 600; margin-bottom: 8px; }
.fb-section ul { padding-left: 20px; }
.fb-section li { font-size: 14px; margin: 4px 0; color: var(--color-text-secondary); }
.model-answer {
  font-size: 14px;
  line-height: 1.7;
  color: var(--color-text-secondary);
  background: #fff;
  padding: 12px;
  border-radius: var(--radius);
  border: 1px solid var(--color-border);
}
</style>
