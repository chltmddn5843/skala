/*
===============================================================================
 학사관리시스템 - 샘플 데이터 및 조회 실습
===============================================================================

 [선행 조건]
 - academic_bridge_model.sql 실행 완료
 - academic 스키마와 5개 테이블 존재

 [실습 항목]
 1. PostgreSQL 접속 확인
 2. 스키마·테이블·ERD 관계 확인
 3. 테이블별 최소 10건 이상의 샘플 데이터 입력
 4. SELECT + WHERE + ORDER BY
 5. COALESCE + CASE WHEN + 날짜 함수
 6. 수강신청 Bridge 테이블 JOIN

 [주의]
 - password_hash는 데이터 구조 실습용 문자열이며 실제 로그인에 사용할 수 없다.
 - INSERT는 UNIQUE 키를 기준으로 재실행해도 중복 행이 생기지 않게 작성했다.
===============================================================================
*/

/*
-------------------------------------------------------------------------------
 1. PostgreSQL 접속 확인
 목적: 현재 연결된 DB, 사용자, 서버 주소와 버전을 확인한다.
 기대 DB: skala_db
-------------------------------------------------------------------------------
*/
SELECT
    current_database() AS database_name,
    current_user AS connected_user,
    inet_server_addr() AS server_address,
    inet_server_port() AS server_port,
    version() AS postgresql_version;

/*
-------------------------------------------------------------------------------
 2. 스키마와 테이블 생성 확인
 목적: academic 스키마와 설계한 5개 테이블이 존재하는지 확인한다.
-------------------------------------------------------------------------------
*/
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'academic'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;

/*
 [ERD 관계 확인]
 목적: FK가 어떤 자식 테이블과 부모 테이블을 연결하는지 확인한다.
 DBeaver ER Diagram과 동일한 관계를 SQL 결과로 검증한다.
*/
SELECT
    tc.table_name AS child_table,
    kcu.column_name AS child_column,
    ccu.table_name AS parent_table,
    ccu.column_name AS parent_column
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
  ON kcu.constraint_name = tc.constraint_name
 AND kcu.constraint_schema = tc.constraint_schema
JOIN information_schema.constraint_column_usage ccu
  ON ccu.constraint_name = tc.constraint_name
 AND ccu.constraint_schema = tc.constraint_schema
WHERE tc.constraint_schema = 'academic'
  AND tc.constraint_type = 'FOREIGN KEY'
ORDER BY child_table, child_column;

/*
-------------------------------------------------------------------------------
 3. 샘플 데이터 입력
 목적: 각 테이블에 최소 10건 이상을 구성해 조회와 JOIN을 실습한다.
 고려: FK 참조 순서에 따라 users/terms/courses → offerings → enrollments 순으로 입력한다.
-------------------------------------------------------------------------------
*/
BEGIN;

/*
 [users: 14건]
 - 관리자 1명, 교수 3명, 학생 10명
 - login_id 충돌 시 같은 실습 사용자의 이름과 역할을 최신 값으로 맞춘다.
*/
INSERT INTO academic.users (login_id, password_hash, name, role)
VALUES
    ('admin01',   'DEMO_ONLY_NOT_A_REAL_HASH', '관리자',   'ADMIN'),
    ('professor01','DEMO_ONLY_NOT_A_REAL_HASH', '김교수',   'PROFESSOR'),
    ('professor02','DEMO_ONLY_NOT_A_REAL_HASH', '이교수',   'PROFESSOR'),
    ('professor03','DEMO_ONLY_NOT_A_REAL_HASH', '박교수',   'PROFESSOR'),
    ('student01', 'DEMO_ONLY_NOT_A_REAL_HASH', '김민준',   'STUDENT'),
    ('student02', 'DEMO_ONLY_NOT_A_REAL_HASH', '이서연',   'STUDENT'),
    ('student03', 'DEMO_ONLY_NOT_A_REAL_HASH', '박지후',   'STUDENT'),
    ('student04', 'DEMO_ONLY_NOT_A_REAL_HASH', '최하윤',   'STUDENT'),
    ('student05', 'DEMO_ONLY_NOT_A_REAL_HASH', '정도윤',   'STUDENT'),
    ('student06', 'DEMO_ONLY_NOT_A_REAL_HASH', '강지민',   'STUDENT'),
    ('student07', 'DEMO_ONLY_NOT_A_REAL_HASH', '조현우',   'STUDENT'),
    ('student08', 'DEMO_ONLY_NOT_A_REAL_HASH', '윤서아',   'STUDENT'),
    ('student09', 'DEMO_ONLY_NOT_A_REAL_HASH', '장우진',   'STUDENT'),
    ('student10', 'DEMO_ONLY_NOT_A_REAL_HASH', '임수빈',   'STUDENT')
