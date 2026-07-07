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
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 22px 24px;
  box-shadow: var(--shadow-xs);
  transition: box-shadow 0.2s, transform 0.2s;
}
.info-card:hover {
  box-shadow: var(--shadow-sm);
}
.card-title {
  font-size: 15px;
  font-weight: 700;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
  display: flex;
  align-items: center;
  gap: 8px;
}
.card-body {
  font-size: 14px;
  line-height: 1.7;
  color: var(--color-text-secondary);
}
</style>
