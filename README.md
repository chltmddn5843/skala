# SKALA 학습 기록

SKALA 과정에서 학습한 이론, 실습 코드, 프로젝트와 인사이트를 주차별로 정리한 저장소입니다.

## 전체 학습 요약

| 주차 | 주제 | 핵심 학습 내용 | 주요 결과물 |
| --- | --- | --- | --- |
| 1주차 | Git · Web 기초 | Git 저장소와 기본 명령어, HTML 문서 구조, CSS 선택자·레이아웃, JavaScript 이벤트와 DOM 조작 | Git 실습, HTML/CSS/JS 예제 페이지 |
| 2주차 | 데이터 분석 · LLM | 기초 통계와 데이터 분석, LSTM과 Transformer, Attention, 프롬프트·컨텍스트 설계, AI Agent | 분석 노트북, CrewAI 실습, STEP GUARD 대시보드 |
| 3주차 | Java · Spring Boot | 객체지향과 SOLID, DI·IoC, Spring MVC, REST API, 설정·Profile, JPA·트랜잭션, 예외 처리, AOP, Actuator | 메뉴 추천, 주식 거래, 쇼핑 API 프로젝트 |
| 4주차 | Python · ML/DL | Python 자료구조·파일 I/O·예외 처리, Pandas EDA, Feature Engineering, Pydantic 검증, 머신러닝·딥러닝 모델 | 데이터 파이프라인, NYC 택시 수익 최적화 프로젝트 |
| 5주차 | Database · SQL | 관계형 모델링과 정규화, ERD, 트랜잭션·ACID, JOIN·집계·윈도 함수, 인덱스, 실행 계획과 쿼리 튜닝 | 학사 관리 DB 설계, PostgreSQL 쿼리·튜닝 보고서 |

## 주차별 학습 내용

### 1주차 — Git과 프론트엔드 기초

- Git의 저장소 생성, 변경 추적, 커밋과 브랜치 등 버전 관리 흐름을 실습했습니다.
- HTML로 문서 구조를 만들고 CSS로 선택자, 박스 모델, 배치와 반응형 표현을 적용했습니다.
- JavaScript로 이벤트를 처리하고 DOM을 변경하는 동적 페이지를 구현했습니다.
- Emmet을 이용해 반복되는 HTML 구조를 빠르게 작성하는 방법을 익혔습니다.

디렉터리: [`git사용`](./1주차/git사용), [`html_css`](./1주차/html_css)

### 2주차 — 데이터 분석과 LLM 활용

- 기술 통계와 데이터 전처리·시각화를 통해 데이터에서 패턴과 근거를 찾는 과정을 실습했습니다.
- RNN/LSTM의 순차 처리 한계와 Transformer의 Self-Attention, 병렬 처리, Encoder·Decoder 구조를 비교했습니다.
- 토큰화 → 임베딩 → 위치 정보 → Attention → 출력으로 이어지는 LLM 처리 흐름을 학습했습니다.
- CoT, Self-Consistency, ReAct, Memory & Compaction, 단계별 하네스 등 프롬프트 설계 기법과 적용 조건을 정리했습니다.
- 목표, 역할, 도구, 작업과 출력 형식을 정의하는 AI Agent를 CrewAI로 구성했습니다.
- 시설 안전 점검 데이터를 여러 Agent가 분석해 계획을 제안하는 **STEP GUARD** 대시보드를 구현했습니다.

디렉터리: [`데이터 분석 및 기초통계`](./2주차/데이터%20분석%20및%20기초통계), [`LLM모델이해`](./2주차/LLM모델이해), [`Prompt 설계 및 Context Engineering`](./2주차/Prompt_설계및Context_Engineering), [`주간실습`](./2주차/주간실습)

### 3주차 — Java와 Spring Boot 백엔드

- 클래스, 객체, 생성자, 접근 제어, 상속과 다형성을 실습하고 객체지향의 네 가지 특징과 SOLID 원칙을 학습했습니다.
- Spring의 DI·IoC와 계층형 구조(Controller–Service–Repository)를 통해 역할과 구현을 분리했습니다.
- Spring MVC 요청 흐름, REST API, 파라미터 바인딩, DTO와 입력 검증을 학습했습니다.
- 환경별 Configuration·Profile, 컴포넌트 스캔과 자동 설정을 적용했습니다.
- JDBC와 JPA를 비교하고 JpaRepository, Entity 관계, 영속성 및 `@Transactional`을 실습했습니다.
- `@ControllerAdvice` 예외 처리, AOP 공통 관심사 분리, Actuator 엔드포인트와 메트릭을 다뤘습니다.
- 메뉴 추천, 주식 거래, 쇼핑 도메인을 대상으로 CRUD와 API 설계를 반복 실습했습니다.

