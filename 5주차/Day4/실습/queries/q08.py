QUESTION = {
    "title": "리뷰 기반 효자상품",
    "before_sql": """
        SELECT
            p.product_id,
            p.product_name,
            avg(r.rating) AS avg_rating,
            count(*) AS review_count
        FROM ecom.products p
        JOIN ecom.reviews r
          ON r.product_id = p.product_id
        GROUP BY
            p.product_id,
            p.product_name
        HAVING avg(r.rating) >= 4.5
           AND count(*) >= 50
        ORDER BY
            avg_rating DESC,
            review_count DESC,
            p.product_id
    """,
    "after_sql": """
        WITH review_summary AS (
            SELECT
                product_id,
                avg(rating) AS avg_rating,
                count(*) AS review_count
            FROM ecom.reviews
            GROUP BY product_id
            HAVING avg(rating) >= 4.5
               AND count(*) >= 50
        )

        SELECT
            rs.product_id,
            p.product_name,
            rs.avg_rating,
            rs.review_count
        FROM review_summary rs
        JOIN ecom.products p
          ON p.product_id = rs.product_id
        ORDER BY
            rs.avg_rating DESC,
            rs.review_count DESC,
            rs.product_id
    """,
}
