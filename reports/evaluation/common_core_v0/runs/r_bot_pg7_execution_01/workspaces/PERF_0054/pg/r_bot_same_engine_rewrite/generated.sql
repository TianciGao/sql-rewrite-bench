SELECT "t3"."d_year", "t5"."i_brand_id" AS "brand_id", "t5"."i_brand" AS "brand", SUM("t3"."sum_agg" * "t5"."$f3") AS "sum_agg"
FROM (SELECT "t0"."d_year", "t1"."ss_item_sk", SUM("t0"."$f2" * "t1"."sum_agg") AS "sum_agg"
        FROM (SELECT "d_date_sk", "d_year", COUNT(*) AS "$f2"
                FROM "date_dim"
                WHERE "d_moy" = 12
                GROUP BY "d_date_sk", "d_year") AS "t0"
            INNER JOIN (SELECT "ss_sold_date_sk", "ss_item_sk", SUM("ss_ext_sales_price") AS "sum_agg"
                FROM "store_sales"
                GROUP BY "ss_sold_date_sk", "ss_item_sk") AS "t1" ON "t0"."d_date_sk" = "t1"."ss_sold_date_sk"
        GROUP BY "t0"."d_year", "t1"."ss_item_sk") AS "t3"
    INNER JOIN (SELECT "i_item_sk", "i_brand_id", "i_brand", COUNT(*) AS "$f3"
        FROM "item"
        WHERE "i_manufact_id" = 436
        GROUP BY "i_item_sk", "i_brand_id", "i_brand") AS "t5" ON "t3"."ss_item_sk" = "t5"."i_item_sk"
GROUP BY "t3"."d_year", "t5"."i_brand_id", "t5"."i_brand"
ORDER BY "t3"."d_year", 4 DESC, "t5"."i_brand_id"
FETCH NEXT 100 ROWS ONLY;
