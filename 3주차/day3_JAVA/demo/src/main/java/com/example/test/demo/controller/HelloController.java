package com.example.test.demo.controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import com.example.test.demo.dto.HelloResponse;
import com.example.test.demo.service.HelloService;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {
    private final HelloService helloService;
    // 생성자를 이용해서 의존 주의
    public HelloController(HelloService helloService) {
    this.helloService = helloService;
    }
    // GET 방식으로 /hello?name=매개변수값 형식의 요청을 처리하는 메서드
    @GetMapping("/hello")
    public HelloResponse hello(@RequestParam(value = "name", defaultValue = "SKALA") String name) {
    return helloService.createMessage(name);

    }

}