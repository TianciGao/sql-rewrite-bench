/* PERF_0007 source layer */ /* Source registry row: SRC_001 (TPC-H) */ /* Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/6.sql */ /* Seed: TPC-H Query 6, Forecasting Revenue Change Query */ /* Freeze method: manual freeze because local qgen executable was not present. */ /* Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_6 */ /* Substitutions: :1 = 1995-01-01, :2 = 0.09, :3 = 25. */ /* Row limit directive: :n -1 means no row limit. */ /* TPC-H/TPC-R Forecasting Revenue Change Query (Q6) */
SELECT
  SUM(l_extendedprice * l_discount) AS revenue
FROM lineitem
WHERE
  l_shipdate >= CAST('1995-01-01' AS DATE)
  AND l_shipdate < CAST('1995-01-01' AS DATE) + INTERVAL '1 YEAR'
  AND l_discount BETWEEN 0.09 - 0.01 AND 0.09 + 0.01
  AND l_quantity < 25
