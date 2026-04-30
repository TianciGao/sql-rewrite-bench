#!/usr/bin/env python3
"""Current-generation cross-dialect result checker for PERF_0026."""

from __future__ import annotations

import json
import pathlib
import sys
from decimal import Decimal, InvalidOperation


CASE_ID = "PERF_0026"
EXPECTED_FUTURE_INPUTS = [
    "runs/pg/source.tsv",
    "runs/mysql/rewrite_pos_01.tsv",
    "runs/mysql/rewrite_neg_01.tsv",
    "runs/spark/rewrite_pos_01.tsv",
    "runs/spark/rewrite_neg_01.tsv",
]
TOLERANCE = Decimal("0.000001")


def load_lines(path: pathlib.Path) -> list[str]:
    text = path.read_text()
    return [line.strip() for line in text.splitlines() if line.strip()]


def load_value(path: pathlib.Path) -> tuple[str, Decimal | tuple[str, ...]]:
    lines = load_lines(path)
    if len(lines) == 1:
        try:
            return ("numeric", Decimal(lines[0]))
        except InvalidOperation:
            pass
    return ("text", tuple(sorted(lines)))


def values_equal(left: tuple[str, Decimal | tuple[str, ...]], right: tuple[str, Decimal | tuple[str, ...]]) -> bool:
    left_kind, left_value = left
    right_kind, right_value = right
    if left_kind == "numeric" and right_kind == "numeric":
        return abs(left_value - right_value) <= TOLERANCE
    return left == right


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
    source = load_value(source_path)
    mysql_positive = load_value(mysql_pos_path)
    mysql_negative = load_value(mysql_neg_path)
    spark_positive = load_value(spark_pos_path)
    spark_negative = load_value(spark_neg_path)

    mysql_positive_equal = values_equal(source, mysql_positive)
    mysql_negative_differs = not values_equal(source, mysql_negative)
    spark_positive_equal = values_equal(source, spark_positive)
    spark_negative_differs = not values_equal(source, spark_negative)
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
