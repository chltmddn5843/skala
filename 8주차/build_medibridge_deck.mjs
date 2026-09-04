import fs from "node:fs/promises";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const OUT = "/Users/chltmddn5843/Downloads/skala/8주차/메디브릿지_발표자료.pptx";
const RENDER = "/Users/chltmddn5843/Downloads/skala/8주차/ppt_render";
const ASSET = "/Users/chltmddn5843/Downloads/skala/8주차/ppt_assets";
const FLOW = "/Users/chltmddn5843/Downloads/User Interface and-2026-09-03-054358.png";
const ERD = "/Users/chltmddn5843/Downloads/DBerd.png";
const SRC_BACKLOG = "https://docs.google.com/spreadsheets/d/1X3ji7XSqgxXPO-5Ch4LrFJRvc-r4a7HmHxNoIaG5vfA/edit?gid=1939221835";
const SRC_SPRINT = "https://docs.google.com/spreadsheets/d/1vqYW_Ug6UC_3gNdNb3CemyC6BFcaLFNfj1HtguZfumM/edit?gid=1365266729";
const SRC_NOTION = "https://app.notion.com/p/Sprint1-3d074ceed1e18014a121c34110c90363";

const C = { navy:"#17365D", blue:"#2F6BFF", light:"#EAF2FF", cyan:"#DDF5F5", ink:"#111827", gray:"#667085", line:"#D9DEE7", panel:"#F5F7FA", green:"#169B62", amber:"#D49A00", white:"#FFFFFF", red:"#C83E4D" };
const FONT = "Apple SD Gothic Neo";
const deck = Presentation.create({ slideSize: { width: 1280, height: 720 } });

function box(slide, x,y,w,h, fill=C.white, line=C.line, radius="roundRect") {
  return slide.shapes.add({ geometry:radius, position:{left:x,top:y,width:w,height:h}, fill, line:{style:"solid",fill:line,width:1} });
}
function txt(slide, text, x,y,w,h, size=24, color=C.ink, bold=false, align="left") {
  const s=slide.shapes.add({geometry:"textbox",position:{left:x,top:y,width:w,height:h},fill:"none",line:{style:"solid",fill:"none",width:0}});
  s.text=text; s.text.style={typeface:FONT,fontSize:size,color,bold,alignment:align,verticalAlignment:"middle",autoFit:"shrinkText",insets:{top:2,right:2,bottom:2,left:2}}; return s;
}
function line(slide,x1,y1,x2,y2,color=C.line,width=2,endArrow=false){
  return slide.shapes.add({geometry:"line",position:{left:x1,top:y1,width:x2-x1,height:y2-y1},fill:"none",line:{style:"solid",fill:color,width,endArrowType:endArrow?"triangle":"none"}});
}
function title(slide, t, n, kicker="MEDIBRIDGE · MSA AGILE PRACTICE") {
  slide.background.fill=C.white; txt(slide,kicker,42,24,650,28,14,C.blue,true); txt(slide,t,42,54,1130,62,36,C.ink,true); txt(slide,String(n).padStart(2,"0"),1180,28,55,24,13,C.gray,false,"right"); line(slide,42,126,1238,126,C.line,1);
}
function notes(slide, sources=[], extra="") {
  slide.speakerNotes.textFrame.setText(`${extra}${extra?"\n\n":""}[Sources]\n${sources.map(s=>`- ${s}`).join("\n")}\n[/Sources]`);
}
function pill(slide,label,x,y,w,fill=C.light,color=C.navy){ box(slide,x,y,w,38,fill,fill,"roundRect"); txt(slide,label,x+8,y,w-16,38,16,color,true,"center"); }
function card(slide,x,y,w,h,head,body,accent=C.blue){ box(slide,x,y,w,h,C.panel,C.line); box(slide,x,y,8,h,accent,accent,"rect"); txt(slide,head,x+25,y+20,w-45,35,22,C.ink,true); txt(slide,body,x+25,y+64,w-45,h-82,17,C.gray,false); }
function addImage(slide,path,x,y,w,h,fit="contain",alt=""){ box(slide,x,y,w,h,C.panel,C.line); slide.images.add({path,alt,fit,position:{left:x+2,top:y+2,width:w-4,height:h-4},geometry:"roundRect",borderRadius:"rounded-lg"}); }

