<script setup>
import { ref } from 'vue'

const position = ref('')
const tagName = ref('')
const getOnlyEvent = (e) => {
  console.log(e)
  position.value = `종류: ${e.type} / 좌표: X=${e.clientX}, Y=${e.clientY} / 클릭 요소: ${e.target.tagName}`
}
const getWithParam = (name, e) => {
  tagName.value = `대상: ${name} / 클릭된 태그: ${e.target.tagName}`
}
const compareTarget = (e) => {
  tagName.value = `target: ${e.target.tagName} / currentTarget: ${e.currentTarget.tagName}`
}
const

</script>

<template>
  <div class="practice-section">
    <h2>v-on 이벤트 객체($event) 활용</h2>
    <p>좌표: {{ position }}</p>
    <p>태그: {{ tagName }}</p>
    <button @click="getOnlyEvent">클릭 좌표 알아내기</button>
    <button @click="getWithParam('회원A', $event)">회원 정보와 태그 확인</button>
    <!--target와 currentTarget 비교-->
    <!--target: 이벤트가 발생한 실제 요소-->
    <!--currentTarget: 이벤트가 바인딩된 요소-->
    <button @click="compareTarget"><strong>target과 currentTarget 비교</strong></button>
  </div>
</template>


