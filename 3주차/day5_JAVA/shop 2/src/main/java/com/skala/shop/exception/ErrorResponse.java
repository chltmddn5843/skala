package com.skala.shop.exception;

import java.time.LocalDateTime;

// ErrorResponse 클래스는 API에서 발생한 오류에 대한 정보를 담는 DTO(Data Transfer Object)입니다.
public record ErrorResponse(
    LocalDateTime timestamp,
    int status,
    String code,
    String message,
    String path
) {

}