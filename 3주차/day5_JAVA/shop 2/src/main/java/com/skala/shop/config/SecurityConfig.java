package com.skala.shop.config;

import com.skala.shop.security.JwtAuthenticationFilter;
import com.skala.shop.security.RestAuthenticationEntryPoint;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtAuthenticationFilter;
    private final RestAuthenticationEntryPoint authenticationEntryPoint;

    public SecurityConfig(
            JwtAuthenticationFilter jwtAuthenticationFilter,
            RestAuthenticationEntryPoint authenticationEntryPoint
    ) {
        this.jwtAuthenticationFilter = jwtAuthenticationFilter;
        this.authenticationEntryPoint = authenticationEntryPoint;
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(AbstractHttpConfigurer::disable)
            .sessionManagement(session -> session
                    .sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(authorize -> authorize
                    .requestMatchers("/api/health").permitAll()
                    
                    // 🚨 Swagger UI 및 API Docs 경로 전체 접근 허용 추가
                    .requestMatchers(
                            "/v3/api-docs/**",
                            "/v3/api-docs",
                            "/swagger-ui/**",
                            "/swagger-ui.html",
                            "/swagger-resources/**",
                            "/webjars/**"
                    ).permitAll()

                    // 실습 편의를 위해 상품 API 전체를 공개합니다.
                    .requestMatchers("/api/products/**").permitAll()
                    // 회원가입과 로그인은 POST 요청만 공개합니다.
                    .requestMatchers(HttpMethod.POST, "/api/customers").permitAll()
                    .requestMatchers(HttpMethod.POST, "/api/customers/login").permitAll()
                    .anyRequest().authenticated())
            .exceptionHandling(exception -> exception
                    .authenticationEntryPoint(authenticationEntryPoint))
            .addFilterBefore(
                    jwtAuthenticationFilter,
                    UsernamePasswordAuthenticationFilter.class
            );
        return http.build();
    }
}