set search_path to attr113_sqlglot_sqlglot_transpile_same_dialect_noop_perf_001;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
/* PERF_0019 source layer */ /* Source registry row: SRC_001 (TPC-H) */ /* Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/13.sql */ /* Seed: TPC-H Query 13, Customer Distribution Query */ /* Freeze method: manual freeze because local qgen executable was not used for this batch. */ /* Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_13 */ /* Substitutions: :1 = express; :2 = deposits; :n -1 = no row limit. */ /* No execution, equivalence, rewrite, or validation claim is made by this file. */ /* TPC-H/TPC-R Customer Distribution Query (Q13) */
SELECT
  c_count,
  COUNT(*) AS custdist
FROM (
  SELECT
    c_custkey,
    COUNT(o_orderkey)
  FROM customer
  LEFT OUTER JOIN orders
    ON c_custkey = o_custkey AND NOT o_comment LIKE '%express%deposits%'
  GROUP BY
    c_custkey
) AS c_orders(c_custkey, c_count)
GROUP BY
  c_count
ORDER BY
  custdist DESC,
  c_count DESC;
rollback;
