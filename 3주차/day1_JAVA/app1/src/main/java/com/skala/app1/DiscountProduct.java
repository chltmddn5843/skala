package com.skala.app1;

public class DiscountProduct extends Product {
    private int rate;

    public DiscountProduct(String n, int p, int r) {
        super(n, p);
        this.rate = r;
    }

    @Override
    public int getPrice() {
        return super.getPrice() * (100 - rate) / 100;
    }
}
