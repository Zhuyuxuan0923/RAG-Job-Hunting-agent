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
        <router-link to="/" class="btn-secondary">返回工作台</router-link>
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
.interview-report {
  max-width: 880px;
  margin: 0 auto;
}

.report-content {
  animation: fadeIn 0.35s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

section {
  margin: 30px 0;
}

section h2 {
  margin-bottom: 14px;
  padding-bottom: 10px;
  color: var(--color-text);
  border-bottom: 1px solid var(--color-border);
  font-size: 18px;
  font-weight: 800;
}

.actions {
  margin: 34px 0 10px;
  text-align: center;
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 11px 28px;
  color: var(--color-primary);
  background: #fff;
  border: 1px solid #bfdbfe;
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 15px;
  font-weight: 800;
  text-decoration: none;
  transition: background 0.15s, border-color 0.15s, transform 0.15s;
}

.btn-secondary:hover {
  background: var(--color-primary-light);
  border-color: #93c5fd;
  transform: translateY(-1px);
}

.loading-state {
  padding: 80px 20px;
  color: var(--color-text-secondary);
  text-align: center;
}

.loading-spinner {
  width: 38px;
  height: 38px;
  margin: 0 auto 14px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
