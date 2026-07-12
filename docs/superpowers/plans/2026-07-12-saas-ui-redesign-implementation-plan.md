# SaaS UI Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the Vue frontend into a polished professional SaaS workbench and fix visible Chinese mojibake.

**Architecture:** Keep the current Vue 3 + Vite structure, API client, router, and component boundaries. Implement the redesign by refreshing global tokens, correcting page/component copy, and improving existing page/component CSS rather than introducing a UI framework or changing backend contracts.

**Tech Stack:** Vue 3, Vue Router, TypeScript, Vite, scoped Vue CSS, existing inline SVG icons.

## Global Constraints

- Preserve the existing workflow: upload materials, match analysis, simulated interview, interview report.
- Preserve existing backend API contracts and data fields.
- The first screen remains the actual upload workflow, not a marketing landing page.
- Use a professional SaaS tool style with a clean light interface, subtle cool background, white surfaces, and restrained blue/teal accents.
- Fix all visible Chinese mojibake in edited frontend files.
- Do not add new authentication, persistence, user accounts, backend API changes, or algorithm changes.
- Prefer updating existing Vue components and shared CSS over introducing a new UI framework.
- Maintain keyboard focus visibility and predictable responsive layouts.

---

## File Structure

- Modify `frontend/src/style.css`: global design tokens, body background, focus states, shared utility styling, responsive app layout.
- Modify `frontend/src/components/AppHeader.vue`: readable Chinese brand/navigation and upgraded header treatment.
- Modify `frontend/src/pages/UploadPage.vue`: upload workbench copy, layout, steps, upload panels, uploaded states, CTA.
- Modify `frontend/src/pages/MatchReport.vue`: dashboard-like match report copy, hero, cards, table, suggestions, loading/error states.
- Modify `frontend/src/pages/InterviewPage.vue`: guided start panel, active interview workspace copy/styling, completion state.
- Modify `frontend/src/pages/InterviewReport.vue`: readable section headings, loading copy, refined spacing and return action.
- Inspect and modify supporting components only as needed for visual consistency:
  - `frontend/src/components/FileDropZone.vue`
  - `frontend/src/components/TextPasteArea.vue`
  - `frontend/src/components/InfoCard.vue`
  - `frontend/src/components/ThinkingStream.vue`
  - `frontend/src/components/ScoreCircle.vue`
  - `frontend/src/components/ChatBubble.vue`
  - `frontend/src/components/QuestionCard.vue`
  - `frontend/src/components/FeedbackCard.vue`
  - `frontend/src/components/AnswerInput.vue`
  - `frontend/src/components/ScoreSummary.vue`
  - `frontend/src/components/QuestionReview.vue`
  - `frontend/src/components/WeakAreaAnalysis.vue`
  - `frontend/src/components/StudyPlan.vue`

---

### Task 1: Global SaaS Visual Foundation

**Files:**
- Modify: `frontend/src/style.css`
- Modify: `frontend/src/components/AppHeader.vue`

**Interfaces:**
- Consumes: Existing CSS variables referenced by current pages and components.
- Produces: Updated CSS variables with the same names plus optional new variables for consistent shadows, rings, and layout.

- [ ] **Step 1: Inspect current global and header CSS**

Run: `Get-Content -LiteralPath 'frontend\src\style.css'`
Expected: current `:root`, `body`, `.main-content`, and scrollbar styles are visible.

Run: `Get-Content -LiteralPath 'frontend\src\components\AppHeader.vue'`
Expected: current header template and scoped CSS are visible.

- [ ] **Step 2: Replace global tokens and base layout**

In `frontend/src/style.css`, keep the existing variable names but tune them to a professional SaaS palette:

