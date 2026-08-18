QUESTION = {
    "title": "월별 주문 수·매출·AOV",
    "before_sql": """
        SELECT
            date_trunc('month', o.order_ts)::date AS month,
            count(DISTINCT o.order_id) AS order_count,
            sum(oi.line_total) AS revenue,
            sum(oi.line_total) / count(DISTINCT o.order_id) AS aov
        FROM ecom.orders o
        JOIN ecom.order_items oi
          ON oi.order_id = o.order_id
        WHERE o.order_status IN ('paid', 'shipped', 'delivered')
        GROUP BY date_trunc('month', o.order_ts)::date
        ORDER BY month
    """,
    "after_sql": """
        WITH order_totals AS (
            SELECT
                o.order_id,
                date_trunc('month', o.order_ts)::date AS month,
                sum(oi.line_total) AS amount
            FROM ecom.orders o
            JOIN ecom.order_items oi
              ON oi.order_id = o.order_id
            WHERE o.order_status IN ('paid', 'shipped', 'delivered')
            GROUP BY
                o.order_id,
                date_trunc('month', o.order_ts)::date
        )

        SELECT
            month,
            count(*) AS order_count,
            sum(amount) AS revenue,
            ecom.safe_div(sum(amount), count(*)) AS aov
        FROM order_totals
        GROUP BY month
        ORDER BY month
    """,
}
