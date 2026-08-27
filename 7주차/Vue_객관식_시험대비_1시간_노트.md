# Vue 객관식 시험 대비 1시간 노트

> 범위: Vue 입문 → Vue 문법 → Composition API → 컴포넌트
> 학습자료: `Frontend-framework_Vue.js` 25~178쪽
> 목표: 개념의 정의보다 **서로의 차이와 사용 목적**을 설명할 수 있게 한다.

---

## 0~8분: Vue 기본 개념

### Vue.js

- 사용자 인터페이스를 만들기 위한 JavaScript 프레임워크
- 화면을 작은 **컴포넌트** 단위로 나누어 조립한다.
- 데이터가 변경되면 Vue가 화면을 자동으로 갱신한다.

### MVVM

| 구성      | 의미                             |
| --------- | -------------------------------- |
| Model     | 애플리케이션의 데이터            |
| View      | 사용자가 보는 화면               |
| ViewModel | Model과 View를 연결하는 Vue 영역 |

**암기:** Vue는 View와 Model 사이를 ViewModel로 연결한다.

### Virtual DOM

1. 상태가 변경된다.
2. Vue가 새로운 Virtual DOM을 만든다.
3. 이전 Virtual DOM과 비교한다.
4. 실제 DOM에서 필요한 부분만 갱신한다.

### SPA

- 최초에 하나의 `index.html`을 받아 실행한다.
- 페이지 이동 시 전체 HTML을 다시 받지 않고 필요한 화면만 교체한다.
- 빠르고 자연스러운 사용자 경험이 장점이다.

### 양방향 데이터 바인딩

- 데이터가 바뀌면 화면이 바뀐다.
- 입력 화면이 바뀌면 데이터도 바뀐다.
- Vue에서는 주로 `v-model`을 사용한다.

---

## 8~15분: 프로젝트 구조와 SFC

### 핵심 파일

| 파일            | 역할                                    |
| --------------- | --------------------------------------- |
| `index.html`  | 브라우저가 처음 읽는 HTML,`#app` 제공 |
| `main.js`     | Vue 애플리케이션 생성 및 마운트         |
| `App.vue`     | 최상위 Root Component                   |
| `components/` | 재사용하는 컴포넌트 보관                |

### SFC(Single File Component)

하나의 `.vue` 파일에 화면, 로직, 스타일을 함께 작성한다.

```vue
<script setup>
const message = 'Hello Vue'
</script>

<template>
  <h1>{{ message }}</h1>
</template>

<style scoped>
h1 { color: blue; }
</style>
```

- `<script setup>`: 상태와 함수 작성
- `<template>`: 화면 구조 작성
- `<style scoped>`: 현재 컴포넌트에만 적용할 스타일 작성

---

## 15~30분: 핵심 디렉티브

Vue 디렉티브는 `v-`로 시작하는 특별한 HTML 속성이다.

### 텍스트 출력

```vue
<p>{{ message }}</p>
<p v-text="message"></p>
<div v-html="html"></div>
```

| 문법            | 특징                                   |
| --------------- | -------------------------------------- |
| `{{ value }}` | Text Interpolation 값을 텍스트로 출력 |
| `v-text`      | 요소의 전체 텍스트를 지정              |
| `v-html`      | 문자열을 실제 HTML로 해석              |

> `v-html`에 신뢰할 수 없는 사용자 데이터를 넣으면 XSS 공격 위험이 있다.

### 속성 바인딩: `v-bind`

```vue
<img v-bind:src="imageUrl">
<button :disabled="isDisabled">저장</button>
<div :class="{ active: isActive }"></div>
```

- 축약형은 `:`이다.
- HTML 속성, 클래스, 인라인 스타일을 동적으로 연결한다.

### 조건부 렌더링

```vue
<p v-if="score >= 90">A</p>
<p v-else-if="score >= 80">B</p>
<p v-else>C</p>

<p v-show="isVisible">보이거나 숨겨짐</p>
```

