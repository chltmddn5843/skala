QUESTION = {
    "title": "최근 90일 카테고리 매출 Top 10",
    "before_sql": """
        SELECT
            c.category_id,
            c.category_name,
            sum(oi.line_total) AS revenue
        FROM ecom.order_items oi
        JOIN ecom.orders o
          ON o.order_id = oi.order_id
        JOIN ecom.products p
          ON p.product_id = oi.product_id
        JOIN ecom.categories c
          ON c.category_id = p.category_id
        WHERE o.order_status IN ('paid', 'shipped', 'delivered')
          AND o.order_ts >= now() - interval '90 days'
        GROUP BY
            c.category_id,
            c.category_name
        ORDER BY
            revenue DESC,
            c.category_id
        LIMIT 10
    """,
    "after_sql": """
        WITH recent_sales AS (
            SELECT
                oi.product_id,
                oi.line_total
            FROM ecom.orders o
            JOIN ecom.order_items oi
              ON oi.order_id = o.order_id
            WHERE o.order_status IN ('paid', 'shipped', 'delivered')
              AND o.order_ts >= now() - interval '90 days'
        )

        SELECT
            c.category_id,
            c.category_name,
            sum(rs.line_total) AS revenue
        FROM recent_sales rs
        JOIN ecom.products p
          ON p.product_id = rs.product_id
        JOIN ecom.categories c
          ON c.category_id = p.category_id
        GROUP BY
            c.category_id,
            c.category_name
        ORDER BY
            revenue DESC,
            c.category_id
        LIMIT 10
    """,
}
