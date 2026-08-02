package com.skala.shop.controller;

import com.skala.shop.dto.cart.CartItemRequest;
import com.skala.shop.dto.cart.CartResponse;
import com.skala.shop.service.CartService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@Tag(name = "장바구니 API", description = "장바구니 담기, 조회, 삭제 API")
@RestController
@RequestMapping("/api/cart")
public class CartController {

    private final CartService cartService;

    public CartController(CartService cartService) {
        this.cartService = cartService;
    }

    @Operation(summary = "내 장바구니 조회")
    @GetMapping
    public ResponseEntity<CartResponse> getMyCart(@AuthenticationPrincipal String customerId) {
        CartResponse response = cartService.getMyCart(customerId);
        return ResponseEntity.ok(response);
    }

    @Operation(summary = "장바구니 상품 추가")
    @PostMapping("/items")
    public ResponseEntity<Void> addCartItem(
            @AuthenticationPrincipal String customerId,
            @Valid @RequestBody CartItemRequest request
    ) {
        cartService.addCartItem(customerId, request);
        return ResponseEntity.ok().build();
    }

    @Operation(summary = "장바구니 상품 삭제")
    @DeleteMapping("/items/{cartItemId}")
    public ResponseEntity<Void> deleteCartItem(
            @AuthenticationPrincipal String customerId,
            @PathVariable Long cartItemId
    ) {
        cartService.deleteCartItem(customerId, cartItemId);
        return ResponseEntity.ok().build();
    }
}