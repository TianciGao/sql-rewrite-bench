set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_perf_0006_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT "l_returnflag", "l_linestatus", COALESCE(SUM("l_quantity"), 0) AS "sum_qty", COALESCE(SUM("l_extendedprice"), 0) AS "sum_base_price", COALESCE(SUM("l_extendedprice" * (1 - "l_discount")), 0) AS "sum_disc_price", COALESCE(SUM("l_extendedprice" * (1 - "l_discount") * (1 + "l_tax")), 0) AS "sum_charge", AVG("l_quantity") AS "avg_qty", AVG("l_extendedprice") AS "avg_price", AVG("l_discount") AS "avg_disc", COUNT(*) AS "count_order"
FROM "lineitem"
WHERE "l_shipdate" <= DATE '1998-08-27'
GROUP BY "l_returnflag", "l_linestatus"
ORDER BY "l_returnflag", "l_linestatus";
rollback;
