# PartFlow MES 요구사항정의서

기준 자료: `PartFlow_MES_기획안_v2.md`, `PartFlow-API.yml`, `PartFlow-DB.dbml`, `PartFlow_액터별_데이터흐름.md`

## 1. 기능 요구사항

작업지시·LOT·검사·AI 메모 요약 기능을 역할별로 정의한다. 우선순위는 `PartFlow_스프린트계획.md`의 P0/P1/P2를 따른다.

| 요구사항 ID | 대분류 | 세부분류 | 요구사항명 | 상세 요구사항 내용 | 수요자/요청자 | 우선순위 | 관련 화면 ID |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-FUNC-001 | 인증 | 로그인·로그아웃 | 역할 기반 로그인 | 아이디·비밀번호로 로그인, 세션 종료로 로그아웃. 역할(MANAGER/OPERATOR/QUALITY)별 접근 화면이 다르다. | 전체 내부 역할 | P0 | S01 |
| REQ-FUNC-002 | 생산 | 작업지시 | 작업지시 생성 | 품목·목표수량·예정일 입력, 생성 시 상태는 `PLANNED`. 목표수량은 양의 정수만 허용, 없는 품목은 거절. | 생산관리자 | P0 | S03 |
| REQ-FUNC-003 | 생산 | 작업지시 | 작업 시작 | `PLANNED` 상태 지시만 작업자가 시작 가능, 상태는 `IN_PROGRESS`로 전환. 그 외 상태에서 시작 시도 시 409. | 작업자 | P0 | S04 |
| REQ-FUNC-004 | 생산 | 작업지시 | 작업지시 종료 | `IN_PROGRESS` 지시만 생산관리자가 종료 가능. 연결 LOT 수량의 합계가 목표수량 미달이면 종료 사유가 필수이며, 누락 시 400을 반환. | 생산관리자 | P0 | S04 |
| REQ-FUNC-005 | 생산 | LOT | LOT 생산실적 등록 | LOT번호·설비·수량·생산시간(시작~종료)·메모 입력. LOT번호는 전역 유일, 지시 누적목표 초과 시 거절. | 작업자 | P0 | S04 |
| REQ-FUNC-006 | 품질 | 이상징후 | 이상징후 등록 | 유형·발생시각·관찰내용 입력. 등록되면 검사 전까지 LOT 품질상태가 '확인대기'로 표시. | 작업자 | P1 | S04, S02 |
| REQ-FUNC-007 | 품질 | 검사 | 검사 확정(자동판정) | 제품별 측정값 입력 → 서버가 LOT 생성 시점 규격(`inspection_specs`)과 비교해 PASS/FAIL 자동 판정. 측정값 개수는 생산수량과 일치해야 하며 LOT당 1회만 확정. | 품질담당자 | P0 | S06 |
| REQ-FUNC-008 | 품질 | 조회 | 관련 LOT 후보 조회 | 같은 품목·설비·생산일 기준으로 다른 LOT을 후보로 제시(매 조회 시 재계산, 저장 없음). | 품질담당자 | P1 | S05 |
| REQ-FUNC-009 | AI | 요약 | AI 인수인계 요약 생성 | 검사 완료 LOT만 생성 가능. 기준 LOT은 항상 포함, `relatedLotIds`로 선택한 관련 LOT도 함께 분석. 실패해도 이력(`FAILED`) 저장 후 재시도 가능. | 품질담당자 | P2 | S05 |
| REQ-FUNC-010 | AI | 검토 | AI 요약 검토본 저장 | 검토문 저장, AI 원문은 수정하지 않고 이력으로 누적. `FAILED` 원문은 검토 대상에서 제외. | 품질담당자 | P2 | S05 |
| REQ-FUNC-011 | 조회 | 현황 | 생산·품질 현황 조회 | 기간·품목 필터로 생산수량·검사수량·부적합률(Σ부적합/Σ검사수량)·검사대기 LOT 수를 표시. | 생산관리자·전체 | P1 | S02 |
| REQ-FUNC-012 | 조회 | LOT | LOT 목록·상세 조회 | LOT 번호·기간·품목·검사상태로 필터링, 상세에서 생산·검사·측정값·AI 이력을 통합 조회. | 전체 내부 역할 | P0/P1 | S05, S02 |

## 2. 추적성 매트릭스

요구사항 → 화면 → API → DB 테이블의 연결을 명시해, 화면에서 쓰는 데이터가 API·DB까지 끊김 없이 이어지는지 확인한다.

| REQ | 요구사항명 | 관련 화면 ID | 호출 API | 관련 DB 테이블 |
| --- | --- | --- | --- | --- |
| REQ-FUNC-001 | 역할 기반 로그인 | S01 | `POST /auth/login`, `POST /auth/logout`, `GET /auth/me` | users |
| REQ-FUNC-002 | 작업지시 생성 | S03 | `POST /work-orders` | work_orders, products |
| REQ-FUNC-003 | 작업 시작 | S04 | `POST /work-orders/{id}/start` | work_orders |
| REQ-FUNC-004 | 작업지시 종료 | S04 | `POST /work-orders/{id}/close` | work_orders |
| REQ-FUNC-005 | LOT 생산실적 등록 | S04 | `POST /work-orders/{id}/lots` | production_lots, equipment, inspection_specs |
| REQ-FUNC-006 | 이상징후 등록 | S04, S02 | `POST /work-orders/{id}/lots/{lotId}/anomalies` | production_lots |
| REQ-FUNC-007 | 검사 확정(자동판정) | S06 | `POST /lots/{id}/inspection` | inspections, measurements, inspection_specs |
| REQ-FUNC-008 | 관련 LOT 후보 조회 | S05 | `GET /lots/{id}/related` | production_lots, work_orders (저장 없음, 계산만) |
| REQ-FUNC-009 | AI 요약 생성 | S05 | `POST /lots/{id}/ai-summaries` | ai_summaries, ai_summary_related_lots |
| REQ-FUNC-010 | AI 요약 검토본 저장 | S05 | `POST /ai-summaries/{id}/reviews` | summary_reviews |
| REQ-FUNC-011 | 현황 조회 | S02 | `GET /dashboard` | work_orders, production_lots, inspections, measurements (집계만) |
| REQ-FUNC-012 | LOT 목록·상세 조회 | S05, S02 | `GET /lots`, `GET /lots/{id}` | production_lots, inspections, measurements, ai_summaries, summary_reviews |

## 3. 범위 제외 (Out of Scope)

- 재고관리, 설비 자동연동(수기 입력 전제), 재작업, 출하 연동
- 치수검사 외 외관·기타 부적합 유형 분류(대표 사유 단순화)
- 재검사(LOT당 검사는 1회 확정)
- 알림, 파일 첨부, 외부 ERP 연동
