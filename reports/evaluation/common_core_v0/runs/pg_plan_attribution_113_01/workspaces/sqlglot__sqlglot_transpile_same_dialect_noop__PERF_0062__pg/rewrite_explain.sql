set search_path to attr113_sqlglot_sqlglot_transpile_same_dialect_noop_perf_006;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
/* PERF_0062 source SQL. */ /* Frozen from TPC-DS query_templates/query13.tpl via repaired repo-local dsqgen: */ /*   COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi */
SELECT
  AVG(ss_quantity),
  AVG(ss_ext_sales_price),
  AVG(ss_ext_wholesale_cost),
  SUM(ss_ext_wholesale_cost)
FROM store_sales, store, customer_demographics, household_demographics, customer_address, date_dim
WHERE
  s_store_sk = ss_store_sk
  AND ss_sold_date_sk = d_date_sk
  AND d_year = 2001
  AND (
    (
      ss_hdemo_sk = hd_demo_sk
      AND cd_demo_sk = ss_cdemo_sk
      AND cd_marital_status = 'D'
      AND cd_education_status = '2 yr Degree'
      AND ss_sales_price BETWEEN 100.00 AND 150.00
      AND hd_dep_count = 3
    )
    OR (
      ss_hdemo_sk = hd_demo_sk
      AND cd_demo_sk = ss_cdemo_sk
      AND cd_marital_status = 'S'
      AND cd_education_status = 'Secondary'
      AND ss_sales_price BETWEEN 50.00 AND 100.00
      AND hd_dep_count = 1
    )
    OR (
      ss_hdemo_sk = hd_demo_sk
      AND cd_demo_sk = ss_cdemo_sk
      AND cd_marital_status = 'W'
      AND cd_education_status = 'Advanced Degree'
      AND ss_sales_price BETWEEN 150.00 AND 200.00
      AND hd_dep_count = 1
    )
  )
  AND (
    (
      ss_addr_sk = ca_address_sk
      AND ca_country = 'United States'
      AND ca_state IN ('CO', 'IL', 'MN')
      AND ss_net_profit BETWEEN 100 AND 200
    )
    OR (
      ss_addr_sk = ca_address_sk
      AND ca_country = 'United States'
      AND ca_state IN ('OH', 'MT', 'NM')
      AND ss_net_profit BETWEEN 150 AND 300
    )
    OR (
      ss_addr_sk = ca_address_sk
      AND ca_country = 'United States'
      AND ca_state IN ('TX', 'MO', 'MI')
      AND ss_net_profit BETWEEN 50 AND 250
    )
  );
rollback;
