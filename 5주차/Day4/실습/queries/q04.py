QUESTION = {
    "title": "상품별 누적매출 RANK Top 20",
    "before_sql": """
        SELECT
            p.product_id,
            p.product_name,
            sum(oi.line_total) AS revenue,
            rank() OVER (
                ORDER BY sum(oi.line_total) DESC
            ) AS revenue_rank
        FROM ecom.products p
        JOIN ecom.order_items oi
          ON oi.product_id = p.product_id
        JOIN ecom.orders o
          ON o.order_id = oi.order_id
        WHERE o.order_status IN ('paid', 'shipped', 'delivered')
        GROUP BY
            p.product_id,
            p.product_name
        ORDER BY
            revenue_rank,
            p.product_id
        LIMIT 20
    """,
    "after_sql": """
        WITH product_revenue AS (
            SELECT
                oi.product_id,
                sum(oi.line_total) AS revenue
            FROM ecom.order_items oi
            JOIN ecom.orders o
              ON o.order_id = oi.order_id
            WHERE o.order_status IN ('paid', 'shipped', 'delivered')
            GROUP BY oi.product_id
        ),
        ranked_products AS (
            SELECT
                product_id,
                revenue,
                rank() OVER (ORDER BY revenue DESC) AS revenue_rank
            FROM product_revenue
        )

        SELECT
            rp.product_id,
            p.product_name,
            rp.revenue,
            rp.revenue_rank
        FROM ranked_products rp
        JOIN ecom.products p
          ON p.product_id = rp.product_id
        WHERE rp.revenue_rank <= 20
        ORDER BY
            rp.revenue_rank,
            rp.product_id
        LIMIT 20
    """,
}
