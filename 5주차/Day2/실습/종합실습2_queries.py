#########
# 작성 일자 : 2026-08-12
# 작성자 : 최승우
# 작성 목적 : 종합실습 2 쿼리 실행


# 항목 
# 1. INNER JOIN
# 2. LEFT JOIN
# 3. RIGHT JOIN
# 4. FULL OUTER JOIN
# 5. NOT EXISTS
# 6. EXISTS
# 7. 고객별 주문 집계
# 8. 주문 총액 상위 5명
# 9. SELF JOIN
# 10. 과목 분포
# 11. DB 미수강 학생
# 12. 과목별 책임 매니저
# 13. 학생별 과목 추천 후보
# 14. 학생 + 소속 학과명 조회 (학과는 student.major 컬럼에 저장)
# 15. 평균 GPA 보다 높은 학생 (WHERE 서브쿼리)
# 16. 자신의 학과 평균 GPA보다 높은 학생 ( Correlated subquery )
# 17. 수강(enroll) 기록이 있는 학생만
# 18. 한 번도 수강하지 않은 학생
# 19. HR 학과 학생 일부와의 비교 데모
# 20. CS 학과 학생 또는 DB 과목을 수강한 학생 목록
# 21. 학과별 GPA 구간 인원·소계·총계
# 22. 재귀 CTE 조직 경로·깊이와 직속 부하 수
# 23. 학과별 GPA 상위 3명 (서브쿼리·CTE)
# 24. LAG를 이용한 이전 과목 대비 성적 변화
# 25. 주문 누적합·이동평균·50% 도달 주문

#########



import argparse
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path
import sys
from config import connect


class Tee:
    """출력을 터미널과 로그 파일에 동시에 기록한다."""

    def __init__(self, *files):
        self.files = files

    def write(self, text):
        for file in self.files:
            file.write(text)

    def flush(self):
        for file in self.files:
            file.flush()


def print_table(columns, rows):
    """쿼리 결과를 열 너비가 맞는 표로 출력한다."""
    values = [["NULL" if value is None else str(value) for value in row] for row in rows]
    widths = [
        max([len(column), *(len(row[index]) for row in values)])
        for index, column in enumerate(columns)
    ]
    line = "+-" + "-+-".join("-" * width for width in widths) + "-+"
    print(line)
    print("| " + " | ".join(column.ljust(width) for column, width in zip(columns, widths)) + " |")
    print(line)
    for row in values:
        print("| " + " | ".join(value.ljust(width) for value, width in zip(row, widths)) + " |")
    print(line)



def show(title, query):
    """쿼리를 실행하고 컬럼명과 결과를 터미널에 출력한다."""
    with connect() as connection:
        cursor = connection.execute(query)
        print(f"\n[{title}]")
        print_table([column.name for column in cursor.description], cursor.fetchall())


def q01_inner_join():
    """1. 수강 기록이 실제로 존재하는 학생의 과목과 성적을 조회한다."""
    show("1. INNER JOIN", """
        SELECT s.student_id, s.name, e.course, e.grade
        FROM lab.student s
        INNER JOIN lab.enroll e ON e.student_id = s.student_id
        ORDER BY s.student_id, e.course
        LIMIT 5
    """)


def q02_left_join():
    """2. 모든 학생을 보존하고 수강이 없으면 과목과 성적을 NULL로 표시한다."""
    show("2. LEFT JOIN", """
        SELECT s.student_id, s.name, e.course, e.grade
        FROM lab.student s
        LEFT JOIN lab.enroll e ON e.student_id = s.student_id
        ORDER BY s.student_id, e.course
        LIMIT 5
    """)


def q03_right_join():
    """3. 모든 수강 기록을 보존하고 학생이 없으면 학생 정보를 NULL로 표시한다."""
    show("3. RIGHT JOIN", """
        SELECT s.student_id, s.name,
               e.student_id AS enrolled_student_id, e.course, e.grade
        FROM lab.student s
        RIGHT JOIN lab.enroll e ON e.student_id = s.student_id
        ORDER BY s.student_id NULLS FIRST, e.student_id, e.course
        LIMIT 5
    """)


