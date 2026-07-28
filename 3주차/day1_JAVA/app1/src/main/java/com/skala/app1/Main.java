package com.skala.app1;

public class Main {
    public static void main(String[] args){
        Product normalItem = new Product("노말 아이템", 10000);
        DiscountProduct discountItem = new DiscountProduct("할인 아이템", 10000, 20);

        System.out.println(normalItem.getPrice());
        System.out.println(discountItem.getPrice());
    }
}
