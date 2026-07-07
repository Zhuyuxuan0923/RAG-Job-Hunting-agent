<template>
  <div class="question-review">
    <div class="review-header">
      <div class="review-left">
        <span class="q-num">第 {{ review.question_number }} 题</span>
        <span class="q-question">{{ review.question }}</span>
      </div>
      <span class="q-score" :class="scoreClass">{{ review.score }}/10</span>
    </div>
    <div class="review-body">
      <div class="q-answer">
        <h4>你的回答</h4>
        <p>{{ review.answer }}</p>
      </div>
      <div class="q-feedback">
        <h4>AI 点评</h4>
        <p>{{ review.feedback }}</p>
      </div>
    </div>
    <div class="review-tags">
      <span v-for="s in review.strengths" :key="s" class="tag tag-green">{{ s }}</span>
      <span v-for="s in review.improvements" :key="s" class="tag tag-orange">{{ s }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { QuestionReviewData } from '../types'

const props = defineProps<{ review: QuestionReviewData }>()

const scoreClass = computed(() => {
  if (props.review.score >= 8) return 'high'
  if (props.review.score >= 6) return 'mid'
  return 'low'
})
</script>

<style scoped>
.question-review {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 22px 24px;
  margin: 14px 0;
  box-shadow: var(--shadow-xs);
  transition: box-shadow 0.2s;
}
.question-review:hover {
  box-shadow: var(--shadow-sm);
}
.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  gap: 16px;
}
.review-left {
  flex: 1;
}
.q-num {
  font-size: 12px;
  font-weight: 700;
  color: var(--color-primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.q-question {
  display: block;
  font-size: 15px;
  font-weight: 600;
  margin-top: 6px;
  line-height: 1.6;
}
.q-score {
  font-size: 22px;
  font-weight: 800;
  flex-shrink: 0;
}
.q-score.high { color: var(--color-success); }
.q-score.mid { color: var(--color-warning); }
.q-score.low { color: var(--color-error); }
.review-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin: 14px 0;
}
.q-answer, .q-feedback {
  padding: 14px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  line-height: 1.65;
}
.q-answer { background: #f8f8fb; }
.q-feedback { background: var(--color-primary-light); }
.q-answer h4, .q-feedback h4 {
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.q-answer p, .q-feedback p {
  color: var(--color-text-secondary);
}
.review-tags { margin-top: 6px; }
.tag {
  display: inline-block;
  padding: 3px 12px;
  border-radius: 14px;
  font-size: 12px;
  font-weight: 600;
  margin: 4px 6px 4px 0;
}
.tag-green { background: var(--color-success-light); color: var(--color-success); }
.tag-orange { background: var(--color-warning-light); color: #d97706; }
</style>
