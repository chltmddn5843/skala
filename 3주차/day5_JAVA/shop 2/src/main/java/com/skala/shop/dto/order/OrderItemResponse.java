package com.skala.shop.dto.order;

import com.skala.shop.domain.order.OrderItem;

public record OrderItemResponse(
    Long productId,
    String productName,
    long unitPrice,
    int quantity,
    long totalPrice
) {
    public static OrderItemResponse from(OrderItem orderItem) {
        // multiplyExact 는 계산 결과가 long 범위를 넘으면 예외를 던져 금액 오류를 방지합니다.
        long totalPrice = Math.multiplyExact(
                orderItem.getProduct().getPrice(),
                (long) orderItem.getQuantity()
        );
        return new OrderItemResponse(
                orderItem.getProduct().getId(),
                orderItem.getProduct().getName(),
                orderItem.getProduct().getPrice(),
                orderItem.getQuantity(),
                totalPrice
        );
    }
}