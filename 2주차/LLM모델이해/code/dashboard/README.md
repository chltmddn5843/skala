# STEP GUARD Dashboard

별도 프런트엔드 빌드 과정이 없는 웹 대시보드입니다. CSV 데모는 정적으로 동작하고, AI 일정 생성은 Vercel Serverless Function에서 OpenAI API를 호출합니다.

## 개인 API 키 설정

실제 키를 소스코드나 `app.js`에 입력하지 않습니다. Vercel 프로젝트의 **Settings → Environment Variables**에 다음 값을 등록합니다.

```text
OPENAI_API_KEY=개인_API_키
OPENAI_MODEL_NAME=gpt-4o-mini
DASHBOARD_ACCESS_TOKEN=대시보드_실행용_별도_비밀번호
```

- `OPENAI_API_KEY`: 필수. 서버 함수에서만 읽습니다.
- `OPENAI_MODEL_NAME`: 선택. 없으면 `gpt-4o-mini`를 사용합니다.
- `DASHBOARD_ACCESS_TOKEN`: 공개 URL에서 다른 사람이 API 비용을 발생시키지 못하도록 설정하는 별도 비밀번호입니다.

환경변수를 저장한 다음 Vercel에서 다시 배포합니다. 대시보드에서 **AI 일정 생성**을 누르면 접근 토큰을 한 번 입력하고 브라우저 세션 동안만 보관합니다.

## 로컬 실행

`dashboard` 디렉터리에서 다음 명령을 실행합니다.

CSV 화면만 확인할 때는 `python3 -m http.server 4173`을 사용합니다. AI 서버 함수까지 확인하려면 Vercel CLI 설치 후 다음을 사용합니다.

```Shell
vercel dev
```

브라우저에서 `http://localhost:4173`을 엽니다. `index.html`을 직접 열면 브라우저 보안정책 때문에 CSV를 불러오지 못할 수 있습니다.

## Vercel 배포

1. Vercel에서 새 프로젝트를 생성합니다.
2. 저장소를 연결하거나 이 `dashboard` 디렉터리를 업로드합니다.
3. Framework Preset은 `Other`, Root Directory는 `LLM모델이해/code/dashboard`로 지정합니다.
4. Build Command와 Output Directory는 비워 두고 배포합니다.

CLI를 사용한다면 `dashboard` 디렉터리에서 `vercel`을 실행하면 됩니다. 배포 후 환경변수를 등록하고 다시 배포해야 AI 기능이 활성화됩니다.

## AI 실행 흐름

```text
브라우저의 계획월
       ↓
Vercel /api/plan — OPENAI_API_KEY는 여기에서만 사용
       ↓
기계 분석 ─┐
           ├→ 점검 종류·우선순위 → 현장 일정
이용객 분석┘
       ↓
긴급·수시특별·자체점검 + 날짜·교대별 인력운영안
       ↓
대시보드 반영 및 CSV 다운로드
```

기계 분석과 이용객 분석은 동시에 호출하고, 점검 분류와 일정 생성은 순서대로 실행합니다. 한 번의 버튼 실행에 총 4회의 모델 요청이 발생합니다.

## 데이터 갱신

- `data/facilities.csv`: 시설정보
- `data/failures.csv`: 고장이력
- `data/passengers.csv`: 이용객패턴
- `data/workers.csv`: 작업자정보
- `data/emergency.csv`: 긴급점검 일정
- `data/special.csv`: 수시특별점검 일정
- `data/self.csv`: 자체점검 일정
- `data/staffing.csv`: 인력운영안

브라우저에서 수정한 날짜와 승인상태는 로컬 저장소에만 임시 저장됩니다. AI가 만든 결과는 자동 확정되지 않으며 현장 책임자의 승인이 필요합니다.
