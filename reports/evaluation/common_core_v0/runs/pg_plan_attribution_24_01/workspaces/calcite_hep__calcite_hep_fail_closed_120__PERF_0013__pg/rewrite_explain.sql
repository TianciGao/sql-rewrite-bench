set search_path to attr24_calcite_hep__calcite_hep_fail_closed_120__perf_0013__;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT "nation"."n_name", CASE WHEN COUNT("lineitem"."l_extendedprice" * (1 - "lineitem"."l_discount")) = 0 THEN NULL ELSE COALESCE(SUM("lineitem"."l_extendedprice" * (1 - "lineitem"."l_discount")), 0) END AS "revenue"
FROM "customer",
"orders",
"lineitem",
"supplier",
"nation",
"region"
WHERE "customer"."c_custkey" = "orders"."o_custkey" AND "lineitem"."l_orderkey" = "orders"."o_orderkey" AND ("lineitem"."l_suppkey" = "supplier"."s_suppkey" AND "customer"."c_nationkey" = "supplier"."s_nationkey") AND ("supplier"."s_nationkey" = "nation"."n_nationkey" AND "nation"."n_regionkey" = "region"."r_regionkey" AND ("region"."r_name" = 'MIDDLE EAST' AND ("orders"."o_orderdate" >= DATE '1997-01-01' AND "orders"."o_orderdate" < (DATE '1997-01-01' + INTERVAL '1' YEAR))))
GROUP BY "nation"."n_name"
ORDER BY 2 DESC;
rollback;
