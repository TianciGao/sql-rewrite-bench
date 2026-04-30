#!/usr/bin/env python3
"""Draft cross-dialect result checker for PORT_0024."""

from __future__ import annotations

import json
import pathlib
import sys
from decimal import Decimal


CASE_ID = "PORT_0024"
EXPECTED_FILES = {
    "mysql_source": "runs/mysql/source.tsv",
    "pg_positive": "runs/pg/rewrite_pos_01.tsv",
    "pg_negative": "runs/pg/rewrite_neg_01.tsv",
    "spark_positive": "runs/spark/rewrite_pos_01.tsv",
    "spark_negative": "runs/spark/rewrite_neg_01.tsv",
}
TOLERANCE = Decimal("0.000001")


def read_scalar(path: pathlib.Path) -> Decimal:
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text().strip()
    if not text:
        raise ValueError(f"empty scalar output: {path}")
    return Decimal(text)


def is_close(left: Decimal, right: Decimal) -> bool:
    return abs(left - right) <= TOLERANCE


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print(
            "usage: check_results.py <mysql_source.tsv> <pg_positive.tsv> <pg_negative.tsv> <spark_positive.tsv> <spark_negative.tsv> <result_check.json>",
            file=sys.stderr,
        )
        return 2

    source_path, pg_pos_path, pg_neg_path, spark_pos_path, spark_neg_path, json_path = argv
    source = read_scalar(pathlib.Path(source_path))
    pg_positive = read_scalar(pathlib.Path(pg_pos_path))
    pg_negative = read_scalar(pathlib.Path(pg_neg_path))
    spark_positive = read_scalar(pathlib.Path(spark_pos_path))
    spark_negative = read_scalar(pathlib.Path(spark_neg_path))

    pg_positive_equal = is_close(source, pg_positive)
    pg_negative_different = not is_close(source, pg_negative)
    spark_positive_equal = is_close(source, spark_positive)
    spark_negative_different = not is_close(source, spark_negative)
    ok = (
        pg_positive_equal
        and pg_negative_different
        and spark_positive_equal
        and spark_negative_different
    )

    payload = {
        "case_id": CASE_ID,
        "validation_model": "cross_dialect_reference",
        "status": "validated" if ok else "failed",
        "ok": ok,
        "draft_only": True,
        "compared_existing_outputs": True,
        "expected_future_inputs": EXPECTED_FILES,
        "checks": {
            "pg_positive_equals_mysql_source": pg_positive_equal,
            "pg_negative_differs_from_mysql_source": pg_negative_different,
            "spark_positive_equals_mysql_source": spark_positive_equal,
            "spark_negative_differs_from_mysql_source": spark_negative_different,
        },
        "notes": [
            "Draft cross-dialect checker logic only.",
            "MySQL source output is treated as the semantic reference.",
            "Scalar outputs are normalized with Decimal parsing and a small tolerance before comparison.",
            "The checker will fail if any required TSV file is missing.",
            "This checker compares existing MySQL, PostgreSQL, and Spark TSV outputs only.",
            "No registry validation or admission claim is implied.",
        ],
    }
    output_path = pathlib.Path(json_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
