QUESTION = {
    "title": "상위 1% 고객의 최근 60일 매출",
    "before_sql": """
        WITH lifetime AS (
            SELECT
                o.customer_id,
                sum(oi.line_total) AS lifetime_revenue
            FROM ecom.orders o
            JOIN ecom.order_items oi
              ON oi.order_id = o.order_id
            WHERE o.order_status IN ('paid', 'shipped', 'delivered')
            GROUP BY o.customer_id
        ),
        top_customers AS (
            SELECT
                customer_id,
                lifetime_revenue
            FROM lifetime
            ORDER BY
                lifetime_revenue DESC,
                customer_id
            LIMIT 30
        )

        SELECT
            tc.customer_id,
            tc.lifetime_revenue,
            (
                SELECT sum(oi.line_total)
                FROM ecom.orders o
                JOIN ecom.order_items oi
                  ON oi.order_id = o.order_id
                WHERE o.customer_id = tc.customer_id
                  AND o.order_status IN ('paid', 'shipped', 'delivered')
                  AND o.order_ts >= now() - interval '60 days'
            ) AS recent_60d_revenue
        FROM top_customers tc
        ORDER BY
            tc.lifetime_revenue DESC,
            tc.customer_id
    """,
    "after_sql": """
        WITH customer_sales AS (
            SELECT
                o.customer_id,
                sum(oi.line_total) AS lifetime_revenue,
                sum(oi.line_total) FILTER (
                    WHERE o.order_ts >= now() - interval '60 days'
                ) AS recent_60d_revenue
            FROM ecom.orders o
            JOIN ecom.order_items oi
              ON oi.order_id = o.order_id
            WHERE o.order_status IN ('paid', 'shipped', 'delivered')
            GROUP BY o.customer_id
        )

        SELECT
            customer_id,
            lifetime_revenue,
            recent_60d_revenue
        FROM customer_sales
        ORDER BY
            lifetime_revenue DESC,
            customer_id
        LIMIT 30
    """,
}
