<template>
  <div class="chat-bubble" :class="[role]">
    <div class="bubble-avatar">
      {{ role === 'interviewer' ? 'AI' : '你' }}
    </div>
    <div class="bubble-content">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ role: 'interviewer' | 'candidate' }>()
</script>

<style scoped>
.chat-bubble {
  display: flex;
  gap: 12px;
  margin: 16px 0;
  animation: slideIn 0.22s ease;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.chat-bubble.candidate {
  flex-direction: row-reverse;
}

.bubble-avatar {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border-radius: 12px;
  box-shadow: var(--shadow-xs);
  font-size: 13px;
  font-weight: 800;
}

.interviewer .bubble-avatar {
  color: #fff;
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
}

.candidate .bubble-avatar {
  color: var(--color-text);
  background: #e2e8f0;
}

.bubble-content {
  max-width: min(74%, 680px);
  padding: 14px 17px;
  border-radius: var(--radius-lg);
  font-size: 14px;
  line-height: 1.7;
}

.interviewer .bubble-content {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-top-left-radius: var(--radius-sm);
  box-shadow: var(--shadow-xs);
}

.candidate .bubble-content {
  color: #fff;
  background: var(--color-primary);
  border-top-right-radius: var(--radius-sm);
  box-shadow: 0 10px 20px rgba(37, 99, 235, 0.16);
}

@media (max-width: 640px) {
  .bubble-content {
    max-width: calc(100% - 50px);
  }
}
</style>
