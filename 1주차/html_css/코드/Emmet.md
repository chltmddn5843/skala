
## 링크 
https://polarized-pig-889.notion.site/Emmet-362f617e78e3806393a1d659395c8a7a



## 1. ! — HTML 기본 뼈대 (압도적 1위)

!  →  Tab

html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
</body>
</html>새 파일을 만들 때마다 무조건 첫 입력입니다. JSFiddle/CodePen이 숨겨주던 뼈대가 이것이라고 연결해서 설명하면 VSC 전환 브리지로도 완벽합니다. (lang="en"을 ko로 바꾸는 것까지 세트로 가르치세요.)


## 2. .클래스명 — class 있는 div
.card  →  <div class="card"></div>
.card>img+h1+p  →  카드 구조 한 번에태그를 생략하면 div가 기본입니다. 교재 예제 1의 카드가 한 줄로 나오는 걸 보여주면 반응이 좋아요. (#todoList처럼 #을 쓰면 id가 됩니다.)

## 3. ul>li*4 — 자식(>)과 반복(*)
ul>li*4  →  Tab

html
<ul>
  <li></li>
  <li></li>
  <li></li>
  <li></li>
</ul>메뉴, 목록, TodoList 등 반복 구조 필수기. ul.menu>li*4>a까지 확장하면 예제 2의 내비게이션 뼈대가 통째로 나옵니다.
4. + 와 {텍스트} — 형제 나열과 내용 채우기
h1{오늘 할 일}+input+button{추가}  →  Tab

html
<h1>오늘 할 일</h1>
<input type="text">
<button>추가</button>+는 나란히(형제), {}는 태그 안 텍스트. TodoList 입력부가 한 줄에 완성됩니다.
5. $ — 자동 번호 매기기
ul>li{항목 $}*3  →  Tab

html
<ul>
  <li>항목 1</li>
  <li>항목 2</li>
  <li>항목 3</li>
</ul>더미 데이터를 채울 때 최고입니다. 갤러리 카드 여러 장 만들 때 section>div.photo-card$*4 식으로 응용됩니다.
수업 마무리용 종합 예시 — 5가지가 다 들어간 한 줄:
div.todo-app>h1{📝 오늘 할 일}+div.input-row>input+button{추가}^ul#todoList>li{할 일 $}*3(^는 한 단계 위로 올라가기) — 이 한 줄이 교재 예제 6의 HTML 전체입니다. "여러분이 손으로 쳤던 그 코드, 이제 한 줄"이라는 시연으로 쓰시면 Emmet의 존재 이유가 바로 각인됩니다.