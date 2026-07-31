package com.example.test.demo.service;

import com.example.test.demo.dto.CourseResponse;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class CourseService {

    public CourseResponse createCourse(String name, List<String> topics) {
        String description =
                name + " 과정은 " + String.join(", ", topics) + "을 학습합니다.";

        return new CourseResponse(name, topics, description);
    }
}