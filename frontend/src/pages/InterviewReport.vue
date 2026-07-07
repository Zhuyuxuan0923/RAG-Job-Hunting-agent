<template>
  <div class="interview-report">
    <div v-if="data" class="report-content">
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

      <div class="actions">
        <router-link to="/" class="btn-secondary">返回首页</router-link>
      </div>
    </div>

    <div v-else class="loading-state">
      <div class="loading-spinner"></div>
      <p>加载面试报告中...</p>
    </div>
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
.report-content {
  animation: fadeIn 0.4s ease;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
section { margin: 36px 0; }
section h2 {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 18px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--color-primary-light);
}
.actions { text-align: center; margin: 36px 0; }
.btn-secondary {
  display: inline-block;
  padding: 12px 32px;
  background: var(--color-surface);
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
  border-radius: var(--radius);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.15s;
}
.btn-secondary:hover {
  background: var(--color-primary-light);
}

/* Loading */
.loading-state { text-align: center; padding: 80px 20px; color: var(--color-text-secondary); }
.loading-spinner {
  width: 36px; height: 36px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  margin: 0 auto 14px;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
