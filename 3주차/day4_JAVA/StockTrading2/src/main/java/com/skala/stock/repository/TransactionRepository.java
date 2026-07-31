package com.skala.stock.repository;

import com.skala.stock.entity.Transaction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import com.skala.stock.dto.DailyTransaction;
import com.skala.stock.dto.TransactionStatistics;
import org.springframework.data.jpa.repository.Query;
import java.util.List;

@Repository
public interface TransactionRepository extends JpaRepository<Transaction, Long> {
    List<Transaction> findByUserIdOrderByTransactionDateDesc(Long userId);
    List<Transaction> findByUserIdAndStockIdOrderByTransactionDateDesc(Long userId, Long stockId);
    // [분석 3용] "stockId로 찾고 거래일 내림차순" — 역시 메서드 이름만으로 쿼리 완성!
    List<Transaction> findByStockIdOrderByTransactionDateDesc(Long stockId);
    // 
    /** [분석 6] 종목별 거래 통계 — SQL을 직접 작성! (nativeQuery=true: 진짜 SQL 그대로 실행) */
    @Query(nativeQuery = true, value = """
        SELECT s.code                                                        AS "stockCode",
               s.name                                                        AS "stockName",
               SUM(CASE WHEN t.type = 'BUY'  THEN t.quantity     ELSE 0 END) AS "totalBuyQuantity",
               SUM(CASE WHEN t.type = 'SELL' THEN t.quantity     ELSE 0 END) AS "totalSellQuantity",
               SUM(CASE WHEN t.type = 'BUY'  THEN t.quantity
                        ELSE -t.quantity END)                                AS "netQuantity",
               SUM(CASE WHEN t.type = 'BUY'  THEN t.total_amount ELSE 0 END) AS "totalBuyAmount",
               SUM(CASE WHEN t.type = 'SELL' THEN t.total_amount ELSE 0 END) AS "totalSellAmount",
               SUM(CASE WHEN t.type = 'BUY'  THEN t.total_amount
                        ELSE -t.total_amount END)                            AS "netAmount"
        FROM transactions t
        JOIN stocks s ON t.stock_id = s.id
        GROUP BY s.code, s.name
        ORDER BY s.code
        """)
// SQL 읽는 법: CASE WHEN = "조건에 맞을 때만 이 값을" (BUY면 수량을, 아니면 0을 더해라)
//             GROUP BY  = "종목별로 묶어서" 집계
// ★ AS "별칭"의 큰따옴표는 대소문자 보존용 — 인터페이스의 getStockCode()와 이름을 맞추는 핵심!
    List<TransactionStatistics> getTransactionStatistics();

    /** [분석 7] 일별 거래 집계 */
    @Query(nativeQuery = true, value = """
        SELECT FORMATDATETIME(t.transaction_date, 'yyyy-MM-dd') AS "tradeDate",
               COUNT(*)                                         AS "tradeCount",
               SUM(t.total_amount)                              AS "totalAmount"
        FROM transactions t
        GROUP BY FORMATDATETIME(t.transaction_date, 'yyyy-MM-dd')
        ORDER BY "tradeDate" DESC
        """)
// FORMATDATETIME: H2 DB의 함수 — "2026-07-30 14:23:05" 같은 시각에서 시간을 떼고
//                 "2026-07-30" 날짜 문자열로 변환 → 같은 날짜끼리 묶기 위해 사용
    List<DailyTransaction> getDailyTransactions();
}
