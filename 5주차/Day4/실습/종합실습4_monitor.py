
# 사용 주의!! ai로 작성된 코드입니다. 실제 운영 환경에서 사용하기 전에 반드시 검토 후 사용하시기 바랍니다.

# --------------------------------------------------------------
# ecom_실습 실행 쿼리 모니터링 AI 코드
# 작성자 : 최승우
# 작성일 : 26.08.14
# 작성목적 : SKALA 4기 DB 활용 실습 과제 모니터링용 함수
# 함수 설명 : 
# 1. monitor() : 종합실습4 데이터 모니터링
# 2. compare_joins() : join 연산 비교
# 3. compare_access_paths() : Index/Bitmap Heap/Seq Scan 비교
# 4. materialized_view() : materialized view 생성/조회/갱신
# 5. main() : 명령행 인자 처리 및 함수 실행
# 
# 변경내역 
# 1. 26.08.14 최초 작성
# 
# --------------------------------------------------------------




# 라이브러리 설명
# argparse : 명령행 인자 처리
# datetime : 날짜/시간 처리
# config : DB 연결, 쿼리 실행, 결과 포맷, 캡처 저장 등 공통 기능 제공

import argparse
from datetime import datetime
from config import connect, connect_maintenance, format_table, query, save_capture


# 쿼리 설명 : join 연산 비교를 위한 쿼리

JOIN_QUERY = """
    SELECT o.customer_id, count(*) AS item_count, sum(oi.line_total) AS revenue
    FROM ecom.orders o JOIN ecom.order_items oi USING (order_id)
    WHERE o.order_status IN ('paid','shipped','delivered')
    GROUP BY o.customer_id
"""

ACCESS_PATH_QUERIES = {
    "index_scan": """
        SELECT
            order_id,
            customer_id,
            order_ts
        FROM ecom.orders
        WHERE order_id = 1
    """,
    "bitmap_heap_scan": """
        SELECT
            order_id,
            customer_id,
            order_ts
        FROM ecom.orders
        WHERE customer_id BETWEEN 1 AND 100
    """,
    "seq_scan": """
        SELECT
            order_id,
            customer_id,
            order_ts
        FROM ecom.orders
        WHERE customer_id BETWEEN 1 AND 3000
    """,
}


def monitor():
    sql = """
        SELECT 'active_connections' AS metric,
               count(*) FILTER (WHERE state = 'active')::text AS value
        FROM pg_stat_activity WHERE datname = current_database()
        UNION ALL
        SELECT 'cache_hit_ratio',
               round(100.0 * blks_hit / NULLIF(blks_hit + blks_read, 0), 2)::text || '%'
        FROM pg_stat_database WHERE datname = current_database()
        UNION ALL SELECT 'customers', count(*)::text FROM ecom.customers
        UNION ALL SELECT 'database_size', pg_size_pretty(pg_database_size(current_database()))
        UNION ALL SELECT 'latest_order', max(order_ts)::text FROM ecom.orders
        UNION ALL
        SELECT 'lock_waits', count(*)::text
        FROM pg_stat_activity
        WHERE datname = current_database() AND wait_event_type = 'Lock'
        UNION ALL
        SELECT 'long_queries_over_5s', count(*)::text
        FROM pg_stat_activity
        WHERE datname = current_database() AND state = 'active'
          AND pid <> pg_backend_pid() AND now() - query_start > interval '5 seconds'
        UNION ALL SELECT 'low_stock', count(*)::text FROM ecom.inventory WHERE qty_on_hand < reorder_point
        UNION ALL SELECT 'order_items', count(*)::text FROM ecom.order_items
        UNION ALL SELECT 'orders', count(*)::text FROM ecom.orders
        UNION ALL
        SELECT 'replica_lag',
               CASE WHEN pg_is_in_recovery()
                    THEN coalesce((now() - pg_last_xact_replay_timestamp())::text, 'unknown')
                    ELSE 'primary' END
        UNION ALL
        SELECT 'role_security', current_user || ': superuser=' || rolsuper::text
        FROM pg_roles WHERE rolname = current_user
        UNION ALL
        SELECT 'transactions_commit_rollback', xact_commit::text || '/' || xact_rollback::text
        FROM pg_stat_database WHERE datname = current_database()
        ORDER BY metric
    """
    columns, rows = query(sql)
    text = f"종합실습4 데이터 모니터링\n기준시각: {datetime.now().isoformat(timespec='seconds')}\n\n{format_table(columns, rows)}"
    save_capture("monitor_status", text)
    print(text)


def compare_joins():
    settings = {
        "default": ("on", "on", "on"),
        "nested_loop": ("on", "off", "off"),
        "hash_join": ("off", "on", "off"),
        "merge_join": ("off", "off", "on"),
    }
    for name, (nestloop, hashjoin, mergejoin) in settings.items():
        with connect() as connection:
            connection.execute(f"SET LOCAL enable_nestloop = {nestloop}")
            connection.execute(f"SET LOCAL enable_hashjoin = {hashjoin}")
            connection.execute(f"SET LOCAL enable_mergejoin = {mergejoin}")
            rows = connection.execute("EXPLAIN (ANALYZE, BUFFERS) " + JOIN_QUERY).fetchall()
        plan = "\n".join(row[0] for row in rows)
        save_capture(f"join_{name}", f"{name}\n\nSQL\n{JOIN_QUERY.strip()}\n\nPLAN\n{plan}")
        print(f"{name} plan captured")


