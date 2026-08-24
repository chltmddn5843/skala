<script setup>
import { ref } from 'vue'

const inputValue = ref('')
const trustedHtml = '<strong style="color: #42b883">개발자가 작성한 HTML</strong>'
</script>

<template>
  <div class="practice-section">
    <h2>v-html XSS 학습</h2>
    <p>사용자 입력은 보간법으로 출력하면 HTML이 실행되지 않습니다.</p>
    <input v-model="inputValue" placeholder="<img src=x onerror=alert('XSS')>" />
    <p>안전한 출력: {{ inputValue }}</p>
    <p>신뢰할 수 있는 HTML만 v-html 사용:</p>
    <div v-html="trustedHtml"></div>
  </div>
</template>
