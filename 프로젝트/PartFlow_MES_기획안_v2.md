# PartFlow MES — 수정 기획안 (v2)

> 원본 기획안(정의서) 대비 이번 세션에서 확정한 사항만 반영한 개정판입니다. 원본에 없던 부분(관련 LOT API, AI 실패 이력, 컬럼 설계 이유)만 신규 추가로 표시했습니다.

## 0. 이번 세션 확정 사항 요약

| # | 이슈 | 결정 |
|---|---|---|
| 1 | 관련 LOT 조회 조건 | 설비 필드 도입하지 않고 **같은 품목 + 같은 날짜**로 단순화 |
| 2 | F03 요구사항 표 | 작업자(시작) / 관리자(종료)로 액터 분리 표기 |
| 3 | "조사시간" 기준 컬럼 | **검사시각(`inspections.inspected_at`)** 기준으로 확정 (생산일 `produced_at`과 별개) |
| 4 | AI 요약 실패 처리 | 실패도 이력으로 **저장** (`ai_summaries.status` ENUM 추가) |

---

## 1. 액터와 요구사항 (수정)

| ID | 요구사항 | 액터 | 입력 → 출력 | 완료 기준·예외 |
|---|---|---|---|---|
| F01 | 로그인·로그아웃 | 전체 내부 역할 | 계정·비밀번호 → 세션·역할 | 인증 실패 401, 권한 없음 403 |
| F02 | 작업지시 등록 | 생산관리자 | 품목·목표수량·예정일 → 지시번호 | 수량 양의 정수, 없는 품목 거절 |
| F03-1 | 작업 시작 | **작업자** | 지시 ID → 상태 변경 | WAITING→IN_PROGRESS만 허용, 그 외 409 |
| F03-2 | 작업 종료 | **생산관리자** | 지시 ID·종료 사유 → 상태 변경 | 생산량<목표수량이면 사유 필수(400), 그 외 409 |
| F04 | LOT 생산실적 등록 | 작업자 | 진행중 지시·LOT번호·수량·메모 → LOT | LOT번호 고유, 지시 누적목표 초과 거절 |
| F05 | 최종검사 확정 | 품질담당자 | LOT·검사수량·유형별 부적합수량·메모 → 검사기록 | 검사수량=생산수량, 중복 409 |
| F06 | 현황·LOT 이력 조회 | 전체 내부 역할 | 기간·품목·LOT번호 → 현황·이력 | - |
| F07 | AI 요약 생성 | 품질담당자 | 검사완료 LOT ID → 근거 포함 초안 | 검사 전 거절, 실패 시 이력 저장 후 재시도 안내 |
| F08 | 요약 검토본 저장 | 품질담당자 | 요약 ID·검토문 → 검토 이력 | 원문 불변, 이력 추가 |
| **F09 (신규)** | **관련 LOT 조회** | 품질담당자·전체 조회 역할 | LOT ID → 같은 품목·같은 검사일 LOT 목록 | 현재 LOT이 검사완료 상태 아니면 400 |

---

## 2. 데이터 모델 (수정 + 컬럼 설계 이유)

### 2-1. 엔티티 및 컬럼