ON CONFLICT (login_id) DO UPDATE
SET name = EXCLUDED.name,
    role = EXCLUDED.role;

/*
 [terms: 10건]
 - 2022년부터 2026년까지 봄·가을 학기 구성
 - 2026년 가을 학기만 수강신청 OPEN 상태로 둔다.
*/
INSERT INTO academic.terms (
    year, semester, registration_start, registration_end, status
)
VALUES
    (2022, 'SPRING', '2022-02-01 09:00+09', '2022-02-07 18:00+09', 'CLOSED'),
    (2022, 'FALL',   '2022-08-01 09:00+09', '2022-08-07 18:00+09', 'CLOSED'),
    (2023, 'SPRING', '2023-02-01 09:00+09', '2023-02-07 18:00+09', 'CLOSED'),
    (2023, 'FALL',   '2023-08-01 09:00+09', '2023-08-07 18:00+09', 'CLOSED'),
    (2024, 'SPRING', '2024-02-01 09:00+09', '2024-02-07 18:00+09', 'CLOSED'),
    (2024, 'FALL',   '2024-08-01 09:00+09', '2024-08-07 18:00+09', 'CLOSED'),
    (2025, 'SPRING', '2025-02-01 09:00+09', '2025-02-07 18:00+09', 'CLOSED'),
    (2025, 'FALL',   '2025-08-01 09:00+09', '2025-08-07 18:00+09', 'CLOSED'),
    (2026, 'SPRING', '2026-02-01 09:00+09', '2026-02-07 18:00+09', 'CLOSED'),
    (2026, 'FALL',   '2026-08-01 09:00+09', '2026-08-31 18:00+09', 'OPEN')
ON CONFLICT (year, semester) DO UPDATE
SET registration_start = EXCLUDED.registration_start,
    registration_end = EXCLUDED.registration_end,
    status = EXCLUDED.status;

/*
 [courses: 10건]
 - 과목 코드는 업무상 식별값이므로 중복되지 않는다.
*/
INSERT INTO academic.courses (course_code, name, credits)
VALUES
    ('CS101', '컴퓨터개론',       3.0),
    ('CS102', '프로그래밍기초',   3.0),
    ('CS201', '자료구조',         3.0),
    ('CS202', '알고리즘',         3.0),
    ('DB101', '데이터베이스개론', 3.0),
    ('DB201', 'SQL활용',          3.0),
    ('NW101', '컴퓨터네트워크',   3.0),
    ('OS101', '운영체제',         3.0),
    ('AI101', '인공지능개론',     3.0),
    ('SE101', '소프트웨어공학',   3.0)
ON CONFLICT (course_code) DO UPDATE
SET name = EXCLUDED.name,
    credits = EXCLUDED.credits;

/*
 [course_offerings: 10건]
 - 2026년 가을 학기에 과목별 한 개 분반을 개설한다.
 - course_code와 professor login_id로 FK 값을 조회해 ID 값에 의존하지 않는다.
*/
INSERT INTO academic.course_offerings (
    course_id, term_id, professor_id, section_no, capacity, room, status
)
SELECT
    c.course_id,
    t.term_id,
    p.user_id,
    v.section_no,
    v.capacity,
    v.room,
    'OPEN'
