# 프로그램 전체 설명 및 변경 내역
# -------------------
# 작성자 : 최승우
# 작성일 : 2026-08-04
# 작성 목적
# 1) Pandas EDA, Polars Lazy, Duck DB SQL 성능 비교 및 실행 시간 측정
# 
# 변경 내역
# 26.08.04 / 최초 작성 / 전체 코드 작성
# 26.08.04 / 2차 작성 / Pandas named aggregation 추가
# 26.08.04 / 3차 작성 / Polars Lazy API, DuckDB SQL, timeit 벤치마크 및 로깅 통합
# 26.08.04 / 4차 작성 / 11개 원본 컬럼 스키마 호환 및 세 결과 검증 로직 반영
# -------------------

import os
import sys
import timeit
import logging
import duckdb
import pandas as pd
import polars as pl
from pathlib import Path

# ----------------------------------------------------
# 로깅 설정 (콘솔 출력 + app.log 저장)
# ----------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# 기본 경로 설정
file_path = Path("/Users/chltmddn5843/Downloads/skala/4주차/실습자료2/sales_100k.csv")
BENCHMARK_NUMBER = 3  # timeit 반복 횟수


# 1. CSV 파일 읽기 함수
def read_csv_file(path):
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        logging.error(f"파일 읽기 오류: {e}")
        return None


