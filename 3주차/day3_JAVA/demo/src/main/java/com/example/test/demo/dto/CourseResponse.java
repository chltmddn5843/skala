package com.example.test.demo.dto;
import java.util.List;

public record CourseResponse(
        String name,
        List<String> topics,
        String description
) {
}