from __future__ import annotations

import sys
from pathlib import Path
from spark_cons_witness import ensure_case_id, expected_text

VARIANTS = ["source", "rewrite_pos_01", "rewrite_neg_01"]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/check_cons_spark_case.py CONS_0003|CONS_0004")
        return 2

    case_id = ensure_case_id(sys.argv[1])
    root = Path("runs") / case_id.lower() / "spark"

    actual = {}
    for variant in VARIANTS:
        path = root / f"{variant}.tsv"
        if not path.exists():
            print(f"missing file: {path}")
            return 1
        actual[variant] = read_text(path)

    print(f"=== {case_id} :: Spark consistency check ===")
    print(f"source: {actual['source']!r}")
    print(f"rewrite_pos_01: {actual['rewrite_pos_01']!r}")
    print(f"rewrite_neg_01: {actual['rewrite_neg_01']!r}")
    print()
    print("source == rewrite_pos_01:", actual["source"] == actual["rewrite_pos_01"])
    print("source == rewrite_neg_01:", actual["source"] == actual["rewrite_neg_01"])
    print()
    print("expected source/positive rows:")
    print(repr(expected_text(case_id, "source")))
    print("expected negative rows:")
    print(repr(expected_text(case_id, "rewrite_neg_01")))

    ok = True
    ok &= actual["source"] == expected_text(case_id, "source")
    ok &= actual["rewrite_pos_01"] == expected_text(case_id, "rewrite_pos_01")
    ok &= actual["rewrite_neg_01"] == expected_text(case_id, "rewrite_neg_01")
    ok &= actual["source"] == actual["rewrite_pos_01"]
    ok &= actual["source"] != actual["rewrite_neg_01"]

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
