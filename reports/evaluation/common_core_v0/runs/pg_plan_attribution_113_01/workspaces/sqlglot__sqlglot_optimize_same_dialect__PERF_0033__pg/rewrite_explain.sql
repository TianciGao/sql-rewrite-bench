set search_path to attr113_sqlglot_sqlglot_optimize_same_dialect_perf_0033_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
/* PERF_0033 source SQL. */ /* Frozen from TPC-DS query55.tpl via repaired repo-local dsqgen: */ /*   COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi */ /* PostgreSQL normalization only replaces TOP 100 with LIMIT 100. */
SELECT
  "i"."i_brand_id" AS "brand_id",
  "i"."i_brand" AS "brand",
  SUM("ss"."ss_ext_sales_price") AS "ext_price"
FROM "date_dim" AS "d"
JOIN "store_sales" AS "ss"
  ON "d"."d_date_sk" = "ss"."ss_sold_date_sk"
JOIN "item" AS "i"
  ON "i"."i_item_sk" = "ss"."ss_item_sk" AND "i"."i_manager_id" = 36
WHERE
  "d"."d_moy" = 12 AND "d"."d_year" = 2001
GROUP BY
  "i"."i_brand",
  "i"."i_brand_id"
ORDER BY
  "ext_price" DESC,
  "brand_id"
LIMIT 100;
rollback;
