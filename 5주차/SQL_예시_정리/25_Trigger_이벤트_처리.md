# 25. Trigger & 이벤트 처리 - SQL 예시 모음

> 출처: `스마트 데이터 이해 및 활용` 25장, PDF 362-367·373-374쪽
> 범위: 교재의 `[SQL 예시]` 전체. 362-363쪽과 366-367쪽의 중복 예시는 한 번만 수록.

## 빠른 찾기

| 찾고 싶은 것                       | DBMS       | 바로가기                                            | 검색어                                                   |
| ---------------------------------- | ---------- | --------------------------------------------------- | -------------------------------------------------------- |
| INSERT 행마다 감사 로그 남기기     | PostgreSQL | [1](#1-postgresql-row-level-감사-로그)               | `감사 로그`, `row-level`, `TG_OP`, `NEW`         |
| 대량 INSERT를 문장 단위로 감사하기 | PostgreSQL | [2](#2-postgresql-statement-level--transition-table) | `statement-level`, `transition table`, `new_table` |
| INSERT 전에 생성 시각 기본값 넣기  | MySQL      | [3](#3-mysql-beforeafter-trigger)                    | `BEFORE INSERT`, `created_at`, `COALESCE`          |
| INSERT 후 JSON 감사 로그 남기기    | MySQL      | [3](#3-mysql-beforeafter-trigger)                    | `AFTER INSERT`, `JSON_OBJECT`, `audit_log`         |
| 여러 INSERT 행을 JSON으로 감사하기 | SQL Server | [4](#4-sql-server-after-trigger)                     | `inserted`, `FOR JSON PATH`, `SYSUTCDATETIME`      |
| INSERT 전에 생성 시각 기본값 넣기  | Oracle     | [5](#5-oracle-before-row-trigger)                    | `:NEW`, `NVL`, `SYSTIMESTAMP`                      |
| DDL 변경 이력 남기기               | PostgreSQL | [6](#6-postgresql-event-trigger로-ddl-이력-기록)     | `Event Trigger`, `ddl_history`, `ddl_command_end`  |
| INSERT를 앱에 실시간 알림          | PostgreSQL | [7](#7-postgresql-notifylisten-실시간-알림)          | `NOTIFY`, `LISTEN`, `pg_notify`, `order_channel` |

## 선택 기준

- 행마다 처리: `FOR EACH ROW`
- 대량 변경을 한 번에 처리: `FOR EACH STATEMENT` + Transition Table
- 데이터 변경 이력: DML Trigger
- 스키마 변경 이력: Event Trigger
- 앱 실시간 알림: `pg_notify()` + 앱의 `LISTEN`
- 외부 API나 오래 걸리는 작업은 Trigger에서 직접 실행하지 않고, 로그/Outbox에 적재한 뒤 비동기로 처리

## 1. PostgreSQL row-level 감사 로그

**용도:** `sales`에 행이 INSERT될 때마다 새 행 전체를 JSONB 감사 로그로 저장
**교재 위치:** PDF 362쪽(동일 예시: 366쪽)

```sql
-- 감사 로그 테이블
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name TEXT,
    op TEXT,
    row_json JSONB,
    at TIMESTAMPTZ DEFAULT now()
);

-- Row-level Trigger 함수
CREATE OR REPLACE FUNCTION trg_sales_ai() RETURNS trigger AS $$
BEGIN
    INSERT INTO audit_log(table_name, op, row_json)
    VALUES ('sales', TG_OP, to_jsonb(NEW));
    RETURN NEW;
END$$ LANGUAGE plpgsql;

CREATE TRIGGER sales_ai
AFTER INSERT ON sales
FOR EACH ROW EXECUTE FUNCTION trg_sales_ai();
```

## 2. PostgreSQL statement-level + Transition Table

**용도:** 한 INSERT 문이 추가한 모든 행을 `new_table`로 받아 감사 로그에 일괄 기록
**교재 위치:** PDF 363쪽(동일 예시: 367쪽)

```sql
-- audit_log 테이블은 1번 예시와 동일
CREATE OR REPLACE FUNCTION trg_sales_stmt_ai() RETURNS trigger AS $$
BEGIN
    INSERT INTO audit_log(table_name, op, row_json)
    SELECT 'sales', TG_OP, to_jsonb(n)
    FROM new_table AS n;
    RETURN NULL;
END$$ LANGUAGE plpgsql;

CREATE TRIGGER sales_stmt_ai
AFTER INSERT ON sales
REFERENCING NEW TABLE AS new_table
FOR EACH STATEMENT EXECUTE FUNCTION trg_sales_stmt_ai();
```

## 3. MySQL BEFORE/AFTER Trigger

**용도:** INSERT 전 `created_at` 기본값 설정 + INSERT 후 JSON 감사 로그 기록
**교재 위치:** PDF 364쪽

```sql
-- MySQL: row-level only, BEFORE/AFTER
DELIMITER //

CREATE TRIGGER sales_bi BEFORE INSERT ON sales FOR EACH ROW
BEGIN
    SET NEW.created_at = COALESCE(NEW.created_at, NOW());
END//

CREATE TRIGGER sales_ai AFTER INSERT ON sales FOR EACH ROW
BEGIN
    INSERT INTO audit_log(table_name, op, row_json)
    VALUES (
        'sales',
        'INSERT',
        JSON_OBJECT('id', NEW.id, 'amount', NEW.amount)
    );
END//

DELIMITER ;
```

> MySQL Trigger에서 Trigger를 발생시킨 같은 테이블(`sales`)을 다시 수정하면 오류 1442가 발생한다.

## 4. SQL Server AFTER Trigger

**용도:** 한 INSERT 문으로 들어온 모든 행을 `inserted` 가상 테이블에서 읽어 JSON 감사 로그로 저장
**교재 위치:** PDF 365쪽

```sql
-- SQL Server: AFTER/INSTEAD OF, inserted/deleted 가상 테이블
CREATE TRIGGER dbo.trg_sales_ai ON dbo.Sales
AFTER INSERT AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dbo.AuditLog(table_name, op, row_json, at)
    SELECT
        'Sales',
        'INSERT',
        (SELECT * FROM inserted FOR JSON PATH),
        SYSUTCDATETIME();
END;
```

## 5. Oracle BEFORE row Trigger

**용도:** INSERT 전에 `created_at`이 NULL이면 현재 시각 설정
**교재 위치:** PDF 365쪽

```sql
-- Oracle: BEFORE row 기본값
CREATE OR REPLACE TRIGGER sales_bi
BEFORE INSERT ON sales
FOR EACH ROW
BEGIN
    :NEW.created_at := NVL(:NEW.created_at, SYSTIMESTAMP);
END;
/
```

> 교재는 Mutating Table 회피 수단으로 Compound Trigger도 언급하지만, 이 페이지의 SQL은 기본값 설정 예시만 제공한다.

## 6. PostgreSQL Event Trigger로 DDL 이력 기록

**용도:** DDL 명령이 끝날 때 변경된 객체와 명령 종류를 자동 기록
**교재 위치:** PDF 373쪽

```sql
-- DDL 변경 이력 자동 기록
CREATE TABLE ddl_history (
    id BIGSERIAL PRIMARY KEY,
    event_tag TEXT,
    object TEXT,
    executed_by TEXT DEFAULT current_user,
    at TIMESTAMPTZ DEFAULT now()
);

CREATE OR REPLACE FUNCTION fn_ddl_logger() RETURNS event_trigger AS $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN SELECT * FROM pg_event_trigger_ddl_commands() LOOP
        INSERT INTO ddl_history(event_tag, object)
        VALUES (r.command_tag, r.object_identity);
    END LOOP;
END$$ LANGUAGE plpgsql;

CREATE EVENT TRIGGER ddl_logger ON ddl_command_end
EXECUTE FUNCTION fn_ddl_logger();
```

## 7. PostgreSQL NOTIFY/LISTEN 실시간 알림

**용도:** 주문 INSERT 시 앱이 구독한 채널로 새 주문 JSON을 즉시 알림
**교재 위치:** PDF 374쪽

```sql
-- Trigger에서 변경 발생 시 앱에 즉시 알림
CREATE OR REPLACE FUNCTION fn_notify_order() RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('order_channel', row_to_json(NEW)::TEXT);
    RETURN NEW;
END$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_order_notify
AFTER INSERT ON orders
FOR EACH ROW EXECUTE FUNCTION fn_notify_order();
```

교재의 Python 수신 흐름:

```python
# psycopg2 개념 예시
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur.execute("LISTEN order_channel")

while True:
    select.select([conn], [], [])
    conn.poll()
    print(conn.notifies.pop())
```

## DBMS별 핵심 차이

| DBMS       | 기본 실행 범위  | 변경 행 참조                       | 이 장에서 다룬 특징                   |
| ---------- | --------------- | ---------------------------------- | ------------------------------------- |
| PostgreSQL | Row / Statement | `OLD`, `NEW`, Transition Table | Event Trigger,`LISTEN/NOTIFY`       |
| MySQL      | Row             | `OLD`, `NEW`                   | 같은 테이블 재수정 금지(오류 1442)    |
| MariaDB    | Row             | `OLD`, `NEW`                   | 실행 순서`FOLLOWS/PRECEDES`         |
| SQL Server | Statement       | `inserted`, `deleted`          | 다중 행을 집합으로 처리               |
| Oracle     | Row / Statement | `:OLD`, `:NEW`                 | Mutating Table 주의, Compound Trigger |

## 채팅에서 이렇게 찾기

- “PostgreSQL에서 대량 INSERT 감사 로그 쿼리 찾아줘”
- “created_at 자동 입력하는 MySQL Trigger 보여줘”
- “DDL 변경 이력 남기는 예시가 어디 있지?”
- “주문 INSERT를 앱에 실시간 알리는 SQL 찾아줘”
