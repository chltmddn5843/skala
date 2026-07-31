package com.skala.stock.aop;

import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

@Aspect      // "이 클래스는 다른 코드 실행에 끼어드는 역할(Aspect)"이라는 표시
@Component   // Bean으로 등록 — 등록 안 하면 스프링이 이 클래스의 존재를 모름!
@Slf4j       // Lombok이 log 객체를 자동으로 만들어 줌 → log.info(...) 사용 가능
public class LoggingAspect {

    // execution(...) 해석:
    //   *                              → 반환 타입 무관
    //   com.skala.stock.service.*     → service 패키지의 모든 클래스
    //   .*(..)                        → 모든 메서드, 파라미터 무관
    // 즉, "Service의 모든 메서드가 실행될 때 아래 코드를 감싸라"
    @Around("execution(* com.skala.stock.service.*.*(..))")
    public Object logExecution(ProceedingJoinPoint joinPoint) throws Throwable {

        // 지금 실행되려는 메서드 이름 (예: StockService.getStockById(..))
        String methodName = joinPoint.getSignature().toShortString();

        log.info(">>> 시작: {}", methodName);

        Object result = joinPoint.proceed();   // ★ 원래 메서드를 실제로 실행하는 지점!
                                               //   이 줄이 없으면 진짜 로직이 실행되지 않음

        log.info("<<< 종료: {}", methodName);

        return result;   // 원래 메서드의 반환값을 그대로 돌려줌
    }
}