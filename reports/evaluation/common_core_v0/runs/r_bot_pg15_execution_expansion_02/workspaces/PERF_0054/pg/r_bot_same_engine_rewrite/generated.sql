SELECT "t1"."d_year", "t1"."i_brand_id" AS "brand_id", "t1"."i_brand" AS "brand", "t1"."sum_agg"
FROM (SELECT "date_dim"."d_year", "item"."i_brand_id", "item"."i_brand", SUM("store_sales"."ss_ext_sales_price") AS "sum_agg"
        FROM "date_dim",
            "store_sales",
            "item"
        WHERE "date_dim"."d_date_sk" = "store_sales"."ss_sold_date_sk" AND "store_sales"."ss_item_sk" = "item"."i_item_sk" AND "item"."i_manufact_id" = 436 AND "date_dim"."d_moy" = 12
        GROUP BY "date_dim"."d_year", "item"."i_brand_id", "item"."i_brand"
        ORDER BY "date_dim"."d_year", 4 DESC, "item"."i_brand_id"
        FETCH NEXT 100 ROWS ONLY) AS "t1";
