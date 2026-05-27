#!/usr/bin/env python3
"""Draft cross-dialect result checker for PORT_0005; not executed in this task."""

from __future__ import annotations

import json
import pathlib
import sys


CASE_ID = "PORT_0005"
EXPECTED_FILES = {
    "pg_source": "runs/pg/source.tsv",
    "mysql_positive": "runs/mysql/rewrite_pos_01.tsv",
    "mysql_negative": "runs/mysql/rewrite_neg_01.tsv",
    "spark_positive": "runs/spark/rewrite_pos_02_spark.tsv",
    "spark_negative": "runs/spark/rewrite_neg_02_spark.tsv",
}


def read_lines(path: pathlib.Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(path)
    return [line.rstrip("\n") for line in path.read_text().splitlines()]


def normalize_lines(lines: list[str]) -> list[str]:
    normalized = [line.strip() for line in lines]
    normalized.sort()
    return normalized


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print(
            "usage: check_results.py <pg_source.tsv> <mysql_positive.tsv> <mysql_negative.tsv> <spark_positive.tsv> <spark_negative.tsv> <result_check.json>",
            file=sys.stderr,
        )
        return 2

    source_path, mysql_pos_path, mysql_neg_path, spark_pos_path, spark_neg_path, json_path = argv
    source = normalize_lines(read_lines(pathlib.Path(source_path)))
    mysql_positive = normalize_lines(read_lines(pathlib.Path(mysql_pos_path)))
    mysql_negative = normalize_lines(read_lines(pathlib.Path(mysql_neg_path)))
    spark_positive = normalize_lines(read_lines(pathlib.Path(spark_pos_path)))
    spark_negative = normalize_lines(read_lines(pathlib.Path(spark_neg_path)))

    mysql_positive_equal = source == mysql_positive
    mysql_negative_different = source != mysql_negative
    spark_positive_equal = source == spark_positive
    spark_negative_different = source != spark_negative
    ok = (
        mysql_positive_equal
        and mysql_negative_different
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
            "mysql_positive_equals_pg_source": mysql_positive_equal,
            "mysql_negative_differs_from_pg_source": mysql_negative_different,
            "spark_positive_equals_pg_source": spark_positive_equal,
            "spark_negative_differs_from_pg_source": spark_negative_different,
        },
        "notes": [
            "Draft cross-dialect checker logic only.",
            "PostgreSQL source output is treated as the semantic reference.",
            "Top-1 TSV outputs are normalized by trimming and sorting before comparison.",
            "The checker will fail if any required TSV file is missing.",
            "This checker compares existing PostgreSQL, MySQL, and Spark TSV outputs only.",
            "No registry validation or admission claim is implied.",
        ],
    }
    pathlib.Path(json_path).write_text(json.dumps(payload, indent=2) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