// 1 — cover (Codex Grid slide 01: stacked text flow)
{
  const s=deck.slides.add(); s.background.fill=C.white;
  pill(s,"TEAM PROJECT · 5-HOUR AGILE PRACTICE",42,42,330,C.light,C.blue);
  txt(s,"메디브릿지",42,155,760,92,58,C.ink,true);
  txt(s,"영업의 거리를 넘어,\n의약품 공급과 발주를 연결하다",42,255,790,150,34,C.navy,true);
  box(s,900,92,275,440,C.navy,C.navy); txt(s,"CSO",935,145,210,48,26,C.white,true,"center"); line(s,1038,205,1038,265,C.white,3,true); txt(s,"약국·병원",935,278,210,52,26,C.white,true,"center"); line(s,1038,340,1038,400,C.white,3,true); txt(s,"제약회사",935,412,210,52,26,C.white,true,"center");
  txt(s,"비대면 제품 탐색 · 추천 · 발주 플랫폼",42,575,700,42,22,C.gray,false);
  txt(s,"Product Owner 김민주  |  Scrum Master 최승우  |  Front 임형준  |  Backend 권주현  |  Service Planning 전혜민",42,650,1130,28,14,C.gray,false);
  notes(s,[],"발표의 핵심은 개발량보다 이해관계자 가치, 스프린트 의사결정, MSA 통신 경험입니다.");
}

// 2 — stakeholders / pain points (Codex Grid slide 07: three columns)
{
  const s=deck.slides.add(); title(s,"문제는 제품 부족이 아니라 ‘연결의 한계’입니다",2);
  txt(s,"지역·인력·경험에 묶인 영업 구조 때문에 데이터가 구매 의사결정으로 이어지지 않습니다.",42,145,1150,52,23,C.gray);
  card(s,42,225,365,340,"약국·병원","• 다양한 제약사의 유사 제품 비교가 어렵다\n\n• 기존 구매 제품에 머물기 쉽다\n\n• 지역에 따라 제품 탐색 기회가 달라진다",C.blue);
  card(s,458,225,365,340,"CSO 운영사","• 영업사원 1명이 담당할 수 있는 거래처에 한계가 있다\n\n• 거래처별 수요를 체계적으로 활용하기 어렵다\n\n• 경험과 기존 관계에 의존한다",C.amber);
  card(s,874,225,365,340,"제약회사","• 기존 영업망이 닿지 않는 거래처가 있다\n\n• 제품 노출과 신규 판매 기회가 제한된다\n\n• 실제 수요 피드백을 얻기 어렵다",C.green);
  pill(s,"공통 핵심: 판매·주문 이력이 영업과 구매 판단에 충분히 활용되지 않는다",245,610,790,C.navy,C.white);
  notes(s,[],"CSO 현장 영업사원이 아니라 플랫폼 도입을 결정하는 CSO 운영사를 핵심 고객으로 둡니다.");
}

// 3 — solution + AI image (Codex Grid slide 08: half text, half image)
{
  const s=deck.slides.add(); title(s,"셀프서비스 거래 흐름에 추천을 결합합니다",3);
  txt(s,"핵심 서비스",42,155,480,34,18,C.blue,true);
  txt(s,"탐색 → 상세 확인 → 발주 → 상태 확인",42,190,520,52,28,C.ink,true);
  txt(s,"약국·병원이 스스로 제품을 찾고 주문하며, CSO는 더 적은 인력으로 더 넓은 지역에 제안합니다.",42,250,525,90,20,C.gray);
  box(s,42,370,525,175,C.light,C.light); txt(s,"AI의 MVP 역할",66,388,470,32,20,C.navy,true); txt(s,"구매 이력이 있으면 가장 자주 산 약효군을 찾고, 아직 구매하지 않은 관련 제품을 추천합니다. 이력이 없으면 인기 제품을 제시합니다.",66,428,470,92,18,C.navy);
  pill(s,"향후: 유사 거래처 · 재주문 시점 · 대체 제품",42,575,525,C.cyan,C.navy);
  addImage(s,FLOW,650,150,555,500,"contain","구매 이력 기반 의약품 추천 API 흐름");
  notes(s,["User-provided image: User Interface and-2026-09-03-054358.png"],"첨부 그림의 고급 분석 표현은 발전 방향입니다. 현재 MVP는 최빈 카테고리와 미구매 제품을 이용한 규칙 기반 추천입니다.");
}

