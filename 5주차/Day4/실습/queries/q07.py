QUESTION = {
    "title": "재고 부족 위험 상품",
    "before_sql": """
        SELECT
            p.product_id,
            p.product_name,
            (
                SELECT i.qty_on_hand
                FROM ecom.inventory i
                WHERE i.product_id = p.product_id
            ) AS qty_on_hand,
            (
                SELECT i.reorder_point
                FROM ecom.inventory i
                WHERE i.product_id = p.product_id
            ) AS reorder_point,
            (
                SELECT i.reorder_point - i.qty_on_hand
                FROM ecom.inventory i
                WHERE i.product_id = p.product_id
            ) AS shortage
        FROM ecom.products p
        WHERE (
            SELECT i.qty_on_hand < i.reorder_point
            FROM ecom.inventory i
            WHERE i.product_id = p.product_id
        )
        ORDER BY
            shortage DESC,
            p.product_id
    """,
    "after_sql": """
        SELECT
            p.product_id,
            p.product_name,
            i.qty_on_hand,
            i.reorder_point,
            i.reorder_point - i.qty_on_hand AS shortage
        FROM ecom.inventory i
        JOIN ecom.products p
          ON p.product_id = i.product_id
        WHERE i.qty_on_hand < i.reorder_point
        ORDER BY
            shortage DESC,
            p.product_id
    """,
}
