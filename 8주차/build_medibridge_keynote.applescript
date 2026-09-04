property outFile : "/Users/chltmddn5843/Downloads/skala/8주차/메디브릿지_발표자료.pptx"
property flowFile : "/Users/chltmddn5843/Downloads/User Interface and-2026-09-03-054358.png"
property erdFile : "/Users/chltmddn5843/Downloads/DBerd.png"
property assetDir : "/Users/chltmddn5843/Downloads/skala/8주차/ppt_assets/"
property backlogURL : "https://docs.google.com/spreadsheets/d/1X3ji7XSqgxXPO-5Ch4LrFJRvc-r4a7HmHxNoIaG5vfA/edit?gid=1939221835"
property sprintURL : "https://docs.google.com/spreadsheets/d/1vqYW_Ug6UC_3gNdNb3CemyC6BFcaLFNfj1HtguZfumM/edit?gid=1365266729"
property notionURL : "https://app.notion.com/p/Sprint1-3d074ceed1e18014a121c34110c90363"

on styleSlide(aSlide, aTitle, aBody, aNotes)
  tell application "Keynote"
    tell aSlide
      set object text of default title item to aTitle
      set font of object text of default title item to "Apple SD Gothic Neo"
      set size of object text of default title item to 34
      set color of object text of default title item to {4369, 7453, 12850}
      set object text of default body item to aBody
      set font of object text of default body item to "Apple SD Gothic Neo"
      set size of object text of default body item to 21
      set color of object text of default body item to {6682, 8224, 10537}
      set presenter notes to aNotes
    end tell
  end tell
end styleSlide

