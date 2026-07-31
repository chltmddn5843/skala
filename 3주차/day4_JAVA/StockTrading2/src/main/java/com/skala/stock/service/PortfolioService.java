package com.skala.stock.service;

import com.skala.stock.dto.PortfolioDto;
import com.skala.stock.entity.Portfolio;
import com.skala.stock.entity.Stock;
import com.skala.stock.entity.User;
import com.skala.stock.repository.PortfolioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class PortfolioService {

    private final PortfolioRepository portfolioRepository;

    /** [조회] 특정 사용자의 전체 포트폴리오 목록 조회 */
    public List<PortfolioDto> getUserPortfolio(Long userId) {
        List<Portfolio> portfolios = portfolioRepository.findByUserId(userId);
        return portfolios.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }
    /** [CRUD 9] 특정 사용자의 특정 종목 보유 현황 조회 */
    public PortfolioDto getUserStockPortfolio(Long userId, Long stockId) {
        Portfolio portfolio = portfolioRepository.findByUserIdAndStockId(userId, stockId)
                .orElseThrow(() -> new RuntimeException("보유하지 않은 종목입니다"));
        return convertToDto(portfolio);
// convertToDto가 평가액(totalValue)과 손익(profitLoss)까지 계산해 줌
// — 파일 아래쪽의 convertToDto를 열어 어떻게 계산하는지 꼭 읽어보세요! (분석 1에서 재활용됨)
    }
    /** [조회 API용] 특정 종목 보유 정보 DTO 반환 */
    public PortfolioDto findPortfolioDto(Long userId, Long stockId) {
        return portfolioRepository.findByUserIdAndStockId(userId, stockId)
                .map(this::convertToDto)
                .orElse(null);
    }

    /** [내부 로직용] TransactionService 매매 실행 시 사용하는 Entity 원본 조회 */
    public Portfolio findPortfolioEntity(Long userId, Long stockId) {
        return portfolioRepository.findByUserIdAndStockId(userId, stockId)
                .orElse(null);
    }

    /** [부품 1: 매수-신규] 처음 사는 종목 → 포트폴리오에 새로 추가 */
    @Transactional
    public void addToPortfolio(User user, Stock stock, Long quantity, Long price) {
        Portfolio portfolio = Portfolio.builder()
                .user(user)
                .stock(stock)
                .quantity(quantity)
                .averagePrice(price)
                .build();
        portfolioRepository.save(portfolio);
    }

    /** [부품 2: 매수-추가] 이미 보유한 종목을 더 산다 → 수량과 평단가 갱신 */
    @Transactional
    public void updatePortfolio(Portfolio existing, Long quantity, Long price) {
        Long oldTotal = existing.getQuantity() * existing.getAveragePrice();
        Long newTotal = quantity * price;
        Long totalQuantity = existing.getQuantity() + quantity;

        existing.setAveragePrice((oldTotal + newTotal) / totalQuantity);
        existing.setQuantity(totalQuantity);
        portfolioRepository.save(existing);
    }

    /** [부품 3: 매도] 수량 차감, 전량 매도면 목록에서 삭제 */
    @Transactional
    public void removeFromPortfolio(Portfolio existing, Long quantity) {
        Long remaining = existing.getQuantity() - quantity;

        if (remaining == 0) {
            portfolioRepository.delete(existing);   // 전량 매도 시 제거
        } else {
            existing.setQuantity(remaining);        // 일부 매도 시 수량 변경
            portfolioRepository.save(existing);
        }
    }

    private PortfolioDto convertToDto(Portfolio portfolio) {
        Stock stock = portfolio.getStock();
        Long currentPrice = stock.getCurrentPrice();
        Long totalValue = portfolio.getQuantity() * currentPrice;
        Long profitLoss = totalValue - (portfolio.getQuantity() * portfolio.getAveragePrice());

        return PortfolioDto.builder()
                .id(portfolio.getId())
                .userId(portfolio.getUser().getId())
                .username(portfolio.getUser().getUsername())
                .stockId(stock.getId())
                .stockCode(stock.getCode())
                .stockName(stock.getName())
                .quantity(portfolio.getQuantity())
                .averagePrice(portfolio.getAveragePrice())
                .currentPrice(currentPrice)
                .totalValue(totalValue)
                .profitLoss(profitLoss)
                .build();
    }
}