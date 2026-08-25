# skala-vue 개발 및 트러블슈팅 정리

## 1. 프로젝트 구성

- Vue 3 + Vite 기반 프로젝트
- Vue Router: 화면 경로 관리
- Pinia: 전역 상태 관리
- Composition API: `ref`, `reactive`, `computed`, `watch`, `watchEffect` 실습
- 공통 스타일: `src/assets/exercise.css`, `src/assets/practice.css`

## 2. 주요 개발 내용

### 이벤트 객체

파일: `src/components/practices/basic/EventObject.vue`

- 이벤트 객체 자동 전달: `@click="getOnlyEvent"`
- 일반 인자와 함께 전달: `@click="getWithParam('회원A', $event)"`
- `type`, `clientX`, `clientY`, `target` 확인
- `target`과 `currentTarget` 비교

### 이벤트 수식자

파일: `src/components/practices/basic/EventModifier.vue`

- `.prevent`: 링크의 기본 이동 차단
- `.stop`: 부모 요소로 전달되는 이벤트 차단
- 일반 링크와 `.prevent` 링크 비교

### 양방향 데이터 바인딩

파일: `src/components/practices/basic/ModelModifier.vue`

- 기본 `v-model`: 입력 즉시 반영
- `.lazy`: 변경 확정 후 반영
- `.number`: 입력값을 숫자로 변환
- `.trim`: 앞뒤 공백 제거
- `.lazy.trim`: 수식자 조합

### 반응형 상태

파일: `src/components/practices/composition/ReactiveReactive.vue`

- `reactive()` 객체 상태 변경
- `reactive()` 배열 추가·삭제
- 상태 변경 시 화면 자동 갱신

### 날씨 컴포넌트

파일: `src/components/exercise/WeatherComposition.vue`

- 도시별 날씨 배열 출력
- `computed`를 이용한 검색 결과 계산
- `watch`를 이용한 선택 정보 감시
- `watchEffect`를 이용한 검색어 자동 추적
- 온도별 `hot`, `warm`, `cool` 상태 표시

### 지역 버튼 Hover 실습

파일: `src/components/exercise/WeatherRegionHover.vue`

- `v-for`로 지역 버튼 생성
- `@mouseenter`로 날씨 조회 함수 자동 호출
- `@focus`로 키보드 접근 지원
- `ref`: 선택 지역과 조회 횟수 관리
- `computed`: 선택 지역과 날씨 안내 문구 계산
- `watch`: 선택 데이터와 조회 횟수를 Console에 출력

### 스타일 정리

파일: `src/assets/exercise.css`

- 공통 색상을 CSS 변수로 통일
- 카드·입력창·버튼 스타일 단순화
- 입력창 포커스와 카드 Hover 효과 추가
- 모바일 반응형 레이아웃 추가

## 3. 주요 코드 패턴

### 이벤트 객체 전달

```vue
<button @click="handleClick">자동 전달</button>
<button @click="handleClickWithName('인천', $event)">직접 전달</button>
```

### 지역 버튼 반복 출력

```vue
<button
  v-for="city in weatherList"
  :key="city.id"
  @mouseenter="loadWeather(city)"
>
  {{ city.name }}
</button>
```

### 반응형 상태와 계산값

```js
const selectedCityId = ref('')

const selectedCity = computed(() =>
  weatherList.find((city) => city.id === selectedCityId.value),
)
```

### 상태 감시

```js
watch(selectedCity, (city) => {
  if (city) console.log('선택된 지역:', city)
})
```

## 4. 트러블슈팅

### CSS 파일을 찾지 못함

- 증상: `ENOENT`, `postcss-import`, `readFile` 오류
- 원인: `exercise.css` import 경로와 실제 파일명 불일치
- 해결: 실제 파일명과 `@import '@/assets/exercise.css'` 경로 일치 확인

### Pinia Store를 찾지 못함

- 증상: `Could not load src/stores/configStore`
- 원인: `UnitToggler.vue`가 존재하지 않는 Store를 import
- 해결: `src/stores/configStore.js` 생성 후 `useConfigStore` export

### Router 화면 파일을 찾지 못함

- 증상: `Could not resolve '../views/NotFoundView.vue'`
- 원인: Router에 등록된 404 컴포넌트 파일 누락
- 해결: `src/views/NotFoundView.vue` 생성 또는 해당 라우트 제거

### Vue 태그 종료 오류

- 증상: `Element is missing end tag`
- 원인: `</script>`, `</div>`, `</template>` 누락
- 해결: SFC 기본 구조와 태그 쌍 확인

```vue
<script setup>
</script>

<template>
  <div></div>
</template>
```

### 조건식 문법 오류

- 잘못된 코드: `item.temp >= 21 and item.temp < 25`
- 원인: Vue 템플릿은 JavaScript 표현식을 사용
- 해결: `and` 대신 `&&` 사용
- 단순화: 앞의 `v-if`가 25도 이상을 처리하므로 `v-else-if="item.temp >= 21"`만 사용

### Vite 내부 스택만 표시됨

- `TransformPluginContext`는 원인이 아닌 후속 호출 기록
- 오류 메시지의 첫 부분에서 `Could not resolve`, `ENOENT`, `SyntaxError` 확인
- `npm run build`로 전체 오류 재현

## 5. 확인 명령어

```bash
npm run dev
npm run build
npm run lint
```

- 개발 확인: `npm run dev`
- import·문법·빌드 확인: `npm run build`
- 코드 규칙 확인: `npm run lint`
