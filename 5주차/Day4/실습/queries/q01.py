QUESTION = {
    "title": "최근 한 달 실제 총매출",
    "before_sql": """
        SELECT
            sum(oi.line_total) AS total_revenue
        FROM ecom.orders o
        JOIN ecom.order_items oi
          ON oi.order_id = o.order_id
        WHERE o.order_status IN ('paid', 'shipped', 'delivered')
          AND o.order_ts >= now() - interval '1 month'
    """,
    "after_sql": """
        WITH recent_orders AS (
            SELECT
                order_id
            FROM ecom.orders
            WHERE order_status IN ('paid', 'shipped', 'delivered')
              AND order_ts >= now() - interval '1 month'
        )

        SELECT
            sum(oi.line_total) AS total_revenue
        FROM recent_orders ro
        JOIN ecom.order_items oi
          ON oi.order_id = ro.order_id
    """,
}
