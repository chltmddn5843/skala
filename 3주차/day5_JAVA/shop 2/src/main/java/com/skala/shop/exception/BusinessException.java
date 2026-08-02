package com.skala.shop.exception;




// BusinessException 클래스는 RuntimeException을 상속받아 사용자 정의 예외를 나타냅니다. 이 클래스는 ErrorCode 객체를 포함하며, 예외 발생 시 해당 에러 코드와 메시지를 제공합니다.
public class BusinessException extends RuntimeException {

    private final ErrorCode errorCode;

    public BusinessException(ErrorCode errorCode) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
    }

    public ErrorCode getErrorCode() {
        return errorCode;
    }
}