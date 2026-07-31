package com.example.mvcactuator.product;

import java.util.List;

import org.springframework.stereotype.Service;

import com.example.mvcactuator.monitoring.ProductMetrics;

@Service
public class ProductService {

    private final ProductRepository repository;
    private final ProductMetrics metrics;

    // 생성자가 하나이면 @Autowired를 생략할 수 있습니다.
    public ProductService(ProductRepository repository, ProductMetrics metrics) {
        this.repository = repository;
        this.metrics = metrics;
    }

    public List<Product> findAll(String keyword) {
        List<Product> products = repository.findAll();

        if (keyword == null || keyword.isBlank()) {
            return products;
        }

        return products.stream()
                .filter(product -> product.name().contains(keyword))
                .toList();
    }

    public Product findById(Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new ProductNotFoundException(id));
    }

    public Product create(ProductRequest request) {
        Product created = repository.save(
                new Product(null, request.name(), request.price()));
        metrics.recordCreated();
        return created;
    }

    public Product update(Long id, ProductRequest request) {
        findById(id); // 존재하지 않으면 예외 발생
        return repository.save(
                new Product(id, request.name(), request.price()));
    }

    public void delete(Long id) {
        if (!repository.deleteById(id)) {
            throw new ProductNotFoundException(id);
        }
    }

    public long count() {
        return repository.count();
    }
}