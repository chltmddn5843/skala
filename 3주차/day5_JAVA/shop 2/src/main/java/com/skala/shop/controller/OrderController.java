package com.skala.shop.controller;

import com.skala.shop.dto.order.CustomerOrderResponse;
import com.skala.shop.dto.order.OrderRequest;
import com.skala.shop.dto.order.OrderResultResponse;
import com.skala.shop.service.OrderService;

import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Tag(name = "주문 API", description = "주문, 주문 취소, 내 주문 조회 API")
@RequestMapping("/api/customers")
public class OrderController {

    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @GetMapping("/me")
    public ResponseEntity<CustomerOrderResponse> findMyOrders(Authentication authentication) {
        // JWT 필터가 Controller 보다 먼저 실행되어 인증 정보에 고객 ID 를 저장해 둡니다.
        return ResponseEntity.ok(orderService.findMyOrders(authentication.getName()));
    }

    @PostMapping("/order")
    public ResponseEntity<OrderResultResponse> placeOrder(
            Authentication authentication,
            @Valid @RequestBody OrderRequest request
    ) {
        return ResponseEntity.ok(
                orderService.placeOrder(authentication.getName(), request)
        );
    }

    @PostMapping("/cancel")
    public ResponseEntity<OrderResultResponse> cancelOrder(
            Authentication authentication,
            @Valid @RequestBody OrderRequest request
    ) {
        return ResponseEntity.ok(
                orderService.cancelOrder(authentication.getName(), request)
        );
    }
}