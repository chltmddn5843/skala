package com.example.mvcactuator.product;

import java.util.List;
import java.util.Optional;

public interface ProductRepository {

    List<Product> findAll();

    Optional<Product> findById(Long id);

    Product save(Product product);

    boolean deleteById(Long id);

    long count();
}