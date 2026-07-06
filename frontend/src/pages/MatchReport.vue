<template>
  <div class="match-report">
    <ThinkingStream :items="thinking" />

    <div v-if="data" class="report-content">
      <div class="score-section">
        <ScoreCircle :score="data.overall_score" />
        <h2>岗位匹配度分析报告</h2>
      </div>

      <div class="cards-grid">
        <InfoCard title="公司背景">
          <p>{{ data.company_background || '暂无数据' }}</p>
        </InfoCard>
        <InfoCard title="面经参考">
          <p>{{ data.interview_experience || '暂无数据' }}</p>
        </InfoCard>
        <InfoCard title="技能缺口">
          <ul>
            <li v-for="gap in data.skill_gaps" :key="gap">{{ gap }}</li>
          </ul>
        </InfoCard>
        <InfoCard title="准备清单">
          <ul>
            <li v-for="item in data.preparation_checklist" :key="item">{{ item }}</li>
          </ul>
        </InfoCard>
      </div>

      <div class="skill-match-section">
        <h3>技能匹配详情</h3>
        <table class="skill-table">
          <thead>
            <tr><th>技能</th><th>是否必需</th><th>候选人水平</th><th>JD 要求</th></tr>
          </thead>
          <tbody>
            <tr v-for="s in data.skill_match" :key="s.skill">
              <td>{{ s.skill }}</td>
              <td>{{ s.required ? '是' : '否' }}</td>
              <td>{{ s.candidate_level }}/5</td>
              <td>{{ s.jd_level }}/5</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="suggestions">
        <h3>改进建议</h3>
        <ul>
          <li v-for="s in data.suggestions" :key="s">{{ s }}</li>
        </ul>
      </div>

      <div class="actions">
        <button class="btn-primary" @click="startInterview">开始模拟面试</button>
      </div>
    </div>

    <div v-else-if="!done && stage" class="loading">
      <p>{{ statusText }}</p>
    </div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ThinkingStream from '../components/ThinkingStream.vue'
import ScoreCircle from '../components/ScoreCircle.vue'
import InfoCard from '../components/InfoCard.vue'
import { useSSE } from '../composables/useSSE'

const route = useRoute()
const router = useRouter()
const taskId = route.params.taskId as string

const { data, thinking, stage, done, error, connect } = useSSE(`/api/match/${taskId}/stream`)

onMounted(() => connect())

const statusText = computed(() => {
  if (stage.value === 'parsing') return '正在解析文档...'
  if (stage.value === 'indexing') return '正在构建知识库...'
  return 'Agent 正在分析...'
})

function startInterview() {
  router.push(`/interview/${taskId}`)
}
</script>

<style scoped>
.match-report { max-width: 900px; margin: 0 auto; }
.score-section { text-align: center; margin: 24px 0; }
.score-section h2 { margin-top: 16px; font-size: 22px; }
.cards-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin: 24px 0;
}
.skill-match-section { margin: 24px 0; }
.skill-table { width: 100%; border-collapse: collapse; }
.skill-table th, .skill-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}
.skill-table th { font-weight: 600; background: #fafafa; }
.suggestions { margin: 24px 0; }
.suggestions ul, .cards-grid ul { padding-left: 20px; }
.suggestions li, .cards-grid li { margin: 6px 0; }
.actions { text-align: center; margin: 32px 0; }
.btn-primary {
  padding: 14px 40px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}
.btn-primary:hover { background: var(--color-primary-dark); }
.loading { text-align: center; padding: 60px; color: var(--color-text-secondary); }
.error { color: var(--color-error); text-align: center; padding: 20px; }
</style>
