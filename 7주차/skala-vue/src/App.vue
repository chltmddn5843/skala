<template>
  <div class="practice-container">
    <nav class="navigation-bar">
      <RouterLink to="/">실습 홈</RouterLink>
      <RouterLink to="/crud">CRUD</RouterLink>
    </nav>
    <RouterView />
  </div>
</template>

<style>
/* ⚠️ 외부 스타일 파일(예: 버튼 디자인 뭉치)을 이 방 안으로 쏙 가리켜 가져옵니다 */
@import '@/assets/practice.css';

.navigation-bar {
  display: flex;
  gap: 16px;
  padding: 16px 0;
}

.navigation-bar .router-link-exact-active {
  font-weight: bold;
}
</style>
