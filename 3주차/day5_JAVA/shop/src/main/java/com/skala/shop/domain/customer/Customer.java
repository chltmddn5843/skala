package com.skala.shop.domain.customer;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "customers")
public class Customer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "customer_id", nullable = false, unique = true, length = 20)
    private String customerId;

    @Column(nullable = false, length = 100)
    private String password;

    @Column(nullable = false)
    private long point;

    protected Customer() {
    }

    public Customer(String customerId, String password, long point) {
        this.customerId = customerId;
        this.password = password;
        this.point = point;
    }

    public void usePoint(long amount) {
        this.point -= amount;
    }

    public void refundPoint(long amount) {
        this.point += amount;
    }

    public Long getId() {
        return id;
    }

    public String getCustomerId() {
        return customerId;
    }

    public String getPassword() {
        return password;
    }

    public long getPoint() {
        return point;
    }
}