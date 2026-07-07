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
      <div class="actions-right">
        <button class="btn-skip" :disabled="disabled" @click="$emit('skip')">跳过</button>
        <button class="btn-submit" :disabled="disabled || !answer.trim()" @click="$emit('submit', answer)">
          提交回答
        </button>
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
.answer-input {
  margin: 20px 0;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 16px;
  box-shadow: var(--shadow-sm);
}
textarea {
  width: 100%;
  border: none;
  padding: 6px;
  font-size: 15px;
  font-family: inherit;
  resize: vertical;
  outline: none;
  line-height: 1.6;
  background: transparent;
}
.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  padding-top: 12px;
  border-top: 1px solid var(--color-border);
}
.hint { font-size: 12px; color: var(--color-text-secondary); }
.actions-right { display: flex; gap: 8px; }
.btn-skip {
  padding: 8px 18px;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 14px;
  color: var(--color-text-secondary);
  transition: all 0.15s;
}
.btn-skip:hover { border-color: var(--color-text-secondary); }
.btn-submit {
  padding: 8px 22px;
  background: linear-gradient(135deg, var(--color-primary) 0%, #7c3aed 100%);
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.25);
}
.btn-submit:disabled { opacity: 0.4; cursor: not-allowed; box-shadow: none; }
.btn-submit:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.35);
}
</style>
