# PPT 작성 내용 (설계_개발결과서 양식 순서)

양식 구성: 표지 → 과제1(요구사항 / 설계서 / 개발결과서) → 과제2(요구사항 / 설계서 / 개발결과서)
파일명 예: `P131_최승우_AI Agent 설계 및 구축_설계_개발결과서_v0.1.pptx` (재제출 시 v0.2)

---

## 슬라이드 1. 표지
- 캠퍼스: (직접 기재) / 반: 4반 / 고유번호: P131 / 이름: 최승우

## 슬라이드 2. 과제1 요구사항
- 양식에 이미 들어 있는 요구사항 텍스트를 그대로 둔다.

## 슬라이드 3. 과제1 설계서

### 요구사항 분석 (노드명 | 작업 주요 내용)
| 노드 (작업자) 명 | 작업 주요 내용 |
|---|---|
| init_context | [Code] 런타임 콘텍스트(주제·타깃·기준점수·최대반복)를 초기 State에 저장 |
| writer | [LLM] 서론-본론-결론 초안 작성, 피드백 있으면 기존 초안+피드백으로 재작성 |
| evaluator | [LLM] 논리성·완성도·타깃 적합성 각 100점 채점, 보완 지시를 구조화 출력. 통과 판정은 안 함 |
| route_after_evaluation | [Code 라우터] 기준 이상 → finalize / 미만 → writer / 반복 소진 → human_review |
| human_review | [Human] 자동 반복 소진 시 interrupt, 검토자가 approve 또는 revise(수정 지시) |
| finalize | [Code] 최고 점수 원고(best_draft)를 확정본으로 저장 |

### 그래프 구성 설계 (그릴 내용)
- 실선: START → init_context → writer → evaluator, finalize → END
- 점선(조건부): evaluator → writer (점수 < 기준, 반복 남음)
- 점선(조건부): evaluator → finalize (점수 ≥ 기준)
- 점선(조건부): evaluator → human_review (반복 소진)
- 점선(Command goto): human_review → writer (revise) / human_review → finalize (approve)

### State 설계
| 필드명 | Type | 필드 설명 |
|---|---|---|
| topic | str | 마케팅 주제 (Context에서 저장) |
| target_audience | str | 타깃 독자 (Context에서 저장) |
| pass_score / max_loops | int | 통과 기준 / 자동 반복 상한 |
| stage | str | 현재 단계 (drafted, evaluated, approved …) |
| draft | str | 작성 중인 최신 초안 |
| score | int | 최근 평가 점수 |
| evaluation | dict | 세부 점수·강점·보완점 (구조화) |
| feedback | list[str] | 수정 요청 (평가자 + 검토자) |
| loop_count | int | 작성 횟수 |
| best_draft / best_score | str / int | 최고 점수 초안과 점수 |
| final_report | str | 확정본 |
| score_history | list[int] (add) | 회차별 점수 누적 |
| llm_calls | int (add) | LLM 호출 수 누적 (비용 관찰) |

### (공간이 있으면) 설계 고민 3줄
- 통과 판정은 LLM이 아닌 코드가 한다: LLM은 점수만, `score >= pass_score` 비교는 라우터 (교재 p.100 원칙 2)
- 반복 상한 + 사람 검토: 상한만 두면 기준 미달 원고가 그대로 나가므로 예외는 사람에게 (p.103, p.119)
- 최종본은 최고점 원고: 실행에서 92 → 88로 점수가 떨어지는 회차가 나와 마지막 원고를 쓰지 않음

