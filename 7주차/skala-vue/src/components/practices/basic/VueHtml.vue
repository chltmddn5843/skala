<script setup>
import { ref } from 'vue'

const rawHtmlData = ref('이 글자는 <strong style="color: #42b883">초록색 굵은 글자</strong>입니다.')
</script>

<template>
  <div class="practice-section">
    <h2>v-html 디렉티브 실습</h2>
    <button @click="rawHtmlData = '<em style=\'color: tomato\'>기울어진 주황색 글자</em>'">
      HTML 변경
    </button>
    <h3>일반 보간법 {{}} 사용 결과:</h3>
    <p>{{ rawHtmlData }}</p>
    <br />
    <h3>v-html 디렉티브 사용 결과:</h3>
    <p v-html="rawHtmlData"></p>
  </div>
</template>
