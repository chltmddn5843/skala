package com.skala.shop.service;

import com.skala.shop.domain.product.Product;
import com.skala.shop.domain.product.ProductRepository;
import com.skala.shop.dto.product.ProductRequest;
import com.skala.shop.dto.product.ProductResponse;
import com.skala.shop.exception.BusinessException;
import com.skala.shop.exception.ErrorCode;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
@Transactional(readOnly = true)
public class ProductService {
    private static final Logger log = LoggerFactory.getLogger(ProductService.class);

    private final ProductRepository productRepository;

    public ProductService(ProductRepository productRepository) {
        // 생성자 주입을 사용하면 Service 가 저장소 구현을 직접 만들지 않습니다.
        this.productRepository = productRepository;
    }

    public List<ProductResponse> findAll() {
        return productRepository.findAll().stream()
                .map(ProductResponse::from)
                .toList();
    }

    public ProductResponse findById(Long id) {
        // {} 는 자리표시자: 문자열 덧셈(+)과 달리, 이 레벨이 꺼져 있으면
        // 문자열을 만드는 비용 자체가 발생하지 않아 성능에 유리합니다.
        log.debug("상품 단건 조회 요청: id={}", id);
        return ProductResponse.from(getProduct(id));
    }

    @Transactional
    public ProductResponse create(ProductRequest request) {
        // INFO: "무슨 작업이 일어났는지" 를 기록 (누가/무엇을)
        log.info("상품 등록: name={}, price={}", request.name(), request.price());
        Product product = new Product(request.name(), request.price());
        return ProductResponse.from(productRepository.save(product));
    }

    @Transactional
    public ProductResponse update(Long id, ProductRequest request) {
        log.info("상품 수정: id={}, name={}, price={}", id, request.name(), request.price());
        Product product = getProduct(id);
        product.update(request.name(), request.price());
        return ProductResponse.from(product);
    }

    @Transactional
    public void delete(Long id) {
        log.info("상품 삭제: id={}", id);
        Product product = getProduct(id);
        productRepository.delete(product);
    }

    private Product getProduct(Long id) {
        return productRepository.findById(id)
                .orElseThrow(() -> new BusinessException(ErrorCode.PRODUCT_NOT_FOUND));
    }
}