tell application "Keynote"
  activate
  set d to make new document with properties {document theme:theme "기본 흰색", width:1280, height:720}
  tell d
    -- 1. Cover
    set base slide of first slide to master slide "제목"
    my styleSlide(first slide, "메디브릿지", "영업의 거리를 넘어, 의약품 공급과 발주를 연결하다\n\nCSO와 약국·병원을 잇는 비대면 제품 탐색·추천·발주 플랫폼\n\nProduct Owner 김민주  |  Scrum Master 최승우  |  Front 임형준  |  Backend 권주현  |  Service Planning 전혜민", "발표의 핵심은 개발량보다 이해관계자 가치, 스프린트 의사결정, MSA 통신 경험입니다.\n\n[Sources]\n[/Sources]")

    -- 2. Pain points
    set s to make new slide with properties {base slide:master slide "제목 및 구분점"}
    my styleSlide(s, "문제는 제품 부족이 아니라 ‘연결의 한계’입니다", "약국·병원\n• 다양한 제약사의 유사 제품 비교와 신규 제품 탐색이 어렵다\n• 지역에 따라 제품 정보 접근 기회가 달라진다\n\nCSO 운영사\n• 영업사원 1명이 담당할 수 있는 거래처에 한계가 있다\n• 거래처별 수요를 체계적으로 활용하기 어렵다\n\n제약회사\n• 기존 영업망이 닿지 않는 거래처에 제품을 노출하기 어렵다\n\n공통 핵심  |  판매·주문 이력이 영업과 구매 판단에 충분히 활용되지 않는다", "CSO 현장 영업사원이 아니라 플랫폼 도입을 결정하는 CSO 운영사를 핵심 고객으로 둡니다.\n\n[Sources]\n[/Sources]")

    -- 3. Solution and recommendation image
    set s to make new slide with properties {base slide:master slide "제목 및 구분점"}
    my styleSlide(s, "셀프서비스 거래 흐름에 추천을 결합합니다", "핵심 흐름\n탐색 → 상세 확인 → 발주 → 상태 확인\n\nAI의 MVP 역할\n구매 이력이 있으면 가장 자주 산 약효군을 찾고, 아직 구매하지 않은 관련 제품을 추천합니다. 이력이 없으면 인기 제품을 제시합니다.\n\n향후 확장\n유사 거래처 · 재주문 시점 · 대체 제품", "첨부 그림의 고급 분석 표현은 발전 방향입니다. 현재 MVP는 최빈 카테고리와 미구매 제품을 이용한 규칙 기반 추천입니다.\n\n[Sources]\n- User-provided image: User Interface and-2026-09-03-054358.png\n[/Sources]")
    tell s
      set position of default body item to {65, 165}
      set width of default body item to 760
      set height of default body item to 470
      make new image with properties {file:POSIX file flowFile, position:{925, 130}, width:240, height:594}
    end tell

    -- 4. Priority
    set s to make new slide with properties {base slide:master slide "제목 및 구분점"}
    my styleSlide(s, "백로그는 가치·의존성·실습 가능성으로 정렬했습니다", "1  핵심 가치  |  사용자가 탐색부터 발주까지 끝낼 수 있는가\n\n2  업무 의존성  |  사용자·제품·주문 데이터가 먼저 존재하는가\n\n3  학습 가치  |  REST, Kafka, 인증 등 MSA 흐름을 경험하는가\n\n4  시간·위험  |  5시간 안에 검증 가능한 크기인가\n\n결론\nSprint 1은 ‘거래 완주’, Sprint 2는 ‘서비스 간 연동과 추천 확장’", "우선순위는 단순 중요도뿐 아니라 선행 데이터와 5시간 실습 제약을 함께 반영했습니다.\n\n[Sources]\n- " & backlogURL & "\n- " & sprintURL & "\n[/Sources]")

    -- 5. Sprint 1
    set s to make new slide with properties {base slide:master slide "제목 및 구분점"}
    my styleSlide(s, "Sprint 1 — 사용자가 발주까지 완주하는 MVP", "SPRINT GOAL\n로그인 → 의약품 조회 → 발주 신청까지 완료\n\n01 로그인  /login → OAuth2 → /callback\n02 목록 조회  GET /courses\n03 상세 조회  GET /courses/{id}\n04 발주 신청  POST /api/enrollments → PENDING\n05 상태 확인  GET /enrollments\n\nDefinition of Done\nSwagger 응답 성공 · 상태 저장 확인 · 다음 단계에서 조회 가능", "Sprint 1 실행표에는 다섯 단계가 완료로 기록되어 있습니다.\n\n[Sources]\n- " & backlogURL & "\n- " & sprintURL & "\n- " & notionURL & "\n[/Sources]")

    -- 6. Sprint 2
    set s to make new slide with properties {base slide:master slide "제목 및 구분점"}
    my styleSlide(s, "Sprint 2 — 결제 이벤트와 추천으로 MSA 경험 확장", "구매 승인 → payment-service → Kafka 결제 완료 이벤트 → order-service 상태 반영 → recommend-service 추천\n\n핵심 구현\n• 결제 완료 이벤트 전달\n• 주문 상태 변경\n• 구매 이력 기반 미구매 제품 추천\n\n상태 의미 정정\nACTIVE = 입고 완료  ✕\nACTIVE = 발주 확정 / 결제 완료  ○\n\n배송·입고 이벤트가 없는 현재 코드에서는 ‘입고 완료’를 확인할 수 없습니다.", "발표에서는 코드가 실제로 보장하는 상태만 설명합니다.\n\n[Sources]\n- " & sprintURL & "\n- " & notionURL & "\n[/Sources]")

    -- 7. Architecture
    set s to make new slide with properties {base slide:master slide "제목 및 구분점"}
    my styleSlide(s, "업무와 데이터 책임을 기준으로 5개 서비스로 분리했습니다", "Web / App  →  API Gateway  →  인증 서버 · Eureka\n                         ↓\npartner-service  ·  product-service  ·  order-service  ·  payment-service  ·  recommend-service\n계정·거래처          의약품 정보          발주·상태             결제·승인               추천\n\nREST\n사용자 조회·명령과 서비스 간 동기 통신\n\nKafka\npayment-service ── PaymentCompleted ──▶ order-service\n\n원칙\n각 서비스가 자신의 업무 결과 데이터를 소유하고 API 계약·이벤트로 연결", "같은 서비스 안에서는 계층과 트랜잭션 경계로 격리하고, 서비스 간에는 API 계약과 이벤트로 결합도를 낮춥니다.\n\n[Sources]\n[/Sources]")

    -- 8. ERD
    set s to make new slide with properties {base slide:master slide "제목 전용"}
    tell s
      set object text of default title item to "데이터는 사용자·제품·발주·결제의 결과로 남습니다"
      set font of object text of default title item to "Apple SD Gothic Neo"
      set size of object text of default title item to 34
      make new image with properties {file:POSIX file erdFile, position:{55, 145}, width:1170, height:558}
      set presenter notes to "실습 템플릿의 컬럼명(user_id, course_id)은 일부 유지되어 있으며 발표에서는 도메인 의미를 함께 설명합니다.\n\n[Sources]\n- User-provided image: DBerd.png\n[/Sources]"
    end tell

    -- 9. API list
    set s to make new slide with properties {base slide:master slide "제목 및 구분점"}
    my styleSlide(s, "프론트엔드는 Gateway를 통해 이 API를 호출합니다", "POST   /api/users/register        거래처 계정 등록                 201 / user\nGET     /api/users/me              로그인 사용자 확인              200 / role\nGET     /courses                   의약품 목록·카테고리 조회        200 / ACTIVE products\nGET     /courses/{id}              의약품 상세 조회                 200 / product\nPOST   /api/enrollments           발주 신청                        201 / PENDING\nGET     /enrollments               내 발주 상태 조회                200 / PENDING·ACTIVE\nGET     /api/recommend/{userId}    구매 이력 기반 추천              200 / unpurchased products\n\n※ 기존 템플릿 경로(course, enrollment)는 유지하고 화면·설명에서 의약품/발주 의미로 치환", "실제 Swagger 응답과 기존 코드 경로를 기준으로 정리했습니다.\n\n[Sources]\n- " & notionURL & "\n[/Sources]")

    -- 10. Swagger evidence
    set s to make new slide with properties {base slide:master slide "제목 전용"}
    tell s
      set object text of default title item to "Swagger로 핵심 거래 흐름을 검증했습니다"
      set font of object text of default title item to "Apple SD Gothic Neo"
      set size of object text of default title item to 34
      make new image with properties {file:POSIX file (assetDir & "notion-1.png"), position:{45, 200}, width:350, height:211}
      make new image with properties {file:POSIX file (assetDir & "notion-2.png"), position:{465, 200}, width:350, height:239}
      make new image with properties {file:POSIX file (assetDir & "notion-4.png"), position:{885, 200}, width:350, height:201}
      make new image with properties {file:POSIX file (assetDir & "notion-5.png"), position:{255, 470}, width:350, height:199}
      make new image with properties {file:POSIX file (assetDir & "notion-3.png"), position:{675, 470}, width:350, height:231}
      set presenter notes to "이 화면들은 UI 스냅샷이 아니라 Swagger API 응답 증적입니다.\n\n[Sources]\n- " & notionURL & "\n[/Sources]"
    end tell

    -- 11. Conclusion
    set s to make new slide with properties {base slide:master slide "제목 및 구분점"}
    my styleSlide(s, "작게 완주하고, 데이터가 생긴 뒤 확장합니다", "검증한 것\n• 이해관계자별 Pain Point 정의\n• 로그인–조회–발주 흐름\n• 서비스·데이터 책임 분리\n• Swagger 기반 API 응답\n\n다음 백로그\n• 유사 거래처 추천 · 추천 이유 제공\n• 재주문 시점 알림 · 재고/납기 기반 대체 제품\n\n메디브릿지는 영업사원을 없애는 서비스가 아니라, CSO가 더 적은 인력으로 더 많은 거래처에 도달하게 하는 운영 플랫폼입니다.", "현재 구현과 발전 방향을 분리해 설명합니다.\n\n[Sources]\n- " & backlogURL & "\n- " & sprintURL & "\n- " & notionURL & "\n[/Sources]")
  end tell

  export d to POSIX file outFile as Microsoft PowerPoint
  close d saving no
end tell
