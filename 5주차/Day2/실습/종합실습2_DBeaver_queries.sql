-- ============================================================
-- 종합실습 2: JOIN 실습 쿼리 (PostgreSQL / DBeaver)
-- 대상 DB: skala_db
-- 대상 스키마: lab
-- 실행 방법
--   1) DBeaver에서 skala_db 연결
--   2) 실행할 쿼리에 커서를 두고 Ctrl+Enter
--   3) 전체 실행 시 Alt+X
-- 조회 제한: 1~12번 LIMIT 5, 13번 LIMIT 100
-- ============================================================

SET search_path TO lab, public;


-- ============================================================
-- 1. 학생과 수강 INNER JOIN
-- 문제: 수강 기록이 존재하는 학생의 과목과 성적을 조회한다.
-- 설명: 양쪽 테이블에서 student_id가 일치하는 행만 반환한다.
-- ============================================================
SELECT s.student_id,
       s.name,
       e.course,
       e.grade
FROM lab.student s
INNER JOIN lab.enroll e
        ON e.student_id = s.student_id
ORDER BY s.student_id, e.course
LIMIT 5;


-- ============================================================
-- 2. 모든 학생 기준 LEFT JOIN
-- 문제: 모든 학생을 조회하고 수강 정보가 있으면 함께 표시한다.
-- 설명: 수강 기록이 없는 학생은 course와 grade가 NULL로 나온다.
-- ============================================================
SELECT s.student_id,
       s.name,
       e.course,
       e.grade
FROM lab.student s
LEFT JOIN lab.enroll e
       ON e.student_id = s.student_id
ORDER BY s.student_id, e.course
LIMIT 5;


-- ============================================================
-- 3. 모든 수강 기준 RIGHT JOIN
-- 문제: 모든 수강 기록을 조회하고 학생 정보가 있으면 연결한다.
-- 설명: student에 없는 고아 수강은 학생 정보가 NULL로 나온다.
--       NULLS FIRST를 사용해 고아 수강을 먼저 확인한다.
-- ============================================================
SELECT s.student_id,
       s.name,
       e.student_id AS enrolled_student_id,
       e.course,
       e.grade
FROM lab.student s
RIGHT JOIN lab.enroll e
        ON e.student_id = s.student_id
ORDER BY s.student_id NULLS FIRST,
         e.student_id,
         e.course
LIMIT 5;


-- ============================================================
-- 4. 학생과 수강 모두 포함 FULL OUTER JOIN
-- 문제: 학생과 수강 양쪽의 일치·불일치 데이터를 모두 조회한다.
-- 설명: 미수강 학생과 학생 정보가 없는 고아 수강까지 포함한다.
-- ============================================================
SELECT s.student_id,
       s.name,
       e.student_id AS enrolled_student_id,
       e.course,
       e.grade
FROM lab.student s
FULL OUTER JOIN lab.enroll e
             ON e.student_id = s.student_id
ORDER BY COALESCE(s.student_id, e.student_id),
         e.course
LIMIT 5;


-- ============================================================
-- 5. 한 번도 수강하지 않은 학생
-- 문제: 수강 기록이 하나도 없는 학생을 조회한다.
-- 설명: NOT EXISTS를 사용한 Anti-Join 패턴이다.
-- ============================================================
SELECT s.student_id,
       s.name,
       s.major,
       s.gpa
FROM lab.student s
WHERE NOT EXISTS (
    SELECT 1
    FROM lab.enroll e
    WHERE e.student_id = s.student_id
)
ORDER BY s.student_id
LIMIT 5;


-- ============================================================
-- 6. 한 과목 이상 수강한 학생
-- 문제: 수강 기록이 하나 이상 존재하는 학생을 중복 없이 조회한다.
-- 설명: EXISTS는 존재 여부만 검사하므로 DISTINCT가 필요 없다.
-- ============================================================
SELECT s.student_id,
       s.name,
       s.major,
       s.gpa
FROM lab.student s
WHERE EXISTS (
    SELECT 1
    FROM lab.enroll e
    WHERE e.student_id = s.student_id
)
ORDER BY s.student_id
LIMIT 5;


-- ============================================================
-- 7. 고객별 주문 건수와 총액
-- 문제: 모든 고객을 기준으로 주문 건수와 총 주문 금액을 집계한다.
-- 설명
--   - LEFT JOIN: 주문이 없는 고객도 포함
--   - COUNT(o.order_id): 주문 없는 고객을 0건으로 계산
--   - COALESCE: 주문 총액 NULL을 0으로 변경
-- ============================================================
SELECT c.customer_id,
       c.customer_name,
       COUNT(o.order_id) AS order_count,
       COALESCE(SUM(o.amount), 0) AS total_amount
FROM lab.customers c
LEFT JOIN lab.orders o
       ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY c.customer_id
LIMIT 5;


-- ============================================================
-- 8. 주문 총액 상위 고객
-- 문제: 주문 총액이 가장 큰 고객 5명과 금액을 조회한다.
-- 설명: 고객별 합계 계산 후 total_amount 내림차순으로 정렬한다.
--       상위 10명이 필요하면 LIMIT 5를 LIMIT 10으로 변경한다.
-- ============================================================
SELECT c.customer_id,
       c.customer_name,
       SUM(o.amount) AS total_amount
