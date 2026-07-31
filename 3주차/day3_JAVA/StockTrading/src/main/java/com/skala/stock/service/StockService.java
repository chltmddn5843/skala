package com.skala.stock.service;

import com.skala.stock.dto.StockDto;
import com.skala.stock.entity.Stock;
import com.skala.stock.repository.StockRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class StockService {

    private final StockRepository stockRepository;

    @Transactional
    public StockDto createStock(StockDto stockDto) {
        if (stockRepository.existsByCode(stockDto.getCode())) {
            throw new RuntimeException("이미 존재하는 종목 코드입니다: " + stockDto.getCode());
        }

        Stock stock = Stock.builder()
                .code(stockDto.getCode())
                .name(stockDto.getName())
                .currentPrice(stockDto.getCurrentPrice())
                .previousPrice(stockDto.getPreviousPrice())
                .build();

        Stock savedStock = stockRepository.save(stock);
        return convertToDto(savedStock);
    }

    public StockDto getStockById(Long id) {
        
        Stock stock = stockRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("주식을 찾을 수 없습니다: " + id));
        return convertToDto(stock);
    }

    /** 종목 코드로 주식 1개를 조회한다 */
    public StockDto getStockByCode(String code) {
        // findByCode로 찾고, 없으면 예외를 던진다 (getStockById와 같은 구조!)
        Stock stock = stockRepository.findByCode(code)
                .orElseThrow(() -> new RuntimeException("주식을 찾을 수 없습니다: " + code));
        return convertToDto(stock);   // Entity → DTO 변환 후 반환
    }

    public List<StockDto> getAllStocks() {
        return stockRepository.findAll().stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }
    /** 주식 정보를 수정한다 */
    @Transactional   // ★ 필수! 클래스가 readOnly라서, 쓰기 메서드엔 이걸 붙여야 DB에 반영됨
    public StockDto updateStock(Long id, StockDto stockDto) {
        // 1단계: 수정할 대상을 먼저 찾는다 (없으면 예외)
        Stock stock = stockRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("주식을 찾을 수 없습니다: " + id));

        // 2단계: 찾은 객체의 값을 새 값으로 바꾼다
        stock.setName(stockDto.getName());
        stock.setCurrentPrice(stockDto.getCurrentPrice());
        stock.setPreviousPrice(stockDto.getPreviousPrice());
        // (code는 종목의 고유 식별자이므로 바꾸지 않는 것이 일반적)

        // 3단계: 저장하고 DTO로 변환해 반환
        Stock updatedStock = stockRepository.save(stock);
        return convertToDto(updatedStock);
    }
    /** 주식을 삭제한다 */
    @Transactional   // 삭제도 데이터를 바꾸는 일이므로 필수
    public void deleteStock(Long id) {
        // 1단계: 존재하는지 먼저 확인 (없는 걸 지우려 하면 명확한 에러를 줘야 함)
        if (!stockRepository.existsById(id)) {
            throw new RuntimeException("주식을 찾을 수 없습니다: " + id);
        }
        // 2단계: 삭제
        stockRepository.deleteById(id);
    }
    
    private StockDto convertToDto(Stock stock) {
        return StockDto.builder()
                .id(stock.getId())
                .code(stock.getCode())
                .name(stock.getName())
                .currentPrice(stock.getCurrentPrice())
                .previousPrice(stock.getPreviousPrice())
                .build();
    }
}
