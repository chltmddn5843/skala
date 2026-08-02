package com.skala.shop.dto.product;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;

public record ProductRequest(
    @Schema(description = "상품명", example = "무선 마우스")
    @NotBlank(message = "상품명은 필수입니다.")
    @Size(max = 100, message = "상품명은 100자 이하여야 합니다.")
    String name,

    @Schema(description = "상품 가격", example = "15000")
    @Positive(message = "상품 가격은 1원 이상이어야 합니다.")
    long price
) {
}
