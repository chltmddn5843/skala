package com.example.mvcactuator.monitoring;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.example.mvcactuator.product.ProductService;

import io.micrometer.core.instrument.Gauge;
import io.micrometer.core.instrument.binder.MeterBinder;

@Configuration(proxyBeanMethods = false)
public class MetricsConfig {

    @Bean
    MeterBinder productCurrentCount(ProductService productService) {
        return registry -> Gauge
                .builder("product.current.count", productService,
                        service -> service.count())
                .description("현재 저장된 상품 수")
                .register(registry);
    }
}