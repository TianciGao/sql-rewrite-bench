/* PERF_0006 source layer */ /* Source registry row: SRC_001 (TPC-H) */ /* Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/1.sql */ /* Seed: TPC-H Query 1, Pricing Summary Report Query */ /* Freeze method: manual freeze because local qgen executable was not present. */ /* Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_1 */ /* Substitution: :1 = 96 days. */ /* Frozen cutoff: DATE '1998-08-27' = DATE '1998-12-01' - 96 days. */ /* No execution, equivalence, rewrite, or validation claim is made by this file. */ /* TPC-H/TPC-R Pricing Summary Report Query (Q1) */
SELECT
  l_returnflag,
  l_linestatus,
  SUM(l_quantity) AS sum_qty,
  SUM(l_extendedprice) AS sum_base_price,
  SUM(l_extendedprice * (
    1 - l_discount
  )) AS sum_disc_price,
  SUM(l_extendedprice * (
    1 - l_discount
  ) * (
    1 + l_tax
  )) AS sum_charge,
  AVG(l_quantity) AS avg_qty,
  AVG(l_extendedprice) AS avg_price,
  AVG(l_discount) AS avg_disc,
  COUNT(*) AS count_order
FROM lineitem
WHERE
  l_shipdate <= CAST('1998-08-27' AS DATE)
GROUP BY
  l_returnflag,
  l_linestatus
ORDER BY
  l_returnflag,
  l_linestatus
