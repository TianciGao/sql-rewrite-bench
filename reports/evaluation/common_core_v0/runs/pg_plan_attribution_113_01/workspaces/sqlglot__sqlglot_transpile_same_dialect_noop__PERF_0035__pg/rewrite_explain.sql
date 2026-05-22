set search_path to attr113_sqlglot_sqlglot_transpile_same_dialect_noop_perf_003;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
/* PERF_0035 source SQL. */ /* Frozen from TPC-DS query57.tpl via repaired repo-local dsqgen: */ /*   COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi */ /* PostgreSQL normalization only replaces TOP 100 with LIMIT 100. */
WITH v1 AS (
  SELECT
    i.i_category,
    i.i_brand,
    cc.cc_name,
    d.d_year,
    d.d_moy,
    SUM(cs.cs_sales_price) AS sum_sales,
    AVG(SUM(cs.cs_sales_price)) OVER (PARTITION BY i.i_category, i.i_brand, cc.cc_name, d.d_year) AS avg_monthly_sales,
    RANK() OVER (PARTITION BY i.i_category, i.i_brand, cc.cc_name ORDER BY d.d_year, d.d_moy) AS rn
  FROM item AS i, catalog_sales AS cs, date_dim AS d, call_center AS cc
  WHERE
    cs.cs_item_sk = i.i_item_sk
    AND cs.cs_sold_date_sk = d.d_date_sk
    AND cc.cc_call_center_sk = cs.cs_call_center_sk
    AND (
      d.d_year = 2000
      OR (
        d.d_year = 2000 - 1 AND d.d_moy = 12
      )
      OR (
        d.d_year = 2000 + 1 AND d.d_moy = 1
      )
    )
  GROUP BY
    i.i_category,
    i.i_brand,
    cc.cc_name,
    d.d_year,
    d.d_moy
), v2 AS (
  SELECT
    v1.cc_name,
    v1.d_year,
    v1.d_moy,
    v1.avg_monthly_sales,
    v1.sum_sales,
    v1_lag.sum_sales AS psum,
    v1_lead.sum_sales AS nsum
  FROM v1, v1 AS v1_lag, v1 AS v1_lead
  WHERE
    v1.i_category = v1_lag.i_category
    AND v1.i_category = v1_lead.i_category
    AND v1.i_brand = v1_lag.i_brand
    AND v1.i_brand = v1_lead.i_brand
    AND v1.cc_name = v1_lag.cc_name
    AND v1.cc_name = v1_lead.cc_name
    AND v1.rn = v1_lag.rn + 1
    AND v1.rn = v1_lead.rn - 1
)
SELECT
  *
FROM v2
WHERE
  d_year = 2000
  AND avg_monthly_sales > 0
  AND CASE
    WHEN avg_monthly_sales > 0
    THEN ABS(sum_sales - avg_monthly_sales) / avg_monthly_sales
    ELSE NULL
  END > 0.1
ORDER BY
  sum_sales - avg_monthly_sales,
  nsum
LIMIT 100;
rollback;
