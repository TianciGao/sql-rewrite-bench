SELECT "nation"."n_name", SUM("lineitem"."l_extendedprice" * (1 - "lineitem"."l_discount")) AS "revenue"
FROM "customer"
    INNER JOIN (SELECT *
        FROM "orders"
        WHERE "o_orderdate" >= DATE '1997-01-01' AND "o_orderdate" < DATE '1998-01-01') AS "t" ON "customer"."c_custkey" = "t"."o_custkey"
    INNER JOIN "lineitem" ON "t"."o_orderkey" = "lineitem"."l_orderkey"
    INNER JOIN "supplier" ON "lineitem"."l_suppkey" = "supplier"."s_suppkey" AND "customer"."c_nationkey" = "supplier"."s_nationkey"
    INNER JOIN "nation" ON "supplier"."s_nationkey" = "nation"."n_nationkey"
    INNER JOIN (SELECT *
        FROM "region"
        WHERE "r_name" = 'MIDDLE EAST') AS "t0" ON "nation"."n_regionkey" = "t0"."r_regionkey"
GROUP BY "nation"."n_name"
ORDER BY 2 DESC;
