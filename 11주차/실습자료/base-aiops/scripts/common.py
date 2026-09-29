"""AIOps 5단계 실습 전체가 공유하는 데이터 모델·유틸리티.

이 실습 전체(자동 발견/베이스라이닝/이상탐지/근본원인분석/원격조치)가 공유하는
데이터 모델과 파일 입출력 유틸리티를 담는다.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"


@dataclass
class MetricPoint:
    timestamp: int
    service: str
    latency_ms: float


@dataclass
class Deploy:
    id: str
    service: str
    time: int  # 분 단위 타임스탬프(MetricPoint.timestamp와 같은 축)
    commits: list[str] = field(default_factory=list)


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, default=_default)


def _default(o):
    if hasattr(o, "__dataclass_fields__"):
        return asdict(o)
    raise TypeError(f"Object of type {type(o)} is not JSON serializable")


def load_metrics_csv(path: Path) -> list[MetricPoint]:
    import csv

    points = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            points.append(
                MetricPoint(
                    timestamp=int(row["timestamp"]),
                    service=row["service"],
                    latency_ms=float(row["latency_ms"]),
                )
            )
    return points
