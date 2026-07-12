<template>
  <div class="score-summary">
    <ScoreCircle :score="score" />
    <div class="summary-copy">
      <h2>{{ title }}</h2>
      <p>结合回答质量、表达结构与岗位匹配度生成综合评估。</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import ScoreCircle from './ScoreCircle.vue'
defineProps<{ score: number; title: string }>()
</script>

<style scoped>
.score-summary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 26px;
  padding: 30px 28px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.summary-copy {
  max-width: 380px;
}

.score-summary h2 {
  color: var(--color-text);
  font-size: 22px;
  font-weight: 800;
  line-height: 1.3;
}

.score-summary p {
  margin-top: 8px;
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.65;
}

@media (max-width: 640px) {
  .score-summary {
    flex-direction: column;
    text-align: center;
  }
}
</style>
