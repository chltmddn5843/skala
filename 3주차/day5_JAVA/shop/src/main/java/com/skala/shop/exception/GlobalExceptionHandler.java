package com.skala.shop.exception;

import jakarta.servlet.http.HttpServletRequest;
import java.time.LocalDateTime;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;


// GlobalExceptionHandler 클래스는 애플리케이션 전역에서 발생하는 예외를 처리하고, 일관된 형식의 오류 응답을 클라이언트에게 반환합니다. 이를 통해 예외 처리 로직을 중앙 집중화하고, 코드 중복을 줄이며, 클라이언트에게 명확한 오류 정보를 제공할 수 있습니다.
@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    // BusinessException은 애플리케이션의 업무 규칙 위반을 나타내는 사용자 정의 예외입니다. 이 예외가 발생하면, 해당 에러 코드와 메시지를 기반으로 클라이언트에게 적절한 오류 응답을 반환합니다.
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(
            BusinessException exception,
            HttpServletRequest request
    ) {
        ErrorCode errorCode = exception.getErrorCode();
        // 업무 규칙 위반은 정상적인 흐름의 하나이므로 WARN 레벨로 남깁니다.
        log.warn("BusinessException: {} {}", errorCode.getCode(), request.getRequestURI());
        return ResponseEntity.status(errorCode.getStatus())
                .body(createResponse(errorCode, errorCode.getMessage(), request.getRequestURI()));
    }

    // MethodArgumentNotValidException은 @Valid 또는 @Validated 어노테이션을 사용한 요청 바인딩 시, 유효성 검증에 실패했을 때 발생합니다. 이 예외가 발생하면, 필드별 오류 메시지를 수집하여 클라이언트에게 반환합니다.
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(
            MethodArgumentNotValidException exception,
            HttpServletRequest request
    ) {
        // 필드 오류의 순서는 실행마다 달라질 수 있으므로,
        // "필드명: 사유" 형태로 모두 모아 필드명 순으로 정렬해 항상 같은 메시지를 만듭니다.
        String message = exception.getBindingResult().getFieldErrors().stream()
                .map(error -> error.getField() + ": " + error.getDefaultMessage())
                .sorted()
                .collect(Collectors.joining(", "));
        if (message.isBlank()) {
            message = ErrorCode.INVALID_REQUEST.getMessage();
        }
        return ResponseEntity.badRequest()
                .body(createResponse(ErrorCode.INVALID_REQUEST, message, request.getRequestURI()));
    }


    // HttpMessageNotReadableException은 요청 본문을 읽을 수 없거나, JSON 형식이 잘못되었을 때 발생합니다. 이 예외가 발생하면, 클라이언트에게 요청 형식 오류를 알리는 응답을 반환합니다.
    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ErrorResponse> handleUnreadableRequest(
            HttpMessageNotReadableException exception,
            HttpServletRequest request
    ) {
        return ResponseEntity.badRequest()
                .body(createResponse(
                        ErrorCode.INVALID_REQUEST,
                        "JSON 형식과 필드 값을 확인해 주세요.",
                        request.getRequestURI()
                ));
    }


    // Exception은 애플리케이션에서 예상하지 못한 오류가 발생했을 때 처리됩니다. 이 예외가 발생하면, 서버 내부 오류로 간주하고 클라이언트에게 500 상태 코드와 함께 일반적인 오류 메시지를 반환합니다. 또한, 스택 트레이스를 로그에 기록하여 문제의 원인을 추적할 수 있도록 합니다.
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleUnexpectedException(
            Exception exception,
            HttpServletRequest request
    ) {
        // 예상하지 못한 오류는 원인을 추적할 수 있도록 반드시 스택 트레이스와 함께 기록합니다.
        // 이 로그가 없으면 500 오류의 원인을 찾을 방법이 없습니다.
        log.error("Unexpected exception at {}", request.getRequestURI(), exception);
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(createResponse(
                        ErrorCode.INTERNAL_ERROR,
                        ErrorCode.INTERNAL_ERROR.getMessage(),
                        request.getRequestURI()
                ));
    }

    // createResponse 메서드는 ErrorCode와 메시지, 요청 경로를 기반으로 ErrorResponse 객체를 생성합니다. 이 객체는 클라이언트에게 반환될 오류 응답의 구조를 정의하며, 타임스탬프, HTTP 상태 코드, 오류 코드, 메시지, 요청 경로를 포함합니다.
    // 취합해서 메세지 보내는 기능
    private ErrorResponse createResponse(ErrorCode errorCode, String message, String path) {
        return new ErrorResponse(
                LocalDateTime.now(),
                errorCode.getStatus().value(),
                errorCode.getCode(),
                message,
                path
        );
    }
}