// 4 — backlog priority
{
  const s=deck.slides.add(); title(s,"백로그는 가치·의존성·실습 가능성으로 정렬했습니다",4);
  const labels=[["1","핵심 가치","사용자가 탐색부터 발주까지 끝낼 수 있는가"],["2","업무 의존성","사용자·제품·주문 데이터가 먼저 존재하는가"],["3","학습 가치","REST, Kafka, 인증 등 MSA 흐름을 경험하는가"],["4","시간·위험","5시간 안에 검증 가능한 크기인가"]];
  labels.forEach((a,i)=>{const y=155+i*105; pill(s,a[0],42,y,52,C.blue,C.white); txt(s,a[1],115,y,195,38,21,C.ink,true); txt(s,a[2],330,y,850,38,19,C.gray); line(s,115,y+56,1180,y+56,C.line,1);});
  box(s,42,585,1196,70,C.navy,C.navy); txt(s,"결론  ·  Sprint 1은 ‘거래 완주’, Sprint 2는 ‘서비스 간 연동과 추천 확장’",70,585,1140,70,23,C.white,true,"center");
  notes(s,[SRC_BACKLOG,SRC_SPRINT],"우선순위는 단순 중요도뿐 아니라 선행 데이터와 5시간 실습 제약을 함께 반영했습니다.");
}

// 5 — sprint 1
{
  const s=deck.slides.add(); title(s,"Sprint 1 — 사용자가 발주까지 완주하는 MVP",5);
  pill(s,"SPRINT GOAL",42,148,150,C.blue,C.white); txt(s,"로그인 → 의약품 조회 → 발주 신청까지 완료",215,146,840,42,25,C.ink,true);
  const steps=[["01","로그인","OAuth2"],["02","목록","GET /courses"],["03","상세","GET /courses/{id}"],["04","발주","POST /api/enrollments"],["05","상태","GET /enrollments"]];
  steps.forEach((a,i)=>{const x=42+i*239; if(i<4) line(s,x+190,345,x+235,345,C.blue,3,true); box(s,x,250,190,190,C.white,C.line); pill(s,a[0],x+18,270,46,C.light,C.blue); txt(s,a[1],x+18,320,154,34,22,C.ink,true); txt(s,a[2],x+18,368,154,46,15,C.gray);});
  card(s,42,490,570,125,"Definition of Done","Swagger 응답 성공 · 상태 저장 확인 · 다음 단계에서 조회 가능",C.green);
  card(s,650,490,588,125,"왜 먼저 구현했나","모든 확장 기능은 사용자·제품·주문 데이터가 있어야 검증할 수 있기 때문",C.amber);
  notes(s,[SRC_BACKLOG,SRC_SPRINT,SRC_NOTION],"Sprint 1 실행표에는 다섯 단계가 완료로 기록되어 있습니다.");
}

// 6 — sprint 2 and semantic correction
{
  const s=deck.slides.add(); title(s,"Sprint 2 — 결제 이벤트와 추천으로 MSA 경험 확장",6);
  const nodes=[[70,"구매 승인","payment-service"],[360,"결제 완료 이벤트","Kafka"],[650,"상태 변경","order-service"],[940,"맞춤 추천","recommend-service"]];
  nodes.forEach((a,i)=>{ if(i<3) line(s,a[0]+220,300,nodes[i+1][0]-20,300,C.blue,4,true); box(s,a[0],225,220,150,i===3?C.light:C.white,i===3?C.blue:C.line); txt(s,a[1],a[0]+15,248,190,42,22,C.ink,true,"center"); txt(s,a[2],a[0]+15,310,190,46,15,C.gray,false,"center"); });
  box(s,70,435,1090,112,"#FFF7E0","#F0C45A"); txt(s,"상태 의미 정정",95,455,220,30,18,C.amber,true); txt(s,"ACTIVE = 입고 완료  ✕     →     ACTIVE = 발주 확정 / 결제 완료  ○",310,447,800,48,23,C.ink,true,"center"); txt(s,"배송·입고 이벤트가 없는 현재 코드에서 ‘입고 완료’는 확인할 수 없습니다.",310,505,800,30,17,C.gray,false,"center");
  pill(s,"Sprint 2 완료 기준: 서비스 간 이벤트 전달 + 주문 상태 반영 + 구매 이력 기반 추천 응답",145,590,990,C.navy,C.white);
  notes(s,[SRC_SPRINT,SRC_NOTION],"발표에서는 코드가 실제로 보장하는 상태만 설명합니다.");
}