| 기준        | `v-if`             | `v-show`             |
| ----------- | -------------------- | ---------------------- |
| 동작        | DOM 생성·제거       | CSS`display` 변경    |
| 초기 비용   | 조건이 거짓이면 낮음 | 항상 렌더링하므로 높음 |
| 전환 비용   | 높음                 | 낮음                   |
| 적합한 경우 | 조건 변경이 드물 때  | 자주 보이고 숨겨질 때  |

### 반복 렌더링: `v-for`

```vue
<li v-for="item in items" :key="item.id">
  {{ item.name }}
</li>
```

- 배열이나 객체를 반복해 요소를 만든다.
- 각 항목을 식별할 수 있는 고유한 `:key`를 사용한다.

### 이벤트: `v-on`

```vue
<button v-on:click="increase">증가</button>
<button @click="count++">증가</button>
<form @submit.prevent="submitForm"></form>
```

- 축약형은 `@`이다.
- `$event`는 브라우저가 전달하는 이벤트 객체다.

| 수식어       | 의미                                     |
| ------------ | ---------------------------------------- |
| `.prevent` | 기본 동작 방지                           |
| `.stop`    | 이벤트 전파 중지                         |
| `.once`    | 한 번만 실행                             |
| `.self`    | 해당 요소가 직접 이벤트 대상일 때만 실행 |

### 폼 입력: `v-model`

```vue
<input v-model="name">
<input v-model.number="age">
<input v-model.trim="message">
<input v-model.lazy="keyword">
```

| 수식어      | 의미                                  |
| ----------- | ------------------------------------- |
| `.number` | 입력값을 숫자로 변환                  |
| `.trim`   | 앞뒤 공백 제거                        |
| `.lazy`   | `input` 대신 `change` 시점에 반영 |

---

## 30~43분: Composition API

### `ref()`

```vue
<script setup>
import { ref } from 'vue'

const count = ref(0)
count.value++
</script>

<template>
  <p>{{ count }}</p>
</template>
```

- 원시값과 객체 모두 반응형으로 만들 수 있다.
- JavaScript에서는 `.value`로 접근한다.
- 템플릿에서는 `.value`가 자동으로 해제된다.

### `reactive()`

```js
import { reactive } from 'vue'

const user = reactive({ name: 'Kim', age: 20 })
user.age++
```

- 객체, 배열, `Map`, `Set` 같은 참조형에 사용한다.
- 속성 접근 시 `.value`를 사용하지 않는다.

### `ref` vs `reactive`

| 기준         | `ref`         | `reactive`     |
| ------------ | --------------- | ---------------- |
| 대상         | 모든 값         | 주로 객체·배열  |
| Script 접근  | `.value` 필요 | 속성에 직접 접근 |
| 값 전체 교체 | 편리함          | 주의 필요        |

### `computed()`

바뀐 값을 computed(() => x.value * y.value)

value로 접근함

```js
const price = ref(1000)
const quantity = ref(2)
const total = computed(() => price.value * quantity.value)
```

- 다른 반응형 상태로부터 파생된 값을 계산한다.
- 의존 값이 바뀔 때 다시 계산한다.
- 계산 결과를 캐시한다.

### `watch()`

```js
watch(searchKeyword, (newValue, oldValue) => {
  console.log(newValue, oldValue)
})
```

- 감시할 대상을 직접 지정한다.
- 상태가 변경된 뒤 API 호출, 저장, 로그 같은 부수 효과를 수행한다.
- 여러 대상을 감시할 때 `watch([a, b], callback)`을 사용한다.
- 객체 내부까지 감시해야 하면 `{ deep: true }`를 사용할 수 있다.

### `watchEffect()`

```js
watchEffect(() => {
  console.log(searchKeyword.value)
})
```

- 콜백 내부에서 사용한 반응형 데이터를 자동 추적한다.
- 최초 등록 시에도 즉시 실행된다.

### computed vs watch vs watchEffect

| 기능            | 목적                    | 감시 대상 |
| --------------- | ----------------------- | --------- |
| `computed`    | 파생값 계산             | 자동 추적 |
| `watch`       | 변경 후 부수 효과       | 직접 지정 |
| `watchEffect` | 자동 추적하며 부수 효과 | 자동 추적 |

**판단법:** 새로운 값을 만들면 `computed`, 어떤 작업을 실행하면 `watch`.


