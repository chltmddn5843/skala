import { createRouter, createWebHistory } from 'vue-router'
import PracticeHomeView from '@/views/PracticeHomeView.vue'
import WeatherHomeView from '@/views/WeatherHomeView.vue'

const routes = [
  { path: '/', redirect: '/practice' },
  {
    path: '/practice',
    name: 'PracticeHome',
    component: PracticeHomeView,
    meta: { section: 'practice' },
  },
  {
    path: '/practice/crud',
    name: 'CrudPractice',
    component: () => import('@/components/practices/library/AxiosJson.vue'),
    meta: { section: 'practice' },
  },
  {
    path: '/exercise',
    name: 'WeatherHome',
    component: WeatherHomeView,
    meta: { section: 'exercise' },
  },
  {
    path: '/exercise/about',
    name: 'WeatherAbout',
    component: () => import('@/views/WeatherAboutView.vue'),
    meta: { section: 'exercise' },
  },
  {
    path: '/exercise/weather/:cityId',
    name: 'WeatherDetail',
    component: () => import('@/views/WeatherDetailView.vue'),
    meta: { section: 'exercise' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue'),
  },
]

// 라우트(routes) 객체를 생성하고, createRouter 함수를 사용하여 라우터 인스턴스를 생성
// createWebHistory()를 사용하여 HTML5 History 모드를 활성화합니다. 마지막으로, 생성된 라우터 인스턴스를 export default로 내보냅니다.

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
