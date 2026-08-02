package com.skala.shop.dto.product;

import com.skala.shop.domain.product.Product;
import io.swagger.v3.oas.annotations.media.Schema;

public record ProductResponse(
        @Schema(description = "상품 ID", example = "1")
        Long id,

        @Schema(description = "상품명", example = "무선 마우스")
        String name,

        @Schema(description = "상품 가격", example = "15000")
        long price
) {

    public static ProductResponse from(Product product) {
        return new ProductResponse(
                product.getId(),
                product.getName(),
                product.getPrice()
        );
    }
}
