# 프로그램 전체 설명 및 변경 내역
# -------------------
# 작성자 : 최승우
# 작성일 : 2026-08-04
# 작성 목적
# 1) 2x2 EDA 대시보드 시각화 및 이미지 저장
# 2) 서울 vs 부산 t-test 및 카테고리x결제수단 카이제곱 독립성 검정
# 3) scikit-learn Pipeline(ColumnTransformer + Ridge) 구축, 평가 및 joblib 저장/재로드 검증
# 4) Plotly 인터랙티브 차트 생성 및 HTML 저장
#
# 변경 내역
# 2026-08-04 : 최초 작성
# -------------------


# 1) 기본 라이브러리
import os
import sys
import logging
from pathlib import Path

# 2) 시각화 및 통계 검정 수행을 위한 라이브러리
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 3)을 위한 joblib 라이브러리 사용
import joblib 
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer 
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler # 3)을 위한 전처리기 구성
from sklearn.linear_model import Ridge # 3)을 위한 Ridge 회귀 모델 사용

# 4)을 위한 라이브러리 plotly express를 사용하여 인터랙티브 차트 생성
import plotly.express as px # 

# ---------------------------------------------------------
# 기본 환경 설정 및 데이터 로드 함수
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sales_100k.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
MODEL_DIR = BASE_DIR / "models"

# 한글 글꼴 및 마이너스 깨짐 방지 설정
plt.rcParams['font.family'] = 'AppleGothic' 
plt.rcParams['axes.unicode_minus'] = False


# ---------------------------------------------------------
# 0) 데이터 로드 및 전처리 함수
# ---------------------------------------------------------
"""
1. df의 칼럼명 분석 가능하도록 타입 변경
2. order_date를 datetime으로 변환 후 year_month, month_number 컬럼 생성
3. amount NaN 행 제거
4. IQR 기반 이상치 제거
"""

def load_data(path: Path) -> pd.DataFrame:
  try:
    df = pd.read_csv(path)
    # order_date 처리
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['year_month'] = df['order_date'].dt.to_period('M').astype(str)
    df['month_number'] = df['order_date'].dt.month

    # 핵심: 타겟 변수(amount)의 NaN 행 제거
    df = df.dropna(subset=['amount']).copy()

    # IQR 기반 이상치 제거
    q1 = df['amount'].quantile(0.25)
    q3 = df['amount'].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    df = df[df['amount'].between(lower_bound, upper_bound)]

    return df
  except Exception as e:
    logging.error(f'데이터 로드 실패: {e}')
    sys.exit(1)

# ---------------------------------------------------------
# 1) EDA 시각화 4종 (2x2 서브플롯)
# ---------------------------------------------------------
def create_eda_dashboard(df: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1-1. 히스토그램 + KDE (매출액 분포)
    sns.histplot(data=df, x='amount', kde=True, alpha=0.7, ax=axes[0, 0],color='skyblue')
    axes[0, 0].set_title("1) 매출액 분포 및 KDE")
    axes[0, 0].set_xlabel("매출액 (amount)")
    axes[0, 0].set_ylabel("빈도")

    # 1-2. 박스플롯 (서울,부산, 대구, 인천 지역별 매출액 분포)
    sns.boxplot(data=df, x='region', y='amount', ax=axes[0, 1], hue='region', palette='Set2')
    axes[0, 1].set_title("2) 지역별 매출 박스플롯")
    axes[0, 1].set_xlabel("지역")
    axes[0, 1].set_ylabel("매출액")

    # 1-3. 월별 라인 차트 (월별 총매출 추이)
    # amout 값 단위를 천 단위로 변환하여 시각화
    monthly_sales = df.groupby('year_month')['amount'].sum().reset_index()
    monthly_sales['amount'] = monthly_sales['amount'] / 1000  # 천 단위로 변환
    sns.lineplot(data=monthly_sales, x='year_month', y='amount', marker='o', ax=axes[1, 0], color='green')
    axes[1, 0].set_title("3) 월별 총매출 추이")
    axes[1, 0].set_xlabel("년-월")
    axes[1, 0].set_ylabel("총매출액")
    axes[1, 0].tick_params(axis='x', rotation=45)

    # 1-4. 상관 히트맵 (수치형 변수 간)
    numeric_cols = ['amount', 'quantity', 'unit_price', 'customer_age', 'month_number']
    corr_cols = [col for col in numeric_cols if col in df.columns]
    corr_matrix = df[corr_cols].corr()
    
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=axes[1, 1])
    axes[1, 1].set_title("4) 수치형 변수 상관 히트맵")

    plt.tight_layout()
    save_path = OUTPUT_DIR / "eda_dashboard.png"
    plt.savefig(save_path, dpi=150)
    print(f"[저장 완료] 2x2 EDA 대시보드: {save_path}")
    plt.close(fig)

