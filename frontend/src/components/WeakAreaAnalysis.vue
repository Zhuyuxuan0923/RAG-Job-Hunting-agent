<template>
  <div class="weak-areas">
    <h3>薄弱环节分析</h3>
    <div v-for="area in areas" :key="area.area" class="area-item">
      <div class="area-header">
        <span class="area-name">{{ area.area }}</span>
        <span class="area-score">{{ area.score }}/10</span>
      </div>
      <div class="area-bar">
        <div class="area-fill" :style="{ width: area.score * 10 + '%' }" :class="barClass(area.score)"></div>
      </div>
      <p class="area-desc">{{ area.description }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { WeakArea } from '../types'

defineProps<{ areas: WeakArea[] }>()

function barClass(score: number) {
  if (score >= 8) return 'high'
  if (score >= 6) return 'mid'
  return 'low'
}
</script>

<style scoped>
.weak-areas { margin: 24px 0; }
.weak-areas h3 { margin-bottom: 16px; }
.area-item { margin: 12px 0; }
.area-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}
.area-name { font-size: 14px; font-weight: 600; }
.area-score { font-size: 14px; }
.area-bar {
  height: 8px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}
.area-fill { height: 100%; border-radius: 4px; }
.area-fill.high { background: var(--color-success); }
.area-fill.mid { background: var(--color-warning); }
.area-fill.low { background: var(--color-error); }
.area-desc { font-size: 13px; color: var(--color-text-secondary); margin-top: 4px; }
</style>
