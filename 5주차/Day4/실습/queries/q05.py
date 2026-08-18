QUESTION = {
    "title": "고객 RFM",
    "before_sql": """
        SELECT
            c.customer_id,
            c.full_name,
            current_date - max(o.order_ts)::date AS recency_days,
            count(DISTINCT o.order_id) AS frequency,
            sum(oi.line_total) AS monetary
        FROM ecom.customers c
        JOIN ecom.orders o
          ON o.customer_id = c.customer_id
        JOIN ecom.order_items oi
          ON oi.order_id = o.order_id
        WHERE o.order_status IN ('paid', 'shipped', 'delivered')
        GROUP BY
            c.customer_id,
            c.full_name
        ORDER BY
            monetary DESC,
            c.customer_id
    """,
    "after_sql": """
        WITH order_totals AS (
            SELECT
                o.customer_id,
                o.order_id,
                o.order_ts,
                sum(oi.line_total) AS amount
            FROM ecom.orders o
            JOIN ecom.order_items oi
              ON oi.order_id = o.order_id
            WHERE o.order_status IN ('paid', 'shipped', 'delivered')
            GROUP BY
                o.customer_id,
                o.order_id,
                o.order_ts
        )

        SELECT
            c.customer_id,
            c.full_name,
            current_date - max(ot.order_ts)::date AS recency_days,
            count(*) AS frequency,
            sum(ot.amount) AS monetary
        FROM order_totals ot
        JOIN ecom.customers c
          ON c.customer_id = ot.customer_id
        GROUP BY
            c.customer_id,
            c.full_name
        ORDER BY
            monetary DESC,
            c.customer_id
    """,
}
