package com.skala.shop.service;

import com.skala.shop.domain.customer.Customer;
import com.skala.shop.domain.customer.CustomerRepository;
import com.skala.shop.dto.customer.LoginRequest;
import com.skala.shop.dto.customer.LoginResponse;
import com.skala.shop.dto.customer.SignUpRequest;
import com.skala.shop.dto.customer.SignUpResponse;
import com.skala.shop.exception.BusinessException;
import com.skala.shop.exception.ErrorCode;
import com.skala.shop.security.JwtTokenProvider;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
public class AuthService {

    private static final long INITIAL_POINT = 1_000_000L;

    private final CustomerRepository customerRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider jwtTokenProvider;
    private final long expirationMinutes;

    public AuthService(
            CustomerRepository customerRepository,
            PasswordEncoder passwordEncoder,
            JwtTokenProvider jwtTokenProvider,
            @Value("${jwt.expiration-minutes}") long expirationMinutes
    ) {
        this.customerRepository = customerRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtTokenProvider = jwtTokenProvider;
        this.expirationMinutes = expirationMinutes;
    }

    @Transactional
    public SignUpResponse signUp(SignUpRequest request) {
        if (customerRepository.existsByCustomerId(request.customerId())) {
            throw new BusinessException(ErrorCode.DUPLICATE_CUSTOMER_ID);
        }
        Customer customer = new Customer(
                request.customerId(),
                passwordEncoder.encode(request.password()),
                INITIAL_POINT
        );
        customerRepository.save(customer);
        return new SignUpResponse(
                customer.getCustomerId(),
                customer.getPoint(),
                "회원가입이 완료되었습니다."
        );
    }

    public LoginResponse login(LoginRequest request) {
        Customer customer = customerRepository.findByCustomerId(request.customerId())
                .orElseThrow(() -> new BusinessException(ErrorCode.INVALID_CREDENTIALS));
        if (!passwordEncoder.matches(request.password(), customer.getPassword())) {
            throw new BusinessException(ErrorCode.INVALID_CREDENTIALS);
        }
        String token = jwtTokenProvider.generateToken(customer.getCustomerId());
        return new LoginResponse(token, "Bearer", expirationMinutes);
    }
}