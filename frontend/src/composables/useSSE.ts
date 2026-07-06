import { ref, onUnmounted } from 'vue'

export function useSSE(url: string) {
  const data = ref<any>(null)
  const thinking = ref<Array<{ action: string; detail: string; search_round: number }>>([])
  const stage = ref('')
  const done = ref(false)
  const error = ref<string | null>(null)
  let eventSource: EventSource | null = null

  function connect() {
    eventSource = new EventSource(url)
    eventSource.addEventListener('progress', (e) => {
      const d = JSON.parse(e.data)
      stage.value = d.stage
    })
    eventSource.addEventListener('thinking', (e) => {
      const d = JSON.parse(e.data)
      thinking.value.push(d)
    })
    eventSource.addEventListener('result', (e) => {
      data.value = JSON.parse(e.data)
    })
    eventSource.addEventListener('done', () => {
      done.value = true
      eventSource?.close()
    })
    eventSource.onerror = () => {
      error.value = 'SSE connection failed'
      eventSource?.close()
    }
  }

  function close() {
    eventSource?.close()
  }

  onUnmounted(close)

  return { data, thinking, stage, done, error, connect, close }
}
