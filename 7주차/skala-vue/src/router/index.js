import { createRouter, createWebHistory } from 'vue-router'
import PracticeHomeView from '../views/PracticeHomeView.vue'

const routes = [
  {
    path: '/',
    name: 'PracticeHome',
    component: PracticeHomeView,
  },
  {
    path: '/crud',
    name: 'Crud',
    component: () => import('../components/practices/library/AxiosJson.vue'),
  },
  {
    path: '/about',
    name: 'WeatherAbout',
    component: () => import('../views/WeatherAboutView.vue'),
  },
  {
    path: '/weather/:cityId',
    name: 'WeatherDetail',
    component: () => import('../views/WeatherDetailView.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFoundView.vue'),
  }, // lazy-loading : 동적 import
]

// 라우트(routes) 객체를 생성하고, createRouter 함수를 사용하여 라우터 인스턴스를 생성
// createWebHistory()를 사용하여 HTML5 History 모드를 활성화합니다. 마지막으로, 생성된 라우터 인스턴스를 export default로 내보냅니다.

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
