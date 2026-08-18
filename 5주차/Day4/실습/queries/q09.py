QUESTION = {
    "title": "쿠폰 사용 여부별 평균 주문 금액",
    "before_sql": """
        SELECT
            o.coupon_code IS NOT NULL AS used_coupon,
            count(DISTINCT o.order_id) AS order_count,
            sum(oi.line_total) / count(DISTINCT o.order_id) AS avg_order_amount
        FROM ecom.orders o
        JOIN ecom.order_items oi
          ON oi.order_id = o.order_id
        WHERE o.order_status IN ('paid', 'shipped', 'delivered')
        GROUP BY o.coupon_code IS NOT NULL
        ORDER BY used_coupon
    """,
    "after_sql": """
        WITH order_totals AS (
            SELECT
                o.order_id,
                o.coupon_code IS NOT NULL AS used_coupon,
                sum(oi.line_total) AS amount
            FROM ecom.orders o
            JOIN ecom.order_items oi
              ON oi.order_id = o.order_id
            WHERE o.order_status IN ('paid', 'shipped', 'delivered')
            GROUP BY
                o.order_id,
                o.coupon_code IS NOT NULL
        )

        SELECT
            used_coupon,
            count(*) AS order_count,
            avg(amount) AS avg_order_amount
        FROM order_totals
        GROUP BY used_coupon
        ORDER BY used_coupon
    """,
}
