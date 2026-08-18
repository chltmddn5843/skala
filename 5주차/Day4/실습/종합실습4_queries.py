
# 사용 주의!! ai로 작성된 코드입니다. 실제 운영 환경에서 사용하기 전에 반드시 검토 후 사용하시기 바랍니다.

# --------------------------------------------------------------
# ecom_실습 실행 쿼리 실행용 AI 코드
# 작성자 : 최승우
# 작성일 : 26.08.14
# 작성목적 : SKALA 4기 DB 활용 실습 과제 실행용 함수
# 함수 설명
# 1. performance_log() : EXPLAIN (ANALYZE, BUFFERS) 실행 및 원문 반환
# 2. run_question() : Q1~Q11 실행 및 로그 캡처
# 3. q01()~q11() : Q1~Q11 실행용
# 4. main() : 명령행 인자 처리 및 함수 실행
# 
# 변경내역 
# 1. 26.08.14 최초 작성
# 
# --------------------------------------------------------------





import argparse
from time import perf_counter

from config import format_table, query, save_capture
from queries import QUESTIONS


def performance_log(sql):
    """실제 EXPLAIN 실행 SQL과 PostgreSQL 반환 결과를 그대로 돌려준다."""
    explain_sql = "EXPLAIN (ANALYZE, BUFFERS)\n" + sql
    _, plan_rows = query(explain_sql)
    return explain_sql, "\n".join(row[0] for row in plan_rows)


def run_variant(number, variant):
    item = QUESTIONS[number]
    sql = item[f"{variant}_sql"].strip()
    started = perf_counter()
    columns, rows = query(sql)
    elapsed_ms = (perf_counter() - started) * 1000

    result_log = (
        f"Q{number:02d} {item['title']} [{variant}]\n\n"
        f"SQL\n{sql}\n\n"
        f"RESULT ({elapsed_ms:.2f} ms)\n{format_table(columns, rows)}"
    )
    explain_sql, plan_result = performance_log(sql)
    plan_log = (
        f"Q{number:02d} {item['title']} [{variant}]\n\n"
        f"PERFORMANCE SQL\n{explain_sql}\n\n"
        f"PERFORMANCE RESULT\n{plan_result}"
    )

    save_capture(f"Q{number:02d}_{variant}", result_log)
    save_capture(f"Q{number:02d}_plan_{variant}", plan_log)
    print(f"Q{number:02d} {variant}: {len(rows)} rows, {elapsed_ms:.2f} ms")
    return rows


def run_question(number):
    if number == 11:
        item = QUESTIONS[number]
        sql = item["sql"].strip()
        columns, rows = query(sql)
        explain_sql, plan_result = performance_log(sql)
        result_log = f"Q11 {item['title']}\n\nSQL\n{sql}\n\nRESULT\n{format_table(columns, rows)}"
        plan_log = (
            f"Q11 {item['title']}\n\n"
            f"PERFORMANCE SQL\n{explain_sql}\n\n"
            f"PERFORMANCE RESULT\n{plan_result}"
        )
        save_capture("Q11", result_log)
        save_capture("Q11_plan", plan_log)
        print(f"Q11: {len(rows)} rows")
        return rows

    before = run_variant(number, "before")
    after = run_variant(number, "after")
    assert before == after, f"Q{number:02d} 튜닝 전후 결과 불일치"
    return {"before": before, "after": after}


def q01(): return run_question(1)
def q02(): return run_question(2)
def q03(): return run_question(3)
def q04(): return run_question(4)
def q05(): return run_question(5)
def q06(): return run_question(6)
def q07(): return run_question(7)
def q08(): return run_question(8)
def q09(): return run_question(9)
def q10(): return run_question(10)
def q11(): return run_question(11)


FUNCTIONS = {number: globals()[f"q{number:02d}"] for number in QUESTIONS}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="종합실습 4 Q1~Q11 실행 및 로그 캡처")
    parser.add_argument("question", nargs="?", default="all", choices=["all", *map(str, QUESTIONS)])
    args = parser.parse_args()
    targets = FUNCTIONS.values() if args.question == "all" else [FUNCTIONS[int(args.question)]]
    for function in targets:
        function()
