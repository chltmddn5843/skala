package com.example.mvcactuator.monitoring;

import java.util.Map;

import org.springframework.boot.actuate.info.Info;
import org.springframework.boot.actuate.info.InfoContributor;
import org.springframework.stereotype.Component;

@Component
public class ProductInfoContributor implements InfoContributor {

    @Override
    public void contribute(Info.Builder builder) {
        builder.withDetail("application", Map.of(
                "name", "MVC Actuator Lab",
                "version", "1.0",
                "purpose", "Spring MVC and Actuator practice"));
    }
}