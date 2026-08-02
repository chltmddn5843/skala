package com.skala.shop.dto.cart;

import java.util.List;

public record CartResponse(
    List<CartItemResponse> items,
    long totalPrice
) {
}