FROM lab.customers c
INNER JOIN lab.orders o
        ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_amount DESC, c.customer_id
LIMIT 5;


-- ============================================================
-- 9. 모든 직원과 매니저 이름
-- 문제: 모든 직원과 해당 직원의 직속 매니저 이름을 조회한다.
-- 설명: 같은 emp 테이블을 직원(e)과 매니저(m) 역할로 SELF JOIN한다.
--       매니저가 없는 CEO도 포함하기 위해 LEFT JOIN을 사용한다.
-- ============================================================
SELECT e.emp_id,
       e.name AS employee_name,
       m.name AS manager_name
FROM lab.emp e
LEFT JOIN lab.emp m
       ON m.emp_id = e.manager_id
ORDER BY e.emp_id
LIMIT 5;


-- ============================================================
-- 10. 모든 학생 기준 과목 분포
-- 문제: 모든 학생을 기준으로 과목별 수강 인원을 집계한다.
-- 설명: 미수강 학생의 NULL 과목은 '미수강'으로 표시한다.
--       학생 기준 LEFT JOIN이므로 고아 수강 데이터는 제외된다.
-- ============================================================
SELECT COALESCE(e.course, '미수강') AS course,
       COUNT(s.student_id) AS student_count
FROM lab.student s
LEFT JOIN lab.enroll e
       ON e.student_id = s.student_id
GROUP BY e.course
ORDER BY student_count DESC, course
LIMIT 5;


-- ============================================================
-- 11. DB 과목을 듣지 않은 학생
-- 문제: 다른 과목의 수강 여부와 관계없이 DB 과목 기록이 없는 학생을 찾는다.
-- 설명: 학생별로 course='DB'인 행이 존재하지 않는지 검사한다.
-- ============================================================
SELECT s.student_id,
       s.name,
       s.major,
       s.gpa
FROM lab.student s
WHERE NOT EXISTS (
    SELECT 1
    FROM lab.enroll e
    WHERE e.student_id = s.student_id
      AND e.course = 'DB'
)
ORDER BY s.student_id
LIMIT 5;


-- ============================================================
-- 12. 과목별 책임 매니저와 수강 인원
-- 문제
--   과목을 이름이 'Mgr_'로 시작하는 매니저에게 순서대로 배정하고,
--   과목별 수강 인원과 책임 매니저 이름을 출력한다.
-- 설명
--   1) course_owner 테이블 생성
--   2) 반복 실행을 위해 기존 매핑 제거
--   3) ROW_NUMBER와 나머지 연산으로 과목을 10명의 매니저에게 순환 배정
--   4) enroll과 집계하여 과목별 수강 인원 출력
-- 주의: 아래 3개 SQL을 순서대로 실행한다.
-- ============================================================

-- 12-1. 과목-매니저 매핑 테이블 생성
CREATE TABLE IF NOT EXISTS lab.course_owner (
    course     VARCHAR(50) PRIMARY KEY,
    manager_id INT REFERENCES lab.emp(emp_id)
);

-- 12-2. 과목을 매니저에게 순환 배정
TRUNCATE lab.course_owner;

WITH managers AS (
    SELECT emp_id,
           ROW_NUMBER() OVER (ORDER BY emp_id) AS rn,
           COUNT(*) OVER () AS cnt
    FROM lab.emp
    WHERE name LIKE 'Mgr_%'
),
courses AS (
    SELECT course,
           ROW_NUMBER() OVER (ORDER BY course) AS rn
    FROM (
        SELECT DISTINCT course
        FROM lab.enroll
    ) c
)
INSERT INTO lab.course_owner (course, manager_id)
SELECT c.course,
       m.emp_id
FROM courses c
JOIN managers m
  ON m.rn = ((c.rn - 1) % m.cnt) + 1;

-- 12-3. 과목별 수강 인원과 책임 매니저 조회
SELECT co.course,
       COUNT(e.student_id) AS student_count,
       m.name AS manager_name
FROM lab.course_owner co
JOIN lab.emp m
  ON m.emp_id = co.manager_id
LEFT JOIN lab.enroll e
       ON e.course = co.course
GROUP BY co.course, m.name
ORDER BY co.course
LIMIT 5;


-- ============================================================
-- 13. 학생별 과목 추천 후보
-- 문제: 모든 학생과 전체 과목의 조합을 생성하고 샘플 100건을 조회한다.
-- 설명
--   - CROSS JOIN으로 학생 × 과목의 모든 조합 생성
--   - DISTINCT로 중복 과목 제거
--   - 조합 수가 크므로 LIMIT 100 적용
-- ============================================================
SELECT s.student_id,
       s.name,
       c.course
FROM lab.student s
CROSS JOIN (
    SELECT DISTINCT course
    FROM lab.enroll
) c
ORDER BY s.student_id, c.course
LIMIT 100;

select
    cnt as "수강 건수",
    count(*) as "학생 수"
from (
    select
        s.student_id,
        count(e.student_id) as cnt
    from student s
    left join enroll e
        on s.student_id = e.student_id
    group by s.student_id
) t
group by cnt
order by cnt;