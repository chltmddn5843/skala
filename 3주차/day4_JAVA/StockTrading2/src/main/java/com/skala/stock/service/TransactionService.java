package com.skala.stock.service;

import com.skala.stock.dto.TradeRequestDto;
import com.skala.stock.dto.TransactionDto;
import com.skala.stock.entity.Portfolio;
import com.skala.stock.entity.Stock;
import com.skala.stock.entity.Transaction;
import com.skala.stock.entity.User;
import com.skala.stock.repository.StockRepository;
import com.skala.stock.repository.TransactionRepository;
import com.skala.stock.repository.UserRepository;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class TransactionService {

    private final TransactionRepository transactionRepository;
    private final UserRepository userRepository;         // 거래 시 잔액 차감/입금용
    private final StockRepository stockRepository;       // 현재가 조회용
    private final PortfolioService portfolioService;     // 포트폴리오 업데이트 부품

    /** [CRUD 7] 특정 사용자의 전체 거래 내역 조회 */
    public List<TransactionDto> getUserTransactions(Long userId) {
        List<Transaction> transactions = transactionRepository.findByUserIdOrderByTransactionDateDesc(userId);
        return transactions.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    /** [CRUD 8] 매수/매도 실행 — 잔액·포트폴리오·거래내역이 "한 묶음"으로 처리된다 */
    @Transactional
    public TransactionDto executeTrade(TradeRequestDto request) {

        // 1단계: 사용자 및 종목 조회
        User user = userRepository.findById(request.getUserId())
                .orElseThrow(() -> new RuntimeException("사용자를 찾을 수 없습니다: " + request.getUserId()));
        Stock stock = stockRepository.findById(request.getStockId())
                .orElseThrow(() -> new RuntimeException("주식을 찾을 수 없습니다: " + request.getStockId()));

        Long price = stock.getCurrentPrice();               // 거래 가격 = 현재가
        Long totalAmount = price * request.getQuantity();   // 총 거래 금액

        // 2단계: 매수 / 매도 분기
        if (request.getType() == Transaction.TransactionType.BUY) {

            // [매수 검증] 잔액 확인
            if (user.getBalance() < totalAmount) {
                throw new RuntimeException("잔액이 부족합니다. 필요: " + totalAmount
                        + "원, 보유: " + user.getBalance() + "원");
            }

            user.setBalance(user.getBalance() - totalAmount);   // 잔액 차감

            // Entity 원본 조회 후 포트폴리오 갱신
            Portfolio existing = portfolioService.findPortfolioEntity(user.getId(), stock.getId());
            if (existing == null) {
                portfolioService.addToPortfolio(user, stock, request.getQuantity(), price);   // 신규 추가
            } else {
                portfolioService.updatePortfolio(existing, request.getQuantity(), price);     // 수량/평단가 갱신
            }

        } else {   // SELL (매도)

            // [매도 검증] 보유 수량 확인
            Portfolio existing = portfolioService.findPortfolioEntity(user.getId(), stock.getId());
            if (existing == null || existing.getQuantity() < request.getQuantity()) {
                throw new RuntimeException("보유 수량이 부족합니다");
            }

            user.setBalance(user.getBalance() + totalAmount);   // 판매 금액 입금
            portfolioService.removeFromPortfolio(existing, request.getQuantity());
        }

        // 3단계: 거래 내역 저장
        Transaction transaction = Transaction.builder()
                .user(user)
                .stock(stock)
                .type(request.getType())
                .quantity(request.getQuantity())
                .price(price)
                .totalAmount(totalAmount)
                .build();

        Transaction saved = transactionRepository.save(transaction);
        return convertToDto(saved);
    }

    private TransactionDto convertToDto(Transaction transaction) {
        return TransactionDto.builder()
                .id(transaction.getId())
                .userId(transaction.getUser().getId())
                .username(transaction.getUser().getUsername())
                .stockId(transaction.getStock().getId())
                .stockCode(transaction.getStock().getCode())
                .stockName(transaction.getStock().getName())
                .type(transaction.getType())
                .quantity(transaction.getQuantity())
                .price(transaction.getPrice())
                .totalAmount(transaction.getTotalAmount())
                .transactionDate(transaction.getTransactionDate())
                .createdAt(transaction.getCreatedAt())
                .build();
    }
    /** [CRUD 7] 거래 1건 상세 조회 */
    public TransactionDto getTransactionById(Long id) {
        Transaction transaction = transactionRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("거래를 찾을 수 없습니다: " + id));
        return convertToDto(transaction);
    }

    /** [분석 8] 특정 사용자의 특정 주식 거래 내역 */
    public List<TransactionDto> getUserStockTransactions(Long userId, Long stockId) {
// Repository에 이미 준비된 메서드! 이름을 읽어보세요:
// "userId 그리고 stockId로 찾고, 거래일(TransactionDate) 내림차순(Desc) 정렬"
// — 메서드 이름이 곧 쿼리. JPA가 이름을 해석해 SQL을 자동으로 만든다
        List<Transaction> transactions = transactionRepository
                .findByUserIdAndStockIdOrderByTransactionDateDesc(userId, stockId);
        return transactions.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }
    /** [분석 3] 특정 주식의 전체 거래 내역 (모든 사용자의 거래) */
    public List<TransactionDto> getStockTransactions(Long stockId) {
        return transactionRepository.findByStockIdOrderByTransactionDateDesc(stockId)
                .stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }
}