## reactive 반응형 데이터

- 변경된 데이터가 여러번 바뀌면 중간과정의 롤백을 못함
- 객체 내부 값이 변경되어서 감시가 가능하기 위해서는 watch( () => .특정 속성 => {수행 함수} )



---

## 43~60분: 컴포넌트

### 지역 등록과 전역 등록

- 지역 등록: 사용하는 부모 컴포넌트에서 자식을 `import`
- 전역 등록: 애플리케이션 전체에서 별도 `import` 없이 사용
- 필요한 곳에서만 사용하는 지역 등록이 의존 관계를 파악하기 쉽다.

### 생명주기

| Hook            | 실행 시점                       | 주요 용도               |
| --------------- | ------------------------------- | ----------------------- |
| `onMounted`   | DOM에 장착된 후                 | 초기 API 요청, DOM 접근 |
| `onUpdated`   | 반응형 변경으로 DOM이 갱신된 후 | 갱신된 DOM 처리         |
| `onUnmounted` | 컴포넌트가 제거된 후            | 타이머·이벤트 정리     |

### Props: 부모 → 자식 데이터 전달

```vue
<!-- Parent.vue -->
<UserCard :user-name="name" :age="age" />
```

```vue
<!-- UserCard.vue -->
<script setup>
defineProps({
  userName: { type: String, required: true },
  age: { type: Number, default: 0 }
})
</script>
```

- Props는 부모가 자식에게 전달한다.
- 자식이 받은 Props는 **읽기 전용**이다.
- JavaScript에서는 `camelCase`, 템플릿 속성에서는 `kebab-case`를 사용한다.
- `type`, `required`, `default`, `validator`로 유효성을 검사할 수 있다.

### Emits: 자식 → 부모 이벤트 전달

```vue
<!-- Child.vue -->
<script setup>
const emit = defineEmits(['save'])

const requestSave = () => emit('save', { id: 1 })
</script>

<template>
  <button @click="requestSave">저장</button>
</template>
```

```vue
<!-- Parent.vue -->
<Child @save="handleSave" />
```

**한 문장 암기:** 데이터는 Props로 내려가고, 이벤트는 Emits로 올라간다.

### Provide / Inject

```js
// 상위 컴포넌트
provide('theme', 'dark')

// 하위 컴포넌트
const theme = inject('theme')
```

- 깊이 떨어진 컴포넌트에 데이터를 전달한다.
- 중간 컴포넌트가 사용하지 않는 Props를 계속 전달하는 **Props Drilling**을 줄인다.

### Slot

자식 컴포넌트의 일부 화면을 부모가 채울 수 있게 한다.

부모가 아무것도 입력안하면 <slot></slot><slot><slot</slot>슬랏 안에 있는 값 들어감


#### Default Slot

```vue
<!-- Card.vue -->
<div class="card"><slot /></div>

<!-- Parent.vue -->
<Card><p>본문</p></Card>
```

#### Named Slot

```vue
<!-- Layout.vue -->
<header><slot name="header" /></header>
<main><slot /></main>

<!-- Parent.vue -->
<Layout>
  <template #header>제목</template>
  <p>본문</p>
</Layout>
```

#### Scoped Slot

- 자식이 제공한 데이터를 부모의 슬롯 콘텐츠에서 사용한다.
- 일반적인 Props의 반대 방향처럼 보이지만, 목적은 **슬롯 내용 구성에 필요한 데이터 제공**이다.


---

## Vue Router Basic

- 웹페이지가 변화할 때 js 엔진이 가로채서 서버에 새 페이지를 요청하지 않고 현재 주소에 매칭되는 컴포넌트만 가상 DOM 상에서 실식산으로 교체해준다.





---

## 시험 직전 비교표

| 비교                     | 정답 기준                                  |
| ------------------------ | ------------------------------------------ |
| `v-if` / `v-show`    | DOM 생성·제거 / CSS로 숨김                |
| `v-bind` / `v-model` | 단방향 속성 연결 / 폼 양방향 연결          |
| `ref` / `reactive`   | 모든 값·`.value` / 객체 중심·직접 접근 |
| `computed` / `watch` | 파생값 계산 / 변경 후 작업                 |
| Props / Emits            | 부모→자식 데이터 / 자식→부모 이벤트      |
| Provide·Inject / Props  | 깊은 계층 전달 / 직접적인 부모·자식 전달  |
| Default / Named Slot     | 이름 없음 / 여러 영역을 이름으로 구분      |

