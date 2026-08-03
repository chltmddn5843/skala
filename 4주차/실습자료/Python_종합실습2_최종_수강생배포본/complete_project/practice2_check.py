from __future__ import annotations

import csv
import json
import tempfile
from pathlib import Path

from pydantic import ValidationError

from practice2 import (
    INPUT_FILE,
    SalesRecord,
    safe_load_csv,
    save_errors_json,
    save_valid_csv,
    validate_records,
)


def pass_message(message: str) -> None:
    print(f"[PASS] {message}")


def main() -> None:
    raw_data = safe_load_csv(INPUT_FILE)
    assert raw_data is not None
    assert len(raw_data) == 7
    pass_message("CSV 입력 7건 로딩")

    with tempfile.TemporaryDirectory() as temp_dir:
        missing_file = Path(temp_dir) / "missing.csv"
        assert safe_load_csv(missing_file) is None
        pass_message("없는 파일에서 None 반환")

        try:
            SalesRecord(month="", region="서울", amount=1000)
        except ValidationError:
            pass_message("비어 있는 month 검증")
        else:
            raise AssertionError(
                "비어 있는 month가 ValidationError를 발생시키지 않았습니다."
            )

        try:
            SalesRecord(month="2026-01", region="서울", amount=0)
        except ValidationError:
            pass_message("amount > 0 검증")
        else:
            raise AssertionError(
                "amount=0이 ValidationError를 발생시키지 않았습니다."
            )

        valid, errors = validate_records(raw_data)
        assert len(valid) == 4
        assert len(errors) == 3
        pass_message("정상 4건 / 오류 3건 분리")

        assert valid[2].category is None
        pass_message("category 선택값 처리")

        valid_path = Path(temp_dir) / "valid_sales.csv"
        error_path = Path(temp_dir) / "validation_errors.json"

        save_valid_csv(valid, valid_path)
        save_errors_json(errors, error_path)

        with valid_path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            reloaded = list(csv.DictReader(file))

        assert len(reloaded) == 4
        pass_message("정상 CSV 저장 및 재로딩")

        with error_path.open("r", encoding="utf-8") as file:
            error_data = json.load(file)

        assert len(error_data) == 3
        assert all(
            "row" in item and "error" in item
            for item in error_data
        )
        pass_message("오류 JSON 저장 및 구조 확인")

        dumped = valid[0].model_dump()
        assert dumped["month"] == "2026-01"
        pass_message("Pydantic v2 model_dump() 사용")

    print("\n전체 검사를 통과했습니다.")


if __name__ == "__main__":
    main()
