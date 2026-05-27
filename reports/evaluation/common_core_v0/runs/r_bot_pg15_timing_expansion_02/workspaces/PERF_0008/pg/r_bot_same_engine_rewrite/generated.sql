SELECT "t3"."l_orderkey", SUM("t3"."l_extendedprice" * (1 - "t3"."l_discount")) AS "revenue", "t1"."o_orderdate", "t1"."o_shippriority"
FROM (SELECT *
        FROM "customer"
        WHERE "c_mktsegment" = 'MACHINERY') AS "t"
    INNER JOIN (SELECT *
        FROM (SELECT *
                FROM "orders"
                WHERE "o_orderdate" < DATE '1995-03-27') AS "t0"
        WHERE "o_custkey" IS NOT NULL) AS "t1" ON "t"."c_custkey" = "t1"."o_custkey"
    INNER JOIN (SELECT *
        FROM (SELECT *
                FROM "lineitem"
                WHERE "l_shipdate" > DATE '1995-03-27') AS "t2"
        WHERE "l_orderkey" IS NOT NULL) AS "t3" ON "t1"."o_orderkey" = "t3"."l_orderkey"
GROUP BY "t3"."l_orderkey", "t1"."o_orderdate", "t1"."o_shippriority"
ORDER BY 2 DESC, "t1"."o_orderdate"
FETCH NEXT 10 ROWS ONLY;
