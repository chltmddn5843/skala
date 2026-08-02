package com.skala.shop;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;


// ShopApplication 클래스는 Spring Boot 애플리케이션의 진입점으로, main 메서드를 통해 애플리케이션을 실행합니다. @SpringBootApplication 어노테이션은 스프링 부트의 자동 설정, 컴포넌트 스캔 등을 활성화하여 개발자가 최소한의 설정으로 애플리케이션을 시작할 수 있도록 도와줍니다.

//
@SpringBootApplication
public class ShopApplication {

	public static void main(String[] args) {
		SpringApplication.run(ShopApplication.class, args);
	}

}
