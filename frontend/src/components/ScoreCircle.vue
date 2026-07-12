<template>
  <div class="score-circle">
    <svg viewBox="0 0 120 120" class="circle-svg">
      <circle cx="60" cy="60" r="52" fill="none" stroke="#e2e8f0" stroke-width="8" />
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
  width: 132px;
  height: 132px;
  margin: 0 auto;
}

.circle-svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 8px 18px rgba(15, 23, 42, 0.08));
}

.progress-ring {
  transition: stroke-dashoffset 1.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.score-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.score-value {
  display: block;
  font-size: 34px;
  font-weight: 850;
  letter-spacing: 0;
  line-height: 1;
}

.score-label {
  display: block;
  margin-top: 5px;
  color: var(--color-text-secondary);
  font-size: 12px;
  font-weight: 650;
}
</style>
