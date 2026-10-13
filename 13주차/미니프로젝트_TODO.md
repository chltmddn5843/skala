# 13주차 데이터분석 미니프로젝트 TODO

근거: [프로젝트 일정계획.txt](<실습자료/프로젝트%20일정계획.txt>), 학습자료 PDF p.22~25
과제: Target_1(D+3 KOSPI 상승), Target_2(D+3 건강식품 지수 상승) 확률 예측, 평가지표 AUC
배점: Private Score 평균 60 + 보고서·코드 정성평가 40

> 파일명의 `4반_최승우`는 기존 폴더명(판교_4반_최승우)에서 추정했습니다. 반이 다르면 수정하세요.
> 1일차·2일차의 실제 날짜는 아직 확인하지 않았습니다.

## ⚠️ 제출 전 필수 확인 (주소·이름)

| 제출    | 노트북 [2]번 셀 입력 | [30]번 셀 파일명                     | 제출 주소                           |
| ------- | -------------------- | ------------------------------------ | ----------------------------------- |
| Public  |  `test_public.csv` | `public_4반_최승우_N.csv` (N=회차) | https://forms.gle/S8X2XRqHtAGuvwgq5 |
| Private | `test_private.csv` | `private_4반_최승우.csv`           | https://forms.gle/eyvChbVYL6MhhdtaA |

- [X] 입력 파일, 파일명, 제출 주소 3개가 **같은 줄(Public 또는 Private)** 에 맞춰져 있는지 확인
- [X] 파일명의 `1반_홍길동`(Baseline 예시)을 내 반·이름으로 바꿨는지, Public은 회차 번호를 올렸는지 확인

## 1일차

### 오전 (~14:00 1차 제출 전)

- [ ] Baseline 노트북 실행해서 Valid AUC 기준점 기록 (Target별)
- [ ] 변수 설명서(xlsx) 훑고 Target과 관련 있어 보이는 변수군 메모
- [ ] Leakage 점검: fit은 Train만, `shift(-n)`·`center=True` 금지
- [ ] (선택) Baseline 결과를 1차 Public으로 제출 → `public_4반_최승우_1.csv`

### 오후 (~16:00 2차, ~17:30 3차)

- [ ] Feature Extraction: Lag(1·3·7일), Rolling(7·30일 평균), 2차 파생변수(비율)
- [ ] Feature Selection: Train/Valid 기준 중요도로 변수 정리
- [ ] 모델 비교: RandomForest vs XGBoost/LightGBM (Valid AUC)
- [ ] 하이퍼파라미터 튜닝은 **Valid 기준** (Public 점수에 맞추지 않기)
- [ ] (선택) 개선 결과를 Public으로 제출 (2·3회차)
- [ ] 실험 기록표 유지: 변경점 / Valid AUC / Public AUC

## 2일차

### ~10:00

- [ ] (선택) 마지막 Public 제출. **총 4회까지만 가능**하고 10시 이후 제출분은 무효
- [ ] 최종 모델 확정

### ~14:00 Private 제출 (필수, 1회만 가능)

- [ ] `test_private.csv`로 바꿔 예측 (Baseline [2]번 셀 주석 전환)
- [ ] 최종 모델은 Train+Valid로 재학습할지 결정 (p.8)
- [ ] 제출 형식 확인: 컬럼명이 sample과 같은지, pred_1·pred_2가 0~1 사이인지, 행 수가 맞는지
- [ ] `private_4반_최승우.csv` 제출 → https://forms.gle/eyvChbVYL6MhhdtaA

### ~14:50 보고서·코드 제출

- [ ] 보고서 PDF `모델결과보고서_4반_최승우.pdf`: 전처리 → Feature Extraction/Selection → 모델·검증 설계 → 최적화 과정 → 결과 및 인사이트
- [ ] 코드 `코드_4반_최승우.zip`: Private Score를 재현할 수 있는 .ipynb
- [ ] 제출처(반별 공지) 확인 후 제출

### 15:00~

- [ ] 반 상위 10명에 들면 5분 발표
- [ ] 16:00 Wrap-up

## 링크

- Public 제출: https://forms.gle/S8X2XRqHtAGuvwgq5
- Private 제출: https://forms.gle/eyvChbVYL6MhhdtaA
