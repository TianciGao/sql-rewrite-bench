set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_perf_0007_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT CASE WHEN COUNT(*) = 0 THEN NULL ELSE COALESCE(SUM("l_extendedprice" * "l_discount"), 0) END AS "revenue"
FROM "lineitem"
WHERE "l_shipdate" >= DATE '1995-01-01' AND "l_shipdate" < (DATE '1995-01-01' + INTERVAL '1' YEAR) AND "l_discount" >= 0.09 - 0.01 AND "l_discount" <= 0.09 + 0.01 AND "l_quantity" < 25.00;
rollback;
