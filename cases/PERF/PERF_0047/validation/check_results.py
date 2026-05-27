#!/usr/bin/env python3
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

CASE_ID = "PERF_0047"
NUMERIC_TOLERANCE = Decimal("0.0001")
NULL_LIKE = {"", "NULL"}


def read_rows(path_str: str):
    text = Path(path_str).read_text()
    lines = text.splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    rows = []
    for line in lines:
        cleaned = line.rstrip()
        if cleaned:
            rows.append(cleaned.split("\t"))
    return rows


def parse_decimal(value: str):
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return None


def fields_equal(left: str, right: str) -> bool:
    left_trimmed = left.strip()
    right_trimmed = right.strip()
    left_num = parse_decimal(left_trimmed)
    right_num = parse_decimal(right_trimmed)
    if left_num is not None and right_num is not None:
        return abs(left_num - right_num) <= NUMERIC_TOLERANCE
    if left_trimmed in NULL_LIKE and right_trimmed in NULL_LIKE:
        return True
    return left_trimmed == right_trimmed


def rows_equal(left_row, right_row) -> bool:
    if len(left_row) != len(right_row):
        return False
    return all(fields_equal(left, right) for left, right in zip(left_row, right_row))


def normalize_row(row):
    return tuple(field.strip() for field in row)


def rowset_equal(left_rows, right_rows) -> bool:
    if len(left_rows) != len(right_rows):
        return False
    remaining = list(right_rows)
    for left_row in sorted(left_rows, key=normalize_row):
        match_index = None
        for idx, candidate in enumerate(remaining):
            if rows_equal(left_row, candidate):
                match_index = idx
                break
        if match_index is None:
            return False
        remaining.pop(match_index)
    return not remaining


def rowset_differs(left_rows, right_rows) -> bool:
    return not rowset_equal(left_rows, right_rows)


def main() -> int:
    if len(sys.argv) != 7:
        print(
            "usage: check_results.py pg_source.tsv mysql_positive.tsv mysql_negative.tsv "
            "spark_positive.tsv spark_negative.tsv output.json",
            file=sys.stderr,
        )
        return 2

    pg_source, mysql_pos, mysql_neg, spark_pos, spark_neg, output_path = sys.argv[1:]

    source_rows = read_rows(pg_source)
    mysql_pos_rows = read_rows(mysql_pos)
    mysql_neg_rows = read_rows(mysql_neg)
    spark_pos_rows = read_rows(spark_pos)
    spark_neg_rows = read_rows(spark_neg)

    checks = {
        "mysql_positive_equals_pg_source": rowset_equal(source_rows, mysql_pos_rows),
        "mysql_negative_differs_from_pg_source": rowset_differs(source_rows, mysql_neg_rows),
        "spark_positive_equals_pg_source": rowset_equal(source_rows, spark_pos_rows),
        "spark_negative_differs_from_pg_source": rowset_differs(source_rows, spark_neg_rows),
    }

    ok = all(checks.values())
    payload = {
        "case_id": CASE_ID,
        "validation_model": "cross_dialect_reference",
        "source_reference_engine": "pg",
        "target_engines": ["mysql", "spark"],
        "status": "validated" if ok else "failed",
        "ok": ok,
        "draft_only": True,
        "compared_existing_outputs": True,
        "expected_future_inputs": [
            "runs/pg/source.tsv",
            "runs/mysql/rewrite_pos_01.tsv",
            "runs/mysql/rewrite_neg_01.tsv",
            "runs/spark/rewrite_pos_01.tsv",
            "runs/spark/rewrite_neg_01.tsv",
        ],
        "checks": checks,
        "notes": [
            "Existing local outputs compared only.",
            "No database execution was performed by this checker.",
            "Case-specific normalization is limited to documented engine output formatting differences.",
            "No registry validation, admission, formal-review completion, or release-grade claim is implied.",
        ],
    }

    Path(output_path).write_text(json.dumps(payload, indent=2) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
