
# 사용 주의!! ai로 작성된 코드입니다. 실제 운영 환경에서 사용하기 전에 반드시 검토 후 사용하시기 바랍니다.

# --------------------------------------------------------------
# ecom_실습 DB 및 vscode 환경 세팅 코드
# 작성자 : 최승우
# 작성일 : 26.08.14
# 작성목적 : SKALA 4기 DB 활용 실습 과제 모니터링용 함수
# 함수 설명 :
# 1. connect() : 분석 쿼리용 연결
# 2. connect_maintenance() : Materialized View 등 유지보수 작업용 연결
# 3. query() : 쿼리 실행 및 결과 반환
# 4. explain() : 쿼리 실행 계획 반환
# 5. format_table() : 쿼리 결과를 표 형태로 포맷
# 
# 변경내역 
# 1. 26.08.14 최초 작성
# 
# --------------------------------------------------------------




# 라이브러리 설명
import os
import textwrap
from pathlib import Path
import psycopg
from PIL import Image, ImageDraw, ImageFont

# 환경 변수 및 경로 설정
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql:///skala_ecom_practice4")
ANALYTICS_DATABASE_URL = os.getenv("ANALYTICS_DATABASE_URL", DATABASE_URL)
MAINTENANCE_DATABASE_URL = os.getenv("MAINTENANCE_DATABASE_URL", DATABASE_URL)
BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
FONT_PATH = "/System/Library/Fonts/AppleSDGothicNeo.ttc"


def connect(**kwargs):
    """분석 쿼리용 연결. 운영에서는 읽기 전용 URL을 지정한다."""
    return psycopg.connect(ANALYTICS_DATABASE_URL, **kwargs)


def connect_maintenance(**kwargs):
    """Materialized View 등 유지보수 작업용 연결."""
    return psycopg.connect(MAINTENANCE_DATABASE_URL, **kwargs)


def query(sql, params=None):
    with connect() as connection:
        cursor = connection.execute(sql, params)
        return [column.name for column in cursor.description], cursor.fetchall()


def explain(sql):
    columns, rows = query("EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) " + sql)
    return "\n".join(row[0] for row in rows)


def format_table(columns, rows, max_rows=20):
    shown = rows[:max_rows]
    values = [["NULL" if value is None else str(value) for value in row] for row in shown]
    widths = [
        min(28, max([len(name), *(len(row[i]) for row in values)]))
        for i, name in enumerate(columns)
    ]

    def line(row):
        return " | ".join(str(value)[:width].ljust(width) for value, width in zip(row, widths))

    output = [line(columns), "-+-".join("-" * width for width in widths)]
    output.extend(line(row) for row in values)
    if len(rows) > max_rows:
        output.append(f"... {len(rows) - max_rows} rows omitted")
    output.append(f"total rows: {len(rows)}")
    return "\n".join(output)


def save_capture(name, text):
    """같은 내용을 검색 가능한 .log와 제출용 .png로 저장한다."""
    LOG_DIR.mkdir(exist_ok=True)
    (LOG_DIR / f"{name}.log").write_text(text, encoding="utf-8")

    font = ImageFont.truetype(FONT_PATH, 22)
    wrapped = []
    for line in text.splitlines() or [""]:
        wrapped.extend(textwrap.wrap(line, width=105, replace_whitespace=False) or [""])
    line_height = 31
    image = Image.new("RGB", (1800, max(500, 80 + line_height * len(wrapped))), "#111827")
    draw = ImageDraw.Draw(image)
    draw.multiline_text((40, 35), "\n".join(wrapped), font=font, fill="#f9fafb", spacing=7)
    image.save(LOG_DIR / f"{name}.png")


if __name__ == "__main__":
    columns, rows = query("SELECT current_database(), current_user")
    print(format_table(columns, rows))
