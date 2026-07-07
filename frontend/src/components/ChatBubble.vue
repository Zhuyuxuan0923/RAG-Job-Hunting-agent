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
  animation: slideIn 0.25s ease;
}
@keyframes slideIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
.chat-bubble.candidate {
  flex-direction: row-reverse;
}
.bubble-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
  box-shadow: var(--shadow-xs);
}
.interviewer .bubble-avatar {
  background: linear-gradient(135deg, var(--color-primary), #7c3aed);
  color: #fff;
}
.candidate .bubble-avatar {
  background: linear-gradient(135deg, #e8e8ee, #d8d8e2);
  color: var(--color-text);
}
.bubble-content {
  max-width: 72%;
  padding: 14px 18px;
  border-radius: 14px;
  font-size: 14px;
  line-height: 1.65;
}
.interviewer .bubble-content {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-top-left-radius: 4px;
  box-shadow: var(--shadow-xs);
}
.candidate .bubble-content {
  background: linear-gradient(135deg, var(--color-primary), #7c3aed);
  color: #fff;
  border-top-right-radius: 4px;
}
</style>
