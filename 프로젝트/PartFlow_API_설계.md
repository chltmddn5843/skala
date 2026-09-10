# PartFlow MES API 설계

## 범위와 원칙

- 기준 자료: `PartFlow-API.yml`, `PartFlow-DB.dbml`, `PartFlow-wireframes-code/`.
- Base URL은 `/api`이며, 로그인 세션의 역할(`MANAGER`, `OPERATOR`, `QUALITY`)로 권한을 확인한다.
- 모든 오류는 `code`, `message`, `fieldErrors`를 포함한 공통 오류 형식으로 응답한다.
- 생성·변경 API는 서버가 상태 전이와 수량 검증을 수행한다. 화면은 성공 응답 뒤에만 목록·상세를 갱신한다.

## 화면·Actor별 API 흐름

| Actor | 화면 흐름 | 호출 순서 | 핵심 규칙 |
| --- | --- | --- | --- |
| 생산관리자 | S01 → S02 → S03 → S04 | `POST /auth/login` → `GET /dashboard` → `GET/POST /work-orders` → `POST /work-orders/{id}/close` | 지시는 `PLANNED → IN_PROGRESS → CLOSED` 순서만 허용한다. 종료 시 누적 실적을 다시 확인한다. |
| 작업자 | S01 → S04 → S05 | `POST /auth/login` → `GET /work-orders/{id}` → `POST /work-orders/{id}/start` → `POST /work-orders/{id}/lots` → `POST /work-orders/{id}/lots/{lotId}/anomalies` | 작업 시작 뒤에만 LOT를 등록한다. LOT 수량은 양수이며 지시 목표수량을 넘지 않는다. |
| 품질 담당자 | S01 → S05 → S06 → S05 | `POST /auth/login` → `GET /lots/{id}` → `POST /lots/{id}/inspection` → `GET /lots/{id}/related` → `POST /lots/{id}/ai-summaries` → `POST /ai-summaries/{id}/reviews` | 검사가 확정된 LOT만 AI 요약을 생성한다. 검토본은 AI 원문을 수정하지 않고 별도 이력으로 저장한다. |
| 공통 조회 | S02/S04/S05 | `GET /products`, `GET /equipment`, `GET /work-orders/{id}`, `GET /lots`, `GET /lots/{id}` | 목록 필터와 상세의 ID는 URL path/query로 전달하고, 조회 권한은 로그인 역할별로 제한한다. |

## 기능별 계약

| 기능 | API | 요청 데이터 | 성공 결과·화면 이동 |
| --- | --- | --- | --- |
| 로그인 | `POST /auth/login` | 사용자명, 비밀번호 | 세션과 사용자 역할 반환 후 역할별 첫 화면으로 이동한다. |
| 현황 조회 | `GET /dashboard?from&to&productId` | 기간, 선택 품목 | 생산·검사·불량 지표와 검사대기 LOT를 S02에 표시한다. |
| 작업지시 생성 | `POST /work-orders` | 품목, 설비, 목표수량, 예정일 | 생성된 지시를 S03 목록에 반영하고 S04 상세로 이동한다. |
| 지시 시작·종료 | `POST /work-orders/{id}/start`, `POST /work-orders/{id}/close` | 없음 | 현재 상태를 반환하고 S04의 버튼·상태 배지를 갱신한다. |
| LOT 실적·이상 등록 | `POST /work-orders/{id}/lots`, `POST /work-orders/{id}/lots/{lotId}/anomalies` | LOT 번호, 수량, 작업 메모 / 이상유형, 수량, 메모 | LOT와 누적 실적을 갱신하고 S05 LOT 상세로 이동한다. |
| 검사 확정 | `POST /lots/{id}/inspection` | 검사 항목별 수량, 메모 | 자동 합계 검증 후 검사 이력과 상태를 S05에 반영한다. |
| 관련 LOT 조회·AI 요약 | `GET /lots/{id}/related`, `POST /lots/{id}/ai-summaries` | 관련 LOT 선택값 `relatedLotIds` | 기준 LOT는 항상 포함하고, 선택된 관련 LOT를 함께 분석해 요약 이력을 S05에 추가한다. |
| AI 요약 검토 | `POST /ai-summaries/{id}/reviews` | `reviewedText` | 검토본을 별도 저장하고 S05 검토 이력에 표시한다. |

## 상태·검증 규칙

1. 로그인하지 않은 요청은 `401`, 역할 권한이 없는 변경 요청은 `403`으로 처리한다.
2. 작업지시 시작은 `PLANNED`에서만, 종료는 `IN_PROGRESS`에서만 가능하다.
3. LOT 등록과 이상 등록은 진행 중인 작업지시에서만 가능하며, 등록 뒤 지시 누적 실적과 LOT 수량을 같은 트랜잭션으로 갱신한다.
4. 검사 확정은 검사 합계가 생산수량과 일치할 때만 허용한다. 이미 확정된 LOT는 중복 확정하지 않는다.
5. `relatedLotIds`는 현재 LOT 자신을 제외하고 `GET /lots/{id}/related` 결과에 포함된 ID만 허용한다. 생략하면 기준 LOT만으로 요약한다.
6. AI 공급자 실패·시간 초과는 `AiSummary`를 `FAILED` 상태로 저장한 뒤 `201`로 반환한다. 화면은 실패 이력을 보여주고 재생성을 허용한다.

## 최소 통합 확인

- 생산관리자가 작업지시를 생성하고 작업자가 시작한 뒤, LOT를 등록할 수 있다.
- 검사 수량 합계가 생산수량과 다르면 검사 확정이 거절된다.
- 검사 확정 전 AI 생성은 거절되고, 확정 후 선택한 관련 LOT가 요약 요청에 포함된다.
- 품질 담당자의 검토 저장 뒤 AI 원문과 검토 이력이 함께 조회된다.
