/* PERF_0033 source SQL. */ /* Frozen from TPC-DS query55.tpl via repaired repo-local dsqgen: */ /*   COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi */ /* PostgreSQL normalization only replaces TOP 100 with LIMIT 100. */
SELECT
  i.i_brand_id AS brand_id,
  i.i_brand AS brand,
  SUM(ss.ss_ext_sales_price) AS ext_price
FROM date_dim AS d
CROSS JOIN store_sales AS ss
CROSS JOIN item AS i
WHERE
  d.d_date_sk = ss.ss_sold_date_sk
  AND ss.ss_item_sk = i.i_item_sk
  AND i.i_manager_id = 36
  AND d.d_moy = 12
  AND d.d_year = 2001
GROUP BY
  i.i_brand,
  i.i_brand_id
ORDER BY
  ext_price DESC,
  i.i_brand_id
LIMIT 100