FROM (VALUES
    ('CS101', 'professor01', 1::smallint, 30, 'A101'),
    ('CS102', 'professor02', 1::smallint, 25, 'A102'),
    ('CS201', 'professor03', 1::smallint, 30, 'B201'),
    ('CS202', 'professor01', 1::smallint, 25, 'B202'),
    ('DB101', 'professor02', 1::smallint, 35, 'C301'),
    ('DB201', 'professor03', 1::smallint, 30, 'C302'),
    ('NW101', 'professor01', 1::smallint, 30, 'D401'),
    ('OS101', 'professor02', 1::smallint, 25, 'D402'),
    ('AI101', 'professor03', 1::smallint, 40, 'E501'),
    ('SE101', 'professor01', 1::smallint, 30, 'E502')
) AS v(course_code, professor_login_id, section_no, capacity, room)
JOIN academic.courses c
  ON c.course_code = v.course_code
JOIN academic.users p
  ON p.login_id = v.professor_login_id
JOIN academic.terms t
  ON t.year = 2026
 AND t.semester = 'FALL'
ON CONFLICT (term_id, course_id, section_no) DO UPDATE
SET professor_id = EXCLUDED.professor_id,
    capacity = EXCLUDED.capacity,
    room = EXCLUDED.room,
    status = EXCLUDED.status;

/*
 [enrollments: 10건]
 - 학생과 개설 강좌를 교차 연결한다.
 - 미입력, 초안, 공개 성적을 모두 포함해 COALESCE와 CASE를 실습한다.
*/
INSERT INTO academic.enrollments (
    student_id, offering_id, score, letter_grade, grade_status
)
SELECT
    s.user_id,
    co.offering_id,
    v.score,
    v.letter_grade,
    v.grade_status
FROM (VALUES
    ('student01', 'DB101', 95.00::numeric, 'A+', 'PUBLISHED'),
    ('student02', 'DB101', 88.00::numeric, 'B+', 'PUBLISHED'),
    ('student03', 'DB101', 82.00::numeric, 'B0', 'PUBLISHED'),
    ('student04', 'DB101', 76.00::numeric, 'C+', 'PUBLISHED'),
    ('student05', 'DB101', 68.00::numeric, 'D+', 'PUBLISHED'),
    ('student06', 'CS101', 91.00::numeric, 'A0', 'DRAFT'),
    ('student07', 'CS101', 79.00::numeric, 'C+', 'DRAFT'),
    ('student08', 'CS101', NULL::numeric, NULL::varchar, 'NOT_GRADED'),
    ('student09', 'AI101', NULL::numeric, NULL::varchar, 'NOT_GRADED'),
    ('student10', 'AI101', NULL::numeric, NULL::varchar, 'NOT_GRADED')
) AS v(student_login_id, course_code, score, letter_grade, grade_status)
JOIN academic.users s
  ON s.login_id = v.student_login_id
JOIN academic.courses c
  ON c.course_code = v.course_code
JOIN academic.terms t
  ON t.year = 2026
 AND t.semester = 'FALL'
JOIN academic.course_offerings co
  ON co.course_id = c.course_id
 AND co.term_id = t.term_id
 AND co.section_no = 1
ON CONFLICT (student_id, offering_id) DO UPDATE
SET score = EXCLUDED.score,
    letter_grade = EXCLUDED.letter_grade,
    grade_status = EXCLUDED.grade_status;

COMMIT;

/*
 [입력 건수 검증]
 목적: 모든 테이블이 실습 조건인 10건 이상인지 한 번에 확인한다.
 기대 결과: users 14, terms 10, courses 10, course_offerings 10, enrollments 10
*/
SELECT 'users' AS table_name, count(*) AS row_count FROM academic.users
UNION ALL
SELECT 'terms', count(*) FROM academic.terms
UNION ALL
SELECT 'courses', count(*) FROM academic.courses
UNION ALL
SELECT 'course_offerings', count(*) FROM academic.course_offerings
UNION ALL
SELECT 'enrollments', count(*) FROM academic.enrollments
ORDER BY table_name;