## 슬라이드 4. 과제1 개발결과서
- 그래프 생성 결과 이미지: `task1_graph.png`
- 실행 결과 로그 (`task1_run.log`에서 발췌, 시나리오 2):
```
[init_context] 주제=생성형 AI 기반 초개인화 CRM 마케팅 | 기준 95점 | 최대 3회
[writer] 1회차 초안 작성 시작
[writer] 완료 | 1779자 | stage initialized -> drafted | loop_count 0 -> 1
[evaluator] 1회차 | 종합 80 (논리 85 / 완성 75 / 타깃 80) | 기준 95
    보완1: 서론에 생성형 AI와 초개인화 CRM의 개념을 간략히 정의하여 비전문가 이해를 돕기
[router] 80 < 95 -> writer 재작성 (2/3)
[evaluator] 2회차 | 종합 88 (논리 90 / 완성 85 / 타깃 88) | 기준 95
[router] 88 < 95 -> writer 재작성 (3/3)
[evaluator] 3회차 | 종합 92 (논리 95 / 완성 90 / 타깃 92) | 기준 95
[router] 92 < 95, 작성 3회로 자동 반복 소진 -> human_review
[INTERRUPT] human_review 대기 | 최고 92점 | 점수 추이 [80, 88, 92]
[human_review] 검토자 결정 revise | 지시: 분량을 1,500자 내외로 줄이고, 트렌드마다 도구 1개와 월 예상 비용
[evaluator] 4회차 | 종합 88 | best_score 92 -> 92
[INTERRUPT] human_review 대기 | 최고 92점 | 점수 추이 [80, 88, 92, 88]
[human_review] 검토자 결정 approve | 최고점 92점 원고로 확정
[finalize] stage -> approved_by_human | 확정본 92점 | 작성 4회 | LLM 호출 8회
```
- 시나리오 1(기준 80점)은 1회차 88점으로 바로 통과 (`[router] 88 >= 80 -> finalize`)

---

## 슬라이드 5. 과제2 요구사항
- 양식 텍스트 그대로.

## 슬라이드 6. 과제2 설계서

### 요구사항 분석
| 노드 (작업자) 명 | 작업 주요 내용 |
|---|---|
| load_memory | [Code] user_id로 장기 메모리(Store)에서 투자 성향·과거 거래 이력 로드 |
| supervisor | [Code+LLM] 정해진 순서는 코드로 라우팅, 고객 반려 시에만 LLM이 재분석/재배분/종료 판단 |
| market_analyst (브릿지) | 부모 State 중 profile·feedback만 서브그래프에 전달 (계좌·자산 미전달) |
| └ fetch_market_data | [Code] 자산·트렌드 데이터 조회 (가상 데이터) |
| └ extract_candidates | [LLM] 성향에 맞는 투자 후보 추출, 없는 종목 코드 제거 |
| portfolio_planner (서브그래프) | 공유 State로 제안 작성 |
| └ draft_allocation | [LLM] 투자 비율·리포트 초안, 반려 피드백 반영 |
| └ finalize_proposal | [Code] 비율 정규화·금액 환산, 승인 대기 전환 |
| human_review | [Human] interrupt로 승인/반려 대기, 잘못된 입력은 재질문(검증 루프) |
| time_travel (실행 헬퍼) | 반려 시 시장 분석 완료 직후(supervisor 직전) 체크포인트로 분기해 재구성 |
| guardrail | [Code] 1회 한도·잔액·계좌 형식·신고 계좌·회피 자산·합계 검증 |
| execute_transfer | [Code] 가상 송금·매수, 자산 갱신, 거래 이력을 장기 메모리에 저장 |
| audit (로그 시스템) | 전환·인터럽트·승인/반려·State 변화를 JSONL에 누적, 계좌 마스킹 |

### 그래프 구성 설계 (그릴 내용)
- 실선: START → load_memory → supervisor, market_analyst → supervisor, portfolio_planner → human_review, execute_transfer → END
- 점선(조건부): supervisor → market_analyst (후보군 없음 / 반려 후 재분석) / portfolio_planner (첫 제안 / 비중 조정) / END (FINISH: 투자 취소)
- 점선(Command goto): human_review → guardrail (approve) / END (reject)
- 점선(조건부): guardrail → execute_transfer (통과) / END (차단)
- 그래프 밖 화살표(설명용): END(reject) ⇢ time travel ⇢ supervisor 직전 체크포인트
- 서브그래프 박스 2개: market_analyst(State 분리), portfolio_planner(State 공유)

