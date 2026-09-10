# PartFlow MES — 수정 기획안 (v2.2)

> v2.1 대비 이번 세션에서 확정한 사항만 반영한 개정판입니다. 세부 내용은 아래 companion 문서를 함께 참고하세요.

## 0. 문서 구성 (Companion 문서)

이 기획안은 아래 문서들과 함께 하나의 세트로 관리합니다.

| 문서 | 내용 |
|---|---|
| `PartFlow-개요.docx` | 프로젝트 기술서 — 배경·액터·UI흐름·화면 캡처 8종 |
| `PartFlow_요구사항정의서.md` | 기능요구사항 12건 + 추적성 매트릭스(요구사항→화면→API→DB) |
| `PartFlow_액터별_데이터흐름.md` | 액터별 입력·저장·조회 흐름, 상태 전이, 설계 이유 |
| `PartFlow_API_설계.md` | 화면·Actor별 API 호출 순서, 기능별 계약, 검증 규칙 |
| `PartFlow_스프린트계획.md` | P0/P1/P2 우선순위, Sprint 1~3 계획 |
| `PartFlow-API.yml` | OpenAPI 3.0.3 명세 (18 paths · 22 schemas) |
| `PartFlow-DB.dbml` | dbdiagram.io 호환 ERD |
| `PartFlow-swagger-ui/` | API.yml을 오프라인으로 열람하는 Swagger UI 패키지 |
| `PartFlow-wireframes-code/` | 화면 8종 HTML/CSS 원본 |

## 1. 이번 세션 확정 사항 요약

| # | 이슈 | 결정 |
|---|---|---|
| 1 | 관련 LOT 조회 조건 | **같은 품목 + 같은 설비 + 같은 생산일**(v2.1 확정, 실제 와이어프레임 근거) |
| 2 | AI 요약 실패 처리 | 실패도 이력으로 저장 (`ai_summaries.status`) |
| 3 | 검사 판정 방식 | 개별 측정값(`measurements`)을 LOT 생성 시점 규격(`inspection_specs`)과 서버가 비교해 자동 판정 |
| 4 | **관련 LOT 선택값(relatedLotIds) 저장** | **신규 결정** — `ai_summary_related_lots` 연결 테이블에 요약 생성 시점 스냅샷으로 저장. 상세 근거는 `PartFlow_액터별_데이터흐름.md` §"관련 LOT 선택과 AI 요약 근거 보존" 참고 |

이전 v2.1의 "다음 확인 필요 사항"(품목+설비+생산일 재조정안)은 이번 세션에서 최종 확정되었고, 새로 발견된 relatedLotIds 저장 이슈도 위 4번으로 해결되어 **현재 다음 확인 필요 사항은 없음**.

## 2. 액터와 요구사항

전체 12건의 기능요구사항(F01~F09 + 이상징후·관련LOT선택·조회 세분화)은 `PartFlow_요구사항정의서.md`의 REQ-FUNC-001~012로 이관되었으며, 요구사항→화면→API→DB 매핑은 그 문서의 추적성 매트릭스를 정본으로 한다. 액터 구분(생산관리자/작업자/품질담당자/외부 AI)과 F03 시작·종료 책임 분리는 기존과 동일하다.

## 3. 데이터 모델

`PartFlow-DB.dbml`이 정본이며, 이번 세션에서 `ai_summary_related_lots` 테이블이 추가되었다(§1-4 참고). 나머지 엔티티(users/products/equipment/inspection_specs/work_orders/production_lots/inspections/measurements/ai_summaries/summary_reviews)와 컬럼 설계 이유는 `PartFlow_액터별_데이터흐름.md`의 "설계 이유" 열에 정리되어 있다.

## 4. API

`PartFlow-API.yml`이 정본이며, `POST /lots/{id}/ai-summaries`에 `relatedLotIds` 요청 필드와 응답의 `relatedLotIds` 필드가 이번 세션에 추가되었다. 화면·Actor별 호출 순서는 `PartFlow_API_설계.md`를 참고한다.

## 5. 남은 작업

- `PartFlow-API.yml` / `PartFlow-DB.dbml`에 반영한 `ai_summary_related_lots`를 dbdiagram.io에서 재렌더링해 ERD 이미지·기술서 캡처를 최신화할지 결정
- 스프린트 3(AI 요약) 착수 시 `relatedLotIds` 검증 로직(후보 목록 밖 ID 거절)을 서버에 구현
