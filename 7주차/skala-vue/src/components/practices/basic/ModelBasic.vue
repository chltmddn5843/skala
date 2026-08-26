# 4. Vue Form Handling (v-model)
# 기존 내용
# 1. v-model 축약 문법 (양방향)
# 2. v-model의 내부 작동 원리 (단방향 + 이벤트)

<script setup>
import { ref } from 'vue'

const name = ref('')
const agreed = ref(false)
const gender = ref('')
const hobbies = ref([])
const city = ref('')
</script>

<template>
  <input v-model="name" />

  <input v-model="agreed" type="checkbox" />
  약관 동의

  <input v-model="gender" type="radio" value="male" />
  남성
  <input v-model="gender" type="radio" value="female" />
  여성

  <input v-model="hobbies" type="checkbox" value="운동" />
  운동
  <input v-model="hobbies" type="checkbox" value="독서" />
  독서

  <select v-model="city">
    <option value="">도시 선택</option>
    <option value="서울">서울</option>
    <option value="부산">부산</option>
  </select>

  <pre>{{ { name, agreed, gender, hobbies, city } }}</pre>
</template>