# 2. EDA 및 이상치 탐지/제거 함수
def detect_and_remove_outliers(df, column):
    if df is None:
        print("원본 데이터가 올바르지 않습니다.")
        return None, None, None, None

    # amount 컬럼 숫자 변환 및 필수값 정제
    df_clean = df.dropna(subset=['region', 'category', column]).copy()
    df_clean[column] = pd.to_numeric(df_clean[column], errors='coerce')

    Q1 = df_clean[column].quantile(0.25)
    Q3 = df_clean[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df_clean[(df_clean[column] < lower_bound) | (df_clean[column] > upper_bound)]
    cleaned_df = df_clean[(df_clean[column] >= lower_bound) & (df_clean[column] <= upper_bound)]

    print("\n" + "=" * 50)
    print("[이상치 탐지 및 제거 결과]")
    print("=" * 50)
    print(f"원본 데이터 개수: {len(df):,}건")
    print(f"정제 후 데이터 개수: {len(df_clean):,}건")
    print(f"이상치 제거 후 데이터 개수: {len(cleaned_df):,}건")
    print(f"제거된 이상치 개수: {len(outliers):,}건")
    print(f"IQR 하한: {lower_bound:,.2f} / 상한: {upper_bound:,.2f}")

    return outliers, cleaned_df, lower_bound, upper_bound


# 3. Pandas Named Aggregation
def pandas_groupby_named_aggregation(path, lower, upper):
    df = pd.read_csv(path)
    df['region'] = df['region'].astype(str).str.strip()
    df['category'] = df['category'].astype(str).str.strip()
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    
    cleaned = df.dropna(subset=['region', 'category', 'amount'])
    normal = cleaned[(cleaned['amount'] >= lower) & (cleaned['amount'] <= upper)]

    result = (
        normal.groupby(['region', 'category'], as_index=False)
        .agg(
            total=('amount', 'sum'),
            mean=('amount', 'mean'),
            count=('amount', 'count')
        )
        .sort_values(by=['total', 'region', 'category'], ascending=[False, True, True])
        .reset_index(drop=True)
    )
    return result


# 4. Polars Lazy API 집계
# 플로우: scan_csv -> filter -> group_by -> agg -> sort -> collect()
def polars_lazy_aggregation(path, lower, upper):
    result = (
        pl.scan_csv(
            str(path),
            schema_overrides={
                "region": pl.String,
                "category": pl.String,
                "amount": pl.String,
            }
        )

        # 데이터 타입 정제 및 수식어 제거
        # 공백으로 인해서 Seoul과 Seoul  가 다른 값으로 인식되는 문제 해결
        .with_columns([
            pl.col("region").str.strip_chars(),
            pl.col("category").str.strip_chars(),
            pl.col("amount").cast(pl.Float64, strict=False)
        ])

        # 필터링 조건: region, category, amount 컬럼이 null이 아니고, amount가 lower와 upper 사이에 있는 데이터만 선택
        .filter(
            pl.col("region").is_not_null() &
            pl.col("category").is_not_null() &
            (pl.col("region") != "") &
            (pl.col("category") != "") &
            pl.col("amount").is_not_null() &
            (pl.col("amount") >= lower) &
            (pl.col("amount") <= upper)
        )
        
        # 실습 조건
        .group_by(["region", "category"])
        .agg([
            pl.col("amount").sum().alias("total"),
            pl.col("amount").mean().alias("mean"),
            pl.len().alias("count")
        ])
        .sort(["total", "region", "category"], descending=[True, False, False])
        .collect()
    )
    return result.to_pandas()


# 5. DuckDB SQL 집계
def duckdb_sql_aggregation(path, lower, upper):
    sql_path = str(path).replace("\\", "/")
    query = f"""
        WITH cleaned AS (
            SELECT
                TRIM(region) AS region,
                TRIM(category) AS category,
                TRY_CAST(amount AS DOUBLE) AS amount
            FROM read_csv('{sql_path}', header=true, all_varchar=true)
        )
        SELECT
            region,
            category,
            SUM(amount) AS total,
            AVG(amount) AS mean,
            COUNT(amount) AS count
        FROM cleaned
        WHERE region IS NOT NULL AND region <> ''
          AND category IS NOT NULL AND category <> ''
          AND amount IS NOT NULL
          AND amount BETWEEN {lower} AND {upper}
        GROUP BY region, category
        ORDER BY total DESC, region ASC, category ASC
    """
    with duckdb.connect(database=":memory:") as conn:
        return conn.execute(query).df()


# 6. 세 도구 결과 일치성 검증 함수
def check_results_equal(df1, df2, tool1_name="Tool1", tool2_name="Tool2"):
    try:
        pd.testing.assert_frame_equal(
            df1.sort_values(['region', 'category']).reset_index(drop=True),
            df2.sort_values(['region', 'category']).reset_index(drop=True),
            check_dtype=False,
            rtol=1e-5
        )
        logging.info(f"[{tool1_name} vs {tool2_name}] 집계 결과 일치: True")
        return True
    except AssertionError as e:
        logging.error(f"[{tool1_name} vs {tool2_name}] 집계 결과 불일치: {e}")
        return False


# 7. timeit 실행 시간 벤치마크 함수
def benchmark(name, func):
    logging.info(f"{name} 벤치마크 측정 시작 (반복 횟수: {BENCHMARK_NUMBER})...")
    seconds = timeit.timeit(func, number=BENCHMARK_NUMBER)
    avg_sec = seconds / BENCHMARK_NUMBER
    logging.info(f"{name} 평균 실행 시간: {avg_sec:.6f}초")
    return {"도구": name, "평균 실행 시간(초)": round(avg_sec, 6)}


# 메인 실행 함수
def main():
    logging.info("================ 프로그램 시작 ================")
    
    # 1. 파일 확인 및 이상치 범위 확보
    df = read_csv_file(file_path)
    if df is None:
        return

    _, _, lower_bound, upper_bound = detect_and_remove_outliers(df, 'amount')

    # 2. 각 방식별 집계 결과 확인 및 출력
    logging.info("각 도구별 집계를 수행합니다.")
    pandas_df = pandas_groupby_named_aggregation(file_path, lower_bound, upper_bound)
    polars_df = polars_lazy_aggregation(file_path, lower_bound, upper_bound)
    duckdb_df = duckdb_sql_aggregation(file_path, lower_bound, upper_bound)

    print("\n" + "=" * 50)
    print("[Pandas Aggregation 결과 (상위 5개)]")
    print(pandas_df.head())

    print("\n" + "=" * 50)
    print("[Polars Lazy API Aggregation 결과 (상위 5개)]")
    print(polars_df.head())

    print("\n" + "=" * 50)
    print("[DuckDB SQL Aggregation 결과 (상위 5개)]")
    print(duckdb_df.head())

    # 3. 결과 일치성 검증
    print("\n" + "=" * 50)
    print("[집계 결과 일치 검증]")
    print("=" * 50)
    match_polars = check_results_equal(pandas_df, polars_df, "Pandas", "Polars")
    match_duckdb = check_results_equal(pandas_df, duckdb_df, "Pandas", "DuckDB")
    print(f"Pandas와 Polars 결과 일치: {match_polars}")
    print(f"Pandas와 DuckDB 결과 일치: {match_duckdb}")

    # 4. timeit 벤치마크 실행
    print("\n" + "=" * 50)
    print(f"[timeit 실행 시간 비교 (동일 반복 횟수: {BENCHMARK_NUMBER}회)]")
    print("=" * 50)
    
    results = [
        benchmark("Pandas", lambda: pandas_groupby_named_aggregation(file_path, lower_bound, upper_bound)),
        benchmark("Polars Lazy", lambda: polars_lazy_aggregation(file_path, lower_bound, upper_bound)),
        benchmark("DuckDB SQL", lambda: duckdb_sql_aggregation(file_path, lower_bound, upper_bound))
    ]

    benchmark_df = pd.DataFrame(results).sort_values(by="평균 실행 시간(초)")
    print("\n" + benchmark_df.to_string(index=False))
    
    # 벤치마크 최종 결과를 로그 파일에 남김
    logging.info(f"최종 벤치마크 결과:\n{benchmark_df.to_string(index=False)}")
    logging.info("================ 프로그램 완료 ================")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.critical(f"프로그램 실행 중 오류 발생: {e}", exc_info=True)