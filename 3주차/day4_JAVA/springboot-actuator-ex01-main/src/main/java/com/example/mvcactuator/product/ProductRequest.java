package com.example.mvcactuator.product;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;

public record ProductRequest(
        @NotBlank(message = "상품명은 필수입니다.")
        String name,

        @Positive(message = "가격은 1원 이상이어야 합니다.")
        int price) {
}