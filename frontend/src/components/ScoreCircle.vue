<template>
  <div class="score-circle">
    <svg viewBox="0 0 120 120" class="circle-svg">
      <defs>
        <filter id="score-glow">
          <feGaussianBlur stdDeviation="2" result="blur" />
          <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
        </filter>
      </defs>
      <circle cx="60" cy="60" r="52" fill="none" stroke="#e8e8ee" stroke-width="8" />
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
        filter="url(#score-glow)"
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
  width: 130px;
  height: 130px;
  margin: 0 auto;
}
.circle-svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 2px 6px rgba(0,0,0,0.08));
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
  font-size: 34px;
  font-weight: 800;
  display: block;
  letter-spacing: -0.5px;
}
.score-label {
  font-size: 12px;
  color: var(--color-text-secondary);
  font-weight: 500;
}
</style>