# ---------------------------------------------------------
# 2) 통계 검정 (t-test + 카이제곱 독립성 검정)
# ---------------------------------------------------------
def run_statistical_tests(df: pd.DataFrame) -> None:
    """t-test 및 카이제곱 검정을 수행하고 결과를 출력합니다."""
    print("\n" + "="*50)
    print(" 2) 통계 검정 수행")
    print("="*50)

    # [2-1] 서울 vs 부산 독립표본 t-test (Welch's t-test)
    seoul_amount = df.loc[df['region'] == '서울', 'amount'].dropna()
    busan_amount = df.loc[df['region'] == '부산', 'amount'].dropna()

    t_stat, p_val_t = stats.ttest_ind(seoul_amount, busan_amount, equal_var=False)
    print(f"[독립표본 t-test: 서울 vs 부산 매출 평균 비교]")
    print(f" - t-statistic: {t_stat:.4f}, p-value: {p_val_t:.6e}")
    
    if p_val_t < 0.05:
        print(" - [해석] p-value < 0.05 이므로 서울과 부산의 평균 매출액은 통계적으로 유의미한 차이가 있습니다.")
    else:
        print(" - [해석] p-value >= 0.05 이므로 서울과 부산의 평균 매출액 차이는 통계적으로 유의미하지 않습니다.")

    # [2-2] 카테고리 x 결제수단 카이제곱 독립성 검정
    contingency_tab = pd.crosstab(df['category'], df['payment_method'])
    chi2, p_val_chi2, dof, expected = stats.chi2_contingency(contingency_tab)
    
    print(f"\n[카이제곱 독립성 검정: category vs payment_method]")
    print(f" - chi2: {chi2:.4f}, dof: {dof}, p-value: {p_val_chi2:.6e}")
    
    if p_val_chi2 < 0.05:
        print(" - [해석] p-value < 0.05 이므로 상품 카테고리와 결제 수단 간에는 통계적으로 유의미한 상관관계(의존성)가 있습니다.")
    else:
        print(" - [해석] p-value >= 0.05 이므로 상품 카테고리와 결제 수단은 서로 독립적입니다.")

# ---------------------------------------------------------
# 3) sklearn Pipeline 구성, 학습, 평가 및 모델 저장
# ---------------------------------------------------------
def build_and_save_pipeline(df: pd.DataFrame) -> None:
  # amount가 NaN인 데이터 제거
    df_clean = df.dropna(subset=['amount']).copy()

    feature_cols = [
        'quantity',
        'unit_price',
        'customer_age',
        'month_number',
        'region',
        'category',
        'payment_method',
        'customer_gender',
    ]
    X = df_clean[feature_cols]
    y = df_clean['amount']


    # 수치형/범주형 컬럼 분리
    num_cols = ['quantity', 'unit_price', 'customer_age', 'month_number']
    cat_cols = ['region', 'category', 'payment_method', 'customer_gender']

    # 전처리기 구축
    num_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    cat_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ('num', num_transformer, num_cols),
        ('cat', cat_transformer, cat_cols)
    ])

    # 파이프라인 결합 (전처리 + Ridge 모델)
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', Ridge(alpha=1.0))
    ])

    # 학습/테스트 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 학습 및 평가
    model_pipeline.fit(X_train, y_train)
    r2_score = model_pipeline.score(X_test, y_test)
    print(f" - Pipeline 모델 테스트 R² Score: {r2_score:.4f}")

    # joblib 모델 파일 저장
    model_path = MODEL_DIR / "sales_pipeline.joblib"
    joblib.dump(model_pipeline, model_path)
    print(f"[저장 완료] Pipeline 모델: {model_path}")

    # 재로드 검증
    loaded_pipeline = joblib.load(model_path)
    preds = loaded_pipeline.predict(X_test.head(5))
    print(f" - 재로드된 모델 샘플 예측값(5건): {np.round(preds, 2)}")

# ---------------------------------------------------------
# 4) Plotly 인터랙티브 차트 저장 (.html)
# ---------------------------------------------------------
def create_plotly_chart(df: pd.DataFrame) -> None:
    """지역 및 카테고리별 총매출을 표현하는 Plotly 인터랙티브 막대 차트를 작성합니다."""
    grouped_df = df.groupby(['region', 'category'], as_index=False)['amount'].sum()

    fig = px.bar(
        grouped_df,
        x='region',
        y='amount',
        color='category',
        barmode='group',
        title='지역 및 카테고리별 총매출액',
        labels={'region': '지역', 'amount': '총매출액(원)', 'category': '카테고리'}
    )

    fig.update_layout(
        font=dict(size=13),
        yaxis_tickformat=','
    )

    html_path = OUTPUT_DIR / "interactive_sales.html"
    fig.write_html(str(html_path), include_plotlyjs='cdn')
    print(f"\n[저장 완료] Plotly 인터랙티브 차트: {html_path}")

# ---------------------------------------------------------
# Main 실행 함수
# ---------------------------------------------------------
if __name__ == "__main__":
    # 0) 데이터 로드
    df = load_data(DATA_PATH)

    # 1) EDA 대시보드 시각화 (2x2 서브플롯)
    create_eda_dashboard(df)

    # 2) 통계 검정 (t-test & 카이제곱)
    run_statistical_tests(df)

    # 3) Pipeline 학습 및 저장
    build_and_save_pipeline(df)

    # 4) Plotly 차트 저장
    create_plotly_chart(df)

    print("\n전체 작업이 성공적으로 종료되었습니다.")