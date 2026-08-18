# PostgreSQL SQL 작성 Checkpoint (목차 24~32)

> 기준: 「스마트 데이터 이해 및 활용」 목차 24부터 32까지의 SQL 예시와 Checkpoint  
> 범위: PostgreSQL 중심. MySQL, Oracle, SQL Server 전용 문법은 제외  
> 보는 법: **하지 말 것 → 이유 → 권장 대안** 순서로 확인

## 빠른 체크리스트

- 사용자 입력을 f-string, `%`, `format()`으로 SQL 문자열에 합치지 않는다.
- 값은 psycopg 파라미터 바인딩(`%s`)을 사용한다.
- 컬럼명·정렬 방향처럼 바인딩할 수 없는 식별자는 화이트리스트로 제한한다.
- 실제로 변하는 함수를 `IMMUTABLE`로 선언하지 않는다.
- `SECURITY DEFINER` 함수는 최소한으로 사용하고 `search_path`를 고정한다.
- 대량 DML에 `FOR EACH ROW` 트리거를 남발하지 않는다.
- 트리거에서 외부 API나 장시간 작업을 실행하지 않는다.
- 애플리케이션 계정에 소유자·슈퍼유저·DDL 권한을 주지 않는다.
- 분석 쿼리에서 `SELECT *`를 피하고 필요한 컬럼만 조회한다.
- 파티션 테이블 조회 시 `WHERE`에 파티션 키를 포함한다.
- 백업 파일만 만들고 끝내지 말고 복구 가능 여부까지 검증한다.

---

## 24. Stored Procedure & 함수

### 24-1. 함수 안정성을 과장해서 선언하지 않기

**하지 말 것**

```sql
-- 현재 시간이나 테이블 데이터에 따라 결과가 변하는데 IMMUTABLE 선언
CREATE FUNCTION changing_value()
RETURNS timestamptz
LANGUAGE sql
IMMUTABLE
AS $$ SELECT now() $$;
```

**이유**

- `IMMUTABLE`은 같은 입력이면 항상 같은 결과라는 약속이다.
- PostgreSQL은 이 약속을 믿고 상수 폴딩과 함수 기반 인덱스를 적용한다.
- 잘못 선언하면 오래된 값이나 잘못된 인덱스 결과가 사용될 수 있다.

**대안**

| 등급 | 적용 기준 | 대표 용도 |
|---|---|---|
| `IMMUTABLE` | 같은 입력이면 항상 같은 결과 | 순수 계산, 인덱스 표현식 |
| `STABLE` | 한 SQL 문 안에서는 결과가 동일 | 조회·세션 상태 기반 함수 |
| `VOLATILE` | 호출마다 결과가 달라질 수 있음 | 난수, 데이터 변경 함수 |

```sql
CREATE OR REPLACE FUNCTION fn_vat(amount numeric)
RETURNS numeric
LANGUAGE sql
IMMUTABLE
AS $$ SELECT amount * 0.1 $$;
```

> 교본 정정 메모: `now()`는 교본 표와 달리 PostgreSQL에서 `STABLE`이다.

### 24-2. 함수 기반 인덱스는 쿼리 표현식과 맞추기

```sql
CREATE INDEX idx_tax ON orders ((fn_vat(total_amount)));

-- 인덱스 표현식과 같은 형태로 조회
SELECT order_id, total_amount
FROM orders
WHERE fn_vat(total_amount) = 1000;
```

**Checkpoint**

- 함수는 반드시 `IMMUTABLE`이어야 한다.
- 조회 조건과 인덱스 표현식이 일치해야 한다.
- 단순 계산은 함수 인덱스보다 원본 컬럼 인덱스와 조건 변환이 더 단순한지 먼저 확인한다.
- 인덱스 추가 후 `EXPLAIN (ANALYZE, BUFFERS)`로 실제 사용 여부를 확인한다.

### 24-3. `SECURITY DEFINER`를 기본 선택으로 사용하지 않기

**하지 말 것**

- 필요하지 않은 함수에 `SECURITY DEFINER` 적용
- 호출자가 변경할 수 있는 `search_path`에 의존
- 사용자 입력으로 동적 SQL을 만들어 소유자 권한으로 실행

**이유**