def q04_full_outer_join():
    """4. 학생과 수강 양쪽의 미매칭 행까지 모두 조회한다."""
    show("4. FULL OUTER JOIN", """
        SELECT s.student_id, s.name,
               e.student_id AS enrolled_student_id, e.course, e.grade
        FROM lab.student s
        FULL OUTER JOIN lab.enroll e ON e.student_id = s.student_id
        ORDER BY COALESCE(s.student_id, e.student_id), e.course
        LIMIT 5
    """)


def q05_students_without_enrollment():
    """5. NOT EXISTS로 한 번도 수강하지 않은 학생을 찾는다."""
    show("5. 미수강 학생", """
        SELECT s.student_id, s.name, s.major, s.gpa
        FROM lab.student s
        WHERE NOT EXISTS (
          SELECT 1 FROM lab.enroll e WHERE e.student_id = s.student_id
        )
        ORDER BY s.student_id
        LIMIT 5
    """)


def q06_students_with_enrollment():
    """6. EXISTS로 한 과목 이상 수강한 학생을 중복 없이 찾는다."""
    show("6. 수강 학생", """
        SELECT s.student_id, s.name, s.major, s.gpa
        FROM lab.student s
        WHERE EXISTS (
          SELECT 1 FROM lab.enroll e WHERE e.student_id = s.student_id
        )
        ORDER BY s.student_id
        LIMIT 5
    """)


def q07_customer_order_summary():
    """7. 고객별 주문 건수와 총 주문 금액을 집계한다."""
    show("7. 고객별 주문 집계", """
        SELECT c.customer_id, c.customer_name,
               COUNT(o.order_id) AS order_count,
               COALESCE(SUM(o.amount), 0) AS total_amount
        FROM lab.customers c
        LEFT JOIN lab.orders o ON o.customer_id = c.customer_id
        GROUP BY c.customer_id, c.customer_name
        ORDER BY c.customer_id
        LIMIT 5
    """)


def q08_top_customers():
    """8. 주문 총액이 가장 큰 고객 5명과 금액을 조회한다."""
    show("8. 주문 총액 상위 10명", """
        SELECT c.customer_id, c.customer_name, SUM(o.amount) AS total_amount
        FROM lab.customers c
        INNER JOIN lab.orders o ON o.customer_id = c.customer_id
        GROUP BY c.customer_id, c.customer_name
        ORDER BY total_amount DESC, c.customer_id
        LIMIT 10
    """)


def q09_employee_manager():
    """9. SELF JOIN으로 모든 직원과 직속 매니저 이름을 조회한다."""
    show("9. 직원과 매니저", """
        SELECT e.emp_id, e.name AS employee_name, m.name AS manager_name
        FROM lab.emp e
        LEFT JOIN lab.emp m ON m.emp_id = e.manager_id
        ORDER BY e.emp_id
        LIMIT 5
    """)


def q10_course_distribution():
    """10. 모든 학생을 기준으로 과목별 수강 인원을 집계한다."""
    show("10. 과목 분포", """
        SELECT COALESCE(e.course, '미수강') AS course,
               COUNT(s.student_id) AS student_count
        FROM lab.student s
        LEFT JOIN lab.enroll e ON e.student_id = s.student_id
        GROUP BY e.course
        ORDER BY student_count DESC, course
        LIMIT 5
    """)


def q11_students_without_db():
    """11. DB 과목 수강 기록이 없는 모든 학생을 NOT EXISTS로 찾는다."""
    show("11. DB 미수강 학생", """
        SELECT s.student_id, s.name, s.major, s.gpa
        FROM lab.student s
        WHERE NOT EXISTS (
          SELECT 1
          FROM lab.enroll e
          WHERE e.student_id = s.student_id AND e.course = 'DB'
        )
        ORDER BY s.student_id
        LIMIT 5
    """)


