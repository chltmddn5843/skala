<script setup>
import { ref } from 'vue'

const newFruit = ref('')
const fruits = ref([
  { id: 1, name: '사과' },
  { id: 2, name: '바나나' },
  { id: 3, name: '딸기' },
])
let nextFruitId = 4
const user = ref({
  name: '홍길동',
  age: 25,
  role: '개발자',
})
const items = ref([
  { id: 'prod_101', name: '아이폰' },
  { id: 'prod_102', name: '갤럭시' },
])

function addFruit() {
  const name = newFruit.value.trim()
  if (!name) return

  fruits.value.push({ id: nextFruitId++, name })
  newFruit.value = ''
}
</script>

<template>
  <div class="practice-section">
    <h2>v-for 디렉티브 학습</h2>
    <h3>1) 배열 렌더링</h3>
    <form @submit.prevent="addFruit">
      <input v-model="newFruit" aria-label="새 과일" placeholder="과일 이름" />
      <button>추가</button>
    </form>
    <ul>
      <li v-for="(fruit, index) in fruits" :key="fruit.id">
        {{ index + 1 }}번 과일: {{ fruit.name }}
        <button type="button" @click="fruits.splice(index, 1)">삭제</button>
      </li>
    </ul>
    <h3>2) 객체 렌더링</h3>
    <ul>
      <li v-for="(value, key, index) in user" :key="key">[{{ index }}] {{ key }} : {{ value }}</li>
    </ul>
    <h3>3) 배열 내 객체 렌더링</h3>
    <ul>
      <li v-for="(item, index) in items" :key="item.id">[{{ index }}] {{ item.name }}</li>
    </ul>
  </div>
</template>