---

## 5분 객관식 자가점검

정답을 가리고 먼저 풀어본다.

### 1

자주 열고 닫는 메뉴의 표시 여부를 제어하기 가장 적절한 디렉티브는?

1. `v-if`
2. `v-show`
3. `v-for`
4. `v-once`

### 2

`ref(0)`으로 만든 `count`를 `<script setup>`에서 1 증가시키는 코드는?

1. `count++`
2. `count.value++`
3. `count.get()++`
4. `ref.count++`

### 3

상품 가격과 수량으로 합계를 표시할 때 가장 적절한 기능은?

1. `watch`
2. `onMounted`
3. `computed`
4. `provide`

### 4

폼 제출 시 페이지가 새로고침되는 기본 동작을 막는 코드는?

1. `@submit.stop`
2. `@submit.prevent`
3. `@submit.once`
4. `@submit.self`

### 5

부모가 자식에게 데이터를 전달할 때 사용하는 것은?

1. Emits
2. Props
3. Slot
4. Watch

### 6

자식이 부모에게 저장 요청과 데이터를 전달하는 올바른 방법은?

1. 받은 Props를 자식이 직접 수정한다.
2. `defineEmits()`로 이벤트를 발생시킨다.
3. `computed()`를 사용한다.
4. `v-html`을 사용한다.

### 7

다음 중 `v-html`에 관한 설명으로 옳은 것은?

1. 문자열을 항상 일반 텍스트로 출력한다.
2. 이벤트를 연결한다.
3. 문자열을 HTML로 해석하며 XSS에 주의해야 한다.
4. 입력값을 숫자로 변환한다.

### 8

`watchEffect()`의 특징은?

1. 감시 대상을 배열로 반드시 지정해야 한다.
2. 내부에서 사용한 반응형 데이터를 자동 추적한다.
3. 계산 결과를 항상 캐시한다.
4. 컴포넌트가 제거될 때만 실행된다.

### 9

Props Drilling을 줄이기 위해 깊은 하위 컴포넌트에 값을 전달하는 기능은?

1. Provide / Inject
2. `v-show`
3. `onUpdated`
4. Named Slot

### 10

컴포넌트가 제거될 때 타이머를 해제하기 적절한 Hook은?

1. `onMounted`
2. `onUpdated`
3. `onUnmounted`
4. `computed`

<details>
<summary>정답 및 핵심 해설</summary>

1. **②** — `v-show`는 DOM을 유지해 반복 전환 비용이 낮다.
2. **②** — Script에서는 ref 값에 `.value`로 접근한다.
3. **③** — 기존 상태로부터 파생값을 만들 때 `computed`를 사용한다.
4. **②** — `.prevent`는 `preventDefault()`에 해당한다.
5. **②** — Props는 부모에서 자식으로 전달된다.
6. **②** — 자식은 Emits로 부모에게 이벤트와 payload를 보낸다.
7. **③** — 신뢰할 수 없는 HTML은 XSS 공격으로 이어질 수 있다.
8. **②** — 콜백 실행 중 사용된 반응형 값을 자동으로 추적한다.
9. **①** — Provide / Inject는 중간 단계의 불필요한 Props 전달을 줄인다.
10. **③** — 제거 시 발생하는 자원 정리는 `onUnmounted`에서 한다.

</details>

---

## 마지막 1분 암기 문장

> `:`는 속성, `@`는 이벤트, `v-model`은 양방향 입력이다.
> `v-if`는 DOM을 없애고, `v-show`는 CSS로 숨긴다.
> `ref`는 Script에서 `.value`, `reactive`는 객체 속성에 직접 접근한다.
> `computed`는 값을 만들고, `watch`는 작업을 실행한다.
> 데이터는 Props로 내려가고, 이벤트는 Emits로 올라간다.