`SECURITY DEFINER` 함수는 호출자가 아니라 함수 소유자 권한으로 실행되므로 SQL Injection이나 `search_path` 하이재킹이 권한 상승으로 이어질 수 있다.

**대안**

```sql
CREATE OR REPLACE FUNCTION app.safe_function(p_id bigint)
RETURNS bigint
LANGUAGE sql
SECURITY DEFINER
SET search_path = pg_catalog, app
AS $$
    SELECT id FROM app.orders WHERE id = p_id
$$;
```

- 기본은 호출자 권한인 `SECURITY INVOKER`로 둔다.
- 꼭 필요한 경우에만 `SECURITY DEFINER`를 사용한다.
- 안전한 스키마만 포함하도록 `search_path`를 고정한다.
- 함수 소유자와 `EXECUTE` 권한을 최소화한다.

### 24-4. 대용량 데이터를 커서·반복문으로 한 행씩 처리하지 않기

**하지 말 것**

```text
결과를 커서로 읽음 → 행마다 UPDATE 반복
```

**이유**

행 단위 반복은 호출 횟수와 잠금 시간이 증가해 대량 데이터에서 느리다.

**대안**

```sql
UPDATE orders
SET status = 'DONE'
WHERE status = 'PENDING';
```

가능하면 한 번의 `INSERT ... SELECT`, `UPDATE`, `DELETE` 같은 Set-based SQL로 처리한다.

### 24-5. 여러 단계의 변경은 오류 시 전체 취소되게 만들기

주문 생성처럼 주문 헤더·상세·재고가 함께 바뀌는 작업은 중간 성공 상태를 남기면 안 된다.

```sql
SELECT stock_qty, price
INTO v_stock, v_price
FROM products
WHERE id = p_product_id
FOR UPDATE;
```

**Checkpoint**

- 재고처럼 동시에 변경되는 행은 `FOR UPDATE`로 잠근다.
- 재고 부족 등 비정상 상태는 `RAISE EXCEPTION`으로 중단한다.
- 예외 발생 시 작업 전체가 롤백되는지 실습으로 확인한다.
- 자주 바뀌는 비즈니스 로직·외부 API 연동은 앱 코드에 두고, 공통 계산·배치·데이터 밀접 작업만 DB 함수나 프로시저에 둔다.

> 실행 주의: 교본의 PostgreSQL `sp_top_customers`처럼 프로시저 안에 결과를 소비하지 않는 `SELECT`만 작성하면 호출자에게 결과 집합이 바로 반환되지 않는다. 결과 조회가 목적이면 `RETURNS TABLE` 함수 또는 명시적인 결과 전달 방식을 사용한다.

---

## 25. Trigger & 이벤트 처리

### 25-1. 대량 DML에 행 단위 트리거를 남발하지 않기

**하지 말 것**

```sql
CREATE TRIGGER sales_ai
AFTER INSERT ON sales
FOR EACH ROW EXECUTE FUNCTION trg_sales_ai();
```

위 방식 자체가 잘못은 아니지만, 대량 입력에서는 입력 행 수만큼 함수가 호출된다.

**대안: 문장 단위 트리거 + Transition Table**

```sql
CREATE OR REPLACE FUNCTION trg_sales_stmt_ai()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO audit_log(table_name, op, row_json)
    SELECT 'sales', TG_OP, to_jsonb(n)
    FROM new_table AS n;
    RETURN NULL;
END
$$;

CREATE TRIGGER sales_stmt_ai
AFTER INSERT ON sales
REFERENCING NEW TABLE AS new_table
FOR EACH STATEMENT EXECUTE FUNCTION trg_sales_stmt_ai();
```

### 25-2. 트리거에서 외부 API를 직접 호출하지 않기

**하지 말 것**

```text
트리거 → 외부 API 호출 → 응답 대기
```

**이유**

- 원본 트랜잭션이 길어진다.
- 외부 서비스 장애가 DB 트랜잭션 실패로 전파된다.
- 재시도와 중복 처리 제어가 어려워진다.

**대안**

```text
트리거 → Outbox/로그 테이블 기록 → 별도 소비자가 비동기 처리
```

간단한 알림은 `pg_notify()`로 전달하되, 실제 업무 처리는 앱 소비자가 담당한다.

### 25-3. 복잡하고 순서에 의존하는 트리거를 만들지 않기

