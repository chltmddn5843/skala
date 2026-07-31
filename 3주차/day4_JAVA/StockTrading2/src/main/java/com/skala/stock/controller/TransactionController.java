package com.skala.stock.controller;

import com.skala.stock.dto.TransactionDto;
import com.skala.stock.dto.TradeRequestDto;
import jakarta.validation.Valid;
import com.skala.stock.service.TransactionService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/transactions")
@RequiredArgsConstructor
@Tag(name = "거래 관리", description = "주식 매수/매도 거래 API")
public class TransactionController {

    private final TransactionService transactionService;
    @PostMapping("/trade")   // 최종 주소: POST /api/transactions/trade
    @Operation(summary = "거래 실행", description = "주식을 매수 또는 매도합니다")
    public ResponseEntity<TransactionDto> executeTrade(@Valid @RequestBody TradeRequestDto request) {
// TradeRequestDto(userId, stockId, type, quantity)는 교수님이 이미 만들어 둠!
// @Valid → DTO 안의 @NotNull 검증이 자동 실행 (dto 폴더에서 열어 확인해 보세요)
        TransactionDto result = transactionService.executeTrade(request);
        return ResponseEntity.ok(result);
    }
    @GetMapping("/user/{userId}")
    @Operation(summary = "사용자 거래 내역 조회", description = "특정 사용자의 전체 거래 내역을 조회합니다")
    public ResponseEntity<List<TransactionDto>> getUserTransactions(@PathVariable Long userId) {
        List<TransactionDto> transactions = transactionService.getUserTransactions(userId);
        return ResponseEntity.ok(transactions);
    }
    @GetMapping("/{id}")   // GET /api/transactions/{id}
// ※ "/user/{userId}"와 모양이 다르므로(중간에 /user가 있고 없고) 충돌하지 않는다
    @Operation(summary = "거래 상세 조회", description = "거래 ID로 상세 정보를 조회합니다")
    public ResponseEntity<TransactionDto> getTransactionById(@PathVariable Long id) {
        return ResponseEntity.ok(transactionService.getTransactionById(id));
    }

    @GetMapping("/user/{userId}/stock/{stockId}")   // 주소에 변수가 2개!
    @Operation(summary = "사용자-주식별 거래 내역", description = "특정 사용자의 특정 주식 거래 내역을 조회합니다")
    public ResponseEntity<List<TransactionDto>> getUserStockTransactions(
            @PathVariable Long userId,      // 주소의 {userId} 자리 값이 여기로
            @PathVariable Long stockId) {   // 주소의 {stockId} 자리 값이 여기로
        return ResponseEntity.ok(transactionService.getUserStockTransactions(userId, stockId));
    }
}