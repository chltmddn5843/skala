package com.example.mvcactuator.product;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.stereotype.Repository;

@Repository
public class MemoryProductRepository implements ProductRepository {

    private final Map<Long, Product> store = new ConcurrentHashMap<>();
    private final AtomicLong sequence = new AtomicLong();

    public MemoryProductRepository() {
        save(new Product(null, "노트북", 1_500_000));
        save(new Product(null, "키보드", 120_000));
    }

    @Override
    public List<Product> findAll() {
        return new ArrayList<>(store.values());
    }

    @Override
    public Optional<Product> findById(Long id) {
        return Optional.ofNullable(store.get(id));
    }

    @Override
    public Product save(Product product) {
        Long id = product.id();

        // 새 상품은 서버에서 ID를 발급합니다.
        if (id == null) {
            id = sequence.incrementAndGet();
        }

        Product saved = new Product(id, product.name(), product.price());
        store.put(id, saved);
        return saved;
    }

    @Override
    public boolean deleteById(Long id) {
        return store.remove(id) != null;
    }

    @Override
    public long count() {
        return store.size();
    }
}