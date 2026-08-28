<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import UnitToggler from '@/components/exercise/UnitToggler.vue'

const route = useRoute()
const section = computed(() => route.meta.section)
</script>

<template>
  <header class="site-header">
    <h1>Vue 학습 내용 정리</h1>
    <nav class="section-nav" aria-label="학습 영역">
      <RouterLink to="/practice">📚 실습 내용</RouterLink>
      <RouterLink to="/exercise">🛠️ 자체 구현 기능</RouterLink>
    </nav>

    <nav v-if="section === 'practice'" class="sub-nav" aria-label="실습 메뉴">
      <RouterLink to="/practice">전체 실습</RouterLink>
      <RouterLink to="/practice/crud">CRUD 실습</RouterLink>
    </nav>

    <nav v-if="section === 'exercise'" class="sub-nav" aria-label="날씨 기능 메뉴">
      <RouterLink to="/exercise">날씨 대시보드</RouterLink>
      <RouterLink to="/exercise/about">서비스 소개</RouterLink>
      <UnitToggler />
    </nav>
  </header>

  <main :class="section === 'practice' ? 'practice-container' : 'app-container'">
    <RouterView />
  </main>
</template>

<style>
@import '@/assets/practice.css';
@import '@/assets/exercise.css';

.site-header {
  max-width: 900px;
  margin: 0 auto 24px;
  text-align: center;
}

.section-nav,
.sub-nav {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  padding: 12px;
}

.section-nav {
  font-size: 1.1rem;
  font-weight: 700;
  border-bottom: 1px solid #dfe6e9;
}

.section-nav a,
.sub-nav a {
  color: #7f8c8d;
}

.section-nav a.router-link-active,
.sub-nav a.router-link-exact-active {
  color: #3498db;
}
</style>