디렉터리: [`day1_JAVA`](./3주차/day1_JAVA), [`day2_JAVA`](./3주차/day2_JAVA), [`day3_JAVA`](./3주차/day3_JAVA), [`day4_JAVA`](./3주차/day4_JAVA), [`day5_JAVA`](./3주차/day5_JAVA)

### 4주차 — Python 데이터 분석과 머신러닝

- Python 자료구조, 제어문, 컴프리헨션, 파일 I/O, 예외 처리, 로깅과 메모리 관리 기초를 학습했습니다.
- Pandas로 데이터를 정제·집계하고 EDA와 시각화로 분석 가설을 검토했습니다.
- 결측치·이상치 처리, 인코딩, 스케일링과 파생 변수 생성 등 Feature Engineering 흐름을 실습했습니다.
- Pydantic으로 입력 데이터를 검증하고 정상 데이터와 오류를 분리하는 파이프라인을 구현했습니다.
- 비동기 API 수집, 외부 API Mock 테스트와 CSV·Parquet 저장 방식을 실습했습니다.
- 회귀·분류·군집화와 CNN, LSTM, Autoencoder, ResNet, BERT 등 ML/DL 구조를 학습했습니다.
- **NYC 택시 수익 최적화** 프로젝트에서 전처리 → EDA → K-Means 장거리 라벨링 → 시간순 검증 → 사전 분류 모델 학습의 전체 분석 파이프라인을 구성했습니다.

디렉터리: [`학습자료`](./4주차/학습자료), [`Day3`](./4주차/Day3), [`Day4`](./4주차/Day4), [`실습자료`](./4주차/실습자료), [`실습자료2`](./4주차/실습자료2), [`실습자료3`](./4주차/실습자료3), [`실습자료4`](./4주차/실습자료4), [`nyc-taxi-earnings-optimizer`](./4주차/nyc-taxi-earnings-optimizer)

### 5주차 — 데이터베이스 설계와 SQL 최적화

- DBMS 선택 기준, 관계형 데이터 모델, 키와 제약조건, 정규화와 ERD 설계 과정을 학습했습니다.
- 트랜잭션과 ACID, WAL, Lock, 스키마와 멀티 테넌시 전략을 정리했습니다.
- 학사 관리 시스템의 요구사항에서 엔티티를 도출하고 다대다 관계를 Bridge Table로 설계했습니다.
- `GROUP BY`, `HAVING`, `ROLLUP`, `CUBE`, `FILTER`와 Window Function으로 집계·분석 쿼리를 작성했습니다.
- INNER/OUTER/SELF/Anti JOIN, 서브쿼리, CTE, View와 Materialized View의 용도를 비교했습니다.
- Nested Loop, Sort-Merge, Hash Join 알고리즘과 OFFSET·Keyset 페이지네이션의 차이를 학습했습니다.
- 인덱스 선택도와 복합 인덱스, `EXPLAIN ANALYZE`, 파티셔닝, 통계 갱신 및 SQL 안티패턴을 이용해 느린 쿼리를 진단·개선했습니다.

디렉터리: [`Day1`](./5주차/Day1), [`Day2`](./5주차/Day2), [`Day3`](./5주차/Day3), [`학습자료`](./5주차/학습자료)

## 핵심 인사이트

- 기술보다 먼저 해결할 업무 문제와 측정 가능한 성공 기준을 정의합니다.
- AI·ML은 단순 규칙으로 해결하기 어려운지 확인한 뒤, 목적과 비용에 맞는 모델을 선택합니다.
- 데이터 수집 → 분석·학습 → 평가 → 개선으로 이어지는 반복 가능한 흐름을 설계합니다.
- 모델 성능뿐 아니라 운영 안정성, 비용, 설명 가능성과 비즈니스 효과를 함께 검증합니다.
- 프로젝트는 **문제 정의 → 가설과 시도 → 결과 근거 → 개선 방향**의 순서로 기록합니다.

관련 기록: [`교육 인사이트 및 실행 계획`](./기타/교육인사이트/전체인사이트.md), [`트러블슈팅`](./기타/학습자료/트러블슈팅.md)
