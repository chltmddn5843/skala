# 프로그램 전체 설명 및 변경 내역
# -------------------
# 작성자 : 최승우
# 작성 목적 : 파이썬 기본 이해 실습
# 작성일 : 2026-08-03
#
# 실습 내용 : json(Sales) 리스트에서 아래 4가지 시나리오 실습 수행
# 변경 내역
# 26.08.03 / 최초 작성 / 전체 코드 작성
#
# -------------------




# -------------------
# 코드 목차

# 1
# 1.1 json 파일 로드 함수
# 1.2 amount ≥ 1000인 거래만 필터링
# 1.3 지역별 총 매출 dict를 컴프리헨션으로 계산

# 2
# 2.1 Counter로 지역별 거래 건수
# 2.2 defaultdict로 카테고리별 amount 리스트

# 3
# 3.1 amount > 1000 인 행만 yield 하는 제너레이터
# 3.2 리스트 버전과 메모리 크기를 비교

# 4
# 4.1 월별 카테고리 매출 그룹핑
# 4.2 총매출 dict 생성

# -------------------

"""

# 1번 시나리오
- 리스트/딕셔너리 컴프리헨션
① amount ≥ 1000인 거래만 필터링
② 지역별 총 매출 dict를 컴프리헨션으로 계산

"""
import json 

# 1.1 json 파일 로드 함수
def load_json_file(file_path: str) -> list:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

sales_data = load_json_file('Python_Practice2_Data.json') 
print("[1.1]json 파일 로드 완료, 거래 데이터 수:", len(sales_data))
# Practice2 : json 파일 
# Practice1 : dict 파일


# 1.2 amount ≥ 1000인 거래만 필터링
amount_over_1000 = [sale for sale in sales_data if sale['amount'] >= 1000]
print("\n[1.2]거래량 1000개 이상 :", amount_over_1000)


# 1.3 지역별 총 매출 dict를 컴프리헨션으로 계산
region_total = {region: sum(sale['amount'] for sale in sales_data if sale['region'] == region) for region in set(sale['region'] for sale in sales_data)}
print("\n[1.3]지역별 총 매출:",region_total)


print("\n--------------------------------")


"""
# 2번 시나리오
2) Counter + defaultdict
① Counter로 지역별 거래 건수를 계산
② default dict로 카테고리별 amount 리스트
"""

from collections import Counter, defaultdict

# 2.1 Counter로 지역별 거래 건수
region_count = Counter(sale['region'] for sale in sales_data)
print("[2.1]지역별 거래 건수:",region_count)



# 2.2 defaultdict로 카테고리별 amount 리스트
category_amounts = defaultdict(list)
for sale in sales_data:
    category_amounts[sale['category']].append(sale['amount'])
print("\n[2.2]카테고리별 amount 리스트:", category_amounts)


print("\n--------------------------------")


"""
# 3번 시나리오
3) 제너레이터 - 메모리 비교
① amount > 1000 인 행만 yield 하는 제너레이터를 작성
② 리스트 버전과 메모리 크기를 비교
"""
from sys import getsizeof

# 3.1 amount > 1000 인 행만 yield 하는 제너레이터를 작성
def amount_over_1000_generator(sales_data):
    for sale in sales_data:
        if sale['amount'] > 1000:
            yield sale

# 3.2 리스트 버전과 메모리 크기를 비교)
amount_list = [sale for sale in sales_data if sale['amount'] > 1000]
sale_generator = amount_over_1000_generator(sales_data)
memory_list = getsizeof(amount_list)  # 리스트 버전 메모리 크기
memory_generator = getsizeof(sale_generator)  # 제너레이터 버전 메모리 크기

print("\n[3.2]리스트 버전과 제너레이터 버전 메모리 크기 비교:")
print(f"리스트 버전 메모리 크기: {memory_list} bytes")
print(f"제네레이터 버전 메모리 크기 : {memory_generator} bytes")
print(f"제너레이터가 리스트보다 작음: {memory_generator < memory_list}")


print("\n--------------------------------") 



"""
# 4번 시나리오
4) 종합 - 월별 카테고리 매출 집계
① sales 데이터를 month·category 기준으로 그룹핑
② 총매출 dict를 완성
- 조건 : 컴프리헨션+ defaultdict 활용

"""
# 4.1 월별 카테고리 매출 그룹핑
month_category_sales = defaultdict(lambda: defaultdict(int))
for sale in sales_data:
    month = sale['month']
    category = sale['category']
    amount = sale['amount']
    month_category_sales[month][category] += amount
print("\n[4.1]월별 카테고리 매출 그룹핑:", month_category_sales)


# 4.2 총매출 dict 생성
total_sales = {month: sum(category_sales.values()) for month, category_sales in month_category_sales.items()}
print("\n[4.2]총매출 dict 생성:", total_sales)

# 4.3 내림차순 정렬
sorted_total_sales = dict(sorted(total_sales.items(), key=lambda x: x[1], reverse=True))
print("\n[4.3]총매출 내림차순 정렬:", sorted_total_sales)