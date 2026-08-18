QUESTION = {
    "title": "첫 구매 후 30일 내 재구매율",
    "before_sql": """
        WITH purchases AS (
            SELECT
                customer_id,
                order_ts
            FROM ecom.orders
            WHERE order_status IN ('paid', 'shipped', 'delivered')
        ),
        first_buy AS (
            SELECT
                customer_id,
                min(order_ts) AS first_order_ts
            FROM purchases
            GROUP BY customer_id
        )

        SELECT
            count(*) AS first_buyers,
            count(*) FILTER (
                WHERE EXISTS (
                    SELECT 1
                    FROM purchases p
                    WHERE p.customer_id = f.customer_id
                      AND p.order_ts > f.first_order_ts
                      AND p.order_ts <= f.first_order_ts + interval '30 days'
                )
            ) AS repurchasers,
            ecom.safe_div(
                count(*) FILTER (
                    WHERE EXISTS (
                        SELECT 1
                        FROM purchases p
                        WHERE p.customer_id = f.customer_id
                          AND p.order_ts > f.first_order_ts
                          AND p.order_ts <= f.first_order_ts + interval '30 days'
                    )
                ),
                count(*)
            ) AS repurchase_rate
        FROM first_buy f
    """,
    "after_sql": """
        WITH purchases AS (
            SELECT
                customer_id,
                order_ts,
                min(order_ts) OVER (
                    PARTITION BY customer_id
                ) AS first_order_ts
            FROM ecom.orders
            WHERE order_status IN ('paid', 'shipped', 'delivered')
        ),
        customer_flags AS (
            SELECT
                customer_id,
                bool_or(
                    order_ts > first_order_ts
                    AND order_ts <= first_order_ts + interval '30 days'
                ) AS repurchased
            FROM purchases
            GROUP BY customer_id
        )

        SELECT
            count(*) AS first_buyers,
            count(*) FILTER (WHERE repurchased) AS repurchasers,
            ecom.safe_div(
                count(*) FILTER (WHERE repurchased),
                count(*)
            ) AS repurchase_rate
        FROM customer_flags
    """,
}
