package com.skala.shop.service;

import com.skala.shop.domain.cart.CartItem;
import com.skala.shop.domain.cart.CartItemRepository;
import com.skala.shop.domain.customer.Customer;
import com.skala.shop.domain.customer.CustomerRepository;
import com.skala.shop.domain.product.Product;
import com.skala.shop.domain.product.ProductRepository;
import com.skala.shop.dto.cart.CartItemRequest;
import com.skala.shop.dto.cart.CartItemResponse;
import com.skala.shop.dto.cart.CartResponse;
import com.skala.shop.exception.BusinessException;
import com.skala.shop.exception.ErrorCode;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@Transactional(readOnly = true)
public class CartService {

    private final CartItemRepository cartItemRepository;
    private final CustomerRepository customerRepository;
    private final ProductRepository productRepository;

    public CartService(CartItemRepository cartItemRepository,
                       CustomerRepository customerRepository,
                       ProductRepository productRepository) {
        this.cartItemRepository = cartItemRepository;
        this.customerRepository = customerRepository;
        this.productRepository = productRepository;
    }

    public CartResponse getMyCart(String customerId) {
        Customer customer = getCustomer(customerId);
        List<CartItem> cartItems = cartItemRepository.findAllByCustomer(customer);

        List<CartItemResponse> itemResponses = cartItems.stream()
                .map(CartItemResponse::from)
                .toList();

        long totalPrice = itemResponses.stream()
                .mapToLong(CartItemResponse::itemTotalPrice)
                .sum();

        return new CartResponse(itemResponses, totalPrice);
    }

    @Transactional
    public void addCartItem(String customerId, CartItemRequest request) {
        Customer customer = getCustomer(customerId);
        Product product = getProduct(request.productId());

        CartItem cartItem = cartItemRepository.findByCustomerAndProduct(customer, product)
                .orElseGet(() -> new CartItem(customer, product, 0));

        cartItem.addQuantity(request.quantity());
        cartItemRepository.save(cartItem);
    }

    @Transactional
    public void deleteCartItem(String customerId, Long cartItemId) {
        Customer customer = getCustomer(customerId);
        CartItem cartItem = cartItemRepository.findById(cartItemId)
                .orElseThrow(() -> new BusinessException(ErrorCode.ORDER_NOT_FOUND));

            if (!cartItem.getCustomer().getCustomerId().equals(customerId)) {
                throw new BusinessException(ErrorCode.ORDER_NOT_FOUND); // 본인 장바구니 항목이 아니면 찾을 수 없는 것으로 처리
            }

        cartItemRepository.delete(cartItem);
    }

    private Customer getCustomer(String customerId) {
        return customerRepository.findByCustomerId(customerId)
                .orElseThrow(() -> new BusinessException(ErrorCode.CUSTOMER_NOT_FOUND));
    }

    private Product getProduct(Long productId) {
        return productRepository.findById(productId)
                .orElseThrow(() -> new BusinessException(ErrorCode.PRODUCT_NOT_FOUND));
    }
}