set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_perf_0033_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
-- PERF_0033 source SQL.
-- Frozen from TPC-DS query55.tpl via repaired repo-local dsqgen:
--   COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi
-- PostgreSQL normalization only replaces TOP 100 with LIMIT 100.

select
    i.i_brand_id as brand_id,
    i.i_brand as brand,
    sum(ss.ss_ext_sales_price) as ext_price
from date_dim d,
     store_sales ss,
     item i
where d.d_date_sk = ss.ss_sold_date_sk
  and ss.ss_item_sk = i.i_item_sk
  and i.i_manager_id = 36
  and d.d_moy = 12
  and d.d_year = 2001
group by i.i_brand, i.i_brand_id
order by ext_price desc, i.i_brand_id
limit 100;
rollback;
