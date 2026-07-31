package com.example.mvcactuator.monitoring;

import org.springframework.boot.health.contributor.Health;
import org.springframework.boot.health.contributor.HealthIndicator;
import org.springframework.stereotype.Component;

import com.example.mvcactuator.product.ProductRepository;

@Component("productStore")
public class ProductStoreHealthIndicator implements HealthIndicator {

    private final ProductRepository repository;

    public ProductStoreHealthIndicator(ProductRepository repository) {
        this.repository = repository;
    }

    @Override
    public Health health() {
        try {
            return Health.up()
                    .withDetail("productCount", repository.count())
                    .withDetail("storage", "in-memory")
                    .build();
        } catch (Exception exception) {
            return Health.down(exception).build();
        }
    }
}