 

# JavaScript 심화 시험 대비 노트

> 범위: 학습자료 8. JavaScript 심화, 233~263쪽
> 핵심: DOM, 이벤트, 비동기, Promise, async/await, Browser API, fetch, 모듈

## 1. 전체 흐름

```text
HTML 문서
  → DOM 객체로 변환
  → JavaScript로 요소 선택·변경
  → 이벤트로 사용자 행동 감지
  → 비동기로 서버와 통신
  → 받은 데이터로 DOM 갱신
```

---

## 2. DOM

### DOM이란? 

DOM(Document Object Model)은 브라우저가 HTML 문서를 JavaScript로 다룰 수 있도록 만든 **트리 구조의 객체 모델**이다.

```html
<body>
  <h1 id="title">Hello</h1>
</body>
```

```text
Document
└─ html
   └─ body
      └─ h1
         └─ "Hello" (Text Node)
```

- `document`: 전체 HTML 문서를 나타내는 객체
- Element Node: `html`, `body`, `h1` 같은 태그
- Attribute Node: `id`, `href` 같은 속성
- Text Node: 태그 안의 문자열
- DOM API: DOM을 선택하고 변경할 수 있는 메서드와 속성의 집합

### 요소 선택

```js
const title = document.getElementById('title')
const item = document.querySelector('.item')
const items = document.querySelectorAll('.item')
```

| 메서드                             | 결과                            |
| ---------------------------------- | ------------------------------- |
| `getElementById('id')`           | 해당 ID의 요소 하나             |
| `getElementsByTagName('li')`     | 해당 태그들의 컬렉션            |
| `getElementsByClassName('item')` | 해당 클래스들의 컬렉션          |
| `querySelector('.item')`         | CSS 선택자와 일치하는 첫 요소   |
| `querySelectorAll('.item')`      | CSS 선택자와 일치하는 모든 요소 |

### 요소 변경

```js
title.textContent = '안녕하세요'
title.innerHTML = '<strong>안녕하세요</strong>'
title.style.color = 'blue'
title.setAttribute('class', 'active')
```

| 기능                                       | 의미                        |
| ------------------------------------------ | --------------------------- |
| `textContent`                            | 문자열을 일반 텍스트로 처리 |
| `innerHTML`                              | 문자열을 HTML로 해석        |
| `element.attribute` / `setAttribute()` | HTML 속성 변경              |
| `style.property`                         | 인라인 스타일 변경          |

> 사용자 입력을 `innerHTML`에 직접 넣으면 XSS 위험이 있으므로 일반 텍스트는 `textContent`가 안전하다.

`document.write()`는 문서 로딩 후 실행하면 기존 문서를 덮어쓸 수 있어 일반적인 DOM 변경에는 사용하지 않는다.

---

## 3. 이벤트

이벤트는 클릭, 키 입력, 값 변경, 페이지 로딩처럼 브라우저에서 발생한 사건이다. 이벤트 핸들러는 사건이 발생했을 때 실행할 함수다.

### 주요 이벤트

| 이벤트                       | 발생 시점                 |
| ---------------------------- | ------------------------- |
| `click`                    | 한 번 클릭                |
| `dblclick`                 | 두 번 클릭                |
| `mouseover` / `mouseout` | 마우스 진입 / 이탈        |
| `keydown` / `keyup`      | 키를 누름 / 뗌            |
| `change`                   | 입력값 또는 선택값 변경   |
| `focus` / `blur`         | 포커스를 얻음 / 잃음      |
| `load`                     | 페이지나 리소스 로드 완료 |

### 이벤트 등록 방법

```html
<!-- 인라인: 비권장 -->
<button onclick="handleClick()">클릭</button>
```

```js
// DOM Property: 핸들러 하나만 유지됨
button.onclick = handleClick

// Event Listener: 권장
button.addEventListener('click', handleClick)
```

`addEventListener()`는 같은 이벤트에 여러 핸들러를 등록할 수 있고, 버블링과 캡처링도 제어할 수 있다.

### 이벤트 전파

중첩된 요소에서 이벤트가 발생하면 다른 조상 요소에도 이벤트가 전달된다.

```html
<div id="parent">
  <button id="child">클릭</button>
</div>
```

