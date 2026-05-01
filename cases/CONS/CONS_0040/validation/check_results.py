#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


ENGINES = ["pg", "mysql", "spark"]
TOLERANCE = Decimal("0.000001")


def _read_lines(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines()]
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def _split_rows(path: Path) -> list[list[str]]:
    return [line.split("\t") for line in _read_lines(path)]


def _to_decimal(value: str) -> Decimal | None:
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return None


def _field_equal(left: str, right: str) -> bool:
    left = left.strip()
    right = right.strip()
    left_num = _to_decimal(left)
    right_num = _to_decimal(right)
    if left_num is not None and right_num is not None:
        return abs(left_num - right_num) <= TOLERANCE
    return left == right


def _row_equal(left: list[str], right: list[str]) -> bool:
    if len(left) != len(right):
        return False
    return all(_field_equal(lf, rf) for lf, rf in zip(left, right))


def _rows_equal(left_rows: list[list[str]], right_rows: list[list[str]]) -> bool:
    if not left_rows and right_rows:
        return False
    if left_rows and not right_rows:
        return False
    if len(left_rows) != len(right_rows):
        return False

    remaining = [row[:] for row in right_rows]
    for left in left_rows:
        match_index = None
        for idx, right in enumerate(remaining):
            if _row_equal(left, right):
                match_index = idx
                break
        if match_index is None:
            return False
        remaining.pop(match_index)
    return not remaining


def _engine_success(payload: dict) -> bool:
    ok = payload.get("ok") is True
    status = str(payload.get("status", "")).lower()
    if ok and status in {"validated", "success", "passed"}:
        return True
    if ok and not status:
        return True
    validated = payload.get("validated")
    return ok and validated is True


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_results.py <output_json>", file=sys.stderr)
        return 2

    case_dir = Path(__file__).resolve().parent.parent
    case_id = case_dir.name
    output_path = Path(sys.argv[1]).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    checks = {}
    failures = []

    for engine in ENGINES:
        run_dir = case_dir / "runs" / engine
        source_rows = _split_rows(run_dir / "source.tsv")
        positive_rows = _split_rows(run_dir / "rewrite_pos_01.tsv")
        negative_rows = _split_rows(run_dir / "rewrite_neg_01.tsv")
        engine_payload = json.loads((run_dir / "result_check.json").read_text(encoding="utf-8"))

        positive_equal = _rows_equal(source_rows, positive_rows)
        negative_differs = not _rows_equal(source_rows, negative_rows)
        engine_ok = _engine_success(engine_payload)

        checks[f"{engine}_positive_equals_source"] = positive_equal
        checks[f"{engine}_negative_differs_from_source"] = negative_differs

        if not positive_equal:
            failures.append(f"{engine} positive != source")
        if not negative_differs:
            failures.append(f"{engine} negative == source")
        if not engine_ok:
            failures.append(f"{engine} result_check not successful")

    ok = not failures
    status = "validated" if ok else "failed"
    payload = {
        "case_id": case_id,
        "validation_model": "engine_local_witness",
        "engines": ENGINES,
        "status": status,
        "ok": ok,
        "draft_only": True,
        "compared_existing_outputs": True,
        "expected_future_inputs": [
            "runs/pg/source.tsv",
            "runs/pg/rewrite_pos_01.tsv",
            "runs/pg/rewrite_neg_01.tsv",
            "runs/pg/result_check.json",
            "runs/mysql/source.tsv",
            "runs/mysql/rewrite_pos_01.tsv",
            "runs/mysql/rewrite_neg_01.tsv",
            "runs/mysql/result_check.json",
            "runs/spark/source.tsv",
            "runs/spark/rewrite_pos_01.tsv",
            "runs/spark/rewrite_neg_01.tsv",
            "runs/spark/result_check.json",
        ],
        "checks": checks,
        "notes": [
            "Existing per-engine local outputs compared only.",
            "No database execution was performed by this checker.",
            "Engine-local witness validation model; not a cross-dialect source-reference claim.",
            "No registry validation, admission, common-core promotion, formal-review completion, or release-grade claim is implied.",
        ],
    }
    if failures:
        payload["failures"] = failures

    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
