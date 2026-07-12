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
        <button class="btn-skip" type="button" :disabled="disabled" @click="$emit('skip')">跳过</button>
        <button class="btn-submit" type="button" :disabled="disabled || !answer.trim()" @click="$emit('submit', answer)">
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
  position: sticky;
  bottom: 18px;
  margin: 22px 0 0;
  padding: 15px;
  background: rgba(255, 255, 255, 0.94);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  backdrop-filter: blur(12px);
}

textarea {
  width: 100%;
  min-height: 112px;
  padding: 6px;
  color: var(--color-text);
  background: transparent;
  border: none;
  font-size: 15px;
  line-height: 1.65;
  resize: vertical;
}

textarea::placeholder {
  color: #94a3b8;
}

.input-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 10px;
  padding-top: 12px;
  border-top: 1px solid var(--color-border);
}

.hint {
  color: var(--color-text-secondary);
  font-size: 12px;
}

.actions-right {
  display: flex;
  gap: 8px;
}

.btn-skip,
.btn-submit {
  min-height: 36px;
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s, color 0.15s, transform 0.15s;
}

.btn-skip {
  color: var(--color-text-secondary);
  background: #fff;
  border: 1px solid var(--color-border);
}

.btn-skip:hover:not(:disabled) {
  color: var(--color-text);
  border-color: #cbd5e1;
}

.btn-submit {
  color: #fff;
  background: var(--color-primary);
  border: 1px solid var(--color-primary);
  box-shadow: 0 8px 18px rgba(37, 99, 235, 0.18);
}

.btn-submit:disabled,
.btn-skip:disabled {
  opacity: 0.48;
  box-shadow: none;
}

.btn-submit:hover:not(:disabled) {
  background: var(--color-primary-dark);
  border-color: var(--color-primary-dark);
  transform: translateY(-1px);
}

@media (max-width: 560px) {
  .input-actions {
    align-items: stretch;
    flex-direction: column;
  }

  .actions-right {
    width: 100%;
  }

  .btn-skip,
  .btn-submit {
    flex: 1;
  }
}
</style>
