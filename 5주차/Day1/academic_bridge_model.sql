/*
===============================================================================
 학사관리시스템 - 축소형 Bridge Model
===============================================================================

 [범례]
 - PK        : 행을 대표하는 기본키
 - FK        : 다른 테이블의 행을 참조하는 외래키
 - IDENTITY  : PostgreSQL이 PK 값을 자동 생성하는 대리키
 - NOT NULL  : 업무 수행에 반드시 필요한 값
 - UNIQUE    : 업무상 중복되면 안 되는 값 또는 값의 조합
 - CHECK     : DB가 직접 검증할 수 있는 값의 범위와 상태
 - DEFAULT   : 입력하지 않았을 때 적용되는 최초 상태

 [설계 범위]
 - 지원 기능: 강좌 개설, 수강신청, 성적 초안 및 공개
 - 제외 기능: 학과, 선수과목, 공동교수, 출결, 수강취소
 - users 하나에서 STUDENT, PROFESSOR, ADMIN 역할을 구분한다.
 - enrollments가 학생과 개설 강좌를 연결하는 Bridge 엔티티다.

 [실행 주의]
 - 아래 DROP SCHEMA ... CASCADE는 해당 스키마의 테이블과 데이터를 삭제한다.
 - 전체 작업을 트랜잭션으로 묶어 중간 오류 시 일부 구조만 남는 것을 방지한다.
===============================================================================
*/

BEGIN;

/*
 [기존 구조 정리]
 목적: 이전 설계와 새 설계가 동시에 존재해 참조 대상이 혼동되는 것을 방지한다.
 고려: 삭제 범위를 프로젝트에서 사용한 세 스키마로 한정한다.
 CASCADE: 스키마 내부 테이블, 인덱스, FK를 의존 순서와 무관하게 함께 제거한다.
*/
DROP SCHEMA IF EXISTS global CASCADE;
DROP SCHEMA IF EXISTS prj_academic CASCADE;
DROP SCHEMA IF EXISTS academic CASCADE;

/*
 [academic 스키마]
 목적: 축소된 학사관리 기능의 테이블을 하나의 업무 경계로 묶는다.
 고려: 현재는 다른 프로젝트와 공유할 데이터가 없으므로 global을 분리하지 않는다.
*/
CREATE SCHEMA academic;

/*
 [users]
 목적: 학생, 교수, 관리자의 로그인 정보와 공통 사용자 정보를 관리한다.

 설계 근거:
 - user_id: 로그인 ID 변경과 무관한 안정적인 참조값이 필요해 IDENTITY PK를 사용한다.
 - login_id UNIQUE: 서로 다른 사용자가 같은 로그인 ID를 가질 수 없게 한다.
 - password_hash: 원문 비밀번호를 저장하지 않고 해시 결과만 저장한다.
 - role CHECK: 현재 업무에 필요한 세 역할 외의 잘못된 값 저장을 막는다.

 한계:
 - professor_id/student_id FK가 참조한 사용자의 실제 role까지 FK가 검사하지는 않는다.
 - 교수 배정과 수강신청 시 역할 검사는 애플리케이션에서 수행한다.
*/
CREATE TABLE academic.users (
    user_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    login_id varchar(50) NOT NULL UNIQUE,
    password_hash varchar(255) NOT NULL,
    name varchar(100) NOT NULL,
    role varchar(20) NOT NULL
        CHECK (role IN ('STUDENT', 'PROFESSOR', 'ADMIN'))
);

/*
 [terms]
 목적: 강좌 개설과 수강신청의 기준이 되는 학기와 신청 기간을 관리한다.

 설계 근거:
 - UNIQUE(year, semester): 같은 연도와 학기가 중복 생성되는 것을 막는다.
 - year >= 2000: 실습 시스템에서 허용할 현실적인 연도 하한을 둔다.
 - registration_start < registration_end: 종료가 시작보다 빠른 잘못된 기간을 막는다.
 - status: 기간과 별개로 관리자가 신청을 열거나 닫을 수 있게 한다.
*/
CREATE TABLE academic.terms (
    term_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    year smallint NOT NULL CHECK (year >= 2000),
    semester varchar(10) NOT NULL
        CHECK (semester IN ('SPRING', 'SUMMER', 'FALL', 'WINTER')),
    registration_start timestamptz NOT NULL,
    registration_end timestamptz NOT NULL,
    status varchar(20) NOT NULL DEFAULT 'PLANNED'
        CHECK (status IN ('PLANNED', 'OPEN', 'CLOSED')),
    UNIQUE (year, semester),
    CHECK (registration_start < registration_end)
);

/*
 [courses]
 목적: 특정 학기와 무관한 과목의 고정 정보를 관리한다.

 설계 근거:
 - course_code UNIQUE: 동일한 과목 코드가 중복되는 것을 막는다.
 - credits > 0: 0 이하의 학점이 저장되는 것을 막는다.
 - 교수, 학기, 분반은 매 개설마다 달라지므로 이 테이블에 저장하지 않는다.
*/
CREATE TABLE academic.courses (
    course_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_code varchar(20) NOT NULL UNIQUE,
    name varchar(100) NOT NULL,
    credits numeric(2,1) NOT NULL CHECK (credits > 0)
);