| 방식      | 방향         | 설정                          |
| --------- | ------------ | ----------------------------- |
| Bubbling  | 자식 → 부모 | 기본값, 세 번째 인자`false` |
| Capturing | 부모 → 자식 | 세 번째 인자`true`          |

```js
element.addEventListener('click', handler)       // 버블링
element.addEventListener('click', handler, true) // 캡처링
```

### 이벤트 제어

| 메서드                               | 역할                                      |
| ------------------------------------ | ----------------------------------------- |
| `event.preventDefault()`           | 링크 이동, 폼 제출 같은 기본 동작 방지    |
| `event.stopPropagation()`          | 부모·자식으로의 이벤트 전파 중단         |
| `event.stopImmediatePropagation()` | 전파와 현재 요소의 나머지 핸들러까지 중단 |
| `removeEventListener()`            | 등록한 이벤트 핸들러 제거                 |

```js
function handleClick(event) {
  event.preventDefault()
}

button.addEventListener('click', handleClick)
button.removeEventListener('click', handleClick)
```

`removeEventListener()`에는 등록할 때 사용한 것과 **동일한 함수 참조**를 전달해야 한다.

---

## 4. 동기와 비동기

### 동기(Synchronous)

앞 작업이 끝나야 다음 작업을 실행한다.

```js
console.log('A')
console.log('B')
console.log('C')
// A → B → C
```

### 비동기(Asynchronous)

시간이 오래 걸리는 작업을 기다리는 동안 다음 코드를 계속 실행한다.

```js
console.log('A')
setTimeout(() => console.log('B'), 0)
console.log('C')
// A → C → B
```

- JavaScript는 한 번에 하나의 작업을 실행하는 Single Thread 언어다.
- 타이머나 네트워크 작업은 브라우저 API에 맡긴다.
- 작업 완료 후 콜백이 Queue에 등록된다.
- Call Stack이 비면 Event Loop가 대기 중인 작업을 실행시킨다.

### 비동기 처리의 발전

```text
Callback → Promise → async/await
```

| 방식        | 특징                         | 문제 또는 장점               |
| ----------- | ---------------------------- | ---------------------------- |
| Callback    | 함수 안에 콜백 전달          | 중첩 시 Callback Hell        |
| Promise     | `.then()`·`.catch()`    | 상태와 오류 처리가 구조화됨  |
| async/await | Promise를 동기 코드처럼 표현 | 순서와 오류 처리가 읽기 쉬움 |

---

## 5. Promise

Promise는 비동기 작업의 미래 성공 또는 실패 결과를 나타내는 객체다.

### 세 가지 상태

| 상태          | 의미         |
| ------------- | ------------ |
| `pending`   | 작업 진행 중 |
| `fulfilled` | 작업 성공    |
| `rejected`  | 작업 실패    |

```js
const promise = new Promise((resolve, reject) => {
  const success = true

  if (success) resolve('성공 데이터')
  else reject(new Error('실패 이유'))
})

promise
  .then(value => console.log(value))
  .catch(error => console.error(error))
```

- `resolve(value)`: 성공시키고 값을 `.then()`으로 전달
- `reject(error)`: 실패시키고 이유를 `.catch()`로 전달
- `resolve()`와 `reject()`는 함수 실행 자체를 종료하지 않는다.
- 이후 코드 실행을 막으려면 `return resolve(value)`처럼 반환한다.

### Promise Chain

```js
step1()
  .then(value => step2(value))
  .then(value => step3(value))
  .then(result => console.log(result))
  .catch(error => console.error(error))
```

다음 비동기 작업의 순서를 보장하려면 `.then()`에서 Promise를 **return**해야 한다.

---

## 6. async와 await

### `async`

함수를 Promise를 반환하는 비동기 함수로 만든다.

```js
async function hello() {
  return '안녕하세요'
}

hello().then(value => console.log(value))
```

일반 값을 반환해도 다음과 같이 Promise로 감싸진다.

```js
return '안녕하세요'
// Promise.resolve('안녕하세요')와 같은 결과
```

### `await`

Promise가 처리될 때까지 **현재 async 함수의 실행만** 일시 정지하고, 성공 결과를 꺼낸다.

```js
async function run() {
  const first = await step1()
  const second = await step2(first)
  return second
}
```

- 일반적으로 `await`는 `async` 함수 안에서 사용한다.
- `await`가 전체 JavaScript 실행을 멈추는 것은 아니다.
- 기다리는 동안 바깥의 동기 코드는 계속 실행된다.