| 엔터티 | 컬럼 | 설계 이유 |
|---|---|---|
| users | role ENUM(생산관리자/작업자/품질담당자) | 문자열 자유입력 대신 ENUM으로 제한해 권한 체크 로직을 단순화하고 오타로 인한 권한 오류를 방지 |
| work_orders | status ENUM(대기/진행/종료) | 상태 전이 규칙(F03-1/F03-2)이 명확히 3단계뿐이라 ENUM이 CHECK 제약보다 의도 표현이 명확함 |
| work_orders | close_reason (nullable) | 항상 필수가 아니라 "목표 미달 종료 시에만" 필요한 조건부 필드 → NOT NULL 대신 애플리케이션 레벨 검증으로 처리 |
| production_lots | lot_no UNIQUE | 동일 지시 내뿐 아니라 전체 시스템에서 LOT 추적 단위이므로 전역 유니크로 설계 (지시별 유니크였다면 LOT 이력 조회 시 조인 키가 애매해짐) |
| production_lots | produced_at | **대시보드 기간 필터(F06)의 기준 컬럼.** "생산이 언제 일어났는가"를 의미 |
| inspections | lot_id UNIQUE | LOT당 검사 1회 확정이라는 정책(재검사는 후속 범위)을 스키마 레벨에서 강제 |
| inspections | inspected_at | **관련 LOT 조회(F09)의 기준 컬럼.** "언제 검사했는가"이며 produced_at과 의도적으로 분리 — 같은 날 생산되어도 검사는 다른 날 이뤄질 수 있고, 관련 이슈 탐색은 검사 시점 기준이 더 실무적으로 의미 있음 |
| inspections | dimensional/visual/other_reject_qty 분리 | 대표 사유 1개만 기록한다는 정책(치수·외관 중복 시 치수 우선)이지만, 집계 계산식(Σ부적합/Σ검사수량)을 위해 유형별로 분리 저장해 두어야 향후 "치수 부적합만 필터링" 같은 조회가 가능 |
| **ai_summaries.status (신규)** | ENUM(SUCCESS/FAILED) | AI 실패도 이력으로 남기기로 했으므로, 실패 레코드와 성공 레코드를 같은 테이블에서 구분해야 함. generated_text는 FAILED일 때 NULL 허용 |

### 2-2. dbdiagram.io용 DBML

```dbml
Enum work_order_status {
  WAITING
  IN_PROGRESS
  CLOSED
}

Enum user_role {
  PRODUCTION_MANAGER
  OPERATOR
  QUALITY_INSPECTOR
}

Enum ai_summary_status {
  SUCCESS
  FAILED
}

Table users {
  id integer [pk, increment]
  login_id varchar [unique, not null]
  password_hash varchar [not null]
  name varchar
  role user_role [not null]
}

Table products {
  id integer [pk, increment]
  code varchar [unique, not null]
  name varchar
  application varchar // 자동차 / 가전
}

Table work_orders {
  id integer [pk, increment]
  order_no varchar [unique, not null]
  product_id integer [ref: > products.id]
  target_qty integer [not null]
  due_date date
  status work_order_status [not null, default: 'WAITING']
  created_by integer [ref: > users.id]
  started_by integer [ref: > users.id]
  closed_by integer [ref: > users.id]
  created_at timestamp
  started_at timestamp
  closed_at timestamp
  close_reason varchar [note: '생산량 < 목표수량일 때 필수']
}

Table production_lots {
  id integer [pk, increment]
  lot_no varchar [unique, not null]
  work_order_id integer [ref: > work_orders.id]
  produced_qty integer [not null]
  operator_id integer [ref: > users.id]
  produced_at timestamp [note: '대시보드 기간필터 기준']
  memo text
}

Table inspections {
  id integer [pk, increment]
  lot_id integer [ref: - production_lots.id, unique, not null]
  inspected_qty integer [not null]
  dimensional_reject_qty integer [not null, default: 0]
  visual_reject_qty integer [not null, default: 0]
  other_reject_qty integer [not null, default: 0]
  memo text
  inspector_id integer [ref: > users.id]
  inspected_at timestamp [note: '관련LOT 조회 기준']
}

Table ai_summaries {
  id integer [pk, increment]
  inspection_id integer [ref: > inspections.id]
  status ai_summary_status [not null]
  generated_text text [note: 'FAILED면 null 허용']
  model varchar
  requested_by integer [ref: > users.id]
  created_at timestamp
}

Table summary_reviews {
  id integer [pk, increment]
  summary_id integer [ref: > ai_summaries.id]
  reviewed_text text [not null]
  reviewer_id integer [ref: > users.id]
  reviewed_at timestamp
}
```

---

## 3. API 목록 (수정 — 신규 2건)

기존 API 목록(원본 6장)에 아래 2건 추가:

| 화면 | Method·Path | 주요 데이터·처리 |
|---|---|---|
| S05 | **GET /api/lots/{id}/related** (신규) | 현재 LOT과 같은 product_id + 같은 검사일(DATE(inspected_at))인 LOT 목록 반환. 현재 LOT 미검사 상태면 400 |
| S05 | POST /api/lots/{id}/ai-summaries (동작 수정) | 성공/실패 모두 ai_summaries에 status와 함께 저장. 재시도는 같은 엔드포인트 재호출 → 새 행 추가(이전 실패 이력은 보존) |

