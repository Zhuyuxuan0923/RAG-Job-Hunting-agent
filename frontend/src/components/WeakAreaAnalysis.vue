<template>
  <div class="weak-areas">
    <h3>薄弱环节分析</h3>
    <div class="areas-grid">
      <div v-for="area in areas" :key="area.area" class="area-card">
        <div class="area-header">
          <span class="area-name">{{ area.area }}</span>
          <span class="area-score" :class="scoreClass(area.score)">{{ area.score }}/10</span>
        </div>
        <div class="area-bar">
          <div class="area-fill" :style="{ width: area.score * 10 + '%' }" :class="barClass(area.score)"></div>
        </div>
        <p class="area-desc">{{ area.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { WeakArea } from '../types'

defineProps<{ areas: WeakArea[] }>()

function scoreClass(score: number) {
  if (score >= 8) return 'high'
  if (score >= 6) return 'mid'
  return 'low'
}
function barClass(score: number) {
  if (score >= 8) return 'high'
  if (score >= 6) return 'mid'
  return 'low'
}
</script>

<style scoped>
.weak-areas { margin: 28px 0; }
.weak-areas h3 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 16px;
}
.areas-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}
.area-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 18px 20px;
  box-shadow: var(--shadow-xs);
}
.area-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.area-name { font-size: 14px; font-weight: 700; }
.area-score { font-size: 16px; font-weight: 700; }
.area-score.high { color: var(--color-success); }
.area-score.mid { color: var(--color-warning); }
.area-score.low { color: var(--color-error); }
.area-bar {
  height: 8px;
  background: #e8e8ee;
  border-radius: 4px;
  overflow: hidden;
  margin: 8px 0;
}
.area-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 1s ease;
}
.area-fill.high { background: linear-gradient(90deg, var(--color-success), #34d399); }
.area-fill.mid { background: linear-gradient(90deg, var(--color-warning), #fbbf24); }
.area-fill.low { background: linear-gradient(90deg, var(--color-error), #f87171); }
.area-desc { font-size: 13px; color: var(--color-text-secondary); line-height: 1.6; margin-top: 8px; }
</style>
