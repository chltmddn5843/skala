package com.skala.shop.service;

import com.skala.shop.domain.customer.Customer;
import com.skala.shop.domain.customer.CustomerRepository;
import com.skala.shop.domain.order.OrderItem;
import com.skala.shop.domain.order.OrderItemRepository;
import com.skala.shop.domain.product.Product;
import com.skala.shop.domain.product.ProductRepository;
import com.skala.shop.dto.order.CustomerOrderResponse;
import com.skala.shop.dto.order.OrderItemResponse;
import com.skala.shop.dto.order.OrderRequest;
import com.skala.shop.dto.order.OrderResultResponse;
import com.skala.shop.exception.BusinessException;
import com.skala.shop.exception.ErrorCode;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
public class OrderService {

    private final CustomerRepository customerRepository;
    private final ProductRepository productRepository;
    private final OrderItemRepository orderItemRepository;

    public OrderService(
            CustomerRepository customerRepository,
            ProductRepository productRepository,
            OrderItemRepository orderItemRepository
    ) {
        this.customerRepository = customerRepository;
        this.productRepository = productRepository;
        this.orderItemRepository = orderItemRepository;
    }

    public CustomerOrderResponse findMyOrders(String customerId) {
        Customer customer = getCustomer(customerId);
        List<OrderItemResponse> orders = orderItemRepository.findAllByCustomer(customer).stream()
                .map(OrderItemResponse::from)
                .toList();
        return new CustomerOrderResponse(customer.getCustomerId(), customer.getPoint(), orders);
    }

    @Transactional
    public OrderResultResponse placeOrder(String customerId, OrderRequest request) {
        Customer customer = getCustomer(customerId);
        Product product = getProduct(request.productId());
        long orderPrice = Math.multiplyExact(product.getPrice(), (long) request.quantity());
        if (customer.getPoint() < orderPrice) {
            throw new BusinessException(ErrorCode.INSUFFICIENT_FUNDS);
        }
        // 포인트 차감과 주문 수량 변경은 하나의 트랜잭션으로 함께 처리합니다.
        customer.usePoint(orderPrice);
        OrderItem orderItem = orderItemRepository.findByCustomerAndProduct(customer, product)
                .orElseGet(() -> new OrderItem(customer, product, 0));
        orderItem.addQuantity(request.quantity());
        orderItemRepository.save(orderItem);
        return new OrderResultResponse(
                "상품 주문이 완료되었습니다.",
                customer.getPoint(),
                product.getId(),
                product.getName(),
                orderItem.getQuantity()
        );
    }

    @Transactional
    public OrderResultResponse cancelOrder(String customerId, OrderRequest request) {
        Customer customer = getCustomer(customerId);
        Product product = getProduct(request.productId());
        OrderItem orderItem = orderItemRepository.findByCustomerAndProduct(customer, product)
                .orElseThrow(() -> new BusinessException(ErrorCode.ORDER_NOT_FOUND));
        if (orderItem.getQuantity() < request.quantity()) {
            throw new BusinessException(ErrorCode.INSUFFICIENT_QUANTITY);
        }
        long refundPrice = Math.multiplyExact(product.getPrice(), (long) request.quantity());
        orderItem.decreaseQuantity(request.quantity());
        customer.refundPoint(refundPrice);
        int remainingQuantity = orderItem.getQuantity();
        if (remainingQuantity == 0) {
            orderItemRepository.delete(orderItem);
        }
        return new OrderResultResponse(
                "주문 취소가 완료되었습니다.",
                customer.getPoint(),
                product.getId(),
                product.getName(),
                remainingQuantity
        );
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