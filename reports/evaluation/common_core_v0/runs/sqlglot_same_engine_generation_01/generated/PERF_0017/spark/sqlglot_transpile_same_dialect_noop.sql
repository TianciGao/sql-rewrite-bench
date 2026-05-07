/* PERF_0017 source layer */ /* Source registry row: SRC_001 (TPC-H) */ /* Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/10.sql */ /* Seed: TPC-H Query 10, Returned Item Reporting Query */ /* Freeze method: manual freeze because local qgen executable was not used for this batch. */ /* Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_10 */ /* Substitutions: :1 = 1993-11-01; :n 20 = LIMIT 20. */ /* No execution, equivalence, rewrite, or validation claim is made by this file. */ /* TPC-H/TPC-R Returned Item Reporting Query (Q10) */
SELECT
  c_custkey,
  c_name,
  SUM(l_extendedprice * (
    1 - l_discount
  )) AS revenue,
  c_acctbal,
  n_name,
  c_address,
  c_phone,
  c_comment
FROM customer
CROSS JOIN orders
CROSS JOIN lineitem
CROSS JOIN nation
WHERE
  c_custkey = o_custkey
  AND l_orderkey = o_orderkey
  AND o_orderdate >= CAST('1993-11-01' AS DATE)
  AND o_orderdate < CAST('1993-11-01' AS DATE) + INTERVAL '3' MONTH
  AND l_returnflag = 'R'
  AND c_nationkey = n_nationkey
GROUP BY
  c_custkey,
  c_name,
  c_acctbal,
  c_phone,
  n_name,
  c_address,
  c_comment
ORDER BY
  revenue DESC
LIMIT 20
