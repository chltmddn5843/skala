# ── 1) 빌드 스테이지: Gradle + JDK 21 로 JAR 를 만든다 ──────────────
FROM gradle:8.14-jdk21 AS build
WORKDIR /app

# 소스 전체를 복사한 뒤 빌드 (-x test: 실습 편의상 테스트 생략)
COPY . .
RUN gradle clean build -x test

# ── 2) 실행 스테이지: 경량 JRE 이미지에 JAR 만 복사한다 ──────────────
FROM eclipse-temurin:21-jre
WORKDIR /app

# --from=build : 1단계(빌드 스테이지)의 산출물만 가져온다
COPY --from=build /app/build/libs/skala-shop-api-0.0.1-SNAPSHOT.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]