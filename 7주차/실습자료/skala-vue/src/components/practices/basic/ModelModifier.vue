<script setup>
import { ref } from 'vue'

const normalText = ref('')
const lazyText = ref('')

const ageText = ref('')
const ageNumber = ref('')

const rawEmail = ref('')
const trimmedEmail = ref('')

const nickname = ref('')
</script>

<template>
  <div class="practice-section">
    <h2>v-model 수식어 실습</h2>

    <section>
      <h3>1. 기본 v-model과 .lazy 비교</h3>

      <label>
        기본 입력
        <input v-model="normalText" placeholder="입력 즉시 반영" />
      </label>

      <p>기본 입력 결과: "{{ normalText }}"</p>

      <label>
        .lazy 입력
        <input v-model.lazy="lazyText" placeholder="입력 후 Enter 또는 외부 클릭" />
      </label>

      <p>.lazy 결과: "{{ lazyText }}"</p>
    </section>

    <section>
      <h3>2. 기본 입력과 .number 비교</h3>

      <label>
        기본 숫자 입력
        <input v-model="ageText" type="number" placeholder="나이 입력" />
      </label>

      <p>
        값: {{ ageText }} /
        타입: {{ typeof ageText }}
      </p>

      <label>
        .number 숫자 입력
        <input v-model.number="ageNumber" type="number" placeholder="나이 입력" />
      </label>

      <p>
        값: {{ ageNumber }} /
        타입: {{ typeof ageNumber }}
      </p>
    </section>

    <section>
      <h3>3. 기본 입력과 .trim 비교</h3>

      <label>
        기본 이메일 입력
        <input v-model="rawEmail" type="email" placeholder="앞뒤에 공백을 넣어보세요" />
      </label>

      <p>
        값: "{{ rawEmail }}" /
        길이: {{ rawEmail.length }}
      </p>

      <label>
        .trim 이메일 입력
        <input
          v-model.trim="trimmedEmail"
          type="email"
          placeholder="앞뒤에 공백을 넣어보세요"
        />
      </label>

      <p>
        값: "{{ trimmedEmail }}" /
        길이: {{ trimmedEmail.length }}
      </p>
    </section>

    <section>
      <h3>4. .lazy.trim 수식자 조합</h3>

      <label>
        닉네임
        <input
          v-model.lazy.trim="nickname"
          placeholder="앞뒤 공백 입력 후 Enter 또는 외부 클릭"
        />
      </label>

      <p>
        처리된 값: "{{ nickname }}" /
        길이: {{ nickname.length }}
      </p>
    </section>
  </div>
</template>

<style scoped>
section {
  margin-bottom: 24px;
}

label {
  display: block;
  margin: 8px 0;
}

input {
  display: block;
  width: 100%;
  max-width: 400px;
  margin-top: 4px;
  padding: 8px;
}
</style>
