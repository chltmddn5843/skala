package com.skala.stock.dto;

/** [분석 6] 종목별 거래 통계의 결과 그릇
 *  규칙: SQL의  AS "stockCode"  ↔  getStockCode()  처럼
 *        별칭과 get 뒤의 이름이 같으면 스프링이 자동으로 값을 채워 준다 */
public interface TransactionStatistics {
    String getStockCode();         // 종목 코드
    String getStockName();         // 종목 이름
    Long getTotalBuyQuantity();    // 총 매수 수량
    Long getTotalSellQuantity();   // 총 매도 수량
    Long getNetQuantity();         // 순수량 (매수 - 매도)
    Long getTotalBuyAmount();      // 총 매수 금액
    Long getTotalSellAmount();     // 총 매도 금액
    Long getNetAmount();           // 순금액
}