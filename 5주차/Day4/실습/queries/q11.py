QUESTION = {
    "title": "안전한 나눗셈 함수 비교",
    "sql": """
        SELECT
            ecom.f_safe_div(10, 2) AS f_normal,
            ecom.f_safe_div(10, 0) AS f_zero,
            ecom.safe_div(10, 2) AS safe_normal,
            ecom.safe_div(10, 0) AS safe_zero,
            ecom.safe_div(10, NULL) AS safe_null
    """,
}
