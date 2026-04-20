-- PERF_0005 source SQL.
-- Frozen from TPC-DS query52.tpl with explicit source-layer substitutions:
--   MONTH=11
--   YEAR=2001
--   LIMIT=100
-- No rewrite, validation, result, or plan facts are implied by this source freeze.

select
    dt.d_year,
    item.i_brand_id as brand_id,
    item.i_brand as brand,
    sum(store_sales.ss_ext_sales_price) as ext_price
from date_dim dt,
     store_sales,
     item
where dt.d_date_sk = store_sales.ss_sold_date_sk
  and store_sales.ss_item_sk = item.i_item_sk
  and item.i_manager_id = 1
  and dt.d_moy = 11
  and dt.d_year = 2001
group by
    dt.d_year,
    item.i_brand,
    item.i_brand_id
order by
    dt.d_year,
    ext_price desc,
    brand_id
limit 100;
