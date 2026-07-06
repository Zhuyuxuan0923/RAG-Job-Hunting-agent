<template>
  <div class="interview-report">
    <div v-if="data">
      <ScoreSummary :score="data.overall_score" title="面试综合评分" />

      <section>
        <h2>逐题回顾</h2>
        <QuestionReview v-for="q in data.questions" :key="q.question_number" :review="q" />
      </section>

      <section>
        <WeakAreaAnalysis :areas="data.weak_areas" />
      </section>

      <section>
        <StudyPlan :plan="data.study_plan" />
      </section>
    </div>

    <div v-else class="loading">加载中...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import ScoreSummary from '../components/ScoreSummary.vue'
import QuestionReview from '../components/QuestionReview.vue'
import WeakAreaAnalysis from '../components/WeakAreaAnalysis.vue'
import StudyPlan from '../components/StudyPlan.vue'
import { api } from '../api/client'
import type { InterviewReportData } from '../types'

const route = useRoute()
const data = ref<InterviewReportData | null>(null)

onMounted(async () => {
  try {
    data.value = await api.getInterviewReport(route.params.sessionId as string)
  } catch (e) {
    console.error(e)
  }
})
</script>

<style scoped>
.interview-report { max-width: 800px; margin: 0 auto; }
section { margin: 32px 0; }
section h2 { font-size: 20px; margin-bottom: 16px; }
.loading { text-align: center; padding: 60px; color: var(--color-text-secondary); }
</style>