// 7 — architecture; connectors first
{
  const s=deck.slides.add(); title(s,"업무와 데이터 책임을 기준으로 5개 서비스로 분리했습니다",7);
  // Connectors first
  line(s,165,250,305,250,C.blue,3,true); line(s,430,250,570,250,C.blue,3,true); line(s,695,250,835,250,C.blue,3,true); line(s,960,250,1090,250,C.blue,3,true);
  line(s,680,393,680,478,C.amber,3,true); line(s,935,393,935,478,C.amber,3,true); line(s,775,540,840,540,C.amber,3,true);
  box(s,50,205,115,90,C.navy,C.navy); txt(s,"Web / App",60,220,95,60,18,C.white,true,"center");
  box(s,305,205,125,90,C.light,C.blue); txt(s,"API\nGateway",320,218,95,65,18,C.navy,true,"center");
  box(s,570,205,125,90,C.white,C.line); txt(s,"Auth\nServer",585,218,95,65,18,C.ink,true,"center");
  box(s,835,205,125,90,C.white,C.line); txt(s,"Eureka",850,223,95,55,18,C.ink,true,"center");
  box(s,1090,205,130,90,C.panel,C.line); txt(s,"서비스\n탐색",1105,218,100,65,18,C.ink,true,"center");
  const sv=[[55,"partner-service","계정·거래처"],[300,"product-service","의약품 정보"],[545,"order-service","발주·상태"],[790,"payment-service","결제·승인"],[1035,"recommend-service","추천"]];
  sv.forEach((a,i)=>{box(s,a[0],350,190,95,i===4?C.light:C.white,i===4?C.blue:C.line);txt(s,a[1],a[0]+10,365,170,30,16,C.ink,true,"center");txt(s,a[2],a[0]+10,400,170,28,15,C.gray,false,"center");});
  box(s,600,485,160,100,"#FFF7E0","#F0C45A"); txt(s,"Kafka",620,510,120,42,24,C.amber,true,"center");
  box(s,840,485,190,100,C.panel,C.line); txt(s,"Event",860,503,150,28,17,C.gray,true,"center"); txt(s,"PaymentCompleted",855,535,160,28,15,C.ink,false,"center");
  pill(s,"REST: 조회·명령     |     Kafka: 결제 완료 이벤트",370,620,540,C.cyan,C.navy);
  notes(s,[],"각 서비스는 자신의 데이터를 소유합니다. 같은 서비스 안에서는 계층·트랜잭션 경계로 격리하고, 서비스 간에는 API 계약과 이벤트로 결합도를 낮춥니다.");
}

// 8 — ERD
{
  const s=deck.slides.add(); title(s,"데이터는 사용자·제품·발주·결제의 결과로 남습니다",8);
  addImage(s,ERD,42,145,1196,440,"contain","메디브릿지 users products orders payments ERD");
  pill(s,"users 1:N products",80,610,240,C.light,C.navy); pill(s,"users 1:N orders",360,610,240,C.light,C.navy); pill(s,"products 1:N orders",640,610,250,C.light,C.navy); pill(s,"orders ↔ payments",930,610,250,C.light,C.navy);
  notes(s,["User-provided image: DBerd.png"],"실습 템플릿의 컬럼명(user_id, course_id)은 일부 유지되어 있으며 발표에서는 도메인 의미를 함께 설명합니다.");
}

