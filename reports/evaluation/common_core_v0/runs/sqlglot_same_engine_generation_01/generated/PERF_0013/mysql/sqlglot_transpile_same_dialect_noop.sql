/* PERF_0013 source layer */ /* Source registry row: SRC_001 (TPC-H) */ /* Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/5.sql */ /* Seed: TPC-H Query 5, Local Supplier Volume Query */ /* Freeze method: manual freeze because local qgen executable was not present. */ /* Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_5 */ /* Substitutions: :1 = MIDDLE EAST; :2 = 1997-01-01; :n -1 = no row limit. */ /* No execution, equivalence, rewrite, or validation claim is made by this file. */ /* TPC-H/TPC-R Local Supplier Volume Query (Q5) */
SELECT
  n_name,
  SUM(l_extendedprice * (
    1 - l_discount
  )) AS revenue
FROM customer, orders, lineitem, supplier, nation, region
WHERE
  c_custkey = o_custkey
  AND l_orderkey = o_orderkey
  AND l_suppkey = s_suppkey
  AND c_nationkey = s_nationkey
  AND s_nationkey = n_nationkey
  AND n_regionkey = r_regionkey
  AND r_name = 'MIDDLE EAST'
  AND o_orderdate >= CAST('1997-01-01' AS DATE)
  AND o_orderdate < CAST('1997-01-01' AS DATE) + INTERVAL '1' YEAR
GROUP BY
  n_name
ORDER BY
  revenue DESC
