package com.skala.shop.dto.customer;

public record SignUpResponse(
        String customerId,
        long point,
        String message
) {
}
