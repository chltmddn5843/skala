package com.example.mvcactuator.monitoring;

import org.springframework.stereotype.Component;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;

@Component
public class ProductMetrics {

    private final Counter productCreatedCounter;

    public ProductMetrics(MeterRegistry registry) {
        this.productCreatedCounter = Counter
                .builder("product.created.total")
                .description("생성된 상품 수")
                .register(registry);
    }

    public void recordCreated() {
        productCreatedCounter.increment();
    }
}