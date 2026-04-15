from __future__ import annotations

import sys
from spark_cons_witness import (
    make_spark,
    register_tables,
    run_variant,
    rows_to_text,
    write_variant_output,
    ensure_case_id,
)

VARIANTS = ["source", "rewrite_pos_01", "rewrite_neg_01"]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/run_spark_cons_case.py CONS_0003|CONS_0004")
        return 2

    case_id = ensure_case_id(sys.argv[1])
    spark = make_spark(f"{case_id.lower()}-spark-run")

    try:
        register_tables(spark, case_id)

        for variant in VARIANTS:
            rows = run_variant(spark, case_id, variant)
            write_variant_output(case_id, variant, rows)

            print(f"=== Spark :: {case_id} :: {variant} ===")
            text = rows_to_text(rows)
            if text:
                print(text)
            print()
    finally:
        spark.stop()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