- 트리거끼리 서로 호출하거나 실행 순서에 의존하지 않는다.
- 같은 테이블을 다시 수정하는 재귀 구조를 피한다.
- 감사·무결성처럼 모든 변경 경로에서 반드시 실행돼야 하는 짧은 로직에 사용한다.
- 복잡한 흐름 제어와 외부 시스템 연동은 애플리케이션으로 분리한다.

**핵심 원칙**

```text
트리거는 짧고 결정적으로, 외부 의존성 없이 작성한다.
```

---

## 26. Cloud DB 개요

DBaaS가 백업·패치·고가용성을 제공해도 SQL 최적화까지 대신해 주지는 않는다.

| 피해야 할 패턴 | PostgreSQL 대안 |
|---|---|
| 인덱스 컬럼에 불필요한 함수 적용 | 범위 조건 또는 함수 기반 인덱스 |
| 반복 실행되는 상관 서브쿼리 | `JOIN`, CTE, Window Function 검토 |
| 루프 안에서 N번 조회하는 N+1 | 한 번의 `JOIN` 또는 묶음 조회 |
| 매번 수행하는 대용량 집계 | Materialized View 또는 집계 테이블 |
| 피할 수 없는 전체 스캔 | 파티셔닝으로 스캔 범위 축소 |
| Primary에 읽기 부하 집중 | 읽기 전용 Replica 활용 |

**Checkpoint**

- Cloud DB에서도 스키마·인덱스·쿼리 최적화는 사용자 책임이다.
- 관리형 서비스의 제한된 확장, 파라미터, 비용(IOPS·백업·Egress)을 함께 확인한다.

---

## 27. 서버리스 & 분산 Cloud DB

### 분산 환경에서 피해야 할 설계

- 서비스별 DB를 나눈 뒤 일반 SQL처럼 Cross-service JOIN을 기대하지 않는다.
- Saga나 Outbox에서 이벤트가 정확히 한 번만 전달될 것이라고 가정하지 않는다.
- 이벤트 소비자가 같은 메시지를 두 번 처리해도 결과가 깨지지 않도록 멱등성을 보장한다.
- Event Sourcing을 쓰면서 복잡한 조회 비용과 읽기 모델을 생략하지 않는다.

```text
Database per Service → 서비스 간 직접 JOIN 불가
Outbox/이벤트 전달   → At-least-once를 전제로 중복 처리 방어
```

---

## 28. 데이터 웨어하우스 & 분석 DB

### 28-1. 분석 쿼리에서 `SELECT *` 사용하지 않기

**하지 말 것**

```sql
SELECT * FROM fact_sales;
```

**대안**

```sql
SELECT event_ts, user_id, amount
FROM fact_sales
WHERE event_ts >= DATE '2026-01-01'
  AND event_ts <  DATE '2026-02-01';
```

- 필요한 컬럼만 읽어 I/O와 전송량을 줄인다.
- 시간 파티션 테이블은 `WHERE`에 파티션 키 범위를 포함해 Partition Pruning을 유도한다.
- 날짜 범위는 종료 시점을 미포함하는 `>= 시작 AND < 다음 시작` 형태가 안전하다.

> 교본의 28장 SQL 예시는 BigQuery와 ClickHouse 전용이므로 이 문서에서는 해당 문법을 제외하고 PostgreSQL에도 적용되는 원칙만 남겼다.

---

## 29. 현재의 트렌드

### 29-1. pgvector 검색값을 SQL 문자열에 삽입하지 않기

교본의 하이브리드 검색처럼 값은 자리표시자를 사용한다.

```sql
SELECT id, 1 - (embedding <=> $1::vector) AS vec_score
FROM knowledge_base
ORDER BY embedding <=> $1::vector
LIMIT 20;
```

애플리케이션에서는 드라이버의 파라미터 바인딩을 사용한다. 사용자 입력 벡터나 검색어를 f-string으로 붙이지 않는다.

### 29-2. 벡터 인덱스와 연산자를 맞추기

```sql
CREATE INDEX ON knowledge_base
USING hnsw (embedding vector_cosine_ops);
```

**Checkpoint**

