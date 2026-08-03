package com.skala.shop.dto.customer;

public record SignUpResponse(String customerId, long initialPoint, String message) {
}