import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'upload',
      component: () => import('../pages/UploadPage.vue'),
    },
    {
      path: '/match/:taskId',
      name: 'match',
      component: () => import('../pages/MatchReport.vue'),
    },
    {
      path: '/interview/:sessionId',
      name: 'interview',
      component: () => import('../pages/InterviewPage.vue'),
    },
    {
      path: '/report/:sessionId',
      name: 'report',
      component: () => import('../pages/InterviewReport.vue'),
    },
  ],
})

export default router
