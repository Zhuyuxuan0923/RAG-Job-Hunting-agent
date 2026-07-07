<template>
  <div class="feedback-card">
    <div class="fb-header">
      <span class="fb-score" :class="scoreClass">{{ feedback.score }}<small>/10</small></span>
      <span class="fb-label">AI 评分</span>
    </div>
    <p class="fb-text">{{ feedback.feedback }}</p>
    <div v-if="feedback.strengths.length" class="fb-section strengths">
      <h4>优点</h4>
      <ul><li v-for="s in feedback.strengths" :key="s">{{ s }}</li></ul>
    </div>
    <div v-if="feedback.improvements.length" class="fb-section improvements">
      <h4>改进建议</h4>
      <ul><li v-for="s in feedback.improvements" :key="s">{{ s }}</li></ul>
    </div>
    <div v-if="feedback.model_answer" class="fb-section model">
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
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 22px 24px;
  margin: 14px 0;
  box-shadow: var(--shadow-xs);
}
.fb-header {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 14px;
}
.fb-score {
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.5px;
}
.fb-score small {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
}
.fb-score.high { color: var(--color-success); }
.fb-score.mid { color: var(--color-warning); }
.fb-score.low { color: var(--color-error); }
.fb-label {
  font-size: 13px;
  color: var(--color-text-secondary);
  font-weight: 500;
}
.fb-text {
  font-size: 14px;
  line-height: 1.7;
  color: var(--color-text);
  margin-bottom: 6px;
}
.fb-section {
  margin-top: 16px;
  padding: 14px 16px;
  border-radius: var(--radius-sm);
}
.fb-section.strengths {
  background: var(--color-success-light);
}
.fb-section.improvements {
  background: var(--color-warning-light);
}
.fb-section.model {
  background: var(--color-primary-light);
}
.fb-section h4 {
  font-size: 13px;
  font-weight: 700;
  margin-bottom: 8px;
}
.fb-section ul {
  padding-left: 20px;
}
.fb-section li {
  font-size: 13px;
  margin: 4px 0;
  color: var(--color-text-secondary);
  line-height: 1.6;
}
.model-answer {
  font-size: 14px;
  line-height: 1.7;
  color: var(--color-text-secondary);
}
</style>
