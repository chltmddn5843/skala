package com.skala.shop.exception;

import org.springframework.http.HttpStatus;



// ErrorCode enum은 애플리케이션에서 발생할 수 있는 다양한 오류 상황을 정의하고, 각 오류에 대한 HTTP 상태 코드, 오류 코드 문자열, 그리고 사용자에게 보여줄 메시지를 포함합니다. 이를 통해 일관된 방식으로 오류를 처리하고 클라이언트에게 명확한 정보를 제공할 수 있습니다.
public enum ErrorCode {
    PRODUCT_NOT_FOUND(HttpStatus.NOT_FOUND, "PRODUCT_NOT_FOUND", "상품을 찾을 수 없습니다."),
    CUSTOMER_NOT_FOUND(HttpStatus.NOT_FOUND, "CUSTOMER_NOT_FOUND", "고객을 찾을 수 없습니다."),
    DUPLICATE_CUSTOMER_ID(HttpStatus.CONFLICT, "DUPLICATE_CUSTOMER_ID", "이미 사용 중인 고객 ID 입니다."),
    INVALID_CREDENTIALS(HttpStatus.UNAUTHORIZED, "INVALID_CREDENTIALS", "고객 ID 또는 비밀번호가 올바르지 않습니다."),
    INSUFFICIENT_FUNDS(HttpStatus.CONFLICT, "INSUFFICIENT_FUNDS", "보유 포인트가 부족합니다."),
    ORDER_NOT_FOUND(HttpStatus.NOT_FOUND, "ORDER_NOT_FOUND", "주문한 상품을 찾을 수 없습니다."),
    INSUFFICIENT_QUANTITY(HttpStatus.CONFLICT, "INSUFFICIENT_QUANTITY", "취소 수량이 주문 수량보다 많습니다."),
    INVALID_REQUEST(HttpStatus.BAD_REQUEST, "INVALID_REQUEST", "요청 값을 확인해 주세요."),
    INTERNAL_ERROR(HttpStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "서버 내부 오류가 발생했습니다.");

    private final HttpStatus status;
    private final String code;
    private final String message;

    ErrorCode(HttpStatus status, String code, String message) {
        this.status = status;
        this.code = code;
        this.message = message;
    }

    public HttpStatus getStatus() {
        return status;
    }

    public String getCode() {
        return code;
    }

    public String getMessage() {
        return message;
    }
}