---

## 4. PPT 목차 (PartFlow 실제 명칭 반영)

| 목차 | PartFlow 기준 내용 |
|---|---|
| 1. 기획 배경 | Pain Point(작업지시·생산·검사 기록 분산) 및 도입 필요성(LOT 중심 통합 조회 + AI 인수인계 초안) |
| 2. 시스템 액터 정의 | **생산관리자 · 작업자 · 품질담당자** 권한 분리 (F03을 시작/종료로 분리한 표 사용) |
| 3. 전체 UI 흐름도 및 화면별 상세 설계 | 로그인(S01) → 현황(S02) → 작업지시(S03/S04) → LOT 상세·검사(S05/S06) 흐름 + mermaid 다이어그램 |
| 4. 데이터 모델 설계 | 위 2장 ERD(dbdiagram.io) + ENUM 3종(work_order_status, user_role, ai_summary_status) |
| 5. API 명세 및 Appendix | 본문엔 API 요약표, Appendix에 상세 스키마 |

---

## 5. Appendix로 분리할 내용

- 공통 에러 응답 스키마 (`code` / `message` / `fieldErrors` 예시 JSON)
- ENUM 전체 값 목록 (work_order_status, user_role, ai_summary_status, 부적합 유형 3종)
- 프로젝트 패키지/파일 구조 제안 (컨트롤러·서비스·리포지토리 계층 구조)
- 학습용 가정 및 스코프 제외 사항 요약 (원본 1장 내용 재정리)
- 대표 검증 시나리오 표 (원본 7장 정상/오류/중복/집계/AI장애/권한 케이스)
- 미확정 사항 (달력 마감일, 제출용 학번 등)

---

## 6. v2.1 업데이트 — 와이어프레임 반영 (실제 화면 근거로 재조정)

업로드된 와이어프레임(LOT 상세 화면)에서 관련 LOT 후보 선정 근거가 "같은 품목·**같은 설비**·시간 중첩"으로 표시되어 있어, v2에서 결정한 "품목+날짜(검사시각 기준)" 단순화안을 아래와 같이 재조정함.

### 6-1. production_lots 테이블 변경

```dbml
Table production_lots {
  id integer [pk, increment]
  lot_no varchar [unique, not null]
  work_order_id integer [ref: > work_orders.id]
  equipment_code varchar [note: '예: M1, M2. 별도 마스터 테이블 없이 단순 텍스트 — 설비 자동연동은 범위 밖']
  produced_qty integer [not null]
  operator_id integer [ref: > users.id]
  produced_at timestamp [note: '대시보드 기간필터 + 관련LOT 매칭 기준 컬럼(생산일)']
  memo text
  anomaly_type varchar [note: '이상징후 유형(예: 소음). nullable']
  anomaly_detected_at timestamp [note: '이상징후 발생 시각. nullable']
  anomaly_memo text [note: '이상징후 관찰 내용. nullable']
}
```

### 6-2. 관련 LOT 조회(F09) 기준 재확정

- **변경 전(v2)**: 같은 품목 + 같은 검사일(`inspected_at`)
- **변경 후(v2.1)**: 같은 품목(`work_order.product_id`) + 같은 설비(`equipment_code`) + 같은 생산일(`DATE(produced_at)`)
- "시간 중첩"(정확한 시:분 겹침)까지는 구현하지 않고 "같은 날"로 단순화 — 정밀 구현은 후속 범위

### 6-3. LOT 품질 상태(화면 표시용, 계산 필드— DB 저장 안 함)

- **확인대기**: `anomaly_type IS NOT NULL` AND 검사기록 없음
- **검사대기**: `anomaly_type IS NULL` AND 검사기록 없음
- **검사완료**: 검사기록 존재

### 6-4. API 추가

| 화면 | Method·Path | 처리 |
|---|---|---|
| S04 | POST /api/work-orders/{id}/lots/{lotId}/anomalies (신규) | type/detectedAt/memo → LOT의 anomaly 필드 갱신, 품질상태를 확인대기로 전환 |

## 7. 다음 확인 필요 사항

- **위 6-2 재조정안(품목+설비+생산일)으로 확정할지 확인 필요** — 와이어프레임 근거로 우선 반영했으나 최종 확인 전까지는 잠정안
