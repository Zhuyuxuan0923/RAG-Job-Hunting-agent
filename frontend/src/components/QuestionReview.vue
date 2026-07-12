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
  margin: 14px 0;
  padding: 20px 22px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xs);
  transition: border-color 0.18s, box-shadow 0.18s;
}

.question-review:hover {
  border-color: #cbd5e1;
  box-shadow: var(--shadow-sm);
}

.review-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 15px;
}

.review-left {
  flex: 1;
}

.q-num {
  color: var(--color-primary);
  font-size: 12px;
  font-weight: 800;
}

.q-question {
  display: block;
  margin-top: 6px;
  color: var(--color-text);
  font-size: 15px;
  font-weight: 700;
  line-height: 1.65;
}

.q-score {
  flex-shrink: 0;
  font-size: 22px;
  font-weight: 850;
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

.q-answer,
.q-feedback {
  padding: 14px;
  border-radius: var(--radius);
  font-size: 13px;
  line-height: 1.7;
}

.q-answer {
  background: var(--color-surface-soft);
}

.q-feedback {
  background: var(--color-primary-light);
}

.q-answer h4,
.q-feedback h4 {
  margin-bottom: 7px;
  color: var(--color-text);
  font-size: 12px;
  font-weight: 800;
}

.q-answer p,
.q-feedback p {
  color: var(--color-text-secondary);
}

.review-tags {
  margin-top: 6px;
}

.tag {
  display: inline-block;
  margin: 4px 6px 4px 0;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
}

.tag-green {
  color: var(--color-success);
  background: var(--color-success-light);
}

.tag-orange {
  color: var(--color-warning);
  background: var(--color-warning-light);
}

@media (max-width: 700px) {
  .review-body {
    grid-template-columns: 1fr;
  }
}
</style>
