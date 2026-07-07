<template>
  <div class="match-report">
    <ThinkingStream :items="thinking" />

    <div v-if="data" class="report-content">
      <div class="hero-section">
        <ScoreCircle :score="data.overall_score" />
        <h2>岗位匹配度分析报告</h2>
        <p class="hero-sub">AI 综合评估候选人背景与岗位需求的匹配程度</p>
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
          <p v-if="!data.skill_gaps.length" class="empty-text">暂无显著技能缺口</p>
        </InfoCard>
        <InfoCard title="准备清单">
          <ul>
            <li v-for="item in data.preparation_checklist" :key="item">{{ item }}</li>
          </ul>
          <p v-if="!data.preparation_checklist.length" class="empty-text">暂无准备项</p>
        </InfoCard>
      </div>

      <div class="skill-match-section">
        <h3>技能匹配详情</h3>
        <div class="table-wrap">
          <table class="skill-table">
            <thead>
              <tr><th>技能</th><th>是否必需</th><th>候选人水平</th><th>JD 要求</th></tr>
            </thead>
            <tbody>
              <tr v-for="s in data.skill_match" :key="s.skill">
                <td class="skill-name">{{ s.skill }}</td>
                <td>
                  <span class="tag" :class="s.required ? 'tag-required' : 'tag-optional'">
                    {{ s.required ? '必需' : '加分' }}
                  </span>
                </td>
                <td>
                  <div class="level-cell">
                    <div class="level-bar">
                      <div class="level-fill candidate" :style="{ width: (s.candidate_level / 10 * 100) + '%' }"></div>
                    </div>
                    <span class="level-num">{{ s.candidate_level }}/10</span>
                  </div>
                </td>
                <td>
                  <div class="level-cell">
                    <div class="level-bar">
                      <div class="level-fill jd" :style="{ width: (s.jd_level / 10 * 100) + '%' }"></div>
                    </div>
                    <span class="level-num">{{ s.jd_level }}/10</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="suggestions">
        <h3>改进建议</h3>
        <ul>
          <li v-for="s in data.suggestions" :key="s">{{ s }}</li>
        </ul>
      </div>

      <div class="actions">
        <button class="btn-primary" @click="startInterview">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polygon points="5 3 19 12 5 21 5 3"/>
          </svg>
          开始模拟面试
        </button>
      </div>
    </div>

    <div v-else-if="!done && stage" class="loading-state">
      <div class="loading-spinner"></div>
      <p>{{ statusText }}</p>
    </div>
    <div v-if="error" class="error-state">{{ error }}</div>
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
.report-content {
  animation: fadeIn 0.4s ease;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Hero */
.hero-section {
  text-align: center;
  margin: 16px 0 32px;
  padding: 32px 20px;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}
.hero-section h2 {
  margin-top: 18px;
  font-size: 22px;
  font-weight: 700;
}
.hero-sub {
  margin-top: 6px;
  font-size: 14px;
  color: var(--color-text-secondary);
}

/* Cards grid */
.cards-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin: 24px 0;
}
.cards-grid ul {
  padding-left: 20px;
}
.cards-grid li {
  margin: 5px 0;
  font-size: 14px;
}
.empty-text {
  color: var(--color-text-secondary);
  font-size: 13px;
}

/* Skill table */
.skill-match-section {
  margin: 28px 0;
}
.skill-match-section h3 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 14px;
}
.table-wrap {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-xs);
}
.skill-table {
  width: 100%;
  border-collapse: collapse;
}
.skill-table th {
  padding: 12px 16px;
  text-align: left;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--color-text-secondary);
  background: #fafafc;
  border-bottom: 1px solid var(--color-border);
}
.skill-table td {
  padding: 12px 16px;
  font-size: 14px;
  border-bottom: 1px solid #f5f5f7;
}
.skill-table tbody tr:last-child td {
  border-bottom: none;
}
.skill-table tbody tr:hover {
  background: #fafafc;
}
.skill-name {
  font-weight: 600;
}
.tag {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}
.tag-required {
  background: var(--color-error-light);
  color: var(--color-error);
}
.tag-optional {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

/* Level bars */
.level-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}
.level-bar {
  width: 80px;
  height: 6px;
  background: #e8e8ee;
  border-radius: 3px;
  overflow: hidden;
  flex-shrink: 0;
}
.level-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.6s ease;
}
.level-fill.candidate {
  background: linear-gradient(90deg, var(--color-primary), #7c3aed);
}
.level-fill.jd {
  background: linear-gradient(90deg, var(--color-warning), #f97316);
}
.level-num {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-secondary);
}

/* Suggestions */
.suggestions {
  margin: 28px 0;
}
.suggestions h3 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 14px;
}
.suggestions ul {
  list-style: none;
  padding: 0;
}
.suggestions li {
  padding: 12px 16px;
  margin: 8px 0;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  font-size: 14px;
  box-shadow: var(--shadow-xs);
  position: relative;
  padding-left: 36px;
}
.suggestions li::before {
  content: '';
  position: absolute;
  left: 14px;
  top: 17px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-primary);
}

/* Actions */
.actions {
  text-align: center;
  margin: 36px 0;
}
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 40px;
  background: linear-gradient(135deg, var(--color-primary) 0%, #7c3aed 100%);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3);
}
.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
}

/* Loading */
.loading-state {
  text-align: center;
  padding: 80px 20px;
  color: var(--color-text-secondary);
}
.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  margin: 0 auto 16px;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state {
  text-align: center;
  padding: 40px;
  color: var(--color-error);
  background: var(--color-error-light);
  border-radius: var(--radius);
}
</style>
