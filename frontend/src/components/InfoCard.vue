<template>
  <div class="info-card">
    <h3 class="card-title">{{ title }}</h3>
    <div class="card-body">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ title: string }>()
</script>

<style scoped>
.info-card {
  min-height: 100%;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 20px 22px;
  box-shadow: var(--shadow-xs);
  transition: border-color 0.18s, box-shadow 0.18s, transform 0.18s;
}

.info-card:hover {
  border-color: #cbd5e1;
  box-shadow: var(--shadow-sm);
  transform: translateY(-1px);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  padding-bottom: 10px;
  color: var(--color-text);
  border-bottom: 1px solid var(--color-border);
  font-size: 15px;
  font-weight: 750;
}

.card-title::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: var(--color-accent);
}

.card-body {
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.75;
}
</style>
