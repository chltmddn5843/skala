# PartFlow MES 스프린트 계획

## 우선순위

- **P0**: 로그인, 작업지시, 작업 시작, LOT 실적, 검사 확정. 생산·품질 업무가 끝까지 이어지는 최소 흐름이다.
- **P1**: 현황 대시보드, LOT·지시 조회, 이상 등록, 관련 LOT 조회.
- **P2**: AI 요약 생성·실패 이력·검토 이력. P0 검사 데이터가 있어야 의미 있는 결과를 만든다.

## Sprint 1 — 작업지시와 접근 제어

| 구분 | 내용 |
| --- | --- |
| 목표 | 역할별 로그인 후 생산관리자가 지시를 만들고 작업자가 시작할 수 있게 한다. |
| 백엔드 | `POST /auth/login`, `POST /auth/logout`, `GET /auth/me`, `GET /products`, `GET /equipment`, `GET/POST /work-orders`, `GET /work-orders/{id}`, `POST /work-orders/{id}/start` |
| 프론트 연결 | S01 로그인, S03 지시 목록·등록, S04 지시 상세·시작 버튼 |
| 완료 기준 | 세 역할의 권한이 구분되고, 생산관리자가 만든 `PLANNED` 지시만 시작되어 `IN_PROGRESS` 상세 화면에 표시된다. |
| 제외 | LOT 등록, 검사, AI 요약은 다음 스프린트로 미룬다. |

## Sprint 2 — 생산 실적과 품질 검사

| 구분 | 내용 |
| --- | --- |
| 목표 | 작업자가 LOT 실적과 이상을 남기고, 품질 담당자가 검사 확정까지 완료한다. |
| 백엔드 | `POST /work-orders/{id}/lots`, `POST /work-orders/{id}/lots/{lotId}/anomalies`, `GET /lots`, `GET /lots/{id}`, `POST /lots/{id}/inspection`, `POST /work-orders/{id}/close` |
| 프론트 연결 | S04 LOT 실적·이상 입력, S05 LOT 상세, S06 검사 입력 |
| 완료 기준 | 등록된 LOT가 지시 누적 실적에 반영되고, 검사 합계 불일치는 저장되지 않으며, 검사 확정 결과가 LOT 상세에 나타난다. |
| 제외 | AI 요약과 대시보드는 다음 스프린트로 미룬다. |

## Sprint 3 — 현황과 AI 인수인계

| 구분 | 내용 |
| --- | --- |
| 목표 | 생산관리자는 현황을 보고, 품질 담당자는 검사 완료 LOT를 AI로 요약·검토한다. |
| 백엔드 | `GET /dashboard`, `GET /lots/{id}/related`, `POST /lots/{id}/ai-summaries`, `POST /ai-summaries/{id}/reviews` |
| 프론트 연결 | S02 현황, S05 관련 LOT 선택·AI 요약·검토 이력 |
| 완료 기준 | 기간·품목 필터 결과가 S02 지표에 반영되고, 검사 완료 LOT만 AI 생성이 가능하며, 선택 LOT·실패·검토 이력이 모두 S05에 표시된다. |
| 제외 | 알림, 파일 첨부, 외부 ERP 연동은 현재 범위 밖이다. |

## 릴리스 점검 순서

1. Sprint 1의 로그인 → 지시 생성 → 지시 시작을 역할 계정으로 확인한다.
2. Sprint 2의 LOT 등록 → 이상 등록 → 검사 확정을 수량 불일치 사례와 함께 확인한다.
3. Sprint 3의 관련 LOT 선택 → AI 요약 → 검토 저장과 AI 실패 이력 표시를 확인한다.
