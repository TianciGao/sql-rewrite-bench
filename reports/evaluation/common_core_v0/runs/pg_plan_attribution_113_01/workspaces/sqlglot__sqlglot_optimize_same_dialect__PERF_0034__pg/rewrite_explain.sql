set search_path to attr113_sqlglot_sqlglot_optimize_same_dialect_perf_0034_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
WITH "_u_0" AS (
  SELECT
    "item"."i_item_id" AS "i_item_id"
  FROM "item" AS "item"
  WHERE
    "item"."i_color" IN ('orchid', 'chiffon', 'lace')
  GROUP BY
    "item"."i_item_id"
), "ss" AS (
  SELECT
    "i"."i_item_id" AS "i_item_id",
    SUM("ss"."ss_ext_sales_price") AS "total_sales"
  FROM "store_sales" AS "ss"
  JOIN "date_dim" AS "d"
    ON "d"."d_date_sk" = "ss"."ss_sold_date_sk"
    AND "d"."d_moy" = 1
    AND "d"."d_year" = 2000
  JOIN "customer_address" AS "ca"
    ON "ca"."ca_address_sk" = "ss"."ss_addr_sk" AND "ca"."ca_gmt_offset" = -8
  JOIN "item" AS "i"
    ON "i"."i_item_sk" = "ss"."ss_item_sk"
  LEFT JOIN "_u_0" AS "_u_0"
    ON "_u_0"."i_item_id" = "i"."i_item_id"
  WHERE
    NOT "_u_0"."i_item_id" IS NULL
  GROUP BY
    "i"."i_item_id"
), "cs" AS (
  SELECT
    "i"."i_item_id" AS "i_item_id",
    SUM("cs"."cs_ext_sales_price") AS "total_sales"
  FROM "catalog_sales" AS "cs"
  JOIN "date_dim" AS "d"
    ON "cs"."cs_sold_date_sk" = "d"."d_date_sk"
    AND "d"."d_moy" = 1
    AND "d"."d_year" = 2000
  JOIN "customer_address" AS "ca"
    ON "ca"."ca_address_sk" = "cs"."cs_bill_addr_sk" AND "ca"."ca_gmt_offset" = -8
  JOIN "item" AS "i"
    ON "cs"."cs_item_sk" = "i"."i_item_sk"
  LEFT JOIN "_u_0" AS "_u_1"
    ON "_u_1"."i_item_id" = "i"."i_item_id"
  WHERE
    NOT "_u_1"."i_item_id" IS NULL
  GROUP BY
    "i"."i_item_id"
), "ws" AS (
  SELECT
    "i"."i_item_id" AS "i_item_id",
    SUM("ws"."ws_ext_sales_price") AS "total_sales"
  FROM "web_sales" AS "ws"
  JOIN "date_dim" AS "d"
    ON "d"."d_date_sk" = "ws"."ws_sold_date_sk"
    AND "d"."d_moy" = 1
    AND "d"."d_year" = 2000
  JOIN "customer_address" AS "ca"
    ON "ca"."ca_address_sk" = "ws"."ws_bill_addr_sk" AND "ca"."ca_gmt_offset" = -8
  JOIN "item" AS "i"
    ON "i"."i_item_sk" = "ws"."ws_item_sk"
  LEFT JOIN "_u_0" AS "_u_2"
    ON "_u_2"."i_item_id" = "i"."i_item_id"
  WHERE
    NOT "_u_2"."i_item_id" IS NULL
  GROUP BY
    "i"."i_item_id"
), "tmp1" AS (
  SELECT
    "ss"."i_item_id" AS "i_item_id",
    "ss"."total_sales" AS "total_sales"
  FROM "ss" AS "ss"
  UNION ALL
  SELECT
    "cs"."i_item_id" AS "i_item_id",
    "cs"."total_sales" AS "total_sales"
  FROM "cs" AS "cs"
  UNION ALL
  SELECT
    "ws"."i_item_id" AS "i_item_id",
    "ws"."total_sales" AS "total_sales"
  FROM "ws" AS "ws"
)
SELECT
  "tmp1"."i_item_id" AS "i_item_id",
  SUM("tmp1"."total_sales") AS "total_sales"
FROM "tmp1" AS "tmp1"
GROUP BY
  "tmp1"."i_item_id"
ORDER BY
  "total_sales",
  "i_item_id"
LIMIT 100;
rollback;