### State 설계
| 필드명 | Type | 필드 설명 |
|---|---|---|
| customer | dict | 고객 정보 (이름·나이·목표) |
| assets | dict | 자산 현황 {cash, holdings} |
| invest_amount | int | 투자(송금) 금액 |
| target_account | str | 송금 계좌 |
| profile | dict | 장기 메모리 투자 성향 + 이력 |
| candidates | list[dict] | 투자 후보군 |
| portfolio | dict | 제안 {allocations, report} |
| approval_status | str | pending/approved/rejected/blocked/completed |
| feedback | str | 고객 수정 요청 |
| rejection_count | int | 반려 횟수 |
| next_agent | str | Supervisor 라우팅 결과 |
| guardrail / tx_id | dict / str | 검증 결과 / 거래 ID |

(별도) AnalystState: profile, feedback, market_data, candidates — 시장 분석 서브그래프 전용 (조회 데이터는 부모 State에 올리지 않음)
(별도) Store: (user_id, "profile") 투자 성향, (user_id, "history") 상담·거래 이력

### (공간이 있으면) 설계 고민 3줄
- Supervisor LLM은 판단이 필요할 때만: 매번 호출하던 v0.2는 코드 가드가 항상 결과를 덮어써 호출 2회가 낭비 → 반려 사유 해석(재분석/재배분/종료)에만 LLM 사용
- 서브그래프 State: 시장 분석은 계좌 정보가 필요 없어 State를 분리하고 브릿지로 profile·feedback만 전달 (최소 권한)
- 승인 입력은 명시적 값만 + interrupt 앞 부수효과 금지: 재개 시 노드가 처음부터 다시 실행됨을 직접 확인 (교재 p.151 설명과 다름)

## 슬라이드 7. 과제2 개발결과서
- 그래프 생성 결과 이미지: `task2_graph_xray.png`
- 실행 결과 로그 (`task2_run.log`에서 발췌):
```
[MEMORY_LOAD    ] user_id=user_001 | risk=중립형 | history_count=1
[AGENT_SWITCH   ] frm=supervisor | to=market_analyst | by=code | reason=후보군 없음
[BRIDGE         ] to=market_analyst | passed_fields=['profile', 'feedback'] | withheld=['assets', 'target_account']
[AGENT_DONE     ] market_analyst | candidates=['KR_LARGE', 'US_SP500', 'US_DIV', 'KTB_10Y', 'MMF']
[AGENT_SWITCH   ] frm=supervisor | to=portfolio_planner | by=code | reason=후보군 준비됨
[AGENT_DONE     ] portfolio_planner | allocation={'KR_LARGE': 30%, 'US_DIV': 30%, 'KTB_10Y': 30%, 'MMF': 10%}
[INTERRUPT      ] node=human_review | amount=20,000,000원
[INTERRUPT      ] 입력 오류({'action': 'reject'}): feedback 이 포함된 reject 만 허용
[HUMAN_REJECT   ] feedback=인플레이션 대비로 금을 10% 정도 넣고, 국내 주식 비중은 15% 이하로
[TIME_TRAVEL    ] to=supervisor 실행 직전 | step=3
[AGENT_SWITCH   ] frm=supervisor | to=market_analyst | by=llm | reason=현재 후보군에 금 관련 자산이 없어 후보군 재선정 필요
[AGENT_DONE     ] market_analyst | candidates=['GOLD', 'US_DIV', 'US_SP500', 'KR_LARGE', 'KTB_10Y']
[AGENT_DONE     ] portfolio_planner | allocation={'GOLD': 10%, 'KR_LARGE': 15%, 'US_DIV': 35%, 'KTB_10Y': 30%, 'US_SP500': 10%}
[HUMAN_APPROVE  ] amount=20,000,000원 | account=110-**-***789
[GUARDRAIL_PASS ] amount=20,000,000원
[TRANSFER_DONE  ] tx_id=TX-BED490C3 | cash_after=60,000,000원 | memory=history 저장
--- 시나리오 2 (같은 user_id, 새 thread) ---
[MEMORY_LOAD    ] user_id=user_001 | risk=중립형 | history_count=2
[HUMAN_APPROVE  ] amount=50,000,000원 | account=999-**-***999
[GUARDRAIL_BLOCK] violations=['1회 한도 30,000,000원 초과', '비정상(신고) 계좌']
```
