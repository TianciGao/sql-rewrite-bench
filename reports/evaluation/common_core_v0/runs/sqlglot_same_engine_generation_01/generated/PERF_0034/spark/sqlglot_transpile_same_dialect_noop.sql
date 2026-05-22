/* PERF_0034 source SQL. */ /* Frozen from TPC-DS query56.tpl via repaired repo-local dsqgen: */ /*   COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi */ /* PostgreSQL normalization only replaces TOP 100 with LIMIT 100. */
WITH ss AS (
  SELECT
    i.i_item_id,
    SUM(ss.ss_ext_sales_price) AS total_sales
  FROM store_sales AS ss
  CROSS JOIN date_dim AS d
  CROSS JOIN customer_address AS ca
  CROSS JOIN item AS i
  WHERE
    i.i_item_id IN (
      SELECT
        i_item_id
      FROM item
      WHERE
        i_color IN ('orchid', 'chiffon', 'lace')
    )
    AND ss.ss_item_sk = i.i_item_sk
    AND ss.ss_sold_date_sk = d.d_date_sk
    AND d.d_year = 2000
    AND d.d_moy = 1
    AND ss.ss_addr_sk = ca.ca_address_sk
    AND ca.ca_gmt_offset = -8
  GROUP BY
    i.i_item_id
), cs AS (
  SELECT
    i.i_item_id,
    SUM(cs.cs_ext_sales_price) AS total_sales
  FROM catalog_sales AS cs
  CROSS JOIN date_dim AS d
  CROSS JOIN customer_address AS ca
  CROSS JOIN item AS i
  WHERE
    i.i_item_id IN (
      SELECT
        i_item_id
      FROM item
      WHERE
        i_color IN ('orchid', 'chiffon', 'lace')
    )
    AND cs.cs_item_sk = i.i_item_sk
    AND cs.cs_sold_date_sk = d.d_date_sk
    AND d.d_year = 2000
    AND d.d_moy = 1
    AND cs.cs_bill_addr_sk = ca.ca_address_sk
    AND ca.ca_gmt_offset = -8
  GROUP BY
    i.i_item_id
), ws AS (
  SELECT
    i.i_item_id,
    SUM(ws.ws_ext_sales_price) AS total_sales
  FROM web_sales AS ws
  CROSS JOIN date_dim AS d
  CROSS JOIN customer_address AS ca
  CROSS JOIN item AS i
  WHERE
    i.i_item_id IN (
      SELECT
        i_item_id
      FROM item
      WHERE
        i_color IN ('orchid', 'chiffon', 'lace')
    )
    AND ws.ws_item_sk = i.i_item_sk
    AND ws.ws_sold_date_sk = d.d_date_sk
    AND d.d_year = 2000
    AND d.d_moy = 1
    AND ws.ws_bill_addr_sk = ca.ca_address_sk
    AND ca.ca_gmt_offset = -8
  GROUP BY
    i.i_item_id
)
SELECT
  i_item_id,
  SUM(total_sales) AS total_sales
FROM (
  SELECT
    *
  FROM ss
  UNION ALL
  SELECT
    *
  FROM cs
  UNION ALL
  SELECT
    *
  FROM ws
) AS tmp1
GROUP BY
  i_item_id
ORDER BY
  total_sales,
  i_item_id
LIMIT 100
