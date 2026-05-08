SELECT "t1"."l_orderkey", SUM("t1"."l_extendedprice" * (1 - "t1"."l_discount")) AS "revenue", "t0"."o_orderdate", "t0"."o_shippriority"
FROM (SELECT *
        FROM "customer"
        WHERE "c_mktsegment" = 'MACHINERY') AS "t"
    INNER JOIN (SELECT *
        FROM "orders"
        WHERE "o_orderdate" < DATE '1995-03-27') AS "t0" ON "t"."c_custkey" = "t0"."o_custkey"
    INNER JOIN (SELECT *
        FROM "lineitem"
        WHERE "l_shipdate" > DATE '1995-03-27') AS "t1" ON "t0"."o_orderkey" = "t1"."l_orderkey"
GROUP BY "t1"."l_orderkey", "t0"."o_orderdate", "t0"."o_shippriority"
ORDER BY 2 DESC, "t0"."o_orderdate"
FETCH NEXT 10 ROWS ONLY;
