package com.example.menu.service;

import org.springframework.stereotype.Service;

import java.util.List;
import java.util.concurrent.ThreadLocalRandom;

/**
 * 메뉴 추천 비즈니스 로직을 담당하는 Spring Bean입니다.
 *
 * @Service를 사용하면 Component Scan을 통해 Spring Container에
 * 자동으로 Bean으로 등록됩니다.
 */
@Service
public class MenuService {

    private final List<String> menus = List.of(
            "김치찌개",
            "불고기",
            "짜장면",
            "돈가스",
            "떡볶이",
            "치킨",
            "피자"
    );

    public String recommend() {
        return "김치찌개";
    }

    public String recommendByCategory(String category) {
        return switch (category) {
            case "korean" -> "불고기";
            case "chinese" -> "짜장면";
            case "japanese" -> "돈가스";
            case "snack" -> "떡볶이";
            default -> "추천 가능한 메뉴가 없습니다";
        };
    }

    public String randomMenu() {
        int index = ThreadLocalRandom.current().nextInt(menus.size());
        return menus.get(index);
    }

    public String recommendByWeather(String weather) {
        return switch (weather) {
            case "sunny" -> "샐러드";
            case "hot" -> "아이스크림";
            case "cold" -> "국밥";
            case "rainy" -> "라면";
            default -> "추천 가능한 메뉴가 없습니다";
        };
    }

    public String mood (String mood) {    
        return switch (mood) {
            case "happy" -> "치킨";
            case "sad" -> "아이스크림";
            case "tired" -> "피자";
            case "stressed" -> "초콜릿";
            default -> "추천 가능한 메뉴가 없습니다";
        };
    }

    public String recommendByPrice(int min, int max) {
        if (min > max) {
            return "최소 가격은 최대 가격보다 작아야 합니다.";
        } else if (max <= 6000) {
            return "추천 메뉴는 김치찌개입니다.";
        } else if (max <= 12000) {
            return "추천 메뉴는 불고기입니다.";
        } else {
            return "특별한 날에는 피자를 추천합니다.";
        }
    }

    public String recommendByCompanion(String companion) {
        return switch (companion) {
            case "solo" -> "김치찌개";
            case "friend" -> "치킨";
            case "family" -> "불고기";
            default -> "추천 가능한 메뉴가 없습니다";
        };
    }

}