/*
 [course_offerings]
 목적: 과목이 특정 학기에 실제로 운영되는 분반을 관리한다.

 관계:
 - course_id    → courses: 어떤 과목의 개설인지 확인한다.
 - term_id      → terms: 어느 학기에 개설되는지 확인한다.
 - professor_id → users: 담당 교수를 연결한다.

 설계 근거:
 - 현재 요구사항은 강좌당 교수 한 명이므로 professor_id를 직접 둔다.
 - UNIQUE(term_id, course_id, section_no): 동일 학기·과목·분반 중복을 막는다.
 - capacity > 0, section_no > 0: 의미 없는 정원과 분반 번호를 막는다.
 - status: 개설 준비부터 수강신청 공개, 종료까지의 상태를 표현한다.

 한계:
 - 정원 초과는 enrollments 여러 행을 세어야 하므로 CHECK로 처리할 수 없다.
 - 수강신청 트랜잭션에서 개설 강좌를 잠그고 현재 인원을 확인해야 한다.
*/
CREATE TABLE academic.course_offerings (
    offering_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_id bigint NOT NULL REFERENCES academic.courses(course_id),
    term_id bigint NOT NULL REFERENCES academic.terms(term_id),
    professor_id bigint NOT NULL REFERENCES academic.users(user_id),
    section_no smallint NOT NULL CHECK (section_no > 0),
    capacity integer NOT NULL CHECK (capacity > 0),
    room varchar(50) NOT NULL,
    status varchar(20) NOT NULL DEFAULT 'PLANNED'
        CHECK (status IN ('PLANNED', 'OPEN', 'CLOSED', 'COMPLETED')),
    UNIQUE (term_id, course_id, section_no)
);

/*
 [enrollments - Bridge 엔티티]
 목적: 학생과 개설 강좌의 N:M 관계를 연결하고 수강 결과를 관리한다.

 관계:
 - student_id  → users: 수강을 신청한 학생을 연결한다.
 - offering_id → course_offerings: 학생이 신청한 실제 분반을 연결한다.

 설계 근거:
 - UNIQUE(student_id, offering_id): 같은 학생의 동일 분반 중복 신청을 막는다.
 - enrolled_at DEFAULT now(): 신청이 발생한 시각을 자동 기록한다.
 - 수강 한 건당 성적이 최대 하나이므로 score와 grade를 이 테이블에 포함한다.
 - 아직 성적이 없는 동안 score와 letter_grade의 NULL을 허용한다.

 성적 상태 규칙:
 - NOT_GRADED: 점수와 등급이 모두 없어야 한다.
 - DRAFT: 교수의 작성 중 상태로 부분 입력을 허용한다.
 - PUBLISHED: 학생에게 공개되므로 점수와 등급이 모두 있어야 한다.
*/
CREATE TABLE academic.enrollments (
    enrollment_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id bigint NOT NULL REFERENCES academic.users(user_id),
    offering_id bigint NOT NULL REFERENCES academic.course_offerings(offering_id),
    enrolled_at timestamptz NOT NULL DEFAULT now(),

    -- 성적 입력 전에는 NULL, 입력할 경우 0~100만 허용한다.
    score numeric(5,2) CHECK (score BETWEEN 0 AND 100),

    -- 성적 입력 전에는 NULL, 입력할 경우 지정된 등급만 허용한다.
    letter_grade varchar(2)
        CHECK (letter_grade IS NULL OR letter_grade IN
            ('A+', 'A0', 'B+', 'B0', 'C+', 'C0', 'D+', 'D0', 'F')),

    grade_status varchar(20) NOT NULL DEFAULT 'NOT_GRADED'
        CHECK (grade_status IN ('NOT_GRADED', 'DRAFT', 'PUBLISHED')),

    UNIQUE (student_id, offering_id),

    -- NOT_GRADED인데 성적값이 들어가는 모순을 방지한다.
    CHECK (
        grade_status <> 'NOT_GRADED'
        OR (score IS NULL AND letter_grade IS NULL)
    ),

    -- 공개된 성적에 점수나 등급이 빠지는 것을 방지한다.
    CHECK (
        grade_status <> 'PUBLISHED'
        OR (score IS NOT NULL AND letter_grade IS NOT NULL)
    )
);

/*
 [조회 인덱스]
 목적: 실제 업무 흐름에서 자주 사용하는 FK 및 검색 조건의 조회 비용을 줄인다.

 - professor_id: 교수가 자신의 담당 강좌를 조회할 때 사용한다.
 - term_id + status: 학생이 특정 학기의 OPEN 강좌를 조회할 때 사용한다.
 - offering_id: 강좌별 수강생 목록 및 현재 신청 인원 집계에 사용한다.

 참고: PK와 UNIQUE에는 PostgreSQL이 자동으로 인덱스를 생성하므로 중복 생성하지 않는다.
*/
CREATE INDEX idx_course_offerings_professor
    ON academic.course_offerings(professor_id);

CREATE INDEX idx_course_offerings_term_status
    ON academic.course_offerings(term_id, status);

CREATE INDEX idx_enrollments_offering
    ON academic.enrollments(offering_id);

/*
 [트랜잭션 확정]
 목적: 위의 스키마, 테이블, 인덱스가 모두 성공했을 때만 변경사항을 저장한다.
*/
COMMIT;

/*
 [실행 검증]
 목적: academic 스키마에 의도한 5개 테이블이 생성됐는지 확인한다.
 기대 결과: course_offerings, courses, enrollments, terms, users
*/
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'academic'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
