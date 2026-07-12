<template>
  <div class="paste-area">
    <textarea
      v-model="content"
      :placeholder="placeholder"
      class="paste-input"
      rows="8"
    ></textarea>
    <div class="paste-footer">
      <span class="char-count">{{ content.length }} 字</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{ placeholder: string; modelValue: string }>()
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

const content = ref(props.modelValue)
watch(content, (v) => emit('update:modelValue', v))
watch(() => props.modelValue, (v) => { content.value = v })
</script>

<style scoped>
.paste-area {
  overflow: hidden;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  transition: border-color 0.15s, box-shadow 0.15s;
}

.paste-area:focus-within {
  border-color: var(--color-primary);
  box-shadow: var(--focus-ring);
}

.paste-input {
  width: 100%;
  min-height: 168px;
  border: none;
  padding: 15px 16px;
  color: var(--color-text);
  background: transparent;
  font-size: 14px;
  line-height: 1.65;
  resize: vertical;
}

.paste-input::placeholder {
  color: #94a3b8;
}

.paste-footer {
  display: flex;
  justify-content: flex-end;
  padding: 8px 16px;
  color: var(--color-text-secondary);
  background: var(--color-surface-soft);
  border-top: 1px solid var(--color-border);
  font-size: 12px;
}
</style>
