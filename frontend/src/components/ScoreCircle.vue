<template>
  <div class="score-circle">
    <svg viewBox="0 0 120 120" class="circle-svg">
      <circle cx="60" cy="60" r="52" fill="none" stroke="#e0e0e0" stroke-width="8" />
      <circle
        cx="60" cy="60" r="52"
        fill="none"
        :stroke="color"
        stroke-width="8"
        stroke-linecap="round"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="offset"
        transform="rotate(-90 60 60)"
        class="progress-ring"
      />
    </svg>
    <div class="score-text">
      <span class="score-value" :style="{ color }">{{ score }}</span>
      <span class="score-label">匹配度</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ score: number }>()
const circumference = 2 * Math.PI * 52

const offset = computed(() => circumference - (props.score / 100) * circumference)

const color = computed(() => {
  if (props.score >= 80) return 'var(--color-success)'
  if (props.score >= 60) return 'var(--color-warning)'
  return 'var(--color-error)'
})
</script>

<style scoped>
.score-circle {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto;
}
.circle-svg {
  width: 100%;
  height: 100%;
}
.progress-ring {
  transition: stroke-dashoffset 1s ease;
}
.score-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}
.score-value {
  font-size: 32px;
  font-weight: 700;
  display: block;
}
.score-label {
  font-size: 12px;
  color: var(--color-text-secondary);
}
</style>