/*
-------------------------------------------------------------------------------
 4. SELECT + WHERE + ORDER BY
 목적: 2026년 가을 학기에 수강신청 가능한 강좌를 과목 코드순으로 조회한다.
-------------------------------------------------------------------------------
*/
SELECT
    c.course_code,
    c.name AS course_name,
    u.name AS professor_name,
    co.section_no,
    co.capacity,
    co.room
FROM academic.course_offerings co
JOIN academic.courses c ON c.course_id = co.course_id
JOIN academic.terms t ON t.term_id = co.term_id
JOIN academic.users u ON u.user_id = co.professor_id
WHERE t.year = 2026
  AND t.semester = 'FALL'
  AND co.status = 'OPEN'
ORDER BY c.course_code, co.section_no;

/*
-------------------------------------------------------------------------------
 5. COALESCE + CASE WHEN + 날짜 함수
 목적: NULL 성적을 화면용 문구로 바꾸고 상태를 한글로 표현한다.
 - COALESCE: NULL 등급을 '미입력'으로 표시
 - CASE: 저장 상태를 사용자 친화적인 문구로 변환
 - 날짜 함수: 신청 일시와 경과 일수를 계산
-------------------------------------------------------------------------------
*/
SELECT
    s.name AS student_name,
    c.name AS course_name,
    COALESCE(e.letter_grade, '미입력') AS displayed_grade,
    CASE e.grade_status
        WHEN 'NOT_GRADED' THEN '성적 미입력'
        WHEN 'DRAFT' THEN '교수 작성 중'
        WHEN 'PUBLISHED' THEN '학생 공개 완료'
    END AS grade_status_name,
    to_char(e.enrolled_at AT TIME ZONE 'Asia/Seoul', 'YYYY-MM-DD HH24:MI')
        AS enrolled_at_kst,
    current_date - e.enrolled_at::date AS days_since_enrollment
FROM academic.enrollments e
JOIN academic.users s ON s.user_id = e.student_id
JOIN academic.course_offerings co ON co.offering_id = e.offering_id
JOIN academic.courses c ON c.course_id = co.course_id
ORDER BY e.enrolled_at, s.name;

/*
-------------------------------------------------------------------------------
 6. 수강신청 Bridge 테이블 JOIN
 목적: enrollments를 중심으로 학생·강좌·과목·학기·교수를 교차 조회한다.
-------------------------------------------------------------------------------
*/
SELECT
    e.enrollment_id,
    student.name AS student_name,
    t.year,
    t.semester,
    c.course_code,
    c.name AS course_name,
    professor.name AS professor_name,
    co.section_no,
    co.room,
    e.score,
    COALESCE(e.letter_grade, '미입력') AS letter_grade,
    e.grade_status
FROM academic.enrollments e
JOIN academic.users student
  ON student.user_id = e.student_id
JOIN academic.course_offerings co
  ON co.offering_id = e.offering_id
JOIN academic.courses c
  ON c.course_id = co.course_id
JOIN academic.terms t
  ON t.term_id = co.term_id
JOIN academic.users professor
  ON professor.user_id = co.professor_id
ORDER BY c.course_code, student.name;

/*
 [추가 실무형 조회: 강좌별 신청 현황]
 목적: LEFT JOIN으로 신청자가 없는 강좌도 포함하고 남은 정원을 계산한다.
*/
SELECT
    c.course_code,
    c.name AS course_name,
    co.capacity,
    count(e.enrollment_id) AS enrolled_count,
    co.capacity - count(e.enrollment_id) AS remaining_capacity
FROM academic.course_offerings co
JOIN academic.courses c
  ON c.course_id = co.course_id
LEFT JOIN academic.enrollments e
  ON e.offering_id = co.offering_id
GROUP BY co.offering_id, c.course_code, c.name, co.capacity
ORDER BY c.course_code;
