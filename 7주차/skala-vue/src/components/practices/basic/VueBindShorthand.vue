<script setup>
import { ref } from 'vue'

const id = 'user-profile-card'
const src = 'https://vuejs.org/images/logo.png'
const size = ref(50)
</script>

<template>
  <div class="practice-section">
    <h2>v-bind 디렉티브 고급 (단축 문법)</h2>
    <div :id>
      <img :src :width="size" alt="Vue 로고" />
    </div>
    <button @click="size = size === 50 ? 100 : 50">로고 크기 변경</button>
  </div>
</template>
