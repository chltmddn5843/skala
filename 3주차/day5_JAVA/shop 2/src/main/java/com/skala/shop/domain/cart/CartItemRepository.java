package com.skala.shop.domain.cart;

import com.skala.shop.domain.customer.Customer;
import com.skala.shop.domain.product.Product;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface CartItemRepository extends JpaRepository<CartItem, Long> {
    List<CartItem> findAllByCustomer(Customer customer);
    Optional<CartItem> findByCustomerAndProduct(Customer customer, Product product);
    void deleteByCustomer(Customer customer);
}