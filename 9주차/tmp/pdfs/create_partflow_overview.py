from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output/pdf/판교_4반_최승우_PartFlow-개요.pdf"
TMP = Path(__file__).resolve().parent
FONT = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
pdfmetrics.registerFont(TTFont("AppleGothic", FONT))

NAVY = colors.HexColor("#183B5B")
BLUE = colors.HexColor("#2F6B9A")
PALE = colors.HexColor("#EAF2F8")
GRAY = colors.HexColor("#5B6470")
LIGHT = colors.HexColor("#F5F7F9")
BORDER = colors.HexColor("#D3D8DE")


def paragraph(text, style):
    return Paragraph(text, style)


def box(c, x, y, width, height, title, rows, accent=BLUE):
    c.setStrokeColor(BORDER)
    c.setFillColor(colors.white)
    c.roundRect(x, y, width, height, 6, fill=1, stroke=1)
    c.setFillColor(accent)
    c.roundRect(x, y + height - 28, width, 28, 6, fill=1, stroke=0)
    c.rect(x, y + height - 28, width, 6, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("AppleGothic", 11)
    c.drawString(x + 10, y + height - 19, title)
    c.setFillColor(colors.HexColor("#4B5563"))
    c.setFont("AppleGothic", 8.5)
    row_y = y + height - 45
    for row in rows:
        c.setFillColor(LIGHT)
        c.roundRect(x + 10, row_y - 10, width - 20, 18, 3, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#4B5563"))
        c.drawString(x + 16, row_y - 3, row)
        row_y -= 27


def arrow(c, start, end, label=None):
    x1, y1 = start
    x2, y2 = end
    c.setStrokeColor(BLUE)
    c.setFillColor(BLUE)
    c.setLineWidth(1.5)
    c.line(x1, y1, x2, y2)
    angle = 0 if x2 >= x1 else 180
    if abs(y2 - y1) > abs(x2 - x1):
        angle = 90 if y2 >= y1 else -90
    c.saveState()
    c.translate(x2, y2)
    c.rotate(angle)
    path = c.beginPath()
    path.moveTo(0, 0)
    path.lineTo(-7, 3.5)
    path.lineTo(-7, -3.5)
    path.close()
    c.drawPath(path, fill=1, stroke=0)
    c.restoreState()
    if label:
        c.setFillColor(GRAY)
        c.setFont("AppleGothic", 7.5)
        c.drawCentredString((x1 + x2) / 2, (y1 + y2) / 2 + 7, label)


def make_flow(path):
    c = canvas.Canvas(str(path), pagesize=(760, 280))
    c.setFillColor(colors.white)
    c.rect(0, 0, 760, 280, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("AppleGothic", 15)
    c.drawString(24, 245, "PartFlow 사용자 흐름")
    steps = [
        (12, "S01 로그인", "역할 인증"),
        (137, "S02 현황", "LOT/지시 조회"),
        (262, "S03 지시 목록", "등록·선택"),
        (387, "S04 지시 상세", "생산 LOT 등록"),
        (512, "S05 LOT 상세", "이력·관련 LOT"),
        (637, "S06 검사 입력", "측정값 확정"),
    ]
    for x, title, sub in steps:
        c.setFillColor(PALE)
        c.setStrokeColor(BLUE)
        c.roundRect(x, 120, 105, 62, 8, fill=1, stroke=1)
        c.setFillColor(NAVY)
        c.setFont("AppleGothic", 10)
        c.drawCentredString(x + 52, 154, title)
        c.setFillColor(GRAY)
        c.setFont("AppleGothic", 8)
        c.drawCentredString(x + 52, 136, sub)
    for x in [117, 242, 367, 492, 617]:
        arrow(c, (x, 151), (x + 18, 151))
    arrow(c, (690, 120), (565, 92), "확정 후 LOT 상세로")
    c.setFillColor(colors.HexColor("#EAF6EF"))
    c.setStrokeColor(colors.HexColor("#3F8D5A"))
    c.roundRect(475, 32, 155, 38, 7, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#26643C"))
    c.setFont("AppleGothic", 9)
    c.drawCentredString(552, 54, "S05 내부: AI 메모 요약·검토 저장")
    c.setFillColor(GRAY)
    c.setFont("AppleGothic", 8)
    c.drawString(24, 28, "보조 경로: S02에서 LOT을 선택하면 S05로 바로 이동한다. AI 요약은 S05 안에서 생성·검토·저장한다.")
    c.save()


def make_wireframes(path, page):
    c = canvas.Canvas(str(path), pagesize=(760, 560))
    c.setFillColor(colors.white)
    c.rect(0, 0, 760, 560, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("AppleGothic", 15)
    c.drawString(24, 530, f"화면 와이어프레임 {page}/2")
    if page == 1:
        box(c, 25, 270, 210, 210, "S01 로그인", ["아이디", "비밀번호", "[로그인]", "오류: 인증 정보를 확인하세요"])
        box(c, 275, 270, 210, 210, "S02 생산·품질 현황", ["기간 / 품목 필터", "생산수량 · 검사수량", "검사대기 LOT 목록", "[지시 관리] [LOT 선택]"])
        box(c, 525, 270, 210, 210, "S03 작업지시 목록·등록", ["작업지시 목록", "품목 · 목표수량 · 예정일", "[등록]", "행 선택 → 상세"])
        arrow(c, (235, 375), (275, 375), "로그인 성공")
        arrow(c, (485, 375), (525, 375), "지시 관리")
        c.setFillColor(GRAY)
        c.setFont("AppleGothic", 9)
        c.drawString(25, 220, "S01 로그인 - 내부 역할 계정으로 인증한다. 성공하면 S02 현황으로, 실패하면 오류를 표시하고 입력 화면을 유지한다.")
        c.drawString(25, 190, "S02 현황 - 생산·검사 현황과 검사대기 LOT을 조회한다. LOT을 선택하면 S05, 지시 관리를 누르면 S03으로 이동한다.")
        c.drawString(25, 160, "S03 작업지시 목록·등록 - 생산관리자가 품목·목표수량·예정일을 입력해 등록하고, 목록 행을 선택하면 S04로 이동한다.")
    else:
        box(c, 25, 270, 210, 210, "S04 작업지시 상세", ["지시 상태 · 목표/누적 수량", "LOT 목록", "LOT번호 · 생산수량 · 메모", "[시작] [LOT 저장] [종료]"], NAVY)
        box(c, 275, 270, 210, 210, "S05 LOT 상세", ["생산 설비·시간·작업자", "규격 · 측정값 · 검사 결과", "관련 LOT 후보", "[검사 입력] [AI 요약]"], NAVY)
        box(c, 525, 270, 210, 210, "S06 치수 검사 입력", ["규격: 9.90~10.10 mm", "대상 번호별 측정값", "적합/부적합 자동 계산", "[확정]"], NAVY)
        arrow(c, (235, 375), (275, 375), "LOT 선택")
        arrow(c, (485, 375), (525, 375), "검사 입력")
        arrow(c, (630, 270), (380, 245), "확정")
        c.setFillColor(GRAY)
        c.setFont("AppleGothic", 9)
        c.drawString(25, 220, "S04 작업지시 상세 - 작업자가 지시를 시작하고 LOT 생산실적을 등록한다. LOT을 선택하면 S05로 이동한다.")
        c.drawString(25, 190, "S05 LOT 상세 - 생산·검사 이력, 사용 규격, 시간·설비 조건이 같은 관련 LOT 후보를 함께 본다. 품질 담당자는 검사·AI 요약을 실행한다.")
        c.drawString(25, 160, "S06 치수 검사 입력 - 품질 담당자가 대상별 측정값을 모두 입력한다. 서버가 규격 내/외를 판정하고 확정 후 S05로 돌아간다.")
    c.save()


def pdf_to_png(source, destination):
    import subprocess

    prefix = destination.with_suffix("")
    subprocess.run(["pdftoppm", "-f", "1", "-singlefile", "-r", "144", "-png", str(source), str(prefix)], check=True)


flow_pdf = TMP / "partflow_flow.pdf"
wire_1_pdf = TMP / "partflow_wire_1.pdf"
wire_2_pdf = TMP / "partflow_wire_2.pdf"
flow = TMP / "partflow_flow.png"
wire_1 = TMP / "partflow_wire_1.png"
wire_2 = TMP / "partflow_wire_2.png"
make_flow(flow_pdf)
make_wireframes(wire_1_pdf, 1)
make_wireframes(wire_2_pdf, 2)
pdf_to_png(flow_pdf, flow)
pdf_to_png(wire_1_pdf, wire_1)
pdf_to_png(wire_2_pdf, wire_2)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleKo", fontName="AppleGothic", fontSize=23, leading=31, textColor=NAVY, alignment=TA_CENTER, spaceAfter=10))
styles.add(ParagraphStyle(name="SubtitleKo", fontName="AppleGothic", fontSize=11, leading=17, textColor=GRAY, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="H1Ko", fontName="AppleGothic", fontSize=16, leading=23, textColor=NAVY, spaceBefore=10, spaceAfter=9))
styles.add(ParagraphStyle(name="H2Ko", fontName="AppleGothic", fontSize=12, leading=18, textColor=NAVY, spaceBefore=8, spaceAfter=5))
styles.add(ParagraphStyle(name="BodyKo", fontName="AppleGothic", fontSize=9.6, leading=16, textColor=colors.HexColor("#27313B"), spaceAfter=7))
styles.add(ParagraphStyle(name="SmallKo", fontName="AppleGothic", fontSize=8.5, leading=13, textColor=colors.HexColor("#27313B")))
styles.add(ParagraphStyle(name="CaptionKo", fontName="AppleGothic", fontSize=8.7, leading=14, textColor=GRAY, spaceBefore=5, spaceAfter=10))


def page_number(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFont("AppleGothic", 8)
    canvas_obj.setFillColor(GRAY)
    canvas_obj.drawRightString(A4[0] - 18 * mm, 12 * mm, f"PartFlow 프로젝트 기술서 | {doc.page}")
    canvas_obj.restoreState()


doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=18 * mm, bottomMargin=18 * mm)
story = []
story += [Spacer(1, 34 * mm), paragraph("PartFlow 프로젝트 기술서", styles["TitleKo"]), paragraph("생산 기록과 품질 기록을 LOT 단위로 연결하고, AI가 기록 요약을 보조하는 기본 MES 웹 서비스", styles["SubtitleKo"]), Spacer(1, 18 * mm)]
story += [paragraph("프로젝트 한 줄 요약", styles["H1Ko"]), paragraph("<b>PartFlow:</b> 작업지시부터 LOT 생산실적, 구멍 지름 치수 검사, 관련 LOT 조회까지 연결하고 AI가 메모를 사실 중심으로 요약하는 제조 현장 학습용 웹 서비스", styles["BodyKo"])]
story += [paragraph("작성 기준", styles["H2Ko"]), paragraph("기준일 2026-09-08 · 교육용 가상 사례(BR-A 브래킷) · 수업에서 학습한 Vue.js 화면 단위 구성과 페이지 이동을 고려해 설계", styles["BodyKo"])]
story += [Spacer(1, 65 * mm), paragraph("제출 파일명: 판교_4반_최승우_PartFlow-개요.pdf", styles["SubtitleKo"]), PageBreak()]

story += [paragraph("1. 서비스 개요 및 배경", styles["H1Ko"])]
story += [paragraph("<b>목적</b> - 생산 현장에서는 작업지시, 생산실적, 검사 결과가 따로 기록되기 쉽다. PartFlow는 이 기록을 LOT 단위로 연결해 특정 생산 묶음의 생산 이력, 검사 결과, 사용 규격을 한 화면에서 확인하게 한다.", styles["BodyKo"])]
story += [paragraph("<b>대상 사용자</b> - 가상의 자동차·가전 부품 제조 현장에서 작업지시와 생산을 관리하는 생산관리자·작업자, 치수 검사 기록을 확인하는 품질 담당자이다. 이번 프로젝트는 한 공장·한 라인·대표 품목 BR-A의 구멍 지름 검사로 범위를 제한한다.", styles["BodyKo"])]
story += [paragraph("<b>대표 업무 흐름</b> - 작업지시 등록 → LOT 생산실적 등록(설비·생산 시작/종료 시간 포함) → 대상별 지름 측정값 입력 → 서버의 규격 내/외 판정 → LOT 이력 및 관련 LOT 후보 조회", styles["BodyKo"])]
story += [paragraph("AI 도입 필요성", styles["H2Ko"])]
ai_rows = [
    [paragraph("기록 정리 부담", styles["SmallKo"]), paragraph("생산 메모와 검사 메모는 자유문장이라, 교대·인수인계 때 담당자가 여러 기록을 다시 읽고 정리해야 한다.", styles["SmallKo"])],
    [paragraph("AI가 적합한 역할", styles["SmallKo"]), paragraph("LLM은 선택된 기록을 ‘관찰 사실 / 아직 모르는 것 / 다음 확인 질문’으로 재구성해 담당자가 검토할 초안을 빠르게 만든다.", styles["SmallKo"])],
    [paragraph("판단의 경계", styles["SmallKo"]), paragraph("합불 판정과 관련 LOT 선정은 규격 비교·시간/설비 조건의 일반 로직으로 처리한다. AI는 불량 원인, 출하 가능 여부, 영향 범위를 확정하지 않는다.", styles["SmallKo"])],
]
table = Table(ai_rows, colWidths=[36 * mm, 130 * mm])
table.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), PALE), ("GRID", (0, 0), (-1, -1), 0.5, BORDER), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
story += [table, Spacer(1, 8 * mm), paragraph("<b>대표 검사 규격(가상)</b> - BR-A 구멍 지름의 하한 9.90 mm, 상한 10.10 mm를 포함한다. 예를 들어 9.90·10.10은 적합, 9.89·10.11은 부적합이며 서버가 십진수로 판정한다.", styles["BodyKo"]), PageBreak()]

story += [paragraph("2. Actor별 시스템 기능(요구사항)", styles["H1Ko"]), paragraph("화면에서 보이는 버튼과 별개로 서버가 역할을 확인한다. 외부 AI 서비스 장애는 생산·검사 기록을 지우거나 막지 않으며, 요약 생성만 재시도하도록 안내한다.", styles["BodyKo"])]
actors = [
    ["Actor", "역할", "주요 기능 요구사항"],
    ["생산관리자", "작업지시와 전체 현황을 관리", "작업지시 등록 / 작업지시 종료 / 기간·품목별 생산·검사 현황 조회 / LOT 이력 조회"],
    ["작업자", "지시에 따라 생산 실적을 기록", "진행 중인 지시 시작 / LOT번호·생산수량·설비·생산시간·메모 등록 / LOT 이력 조회"],
    ["품질 담당자", "치수 검사와 기록 검토를 수행", "LOT의 대상별 측정값 입력 / 서버 판정 결과 확인 / 관련 LOT 후보 조회 / AI 요약 생성·검토본 저장"],
    ["AI 요약 서비스", "자유문장 기록을 보조적으로 정리", "서버가 제공한 생산·검사·메모를 근거로 사실·미확인 사항·확인 질문 초안 생성 / 원인·합불·출하 판정은 수행하지 않음"],
    ["PartFlow 서버", "권한·업무 규칙·데이터 무결성 보장", "역할 권한 검사 / LOT 번호 중복·수량·상태 검증 / 규격과 측정값 비교 / 관련 LOT 조건 조회 / AI 요청 실패 분리"],
]
actor_table = Table([[paragraph(cell, styles["SmallKo"]) for cell in row] for row in actors], colWidths=[32 * mm, 43 * mm, 91 * mm], repeatRows=1)
actor_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("BACKGROUND", (0, 1), (-1, -1), colors.white), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F6F9FC")]), ("GRID", (0, 0), (-1, -1), 0.5, BORDER), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
story += [actor_table, Spacer(1, 10 * mm), paragraph("<b>핵심 검증 규칙</b> - 작업지시는 대기→진행→종료로 이동한다. LOT당 확정 검사는 한 번만 허용한다. 전수검사이므로 생산수량과 측정값 개수가 일치해야 확정할 수 있다. 관련 LOT은 ‘같은 품목·같은 설비·지정 시간과 생산 시간이 겹침’ 조건을 만족하는 추가 확인 후보이며 불량 확정이 아니다.", styles["BodyKo"]), PageBreak()]

story += [paragraph("3. 서비스 UI 흐름", styles["H1Ko"]), paragraph("Vue.js 화면 단위 구성: LoginView(S01), DashboardView(S02), WorkOrderListView(S03), WorkOrderDetailView(S04), LotDetailView(S05), InspectionFormView(S06). AI 요약은 LOT 상세 내부의 보조 기능으로 구성한다.", styles["BodyKo"]), Image(str(flow), width=174 * mm, height=64 * mm), paragraph("그림 1. 로그인에서 생산·품질 현황을 거쳐 작업지시, LOT, 검사 입력으로 진행하는 전체 흐름이다. 검사 확정 후에는 LOT 상세로 돌아가 결과와 관련 LOT 후보를 확인한다.", styles["CaptionKo"]), paragraph("<b>화면 이동 규칙</b> - 로그인 성공 시 S02로 이동한다. S02의 LOT 선택은 S05로, 지시 관리 메뉴는 S03으로 이동한다. S03에서 지시 행을 선택하면 S04로, S04에서 LOT을 선택하면 S05로 이동한다. S05의 검사 입력은 S06으로, S06의 확정은 S05의 최신 이력으로 돌아간다.", styles["BodyKo"]), PageBreak()]

story += [paragraph("4. 전체 화면 와이어프레임", styles["H1Ko"]), Image(str(wire_1), width=174 * mm, height=128 * mm), paragraph("그림 2. S01~S03 화면. 로그인, 현황, 작업지시 목록·등록 화면에서 각 사용자가 다음 업무로 이동하는 흐름을 표현한다.", styles["CaptionKo"]), Image(str(wire_2), width=174 * mm, height=128 * mm), paragraph("그림 3. S04~S06 화면. 작업지시의 LOT 생산실적을 기록하고, LOT 상세에서 관련 LOT과 기록을 조회하며, 검사 입력 후 결과로 복귀하는 흐름을 표현한다.", styles["CaptionKo"]), Spacer(1, 4 * mm), paragraph("<b>제출 전 확인</b> - 이 PDF에는 전체 화면 와이어프레임 이미지와 각 화면의 이동 설명을 포함했다. 실제 구현에서는 입력 오류 위치 표시, 처리 중 버튼 잠금, 인증 만료와 통신 오류 안내를 공통 상태로 제공한다.", styles["BodyKo"])]

doc.build(story, onFirstPage=page_number, onLaterPages=page_number)
print(OUT)
