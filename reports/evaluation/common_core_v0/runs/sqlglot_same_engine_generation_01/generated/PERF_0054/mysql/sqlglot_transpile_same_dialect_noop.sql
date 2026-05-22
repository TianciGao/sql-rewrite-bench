/* PERF_0054 source SQL. */ /* Frozen from TPC-DS query_templates/query3.tpl via repaired repo-local dsqgen: */ /*   COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi */ /* PostgreSQL normalization replaces TOP 100 with LIMIT 100. */
SELECT
  dt.d_year,
  item.i_brand_id AS brand_id,
  item.i_brand AS brand,
  SUM(ss_ext_sales_price) AS sum_agg
FROM date_dim AS dt, store_sales, item
WHERE
  dt.d_date_sk = store_sales.ss_sold_date_sk
  AND store_sales.ss_item_sk = item.i_item_sk
  AND item.i_manufact_id = 436
  AND dt.d_moy = 12
GROUP BY
  dt.d_year,
  item.i_brand,
  item.i_brand_id
ORDER BY
  dt.d_year,
  sum_agg DESC,
  brand_id
LIMIT 100
