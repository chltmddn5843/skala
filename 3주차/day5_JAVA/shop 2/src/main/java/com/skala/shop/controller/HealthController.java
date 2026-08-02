package com.skala.shop.controller;

import java.util.Map; // Map.of()를 사용하기 위해 필요
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
// 필요한 라이브러리 import

@RestController // json response
@RequestMapping("/api/health") // 기본 주소 health
public class HealthController {
    
    @GetMapping // get 요청
    public Map<String, String> health() {
        return Map.of("status", "UP", "application", "skala-shop-api");
    }
}