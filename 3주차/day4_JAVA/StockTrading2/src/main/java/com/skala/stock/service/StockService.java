package com.skala.stock.service;

import com.skala.stock.dto.StockDto;
import com.skala.stock.entity.Stock;
import com.skala.stock.repository.StockRepository;
import lombok.RequiredArgsConstructor;

import org.springframework.lang.NonNull;
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

    public List<StockDto> getAllStocks() {
        return stockRepository.findAll().stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }
    // 추가 CRUD
    @Transactional   // ★ 필수! 클래스가 readOnly=true라서, 이게 없으면 수정이 조용히 무시됨
    public StockDto updateStock(@NonNull Long id, StockDto stockDto) {
        // 1단계: 수정할 대상을 먼저 찾는다 (없는 id면 예외를 던져 명확한 에러를 줌)
        Stock stock = stockRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("주식을 찾을 수 없습니다: " + id));
        stock.setName(stockDto.getName());
        stock.setCurrentPrice(stockDto.getCurrentPrice());
        stock.setPreviousPrice(stockDto.getPreviousPrice());
        // 2단계: 찾은 객체의 값을 요청받은 새 값으로 교체 (code는 종목의 고유 식별자이므로 바꾸지 않는 것이 원칙)
        // 3단계: 저장하고, 화면에 돌려줄 DTO로 변환해 반환
        Stock updatedStock = stockRepository.save(stock);
        return convertToDto(updatedStock);
    }

    @Transactional
    public void deleteStock(@NonNull Long id) {
        if (!stockRepository.existsById(id)) {
            throw new RuntimeException("주식을 찾을 수 없습니다: " + id);
        }
        stockRepository.deleteById(id);
    }

    // 추가 CRUD 2
    public StockDto getStockByCode(String code) {
        Stock stock = stockRepository.findByCode(code)
                .orElseThrow(() -> new RuntimeException("주식을 찾을 수 없습니다: " + code));
        return convertToDto(stock);
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

    @Transactional
    public StockDto updateStockPrice(String code, int newPrice) {
        Stock stock = stockRepository.findByCode(code)
                .orElseThrow(() -> new RuntimeException("주식을 찾을 수 없습니다: " + code));
        stock.setPreviousPrice(stock.getCurrentPrice());
        stock.setCurrentPrice((long) newPrice);
        Stock updatedStock = stockRepository.save(stock);
        return convertToDto(updatedStock);
    }   
}
