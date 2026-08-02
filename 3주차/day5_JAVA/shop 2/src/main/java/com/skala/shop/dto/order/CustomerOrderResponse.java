package com.skala.shop.dto.order;

import java.util.List;

public record CustomerOrderResponse(
    String customerId,
    long point,
    List<OrderItemResponse> orders
) {
}