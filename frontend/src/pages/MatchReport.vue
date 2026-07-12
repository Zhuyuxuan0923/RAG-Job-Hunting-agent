<template>
  <div class="match-report">
    <ThinkingStream :items="thinking" />

    <div v-if="data" class="report-content">
      <section class="hero-section">
        <ScoreCircle :score="data.overall_score" />
        <div class="hero-copy">
          <h2>岗位匹配度分析报告</h2>
          <p class="hero-sub">AI 综合评估候选人背景与岗位要求的匹配程度，并给出面试准备重点。</p>
        </div>
      </section>

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

      <section class="skill-match-section">
        <div class="section-header">
          <h3>技能匹配详情</h3>
          <span>{{ data.skill_match.length }} 项能力维度</span>
        </div>
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
      </section>

      <section class="suggestions">
        <h3>改进建议</h3>
        <ul>
          <li v-for="s in data.suggestions" :key="s">{{ s }}</li>
        </ul>
      </section>

      <div class="actions">
        <button class="btn-primary" type="button" @click="startInterview">
          <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
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
.match-report {
  max-width: 980px;
  margin: 0 auto;
}

.report-content {
  animation: fadeIn 0.35s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.hero-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 28px;
  margin: 0 0 24px;
  padding: 30px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.hero-copy {
  max-width: 520px;
}

.hero-section h2 {
  color: var(--color-text);
  font-size: 25px;
  font-weight: 850;
  line-height: 1.3;
}

.hero-sub {
  margin-top: 8px;
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.7;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
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

.skill-match-section,
.suggestions {
  margin: 28px 0;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 14px;
}

.section-header h3,
.suggestions h3 {
  color: var(--color-text);
  font-size: 18px;
  font-weight: 800;
}

.section-header span {
  color: var(--color-text-secondary);
  font-size: 13px;
  font-weight: 650;
}

.table-wrap {
  overflow: hidden;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xs);
}

.skill-table {
  width: 100%;
  border-collapse: collapse;
}

.skill-table th {
  padding: 13px 16px;
  color: var(--color-text-secondary);
  background: var(--color-surface-soft);
  border-bottom: 1px solid var(--color-border);
  font-size: 12px;
  font-weight: 800;
  text-align: left;
}

.skill-table td {
  padding: 13px 16px;
  border-bottom: 1px solid #eef2f7;
  font-size: 14px;
}

.skill-table tbody tr:last-child td {
  border-bottom: none;
}

.skill-table tbody tr:hover {
  background: #f8fbff;
}

.skill-name {
  color: var(--color-text);
  font-weight: 750;
}

.tag {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 800;
}

.tag-required {
  color: var(--color-error);
  background: var(--color-error-light);
}

.tag-optional {
  color: var(--color-primary);
  background: var(--color-primary-light);
}

.level-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.level-bar {
  width: 92px;
  height: 7px;
  overflow: hidden;
  flex-shrink: 0;
  background: #e2e8f0;
  border-radius: 999px;
}

.level-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.6s ease;
}

.level-fill.candidate {
  background: var(--color-primary);
}

.level-fill.jd {
  background: var(--color-accent);
}

.level-num {
  color: var(--color-text-secondary);
  font-size: 13px;
  font-weight: 700;
}

.suggestions ul {
  display: grid;
  gap: 10px;
  padding: 0;
  list-style: none;
}

.suggestions li {
  position: relative;
  padding: 13px 16px 13px 40px;
  color: var(--color-text);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-xs);
  font-size: 14px;
  line-height: 1.65;
}

.suggestions li::before {
  content: '';
  position: absolute;
  left: 16px;
  top: 20px;
  width: 8px;
  height: 8px;
  background: var(--color-accent);
  border-radius: 999px;
}

.actions {
  margin: 34px 0 10px;
  text-align: center;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 48px;
  padding: 13px 34px;
  color: #fff;
  background: var(--color-primary);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius);
  box-shadow: 0 12px 24px rgba(37, 99, 235, 0.2);
  cursor: pointer;
  font-size: 15px;
  font-weight: 800;
  transition: background 0.15s, border-color 0.15s, transform 0.15s, box-shadow 0.15s;
}

.btn-primary:hover {
  background: var(--color-primary-dark);
  border-color: var(--color-primary-dark);
  box-shadow: 0 16px 28px rgba(37, 99, 235, 0.24);
  transform: translateY(-1px);
}

.loading-state {
  padding: 80px 20px;
  color: var(--color-text-secondary);
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 16px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state {
  padding: 28px;
  color: var(--color-error);
  background: var(--color-error-light);
  border: 1px solid #fecaca;
  border-radius: var(--radius-lg);
  text-align: center;
}

@media (max-width: 760px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
  }

  .cards-grid {
    grid-template-columns: 1fr;
  }

  .table-wrap {
    overflow-x: auto;
  }

  .skill-table {
    min-width: 700px;
  }
}
</style>