```css
:root {
  --color-primary: #2563eb;
  --color-primary-dark: #1d4ed8;
  --color-primary-light: #dbeafe;
  --color-accent: #0f766e;
  --color-accent-light: #ccfbf1;
  --color-bg: #f6f8fb;
  --color-surface: #ffffff;
  --color-surface-soft: #f8fafc;
  --color-text: #111827;
  --color-text-secondary: #64748b;
  --color-border: #e2e8f0;
  --color-success: #059669;
  --color-success-light: #ecfdf5;
  --color-warning: #d97706;
  --color-warning-light: #fffbeb;
  --color-error: #dc2626;
  --color-error-light: #fef2f2;
  --radius: 8px;
  --radius-sm: 6px;
  --radius-lg: 12px;
  --shadow-xs: 0 1px 2px rgba(15, 23, 42, 0.04);
  --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.08), 0 1px 2px rgba(15, 23, 42, 0.04);
  --shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  --shadow-lg: 0 18px 45px rgba(15, 23, 42, 0.12);
  --focus-ring: 0 0 0 3px rgba(37, 99, 235, 0.16);
  --font-mono: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
}
```

Keep body typography on system fonts and set a subtle layered background:

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', Roboto, sans-serif;
  background:
    radial-gradient(circle at top left, rgba(37, 99, 235, 0.08), transparent 34rem),
    linear-gradient(180deg, #f8fafc 0%, var(--color-bg) 42%, #eef3f8 100%);
  color: var(--color-text);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

- [ ] **Step 3: Update header copy and shell styling**

In `frontend/src/components/AppHeader.vue`, replace mojibake with:

```vue
<span class="logo-text">Agentic RAG 求职助手</span>
<router-link to="/" class="nav-link">工作台</router-link>
```

Add a compact right-side status label if it fits the header without adding a new route:

```vue
<span class="header-status">AI 面试准备工作流</span>
```

Update header CSS to use a white translucent surface, restrained border, clear logo mark, and mobile-safe wrapping.

- [ ] **Step 4: Verify global foundation**

Run: `npm run build`
Working directory: `frontend`
Expected: `vue-tsc && vite build` completes successfully.

- [ ] **Step 5: Commit global foundation**

Run:

```bash
git add frontend/src/style.css frontend/src/components/AppHeader.vue
git commit -m "style: refresh SaaS app shell"
```

Expected: commit succeeds.

---

### Task 2: Upload Workbench Redesign

**Files:**
- Modify: `frontend/src/pages/UploadPage.vue`
- Modify if needed: `frontend/src/components/FileDropZone.vue`
- Modify if needed: `frontend/src/components/TextPasteArea.vue`

**Interfaces:**
- Consumes: Existing `api.uploadResume`, `api.uploadJD`, `api.startMatch`, `FileDropZone @file`, and `TextPasteArea v-model`.
- Produces: Same route behavior and same `startAnalysis()` behavior.

- [ ] **Step 1: Inspect upload components**

Run: `Get-Content -LiteralPath 'frontend\src\components\FileDropZone.vue'`
Expected: file input/drop component implementation is visible.

Run: `Get-Content -LiteralPath 'frontend\src\components\TextPasteArea.vue'`
Expected: text area component implementation is visible.

- [ ] **Step 2: Fix upload page Chinese copy**

Replace page visible copy in `frontend/src/pages/UploadPage.vue` with these strings:

```text
智能求职准备工作台
上传简历和职位描述，AI 将生成岗位匹配分析，并继续引导模拟面试。
上传资料
匹配分析
模拟面试
个人简历
职位描述
已完成
点击或拖拽上传简历文件
点击或拖拽上传 JD 文件
或直接粘贴
在此粘贴简历文本内容...
在此粘贴 JD 文本内容...
简历解析完成
JD 解析完成
重新上传
开始匹配度分析
请先上传简历和 JD 后再开始分析
```

Keep the existing script API behavior.

- [ ] **Step 3: Upgrade upload layout CSS**

Keep `.upload-grid` desktop two-column behavior and add mobile collapse:

```css
@media (max-width: 820px) {
  .upload-grid {
    grid-template-columns: 1fr;
  }
  .steps-indicator {
    justify-content: flex-start;
    overflow-x: auto;
    padding-bottom: 4px;
  }
}
```

Restyle `.page-hero`, `.steps-indicator`, `.upload-column`, `.upload-card`, and `.btn-primary` to match the global SaaS tokens: white panels, crisp borders, light shadows, blue primary action, green success state, and no purple-dominant gradient.

- [ ] **Step 4: Polish upload child components if needed**

If `FileDropZone.vue` or `TextPasteArea.vue` still uses generic or mojibake copy, update only visible copy and styles. Keep props and emitted events unchanged:

```ts
defineProps<{ label: string }>()
defineEmits<{ file: [file: File] }>()
```

- [ ] **Step 5: Verify upload build**

Run: `npm run build`
Working directory: `frontend`
Expected: build completes successfully.

- [ ] **Step 6: Commit upload workbench**

Run:

```bash
git add frontend/src/pages/UploadPage.vue frontend/src/components/FileDropZone.vue frontend/src/components/TextPasteArea.vue
git commit -m "style: redesign upload workbench"
```

Expected: commit succeeds. If either component was not modified, omit it from `git add`.

---

### Task 3: Match Report Dashboard Redesign

**Files:**
- Modify: `frontend/src/pages/MatchReport.vue`
- Modify if needed: `frontend/src/components/InfoCard.vue`
- Modify if needed: `frontend/src/components/ScoreCircle.vue`
- Modify if needed: `frontend/src/components/ThinkingStream.vue`

**Interfaces:**
- Consumes: `useSSE('/api/match/${taskId}/stream')`, `data.overall_score`, `data.company_background`, `data.interview_experience`, `data.skill_gaps`, `data.preparation_checklist`, `data.skill_match`, `data.suggestions`.
- Produces: Same start interview route: `router.push(`/interview/${taskId}`)`.

- [ ] **Step 1: Inspect report support components**

Run: `Get-Content -LiteralPath 'frontend\src\components\InfoCard.vue'`
Expected: card component is visible.

Run: `Get-Content -LiteralPath 'frontend\src\components\ScoreCircle.vue'`
Expected: score display component is visible.

Run: `Get-Content -LiteralPath 'frontend\src\components\ThinkingStream.vue'`
Expected: streaming thought component is visible.

- [ ] **Step 2: Fix match report Chinese copy**

Replace visible mojibake in `frontend/src/pages/MatchReport.vue` with:

```text
岗位匹配度分析报告
AI 综合评估候选人背景与岗位要求的匹配程度
公司背景
面经参考
技能缺口
准备清单
暂无数据
暂无显著技能缺口
暂无准备项
技能匹配详情
技能
是否必需
候选人水平
JD 要求
必需
加分
改进建议
开始模拟面试
正在解析文档...
正在构建知识库...
Agent 正在分析...
```

- [ ] **Step 3: Upgrade dashboard styling**

Update `.hero-section` to a horizontal dashboard summary on desktop when space allows: score on one side, title/subtitle on the other, with white surface and border.

Update cards and table:

```css
.cards-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

@media (max-width: 760px) {
  .cards-grid {
    grid-template-columns: 1fr;
  }
  .table-wrap {
    overflow-x: auto;
  }
}
```

Use blue for candidate level, teal/amber for JD level, and keep tags compact.

- [ ] **Step 4: Polish support components if needed**

If support components visually clash after page changes, adjust their CSS only. Preserve props and slots:

```vue
<InfoCard title="..."><p>...</p></InfoCard>
<ScoreCircle :score="data.overall_score" />
<ThinkingStream :items="thinking" />
```

- [ ] **Step 5: Verify match report build**

Run: `npm run build`
Working directory: `frontend`
Expected: build completes successfully.

- [ ] **Step 6: Commit match report dashboard**

Run:

```bash
git add frontend/src/pages/MatchReport.vue frontend/src/components/InfoCard.vue frontend/src/components/ScoreCircle.vue frontend/src/components/ThinkingStream.vue
git commit -m "style: polish match report dashboard"
```

Expected: commit succeeds. If a support component was not modified, omit it from `git add`.

---

### Task 4: Interview Workspace Redesign

**Files:**
- Modify: `frontend/src/pages/InterviewPage.vue`
- Modify if needed: `frontend/src/components/ChatBubble.vue`
- Modify if needed: `frontend/src/components/QuestionCard.vue`
- Modify if needed: `frontend/src/components/FeedbackCard.vue`
- Modify if needed: `frontend/src/components/AnswerInput.vue`

**Interfaces:**
- Consumes: `api.getMatchReport`, `api.startInterview`, `api.submitAnswer`, and `route.params.sessionId`.
- Produces: Same chat flow, same skip behavior, same final report route: `router.push(`/report/${sessionId.value}`)`.

- [ ] **Step 1: Inspect interview support components**

Run: `Get-Content -LiteralPath 'frontend\src\components\ChatBubble.vue'`
Expected: chat bubble component is visible.

Run: `Get-Content -LiteralPath 'frontend\src\components\QuestionCard.vue'`
Expected: question card component is visible.

Run: `Get-Content -LiteralPath 'frontend\src\components\FeedbackCard.vue'`
Expected: feedback component is visible.

Run: `Get-Content -LiteralPath 'frontend\src\components\AnswerInput.vue'`
Expected: answer input component is visible.

- [ ] **Step 2: Fix interview page Chinese copy**

Replace visible mojibake in `frontend/src/pages/InterviewPage.vue` with:

```text
模拟面试
AI 面试官将基于 JD 要求和你的简历缺口出题，模拟真实面试场景。
输入 Match Task ID 开始面试
例如：a1b2c3d4
正在准备面试题...
开始面试
AI 面试进行中
(跳过)
面试完成
所有问题已回答完毕，可以查看详细面试报告。
查看面试报告
```

- [ ] **Step 3: Upgrade interview workspace styling**

Make `.start-card` a polished setup panel with a compact icon, readable title, helper text, input, and CTA.

Make `.interview-active` feel like a workbench:

```css
.interview-header {
  position: sticky;
  top: 72px;
  z-index: 10;
  background: rgba(246, 248, 251, 0.86);
  backdrop-filter: blur(10px);
}
```

Keep chat messages readable with stable widths on desktop and full width on mobile.

- [ ] **Step 4: Polish support components if needed**

If support components contain mojibake or clash visually, update visible copy and CSS only. Keep event and prop interfaces unchanged:

```vue
<AnswerInput :disabled="waiting" @submit="submitAnswer" @skip="submitAnswer('')" />
<ChatBubble :role="msg.role">...</ChatBubble>
<QuestionCard :question="msg.question" />
<FeedbackCard :feedback="msg.feedback" />
```

- [ ] **Step 5: Verify interview build**

Run: `npm run build`
Working directory: `frontend`
Expected: build completes successfully.

- [ ] **Step 6: Commit interview workspace**

Run:

```bash
git add frontend/src/pages/InterviewPage.vue frontend/src/components/ChatBubble.vue frontend/src/components/QuestionCard.vue frontend/src/components/FeedbackCard.vue frontend/src/components/AnswerInput.vue
git commit -m "style: redesign interview workspace"
```

Expected: commit succeeds. If a support component was not modified, omit it from `git add`.

---

### Task 5: Interview Report Polish

**Files:**
- Modify: `frontend/src/pages/InterviewReport.vue`
- Modify if needed: `frontend/src/components/ScoreSummary.vue`
- Modify if needed: `frontend/src/components/QuestionReview.vue`
- Modify if needed: `frontend/src/components/WeakAreaAnalysis.vue`
- Modify if needed: `frontend/src/components/StudyPlan.vue`

**Interfaces:**
- Consumes: `api.getInterviewReport(route.params.sessionId as string)` and existing report data shapes.
- Produces: Same report rendering and same return route.

- [ ] **Step 1: Inspect interview report components**

Run: `Get-Content -LiteralPath 'frontend\src\components\ScoreSummary.vue'`
Expected: score summary component is visible.

Run: `Get-Content -LiteralPath 'frontend\src\components\QuestionReview.vue'`
Expected: question review component is visible.

Run: `Get-Content -LiteralPath 'frontend\src\components\WeakAreaAnalysis.vue'`
Expected: weak area component is visible.

Run: `Get-Content -LiteralPath 'frontend\src\components\StudyPlan.vue'`
Expected: study plan component is visible.

- [ ] **Step 2: Fix interview report Chinese copy**

Replace visible mojibake in `frontend/src/pages/InterviewReport.vue` with:

```text
面试综合评分
逐题回顾
返回工作台
加载面试报告中...
```

- [ ] **Step 3: Upgrade report styling**

Use consistent report sections:

```css
section {
  margin: 28px 0;
}

section h2 {
  font-size: 18px;
  font-weight: 750;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--color-border);
}
```

Update `.btn-secondary` to a restrained outline button that matches global tokens.

- [ ] **Step 4: Polish support components if needed**

If support components include mojibake or inconsistent styling, update visible copy and CSS only. Preserve props:

```vue
<ScoreSummary :score="data.overall_score" title="面试综合评分" />
<QuestionReview v-for="q in data.questions" :key="q.question_number" :review="q" />
<WeakAreaAnalysis :areas="data.weak_areas" />
<StudyPlan :plan="data.study_plan" />
```

- [ ] **Step 5: Verify interview report build**

Run: `npm run build`
Working directory: `frontend`
Expected: build completes successfully.

- [ ] **Step 6: Commit interview report polish**

Run:

```bash
git add frontend/src/pages/InterviewReport.vue frontend/src/components/ScoreSummary.vue frontend/src/components/QuestionReview.vue frontend/src/components/WeakAreaAnalysis.vue frontend/src/components/StudyPlan.vue
git commit -m "style: polish interview report"
```

Expected: commit succeeds. If a support component was not modified, omit it from `git add`.

---

### Task 6: Final Verification And Browser QA

**Files:**
- Modify only if QA reveals fixable visual or build issues in files already touched by Tasks 1-5.

**Interfaces:**
- Consumes: Completed UI redesign commits.
- Produces: Verified frontend build and local dev URL for user review.

- [ ] **Step 1: Scan edited frontend files for mojibake markers**

Run:

```bash
rg "姹|鏅|涓|鍖|闈|绠|璇|寮|宸|棣|杩|鎶|暂无|锛|.." frontend/src
```

Expected: no mojibake remains. Legitimate Chinese text such as `暂无数据` is allowed.

- [ ] **Step 2: Run production build**

Run: `npm run build`
Working directory: `frontend`
Expected: TypeScript check and Vite build complete successfully.

- [ ] **Step 3: Start local dev server**

Run: `npm run dev -- --host 127.0.0.1`
Working directory: `frontend`
Expected: Vite prints a local URL such as `http://127.0.0.1:5173/`.

- [ ] **Step 4: Browser-check desktop upload page**

Open the local URL in the browser. Expected:

- Header reads `Agentic RAG 求职助手`.
- First screen is the upload workflow.
- Upload panels are aligned, readable, and visually polished.
- Primary CTA is disabled until inputs are available.
- No visible mojibake.

- [ ] **Step 5: Browser-check mobile upload page**

Set viewport around `390x844`. Expected:

- Header content does not overlap.
- Upload columns stack into one column.
- Step indicator remains readable.
- Primary button text fits.

- [ ] **Step 6: Browser-check available report and interview states**

Open routes that can render without seeded backend data where possible:

```text
/
/interview/example-task
/match/example-task
/report/example-session
```

Expected:

- Loading/start/error states are readable.
- No obvious layout overflow.
- No visible mojibake in page chrome.

- [ ] **Step 7: Fix QA findings**

If any issue is found, edit the relevant touched file, then rerun:

```bash
npm run build
```

Expected: build succeeds after each fix.

- [ ] **Step 8: Commit final QA fixes**

If fixes were made, run:

```bash
git add frontend/src
git commit -m "style: finalize responsive UI polish"
```

Expected: commit succeeds.

If no fixes were needed, do not create an empty commit.

---

## Self-Review

- Spec coverage: Tasks 1-6 cover global shell, upload page, match report, interview page, interview report, component consistency, responsive behavior, build verification, browser QA, and mojibake cleanup.
- Placeholder scan: This plan uses exact files, exact strings, exact commands, and expected outcomes. No unresolved markers are present.
- Type consistency: Existing component prop/event interfaces are preserved and repeated consistently across tasks.
