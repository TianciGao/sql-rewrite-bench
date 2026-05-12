set search_path to attr113_sqlglot_sqlglot_optimize_same_dialect_perf_0006_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
/* PERF_0006 source layer */ /* Source registry row: SRC_001 (TPC-H) */ /* Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/1.sql */ /* Seed: TPC-H Query 1, Pricing Summary Report Query */ /* Freeze method: manual freeze because local qgen executable was not present. */ /* Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_1 */ /* Substitution: :1 = 96 days. */ /* Frozen cutoff: DATE '1998-08-27' = DATE '1998-12-01' - 96 days. */ /* No execution, equivalence, rewrite, or validation claim is made by this file. */ /* TPC-H/TPC-R Pricing Summary Report Query (Q1) */
SELECT
  "lineitem"."l_returnflag" AS "l_returnflag",
  "lineitem"."l_linestatus" AS "l_linestatus",
  SUM("lineitem"."l_quantity") AS "sum_qty",
  SUM("lineitem"."l_extendedprice") AS "sum_base_price",
  SUM("lineitem"."l_extendedprice" * (
    1 - "lineitem"."l_discount"
  )) AS "sum_disc_price",
  SUM(
    "lineitem"."l_extendedprice" * (
      1 - "lineitem"."l_discount"
    ) * (
      1 + "lineitem"."l_tax"
    )
  ) AS "sum_charge",
  AVG("lineitem"."l_quantity") AS "avg_qty",
  AVG("lineitem"."l_extendedprice") AS "avg_price",
  AVG("lineitem"."l_discount") AS "avg_disc",
  COUNT(*) AS "count_order"
FROM "lineitem" AS "lineitem"
WHERE
  "lineitem"."l_shipdate" <= CAST('1998-08-27' AS DATE)
GROUP BY
  "lineitem"."l_returnflag",
  "lineitem"."l_linestatus"
ORDER BY
  "l_returnflag",
  "l_linestatus";
rollback;