### 오류 처리

```js
async function loadData() {
  try {
    const response = await fetch('/data.json')

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const data = await response.json()
    console.log(data)
  } catch (error) {
    console.error('요청 실패:', error)
  }
}
```

- `await`로 기다리던 Promise가 reject되면 예외가 발생한다.
- `try...catch`로 실패를 처리한다.
- `fetch()`는 HTTP 404·500만으로 reject되지 않으므로 `response.ok`를 직접 검사한다.

### 실행 흐름

```js
async function example() {
  console.log('2')
  await Promise.resolve()
  console.log('4')
}

console.log('1')
example()
console.log('3')
// 1 → 2 → 3 → 4
```

1. `await` 전까지 즉시 실행한다.
2. `await`에서 async 함수만 잠시 멈춘다.
3. 남은 동기 코드를 실행한다.
4. Promise 후속 작업은 Microtask Queue에서 기다린다.
5. Call Stack이 비면 Event Loop가 후속 코드를 실행한다.

---

## 7. Browser API

Browser API는 브라우저가 JavaScript에 제공하는 기능이다.

| 종류        | 대표 API                                | 역할                    |
| ----------- | --------------------------------------- | ----------------------- |
| DOM API     | `querySelector`, `addEventListener` | HTML 조작과 이벤트 처리 |
| Timer API   | `setTimeout`, `setInterval`         | 지연·반복 실행         |
| Storage API | `localStorage`, `sessionStorage`    | 브라우저에 데이터 저장  |
| Network API | `fetch`                               | 서버와 비동기 통신      |

### Timer API

```js
const timeoutId = setTimeout(() => console.log('한 번'), 1000)
clearTimeout(timeoutId)

const intervalId = setInterval(() => console.log('반복'), 1000)
clearInterval(intervalId)
```

- `setTimeout`: 지정 시간 뒤 한 번 실행
- `setInterval`: 지정 간격마다 반복 실행
- 반환된 Timer ID로 타이머를 취소한다.
- 시간은 밀리초이며 1초는 1000ms다.

### Storage API

| 기준       | `localStorage`   | `sessionStorage`    |
| ---------- | ------------------ | --------------------- |
| 유지 기간  | 직접 삭제할 때까지 | 현재 탭을 닫을 때까지 |
| 탭 간 공유 | 같은 출처에서 가능 | 해당 탭에 한정        |
| 저장 형식  | 문자열             | 문자열                |

```js
localStorage.setItem('theme', 'dark')
const theme = localStorage.getItem('theme')
localStorage.removeItem('theme')
localStorage.clear()
```

객체는 JSON 문자열로 변환해 저장한다.

```js
localStorage.setItem('user', JSON.stringify(user))
const user = JSON.parse(localStorage.getItem('user'))
```

---

## 8. fetch

`fetch()`는 서버에 네트워크 요청을 보내며 Promise를 반환한다.

