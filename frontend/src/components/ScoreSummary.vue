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
.score-summary { text-align: center; padding: 24px 0; }
.score-summary h2 { margin-top: 16px; }
</style>
