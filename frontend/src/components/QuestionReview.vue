<template>
  <div class="question-review">
    <div class="review-header">
      <span class="q-num">第 {{ review.question_number }} 题</span>
      <span class="q-score" :class="scoreClass">{{ review.score }}/10</span>
    </div>
    <p class="q-question">{{ review.question }}</p>
    <div class="q-answer">
      <h4>你的回答</h4>
      <p>{{ review.answer }}</p>
    </div>
    <div class="q-feedback">
      <h4>AI 点评</h4>
      <p>{{ review.feedback }}</p>
    </div>
    <div v-if="review.strengths.length" class="q-tags">
      <span v-for="s in review.strengths" :key="s" class="tag green">{{ s }}</span>
    </div>
    <div v-if="review.improvements.length" class="q-tags">
      <span v-for="s in review.improvements" :key="s" class="tag orange">{{ s }}</span>
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
  border-radius: var(--radius);
  padding: 20px;
  margin: 16px 0;
}
.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.q-num { font-weight: 600; }
.q-score { font-size: 18px; font-weight: 700; }
.q-score.high { color: var(--color-success); }
.q-score.mid { color: var(--color-warning); }
.q-score.low { color: var(--color-error); }
.q-question { font-size: 15px; line-height: 1.6; margin-bottom: 16px; }
.q-answer, .q-feedback { margin: 12px 0; }
.q-answer h4, .q-feedback h4 { font-size: 13px; font-weight: 600; margin-bottom: 4px; }
.q-answer p, .q-feedback p { font-size: 14px; color: var(--color-text-secondary); line-height: 1.6; }
.q-tags { margin-top: 8px; }
.tag {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 12px;
  margin: 4px 4px 4px 0;
}
.tag.green { background: #e6f4ea; color: var(--color-success); }
.tag.orange { background: #fef7e0; color: #e37400; }
</style>
