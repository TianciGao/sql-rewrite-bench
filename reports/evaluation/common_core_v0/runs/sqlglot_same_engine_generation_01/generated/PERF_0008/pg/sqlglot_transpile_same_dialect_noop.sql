/* PERF_0008 source layer */ /* Source registry row: SRC_001 (TPC-H) */ /* Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/3.sql */ /* Seed: TPC-H Query 3, Shipping Priority Query */ /* Freeze method: manual freeze because local qgen executable was not present. */ /* Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_3 */ /* Substitutions: :1 = MACHINERY; :2 = 1995-03-27; :n 10 = LIMIT 10. */ /* No execution, equivalence, rewrite, or validation claim is made by this file. */ /* TPC-H/TPC-R Shipping Priority Query (Q3) */
SELECT
  l_orderkey,
  SUM(l_extendedprice * (
    1 - l_discount
  )) AS revenue,
  o_orderdate,
  o_shippriority
FROM customer, orders, lineitem
WHERE
  c_mktsegment = 'MACHINERY'
  AND c_custkey = o_custkey
  AND l_orderkey = o_orderkey
  AND o_orderdate < CAST('1995-03-27' AS DATE)
  AND l_shipdate > CAST('1995-03-27' AS DATE)
GROUP BY
  l_orderkey,
  o_orderdate,
  o_shippriority
ORDER BY
  revenue DESC,
  o_orderdate
LIMIT 10
