package com.skala.stock.service;

import com.skala.stock.dto.DailyTransaction;
import com.skala.stock.dto.PortfolioDto;
import com.skala.stock.dto.TradeSnapshotDto;
import com.skala.stock.dto.TransactionDto;
import com.skala.stock.dto.TransactionStatistics;
import com.skala.stock.entity.User;
import com.skala.stock.repository.TransactionRepository;
import com.skala.stock.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)   // 분석은 전부 "조회"이므로 클래스 전체 읽기 전용 적용
public class StockAnalysisService {

    private final PortfolioService portfolioService;
    private final TransactionService transactionService;
    private final UserRepository userRepository;
    private final TransactionRepository transactionRepository;   // @Query 호출용

    /** [분석 1] 포트폴리오 평가 손익
     * — getUserPortfolio의 convertToDto가 이미 profitLoss를 계산함 */
    public List<PortfolioDto> getPortfolioProfitLoss(Long userId) {
        return portfolioService.getUserPortfolio(userId);
    }

    /** [분석 2] 거래 내역 상세 조회 (사용자의 전체 거래) */
    public List<TransactionDto> getTransactionDetails(Long userId) {
        return transactionService.getUserTransactions(userId);
    }

    /** [분석 3] 특정 주식 거래 내역 조회 */
    public List<TransactionDto> getStockTransactions(Long stockId) {
        return transactionService.getStockTransactions(stockId);
    }

    /** [분석 4] 총 자산 = 현금 잔액 + 보유 주식 평가액의 합 */
    public TradeSnapshotDto getTotalAssets(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("사용자를 찾을 수 없습니다: " + userId));

        // 보유 종목들의 평가액(totalValue = 수량 × 현재가)을 전부 더한다
        Long stockValue = portfolioService.getUserPortfolio(userId).stream()
                .mapToLong(PortfolioDto::getTotalValue)   // 각 항목에서 totalValue만 추출
                .sum();                                   // 합산

        return TradeSnapshotDto.builder()
                .userId(userId)
                .totalAssets(user.getBalance() + stockValue)
                .build();
    }

    /** [분석 5] 총 수익률(%) = 평가손익 합 ÷ 투자원금 합 × 100 */
    public TradeSnapshotDto getTotalReturnRate(Long userId) {
        List<PortfolioDto> portfolios = portfolioService.getUserPortfolio(userId);

        // 투자원금 = Σ(수량 × 평단가), 평가손익 = Σ(profitLoss)
        long invested = portfolios.stream()
                .mapToLong(p -> p.getQuantity() * p.getAveragePrice())
                .sum();
        long profitLoss = portfolios.stream()
                .mapToLong(PortfolioDto::getProfitLoss)
                .sum();

        // ★ 방어 코드: 보유 주식이 없으면 invested가 0 → 0으로 나누면 ArithmeticException 발생!
        double rate = (invested == 0) ? 0.0 : (profitLoss * 100.0) / invested;

        return TradeSnapshotDto.builder()
                .userId(userId)
                .totalReturnRate(Math.round(rate * 100) / 100.0)   // 소수 둘째 자리 반올림
                .build();
    }

    /** [분석 6] 종목별 거래 통계 — Repository의 @Query가 실행됨 */
    public List<TransactionStatistics> getTransactionStatistics() {
        return transactionRepository.getTransactionStatistics();
    }

    /** [분석 7] 일별 거래 내역 */
    public List<DailyTransaction> getDailyTransactions() {
        return transactionRepository.getDailyTransactions();
    }
}