def q12_course_owner_report():
    """12. 과목을 매니저에게 순서대로 배정하고 과목별 인원과 책임자를 출력한다."""
    with connect() as connection:
        # 반복 실행할 수 있도록 매핑 테이블을 비운 뒤 다시 채운다.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS lab.course_owner (
              course VARCHAR(50) PRIMARY KEY,
              manager_id INT REFERENCES lab.emp(emp_id)
            );
            TRUNCATE lab.course_owner;
            WITH managers AS (
              SELECT emp_id, ROW_NUMBER() OVER (ORDER BY emp_id) AS rn,
                     COUNT(*) OVER () AS cnt
              FROM lab.emp
              WHERE name LIKE 'Mgr_%'
            ), courses AS (
              SELECT course, ROW_NUMBER() OVER (ORDER BY course) AS rn
              FROM (SELECT DISTINCT course FROM lab.enroll) c
            )
            INSERT INTO lab.course_owner (course, manager_id)
            SELECT c.course, m.emp_id
            FROM courses c
            JOIN managers m ON m.rn = ((c.rn - 1) % m.cnt) + 1;
        """)
        cursor = connection.execute("""
            SELECT co.course, COUNT(e.student_id) AS student_count,
                   m.name AS manager_name
            FROM lab.course_owner co
            JOIN lab.emp m ON m.emp_id = co.manager_id
            LEFT JOIN lab.enroll e ON e.course = co.course
            GROUP BY co.course, m.name
            ORDER BY co.course
            LIMIT 5
        """)
        print("\n[12. 과목별 책임 매니저]")
        print_table([column.name for column in cursor.description], cursor.fetchall())


def q13_student_course_candidates():
    """13. 학생과 전체 과목의 CROSS JOIN으로 추천 후보 조합 100개를 만든다."""
    show("13. 학생별 과목 추천 후보", """
        SELECT s.student_id, s.name, c.course
        FROM lab.student s
        CROSS JOIN (SELECT DISTINCT course FROM lab.enroll) c
        ORDER BY s.student_id, c.course
        LIMIT 100
    """)

def q14_student_department():
    """14. 스칼라 서브쿼리 (SELECT 절) 사용 학생 + 소속 학과명 붙이기"""
    show("14. 학생 + 학과명", """
        SELECT s.student_id, s.name,
               (
                   SELECT s2.major
                   FROM lab.student s2
                   WHERE s2.student_id = s.student_id
               ) AS department_name,
               s.gpa
        FROM lab.student s
        ORDER BY s.student_id
        LIMIT 5
    """)

def q15_students_above_average_gpa():
    """15. 평균 GPA 보다 높은 학생 (WHERE 서브쿼리)"""
    show("15. 평균 GPA 보다 높은 학생", """
        SELECT s.student_id, s.name, s.major, s.gpa
        FROM lab.student s
        WHERE s.gpa > (SELECT AVG(gpa) FROM lab.student)
        ORDER BY s.student_id
        LIMIT 5
    """)
def q16_students_above_department_average_gpa():
    """16. 자신의 학과 평균 GPA보다 높은 학생 ( Correlated subquery )"""
    show("16. 자신의 학과 평균 GPA보다 높은 학생", """
        SELECT s.student_id, s.name, s.major, s.gpa
        FROM lab.student s
        WHERE s.gpa > (
            SELECT AVG(s2.gpa)
            FROM lab.student s2
            WHERE s2.major = s.major
        )
        ORDER BY s.student_id
        LIMIT 5
    """)

def q17_students_with_enrollment():
    """17. 수강(enroll) 기록이 있는 학생만"""
    show("17. 수강 기록이 있는 학생", """
        SELECT s.student_id, s.name, s.major, s.gpa
        FROM lab.student s
        WHERE EXISTS (
            SELECT 1
            FROM lab.enroll e
            WHERE e.student_id = s.student_id
        )
        ORDER BY s.student_id
        LIMIT 5
    """)

def q18_students_without_enrollment():
    """18. 한 번도 수강하지 않은 학생"""
    show("18. 한 번도 수강하지 않은 학생", """
        SELECT s.student_id, s.name, s.major, s.gpa
        FROM lab.student s
        WHERE NOT EXISTS (
            SELECT 1
            FROM lab.enroll e
            WHERE e.student_id = s.student_id
        )
        ORDER BY s.student_id
        LIMIT 5
    """)


def q19_hr_students_demo():
    """19. HR 학생과 GPA가 비슷한 타 전공 학생 비교"""
    show("19. HR 학생과 타 전공 학생 GPA 비교", """
        SELECT a.name AS "HR_학생",
               a.gpa AS "HR_GPA",
               b.name AS "비교_학생",
               b.gpa AS "비교_GPA",
               b.major AS "전공"
        FROM lab.student a
        JOIN lab.student b
          ON ABS(a.gpa - b.gpa) < 0.1
         AND b.major <> 'HR'
        WHERE a.major = 'HR'
          AND a.student_id IN (981, 985, 990)
        ORDER BY "HR_학생" ASC, "비교_GPA" DESC
    """)

def q20_cs_or_db_students():
    """20. CS 학과 학생 또는 DB 과목을 수강한 학생 목록"""
    show("20. CS 학과 학생 또는 DB 과목 수강 학생", """
        SELECT DISTINCT s.student_id, s.name, s.major, s.gpa
        FROM lab.student s
        LEFT JOIN lab.enroll e ON e.student_id = s.student_id
        WHERE s.major = 'CS' OR e.course = 'DB'
        ORDER BY s.student_id
        LIMIT 5
    """)


def q21_major_gpa_rollup():
    """21. 학과별·GPA 구간별 인원과 학과 소계·전체 총계를 조회한다."""
    show("21. 학과별 GPA 구간 인원·소계·총계", """
        SELECT
            CASE WHEN GROUPING(major) = 1 THEN '전체' ELSE major END AS major,
            CASE WHEN GROUPING(gpa_tier) = 1 THEN '소계' ELSE gpa_tier END AS gpa_tier,
            COUNT(*) AS student_count
        FROM (
            SELECT major,
                   CASE
                       WHEN gpa < 3.0 THEN '3.0 미만'
                       WHEN gpa <= 3.5 THEN '3.0~3.5'
                       ELSE '3.5 초과'
                   END AS gpa_tier
            FROM lab.student
        ) classified
        GROUP BY ROLLUP(major, gpa_tier)
        ORDER BY GROUPING(major), major,
                 GROUPING(gpa_tier), gpa_tier
    """)


def q22_employee_hierarchy():
    """22. 재귀 CTE로 조직 경로·깊이를 구하고 매니저별 직속 직원 수를 집계한다."""
    show("22-1. 직원 계층 경로와 깊이", """
        WITH RECURSIVE organization AS (
            SELECT emp_id, name, manager_id,
                   0 AS depth,
                   name::TEXT AS path
            FROM lab.emp
            WHERE manager_id IS NULL

            UNION ALL

            SELECT e.emp_id, e.name, e.manager_id,
                   o.depth + 1,
                   o.path || ' > ' || e.name
            FROM lab.emp e
            JOIN organization o ON o.emp_id = e.manager_id
        )
        SELECT emp_id, name, manager_id, depth, path
        FROM organization
        ORDER BY depth, emp_id
        LIMIT 5
    """)
    show("22-2. 매니저별 직속 부하 직원 수", """
        SELECT m.emp_id,
               m.name AS manager_name,
               COUNT(e.emp_id) AS direct_reports
        FROM lab.emp m
        LEFT JOIN lab.emp e ON e.manager_id = m.emp_id
        WHERE m.name LIKE 'Mgr_%'
        GROUP BY m.emp_id, m.name
        ORDER BY m.emp_id
        LIMIT 5
    """)


def q23_top_three_per_major():
    """23. Window Function으로 학과별 GPA 상위 3명을 서브쿼리와 CTE 방식으로 조회한다."""
    show("23-1. 학과별 GPA 상위 3명 - 서브쿼리", """
        SELECT student_id, name, major, gpa,
               row_num, rank_num, dense_rank_num, total_in_major
        FROM (
            SELECT s.*,
                   ROW_NUMBER() OVER (
                       PARTITION BY major ORDER BY gpa DESC, student_id
                   ) AS row_num,
                   RANK() OVER (
                       PARTITION BY major ORDER BY gpa DESC
                   ) AS rank_num,
                   DENSE_RANK() OVER (
                       PARTITION BY major ORDER BY gpa DESC
                   ) AS dense_rank_num,
                   COUNT(*) OVER (PARTITION BY major) AS total_in_major
            FROM lab.student s
        ) ranked
        WHERE row_num <= 3
        ORDER BY major, row_num
    """)
    show("23-2. 학과별 GPA 상위 3명 - CTE", """
        WITH ranked AS (
            SELECT s.*,
                   ROW_NUMBER() OVER (
                       PARTITION BY major ORDER BY gpa DESC, student_id
                   ) AS row_num,
                   RANK() OVER (
                       PARTITION BY major ORDER BY gpa DESC
                   ) AS rank_num,
                   DENSE_RANK() OVER (
                       PARTITION BY major ORDER BY gpa DESC
                   ) AS dense_rank_num,
                   COUNT(*) OVER (PARTITION BY major) AS total_in_major
            FROM lab.student s
        )
        SELECT student_id, name, major, gpa,
               row_num, rank_num, dense_rank_num, total_in_major
        FROM ranked
        WHERE row_num <= 3
        ORDER BY major, row_num
    """)


def q24_grade_change_with_lag():
    """24. LAG로 학생별 이전 과목 대비 성적 변화와 점수 범위를 계산한다."""
    show("24. 학생별 이전 과목 대비 성적 변화", """
        WITH scored AS (
            SELECT student_id, course, grade,
                   CASE grade
                       WHEN 'A' THEN 4 WHEN 'B' THEN 3
                       WHEN 'C' THEN 2 WHEN 'D' THEN 1
                   END AS score
            FROM lab.enroll
        ), compared AS (
            SELECT *,
                   LAG(score) OVER (
                       PARTITION BY student_id ORDER BY course
                   ) AS previous_score,
                   MAX(score) OVER (PARTITION BY student_id)
                   - MIN(score) OVER (PARTITION BY student_id) AS score_range
            FROM scored
        )
        SELECT student_id, course, grade, score, previous_score,
               score - previous_score AS diff,
               CASE
                   WHEN previous_score IS NULL THEN '첫 과목'
                   WHEN score > previous_score THEN '상승'
                   WHEN score = previous_score THEN '유지'
                   ELSE '하락'
               END AS change,
               score_range
        FROM compared
        ORDER BY student_id, course
        LIMIT 5
    """)


def q25_order_window_analysis():
    """25. 주문 누적합·3건 이동평균·고객별 누적액과 전체 합계 50% 도달 주문을 계산한다."""
    show("25-1. 주문 누적합과 이동평균", """
        SELECT order_id, customer_id, amount,
               SUM(amount) OVER (
                   ORDER BY order_id
                   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
               ) AS cumulative_amount,
               ROUND(AVG(amount) OVER (
                   ORDER BY order_id
                   ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
               ), 2) AS moving_avg_3,
               SUM(amount) OVER (
                   PARTITION BY customer_id ORDER BY order_id
                   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
               ) AS customer_cumulative_amount
        FROM lab.orders
        ORDER BY order_id
        LIMIT 5
    """)
    show("25-2. 전체 주문액 50%를 처음 초과한 주문", """
        WITH cumulative AS (
            SELECT order_id, amount,
                   SUM(amount) OVER (ORDER BY order_id) AS cumulative_amount,
                   SUM(amount) OVER () AS total_amount
            FROM lab.orders
        )
        SELECT order_id, amount, cumulative_amount, total_amount,
               ROUND(cumulative_amount / total_amount * 100, 2) AS cumulative_pct
        FROM cumulative
        WHERE cumulative_amount > total_amount * 0.5
        ORDER BY order_id
        LIMIT 1
    """)



QUESTIONS = {
    "1": q01_inner_join,
    "2": q02_left_join,
    "3": q03_right_join,
    "4": q04_full_outer_join,
    "5": q05_students_without_enrollment,
    "6": q06_students_with_enrollment,
    "7": q07_customer_order_summary,
    "8": q08_top_customers,
    "9": q09_employee_manager,
    "10": q10_course_distribution,
    "11": q11_students_without_db,
    "12": q12_course_owner_report,
    "13": q13_student_course_candidates,
    "14": q14_student_department,
    "15": q15_students_above_average_gpa,
    "16": q16_students_above_department_average_gpa,
    "17": q17_students_with_enrollment,
    "18": q18_students_without_enrollment,
    "19": q19_hr_students_demo,
    "20": q20_cs_or_db_students,
    "21": q21_major_gpa_rollup,
    "22": q22_employee_hierarchy,
    "23": q23_top_three_per_major,
    "24": q24_grade_change_with_lag,
    "25": q25_order_window_analysis,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="종합실습 2 쿼리 실행")
    parser.add_argument("question", nargs="?", default="all", choices=(*QUESTIONS, "all"))
    question = parser.parse_args().question
    log_dir = Path(__file__).with_name("logs")
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / f"종합실습2_{question}_{datetime.now():%Y%m%d_%HH%MM%SS}.log"

    with log_path.open("w", encoding="utf-8") as log, redirect_stdout(Tee(sys.stdout, log)):
        if question == "all":
            for function in QUESTIONS.values():
                function()
        else:
            QUESTIONS[question]()
        print(f"\n로그 저장: {log_path}")
