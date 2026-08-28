<template>
  <div class="base-dashboard-card">
    <slot>기본 출력</slot>
  </div>
</template>

<style scoped>
.base-dashboard-card {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 10px;
  border: 2px solid #e9ecef;
  box-sizing: border-box;
  max-width: 100%;
  word-break: break-word;
  overflow: hidden;
}
</style>
