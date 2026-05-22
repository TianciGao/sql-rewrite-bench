set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_perf_0019_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT "t1"."c_count", COUNT(*) AS "custdist"
FROM (SELECT COUNT("orders"."o_orderkey") AS "c_count"
FROM "customer"
LEFT JOIN "orders" ON "customer"."c_custkey" = "orders"."o_custkey" AND "orders"."o_comment" NOT LIKE '%express%deposits%'
GROUP BY "customer"."c_custkey") AS "t1"
GROUP BY "t1"."c_count"
ORDER BY 2 DESC, "t1"."c_count" DESC;
rollback;