def compare_access_paths():
    for name, sql in ACCESS_PATH_QUERIES.items():
        with connect() as connection:
            rows = connection.execute(
                "EXPLAIN (ANALYZE, BUFFERS) " + sql
            ).fetchall()
        plan = "\n".join(row[0] for row in rows)
        save_capture(
            f"access_{name}",
            f"{name}\n\nSQL\n{sql.strip()}\n\nPLAN\n{plan}",
        )
        print(f"{name} plan captured")


def materialized_view():
    # 생성은 보존하되, 미갱신 테스트는 트랜잭션에서 검증하고 롤백한다.
    with connect_maintenance(autocommit=True) as connection:
        connection.execute("SET lock_timeout = '5s'")
        connection.execute("SET statement_timeout = '30s'")
        exists = connection.execute(
            "SELECT to_regclass('ecom.mv_daily_gmv') IS NOT NULL"
        ).fetchone()[0]
        if not exists:
            connection.execute("""
                CREATE MATERIALIZED VIEW ecom.mv_daily_gmv AS
                SELECT date_trunc('day', o.order_ts) AS day, sum(oi.line_total) AS gmv
                FROM ecom.orders o JOIN ecom.order_items oi USING (order_id)
                WHERE o.order_status IN ('paid','shipped','delivered')
                GROUP BY 1
            """)
        connection.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS ux_mv_daily_gmv_day
            ON ecom.mv_daily_gmv(day)
        """)
        connection.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY ecom.mv_daily_gmv")

    with connect_maintenance() as connection:
        connection.execute("SET LOCAL lock_timeout = '5s'")
        connection.execute("SET LOCAL statement_timeout = '30s'")
        baseline = connection.execute(
            "SELECT sum(gmv) AS gmv FROM ecom.mv_daily_gmv"
        )
        baseline_text = format_table([c.name for c in baseline.description], baseline.fetchall())
        connection.execute("""
            INSERT INTO ecom.orders (
                order_id,
                customer_id,
                order_status,
                order_ts,
                channel
            )
            SELECT
                -1,
                min(customer_id),
                'paid',
                now(),
                'web'
            FROM ecom.customers
        """)
        connection.execute("""
            INSERT INTO ecom.order_items (
                order_item_id,
                order_id,
                product_id,
                qty,
                unit_price,
                discount
            )
            SELECT
                -1,
                -1,
                min(product_id),
                1,
                123.45,
                0
            FROM ecom.products
        """)
        stale = connection.execute("""
            SELECT
                (
                    SELECT sum(oi.line_total)
                    FROM ecom.orders o
                    JOIN ecom.order_items oi USING (order_id)
                    WHERE o.order_status IN ('paid', 'shipped', 'delivered')
                ) AS source_gmv,
                (
                    SELECT sum(gmv)
                    FROM ecom.mv_daily_gmv
                ) AS mv_gmv,
                123.45::numeric AS test_amount
        """)
        stale_text = format_table([c.name for c in stale.description], stale.fetchall())
        connection.execute("REFRESH MATERIALIZED VIEW ecom.mv_daily_gmv")
        refreshed = connection.execute("""
            SELECT
                (
                    SELECT sum(oi.line_total)
                    FROM ecom.orders o
                    JOIN ecom.order_items oi USING (order_id)
                    WHERE o.order_status IN ('paid', 'shipped', 'delivered')
                ) AS source_gmv,
                (
                    SELECT sum(gmv)
                    FROM ecom.mv_daily_gmv
                ) AS mv_gmv
        """)
        refreshed_text = format_table([c.name for c in refreshed.description], refreshed.fetchall())
        connection.rollback()

    with connect_maintenance() as connection:
        restored = connection.execute("""
            SELECT
                (SELECT count(*) FROM ecom.orders WHERE order_id = -1) AS test_orders,
                (SELECT count(*) FROM ecom.order_items WHERE order_item_id = -1) AS test_items,
                (SELECT sum(gmv) FROM ecom.mv_daily_gmv) AS mv_gmv,
                to_regclass('ecom.ux_mv_daily_gmv_day') IS NOT NULL AS unique_index
        """)
        restored_text = format_table([c.name for c in restored.description], restored.fetchall())

    save_capture(
        "materialized_view",
        "MATERIALIZED VIEW 자동 갱신 검증\n\n"
        f"1. BASELINE\n{baseline_text}\n\n"
        f"2. TEST INSERT 후, REFRESH 전 (MV는 STALE)\n{stale_text}\n\n"
        f"3. REFRESH 후\n{refreshed_text}\n\n"
        f"4. ROLLBACK 후 보존 확인\n{restored_text}",
    )
    print("materialized view captured")


STEPS = {
    "monitor": monitor,
    "joins": compare_joins,
    "access": compare_access_paths,
    "mv": materialized_view,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="종합실습4 모니터링과 추가 검증")
    parser.add_argument("step", nargs="?", default="all", choices=["all", *STEPS])
    args = parser.parse_args()
    targets = STEPS.values() if args.step == "all" else [STEPS[args.step]]
    for function in targets:
        function()