// 9 — API table
{
  const s=deck.slides.add(); title(s,"프론트엔드는 Gateway를 통해 이 API를 호출합니다",9);
  const cols=[42,155,470,840,1238];
  box(s,42,150,1196,48,C.navy,C.navy,"rect"); ["Method","Endpoint","역할","핵심 상태/응답"].forEach((h,i)=>txt(s,h,cols[i]+10,150,cols[i+1]-cols[i]-20,48,17,C.white,true));
  const rows=[["POST","/api/users/register","거래처 계정 등록","201 / user"],["GET","/api/users/me","로그인 사용자 확인","200 / role"],["GET","/courses","의약품 목록·카테고리 조회","200 / ACTIVE products"],["GET","/courses/{id}","의약품 상세 조회","200 / product"],["POST","/api/enrollments","발주 신청","201 / PENDING"],["GET","/enrollments","내 발주 상태 조회","200 / PENDING·ACTIVE"],["GET","/api/recommend/{userId}","구매 이력 기반 추천","200 / unpurchased products"]];
  rows.forEach((r,ri)=>{const y=198+ri*58; box(s,42,y,1196,58,ri%2?C.white:C.panel,C.line,"rect"); r.forEach((v,i)=>txt(s,v,cols[i]+10,y,cols[i+1]-cols[i]-20,58,i===1?15:16,i===0?C.blue:C.ink,i===0));});
  txt(s,"※ 기존 템플릿 경로(course, enrollment)는 유지하고 화면·설명에서 의약품/발주 의미로 치환",42,630,1196,30,15,C.gray);
  notes(s,[SRC_NOTION],"실제 Swagger 응답과 기존 코드 경로를 기준으로 정리했습니다.");
}

// 10 — API evidence collage
{
  const s=deck.slides.add(); title(s,"Swagger로 핵심 거래 흐름을 검증했습니다",10);
  const imgs=[[1,42,155,"계정 등록 · 201"],[2,445,155,"목록 조회 · 200"],[4,848,155,"발주 신청 · 201"],[5,245,420,"상태 조회 · 200"],[3,648,420,"상세 조회 · 200"]];
  imgs.forEach(([n,x,y,l])=>{addImage(s,`${ASSET}/notion-${n}.png`,x,y,350,200,"cover",`${l} Swagger 응답`); pill(s,l,x+55,y+168,240,C.navy,C.white);});
  notes(s,[SRC_NOTION],"이 화면들은 UI 스냅샷이 아니라 Swagger API 응답 증적입니다.");
}

// 11 — conclusion
{
  const s=deck.slides.add(); title(s,"작게 완주하고, 데이터가 생긴 뒤 확장합니다",11);
  card(s,42,165,365,300,"검증한 것","• 이해관계자별 Pain Point 정의\n\n• 로그인–조회–발주 흐름\n\n• 서비스·데이터 책임 분리\n\n• Swagger 기반 API 응답",C.green);
  card(s,458,165,365,300,"배운 것","• 백로그는 가치와 의존성으로 정렬\n\n• MSA 경계는 업무 결과 데이터로 설명\n\n• 이벤트가 없는 상태는 주장하지 않기\n\n• 피드백을 다음 Sprint에 반영",C.blue);
  card(s,874,165,365,300,"다음 백로그","• 유사 거래처 추천\n\n• 추천 이유 제공\n\n• 재주문 시점 알림\n\n• 재고·납기 기반 대체 제품",C.amber);
  box(s,42,520,1196,115,C.navy,C.navy); txt(s,"메디브릿지는 영업사원을 없애는 서비스가 아니라,\nCSO가 더 적은 인력으로 더 많은 거래처에 도달하게 하는 운영 플랫폼입니다.",75,535,1130,80,25,C.white,true,"center");
  notes(s,[SRC_BACKLOG,SRC_SPRINT,SRC_NOTION],"마지막으로 현재 구현과 발전 방향을 분리해 설명합니다.");
}

await fs.mkdir(RENDER,{recursive:true});
for (const [i,s] of deck.slides.items.entries()) {
  const stem=`slide-${String(i+1).padStart(2,"0")}`;
  const png=await deck.export({slide:s,format:"png",scale:1});
  await fs.writeFile(`${RENDER}/${stem}.png`,new Uint8Array(await png.arrayBuffer()));
  const layout=await s.export({format:"layout"}); await fs.writeFile(`${RENDER}/${stem}.layout.json`,await layout.text());
}
const montage=await deck.export({format:"webp",montage:true,scale:1}); await fs.writeFile(`${RENDER}/montage.webp`,new Uint8Array(await montage.arrayBuffer()));
const pptx=await PresentationFile.exportPptx(deck); await pptx.save(OUT);
console.log(OUT);
