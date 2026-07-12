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
.weak-areas {
  margin: 28px 0;
}

.weak-areas h3 {
  margin-bottom: 16px;
  color: var(--color-text);
  font-size: 18px;
  font-weight: 800;
}

.areas-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.area-card {
  padding: 18px 20px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xs);
}

.area-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 9px;
}

.area-name {
  color: var(--color-text);
  font-size: 14px;
  font-weight: 800;
}

.area-score {
  font-size: 16px;
  font-weight: 850;
}

.area-score.high { color: var(--color-success); }
.area-score.mid { color: var(--color-warning); }
.area-score.low { color: var(--color-error); }

.area-bar {
  overflow: hidden;
  height: 8px;
  margin: 9px 0;
  background: #e2e8f0;
  border-radius: 999px;
}

.area-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 1s ease;
}

.area-fill.high { background: var(--color-success); }
.area-fill.mid { background: var(--color-warning); }
.area-fill.low { background: var(--color-error); }

.area-desc {
  margin-top: 8px;
  color: var(--color-text-secondary);
  font-size: 13px;
  line-height: 1.65;
}

@media (max-width: 720px) {
  .areas-grid {
    grid-template-columns: 1fr;
  }
}
</style>
