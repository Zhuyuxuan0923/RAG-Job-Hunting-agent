<template>
  <div class="score-summary">
    <ScoreCircle :score="score" />
    <h2>{{ title }}</h2>
  </div>
</template>

<script setup lang="ts">
import ScoreCircle from './ScoreCircle.vue'
defineProps<{ score: number; title: string }>()
</script>

<style scoped>
.score-summary {
  text-align: center;
  padding: 32px 20px;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}
.score-summary h2 {
  margin-top: 18px;
  font-size: 20px;
  font-weight: 700;
}
</style>