- `vector_cosine_ops`를 만들었다면 코사인 거리 연산자 `<=>`를 사용한다.
- 임베딩 컬럼 차원과 입력 벡터 차원을 일치시킨다.
- ANN 검색은 `ORDER BY 거리 LIMIT N` 형태로 후보를 제한한다.
- 키워드 검색은 `tsvector`와 GIN 인덱스를 사용한다.
- RAG 품질은 인덱스만이 아니라 Chunking, 필터, 재순위, 최신성, 출처 관리까지 포함한다.

### 29-3. TimescaleDB 보존 정책 적용 전 삭제 범위 확인하기

```sql
SELECT add_retention_policy('metrics', INTERVAL '30 days');
```

보존 기간이 지나면 데이터가 자동 삭제되므로 운영 정책·백업 요구사항을 먼저 확인한다. 원본 전체를 반복 집계하지 말고 Continuous Aggregate를 이용해 반복 비용을 줄인다.

### 29-4. GraphQL의 N+1을 방치하지 않기

GraphQL이 필요한 컬럼만 요청하더라도 연관 데이터 조회가 N+1 쿼리로 바뀔 수 있다. DataLoader, 묶음 조회, 적절한 JOIN으로 호출 수를 줄이고 RLS·멀티테넌시 권한을 함께 적용한다.

---

## 30. 보안 및 권한 관리

### 30-1. 사용자 입력으로 SQL 문자열을 만들지 않기

**절대 금지**

```python
sql = f"SELECT * FROM users WHERE name = '{user_input}'"
cur.execute(sql)
```

다음 형태도 같은 이유로 금지한다.

```python
f"... {user_id} ..."
"... {} ...".format(user_id)
"... %s ..." % user_id
```

**대안: psycopg 파라미터 바인딩**

```python
cur.execute(
    "SELECT id, name FROM users WHERE user_id = %s",
    (user_id,),
)
```

**Checkpoint**

- SQL과 값을 별도 인자로 전달한다.
- 문자열 값에도 직접 따옴표를 붙이지 않는다. 드라이버가 타입과 이스케이프를 처리한다.
- 단일 파라미터 튜플의 쉼표 `(user_id,)`를 빠뜨리지 않는다.
- 저장 프로시저·View·ORM도 내부에서 문자열을 조합하면 안전하지 않다.

### 30-2. 컬럼명과 정렬 방향은 값처럼 바인딩하지 않기

`ORDER BY`, 테이블명, 컬럼명은 일반 값 파라미터로 전달할 수 없다. 허용 목록으로 검증한다.

```python
allowed_order = {"name", "created_at"}
order = user_order if user_order in allowed_order else "created_at"
sql = f"SELECT id, name FROM items ORDER BY {order}"
cur.execute(sql)
```

값은 바인딩하고, 식별자는 화이트리스트 또는 psycopg의 안전한 SQL 조합 API만 사용한다.

### 30-3. 애플리케이션 계정에 과도한 권한을 주지 않기

**하지 말 것**

- 앱 계정에 `SUPERUSER`, 소유자 권한 또는 불필요한 DDL 권한 부여
- 사용자마다 테이블 권한을 직접 반복 부여
- 분석가·API 계정에 민감한 원본 테이블 직접 접근 허용

**대안: 역할 기반 최소 권한**

```sql
CREATE ROLE app_reader NOLOGIN;
GRANT CONNECT ON DATABASE appdb TO app_reader;
GRANT USAGE ON SCHEMA public TO app_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_reader;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO app_reader;

CREATE ROLE app_user LOGIN PASSWORD '***';
GRANT app_reader TO app_user;
```

- 시스템 계정과 스키마 소유자를 분리한다.
- 개인이 아닌 역할에 권한을 부여한다.
- 운영 애플리케이션에서 DDL 권한을 분리한다.
- 신규 테이블 권한은 `ALTER DEFAULT PRIVILEGES`로 누락을 방지한다.
- 예시의 비밀번호를 코드·Git·로그에 평문으로 저장하지 않는다.

### 30-4. View만 허용하고 원본 접근을 남겨두지 않기

```sql
GRANT SELECT ON v_employee_api TO api_user;
REVOKE ALL ON employee FROM api_user;
```

민감 컬럼을 제외한 View를 제공한 뒤 원본 테이블 권한을 반드시 회수한다.

### 30-5. RLS 세션 값을 설정하지 않은 채 조회하지 않기

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY by_customer ON orders
FOR SELECT
USING (customer_id = current_setting('app.customer_id')::int);

