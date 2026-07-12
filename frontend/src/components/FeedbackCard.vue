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
  margin: 14px 0 18px 50px;
  padding: 20px 22px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.fb-header {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 12px;
}

.fb-score {
  font-size: 28px;
  font-weight: 850;
  letter-spacing: 0;
}

.fb-score small {
  color: var(--color-text-secondary);
  font-size: 14px;
  font-weight: 600;
}

.fb-score.high { color: var(--color-success); }
.fb-score.mid { color: var(--color-warning); }
.fb-score.low { color: var(--color-error); }

.fb-label {
  color: var(--color-text-secondary);
  font-size: 13px;
  font-weight: 650;
}

.fb-text {
  margin-bottom: 6px;
  color: var(--color-text);
  font-size: 14px;
  line-height: 1.75;
}

.fb-section {
  margin-top: 14px;
  padding: 13px 15px;
  border-radius: var(--radius);
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
  margin-bottom: 8px;
  color: var(--color-text);
  font-size: 13px;
  font-weight: 800;
}

.fb-section ul {
  padding-left: 20px;
}

.fb-section li,
.model-answer {
  color: var(--color-text-secondary);
  font-size: 13px;
  line-height: 1.65;
}

.fb-section li {
  margin: 4px 0;
}

@media (max-width: 640px) {
  .feedback-card {
    margin-left: 0;
  }
}
</style>
