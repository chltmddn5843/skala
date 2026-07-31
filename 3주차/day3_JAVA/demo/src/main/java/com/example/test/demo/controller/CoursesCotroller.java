package com.example.test.demo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


@RestController
@RequestMapping("/courses")
public class CoursesCotroller {
    @GetMapping("/courses")
    public String getCourses() {
        return "강좌 목록";
    }
}
