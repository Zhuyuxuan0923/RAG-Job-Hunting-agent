<template>
  <div class="answer-input">
    <textarea
      v-model="answer"
      placeholder="输入你的回答..."
      rows="4"
      :disabled="disabled"
      @keydown.ctrl.enter="$emit('submit', answer)"
    ></textarea>
    <div class="input-actions">
      <span class="hint">Ctrl + Enter 发送</span>
      <div>
        <button class="btn-skip" :disabled="disabled" @click="$emit('skip')">跳过</button>
        <button class="btn-submit" :disabled="disabled || !answer.trim()" @click="$emit('submit', answer)">提交回答</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{ disabled: boolean }>()
defineEmits<{ submit: [answer: string]; skip: [] }>()

const answer = ref('')
</script>

<style scoped>
.answer-input { margin: 16px 0; }
textarea {
  width: 100%;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 14px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  outline: none;
  line-height: 1.6;
}
textarea:focus { border-color: var(--color-primary); }
.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}
.hint { font-size: 12px; color: var(--color-text-secondary); }
.btn-skip {
  padding: 8px 20px;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  cursor: pointer;
  margin-right: 8px;
  font-size: 14px;
}
.btn-submit {
  padding: 8px 24px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
}
.btn-submit:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-submit:not(:disabled):hover { background: var(--color-primary-dark); }
</style>
