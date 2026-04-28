#!/usr/bin/env python3
"""Draft result checker for PORT_0004; not executed in this task."""

from __future__ import annotations

import json
import pathlib
import sys


CASE_ID = "PORT_0004"


def read_lines(path: pathlib.Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(path)
    return [line.rstrip("\n") for line in path.read_text().splitlines()]


def normalize_scalar(lines: list[str]) -> list[str]:
    if not lines:
        return []
    return [str(float(lines[0]))]


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(
            "usage: check_results.py <engine> <source.tsv> <positive.tsv> <negative.tsv> <result_check.json>",
            file=sys.stderr,
        )
        return 2

    engine, source_path, positive_path, negative_path, json_path = argv
    source = normalize_scalar(read_lines(pathlib.Path(source_path)))
    positive = normalize_scalar(read_lines(pathlib.Path(positive_path)))
    negative = normalize_scalar(read_lines(pathlib.Path(negative_path)))

    source_positive_equal = source == positive
    source_negative_different = source != negative
    ok = source_positive_equal and source_negative_different

    payload = {
        "case_id": CASE_ID,
        "engine": engine,
        "status": "validated" if ok else "failed",
        "ok": ok,
        "draft_only": True,
        "not_executed_in_current_task": True,
        "checks": {
            "source_positive_equal": source_positive_equal,
            "source_negative_different": source_negative_different,
        },
        "notes": [
            "Draft checker logic only.",
            "Scalar results are normalized numerically before comparison.",
            "No validation was executed in the scaffolding task that created this file.",
        ],
    }
    pathlib.Path(json_path).write_text(json.dumps(payload, indent=2) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
