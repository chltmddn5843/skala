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

"""
Practice 2: 파일 I/O, 예외 처리, Pydantic 검증 파이프라인

변경 내역
- CSV 파일을 안전하게 읽는 safe_load_csv() 구현
- Pydantic v2 SalesRecord 모델로 판매 데이터 검증
- 정상 데이터와 오류 데이터를 분리해 CSV와 JSON으로 저장
- 저장한 정상 CSV를 다시 읽어 건수 검증
"""

from __future__ import annotations

import csv
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "input" / "sales_input.csv"
MISSING_FILE = BASE_DIR / "input" / "missing.csv"
OUTPUT_DIR = BASE_DIR / "output"
VALID_OUTPUT_FILE = OUTPUT_DIR / "valid_sales.csv"
ERROR_OUTPUT_FILE = OUTPUT_DIR / "validation_errors.json"


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s |%(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


class SalesRecord(BaseModel):
    """판매 데이터 한 행의 검증 규칙을 정의합니다."""

    model_config = ConfigDict(str_strip_whitespace=True)

    month: str = Field(min_length=1)
    region: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: Optional[str] = None

    @field_validator("category", mode="before")
    @classmethod
    def blank_category_to_none(cls, value: Any) -> Optional[str]:
        """비어 있는 category를 선택값인 None으로 변환합니다."""
        if value is None:
            return None

        text = str(value).strip()
        return text or None


def safe_load_csv(file_path: Path) -> Optional[List[Dict[str, str]]]:
    """CSV를 안전하게 읽고 실패하면 None을 반환합니다."""
    try:
        with file_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        logger.info("CSV 로딩 성공:%s (%d건)", file_path.name, len(rows))
        return rows
    except FileNotFoundError:
        logger.error("파일을 찾을 수 없습니다:%s", file_path)
        return None
    except (OSError, csv.Error) as exc:
        logger.error("CSV 로딩 실패:%s", exc)
        return None
    finally:
        print("로딩 종료")


def validate_records(
    raw_data: List[Dict[str, str]],
) -> Tuple[List[SalesRecord], List[Dict[str, Any]]]:
    """원본 데이터를 검증하여 정상 목록과 오류 목록으로 분리합니다."""
    valid: List[SalesRecord] = []
    errors: List[Dict[str, Any]] = []

    for row_number, row in enumerate(raw_data, start=2):
        try:
            valid.append(SalesRecord.model_validate(row))
        except ValidationError as exc:
            print(f"\n[검증 오류] CSV{row_number}행")
            print(exc)
            errors.append(
                {
                    "row": row_number,
                    "error": exc.errors(include_url=False),
                }
            )

    return valid, errors


def save_valid_csv(records: List[SalesRecord], file_path: Path) -> None:
    """정상 레코드를 CSV 파일로 저장합니다."""
    rows = [record.model_dump() for record in records]
    fieldnames = ["month", "region", "amount", "category"]

    with file_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    logger.info("정상 데이터 저장:%s (%d건)", file_path.name, len(rows))


def save_errors_json(errors: List[Dict[str, Any]], file_path: Path) -> None:
    """검증 오류를 한글이 깨지지 않는 JSON 파일로 저장"""
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(errors, file, ensure_ascii=False, indent=2)

    logger.info("오류 데이터 저장:%s (%d건)", file_path.name, len(errors))


def main() -> None:
    """파일 로드, 검증, 저장, 재로딩 검사를 순서대로 실행합니다."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("=== 1. 존재하지 않는 파일 처리 확인 ===")
    missing_result = safe_load_csv(MISSING_FILE)
    assert missing_result is None
    print("[PASS] 없는 파일은 None을 반환했습니다.\n")

    print("=== 2. 입력 CSV 로딩 ===")
    raw_data = safe_load_csv(INPUT_FILE)
    if raw_data is None:
        print("입력 파일을 읽지 못해 프로그램을 종료합니다.")
        return

    print("\n=== 3. Pydantic 데이터 검증 ===")
    valid, errors = validate_records(raw_data)
    print(f"\n정상 데이터:{len(valid)}건")
    print(f"오류 데이터:{len(errors)}건")

    assert len(valid) == 4
    assert len(errors) == 3
    print("[PASS] 정상 4건 / 오류 3건")

    print("\n=== 4. 결과 파일 저장 ===")
    save_valid_csv(valid, VALID_OUTPUT_FILE)
    save_errors_json(errors, ERROR_OUTPUT_FILE)

    print("\n=== 5. 정상 CSV 재로딩 확인 ===")
    reloaded = safe_load_csv(VALID_OUTPUT_FILE)
    assert reloaded is not None
    assert len(reloaded) == 4
    print("[PASS] 재로딩 후 정상 데이터 4건")

    print("\n실습을 완료했습니다.")
    print(f"정상 데이터:{VALID_OUTPUT_FILE}")
    print(f"오류 데이터:{ERROR_OUTPUT_FILE}")


if __name__ == "__main__":
    main()