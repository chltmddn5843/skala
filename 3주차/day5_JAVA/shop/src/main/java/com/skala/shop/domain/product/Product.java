package com.skala.shop.domain.product;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "products")
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false)
    private long price;


// Product 클래스는 상품 정보를 나타내는 엔터티입니다. 이 클래스는 JPA를 사용하여 데이터베이스와 매핑되며, 상품의 ID, 이름, 가격을 속성으로 가집니다. 또한, 상품 정보를 생성하고 업데이트하는 메서드를 제공합니다.

// 위에 선언한거랑 아래 선언한 것의 차이는 뭐야



    protected Product() {
        // JPA 가 엔터티를 생성할 때 사용하는 기본 생성자입니다.
    }

    public Product(String name, long price) {
        this.name = name;
        this.price = price;
    }

    public void update(String name, long price) {
        this.name = name;
        this.price = price;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public long getPrice() {
        return price;
    }
}