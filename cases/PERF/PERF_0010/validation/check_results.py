#!/usr/bin/env python3
"""Current-generation cross-dialect result checker."""

from __future__ import annotations

import json
import pathlib
import sys
from decimal import Decimal, InvalidOperation


CASE_DIR = pathlib.Path(__file__).resolve().parent.parent
CASE_ID = CASE_DIR.name
EXPECTED_FUTURE_INPUTS = [
    "runs/pg/source.tsv",
    "runs/mysql/rewrite_pos_01.tsv",
    "runs/mysql/rewrite_neg_01.tsv",
    "runs/spark/rewrite_pos_01.tsv",
    "runs/spark/rewrite_neg_01.tsv",
]
TOLERANCE = Decimal("0.000001")


def load_rows(path: pathlib.Path) -> list[str]:
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def parse_field(field: str) -> tuple[str, Decimal | str]:
    normalized = field.strip()
    try:
        return ("numeric", Decimal(normalized))
    except InvalidOperation:
        return ("text", normalized)


def parse_row(row: str) -> tuple[tuple[str, Decimal | str], ...]:
    return tuple(parse_field(field) for field in row.split("\t"))


def rows_equal(left: tuple[tuple[str, Decimal | str], ...], right: tuple[tuple[str, Decimal | str], ...]) -> bool:
    if len(left) != len(right):
        return False
    for (left_kind, left_value), (right_kind, right_value) in zip(left, right):
        if left_kind == "numeric" and right_kind == "numeric":
            if abs(left_value - right_value) > TOLERANCE:
                return False
        elif left_kind != right_kind or left_value != right_value:
            return False
    return True


def result_sets_equal(left_rows: list[str], right_rows: list[str]) -> bool:
    if len(left_rows) != len(right_rows):
        return False
    parsed_left = [parse_row(row) for row in left_rows]
    parsed_right = [parse_row(row) for row in right_rows]
    used = [False] * len(parsed_right)
    for left_row in parsed_left:
        match_index = None
        for index, right_row in enumerate(parsed_right):
            if not used[index] and rows_equal(left_row, right_row):
                match_index = index
                break
        if match_index is None:
            return False
        used[match_index] = True
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
    source_rows = load_rows(source_path)
    mysql_positive_rows = load_rows(mysql_pos_path)
    mysql_negative_rows = load_rows(mysql_neg_path)
    spark_positive_rows = load_rows(spark_pos_path)
    spark_negative_rows = load_rows(spark_neg_path)

    mysql_positive_equal = result_sets_equal(source_rows, mysql_positive_rows)
    mysql_negative_differs = not result_sets_equal(source_rows, mysql_negative_rows)
    spark_positive_equal = result_sets_equal(source_rows, spark_positive_rows)
    spark_negative_differs = not result_sets_equal(source_rows, spark_negative_rows)
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
