from __future__ import annotations

import sys
from contextlib import redirect_stdout
from spark_cons_witness import (
    make_spark,
    register_tables,
    sql_text,
    plan_dir,
    ensure_case_id,
)

VARIANTS = ["source", "rewrite_pos_01", "rewrite_neg_01"]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/collect_spark_cons_plans.py CONS_0003|CONS_0004")
        return 2

    case_id = ensure_case_id(sys.argv[1])
    spark = make_spark(f"{case_id.lower()}-spark-plans")

    try:
        register_tables(spark, case_id)
        out_dir = plan_dir(case_id)

        for variant in VARIANTS:
            query = sql_text(case_id, variant)
            result = spark.sql(query)
            out_path = out_dir / f"{variant}.txt"
            with out_path.open("w", encoding="utf-8") as f:
                with redirect_stdout(f):
                    result.explain(mode="formatted")
            print(f"wrote {out_path}")
    finally:
        spark.stop()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
