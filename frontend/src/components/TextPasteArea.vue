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
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--color-surface);
}
.paste-input {
  width: 100%;
  border: none;
  padding: 16px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  outline: none;
  line-height: 1.6;
}
.paste-footer {
  padding: 8px 16px;
  border-top: 1px solid var(--color-border);
  font-size: 12px;
  color: var(--color-text-secondary);
}
</style>