SELECT set_config('app.customer_id', '42', true);
```

**Checkpoint**

- 커넥션을 빌리거나 트랜잭션을 시작할 때 고객 ID를 설정한다.
- 연결 풀에서 이전 사용자의 세션 값이 재사용되지 않도록 트랜잭션 범위 설정과 초기화를 확인한다.
- RLS를 적용해도 애플리케이션의 인증·인가 검증을 생략하지 않는다.

### 30-6. 암호화 키를 SQL·로그에 직접 남기지 않기

교본의 `'mypassword'`는 문법 설명용 예시다. 실제 키는 SQL 파일, 소스 코드, 로그에 하드코딩하지 않고 Secret Manager/KMS 등으로 관리한다. 키를 잃으면 암호문과 백업을 복구하지 못할 수 있다.

---

## 31. 백업·복구 & 고가용성

### 하지 말아야 할 운영 판단

- Replica를 백업의 대체물로 보지 않는다. 잘못된 `DELETE`도 복제된다.
- `pg_dump` 하나만으로 모든 장애와 시점 복구가 가능하다고 가정하지 않는다.
- Base Backup 없이 WAL 파일만 보관하거나, WAL 없이 PITR이 된다고 생각하지 않는다.
- 백업 성공 로그만 확인하고 실제 복구 테스트를 생략하지 않는다.

### PostgreSQL 선택 기준

| 목적 | 방법 |
|---|---|
| 객체·데이터의 논리 백업 | `pg_dump` |
| 클러스터 물리 백업 | `pg_basebackup` |
| 특정 시점으로 복구 | Base Backup + 연속 WAL 아카이브 |
| 읽기 분산·장애 대응 | Streaming Replication |

**Checkpoint**

- PITR은 Base Backup과 WAL 아카이브를 함께 보관한다.
- 동기 복제는 RPO를 낮추지만 COMMIT 지연이 생길 수 있다.
- 비동기 복제는 성능이 좋지만 장애 시 일부 데이터 손실 가능성이 있다.
- 업무별 RPO와 RTO를 먼저 정한 뒤 백업·복제 방식을 선택한다.
- 정기적으로 별도 환경에 복원해 백업의 실제 사용 가능성을 검증한다.

---

## 32. 모니터링 및 운영

### 32-1. 실행 시간만 보고 원인을 단정하지 않기

쿼리가 느려지면 다음 순서로 확인한다.

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT ...;

ANALYZE target_table;
```

- 대형 테이블의 `Seq Scan` 여부
- 예상 `rows`와 `actual rows`의 차이
- `Buffers`의 캐시 히트와 디스크 읽기
- 통계가 오래됐다면 `ANALYZE` 실행
- 복제 지연은 `pg_last_xact_replay_timestamp()` 등으로 확인

> `EXPLAIN ANALYZE`는 쿼리를 실제 실행한다. `UPDATE`·`DELETE` 확인 시 테스트 환경을 사용하거나 `BEGIN`/`ROLLBACK`으로 변경을 통제한다.

### 32-2. 평균값 하나만 모니터링하지 않기

- QPS/TPS: 처리량
- Latency와 p95: 느린 요청의 꼬리 지연
- Active connection: 연결 누수·풀 상태
- CPU·메모리·스토리지: 자원 부족
- Replica lag: 복제 지연
- Slow Query: 실제 병목 SQL

교본의 예시 경고 기준은 응답 시간 500ms, CPU 80%, Replica Lag 30초, 잔여 스토리지 10%다. 실제 운영 기준은 서비스 SLO와 평상시 기준값에 맞게 조정한다.

---

## 최종 암기

```text
입력값       → 문자열 포맷 금지, 파라미터 바인딩
식별자       → 화이트리스트
함수 안정성  → 실제 변화 수준대로 선언
DEFINER 함수 → 최소 사용 + search_path 고정
대량 작업    → 커서·행 트리거보다 Set-based 처리
트리거       → 짧게, 외부 API 금지, 비동기 Outbox
권한         → 역할 기반 최소 권한, 앱 DDL 금지
분석 조회    → SELECT * 금지, 파티션 키 조건
벡터 검색    → 연산자·인덱스 일치, 입력 바인딩
백업         → 생성보다 복구 검증
모니터링     → 실행시간 + rows + Buffers + 자원 지표
```
