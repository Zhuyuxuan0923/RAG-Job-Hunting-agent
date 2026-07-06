<template>
  <div class="chat-bubble" :class="[role]">
    <div class="bubble-avatar">{{ role === 'interviewer' ? 'AI' : '你' }}</div>
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
}
.chat-bubble.candidate { flex-direction: row-reverse; }
.bubble-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
}
.interviewer .bubble-avatar { background: var(--color-primary); color: #fff; }
.candidate .bubble-avatar { background: #e0e0e0; color: var(--color-text); }
.bubble-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
}
.interviewer .bubble-content { background: var(--color-surface); border: 1px solid var(--color-border); }
.candidate .bubble-content { background: var(--color-primary); color: #fff; }
</style>
