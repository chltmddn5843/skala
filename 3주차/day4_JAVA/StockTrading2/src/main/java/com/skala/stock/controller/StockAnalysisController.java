package com.skala.stock.controller;

import com.skala.stock.dto.PortfolioDto;
import com.skala.stock.dto.TradeSnapshotDto;
import com.skala.stock.dto.TransactionDto;
import com.skala.stock.service.StockAnalysisService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.skala.stock.dto.DailyTransaction;
import com.skala.stock.dto.TransactionStatistics;
import java.util.List;

@RestController
@RequestMapping("/api/analysis")   // 분석 API의 공통 주소
@RequiredArgsConstructor
@Tag(name = "주식 분석", description = "포트폴리오/거래 분석 API")
public class StockAnalysisController {

    private final StockAnalysisService stockAnalysisService;

    @GetMapping("/portfolio/{userId}")            // [분석 1] GET /api/analysis/portfolio/1
    @Operation(summary = "포트폴리오 평가 손익", description = "보유 종목별 평가액과 손익을 조회합니다")
    public ResponseEntity<List<PortfolioDto>> getPortfolioProfitLoss(@PathVariable Long userId) {
        return ResponseEntity.ok(stockAnalysisService.getPortfolioProfitLoss(userId));
    }

    @GetMapping("/transactions/{userId}")         // [분석 2]
    @Operation(summary = "거래 내역 상세", description = "사용자의 전체 거래 내역을 상세 조회합니다")
    public ResponseEntity<List<TransactionDto>> getTransactionDetails(@PathVariable Long userId) {
        return ResponseEntity.ok(stockAnalysisService.getTransactionDetails(userId));
    }

    @GetMapping("/stock/{stockId}/transactions")  // [분석 3]
    @Operation(summary = "특정 주식 거래 내역", description = "해당 종목의 모든 거래 내역을 조회합니다")
    public ResponseEntity<List<TransactionDto>> getStockTransactions(@PathVariable Long stockId) {
        return ResponseEntity.ok(stockAnalysisService.getStockTransactions(stockId));
    }

    @GetMapping("/assets/{userId}")               // [분석 4]
    @Operation(summary = "총 자산 조회", description = "현금 + 보유 주식 평가액의 합을 조회합니다")
    public ResponseEntity<TradeSnapshotDto> getTotalAssets(@PathVariable Long userId) {
        return ResponseEntity.ok(stockAnalysisService.getTotalAssets(userId));
    }

    @GetMapping("/return-rate/{userId}")          // [분석 5]
    @Operation(summary = "총 수익률 조회", description = "평가손익 기준 총 수익률(%)을 조회합니다")
    public ResponseEntity<TradeSnapshotDto> getTotalReturnRate(@PathVariable Long userId) {
        return ResponseEntity.ok(stockAnalysisService.getTotalReturnRate(userId));
    }
    @GetMapping("/statistics")                    // [분석 6] GET /api/analysis/statistics
    @Operation(summary = "거래 통계", description = "종목별 매수/매도 수량과 금액을 집계합니다")
    public ResponseEntity<List<TransactionStatistics>> getTransactionStatistics() {
        return ResponseEntity.ok(stockAnalysisService.getTransactionStatistics());
    }

    @GetMapping("/daily")                         // [분석 7] GET /api/analysis/daily
    @Operation(summary = "일별 거래 내역", description = "날짜별 거래 건수와 금액을 집계합니다")
    public ResponseEntity<List<DailyTransaction>> getDailyTransactions() {
        return ResponseEntity.ok(stockAnalysisService.getDailyTransactions());
    }
}