```js
async function getWeather() {
  const response = await fetch('/weather.json')

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`)
  }

  const data = await response.json()
  return data
}
```

두 번의 `await`가 필요한 이유:

1. `await fetch(...)`: HTTP 응답 객체를 기다린다.
2. `await response.json()`: 응답 본문을 읽고 JSON으로 변환하는 작업을 기다린다.

---

## 9. JavaScript Module

모듈은 파일별로 스코프를 분리하고 필요한 값만 `export`와 `import`로 공유한다.

### Named Export

```js
// math.js
export const pi = 3.14
export function add(a, b) {
  return a + b
}
```

```js
import { pi, add } from './math.js'
```

- 한 파일에서 여러 개를 내보낼 수 있다.
- 가져올 때 이름을 맞추고 중괄호를 사용한다.

### Default Export

```js
// calculator.js
export default function calculate() {}
```

```js
import calculate from './calculator.js'
```

- 한 모듈에서 하나만 사용할 수 있다.
- 가져오는 쪽에서 원하는 이름을 사용할 수 있다.
- 중괄호를 사용하지 않는다.

### 외부 Script와 Module 비교

| 기준      | 일반 외부 Script       | Module                               |
| --------- | ---------------------- | ------------------------------------ |
| 로드      | `<script src="...">` | `<script type="module" src="...">` |
| Scope     | 전역 공유              | 파일별 모듈 Scope                    |
| 변수 충돌 | 가능                   | 모듈 사이에서는 방지                 |
| 기능 공유 | 전역 변수·함수        | `import` / `export`              |
| 실행      | 일반적으로 즉시        | 기본적으로 지연 실행                 |

---

## 10. 시험 직전 비교표

| 비교                                     | 핵심 차이                                            |
| ---------------------------------------- | ---------------------------------------------------- |
| HTML / DOM                               | 원본 마크업 / 브라우저가 만든 객체 트리              |
| `textContent` / `innerHTML`          | 일반 텍스트 / HTML로 해석                            |
| Bubbling / Capturing                     | 자식→부모 / 부모→자식                              |
| `preventDefault` / `stopPropagation` | 기본 행동 취소 / 이벤트 전파 중단                    |
| 동기 / 비동기                            | 완료 후 다음 작업 / 기다리는 동안 다음 작업 진행     |
| Promise / async-await                    | `.then`·`.catch` / Promise를 동기 코드처럼 표현 |
| `resolve` / `reject`                 | Promise 성공 / Promise 실패                          |
| `setTimeout` / `setInterval`         | 한 번 / 반복                                         |
| Local / Session Storage                  | 직접 삭제 전까지 / 탭 종료까지                       |
| Named / Default Export                   | 여러 개·중괄호 / 하나·중괄호 없음                  |

## 11. 객관식 자가점검

1. DOM은 무엇인가?① JavaScript 컴파일러 ② HTML의 객체 트리 ③ 서버 데이터베이스 ④ CSS 전처리기
2. CSS 선택자로 첫 번째 요소를 찾는 메서드는?① `querySelector` ② `querySelectorAll` ③ `getElementsByTagName` ④ `write`
3. 폼 제출의 기본 새로고침을 막는 메서드는?① `stopPropagation` ② `preventDefault` ③ `clearInterval` ④ `removeEventListener`
4. 기본 이벤트 전파 방향은?① 부모→자식 ② 자식→부모 ③ 형제→형제 ④ 전파하지 않음
5. Promise가 가질 수 없는 상태는?① pending ② fulfilled ③ rejected ④ mounted
6. `async` 함수의 반환값은?① 항상 Promise ② 항상 문자열 ③ 항상 `undefined` ④ DOM Element
7. `await`에 대한 옳은 설명은?① 전체 JavaScript 엔진을 멈춘다. ② 현재 async 함수의 실행을 일시 정지한다. ③ Promise를 만들 수 없다. ④ 실패를 자동으로 무시한다.
8. `fetch()`의 반환값은?① JSON 문자열 ② DOM Node ③ Promise ④ Timer ID
9. 탭을 닫으면 삭제되는 저장소는?① `localStorage` ② `sessionStorage` ③ DOM ④ Cache API
10. Default Export를 import하는 올바른 문법은?
    ① `import { value } from './a.js'` ② `import value from './a.js'` ③ `include value` ④ `require { value }`

<details>
<summary>정답과 핵심 해설</summary>

1. **②** - 브라우저가 HTML을 트리 형태의 객체로 표현한다.
2. **①** - `querySelector()`는 첫 요소, `querySelectorAll()`은 모든 요소를 반환한다.
3. **②** - 브라우저의 기본 동작을 취소한다.
4. **②** - 기본값은 자식에서 부모로 올라가는 버블링이다.
5. **④** - `mounted`는 Promise 상태가 아니다.
6. **①** - 일반 값을 반환해도 Promise로 감싸진다.
7. **②** - 바깥 동기 코드는 계속 실행된다.
8. **③** - 응답을 나타내는 Promise를 반환한다.
9. **②** - 현재 탭 세션이 끝나면 삭제된다.
10. **②** - Default Import에는 중괄호가 없다.

</details>

## 마지막 1분 암기

> DOM은 HTML의 객체 트리이며 `document`로 접근한다.
> 이벤트 기본 전파는 자식에서 부모로 올라가는 버블링이다.
> Promise는 pending에서 fulfilled 또는 rejected로 바뀐다.
> `async` 함수는 항상 Promise를 반환하고, `await`는 현재 async 함수만 기다리게 한다.
> `fetch()`와 `response.json()`은 모두 비동기이므로 각각 `await`한다.
