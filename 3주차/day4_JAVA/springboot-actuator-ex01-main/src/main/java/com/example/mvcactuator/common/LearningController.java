package com.example.mvcactuator.common;

import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/learning")
public class LearningController {

    @GetMapping("/hello")
    public Map<String, String> hello() {
        // Map 객체는 JSON 객체로 변환되어 응답됩니다.
        return Map.of("message", "Spring MVC 실행 성공");
    }

    @GetMapping("/greeting")
    public Map<String, String> greeting(
            @RequestParam(defaultValue = "수강생") String name) {
        return Map.of("message", name + "님, 반갑습니다.");
    }
}
