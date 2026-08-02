package com.skala.shop.dto.customer;

public record LoginResponse(
    String accessToken,
    String tokenType,
    long expiresInMinutes
) {
}