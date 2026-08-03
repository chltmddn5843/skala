"""
Practice 2: 파일 I/O, 예외 처리, Pydantic 검증 파이프라인

제출 파일명
캠퍼스명_반_이름.py
"""

from __future__ import annotations

import csv
import json
import logging
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "input" / "sales_input.csv"
MISSING_FILE = BASE_DIR / "input" / "missing.csv"
OUTPUT_DIR = BASE_DIR / "output"
VALID_OUTPUT_FILE = OUTPUT_DIR / "valid_sales.csv"
ERROR_OUTPUT_FILE = OUTPUT_DIR / "validation_errors.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


class SalesRecord(BaseModel):
    """TODO: month, region, amount, category 규칙을 완성하세요."""

    model_config = ConfigDict(str_strip_whitespace=True)

    # TODO


def safe_load_csv(file_path: Path) -> list[dict[str, str]] | None:
    """TODO: try-except-finally로 CSV를 안전하게 읽으세요."""
    # TODO
    raise NotImplementedError


def validate_records(
    raw_data: list[dict[str, str]],
) -> tuple[list[SalesRecord], list[dict[str, Any]]]:
    """TODO: 정상 데이터와 오류 데이터를 분리하세요."""
    # TODO
    raise NotImplementedError


def save_valid_csv(
    records: list[SalesRecord],
    file_path: Path,
) -> None:
    """TODO: model_dump() 결과를 CSV로 저장하세요."""
    # TODO
    raise NotImplementedError


def save_errors_json(
    errors: list[dict[str, Any]],
    file_path: Path,
) -> None:
    """TODO: ensure_ascii=False로 JSON을 저장하세요."""
    # TODO
    raise NotImplementedError


def main() -> None:
    """TODO: 로드 → 검증 → 저장 → 재로딩 순서로 연결하세요."""
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    main()
