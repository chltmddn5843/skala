package com.skala.shop.dto.cart;

import com.skala.shop.domain.cart.CartItem;

public record CartItemResponse(
    Long cartItemId,
    Long productId,
    String productName,
    long price,
    int quantity,
    long itemTotalPrice
) {
    public static CartItemResponse from(CartItem cartItem) {
        long totalPrice = cartItem.getProduct().getPrice() * cartItem.getQuantity();
        return new CartItemResponse(
            cartItem.getId(),
            cartItem.getProduct().getId(),
            cartItem.getProduct().getName(),
            cartItem.getProduct().getPrice(),
            cartItem.getQuantity(),
            totalPrice
        );
    }
}