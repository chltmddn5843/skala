package com.skala.stock.dto;

/** [분석 7] 일별 거래 집계의 결과 그릇 */
public interface DailyTransaction {
    String getTradeDate();     // 거래 날짜 (yyyy-MM-dd 문자열)
    Long getTradeCount();      // 그날의 거래 건수
    Long getTotalAmount();     // 그날의 총 거래 금액
}