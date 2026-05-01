#!/usr/bin/env python3
"""Current-generation cross-dialect result checker for PERF_0056."""

from __future__ import annotations

import json
import pathlib
import sys
from decimal import Decimal, InvalidOperation


CASE_ID = "PERF_0056"
EXPECTED_FUTURE_INPUTS = [
    "runs/pg/source.tsv",
    "runs/mysql/rewrite_pos_01.tsv",
    "runs/mysql/rewrite_neg_01.tsv",
    "runs/spark/rewrite_pos_01.tsv",
    "runs/spark/rewrite_neg_01.tsv",
]
TOLERANCE = Decimal("0.0001")


def load_rows(path: pathlib.Path) -> list[list[str]]:
    text = path.read_text()
    lines = [line.rstrip() for line in text.splitlines()]
    while lines and not lines[-1].strip():
        lines.pop()
    return [[field.strip() for field in line.split("\t")] for line in lines if line.strip()]


def parse_number(value: str) -> Decimal | None:
    try:
        return Decimal(value)
    except InvalidOperation:
        return None


def normalized_rows(path: pathlib.Path) -> list[list[str]]:
    return sorted(load_rows(path), key=lambda row: "\t".join(row))


def values_equal(left_path: pathlib.Path, right_path: pathlib.Path) -> bool:
    left_rows = normalized_rows(left_path)
    right_rows = normalized_rows(right_path)
    if len(left_rows) != len(right_rows):
        return False
    for left_row, right_row in zip(left_rows, right_rows):
        if len(left_row) != len(right_row):
            return False
        for left_field, right_field in zip(left_row, right_row):
            left_num = parse_number(left_field)
            right_num = parse_number(right_field)
            if left_num is not None and right_num is not None:
                if abs(left_num - right_num) > TOLERANCE:
                    return False
            elif left_field != right_field:
                return False
    return True


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print(
            "usage: check_results.py <pg_source.tsv> <mysql_positive.tsv> <mysql_negative.tsv> <spark_positive.tsv> <spark_negative.tsv> <result_check.json>",
            file=sys.stderr,
        )
        return 2

    source_path, mysql_pos_path, mysql_neg_path, spark_pos_path, spark_neg_path, output_path = [
        pathlib.Path(arg) for arg in argv
    ]

    mysql_positive_equal = values_equal(source_path, mysql_pos_path)
    mysql_negative_differs = not values_equal(source_path, mysql_neg_path)
    spark_positive_equal = values_equal(source_path, spark_pos_path)
    spark_negative_differs = not values_equal(source_path, spark_neg_path)
    ok = (
        mysql_positive_equal
        and mysql_negative_differs
        and spark_positive_equal
        and spark_negative_differs
    )

    payload = {
        "case_id": CASE_ID,
        "validation_model": "cross_dialect_reference",
        "source_reference_engine": "pg",
        "target_engines": ["mysql", "spark"],
        "status": "validated" if ok else "failed",
        "ok": ok,
        "draft_only": True,
        "compared_existing_outputs": True,
        "expected_future_inputs": EXPECTED_FUTURE_INPUTS,
        "checks": {
            "mysql_positive_equals_pg_source": mysql_positive_equal,
            "mysql_negative_differs_from_pg_source": mysql_negative_differs,
            "spark_positive_equals_pg_source": spark_positive_equal,
            "spark_negative_differs_from_pg_source": spark_negative_differs,
        },
        "notes": [
            "Existing local outputs compared only.",
            "No database execution was performed by this checker.",
            "No registry validation, admission, formal-review completion, or release-grade claim is implied.",
        ],
    }
    output = pathlib.Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
